import unittest

from textnode import TextNode, TextType


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

if __name__ == "__main__":
    unittest.main()