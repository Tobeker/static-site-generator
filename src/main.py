from textnode import *

text = "This is some anchor text"
text_typ = TextType.LINK
url = "https://www.boot.dev"

def main():
    Boot = TextNode(text, text_typ, url)
    print(Boot)

main()