from enum import Enum
import re
from htmlnode import *

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
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    returnable = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            returnable.append(node)
        else:
            parts = []
            text = node.text
            while True:
                d_start = text.find(delimiter)
                if d_start == -1:
                    parts.append(TextNode(text, TextType.NORMAL))
                    break
                if d_start > 0 and not text[d_start - 1].isspace():
                    raise Exception("Invalid delimiter attached to word")
                before_start = text[0:d_start]
                if before_start.count(delimiter) > 0:
                    raise Exception("Invalid delimiter order")

                d_end = text.find(delimiter, d_start + len(delimiter))
                if d_end == -1:
                    raise Exception("Second delimiter not found")
                
                parts.append(TextNode(text[0:d_start], TextType.NORMAL))
                parts.append(TextNode(text[d_start + len(delimiter):d_end], text_type))
                text = text[d_end + len(delimiter):]
            returnable.extend(parts)
                        
    return returnable

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return (re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text))