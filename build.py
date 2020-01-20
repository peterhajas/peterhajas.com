import os, sys
import markdown
from datetime import datetime
from pathlib import Path
import shutil

# Where to save contents
output_path_string = "out"
# The markdown extensions to use
# - tables gives MMD-style tables
# - smarty gives smartypants-style quotes
markdown_extensions = ["tables", "smarty"]
before_html = Path("before.html").read_text()
after_html = Path("after.html").read_text()

output_path = Path(output_path_string)

class MarkdownFile:
    # The title associated with this file, or None if it has none
    title = None
    # The date associated with this file, or None if it has none
    date = None

# Given a Markdown file, returns the metadata for it or None if none exists
def metadata_for_markdown_file_contents(contents):
    lines = contents.split("\n")
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

# Returns a pretty date from a datetime date
def pretty_date(date):
    return date.strftime("%B %e, %Y") 

# Processes the file 
def process_markdown(path, dated):

for path in all_markdown_paths:
    file_contents = path.read_text()
    # Grab the "raw" html
    file_html = markdown.markdown(file_contents, extensions=markdown_extensions)
    # Grab the metadata
    metadata = metadata_for_markdown_file_contents(file_contents)

    # The page html is the file html, but with:
    # - before before it
    # - after after it
    # - the date and title replaced (if the page has one)
    page_html = before_html + file_html + after_html
    if metadata != None:
        page_html = page_html.replace("TITLE_HERE", metadata["title"])
        date_pretty = pretty_date(metadata["date"])
        page_html = page_html.replace("DATE_HERE", date_pretty)
    else:
        page_html = page_html.replace("TITLE_HERE", "")
        page_html = page_html.replace("DATE_HERE", "")

    print(page_html)
    # quit()



# Delete the current path
# pathlib will only delete empty directories, so we use shutil
shutil.rmtree(output_path_string)

# Make the new path
output_path.mkdir(parents=True, exist_ok=True)

# Process the site. We'll look for all the markdown files in our tree
all_markdown_paths = sorted(Path().rglob("*.md"))

# We want to use these to:
# - build the index (sorted by date, included in the file)
# - move the compiled HTML files into the output directory

