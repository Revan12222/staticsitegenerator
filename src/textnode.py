from enum import Enum
import os
import htmlnode
from regexfunctions import extract_markdown_images
from regexfunctions import extract_markdown_links
from blockfunctions import markdown_to_blocks
from blockfunctions import BlockType
from blockfunctions import block_to_block_type
from copydir import create_file_path


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, content, text_type, url=None):
        self.text = content
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and \
            self.url == other.url:
            return True
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return htmlnode.LeafNode(None,text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return htmlnode.LeafNode("b",text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return htmlnode.LeafNode("i",text_node.text)
    elif text_node.text_type == TextType.CODE:
        return htmlnode.LeafNode("code",text_node.text)
    elif text_node.text_type == TextType.LINK:
        return htmlnode.LeafNode("a",text_node.text,{"href":text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return htmlnode.LeafNode("img","",{"src":text_node.url,"alt":text_node.text})
    else:
        raise Exception("Not a proper text type.")
    
def split_nodes_delimiter(old_nodes,delimiter,text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text_blocks = node.text.split(delimiter)
        if len(text_blocks) % 2 == 0:
            raise Exception("Missing closing delimiter")
        alternator = 0
        if node.text.startswith(delimiter):
            #new_nodes.append(TextNode("Starts with delimiter",TextType.TEXT))
            #del text_blocks[0]
            alternator = 1
        for block in text_blocks:
            if block != "":
                if alternator == 0:
                    new_nodes.append(TextNode(block,node.text_type))
                    alternator = 1
                else:
                    new_nodes.append(TextNode(block,text_type))
                    alternator = 0
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        sections = [node.text]
        for image in images:
            sections = sections[-1].split(f"![{image[0]}]({image[1]})",1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0],TextType.TEXT))
            new_nodes.append(TextNode(image[0],TextType.IMAGE,image[1]))
        if sections[-1] != "":
            new_nodes.append(TextNode(sections[-1],TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        sections = [node.text]
        for link in links:
            sections = sections[-1].split(f"[{link[0]}]({link[1]})",1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0],TextType.TEXT))
            new_nodes.append(TextNode(link[0],TextType.LINK,link[1]))
        if sections[-1] != "":
            new_nodes.append(TextNode(sections[-1],TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    new_nodes = [TextNode(text,TextType.TEXT)]
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_delimiter(new_nodes,"`",TextType.CODE)
    new_nodes = split_nodes_delimiter(new_nodes,"**",TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes,"_",TextType.ITALIC)
    return new_nodes

def markdown_to_html_node(markdown):
    parent = htmlnode.ParentNode("div",[],None)
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        #block = block.replace("\n"," ")
        html_nodes = []
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            heading = heading_type(block)
            html_nodes = child_to_nodes(block.strip("#").strip())
            block_nodes.append(htmlnode.ParentNode(heading,html_nodes))
        if block_type == BlockType.PARAGRAPH:
            block = block.replace("\n"," ")
            html_nodes = child_to_nodes(block)
            block_nodes.append(htmlnode.ParentNode("p",html_nodes))
        if block_type == BlockType.QUOTE:
            html_nodes = child_to_nodes(block[1:].strip())
            block_nodes.append(htmlnode.ParentNode("blockquote",html_nodes))
        if block_type == BlockType.UNORDERED_LIST:
            list_items = block.split("- ")
            html_list_nodes = []
            #print(f"list_items {list_items}")
            for item in list_items:
                if not item:
                    continue
                html_list_nodes = child_to_nodes(item.strip())
                html_nodes.append(htmlnode.ParentNode("li",html_list_nodes))
            block_nodes.append(htmlnode.ParentNode("ul",html_nodes))
        if block_type == BlockType.ORDERED_LIST:
            list_items = block.split("\n")
            html_list_nodes = []
            #print(f"list_items {list_items}")
            for item in list_items:
                if not item:
                    continue
                item = item[3:]
                html_list_nodes = child_to_nodes(item.strip())
                html_nodes.append(htmlnode.ParentNode("li",html_list_nodes))
            block_nodes.append(htmlnode.ParentNode("ol",html_nodes))
        if block_type == BlockType.CODE:
            text_node = TextNode(block[3:-3].strip(),TextType.TEXT)
            html_nodes = [text_node_to_html_node(text_node)]
            block_nodes.append(htmlnode.ParentNode("pre",[htmlnode.ParentNode("code",html_nodes)]))
            #print(html_nodes)
    parent.children = block_nodes
    #parent_html = parent.to_html()
    #print(f"parent {parent}")
    #print(parent_html)
    #print(block_nodes)
        #node = htmlnode.HTMLNode(tag,value,children,props)
    return parent


def child_to_nodes(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def code_to_nodes(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def heading_type(text):
    count = text.find(" ")
    return f"h{count}"

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block[1:].strip()
    else:
        raise Exception("No title found")
    



