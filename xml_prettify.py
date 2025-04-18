import xml.sax
from io import StringIO
import re
import sys

class Prettifier(xml.sax.ContentHandler, xml.sax.handler.LexicalHandler):
    def __init__(self, print_method=None):
        self.level = -1
        self.preserve_space_stack=[False]
        self.last_was_opening_tag = False #tags without content or empty content don't need closing tag on next line
        self.indent = " "*4
        self.first_tag = True
        self.external_print_method = print_method
        self.string=""
        self.CDATA = False

    def get_string(self):
        return self.string

    def print_method(self, text="", end="\n"):
        if self.external_print_method:
            self.external_print_method(text, end)
        self.string += text + end

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
                self.print_method()
                self.print_method(self.indent*self.level, end="")

            self.print_method(f"<{tag}", end="")
            self.print_method(" "*(len(attributes_string)!=0), end="")
            self.print_method(attributes_string, end="")
            self.print_method(">", end="")
        else:
            if not self.first_tag:
                self.print_method()

            if len(attributes_string) > 60:
                attributes_string = f"\n{self.indent*self.level + ' '*(len(tag)+2)}".join([f'{key}="{value}"' for key,value in attributes.items()])
        
            self.print_method(self.indent*self.level, end="")
            self.print_method(f"<{tag}", end="")
            self.print_method(" "*(len(attributes_string)!=0), end="")
            self.print_method(attributes_string, end="")
            self.print_method(">", end="")

        self.last_was_opening_tag = True   
        self.first_tag = False 


    # Call when an elements ends
    def endElement(self, tag):        
        if self.preserve_space_stack[-1]:
            self.print_method(f"</{tag}", end="")
            self.print_method(">", end="")
        else:
            if not self.last_was_opening_tag:
                self.print_method()
                self.print_method(self.indent*self.level, end="")
            self.print_method(f"</{tag}", end="")
            self.print_method(">",end="")

        self.level -= 1
        self.preserve_space_stack.pop()

        self.last_was_opening_tag = False
    
    # Call when a character is read
    def characters(self, content):    
        if self.CDATA:
            self.print_method(content, end="")
        else:
            empty_content = False
            if self.preserve_space_stack[-1]:
                self.print_method(content, end="")
                empty_content = content == ""
            else:          
                empty_content = content.strip() == ""
                if not empty_content:
                    self.print_method()
                    self.print_method(self.indent*(self.level+1), end="")
                    self.print_method(content.strip(), end="")

            self.last_was_opening_tag = self.last_was_opening_tag and empty_content

    # lexical handler methods:
    def comment(self, content):
        if not self.preserve_space_stack[-1]:
            self.print_method()
            self.print_method(self.indent*(self.level+1), end="")
     
        self.print_method(f"<!--{content}-->", end="")

    def startCDATA(self):
        #The contents of the CDATA marked section will be reported through the characters handler.
        if not self.preserve_space_stack[-1]:
            self.print_method()
            self.print_method(self.indent*(self.level+1), end="")
    
        self.print_method("<![CDATA[", end="")
        self.CDATA = True

    def endCDATA(self):
        self.print_method("]]>", end="")
        self.CDATA = False

        
def process_xml_declaration(xml_string):
    declaration = ""
    regex = r"^\s*(<\?xml [^\?>]*\?>)"
    matches = re.search(regex, xml_string)

    if matches:
        declaration = matches.group(1) + "\n"
    return declaration

def prettify_file(file_name):
    Handler = Prettifier()
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)# turn off namespaces
    parser.setContentHandler(Handler)
    parser.setProperty(xml.sax.handler.property_lexical_handler, Handler)

    parser.parse(file_name)

    declaration = ""
    with open(file_name, 'r', encoding='utf8') as f:
        declaration = process_xml_declaration(f.read())

    return declaration + Handler.get_string()

def prettify_string(xml_string):
    Handler = Prettifier()
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)# turn off namespaces
    parser.setContentHandler(Handler)
    parser.setProperty(xml.sax.handler.property_lexical_handler, Handler)

    xml_string_stream = StringIO(xml_string)
    parser.parse(xml_string_stream)

    declaration = process_xml_declaration(xml_string)

    return declaration + Handler.get_string()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for bad_image_path in sys.argv[1:]:
            svg_string_pretty = prettify_file(bad_image_path)  
            
            with open(bad_image_path, 'w', encoding='utf8', newline='\n') as f:
                f.write(svg_string_pretty)
    else:
        pass
