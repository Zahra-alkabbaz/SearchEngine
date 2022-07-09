# SearchEngine
Built a search tool that can crawl the pages of a website, created an inverted index for all word occurrences in these pages, and provided the user with a functionality to find pages containing certain terms.


In 2021, 
I have has created a search tool which crawls the pages of the following website http://example.python-scraping.com/. For simplicity, she has filtered out some irrelevant terms such the stop words.
Brief Instructions to execute the Coursework
First, the user should open a terminal window and run the following command:
python3 SearchEngine.py
Then, the program will give the following menu for command options to be executed:



<img width="427" alt="Screenshot 2022-07-10 at 01 14 26" src="https://user-images.githubusercontent.com/71462997/178124295-79b5d76b-fe5e-4c3c-8e8a-1b1bdfbb2681.png">

Figure 1: Commands Menu after running the program.






After this, based on the user’s input the program will run one of the following functionalities. The program will show the menu again after running the command if the executed command is print or find. Otherwise, it will exit the program.




**build**


The build command calls the crawlAllAvailableUrls() function which crawls the webpages of the website after checking the permission to which pages the website gives access. The program uses the request library to send requests to the website and it waits 5 seconds after each request, prior to sending a new request. Then, it parses the page using the beautifulSoup library and downloads the content of each page in a txt file to be used later for building the inverted index. The process of downloading all the pages takes a while. Each page is given a number that is identical to the name of the txt file, such
as 0.txt. After this, the program stores a json file (url_index.json) that contains a dictionary of all the indices in the following form: { 0: “www.url1.com”, 1: “www.url2.com”}.


**load**


This command calls the createInvertedIndexForAll() which focuses on building a dictionary that represents the inverted index list and stores it into a file called inverted_index.json. It processes all the saved pages breaking them down into a dictionary of words with their number of occurrences in each page as in figure 2. In figure 2, doc refers to a page. The dictionary has the following structure:


<img width="644" alt="Screenshot 2022-07-10 at 01 23 37" src="https://user-images.githubusercontent.com/71462997/178124484-448c96d8-9c4e-4858-bfb1-803b3baa2bd2.png">
Figure 2: how the inverted list is represented in a python dictionary.




Each document has an index which can be used later to retrieve the page URL from a json file called url_index.json. Where the word could be any word in at least one document and its value is another dictionary which has the index of the page(s) in which the word is in and the number of the term occurring in the associated page.



**print**


This command takes in a word and passes it to the printIndex(word) function which checks if the word exists in the inverted list, which is in this case is a dictionary of words and their occurrences in the pages as shown in figure 2. Then, it returns part of the dictionary for this specific word. This includes the index of a document in which the word has occurred and the number of time that it has occurred. This will be followed by another form of the inverted index which substitutes the index with the associated page’s URL and the number of times of which the term occurs in that page.


<img width="1058" alt="Screenshot 2022-07-10 at 01 22 11" src="https://user-images.githubusercontent.com/71462997/178124448-aa1e6a71-1893-46b9-adfd-a3133486caad.png">
Figure 3: results of using the command “print es-SV”.


  
**find**


The find command calls the documentAtTime(query) which prints a list of all the URLs in which a given word or a phrase has appeared. First, it uses the document at a time evaluation, where it iterates over the documents that had any of the words of the query. Then, if it finds both words it returns the URL as it is considered relevant. The returned URLs will be given in descending score order. In here, the score has been accumulated using the total number of occurrences of the word(s) in the query in each page individually. Then, those with highest score were given at the top. Using the document index, the URLs which have the terms will be found from the data stored in url_index.json. The result will be given by printing the URLs to the user in the terminal.



**exit**


This command allows the user to exit the tool, and to run the tool again they will need to rerun the program from the terminal window.
