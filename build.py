#!/usr/bin/env python3

import os, sys
import markdown
from datetime import datetime
import time
from pathlib import Path
import shutil
import http.server
import socketserver
import threading

# Where to save contents
output_path_string = "out"
# Files to ignore for the site
# If a file matches these or contains any components that match these, then it
# is skipped. Additionally, all hidden files are skipped as are vim undo files
ignore_files = ["before.html", "after.html", "build", "build.py", "deploy", "out", "image_process.py", "readme.md", "repo_tools", "repo_setup", "rss_before.xml", "rss_after.xml", "tags", "tags.lock", "tags.temp", "template.md", "blurb.html", "favicon.afdesign", "apple-touch-icon.afdesign"]
# The markdown extensions to use
# - meta lets us read metadata
# - tables gives MMD-style tables
# - smarty gives smartypants-style quotes
markdown_extensions = ["meta", "tables", "smarty"]
markdown_parser = markdown.Markdown(extensions = markdown_extensions)

output_path = Path(output_path_string)
index_output_path = output_path.joinpath("index.html")
roll_output_path = output_path.joinpath("roll.html")
rss_output_path = output_path.joinpath("rss.xml")

# Command line arguments
extra_head_marker = "<!--EXTRA_HEAD_CONTENT_HERE-->"
rss_redacted_content = "<p><center>Content unavailable in RSS feed</center></p>"

# live - turns on live-reloading
live_reloading = "live" in sys.argv
if live_reloading:
    print("turning on live reloading")
# serve - turns on http serving
# we'll do this after we build
serve = "serve" in sys.argv

# Writes the proposed bytes to path if they haven't changed
def copy_file_to_path_if_different(source, destination):
    do_simple_copy = True
    if destination.exists():
        destination_bytes = None
        if destination.exists():
            destination_bytes = destination.read_bytes()
        if destination_bytes != None:
            source_bytes = source.read_bytes()
            if source_bytes == destination_bytes:
                do_simple_copy = False

    if do_simple_copy:
        shutil.copyfile(source, destination)

# Writes the proposed text to path if they haven't changed
def write_text_to_path_if_different(text_to_write, path):
    existing_text = None
    if path.exists():
        existing_text = path.read_text(encoding='utf8')
    if existing_text != text_to_write:
        path.write_text(text_to_write, encoding='utf8')

class SiteEnvironment:
    # The output root path (e.g. `.../out/`
    output_root = None
    # The html to insert before page contents
    before_html = ""
    # The html to insert after page contents
    after_html = ""

