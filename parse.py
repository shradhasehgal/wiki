import sys
import xml.sax
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords 
import re
from datetime import datetime

class ParsingHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.text = ""
        self.title = ""
        self.docID = 0
        self.tag = ""
    
    def startElement(self, tag, attributes):
        self.tag = tag

    def endElement(self, tag):
        if tag == "page":
            index(self.title, self.text, self.docID)
            self.title = ""
            self.text = ""
            self.docID += 1

    def characters(self, content):
        if self.tag == "title":
            self.title += content
        elif self.tag == "text":
            self.text += content

WORD = re.compile(r'\w+')
stop_words = set(stopwords.words('english')) 
stems = {}
stemmer = SnowballStemmer("english")
overallDict = {}

def tokenize(text):
    words = WORD.findall(text)
    filtered = []
    for w in words: 
        if w not in stop_words:
            if w not in stems:
                stemmed_w = stemmer.stem(w)
                filtered.append(stemmed_w)
                stems[w] = stemmed_w
            else:
                filtered.append([stems[w]])

    return filtered

def index(title, text, docID):
    title = title.lower()
    text = text.lower()
    titleWords = tokenize(title)  
    # bodyWords = tokenize(text)
    
    
    # Infobox
    infoboxWords = []
    infobox = text.split("{{infobox")
    # infobox = re.findall(r"{{infobox(.|\n)*}}", text)
    if len(infobox) > 1:
        infobox = infobox[1].split("}}", 1)
        # print(infobox[0])
    # if infobox:
        # print(infobox)
        infoboxWords = tokenize(str(infobox[0]))

    # Category
    categoryWords = []
    categories = re.findall(r"\[\[category:(.*)\]\]", text)
    if categories:
        categories = " ".join(categories)
        categoryWords = tokenize(categories)

    # Links
    linkWords = []
    links = text.split("==external links==")
    if len(links) > 1:
        links = links[1].split("\n")
        linksInfo = ""
        for line in links:
            if line and line[0] == '*':
                linksInfo += line+" "
        linkWords = tokenize(linksInfo)


    # References
    refWords = []
    refs = text.split("==references==")
    if len(refs) > 1:
        refs = refs[1].split("\n")
        refsInfo = ""
        for line in refs:
            if ("[[category" in line) or ("==" in line) or ("defaultsort" in line):
                break
            refsInfo += line+"\n"
        refWords = tokenize(refsInfo)

    for word in titleWords:
        if word in overallDict:
            overallDict[word][0] += 1
        else:
            overallDict[word] = [1, 0, 0, 0, 0]
    
    for word in infoboxWords:
        if word in overallDict:
            overallDict[word][1] += 1
        else:
            overallDict[word] = [0, 1, 0, 0, 0]

    for word in categoryWords:
        if word in categoryWords:
             overallDict[word][2] += 1
        else:
            overallDict[word] = [0, 0, 1, 0, 0]

    for word in linkWords:
        if word in linkWords:
             overallDict[word][3] += 1
        else:
            overallDict[word] = [0, 0, 0, 1, 0]

    for word in refWords:
        if word in refWords:
             overallDict[word][4] += 1
        else:
            overallDict[word] = [0, 0, 0, 0, 1]
        
    

wikiDump = sys.argv[1]
# create an XMLReader
begin = datetime.now()
parser = xml.sax.make_parser()
# turn off namepsaces
parser.setFeature(xml.sax.handler.feature_namespaces, 0)
Handler = ParsingHandler()
parser.setContentHandler(Handler)
parser.parse(wikiDump)
parse_end = datetime.now()
print("time to parse is ", parse_end-begin)