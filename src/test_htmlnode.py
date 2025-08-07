import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode
from htmlnode import LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        child = HTMLNode("<p>","This is a child")
        node = HTMLNode("<a>","This is a html node",child,{"href": "https://www.google.com"})
        node2 = HTMLNode("<a>","This is a html node",child,{"href": "https://www.google.com"})
        self.assertEqual(node, node2)

    

    def print(self):
        node = HTMLNode("<a>","This is a html node")
        print(node)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

if __name__ == "__main__":
    unittest.main()