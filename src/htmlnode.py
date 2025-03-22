

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children or []
        self.props = props or {}

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        result = ""
        for key in self.props:
            result += f' {key}="{self.props[key]}"'
        return result
    
    def __repr__(self):
        return f"HTMLNode(tag:{self.tag}, value:{self.value}, children:{self.children}, props:{self.props})"
    
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props)
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("no value")
        if self.tag == None:
            return self.value
        else:
            if self.tag == "a" or self.tag == "img":
                return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
            else:
                return f"<{self.tag}>{self.value}</{self.tag}>"
            
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("no tag")
        if self.children == None:
            raise ValueError("no child")
        else:
            result = f"<{self.tag}{self.props_to_html()}>"
            for node in self.children:
                result += node.to_html()
            result += f"</{self.tag}>"
            return result