#!/usr/bin/env python3

import os, sys
from datetime import datetime
import time
from pathlib import Path
import shutil
import http.server
import socketserver
import socket
import threading

from markdownfile import *
from file_utils import *
from constants import *

# Where to read contents
input_path_string = "site"
input_path = Path(input_path_string)

# Where to save contents
output_path_string = "out"

output_path = Path(output_path_string)
index_output_path = output_path.joinpath("index.html")
roll_output_path = output_path.joinpath("roll.html")
rss_output_path = output_path.joinpath("rss.xml")

# Command line arguments

# live - turns on live-reloading
live_reloading = "live" in sys.argv
if live_reloading:
    print("turning on live reloading")
# serve - turns on http serving
# we'll do this after we build
serve = "serve" in sys.argv

class SiteEnvironment:
    # The output root path (e.g. `.../out/`
    output_root = None
    # The input root path (e.g. `.../site/`)
    input_root = None
    # The html to insert before page contents
    before_html = ""
    # The html to insert after page contents
    after_html = ""

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
    environment.input_root = input_path
    environment.before_html = before_html
    environment.after_html = after_html

    # Make the new path
    output_path.mkdir(parents=True, exist_ok=True)

    # Keep track of dated markdown entries
    dated_markdown_files = [ ]

    # Process the site. We'll look for all the files in our tree
    all_file_paths = sorted(input_path.rglob("*"))
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
        path_outpath = output_path.joinpath(path.relative_to(input_path))
        
        # If the path is markdown or php, process it
        if path.suffix == '.md' or path.suffix == '.php':
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

def build_continuously_inner():
    build_website()
    time.sleep(0.1)
    build_continuously()

def build_continuously():
    thread = threading.Thread(target=build_continuously_inner)
    thread.daemon = True
    thread.start()

def start_serving():
    port_number = 8000
    print("serving at localhost:{}".format(port_number))
    http_handler = PeterHTTPRequestHandlerHandler
    httpd = socketserver.TCPServer(("", port_number), http_handler)
    httpd.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()
    return httpd

# clean the site
clean_website()

# if we have live_reloading and serve on, this indicates we should be in an
# interactive reloading mode
interactive = live_reloading and serve

if interactive:
    # Serve
    server = start_serving()
    # and then build in a loop
    build_continuously()
    # keep the script around until we get some input
    command = input('')
    print('terminating...')
    server.shutdown()
    quit()
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
