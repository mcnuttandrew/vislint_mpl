"""
Lint rules for purely computational rules
"""

import os
try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract


def passes_ledgible_text(axes, fig, config_value):
    """
    lint rule for ledgible-text
    """
    fig.savefig('mlsource.png')
    viewed_text = pytesseract.image_to_string(Image.open('mlsource.png'))
    os.remove('mlsource.png')

    known_text = [x.get_text() for x in axes.get_children() if type(x).__name__ == 'Annotation']
    found_text = [x for x in known_text if x in viewed_text]
    return len(known_text) == len(found_text)
