import textwrap

from IPython.display import Markdown


def to_markdown(text: str):

    """
    Convert given text into markdown format for html rendering

    :param text:
    :return:
    """

    text: str = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))