# A class representing a markdown file in the site
class MarkdownFile:
    # The title associated with this file, or None if it has none
    title = None
    # The date associated with this file, or None if it has none
    date = None
    # The emoji associated with this file, or None if it has none
    emoji = None
    # The contents associated with this file
    contents = ""
    # The HTML associated with this file
    html = None
    # The path to export this file to, or None if it has none
    export_path = None
    # The site environment to build this page with
    environment = None

    def prepare_metadata_and_html(self):
        # Process our HTML and metadata
        self.html = markdown_parser.convert(self.contents)
        metadata = markdown_parser.Meta
        # If we do have a metadata dictionary, we have no metadata
        if len(metadata.keys()) == 0:
            return
        # Otherwise, populate our metadata
        self.title = metadata["title"][0]
        self.emoji = metadata["emoji"][0]

        date_string = metadata["date"][0]
        self.date = datetime.strptime(date_string, "%Y%m%d %H:%M")

    # contents_path: Path or None
    # export_path: Path or None
    # contents: String or None
    # Pass contents_path and then export_path and contents will be inferred
    # Pass contents and export_path to be able to save
    def __init__(self, environment, contents_path=None, export_path=None, contents=None):
        self.environment = environment
        self.contents = contents
        self.export_path = export_path
        if contents_path != None:
            self.contents = contents_path.read_text(encoding='utf8')
            self.export_path = self.environment.output_root.joinpath(contents_path).with_suffix(".html")
        self.prepare_metadata_and_html()

    # A pretty-formatted date for self
    def pretty_date(self):
        return self.date.strftime("%B %e, %Y") 

    # Returns whether or not we are an article
    def is_article(self):
        return self.title != None and self.date != None

    # An RSS-formatted date for self
    def rss_date(self):
        # Always PST :-/
        # From python:
        # "For a naive object, the %z and %Z format codes are replaced by empty strings."
        return self.date.strftime("%a, %d %b %Y %H:%M:%S PST")

    # The page title, with prequel, for self
    def page_title(self):
        if self.title != None:
            return self.title
        else:
            return self.export_path.stem.capitalize()
            
    def article_prefix(self):
        prefix = ""
        prefix += "<div class='title'><a href='{}'>{}</a></div>\n".format(self.rendered_path(), self.title)
        prefix += "<div class='article_subhead'>{}  •  {}</div>\n".format(self.pretty_date(), self.emoji)
        return prefix

    # The decorated HTML for this entry, wrapped in <article> and with title /
    # date if appropriate
    def decorated_html(self):
        # The decorated html is:
        # - the <article> entry if we are an article
        # - the title and date if we are an article
        # - the html
        # - the </article> entry if we are an article

        is_article = self.is_article()
        decorated = ""
        if is_article:
            decorated += "<article>\n"
            decorated += self.article_prefix()
            decorated += "</div>\n"
        decorated += self.html + "\n"
        if is_article:
            decorated += "</article>\n"
        return decorated

    # HTML that is its own document
    def page_html(self):
        # The page html is:
        # - before.html
        # - the decorated html
        # - after.html

        page_html = self.environment.before_html + "\n"
        page_html += self.decorated_html()
        page_html += self.environment.after_html

        # replace the title
        page_html = page_html.replace("TITLE_FOR_PAGE_HERE", self.page_title())

        return page_html

    # The path this file is rendered to in the site
    # For example, /about.html, /blog/some_post.html, etc.
    def rendered_path(self):
        relative = self.export_path.relative_to(self.environment.output_root)
        return Path("/").joinpath(relative)

    # The absolute URL where this file is available.
    # For example, http://peter.haj.as/about.html, http://peter.haj.as/blog/some_post.html, etc.
    def rendered_url(self):
        return 'http://peter.haj.as' + str(self.rendered_path())

    # The index item for this page 
    def index_item(self):
    	return self.article_prefix()

    # The HTML to use for the RSS feed
    def rss_html(self):
        html_for_rss = self.html
        # Strip out any RSS ignored stuff
        while 'RSS_IGNORE_START' in html_for_rss:
            lines = html_for_rss.split('\n')
            start_index = None
            end_index = None
            for line_index in range(len(lines)):
                line = lines[line_index]
                if 'RSS_IGNORE_START' in line:
                    start_index = line_index
                if 'RSS_IGNORE_END' in line:
                    end_index = line_index
            if start_index != None and end_index != None:
                # Remove at start and end
                lines[start_index:end_index+1] = [rss_redacted_content]
                html_for_rss = '\n'.join(lines)

        return html_for_rss

    # The RSS item for this page
    def rss_item(self):
        return """<item>
<title>{}</title>
<guid>{}</guid>
<link>{}</link>
<pubDate>{}</pubDate>
<description><![CDATA[
{}
]]></description>
        </item>""".format(self.title, self.rendered_path(), self.rendered_url(), self.rss_date(), self.rss_html())

    # Renders the file to its output location
    # Returns the path that we wrote to
    def render(self):
        self.export_path.parent.mkdir(parents=True, exist_ok=True)
        write_text_to_path_if_different(self.page_html(), self.export_path)
        return self.export_path

