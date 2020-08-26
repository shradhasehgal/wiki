import sys
import xml.sax

class PageHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.CurrentData = ""
        self.title = ""
        self.description = ""
        self.content = ""
    
    def startElement(self, tag, attributes):
        self.CurrentData = tag

            # Call when an elements ends
    def endElement(self, tag):
        if tag =="mediawiki":
            print("Done")

    def characters(self, content):
        if self.CurrentData == "title":
            self.title = content
            print(self.title)


wikiDump = sys.argv[1]
# create an XMLReader
parser = xml.sax.make_parser()
# turn off namepsaces
parser.setFeature(xml.sax.handler.feature_namespaces, 0)
Handler = PageHandler()
parser.setContentHandler(Handler)
parser.parse(wikiDump)