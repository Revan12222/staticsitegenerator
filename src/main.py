from textnode import TextNode
from copydir import copy_dir
from pagegen import generate_pages_recursive
from pagegen import generate_page

def main():
    temp_node = TextNode("Hello World","Bold","google.come")
    #print(temp_node)
    md = """

# This is the _site_ heading

This is **bolded** paragraph
text in a p
tag here

1. Orange
2. Banana
3. Apple

> Let's quote something fun here like "Fear is the mind killer"

This is another paragraph with _italic_ text and `code` here

- Unordered Item 1
- And Item 2
- And Item 3

```
This is text that _should_ remain
the **same** even with inline stuff
```

"""
    #markdown_to_html_node(md)
    copy_dir("static","public")
    #print(extract_title(md))
    #generate_page("content/index.md","template.html", "public/index.html")
    #generate_pages_recursive("content","template.html","public")

main()