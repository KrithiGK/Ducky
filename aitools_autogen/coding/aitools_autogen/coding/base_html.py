# To create a utility that generates HTML pages based on the provided OpenAPI 3.0.1 specification, we'll structure our Python code into multiple classes, each responsible for generating a specific part of the HTML page. The classes will be organized as follows:

# 1. **BaseHTML**: Responsible for the basic structure of an HTML page.
# 2. **Header**: Generates the header section of the page.
# 3. **Paragraph**: Handles the creation of paragraphs.
# 4. **List**: Generates unordered and ordered lists.
# 5. **Link**: Handles the creation of hyperlinks.

# Let's start by defining the `BaseHTML` class.


# filename: aitools_autogen/coding/base_html.py

class BaseHTML:
    def __init__(self, title=""):
        self.title = title
        self.body_content = []

    def add_content(self, content):
        self.body_content.append(content)

    def generate(self):
        html_content = f"<!DOCTYPE html>\n<html>\n<head>\n<title>{self.title}</title>\n</head>\n<body>\n"
        for content in self.body_content:
            html_content += content.generate() + "\n"
        html_content += "</body>\n</html>"
        return html_content