import unittest

from textnode import TextNode, TextType
from textnode import split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node",TextType.IMAGE, "www.google.com")
        node2 = TextNode("This is a text nodes",TextType.IMAGE, "www.google.com")
        self.assertNotEqual(node,node2)

    def test_eq2(self):
        node = TextNode("This is a text node", TextType.BOLD,"www.amazon.com")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

class TestNestedNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes,[
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            ])
        
    def test_eq2(self):
        node = TextNode("**Now this** is text with a bold start word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes,[
            TextNode("Now this", TextType.BOLD),
            TextNode(" is text with a bold start word", TextType.TEXT)
            ])
        
    def test_eq3(self):
        node = TextNode("**Now this** is text with a __bold__ start word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes,"__",TextType.ITALIC)
        self.assertEqual(new_nodes,[
            TextNode("Now this", TextType.BOLD),
            TextNode(" is text with a ", TextType.TEXT),
            TextNode("bold",TextType.ITALIC),
            TextNode(" start word",TextType.TEXT)
            ])


if __name__ == "__main__":
    unittest.main()