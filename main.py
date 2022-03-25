#!env/bin/python
from bs4 import BeautifulSoup
from PyTerminalColor.TerminalColor import TerminalColor
from urllib.parse import urljoin


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


def create_dir(path:str):
    if not os.path.exists(path):
        __success(f"{path} directory created.")
        os.makedirs(path)
    else:
        __info(f"{path} Already Exists.")


def dump_dict_data(path:str, data:dict):
    if os.path.exists(path):
        __info(f"Overwriting {path} file with new data.")
    else:
        __info(f"Writing data to {path}")
    try:
        with open(path, 'w') as f:
            f.write(json.dumps(data, indent=4))
    except json.JSONDecodeError:
        __error(f"Invalid Json Formatted data.")
        exit(2)
    

def url_to_json_fname(url:str):
    return f'{url.replace("http://","").replace("https://","").replace("/","-")}.json'


def get_latest_notifications(url:str, last_page:int=False):
    all_notifications = []
    # get html data
    html_doc = requests.get(url).content.decode('utf-8')
    
    # create soup obj using html parser
    soup = BeautifulSoup(html_doc, 'html.parser')

    # extract last notification page
    last_page = soup.find('li', {"class":"last"}).find('a').get('href').split('?')[-1].split('=')[-1]
    
    content_block = soup.find('div', id='content')
    
    notifications = content_block.find('div', {"class":"item-list"}).find_all('li')
    for notification in notifications:
        a_notification = notification.find('a')
        all_notifications.append((urljoin(url, a_notification.get('href')), a_notification.contents[0]))

    return {"url": all_notifications}


if __name__ == '__main__':
    # basic conf
    links_file_path = 'links.json'
    check_for = "India"
    data_dir = os.path.join(os.getcwd(), 'notification_data')

    # create directory to save data
    create_dir(data_dir)

    # get data from file
    links:dict = get_links(links_file_path)

    # get target links and extract data
    target_links = links.get(check_for, None)
    if target_links.__iter__:
        for target_link in target_links:
            dump_dict_data(os.path.join(data_dir, url_to_json_fname(target_link)), get_latest_notifications(target_link))