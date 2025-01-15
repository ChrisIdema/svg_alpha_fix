# from bs4 import BeautifulSoup

import xml.etree.ElementTree as ET

import xml_prettify

bad_image_path = "svg_test.svg"
converted_image_path = "svg_test_converted_xml.svg"

# with open(bad_image_path, 'r', encoding='utf8') as f:
#     svg_string = f.read()

# soup = BeautifulSoup(svg_string, "xml")


ET.register_namespace('',"http://www.w3.org/2000/svg")
tree = ET.parse(bad_image_path)
root = tree.getroot()

for key in["fill", "stroke", "flood-color"]:
    for node in root.findall(f".//*[@{key}]"):
        value = node.get(key)
        opacity_key = key.removesuffix('-color') + "-opacity" 
        print(value)
        if value.startswith("rgba"):
            rgba = value.replace('rgba(','').replace(')','').split(',')
            opacity_value = rgba[3]     
            node.set(key,f'rgb({rgba[0]},{rgba[1]},{rgba[2]})')                       
            node.set(opacity_key,opacity_value)
        elif value.startswith("#") and len(value) in [5,9]:
            if len(value) == 5:
                color_value = value[0:4]                          
                opacity_float = float(int(value[4:5], base=16)/15)
            else:
                color_value = value[0:7]  
                opacity_float = float(int(value[7:9], base=16)/255)  
            
            # limit to 3 decimal digits, remove unnecessary trailing zeros and decimal point: 
            opacity_value = f"{opacity_float:.3f}".rstrip('0').rstrip('.')
            node.set(key,color_value)                       
            node.set(opacity_key,opacity_value)

tree.write(converted_image_path)


# svg_tag = root.find("svg")

# for tag in root.findall(""):
#     for key, value in list(tag.attrs.items()):
#         print(key)

# for tag in svg_tag.find_all():
#     for key, value in list(tag.attrs.items()):
#         if key in ["fill", "stroke", "flood-color"]:
#             opacity_key = key.removesuffix('-color') + "-opacity"  
#             if value.startswith("rgba("):
#                 rgba = value.replace('rgba(','').replace(')','').split(',')
#                 opacity_value = rgba[3]    
#                 tag.attrs[key] = f'rgb({rgba[0]},{rgba[1]},{rgba[2]})'            
#                 tag.attrs[opacity_key] = opacity_value
#             elif value.startswith("#") and len(value) in [5,9]:
#                 if len(value) == 5:
#                     color_value = value[0:4]                          
#                     opacity_float = float(int(value[4:5], base=16)/15)
#                 else:
#                     color_value = value[0:7]  
#                     opacity_float = float(int(value[7:9], base=16)/255)  
                
#                 # limit to 3 decimal digits, remove unnecessary trailing zeros and decimal point: 
#                 opacity_value = f"{opacity_float:.3f}".rstrip('0').rstrip('.')
#                 tag.attrs[key] = color_value
#                 tag.attrs[opacity_key] = opacity_value


      
# with open(converted_image_path, 'w', encoding='utf8', newline='\n') as f:
#     # f.write(xml_prettify.prettify_string(str(soup)))
#     f.write(str(dom1))
