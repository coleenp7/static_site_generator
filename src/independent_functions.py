import re
from textnode import *
from htmlnode import *

#splits nodes based on a specified delimiter rather than just spaces
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

# def split_nodes_delimiter(old_nodes, delimiter, text_type):
#     new_nodes = []
#     for old_node in old_nodes:
#         if old_node.text_type != TextType.NORMAL:
#             new_nodes.append(old_node)
#             continue
#         split_nodes = []
#         sections = old_node.text.split(delimiter)
#         if len(sections) % 2 == 0:
#             raise ValueError("invalid markdown, formatted section not closed")
#         for i in range(len(sections)):
#             if sections[i] == "":
#                 continue
#             if i % 2 == 0:
#                 split_nodes.append(TextNode(sections[i], TextType.NORMAL))
#             else:
#                 split_nodes.append(TextNode(sections[i], text_type))
#         new_nodes.extend(split_nodes)
#     return new_nodes

#finds all the markdown stuff for images, a special case
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

#finds all the markdown stuff for links, a special case
def extract_markdown_links(text):
    return (re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text))

# #handles images by splitting the data into usaable nodes
# def split_nodes_image(old_nodes):
#     returnable = []
#     for node in old_nodes:
#         if node.text_type != TextType.NORMAL:
#             if not node.text:
#                 returnable.append(node)
#         else:
#             image_tuples = [(a, l) for a, l in extract_markdown_images(node.text)]
#             for image_alt, image_link in image_tuples:
#                 # Split into two parts: before the image, and after the image
#                 sections = node.text.split(f"![{image_alt}]({image_link})", 1)

#                 # Step 1: Add the 'before' text as a TextNode (if it's non-empty)
#                 if sections[0]:
#                     returnable.append(TextNode(sections[0], TextType.NORMAL))

#                 # Step 2: Add the image as its own TextNode
#                 returnable.append(TextNode(image_alt, TextType.IMAGES, image_link))

#                 # Step 3: Update the remaining text to continue processing
#                 node.text = sections[1]  # Only the part after the image
#             return returnable

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGES,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.NORMAL))
    return new_nodes

#handles links by splitting the data into usaable nodes
# def split_nodes_link(old_nodes):
#     returnable = []
#     for node in old_nodes:
#         if node.text_type != TextType.NORMAL:
#             if not node.text:
#                 returnable.append(node)
#         else:
#             image_tuples = [(a, l) for a, l in extract_markdown_links(node.text)]
#             for link_text, link in image_tuples:
#                 # Split into two parts: before the image, and after the image
#                 sections = node.text.split(f"![{link_text}]({link})", 1)

#                 # Step 1: Add the 'before' text as a TextNode (if it's non-empty)
#                 if sections[0]:
#                     returnable.append(TextNode(sections[0], TextType.NORMAL))

#                 # Step 2: Add the image as its own TextNode
#                 returnable.append(TextNode(link_text, TextType.LINKS, link))

#                 # Step 3: Update the remaining text to continue processing
#                 node.text = sections[1]  # Only the part after the image
#             return returnable

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))
            new_nodes.append(TextNode(link[0], TextType.LINKS, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.NORMAL))
    return new_nodes

#converts raw text into nodes that can be worked on by other methods        
def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.NORMAL)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

#turns markdown into useable blocks
def markdown_to_blocks(markdown):
    results = []
    markdown = markdown.strip() 
    temp = temp = markdown.split("\n\n")
    for string in temp:
        var = "\n".join([line.strip() for line in string.splitlines()])
        if var:
            results.append(var)

    return results

#adds block type specifications for later use
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

#changes markdown to HTML nodes
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

#turns a single markdown block into a useable HTML node
def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")

#addresses child noding after markdown
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

#processes paragraph blocks
def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

#processes heading blocks
def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

#processes code blocks
def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[3:-3]
    raw_text_node = TextNode(text, TextType.NORMAL)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

#processes ordered lists
def ordered_list_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        if children:
            html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

#processes unordered lists
def unordered_list_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        if children:
            html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

#processes quotes
def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines or []:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.NORMAL:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINKS:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGES:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"invalid text type: {text_node.text_type}")
