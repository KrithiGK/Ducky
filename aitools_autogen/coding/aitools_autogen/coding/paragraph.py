

# Now, let's define the `Paragraph` class.


# filename: aitools_autogen/coding/paragraph.py

class Paragraph:
    def __init__(self, text):
        self.text = text

    def generate(self):
        return f"<p>{self.text}</p>"