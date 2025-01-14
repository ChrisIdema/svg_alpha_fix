import re
import os, fnmatch

def svg_alpha_fix(svg_string):

    # split rgba colors in color and opacity:
    regex = r"(fill|stroke|flood)(-color)?\s*=\s*\"rgba\(([^\,)]+),([^\,)]+),([^\,)]+),([^\,)]+)\)\""
    subst = "\\1\\2=\"rgb(\\3,\\4,\\5)\" \\1-opacity=\"\\6\""
    result = re.sub(regex, subst, svg_string, 0, re.MULTILINE)

    # split hex colors with alpha in color and opacity:
    regex = r"(fill|stroke|flood-color)\s*=\s*\"#([[:xdigit:]]{4}|[[:xdigit:]]{8})\"".replace("[[:xdigit:]]","[0-9a-fA-F]")

    def hex_color_substitutor(match_obj):
        a = match_obj.group(1)
        b = a.removesuffix('-color') + "-opacity"

        if len(match_obj.group(2)) == 4:
            color_value = match_obj.group(2)[:3]
            opacity_float = float(int(match_obj.group(2)[3:4], base=16)/15)
        else:
            color_value = match_obj.group(2)[:6]   
            opacity_float = float(int(match_obj.group(2)[6:8], base=16)/255)   
        
        # limit to 3 decimal digits, remove unnecessary trailing zeros and decimal point: 
        opacity_value = f"{opacity_float:.3f}".rstrip('0').rstrip('.')

        return f'{a}="#{color_value}" {b}="{opacity_value}"'

    result = re.sub(regex, hex_color_substitutor, result)
    return result


bad_image_path = "svg_test.svg"
converted_image_path = "svg_test_converted.svg"

# test_str = ("fill=\"#11223380\"\n"
# 	"fill=\"#1238\"\n"
# 	"stroke=\"#11223380\"\n"
# 	"flood-color=\"#11223380\"\n"
# 	"fill=\"rgba(1,2,3,0.4)\"\n"
# 	"fill=\"rgba(1,2,3,40%)\"\n"
# 	"stroke=\"rgba(5,6,7,0.8)\"\n"
# 	"flood-color=\"rgba(5,6,7,0.8)\"\n")
# svg_string = test_str

with open(bad_image_path, 'r', encoding='utf8') as f:
    svg_string = f.read()
    
result = svg_alpha_fix(svg_string)

with open(converted_image_path, 'w', encoding='utf8', newline='\n') as f:
    f.write(result)


# bad_image_folder_path = "..."

# fileOfDirectory = os.listdir(bad_image_folder_path)
# pattern = "*.svg"
# for filename in fileOfDirectory:
#     if fnmatch.fnmatch(filename, pattern):
#         full_path = os.path.join(bad_image_folder_path, filename)
#         print(full_path)
#         with open(full_path, 'r', encoding='utf8') as f:
#             svg_string = f.read()
#         result = svg_alpha_fix(svg_string)
#         converted_image_path = os.path.join(bad_image_folder_path, filename)
#         with open(converted_image_path, 'w', encoding='utf8', newline='\n') as f:
#             f.write(result)
