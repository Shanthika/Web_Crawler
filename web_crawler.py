import urllib.request
import re
import os
import http.client
import nltk
from bs4 import BeautifulSoup
from urllib.request import urlopen
from readability.readability import Document


def user_input():
    #print("Enter the Keyword/s. [use - instead of space for more than one word]")
    #keyword = [x for x in input("Search For :").split('-')]
    #print(keyword)
    read_input=open("input.txt","r")
    keyword=[]
    for f in read_input:
    	keyword=f.split()[0]
    collect_urls(keyword)




def collect_urls(keyword):
    try:
        opener = urllib.request.build_opener()
        
        opener.addheaders = [('User-agent','Chrome/35.0.1916.47')]
        
        file = open("links.txt","w",encoding="utf-8")
        
        for searchWord in keyword:
            url = "http://www.google.com/search?q="+ searchWord +"&start="
            page = opener.open(url)
            soup = BeautifulSoup(page,"html.parser")
            
            for cite in soup.find_all('cite'):
                file.write(cite.text)
                file.write("\n")
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
                    soup = BeautifulSoup(readable_article,"lxml")

                    forWrite.write(readable_title)
                    forWrite.write("\n")
                    forWrite.write(soup.text[:5000] + '[...]\"')
                       
                else:
                    con = urlopen("http://"+eachLine).read()
                    readable_article = Document(con).summary()
                    readable_title = Document(con).title()
                    soup = BeautifulSoup(readable_article,"lxml")

                    forWrite.write(readable_title)
                    forWrite.write("\n")
                    forWrite.write(soup.text[:5000] + '[...]\"')
    


            except(urllib.request.HTTPError, urllib.request.URLError, http.client.HTTPException, http.client.IncompleteRead, BaseException):
                continue
    
    forWrite.close()
    forRead.close()


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


def do():
    user_input()
    validate_urls()
    fetch_text()
    clean_fetched_data()
do()





