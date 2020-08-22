# A marker for inserting extra HEAD content
extra_head_marker = "<!--EXTRA_HEAD_CONTENT_HERE-->"

# The text to replace redacted RSS content with
rss_redacted_content = "<p><center>Content unavailable in RSS feed</center></p>"

# Files to ignore for the site
# If a file matches these or contains any components that match these, then it
# is skipped. Additionally, all hidden files are skipped as are vim undo files
ignore_files = ["before.html", "after.html", "build", "build.py", "deploy", "out", "image_process.py", "readme.md", "repo_tools", "repo_setup", "rss_before.xml", "rss_after.xml", "tags", "tags.lock", "tags.temp", "template.md", "blurb.html", "favicon.afdesign", "apple-touch-icon.afdesign", "constants.py", "file_utils.py", "markdownfile.py", "__pycache__"]
