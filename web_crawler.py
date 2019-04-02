import re
import os
import string
import urllib.request
import nltk
import http.client
from bs4 import BeautifulSoup
from urllib.request import urlopen
from readability.readability import Document
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from random import randint


def user_input():
    read_input=open("input.txt","r")
    keyword=[]
    for f in read_input:
        keyword.append(f.split()[0])
    

    collect_urls(keyword)




def collect_urls(key):
    try:
        #urllib.request.build_opener() returns an OpenerDirector instance, which chains the handlers in the order given.
        #The OpenerDirector class opens URLs.
        opener = urllib.request.build_opener()

        #headers are dictionary that accepts a key and a value.
        #User-agent header is used by a browser to identify itself.
        #here Mozilla5.0 is used as a browser.
        opener.addheaders = [('User-agent', 'Chrome/35.0.1916.47')]

        #opens the text file links.txt in write mode which is assigned to a file-object file
        file = open("links.txt", "w",encoding="utf-8")
        for searchWord in key:
            #url format appended with the keyword to be searched
            url = "http://www.google.com/search?q="+ searchWord +"&start="

            #opens the webpage in the browser with the above url
            page = opener.open(url)

            #specifies that the html parser is used to parse the data returned from the page
            soup = BeautifulSoup(page, "html.parser")

            #soup.find_all() method will perform a match against that of argument provided
            #here each match is the url of the cite which is written in the file links.txt
            for cite in soup.find_all('cite'):
                file.write(cite.text)
                file.write("\n")
            file.write("----------------------------------------------------------------------------")
            file.write("\n")
        file.close()
       

    except (urllib.request.HTTPError, urllib.request.URLError, http.client.HTTPException, BaseException):
        pass

def validate_urls():
    forWrite = open("Validlinks.txt","w")
    with open("links.txt") as forRead:
        for eachLine in forRead:
            if eachLine.find("en") >= 0 and \
               eachLine.find("youtube") == -1 and \
               eachLine.find("facebook") == -1 and \
               eachLine.find("imdb") == -1 and \
               eachLine.find("...") == -1:
                forWrite.write(eachLine)
    forWrite.close()
    forRead.close()
    print("Check the file Validlinks.txt for results")
        #deletes 'links.txt' file
    if os.path.exists("links.txt"):
        os.remove("links.txt")
    else:
        print("File does not exists!!")
def fetch_text():
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Chrome/35.0.1916.47')]

    # opens text file to store data from each links
    forWrite = open("web_data.txt", "w")
    forRead = open("Validlinks.txt", "r")

    # removes HTML formatting of the text and collects only plain text/data 
    with open("Validlinks.txt") as forRead:
        for eachLine in forRead:
            try:
                if eachLine.startswith("http"):
                    con = urlopen(eachLine).read()
                    readable_article = Document(con).summary()
                    readable_title = Document(con).title()
                    
                else:
                    con = urlopen("http://"+eachLine).read()
                    readable_article = Document(con).summary()
                    readable_title = Document(con).title()

                soup = BeautifulSoup(readable_article,"lxml")

            except(urllib.request.HTTPError, urllib.request.URLError, http.client.HTTPException, http.client.IncompleteRead, BaseException):
                continue

            try:
                # adds delimeter '|' at the end of portion of text from each link
                result = soup.text[:8000]+'|'
                forWrite.write(result)

                # line break to indicate the following portion of text is from another link
                if re.match('|',result) != None:
                     forWrite.write("\n")
                
            except (SystemError, UnicodeEncodeError):
                continue
         
    forWrite.close()
    forRead.close()
    #print("check links.txt!")


def clean_fetched_data(): 
    forRead = open("web_data.txt","r")
    newFile = open("WebData.txt", "w")

    # cleans the text file for newlines
    for eachLine in forRead:
        if eachLine.rstrip():
            newFile.write(eachLine)
    print("Fetched data modified.")
    forRead.close()
    newFile.close()
    #deletes 'web_data.txt' file
    if os.path.exists("web_data.txt"):
        os.remove("web_data.txt")
    else:
        print("File does not exists!!")


def tokenize_text():
    newFile = open("WebData.txt","r")
    readText = newFile.read()
    newFile.close()

    # tokenize each senetence in text file
    senTokens = nltk.sent_tokenize(readText)
    senTokens = [w.lower() for w in senTokens]
    newFile = open("WebData.txt","w")

    # stores in same file sentence-wise
    for stk in senTokens:
        newFile.write(""+stk)
        newFile.write("\n")
    newFile.close()


def tokenize_words():
    
    newFile = open("WebData.txt","r")
    text = newFile.read()
    newFile.close()        
    wordTokens = nltk.word_tokenize(text)

    # remove punctuation from each word
    table = str.maketrans('','',string.punctuation)
    stripped = [w.translate(table) for w in wordTokens]

    # remove remaining tokens that are not alphabetic/numeric
    checkWords = [word for word in stripped if word.isalnum()]
    
    filename=os.listdir("./static")
    if(len(filename)!=0):
        rm_file="./static/"+filename[0]
        os.system('rm '+rm_file)        

    rm = randint(1,1000)
    f_name="./newData.txt"
    newFile = open(f_name,"w")

    # stores in same file sentence-wise
    for wt in checkWords:
        newFile.write(" "+wt)
        #newFile.write("\n")
    newFile.close()

    #deletes 'web_data.txt' file
    if os.path.exists(" WebData.txt"):
        os.remove("WebData.txt")
    else:
        print("File does not exists!!")
    print("Check the file newData.txt for data!")

def do():
    user_input()
    validate_urls()
    fetch_text()
    clean_fetched_data()
    tokenize_text()
    tokenize_words()
do()





