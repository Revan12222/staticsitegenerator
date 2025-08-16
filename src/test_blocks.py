import unittest

from blockfunctions import markdown_to_blocks
from blockfunctions import block_to_block_type
from blockfunctions import BlockType

class TestBlocks(unittest.TestCase):
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

    def test_markdown_to_blocks2(self):
        md = """      


This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items

Some more _italic_ down here


"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
                "Some more _italic_ down here"
            ],
        )

class TestBlock(unittest.TestCase):
    '''
    def TestBlockType(self):
        md  = "## I am a heading"
        block = block_to_block_type(md)
        self.assertEqual(block,BlockType.HEADING)'''

    def test_block_type2(self):
        md  = "- I am a heading"
        block = block_to_block_type(md)
        self.assertEqual(block,BlockType.UNORDERED_LIST)

if __name__ == "__main__":
    unittest.main()