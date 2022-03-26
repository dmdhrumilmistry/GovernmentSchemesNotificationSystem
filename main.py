#!env/bin/python
from asyncio import FastChildWatcher
from bs4 import BeautifulSoup
from PyTerminalColor.TerminalColor import TerminalColor
from urllib.parse import urljoin


import json
import requests
import os


colorize = TerminalColor(style='BOLD')
all_notifications = []


def __error(message: str):
    '''
    description:
        prints formatted error message.

    params:
        message(str) : message to be printed

    returns: 
        None
    '''
    colorize.cprint(f"[X] {message}", use_default=False,
                    fgcolor='YELLOW', bgcolor='RED')


def __warn(message: str):
    '''
    description:
        prints formatted warning message.

    params:
        message(str) : message to be printed

    returns: 
        None
    '''
    colorize.cprint(f"[!] {message}", use_default=False,
                    fgcolor='BLACK', bgcolor='YELLOW')


def __success(message: str):
    '''
    description:
        prints formatted success message.

    params:
        message(str) : message to be printed

    returns: 
        None
    '''
    colorize.cprint(f"[✓] {message}", use_default=False,
                    fgcolor='GREEN', bgcolor='BLACK')


def __info(message: str):
    '''
    description:
        prints formatted info message.

    params:
        message(str) : message to be printed

    returns: 
        None
    '''
    colorize.cprint(f"[*] {message}", use_default=False,
                    fgcolor='YELLOW', bgcolor='BLACK')


def get_links(file: str = None):
    '''
    description:
        get links from the saved file. returns data in
        python dictionary if data is in valid json 
        format else prints error message and exits the
        program. 

    params:
        file (str): path of the saved file

    returns:
        dict
    '''
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
        __error("Json file is in Invalid format.")
        exit(2)


def create_dir(path: str):
    '''
    description:
        creates a directory if not present else
        prints directory already exists message.

    params:
        path (str): path of the directory to be created

    returns: 
        None
    '''
    if not os.path.exists(path):
        __success(f"{path} directory created.")
        os.makedirs(path)
    else:
        __info(f"{path} Already Exists.")


def dump_dict_data(path: str, data: dict, indent: int = 4):
    '''
    description:
        dumps json data to a file with default indent as 4,
        raises exception if json is in invalid data format
        and exits the program with error code 2.

    params:
        path (str): path of the directory to be created
        data (dict): json data to be stored in the file in dict
        indent (int): json indentation

    returns: 
        None
    '''
    if os.path.exists(path):
        __info(f"Overwriting {path} file with new data.")
    else:
        __info(f"Writing data to {path}")
    try:
        with open(path, 'w') as f:
            f.write(json.dumps(data, indent=indent))
    except json.JSONDecodeError:
        __error(f"Invalid Json Formatted data.")
        exit(2)


def url_to_json_fname(url: str):
    '''
    description:
        converts url into a valid filename and returns
        filename as a string.

    params:
        url (str): url to be converted into a filename

    returns:
        str
    '''
    return f'{url.replace("http://","").replace("https://","").replace("/","-")}.json'


def get_last_page(url: str):
    '''
    description:
        extract last page information from the html page.

    params:
        url (str): url of the page

    returns: 
        int
    '''
    # get html data
    html_doc = requests.get(url).content.decode('utf-8')

    # create soup obj using html parser
    soup = BeautifulSoup(html_doc, 'html.parser')

    # extract last notification page
    last_page = int(soup.find('li', {"class": "last"}).find(
        'a').get('href').split('?')[-1].split('=')[-1])
    return last_page


def get_latest_notifications(url: str):
    '''
    description:
        extract latest notifications from the html page
        and stores it into `all_notifications` global
        variable.

    params:
        url (str): url of the page
    
    returns: 
        None
    '''
    # get html data
    html_doc = requests.get(url).content.decode('utf-8')

    # create soup obj using html parser
    soup = BeautifulSoup(html_doc, 'html.parser')

    content_block = soup.find('div', id='content')

    # get notifications from the content block
    notifications = content_block.find(
        'div', {"class": "item-list"}).find_all('li')

    # extract notification and store it into `all_notifications`
    for notification in notifications:
        a_notification = notification.find('a')
        all_notifications.append(
            [urljoin(url, a_notification.get('href')), a_notification.contents[0]])


def get_saved_notifications(file_path: str):
    '''
    description:
        returns saved notifications from the json file
        in dictionary format. if json data is invalid 
        or file does not exists then returns False.

    params:
        file_path (str): path of the saved notifications file
    
    returns: 
        dict | False
    '''
    if not os.path.exists(file_path):
        __warn(f"{file_path} saved notifications file not found.")
        return False

    __info(f"{file_path} saved notifications found.")
    try:
        with open(file_path, 'r') as f:
            data: dict = json.loads(f.read())
        return data
    except json.JSONDecodeError:
        __error(f"{file_path} json data is in invalid format.")
        return False


def main():
    '''
    description:
        starts the main process.

    params:
        None

    returns: 
        None
    '''
    # basic conf
    saved_file_path = 'notification_data/www.india.gov.in-my-government-schemes.json'
    data_dir = os.path.join(os.getcwd(), 'notification_data')
    base_link = "https://www.india.gov.in/my-government/schemes"

    # create directory to save data
    create_dir(data_dir)

    # get saved notifications data from file
    saved_notifications = get_saved_notifications(saved_file_path)

    # get last page from website
    last_page = int(get_last_page(base_link))

    # append all the notifications from the page into
    # all_notifications list
    for page_no in range(last_page+1):
        page_link = urljoin(base_link, f'?page={page_no}')
        get_latest_notifications(page_link)
        __success(f"{page_link} notifications loaded.")

    # extract new notifications
    if saved_notifications:
        new_notifications = []
        saved_notifications = saved_notifications["urls"]
        for notification in all_notifications:
            if notification not in saved_notifications:
                new_notifications.append(notification)

        # save new schemes notification to the file
        dump_dict_data(os.path.join(data_dir, 'new_notifications.json'), {
                       "urls": new_notifications})

        # inform users about the new schemes if available
        # else inform them about all the available schemes
        if len(new_notifications) != 0:
            __info("Informing users about the new schemes.")
        else:
            __info(
                "No new schemes were published. Informing them about the all the schemes available.")
    else:
        __info("Scraping data for the first time.")

    dump_dict_data(os.path.join(data_dir, url_to_json_fname(base_link)), {
                   "urls": all_notifications})


if __name__ == '__main__':
    colorize.cprint('='*35, use_default=False, fgcolor='CYAN', style='BOLD')
    colorize.cprint('Govt. Scheme Notification System', use_default=False, fgcolor='GREEN', style='BOLD')
    colorize.cprint('='*35, use_default=False, fgcolor='CYAN', style='BOLD')
    colorize.cprint("Written By", use_default=False)
    colorize.cprint('dmdhrumilmistry', use_default=False, fgcolor='YELLOW', style='BOLD')
    colorize.cprint('-'*35, use_default=False, fgcolor='CYAN', style='BOLD')
    print()
    main()