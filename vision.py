from google.cloud import vision
import io
import os

from firebase import vision_api_cred

def detect_labels(filePath: str) -> str:
    client = vision.ImageAnnotatorClient(credentials=vision_api_cred)
    # Loads the image into memory
    with io.open(filePath, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    if response.error.message:
        print(f'{response.error.message}\nFor more info on error messages, check: '
              'https://cloud.google.com/apis/design/errors')
        # raise Exception(
        #     '{}\nFor more info on error messages, check: '
        #     'https://cloud.google.com/apis/design/errors'.format(
        #         response.error.message))
        return 'unknown'
    res = []
    for label in labels:
        res.append(label.description)
    return ";".join(res[:3])