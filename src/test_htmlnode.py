import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        child = HTMLNode("<p>","This is a child")
        node = HTMLNode("<a>","This is a html node",child,{"href": "https://www.google.com"})
        node2 = HTMLNode("<a>","This is a html node",child,{"href": "https://www.google.com"})
        self.assertEqual(node, node2)

    def print(self):
        node = HTMLNode("<a>","This is a html node")
        print(node)



if __name__ == "__main__":
    unittest.main()