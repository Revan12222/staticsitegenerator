

class HTMLNode():
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        props = ""
        for pair in self.props:
            props + f" {pair.key()}={pair.value()}"
        return props
    
    def __eq__(self,other):
        return ((self.tag == other.tag) and (self.value == other.value) and (self.children == other.children) 
                and (self.props == other.props))
    
    def __repr__(self):
        return self.props_to_html()
    
class LeafNode(HTMLNode):
    def __init__(self,tag,value,props=None):
        super().__init__(tag,value,None,props)

    def to_html(self):
        if not self.value:
            raise ValueError
        if not self.tag:
            return self.value
        text = f"<{self.tag}"
        if self.props:
            for key,value in self.props.items():
                text += f' {key}="{value}"'
        return f"{text}>{self.value}</{self.tag}>"


    