from io import BytesIO, StringIO
import requests
import shutil
from PIL import Image
import os

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import json

# Download the images from the urls
with open(os.path.relpath("../garfield.jl")) as input_file:
    for line in input_file:
        image = json.loads(line)["image"]
        image_name = image.split("/")[-1]

        r = requests.get(image, stream=True)

        if r.status_code == 200:
            i = Image.open(BytesIO(r.content))
            # convert gif to jpeg
            if i.format == "GIF":
                i.convert("RGB").save("../images/" + image_name[:-4] + ".jpg", "JPEG")
