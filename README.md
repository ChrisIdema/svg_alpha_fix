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
* Use either `svg_convert_regex.py` or `svg_convert_xml.py` (requires lxml python module)
* change `bad_image_path` and `converted_image_path` in the file
* run

# Prettify
`xml_prettify.py` has a prettify function that respects `xml:space="preserve"` and preserves significant whitespace if needed.
It also keeps comments and CDATA. It doesn't preserve or process DTD.

* `prettify_string` accepts XML string and returns prettified XML string
* `prettify_file` accepts XML filename and returns prettified XML string



# reference
https://gitlab.com/inkscape/inbox/-/issues/1195
