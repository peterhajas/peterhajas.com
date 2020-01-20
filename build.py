import os, sys
import markdown
from datetime import datetime
from pathlib import Path
import shutil

# Where to save contents
output_path_string = "out"
# Files to ignore for the site
# If a file matches these or contains any components that match these, then it
# is skipped. Additionally, all hidden files are skipped
ignore_files = ["before.html", "after.html", "build", "build.py", "deploy", "out", "readme.md", "repo_tools", "repo_setup", "rss_before.xml", "rss_after.xml", "tags"]
# The markdown extensions to use
# - tables gives MMD-style tables
# - smarty gives smartypants-style quotes
markdown_extensions = ["tables", "smarty"]

# The before.html / after.html files
before_html = Path("before.html").read_text()
after_html = Path("after.html").read_text()

output_path = Path(output_path_string)

class MarkdownFile:
    # The title associated with this file, or None if it has none
    title = None
    # The date associated with this file, or None if it has none
    date = None
    # The contents associated with this file
    contents = ""

    def metadata(self):
        lines = self.contents.split("\n")
        # If this markdown file doesn't have 5 or more lines, it is missing its
        # metadata
        if len(lines) < 5:
            return None
        # If the second line isn't an HTML comment, this has no metadata
        if lines[1] != "<!--":
            return None
        # If the fifth line isn't an ending comment, this has no metadata
        if lines[4] != "-->":
            return None
        # OK, so now lines[2] has our title and lines[3] has our date string
        title = lines[2]
        date_string = lines[3]
        date = datetime.strptime(date_string, "%Y%m%d %H:%M")
        return { "date" : date, "title" : title }

    def __init__(self, contents):
        self.contents = contents
        metadata = self.metadata()
        if metadata != None:
            self.title = metadata["title"]
            self.date = metadata["date"]

    # A pretty-formatted date for self
    def pretty_date(self):
        return self.date.strftime("%B %e, %Y") 

    # Just the HTML for this entry
    def html(self):
        return markdown.markdown(self.contents, extensions=markdown_extensions)

    # HTML that can stand alone
    def page_html(self):
        # The page html is the html, but with:
        # - before before it
        # - after after it
        # - the date and title replaced (if the page has one)
        html = self.html()
        page_html = before_html + html + after_html
        if self.title != None:
            page_html = page_html.replace("TITLE_HERE", self.title)
        else:
            page_html = page_html.replace("TITLE_HERE", "")
        if self.date != None:
            page_html = page_html.replace("DATE_HERE", self.pretty_date())
        else:
            page_html = page_html.replace("DATE_HERE", "")
        return page_html

# Delete the current path
# pathlib will only delete empty directories, so we use shutil
shutil.rmtree(output_path_string)

# Make the new path
output_path.mkdir(parents=True, exist_ok=True)

# Process the site. We'll look for all the files in our tree
all_file_paths = sorted(Path().rglob("*"))
for path in all_file_paths:
    # If the path is ignored, then we can skip it
    if path.is_dir():
        print("{} is dir, skipping".format(path))
        continue
    is_ignored = False
    parts = path.parts
    for part in parts:
        if part[0] == ".":
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
        markdownFile = MarkdownFile(path.read_text())
        # Change output path to .html
        path_outpath = path_outpath.with_suffix(".html")
        path_outpath.parent.mkdir(parents=True, exist_ok=True)
        path_outpath.write_text(markdownFile.page_html())
    # Otherwise, just copy it over
    else:
        file_bytes = path.read_bytes()
        path_outpath.parent.mkdir(parents=True, exist_ok=True)
        path_outpath.write_bytes(file_bytes)
        
