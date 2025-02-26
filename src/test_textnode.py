import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_text(self):
        node = TextNode("This is a plain text node", TextType.NORMAL)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a plain text node")

    def test_links(self):
        node = TextNode("This is a link test node", TextType.LINKS, "boot.dev")
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link test node")

    def test_images(self):
        node = TextNode("Alt text", TextType.IMAGES, "www.boot.dev/image.png")
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "www.boot.dev/image.png")
        self.assertEqual(html_node.props["alt"], "Alt text")

    def test_no_delimiter(self):
        node = TextNode("Hello world", TextType.NORMAL)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        assert len(nodes) == 1
        assert nodes[0].text == "Hello world"
        assert nodes[0].text_type == TextType.NORMAL

    def test_basic_split(self):
        nodes = [TextNode("hello `world` today", TextType.NORMAL)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        assert len(result) == 3
        assert result[0].text == "hello "
        assert result[0].text_type == TextType.NORMAL
        assert result[1].text == "world"
        assert result[1].text_type == TextType.CODE
        assert result[2].text == " today"
        assert result[2].text_type == TextType.NORMAL
    
    def test_multiple_delimiter(self):
        nodes = [TextNode("hello `world` and `python`", TextType.NORMAL)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        assert len(result) == 5
        assert result[0].text == "hello "
        assert result[0].text_type == TextType.NORMAL
        assert result[1].text == "world"
        assert result[1].text_type == TextType.CODE
        assert result[2].text == " and "
        assert result[2].text_type == TextType.NORMAL
        assert result[3].text == "python"
        assert result[3].text_type == TextType.CODE
        assert result[4].text == ""
        assert result[4].text_type == TextType.NORMAL

    def test_empty_content(self):
        nodes = [TextNode("hello `` world", TextType.NORMAL)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        assert len(result) == 3
        assert result[0].text == "hello "
        assert result[0].text_type == TextType.NORMAL
        assert result[1].text == ""
        assert result[1].text_type == TextType.CODE
        assert result[2].text == " world"
        assert result[2].text_type == TextType.NORMAL

    def test_double_delimiter(self):
        nodes = [TextNode("hello **cruel** world", TextType.NORMAL)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        assert len(result) == 3
        assert result[0].text == "hello "
        assert result[0].text_type == TextType.NORMAL
        assert result[1].text == "cruel"
        assert result[1].text_type == TextType.BOLD
        assert result[2].text == " world"
        assert result[2].text_type == TextType.NORMAL

    def test_italics_delimiter(self):
        nodes = [TextNode("hello _fun_ world", TextType.NORMAL)]
        result = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        assert len(result) == 3
        assert result[0].text == "hello "
        assert result[0].text_type == TextType.NORMAL
        assert result[1].text == "fun"
        assert result[1].text_type == TextType.ITALIC
        assert result[2].text == " world"
        assert result[2].text_type == TextType.NORMAL

    def test_multiple_nodes(self):
        nodes = [TextNode("hello _fun_ world", TextType.NORMAL), TextNode("Joy _to_ the world", TextType.NORMAL)]
        result = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        assert len(result) == 6
        assert result[0].text == "hello "
        assert result[0].text_type == TextType.NORMAL
        assert result[1].text == "fun"
        assert result[1].text_type == TextType.ITALIC
        assert result[2].text == " world"
        assert result[2].text_type == TextType.NORMAL
        assert result[3].text == "Joy "
        assert result[3].text_type == TextType.NORMAL
        assert result[4].text == "to"
        assert result[4].text_type == TextType.ITALIC
        assert result[5].text == " the world"
        assert result[5].text_type == TextType.NORMAL

    def test_no_second_delimiter(self):
        nodes = [TextNode("hello _fun world", TextType.NORMAL)]
        with self.assertRaises(Exception):
            split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    def test_incorrect_delimiter(self):
        nodes = [TextNode("hello_ fun world_", TextType.NORMAL)]
        with self.assertRaises(Exception):
            split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def simple_markdown(self):
        text = "![test](example.com)"
        result = extract_markdown_images(text)
        print(result)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
        "This is text with a [link to somewhere](https://example.com)"
        )
        self.assertListEqual([("link to somewhere", "https://example.com")], matches)

if __name__ == "__main__":
    unittest.main()