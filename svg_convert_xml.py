from bs4 import BeautifulSoup

import xml_prettify

bad_image_path = "svg_test.svg"
converted_image_path = "svg_test_converted_xml.svg"

with open(bad_image_path, 'r', encoding='utf8') as f:
    svg_string = f.read()

soup = BeautifulSoup(svg_string, "xml")

svg_tag = soup.find("svg")

for tag in svg_tag.find_all():
    for key, value in list(tag.attrs.items()):
        if key in ["fill", "stroke", "flood-color"]:
            opacity_key = key.removesuffix('-color') + "-opacity"  
            if value.startswith("rgba("):
                rgba = value.replace('rgba(','').replace(')','').split(',')
                tag.attrs[key] = f'rgb({rgba[0]},{rgba[1]},{rgba[2]})'
                opacity_value = rgba[3]                
                tag.attrs[opacity_key] = opacity_value
            elif value.startswith("#") and len(value) in [5,9]:
                # print(value)

                if len(value) == 5:
                    color_value = value[0:4]                          
                    opacity_float = float(int(value[4:5], base=16)/15)
                else:
                    color_value = value[0:7]  
                    opacity_float = float(int(value[7:9], base=16)/255)  

                # print(color_value)
                # print(opacity_float)
                
                # limit to 3 decimal digits, remove unnecessary trailing zeros and decimal point: 
                opacity_value = f"{opacity_float:.3f}".rstrip('0').rstrip('.')
                tag.attrs[opacity_key] = opacity_value
                tag.attrs[key] = color_value


      
with open(converted_image_path, 'w', encoding='utf8', newline='\n') as f:
    # f.write(xml_prettify.prettify_string(str(soup)))
    f.write(str(soup))
