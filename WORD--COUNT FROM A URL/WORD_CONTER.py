import csv
import string
import urllib.request
from bs4 import BeautifulSoup
from urllib.request import urlopen
from six.moves.urllib.request import urlopen
import re
import sqlite3
import sqlite3
import pandas as pd
from pandas import DataFrame


#takes the text from a html page
url = "http://www.google.com/"
html = urlopen(url)
html = html.read()
soup = BeautifulSoup(html, 'lxml')

# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    # rip it out

# get text
text = soup.get_text()

# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
text = '\n'.join(chunk for chunk in chunks if chunk)
#removes ascii errors
text = text.encode('ascii', 'ignore').decode('ascii')
#makes the text a string
text = text.split()



word_count = {}
words = text
for word in words:
    #word = word.translate(translator).lower()
    count = word_count.get(word, 0)
    count += 1
    word_count[word] = count

word_count_list = sorted(word_count, key=word_count.get, reverse=True)
for word in word_count_list[:10]:
    print(word, word_count[word])
#outputs the values in a csv
output_file = open('words.csv', 'w')
writer = csv.writer(output_file)
writer.writerow(['word', 'count'])
for word in word_count_list:
    writer.writerow([word, word_count[word]])

# to save it in a database from csv file

# You can create a new database by changing the name within the quotes
conn = sqlite3.connect('words_dat.db')

# The database will be saved in the location where your 'py' file is saved
c = conn.cursor()

# Create table - CLIENTS
### NOTE Run this only once as it will create database with the given name
### if you run it more than once it will give an error saying database already exists
c.execute('''CREATE TABLE WORDS
             ([generated_id] INTEGER PRIMARY KEY,[words] text, [word_count] integer)''')
conn.commit()

#to read a seperate csv file from local disk

#read_words = pd.read_csv (r'C:\Users\user\Downloads\Word-Occurnces-on-a-website--master\words.csv')

words.to_sql('CLIENTS', conn, if_exists='append', index = False)