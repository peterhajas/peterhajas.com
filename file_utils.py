from pathlib import Path
import shutil

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
