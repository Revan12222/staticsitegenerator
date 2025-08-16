

class HTMLNode():
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        props = ""
        for pair in self.props:
            props + f" {pair.key()}={pair.value()}"
        return props
    
    def __eq__(self,other):
        return ((self.tag == other.tag) and (self.value == other.value) and (self.children == other.children) 
                and (self.props == other.props))
    
    def __repr__(self):
        return self.props_to_html()
    
class ParentNode(HTMLNode):
    def __init__(self,tag,children,props=None):
        super().__init__(tag,None,children,props)

    def to_html(self):
        if not self.tag:
            raise ValueError("missing tag")
        if not self.children:
            raise ValueError("missing children")
        text = f"<{self.tag}>"
        for child in self.children:
            text += child.to_html()
        text += f"</{self.tag}>"
        return text
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.value}, {self.children})"

class LeafNode(HTMLNode):
    def __init__(self,tag,value,props=None):
        super().__init__(tag,value,None,props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if not self.tag:
            return self.value
        text = f"<{self.tag}"
        if self.props:
            for key,value in self.props.items():
                text += f' {key}="{value}"'
        return f"{text}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    