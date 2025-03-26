from enum import Enum
from htmlnode import *
from independent_functions import *

class TextType(Enum):

    NORMAL = "Normal text"
    BOLD = "**Bold text**"
    ITALIC = "_Italic text_"
    CODE = "`Code text`"
    LINKS = "Links, in this format: [anchor text](url)"
    IMAGES = "Images, in this format: ![alt text](url)"

class BlockType(Enum):
    PARAGRAPH = "Paragraph"
    HEADING = "Headings start with 1-6 # characters, followed by a space and then the heading text"
    CODE = "Code blocks must start with 3 backticks and end with 3 backticks"
    QUOTE = "Every line in a quote block must start with a > character."
    UNORDERED_LIST = "Every line in an unordered list block must start with a - character, followed by a space."
    ORDERED_LIST = "Every line in an ordered list block must start with a number followed by a . character and a space. The number must start at 1 and increment by 1 for each line."

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text 
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type.value == other.text_type.value and self.url == other.url:
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
    def text_node_to_html_node(self):
        if not isinstance(self.text_type, TextType):
            raise Exception("Invalid text type in textnode")
        elif self.text_type == TextType.LINKS:
            return LeafNode("a", self.text, {"href": self.url})
        elif self.text_type == TextType.IMAGES:
            return LeafNode("img", "", {"src":self.url, "alt": self.text})
        elif self.text_type == TextType.NORMAL:
            return LeafNode(None, self.text)
        elif self.text_type == TextType.BOLD:
            return LeafNode("b", self.text)
        elif self.text_type == TextType.ITALIC:
            return LeafNode("i", self.text)
        elif self.text_type == TextType.CODE:
            return LeafNode("code", self.text)
        else:
            raise Exception("error in conversion")
        
