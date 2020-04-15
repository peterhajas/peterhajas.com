#!/usr/bin/env python3

from pathlib import Path
from PIL import Image
import sys

# This script accepts an image and strips EXIF / resizes it

should_resize = "r" in sys.argv
biggest_image_width = int(1024)

if should_resize:
    print("will resize")

images = sys.argv[-1]

passed_path = Path(sys.argv[-1])

paths_to_process = sorted(Path(passed_path.parent).glob(passed_path.name))

for path in paths_to_process:
    print("processing {}...".format(path))
    
    # open the image in PIL
    image = Image.open(str(path))
    
    if should_resize:
        image_size = image.size
        if image_size[0] > biggest_image_width:
            print("image has size {}, resizing...".format(image_size))
            scale_factor = biggest_image_width / image_size[0]
            new_image_height = int(image_size[1] * scale_factor)
            new_image_size = (biggest_image_width, new_image_height)
            image = image.resize(new_image_size)
            print("resized to {}".format(new_image_size))
        
    
    image.save(path)
    print("saved {}".format(path))

