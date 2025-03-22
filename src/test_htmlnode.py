import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

tag = "p"
value = "this is the value"
child = [HTMLNode()]
prop = {
    "href": "https://www.google.com",
    "target": "_blank",
}
html_prop = ' href="https://www.google.com" target="_blank"'

class TestHTMLNode(unittest.TestCase):
    def test_html(self):
        node = HTMLNode(tag, value, child, prop)
        node2 = HTMLNode(tag, value, child, prop)
        node3 = HTMLNode()
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertIsNotNone(node.children)
        self.assertIsInstance(node, HTMLNode)
        self.assertEqual(node.props_to_html(), html_prop)
        self.assertNotEqual(node.tag, node3.tag)

    def test_leaf_to_html(self):
        node = LeafNode("p", "Hello, world!")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(node2.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()