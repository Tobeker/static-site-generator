from textnode import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_list.append(old_node)
            continue
        text = old_node.text
        parts = []
        while delimiter in text:
            start_idx = text.find(delimiter)
            if start_idx > 0:
                parts.append((text[:start_idx], TextType.TEXT))
            end_idx = text.find(delimiter, start_idx + len(delimiter))
            if end_idx == -1:
                raise Exception("Missing closing delimiter")
            delimited_content = text[start_idx + len(delimiter):end_idx]
            parts.append((delimited_content, text_type))
            text = text[end_idx + len(delimiter):]
        if text:
            parts.append((text, TextType.TEXT))
        for content, node_type in parts:
            new_list.append(TextNode(content, node_type))
    return new_list

def extract_markdown_images(text):
    result = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return result

def extract_markdown_links(text):
    result = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return result

def split_nodes_image(old_nodes):
    result = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
            
        # Extract image information
        images = extract_markdown_images(old_node.text)
        if not images:
            result.append(old_node)
            continue
            
        # Start with the original text
        remaining_text = old_node.text
        
        # Process each image
        for alt_text, url in images:
            # Find the image markdown in the text
            image_markdown = f"![{alt_text}]({url})"
            parts = remaining_text.split(image_markdown, 1)
            
            # Add text before the image if not empty
            if parts[0]:
                result.append(TextNode(parts[0], TextType.TEXT))
                
            # Add the image node
            result.append(TextNode(alt_text, TextType.IMAGE, url))
            
            # Update remaining text
            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""
        
        # Add any remaining text
        if remaining_text:
            result.append(TextNode(remaining_text, TextType.TEXT))
            
    return result

def split_nodes_link(old_nodes):
    result = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
            
        # Extract link information
        links = extract_markdown_links(old_node.text)
        if not links:
            result.append(old_node)
            continue
            
        # Start with the original text
        remaining_text = old_node.text
        
        # Process each link
        for text, url in links:
            # Find the link markdown in the text
            link_markdown = f"[{text}]({url})"
            parts = remaining_text.split(link_markdown, 1)
            
            # Add text before the link if not empty
            if parts[0]:
                result.append(TextNode(parts[0], TextType.TEXT))
                
            # Add the link node
            result.append(TextNode(text, TextType.LINK, url))
            
            # Update remaining text
            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""
        
        # Add any remaining text
        if remaining_text:
            result.append(TextNode(remaining_text, TextType.TEXT))
            
    return result

def text_to_textnodes(text):
    if type(text) != str:
        raise Exception("no Text input")
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    if type(markdown) != str:
        raise Exception("no Text input")
    blocks = markdown.split('\n\n')
    result = []
    for block in blocks:
        cleaned_block = '\n'.join([line.strip() for line in block.split('\n')])
        result.append(cleaned_block.strip())
    return result