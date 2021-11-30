from io import BytesIO, StringIO
import requests
from PIL import Image
import os
import json

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

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
                i.convert("RGB")

                # first panel
                i1 = i.convert("RGB").crop((0, 0, i.size[0] / 3, i.size[1]))

                i1.save(("../images/" + image_name[:-4] + "_1.jpg"))

                i1.transpose(Image.FLIP_LEFT_RIGHT).save(
                    ("../images/" + image_name[:-4] + "_1_f.jpg")
                )

                # second panel
                i2 = i.convert("RGB").crop(
                    (i.size[0] / 3, 0, i.size[0] / 3 * 2, i.size[1])
                )

                i2.save(("../images/" + image_name[:-4] + "_2.jpg"))

                i2.transpose(Image.FLIP_LEFT_RIGHT).save(
                    ("../images/" + image_name[:-4] + "_2_f.jpg")
                )

                # third panel
                i3 = i.convert("RGB").crop((i.size[0] / 3 * 2, 0, i.size[0], i.size[1]))

                i3.save(("../images/" + image_name[:-4] + "_3.jpg"))

                i3.transpose(Image.FLIP_LEFT_RIGHT).save(
                    ("../images/" + image_name[:-4] + "_3_f.jpg")
                )