# Builds the website
def build_website():
    # The before.html / after.html files
    before_html = Path("before.html").read_text(encoding='utf8')
    after_html = Path("after.html").read_text(encoding='utf8')

    # The rss_before.xml and rss_after.xml files
    rss_before_xml = Path("rss_before.xml").read_text(encoding='utf8')
    rss_after_xml = Path("rss_after.xml").read_text(encoding='utf8')

    # The blurb markdown file
    blurb = Path("blurb.html").read_text(encoding='utf8')

    if live_reloading:
        live_js_head = '<script type="text/javascript" src="http://livejs.com/live.js"></script>' + '\n' + extra_head_marker
        before_html = before_html.replace(extra_head_marker, live_js_head)

    # Build our environment
    environment = SiteEnvironment()
    environment.output_root = output_path
    environment.before_html = before_html
    environment.after_html = after_html

    # Make the new path
    output_path.mkdir(parents=True, exist_ok=True)

    # Keep track of dated markdown entries
    dated_markdown_files = [ ]

    # Process the site. We'll look for all the files in our tree
    all_file_paths = sorted(Path().rglob("*"))
    for path in all_file_paths:
        # If the path is ignored, then we can skip it
        if path.is_dir():
            continue
        is_ignored = False
        parts = path.parts
        for part in parts:
            if part[0] == "." or part[-1] == "~":
                is_ignored = True
                break
            if part in ignore_files:
                is_ignored = True
                break
        if is_ignored:
            continue

        path_outpath = output_path.joinpath(path)
        
        # If the path is markdown, process it
        if path.suffix == ".md":
            markdownFile = MarkdownFile(environment, contents_path=path)
            path_outpath = markdownFile.render()
            # If the file has a date, add it to our list of dated entries
            if markdownFile.date != None:
                dated_markdown_files.append(markdownFile)
        # Otherwise, just copy it over if it hasn't changed
        else:
            path_outpath.parent.mkdir(parents=True, exist_ok=True)
            copy_file_to_path_if_different(path, path_outpath)

    # Sort dated markdown files by date
    sorted_dated_markdown_files = sorted(dated_markdown_files, key=lambda entry: entry.date)
    # Reverse the list (so it is newest first)
    sorted_dated_markdown_files.reverse()

    index_markdown_contents = ""
    roll_markdown_contents = ""

    if blurb != None:
        index_markdown_contents = blurb
        roll_markdown_contents = blurb

    rss_contents = rss_before_xml
    # Build the index, roll, and rss files
    for entry in sorted_dated_markdown_files:
        # Index: add index item
        index_markdown_contents += entry.index_item()
        index_markdown_contents += "\n"
        
        # Roll: add in contents
        roll_markdown_contents += entry.decorated_html()
        roll_markdown_contents += "\n"

        # RSS: add in item RSS contents
        rss_contents += entry.rss_item()
    
    index_markdown = MarkdownFile(environment, export_path=index_output_path, contents=index_markdown_contents)
    index_markdown.environment = environment
    index_path = index_markdown.render()
    
    roll_markdown = MarkdownFile(environment, export_path=roll_output_path, contents=roll_markdown_contents)
    roll_markdown.environment = environment
    roll_path = roll_markdown.render()

    rss_contents += rss_after_xml
    write_text_to_path_if_different(rss_contents, rss_output_path)

    # Now, let's see how large the site is
    all_file_paths = sorted(output_path.rglob("*"))
    site_size_bytes = 0
    for path in all_file_paths:
        site_size_bytes += path.stat().st_size

    return site_size_bytes

def clean_website():
    # Delete the current path
    # pathlib will only delete empty directories, so we use shutil
    shutil.rmtree(output_path_string, ignore_errors=True)

class PeterHTTPRequestHandlerHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=output_path_string, **kwargs)

def start_serving():
    port_number = 8000
    print("serving at localhost:{}".format(port_number))
    http_handler = PeterHTTPRequestHandlerHandler
    httpd = socketserver.TCPServer(("", port_number), http_handler)
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()

# clean the site
clean_website()

# if we have live_reloading and serve on, this indicates we should be in an
# interactive reloading mode
interactive = live_reloading and serve

if interactive:
    # Serve
    start_serving()
    # and then build in a loop
    while True:
        build_website()
        time.sleep(0.1)
    while True:
        time.sleep(1)
else:
    # Otherwise, build the site and log the time it took
    start_time = time.time()
    site_size_bytes = build_website()
    end_time = time.time()

    elapsed = end_time - start_time
    print("built in {0:.2f}s".format(elapsed))
    print("site is {0:.2f}MB".format(site_size_bytes / 1000000))

    # if we were asked to serve the site, then do so
    if serve:
        start_serving()
