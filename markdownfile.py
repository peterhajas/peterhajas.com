import markdown
from pathlib import Path
from datetime import datetime
import time

from file_utils import *
from constants import *

# The markdown extensions to use
# - meta lets us read metadata
# - tables gives MMD-style tables
# - smarty gives smartypants-style quotes
# - toc gives us a table of contents
markdown_extensions = ['meta', 'tables', 'smarty', 'toc']
markdown_parser = markdown.Markdown(extensions = markdown_extensions)

# A class representing a markdown / html / php file on the site
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
        if 'title' in metadata.keys():
            self.title = metadata['title'][0]
        if 'emoji' in metadata.keys():
            self.emoji = metadata['emoji'][0]
        if 'date' in metadata.keys():
            date_string = metadata["date"][0]
            self.date = datetime.strptime(date_string, "%Y%m%d %H:%M")

    def suffix(self, contents_path):
        if contents_path.suffix == '.php':
            return '.php'
        return '.html'

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
            self.export_path = self.environment.output_root.joinpath(contents_path.relative_to(self.environment.input_root)).with_suffix(self.suffix(contents_path))
        self.prepare_metadata_and_html()

    # A pretty-formatted date for self
    def pretty_date(self):
        return self.date.strftime("%B %e, %Y") 

    # Returns whether or not we are an article
    def is_article(self):
        return self.emoji is not None or self.date is not None

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
            return self.export_path.stem.replace('_',' ').capitalize()
            
    def article_prefix(self):
        prefix = ""
        if self.title is not None:
            prefix += "<div class='title'><a href='{}'>{}</a></div>\n".format(self.rendered_path(), self.title)
        if self.date is not None and self.emoji is not None:
            prefix += "<div class='article_subhead'>{}  •  {}</div>\n".format(self.pretty_date(), self.emoji)
        elif self.date is not None:
            prefix += "<div class='article_subhead'>{}</div>\n".format(self.pretty_date())
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

