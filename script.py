"""
    Run: python script.py <start-page>
"""

import requests
from bs4 import BeautifulSoup
import sys
import re


def removeBracer(string):
    new_string  = ""
    bracer = False
    quotes = False

    for char in string:

        if char == '(' and not quotes:
            bracer += 1
        elif char == ')' and not quotes:
            bracer -= 1
        elif char == '"' and quotes:
            quotes = False
        elif char == '"' and not quotes:
            quotes = True
        elif bracer == 0 or quotes:
            new_string += char

    return new_string


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Usage: python script.py <start_page_title>')
        sys.exit()

    main_page = 'https://en.wikipedia.org'
    start_page_str = main_page + '/wiki/' + sys.argv[1]
    start_page = requests.get(start_page_str)
    soup = BeautifulSoup(start_page.text, 'lxml')
    current_title = soup.find('h1', attrs={'class' : 'firstHeading'}).text

    previous = {}
    previous[current_title] = True

    while current_title != 'Philosophy':
        next_to_visit = ""
        print(current_title)

        # div mw-parser-output, this contains all writing for wiki page
        main_content = soup.find('div', attrs={'class' : 'mw-parser-output'})

        # paragraph contains first test in wiki page
        all_paragraph = main_content.findAll('p')
        for p in all_paragraph:
            found = False
            text = BeautifulSoup(removeBracer(str(p)), 'lxml')
            links = text.findAll('a')
            if links:
                for link in links:
                    if 'href' in str(link) and 'wiki' in link['href']:
                        next_to_visit = link['href']
                        current_title = link['href'].split('/')[-1]
                        found = True
                        break
            if found:
                break
        if next_to_visit:
            req = requests.get(main_page + next_to_visit)
            soup = BeautifulSoup(req.text, 'lxml')
        else:
            print('Something went wrong')
            sys.exit()

        if current_title in previous:
            print('loop was found before Philosophy')
            sys.exit()
        else:
            previous[current_title] = True

    print('Philosophy')
