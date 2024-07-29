import pathlib
import textwrap


import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown


def to_markdown(text: str):
    text: str = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


GOOGLE_API_KEY = ''

genai.configure(api_key=GOOGLE_API_KEY)


model = genai.GenerativeModel('gemini-1.5-flash')

response = model.generate_content("What is the meaning of life?")
