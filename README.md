# svg_alpha_fix
Fixes svg images that don't render properly in inkscape, extracts alpha from color and puts it in opacity attribute.

Example:
```
fill="rgba(1,2,3,50%)"
```
Becomes:
```
fill="rgba(1,2,3)"
fill-opacity="50%"
```
Example2:
```
fill="#00ff0080"
```
Becomes:
```
fill="#00ff00"
fill-opacity="0.502"
```

The following attributes will be parsed:
* fill (will create fill-opacity)
* stroke (will create stroke-opacity)
* flood-color (will create flood-opacity)

# fix SVG file
Use either `svg_convert_regex.py` or `svg_convert_xml.py` (requires lxml python module)

* pass paths of files to the scripts e.g. `svg_convert_regex.py file.svg` or drag them onto the script if dragging onto python files is enabled on your system
* drag onto `svg_convert.cmd` to use `svg_convert_regex.py`
* or call `svg_alpha_fix()`* 

*note that `svg_convert_xml.py` only accepts filenames and `svg_convert_regex.py` only accepts strings. `svg_convert_xml.py's svg_alpha_fix()` removes xml declaration and needs to be added back manually if needed.

# Prettify
`xml_prettify.py` has a prettify function that respects `xml:space="preserve"` and preserves significant whitespace if needed.
It preserverves the xml declaration. It also keeps comments and CDATA. It doesn't preserve or process DTD. 

* `prettify_string()` accepts XML string and returns prettified XML string
* `prettify_file()` accepts XML filename and returns prettified XML string
* `process_xml_declaration()` accepts XML string and returns the XML declaration (used internally to preserve XML declaration)

# reference
https://gitlab.com/inkscape/inbox/-/issues/1195
