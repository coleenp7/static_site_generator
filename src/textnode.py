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
        
