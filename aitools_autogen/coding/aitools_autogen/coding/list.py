

# Next, we create the `List` class for generating lists.


# filename: aitools_autogen/coding/list.py

class List:
    def __init__(self, items, ordered=False):
        self.items = items
        self.ordered = ordered

    def generate(self):
        list_tag = "ol" if self.ordered else "ul"
        list_items = "".join([f"<li>{item}</li>" for item in self.items])
        return f"<{list_tag}>{list_items}</{list_tag}>"