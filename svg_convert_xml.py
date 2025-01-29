import lxml.etree as ET
import xml_prettify
import sys

def svg_alpha_fix(svg_path):
    parser = ET.XMLParser(strip_cdata=False)
    tree = ET.parse(bad_image_path, parser=parser)
    root = tree.getroot()

    for key in["fill", "stroke", "flood-color"]:
        for node in root.findall(f".//*[@{key}]"):
            value = node.get(key)
            opacity_key = key.removesuffix('-color') + "-opacity" 
            if value.startswith("rgba"):
                rgba = value.replace('rgba(','').replace(')','').split(',')
                opacity_value = rgba[3]     
                node.set(key,f'rgb({rgba[0]},{rgba[1]},{rgba[2]})')                       
                # node.set(opacity_key,opacity_value)

                # insert opacity value right after color:
                attribs = node.attrib.items()
                node.attrib.clear()
                attribs.insert(list(dict(attribs).keys()).index(key)+1, (opacity_key,opacity_value))     
                node.attrib.update(attribs)

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
                # node.set(opacity_key,opacity_value)

                # insert opacity value right after color:
                attribs = node.attrib.items()
                node.attrib.clear()
                attribs.insert(list(dict(attribs).keys()).index(key)+1, (opacity_key,opacity_value))     
                node.attrib.update(attribs)
    return ET.tostring(root, encoding='unicode')
      

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for bad_image_path in sys.argv[1:]:

            with open(bad_image_path, 'r', encoding='utf8') as f:
                svg_string = f.read()
            declaration = xml_prettify.process_xml_declaration(svg_string)

            result = declaration + svg_alpha_fix(bad_image_path)  
            
            with open(bad_image_path, 'w',encoding='utf8', newline='\n') as f:
                f.write(xml_prettify.prettify_string(result))
    else:
        pass
