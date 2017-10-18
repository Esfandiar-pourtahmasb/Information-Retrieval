#function "html2txt_save" is to save all the HTML file which are under a named filepath to one and another txt file, which
#are under the same filepath and named after the corresponding HTML file.
from bs4 import BeautifulSoup
import glob
import re
import html2text
import os
import string
from nltk.stem.porter import * 
stemmer = PorterStemmer()  
import html2text
import nltk
from nltk.corpus import stopwords
from collections import Counter

def convert_old(html):
    soup = BeautifulSoup(html, "lxml")
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text
#convert HTML file to readable text file
def convert(html):
    content = html2text.html2text(html)
    content = re.sub(r'^\[!\[AustLII\].*\][\r\n]*', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\*\* AustLII: \*\*.*[\r\n]*', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\*\*You are here:\*\*.*[\r\n]*', '', content, flags=re.MULTILINE)
    content = re.sub(r'^---\|--- *[\r\n]*', '', content, flags=re.MULTILINE)
    content = re.sub(r'^--- *[\r\n]*', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\| *[\r\n]*', '', content, flags=re.MULTILINE)
    content = re.sub(r'URL: .*[\r\n]*', '', content, flags=re.MULTILINE)
    content = re.sub(r'\(\/cgi-[\r\n]*bin\/LawCite.*[\r\n]*.* \)', r' <LawCite> ', content, flags=re.MULTILINE)
    content = re.sub(r'^ \[\[Name.*[\r\n]*', '', content)
    content = re.sub(r'^\[\[Databases\].*[\r\n]*', '', content)
    content = re.sub(r'^\[\[Search\].*[\r\n]*', '', content)
    content = re.sub(r'\[\[Database Search]\(.*[\r\n].*[\r\n].*[\r\n].*[\r\n].*\)\]', '', content, flags=re.MULTILINE)
    content = re.sub(r' s [.]*\d*[a-zA-Z]*\s*(\([0-9a-zA-Z]*\))*(\[[\w\d\s\(\).\[\]]*?\]\(http[^\)]*?cases[\s\S]*?\))*',' <case>',content,flags=re.MULTILINE)   
    content = re.sub(r'(\[[\w\d\s\(\).\[\]]*?\])*\(http[^\)]*?legis[\s\S]*?\)',' <legislation> ',content,flags=re.MULTILINE)
    content = re.sub(r'\[[\w\d\s\(\).\[\]]*?\]\(http[^\)]*?cases[\s\S]*?\)',' <case> ',content,flags=re.MULTILINE)
    content = re.sub(r'(AustLII:)*\s*\(\/austlii[/a-zA-Z.]*?html\)',r'',content,flags = re.MULTILINE)
    content = content.replace("_", "")
    content = content.replace("`", "'")
    content = content.replace("\\.", ".")
    content = content.replace("\-", "-")
    content = content.replace("&amp;", "&")
    content = content.replace("|", "")
    content = re.sub(r'^(.*[\r\n]*)*?\* \* \*','',content)
    content = re.sub(r'^\*\*\*.*[\r\n]*','',content)
    content = re.sub(r'^\s*[0-9]*[.] ','',content, flags=re.MULTILINE)
    content = re.sub(r'##','',content)
    content = re.sub(r'\*+','',content, flags=re.MULTILINE)
    content = re.sub(r'\-+','',content, flags=re.MULTILINE)
    content = re.sub(r'\*\*$','',content, flags=re.MULTILINE)
    content = re.sub(r'^[ >]*','',content,flags=re.MULTILINE)
    for i in range(100):
        content = re.sub(r'^(["][^"]*)[\r\n]([^>])',r'\1 \2',content, flags=re.MULTILINE)
    content = re.sub(r'\([\d\w]*\) *','',content,flags=re.MULTILINE) 
    content = content.replace("_", "")
    content = content.replace("\\.", ".")
    content = content.replace("\-", "-")
    content = content.replace("&amp;", "&")
    content = content.replace("(NSW)","")  
    content = re.sub(r'^Case Name:([\s\S]*)(^Decision:)',r'\n\2',content,flags=re.MULTILINE)
    content = re.sub(r'^Legislation Cited:([\s\S]*)(^JUDGMENT)',r'\n\2',content,flags=re.MULTILINE)
    content = re.sub(r'^Count[\r\n]*Offence[\r\n]*Sentence[\s\S]*','',content,flags=re.MULTILINE)
    for i in range(100):
        content = re.sub(r'^(Catchwords:[\r\n]*[^\r\n]*)[\r\n]([^\r\n])',r'\1 \2',content,flags=re.MULTILINE)
        content = re.sub(r'^(Decision:[\r\n]*[^\r\n]*)[\r\n]([^\r\n\s])',r'\1 \2',content,flags=re.MULTILINE)
    for i in range(2):
        content = re.sub(r'\[[^\[\]]*?\]','',content,flags=re.MULTILINE)
    content = re.sub(r' \(*at .*?\)',r' ',content,flags = re.MULTILINE)
    content = re.sub(r'\(ROS [\d-]*\)','',content,flags=re.MULTILINE)
    content = re.sub(r'^\d*','',content,flags=re.MULTILINE)
    content = re.sub(r' \([a-z]\) ',r' ',content,flags = re.MULTILINE)
    content = re.sub(r'([,()\d\w<>:"&])\s*[\n]+([a-zA-Z<>"() .,?!$;/])',r'\1 \2',content,flags=re.MULTILINE)
    content = re.sub(r'\s\s',r' ',content,flags=re.MULTILINE)
    content = re.sub(r'\n+',r'\n\n',content,flags = re.MULTILINE)
    return content

def get_html_content(tag):
    return ''.join(tag.findAll(text=True))

def remove_non_ascii(text):
    result = ''
    for i in text:
        if ord(i) < 128:
            result = result + i
        else:
            result = result + ' '
    return result
#get words from text
def get_tokens(text):
    lowers = text.lower()
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
    no_punctuation = lowers.translate(remove_punctuation_map)
    tokens = nltk.word_tokenize(no_punctuation)
    return tokens
#filter the stop words such as preposition/article/demonstrative pro-noun.
def stemandfilter_tokens(tokens,stemmer):
    filtered = [w for w in tokens if not w in stopwords.words('english')]
    return filtered

def word_split(text):
    word_list=[]
    tokens = get_tokens(text)
    text_list = stemandfilter_tokens(tokens,stemmer)   
    for w in text_list:
        word_list.append(w.lower())  
    return word_list
#save one text to local path
def html2txt_save_one(filepath, file):
    child = os.path.join(filepath, file)
    html = open(child, 'r', encoding='utf-8').read()

    newtxt = convert(html)
    newtxt = word_split(newtxt)
    if os.path.isfile(os.path.join('./trans_files/ori_files', file.replace('.html','.txt'))):
        pass
    else:
        f=open(os.path.join('./trans_files/ori_files', file.replace('.html','.txt')), "w", encoding='utf-8')
        f.write(' '.join(newtxt))
        f.close()
#save a number of texts to local path
def html2txt_save(filepath):
    pathDir =  os.listdir(filepath)
    for allDir in pathDir:
        if allDir.endswith('.html'):
            child = os.path.join(filepath,allDir)
            html = open(child, 'r',encoding='utf-8').read()
            txt = convert(html)
            newtxt = word_split(txt)
            if os.path.exists(os.path.join('./trans_files/ori_files',allDir.replace('.html','.txt'))):
                pass
            else:
                f=open(os.path.join('./trans_files/ori_files',allDir.replace('.html','.txt')),"w",encoding='utf-8')
                f.write(' '.join(txt))
                f.close()

