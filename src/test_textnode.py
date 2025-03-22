import unittest
from enum import Enum
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("some other text", TextType.ITALIC, "https://www.google.com")
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertIsNotNone(node3.url)
        self.assertIsInstance(node, TextNode)
        self.assertEqual(node.text_type, node2.text_type)
        self.assertNotEqual(node.text, node3.text)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertEqual(html_node.props, None or {})

    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertEqual(html_node.props, None or {})

    def test_code(self):
        node = TextNode("Code text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code text")
        self.assertEqual(html_node.props, None or {})

    def test_link(self):
        node = TextNode("Link text", TextType.LINK, "https://www.example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Link text")
        self.assertIsNotNone(html_node.props)
        self.assertEqual(html_node.props.get("href"), "https://www.example.com")

    def test_image(self):
        node = TextNode("Alt text", TextType.IMAGE, "https://www.example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")  # Value should be empty for images
        self.assertIsNotNone(html_node.props)
        self.assertEqual(html_node.props.get("src"), "https://www.example.com/image.png")
        self.assertEqual(html_node.props.get("alt"), "Alt text")

    def test_invalid_type(self):
    # Test that an exception is raised for invalid text types
        class InvalidTextType(Enum):
            INVALID = "invalid"
        
        node = TextNode("Invalid text", InvalidTextType.INVALID)
        with self.assertRaises(Exception):
            text_node_to_html_node(node)

if __name__ == "__main__":
    unittest.main()