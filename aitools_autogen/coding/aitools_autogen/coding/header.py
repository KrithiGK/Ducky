

# Next, we define the `Header` class.


# filename: aitools_autogen/coding/header.py

class Header:
    def __init__(self, text, level=1):
        self.text = text
        self.level = level

    def generate(self):
        return f"<h{self.level}>{self.text}</h{self.level}>"