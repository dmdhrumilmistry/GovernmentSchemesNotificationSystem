#!env/bin/python
from bs4 import BeautifulSoup
from PyTerminalColor.TerminalColor import TerminalColor

import json
import requests
import os

colorize = TerminalColor(style='BOLD')


def __error(message:str):
    colorize.cprint(f"[X] {message}", use_default=False, fgcolor='YELLOW', bgcolor='RED')

def __warn(message:str):
    colorize.cprint(f"[!] {message}", use_default=False, fgcolor='BLACK', bgcolor='YELLOW')

def __success(message:str):
    colorize.cprint(f"[✓] {message}", use_default=False, fgcolor='GREEN', bgcolor='BLACK')

def __info(message:str):
    colorize.cprint(f"[*] {message}", use_default=False, fgcolor='YELLOW', bgcolor='BLACK')


def get_links(file:str=None):
    if not os.path.exists(file):
        __error("Links File not found!")
        exit(2)
    else:
        __success(f"Using {file} file for links.")
    try:
        with open(file, 'r') as f:
            data = json.loads(f.read())
        return data
    except json.JSONDecodeError:
        __error("Invalid File")
        exit(2)


def get_latest_notification(url:str):
    # get html data
    html_doc = requests.get(url).content.decode('utf-8')
    
    # create soup obj using html parser
    soup = BeautifulSoup(html_doc, 'html.parser')

    # extract last notification page
    last_page = soup.find('li', {"class":"last"}).find('a').get('href').split('?')[-1].split('=')[-1]
    
    print(soup.title.string)
    content_block = soup.find('div', id='content')
    
    notifications = content_block.find('div', {"class":"item-list"}).find_all('li')
    for notification in notifications:
        a_notification = notification.find('a')
        print(a_notification.contents[0], a_notification.get('href'))


if __name__ == '__main__':
    # basic conf
    links_file_path = 'links.json'
    check_for = "India"

    # get data from file
    links:dict = get_links(links_file_path)

    # get target links and extract data
    target_links = links.get(check_for, None)
    if target_links.__iter__:
        for target_link in target_links:
            get_latest_notification(target_link)
