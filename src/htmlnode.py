class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        returnable = ""
        if not self.props:
            return ""
        else:
            for key, value in self.props.items():
                returnable +=(f' {key}="{value}"')
        return returnable

    def __repr__(self):
        return f"HTML Node({self.tag}, {self.value}, {self.children}, {self.props})"
    
    def __eq__(self, other):
        if self.tag == other.tag and self.value == other.value:
            return True
        return False
    
# class LeafNode(HTMLNode):
#     def __init__(self, tag, value, props=None):
#         # Pass tag and props to the parent constructor, ensure props is always a dictionary
#         super().__init__(tag=tag, value=value, children=None, props=props if props else {})
#         self._children = None  # Explicitly prevent any children for LeafNode

#     def to_html(self):
#         # Raise an error if the value is missing for most tags
#         if self.value is None and self.tag not in ["img", "br", "hr", "input"]:
#             raise ValueError("LeafNode must have a value to render.")

#         # If no tag is provided, return raw text (value)
#         if self.tag is None:
#             return self.value

#         # Use the props_to_html helper method from the parent class to render props
#         props_str = self.props_to_html()

#         # Handle self-closing tags like <img>, <br>, <hr>, etc.
#         if self.tag in ["img", "br", "hr", "input"]:
#             return f"<{self.tag}{props_str} />"

#         # Render the tag normally with value if not self-closing
#         return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"

# class ParentNode(HTMLNode):
#     def __init__(self, tag, children, props=None):
#         # Pass tag, children, and props to the parent constructor, ensure props is always a dictionary
#         super().__init__(tag=tag, children=children, props=props if props else {})

#     def to_html(self):
#         # Error handling
#         if not self.tag:
#             raise ValueError("ParentNode must have a tag.")
        
#         #assigning children
#         children = ""
#         for i, child in enumerate(self.children):
#             if child is None:
#                 print(f"None child found in {self.tag} at index {i}")
#                 children+= child.to_html()
#             return f"<{self.tag}{self.props_to_html()}>{children}</{self.tag}>"
    
#     def __repr__(self):
#         return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
        
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
        if self.children is None:
            raise ValueError("invalid HTML: no children")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
        