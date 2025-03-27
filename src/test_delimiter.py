import unittest
from textnode import TextNode, TextType
from delimiter import * 

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
    
    def test_bold_delimiter(self):
        node = TextNode("This is **bold text** in a sentence", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[1].text, "bold text")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " in a sentence")
    
    def test_italic_delimiter(self):
        node = TextNode("This has _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This has ")
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
    
    def test_multiple_nodes_in_list(self):
        node1 = TextNode("Text with `code`", TextType.TEXT)
        node2 = TextNode("Already bold", TextType.BOLD)
        node3 = TextNode("More _italic_ text", TextType.TEXT)
        nodes = [node1, node2, node3]
        
        # First pass - handle code
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        # Should split the first node but leave others unchanged
        self.assertEqual(len(new_nodes), 4)
        
        # Second pass - handle italic
        final_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        # Should split the last text node but leave others unchanged
        self.assertEqual(len(final_nodes), 6)

    def test_multiple_delimiters_in_text(self):
        node = TextNode("Text with `code` and **bold** words", TextType.TEXT)
        
        # First handle code
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        
        # Then handle bold in the result
        final_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        self.assertEqual(len(final_nodes), 5)
        
        # Check the final structure
        self.assertEqual(final_nodes[0].text, "Text with ")
        self.assertEqual(final_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(final_nodes[1].text, "code")
        self.assertEqual(final_nodes[1].text_type, TextType.CODE)
        self.assertEqual(final_nodes[2].text, " and ")
        self.assertEqual(final_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(final_nodes[3].text, "bold")
        self.assertEqual(final_nodes[3].text_type, TextType.BOLD)
        self.assertEqual(final_nodes[4].text, " words")
        self.assertEqual(final_nodes[4].text_type, TextType.TEXT)
    
    def test_delimiter_at_beginning(self):
        node = TextNode("**Bold** at the start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "Bold")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[1].text, " at the start")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)
    
    def test_delimiter_at_end(self):
        node = TextNode("Text at the end `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "Text at the end ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
    
    def test_only_delimited_content(self):
        node = TextNode("**JustBold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "JustBold")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)
    
    def test_missing_closing_delimiter(self):
        node = TextNode("This has **bold but no closing delimiter", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)
    
    def test_empty_delimited_content(self):
        node = TextNode("Empty ``", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "Empty ")
        self.assertEqual(new_nodes[1].text, "")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
    
    def test_multiple_instances_of_same_delimiter(self):
        node = TextNode("**Bold** text with **multiple bold** sections", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "Bold")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[1].text, " text with ")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[2].text, "multiple bold")
        self.assertEqual(new_nodes[2].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[3].text, " sections")
        self.assertEqual(new_nodes[3].text_type, TextType.TEXT)
    
    def test_non_text_nodes_unchanged(self):
        # Test that nodes that aren't TEXT type are passed through unchanged
        node1 = TextNode("Regular text", TextType.TEXT)
        node2 = TextNode("Already bold", TextType.BOLD)
        node3 = TextNode("Code block", TextType.CODE)
        
        nodes = [node1, node2, node3]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        
        # The non-TEXT nodes should be unchanged
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text, "Already bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, "Code block")
        self.assertEqual(new_nodes[2].text_type, TextType.CODE)
    
    #tests for regex searches
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://www.boot.dev)"
        )
        self.assertListEqual([("link", "https://www.boot.dev")], matches)

    #tests for split images and links
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        node = TextNode("This is text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_at_beginning(self):
        node = TextNode("[link](https://example.com) starts with link", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" starts with link", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_at_end(self):
        node = TextNode("Ends with link [link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Ends with link ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_split_links_with_complex_url(self):
        node = TextNode("Link with [complex url](https://example.com/path?query=123&param=abc#fragment)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Link with ", TextType.TEXT),
                TextNode("complex url", TextType.LINK, "https://example.com/path?query=123&param=abc#fragment"),
            ],
            new_nodes,
        )

    def test_split_links_mixed_with_images(self):
    # This test checks that link extraction doesn't interfere with image markdown
        node = TextNode("Text with [link](https://example.com) and ![image](https://example.com/img.png)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and ![image](https://example.com/img.png)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_with_special_characters(self):
        node = TextNode("Link with [special & chars](https://example.com/special?q=a&b=c)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Link with ", TextType.TEXT),
                TextNode("special & chars", TextType.LINK, "https://example.com/special?q=a&b=c"),
            ],
            new_nodes,
        )

    def test_split_links_empty_link_text(self):
        node = TextNode("This has an [](https://example.com) empty link text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This has an ", TextType.TEXT),
                TextNode("", TextType.LINK, "https://example.com"),
                TextNode(" empty link text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_and_links_interaction(self):
    # Test that image splitting doesn't affect links and vice versa
        node = TextNode("![image](img.png) and [link](url)", TextType.TEXT)
    
    # First split images
        image_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "img.png"),
                TextNode(" and [link](url)", TextType.TEXT),
            ],
            image_nodes,
        )
    
    # Then split links in the resulting nodes
        final_nodes = split_nodes_link(image_nodes)
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "img.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
            ],
            final_nodes,
        )

    #test text_to_textnodes:
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )
    
    #test markdown_to_blocks:
    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )