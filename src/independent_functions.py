import re
from textnode import *
from htmlnode import *

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
                    if text:
                        parts.append(TextNode(text, TextType.NORMAL))
                        break
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


def split_nodes_image(old_nodes):
    returnable = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            if not node.text:
                returnable.append(node)
        else:
            image_tuples = [(a, l) for a, l in extract_markdown_images(node.text)]
            for image_alt, image_link in image_tuples:
                # Split into two parts: before the image, and after the image
                sections = node.text.split(f"![{image_alt}]({image_link})", 1)

                # Step 1: Add the 'before' text as a TextNode (if it's non-empty)
                if sections[0]:
                    returnable.append(TextNode(sections[0], TextType.NORMAL))

                # Step 2: Add the image as its own TextNode
                returnable.append(TextNode(image_alt, TextType.IMAGES, image_link))

                # Step 3: Update the remaining text to continue processing
                node.text = sections[1]  # Only the part after the image
            return returnable

def split_nodes_link(old_nodes):
    returnable = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            if not node.text:
                returnable.append(node)
        else:
            image_tuples = [(a, l) for a, l in extract_markdown_links(node.text)]
            for link_text, link in image_tuples:
                # Split into two parts: before the image, and after the image
                sections = node.text.split(f"![{link_text}]({link})", 1)

                # Step 1: Add the 'before' text as a TextNode (if it's non-empty)
                if sections[0]:
                    returnable.append(TextNode(sections[0], TextType.NORMAL))

                # Step 2: Add the image as its own TextNode
                returnable.append(TextNode(link_text, TextType.LINKS, link))

                # Step 3: Update the remaining text to continue processing
                node.text = sections[1]  # Only the part after the image
            return returnable
        
def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.NORMAL)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    results = []
    markdown = markdown.strip() 
    temp = temp = markdown.split("\n\n")
    for string in temp:
        var = "\n".join([line.strip() for line in string.splitlines()])
        if var:
            results.append(var)

    return results

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    if lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.CODE
    
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

'''
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        type = block_to_block_type(block)'
        '''