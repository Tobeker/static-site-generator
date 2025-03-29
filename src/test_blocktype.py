import unittest
from blocktype import *

class TestMarkdownParser(unittest.TestCase):
    def test_paragraph(self):
        self.assertEqual(block_to_block_type("Dies ist ein normaler Text."), BlockType.PARAGRAPH)

    def test_heading(self):
        self.assertEqual(block_to_block_type("# Überschrift"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Unterüberschrift"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Kleinste Überschrift"), BlockType.HEADING)

    def test_code_block(self):
        self.assertEqual(block_to_block_type("```\ncode\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```\npython\ncode\n```"), BlockType.CODE)

    def test_quote(self):
        self.assertEqual(block_to_block_type("> Dies ist ein Zitat"), BlockType.QUOTE)

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- Ein Listenelement"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- Ein Listenelement\n- Ein Item"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- Ein Listenelement\n- Ein Item\n- Ein Item\n- Ein Item"), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. Erstes Element"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1. Erstes Element\n2. Zweites Element"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1. Erstes Element\n2. Zweites Element\n3. Erstes Element\n4. Zweites Element\n5. Zehntes Element"), BlockType.ORDERED_LIST)

    #test markdown to html node:
    def test_paragraphs(self):
        md = """
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
                ```
                This is text that _should_ remain
                the **same** even with inline stuff
                ```
                """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    #test extract_title:
    def test_extract_title(self):
        markdown = "# Hello"
        markdown2 = "# No Title"
        result = extract_title(markdown)
        result2 = extract_title(markdown2)
        self.assertEqual(result, "Hello")
        self.assertEqual(result2, "No Title")