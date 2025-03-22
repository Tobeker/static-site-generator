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

    def test_parent_node_with_no_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_parent_node_with_multiple_children(self):
        child1 = LeafNode("span", "first")
        child2 = LeafNode("b", "second")
        child3 = LeafNode("i", "third")
        parent_node = ParentNode("div", [child1, child2, child3])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>first</span><b>second</b><i>third</i></div>"
        )

    def test_nested_parent_nodes(self):
        inner_child = LeafNode("b", "text")
        inner_parent = ParentNode("span", [inner_child])
        middle_parent = ParentNode("div", [inner_parent])
        outer_parent = ParentNode("section", [middle_parent])
        self.assertEqual(
            outer_parent.to_html(),
            "<section><div><span><b>text</b></span></div></section>"
        )

    def test_mixed_children_types(self):
        leaf_child = LeafNode("i", "italic")
        parent_child = ParentNode("div", [LeafNode("b", "bold")])
        mixed_parent = ParentNode("section", [leaf_child, parent_child])
        self.assertEqual(
            mixed_parent.to_html(),
            "<section><i>italic</i><div><b>bold</b></div></section>"
        )

    def test_parent_node_raises_error_with_no_tag(self):
        children = [LeafNode("span", "child")]
        parent_node = ParentNode(None, children)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parent_node_raises_error_with_no_children(self):
    # Test that ValueError is raised when children is None
    # Note: This would require bypassing the constructor validation
    # so you might need to create a node and then modify its children
        parent_node = ParentNode("div", [])
        parent_node.children = None
        with self.assertRaises(ValueError):
            parent_node.to_html()
        
    def test_parent_node_with_props(self):
    # Test parent node with properties
        child = LeafNode("span", "text")
        parent = ParentNode("div", [child], {"class": "container", "id": "main"})
        self.assertEqual(
            parent.to_html(),
            '<div class="container" id="main"><span>text</span></div>'
        )
    
    def test_deeply_nested_structure(self):
    # Test a complex nested structure with multiple levels
        leaf1 = LeafNode("b", "bold")
        leaf2 = LeafNode("i", "italic")
        inner_parent1 = ParentNode("p", [leaf1, leaf2])
    
        leaf3 = LeafNode("a", "link", {"href": "#"})
        inner_parent2 = ParentNode("nav", [leaf3])
    
        outer_parent = ParentNode("div", [inner_parent1, inner_parent2], {"class": "wrapper"})
    
        self.assertEqual(
            outer_parent.to_html(),
            '<div class="wrapper"><p><b>bold</b><i>italic</i></p><nav><a href="#">link</a></nav></div>'
        )

if __name__ == "__main__":
    unittest.main()