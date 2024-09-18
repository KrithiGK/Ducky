

# Finally, we define the `Link` class.


# filename: aitools_autogen/coding/link.py

class Link:
    def __init__(self, href, text):
        self.href = href
        self.text = text

    def generate(self):
        return f'<a href="{self.href}">{self.text}</a>'