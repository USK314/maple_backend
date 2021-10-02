from PIL import Image
from io import BytesIO
import os
import re

COMPRESS_QUALITY = 65


def compress(file_path: str, image_type: str) -> str:
    # check file size
    if os.path.getsize(file_path) < 200000:  # smaller than 200kB
        print("no need to compress: ", file_path,
              os.path.getsize(file_path), "bytes")
        return file_path
    file_name, ext = os.path.splitext(os.path.basename(file_path))
    print(file_name, ext)
    out_path = ""
    with open(file_path, 'rb') as inputfile:
        im = Image.open(inputfile)
        if image_type == "image/png":
            im = im.convert('RGB')
            out_path = re.sub('png$', 'jpg', file_path)
        else:
            out_path = file_path
        im_io = BytesIO()
        im.save(im_io, 'JPEG', quality=COMPRESS_QUALITY)
    os.remove(file_path)
    with open(out_path, mode='wb') as outputfile:
        outputfile.write(im_io.getvalue())
    return out_path

# compress("./景色.jpg", "image/jpeg")
# compress("./a/サムス.jpg", "image/jpeg")
