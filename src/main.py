from textnode import *
from htmlnode import *
from independent_functions import *

def main():
    juniper = TextNode("This is a node", TextType.BOLD, "www.bootdev.com")
    print (juniper)

    elm = HTMLNode("p", "test1")
    print (elm)

if __name__ == "__main__":
    main()