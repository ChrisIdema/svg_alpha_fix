#pip install beautifulsoup4

# from bs4 import BeautifulSoup

# bad_image_path = "test_text.svg"

# with open(bad_image_path, 'r', encoding='utf8') as f:
#     svg_string = f.read()
# soup = BeautifulSoup(svg_string, "xml")

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
       
# with open('test_text_converted.svg', 'w', encoding='utf8') as f:
#     # f.write(soup.prettify())  # makes weird changes, because it ignores xml:space="preserve"
#     f.write(str(soup))

# # print(soup.prettify())

# import xml.dom.minidom
# from xml import dom

# with open(bad_image_path, 'r', encoding='utf8') as f:
#     xml_string = f.read()

# output = dom.minidom.parseString(xml_string)
# # print(output.toprettyxml())

# with open('test_text_converted.svg', 'w', encoding='utf8') as f:
#     f.write(output.toprettyxml())
