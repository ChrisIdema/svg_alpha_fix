#this is not working yet, all the pretty print methods modify significant whitespace

from bs4 import BeautifulSoup

bad_image_path = "svg_test.svg"

with open(bad_image_path, 'r', encoding='utf8') as f:
    svg_string = f.read()
soup = BeautifulSoup(svg_string, "xml")

# with open(bad_image_path, 'r', encoding='utf8') as f:
#    soup = BeautifulSoup(f, "xml")


# svg_tag = soup.find("svg")

# print(svg_tag.namespace)
# svg_tag.namespace = ''
# del svg_tag.namespace

# if "xmlns:svg" in svg_tag.attrs:
#    del svg_tag.attrs["xmlns:svg"]

# soup = BeautifulSoup(str(soup), "xml")

# svg_text_tags = svg_tag.find_all(name="text")

# for text in svg_text_tags:
#     if "fill" in text.attrs:
#         fill = text["fill"]
#         # del text["fill"]
#         # print(fill)
#         if fill.startswith("rgba("):
#             rgba = fill.replace('rgba(','').replace(')','').split(',')
#             text['fill'] = f'rgb({rgba[0]},{rgba[1]},{rgba[2]})'
#             text['fill-opacity'] = rgba[3]
#             # print(rgba)


# for tag in soup.find_all(True):
#     level = len(tag.find_parents())

#     preserve = False
#     if 'xml:space' in tag.attrs:
#         preserve = tag.attrs['xml:space'] == 'preserve'

#     parent = tag.find_parent()
#     parent_preserve = False    
#     if parent:
#         if 'xml:space' in parent.attrs:
#             parent_preserve = parent.attrs['xml:space'] == 'preserve'


#     attributes_string = " ".join([f'{key}:"{value}"' for key,value in tag.attrs.items()])
#     # print(attributes_string)
#     print("  "*level + "<" + tag.name + " "*(len(attributes_string)!=0) + attributes_string + ">")


#     # print(tag.name)
#     # print(tag.attrs)

#     # print(tag.contents)


#     # print(preserve)

#     # print(len(tag.find_parents()))

#     # for c in tag.contents:
#     #     print((type(c)))
#     #     print(c)

#     # for string in tag.strings:
#     #     print('"',string,'"')

#     # print('"',tag.text,'"')
       
       
with open('svg_test_soup.svg', 'w', encoding='utf8', newline='\n') as f:
    f.write(soup.prettify())  # makes weird changes, because it ignores xml:space="preserve"
    # f.write(str(soup))

import xml.dom.minidom
from xml import dom

output = dom.minidom.parseString(svg_string)
# print(output.toprettyxml())

with open('svg_test_minidom.svg', 'w', encoding='utf8', newline='\n') as f:
    f.write(output.toprettyxml())


import xml.etree.ElementTree as ET
tree = ET.parse(bad_image_path)

ET.indent(tree, space='  ', level=0)

with open('svg_test_ET.svg', 'wb') as f:
    tree.write(f)


# from defusedxml.ElementTree import parse
# defused = parse(bad_image_path)

# with open('svg_test_defused.svg', 'wb') as f:
#     defused.write(f)

import xml.sax


class Prettifier(xml.sax.ContentHandler, xml.sax.handler.LexicalHandler):
    def __init__(self):
        self.level = -1
        self.preserve_space_stack=[False]
        self.last_was_opening_tag = False #tags without content or empty content don't need closing tag on next line
        self.indent = " "*4
        self.first_tag = True

    # Call when an element starts
    def startElement(self, tag, attributes):
        self.level += 1       

        if 'xml:space' in attributes:
            self.preserve_space_stack.append(attributes['xml:space'] == 'preserve')
        else:
            self.preserve_space_stack.append(self.preserve_space_stack[-1])

        attributes_string = " ".join([f'{key}="{value}"' for key,value in attributes.items()])
  

        if self.preserve_space_stack[-1]:
            if self.preserve_space_stack[-2] == False:
                print()
                print(self.indent*self.level, end="")

            print(f"<{tag}", end="")
            print(" "*(len(attributes_string)!=0), end="")
            print(attributes_string, end="")
            print(">", end="")
        else:
            if not self.first_tag:
                print()

            if len(attributes_string) > 60:
                attributes_string = f"\n{self.indent*self.level + ' '*(len(tag)+2)}".join([f'{key}="{value}"' for key,value in attributes.items()])
        
            print(self.indent*self.level, end="")
            print(f"<{tag}", end="")
            print(" "*(len(attributes_string)!=0), end="")
            print(attributes_string, end="")
            print(">", end="")

        self.last_was_opening_tag = True   
        self.first_tag = False 


    # Call when an elements ends
    def endElement(self, tag):        
        if self.preserve_space_stack[-1]:
            print(f"</{tag}", end="")
            print(">", end="")
        else:
            if not self.last_was_opening_tag:
                print()
                print(self.indent*self.level, end="")
            print(f"</{tag}", end="")
            print(">",end="")

        self.level -= 1
        self.preserve_space_stack.pop()

        self.last_was_opening_tag = False
    


    # Call when a character is read
    def characters(self, content):        
        empty_content = False
        if self.preserve_space_stack[-1]:
            print(content, end="")
            empty_content = content == ""
        else:          
            empty_content = content.strip() == ""
            if not empty_content:
                print()
                print(self.indent*(self.level+1), end="")
                print(content.strip(), end="")

        self.last_was_opening_tag = self.last_was_opening_tag and empty_content

    # lexical handler methods:
    def comment(self, content):
        print(f"<!--{content}-->", end="")


parser = xml.sax.make_parser()
# turn off namepsaces
parser.setFeature(xml.sax.handler.feature_namespaces, 0)

Handler = Prettifier()
parser.setContentHandler( Handler )

parser.setProperty ( xml.sax.handler.property_lexical_handler, Handler)

parser.parse(bad_image_path)
