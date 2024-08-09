# Imports

import textwrap
import json
import base64
from PIL import Image
from io import BytesIO
import os
from IPython.display import Markdown
from django.core.files.base import ContentFile
from ..models import Complain, Attachment

# End imports 

def to_markdown(text: str):

    """
    Convert given text into markdown format for html rendering

    :param text:
    :return:
    """

    text: str = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


def extract_images(chat_history):
    """
    Extracts image data from chat history and returns a list of tuples containing
    the image object and the file extension.

    :params:
    chat_history: A list of chat messages.

    Returns:
    A list of tuples, each containing a PIL Image object and its file extension.
    """
    images = []
    for message in chat_history:
        for part in message.parts:
            if hasattr(part, 'inline_data'):  # Check if 'inline_data' exists in 'parts'
                inline_data = part.inline_data
                image_data = base64.b64decode(inline_data.data)
                img = Image.open(BytesIO(image_data))

                # Determine the file extension from the MIME type
                mime_type = inline_data.mime_type
                file_extension = mime_type.split('/')[-1]  # Extracts 'jpeg' from 'image/jpeg'

                images.append((img, file_extension))

    return images


def save_images_to_model(images, complaint_obj):

    """
    Store the images to evidence model

    :params:
    images: A list of tuples, each containing a PIL Image object and its file extension.
    """

    for index, (img, file_extension) in enumerate(images):
        # Convert the Image object to a file-like object
        img_io = BytesIO()
        img.save(img_io, format=file_extension.upper())
        img_io.seek(0)

        # Create a ContentFile to store in the ImageField
        file_name = f'image_{index}.{file_extension}'
        image_file = ContentFile(img_io.read(), name=file_name)

        # Save the image to the ChatImage model
        Attachment.objects.create(complain=complaint_obj, file=image_file)


