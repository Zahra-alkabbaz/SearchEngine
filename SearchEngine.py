import sys
import os
import requests
import json
import time
from bs4 import BeautifulSoup
import string
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

# This class has the code needed for creating the search engine
class SearchEngine:

    def __init__(self):
        self.queue = []
        self.checked_links = []
        self.url = 'http://example.python-scraping.com'
        self.permission = {}
        self.crawl_delay = 5
        self.doc_index = {}
        self.stop_words  = stopwords.words("english")
        self.inverted_list = {}
        self.current_index = 0
        self.directory = 'WebContent'
        self.info = ['Flag:', 'Area:', 'Population:', 'Iso:', 'Country (District):', 'Capital:', 'Continent:', 'Tld:', 'Currency Code:', 'Currency Name:', 'Phone:', 'Postal Code Format:', 'Postal Code Regex:', 'Languages:', 'Neighbours:']
    
    def initializeQueue(self):
        self.crawling(self.url)

    def updateIndex(self):
        self.current_index = self.current_index + 1

    def printBorders(self):
         print ("*****************************************************************")

    # The function which proccesses user input and runs the associated functions.
    def executeCommand(self):
        self.printBorders()
        
        print ("""
        build
        load
        print
        find
        exit
        """)

        command = input("Please Enter a command option from the ones above: \n")
        
        # Checks the user input and asks for a different input if the input is invalid
        if not (command.startswith('build') or command.startswith('load') or command.startswith('print') or command.startswith('find') or command.startswith('exit')):
            print("Invalid Choice. \n") 
            self.executeCommand()

        elif command == 'build':
            self.checkPermission()
            self.initializeQueue()
            self.crawlAllAvailableUrls()
            self.writeUrlsFile()
            self.printBorders()
        
        elif command == 'load':
            # Checks if the WebContent Directory exists
            if not os.path.exists(self.directory):
                print("Please Run the build Command first")
            else:
                # Exits the program after loading
                self.resetIndex()
                self.createInvertedIndexForAll()
                self.printBorders()
            
        elif command.startswith('print'):
            word = command.partition('print ')[2].strip()
            self.printIndex(word)
            self.executeCommand()
            self.printBorders()


        elif command.startswith('find'):
            query = command.partition('find ')[2]
            query = query.split()
            self.documentAtTime(query)
            self.executeCommand()
            self.printBorders()

        elif command.startswith('exit'):
            print("\nClosing the tool .... \n")
            self.printBorders()
            sys.exit(0)


    # Checks which pages the crawler is permitted to access
    def checkPermission(self):
        # Getting the content of the url
        r = requests.get(self.url + '/robots.txt')

        # Iterating over the files in python
        lines = str(r.text).splitlines()
        number_of_lines = len(lines)
        for i in range(0, number_of_lines):
            if lines[i].strip():
                # {'User agent == *': {'Allow': [], 'Dissallow': []}
                 if lines[i].startswith('User-agent:'):
                     allow = []
                     disallow = []
                     temp = {}
                     for j in range(i, number_of_lines ):
                         if not lines[j].startswith('User-agent:'):
                             if lines[j].startswith('Allow:'):
                                 splitted_line = lines[j].split(':', maxsplit=1)
                                 allow.append(splitted_line[1].strip())

                             if lines[j].startswith('Disallow:'):
                                 splitted_line = lines[j].split(':', maxsplit=1)
                                 disallow.append(splitted_line[1].strip())

                     splitted_line = lines[i].split(':', maxsplit=1)

                     temp['Allow'] = allow
                     temp['Disallow'] = disallow
                     user_agent = splitted_line[1].strip()
                     self.permission[user_agent] = temp

                 elif lines[i].startswith('Crawl-delay:'):
                     self.crawl_delay = lines[i].split(':', maxsplit=1)[1]


    # Writes the page content in a text file
    def writeDoc(self, text):
        # Create a directory if it is not there
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        file_name = self.directory +  '/' + str(self.current_index) + '.txt'
        with open(file_name, "w") as file:
            file.write(text)
        
    # Write all urls with their index in a json file
    def writeUrlsFile(self):
        with open('url_index.json', "w+") as file:
            json.dump(self.doc_index, file)

    # Resets the index
    def resetIndex(self):
        self.current_index = 0


    # Create inverted index for all.
    def createInvertedIndexForAll(self):
        number_of_files =  len(os.listdir(self.directory))-1
        for index in range(0,number_of_files):
            self.current_index = index
            self.createInvertedIndex()
        

        # Write the inverted index to index file
        with open('inverted_index.json', "w") as file:
            json.dump(self.inverted_list, file)
            
    
    # Create an indvidual index 
    def createInvertedIndex(self):
        file_name = self.directory +  '/' + str(self.current_index) +'.txt'
        with open(file_name, "r") as file:
            lines = [l for l in (line.strip() for line in file) if l]
            punctuations = '''!()[]{};:'"\,<>/?@#$%^&*~'''
    
            for i in range(0, len(lines)):  
                # add spaces
                for key_feature in self.info:
                    lines[i] = lines[i].replace(key_feature, ' ' + key_feature + ' ')

                for p in punctuations:
                    lines[i] = lines[i].replace(p,' ')

                lines[i] = ' '.join([word for word in lines[i].split() if word not in (self.stop_words)]).strip()
                
                # inverted_list = {'word': {doc:occurrences, doc:occurrences}}
                for word in lines[i].split():
                    if word not in self.inverted_list:
                        temp = {}
                        temp[self.current_index] = 1
                        self.inverted_list[word] = temp
                    
                    if word in self.inverted_list:
                        if (self.current_index in self.inverted_list[word]):
                            self.inverted_list[word][self.current_index] += 1
                        
                        else:
                            temp = self.inverted_list[word]
                            temp[self.current_index] = 1
                            self.inverted_list[word] = temp


    # Loops over all available urls
    def crawlAllAvailableUrls(self):
        while len(self.queue)>0:
            # pops a url out of the queue to crawl further and writes its data into a text file.
            href = self.queue.pop(0)
            current_link = self.url + href
            self.checked_links.append(href)
            self.crawling(current_link)
            self.doc_index[self.current_index] = current_link
            self.updateIndex()


    def crawling(self, url):
        # getting the content of the url
        r = requests.get(url)

        # parsing the HTML of the URL
        soup = BeautifulSoup(r.text, 'html.parser')
        self.writeDoc(soup.get_text(" ",strip=True))

        # Crawling for links in that url
        for link in soup.find_all('a'):
            temp_len = len(link.contents)

            # Add to queue
            link_href = link.get('href')
            # Chekcking if this url is allowed to be accessed
            dissallow = self.permission['*']['Disallow']
            if (link_href not in self.queue and  link_href not in self.checked_links and link_href not in dissallow) :
                if ('login'  not in link_href and 'register'  not in link_href and 'edit'  not in link_href):
                    self.queue.append(link_href)
                    print(link_href)

        # 5 seconds between successive requests to the website.
        time.sleep(5)

    
    def printIndex(self, word):
        self.readInvertedList()
        self.readUrls()
        temp = {}

        # print(self.inverted_list)
        if word in self.inverted_list:
            print("\n\n************Inverted Index using Indices************:")
            print("\nThe inverted index of " + word + " as follow, using URLs indices: \n")
            print(word + ": ",self.inverted_list[word])

            print("\n\n************Inverted Index using URLs************:")
            for key in self.inverted_list[word]:
                temp[self.doc_index[key]] = self.inverted_list[word][key]
            
            print("\nThe inverted index of " + word + " as follow, using URLs: \n")
            print(word + ": ",temp)
        
        else:
            print("Sorry word is not found, try another one")
    
    # Reads the inverted index
    def readInvertedList(self):
        
        if len(self.inverted_list) == 0:
            try:
                with open('inverted_index.json', "r") as file:
                    self.inverted_list = json.load(file)
            
            except IOError:
                print("Inverted Index does not exist.")

    # Read URLs from a file if the list is empty
    def readUrls(self):
        if len(self.doc_index) == 0:
            try:
                with open('url_index.json', "r") as file:
                    self.doc_index = json.load(file)

            except IOError:
                print("Urls file does not exist.")


    # Does the search query
    def documentAtTime(self, query):
        self.readInvertedList()
        term_in_list = {}
        doc = []
        doc_temp = []
        doc_return = {}

        # creates a minimal inverted index list for the words in the query.
        for term in query:
            if term in self.inverted_list:
                term_in_list[term]= self.inverted_list[term]
                doc_temp.append(self.inverted_list[term])


        # getting all doc numbers that have these terms
        for d in doc_temp:
            for doc_num in d:
                doc.append(doc_num)
        
        # Goes over each page and counts the overall occurrenecess of all terms in the query
        for doc_num in doc:
            sd = 0
            term_appear = 0
            for term in query:
                if term in self.inverted_list and doc_num in self.inverted_list[term]:
                    term_appear +=1

                    # The score here is just the total number of times a term in the query appeared in the doc
                    sd += term_in_list[term][doc_num]

            
            if term_appear == len(query):
                doc_return[doc_num] = sd
            
            # Reads the Urls from the files
            self.readUrls()

        # Sorts the urls from highest score to lowest
        if len(doc_temp) > 0 and len(doc_return)>0 :
            doc_return = dict(sorted(doc_return.items(), key=lambda item: item[1], reverse=True))
  
            print("\n\nThe Following Search Result(s) were found: ")
            for doc in doc_return:
                print(self.doc_index[doc] + '\n')
        
        else:
            print("Sorry query is not found, try another one.")
        

        
        

def main():
    s1 = SearchEngine()
    s1.executeCommand()

if __name__ == "__main__":
    main()

