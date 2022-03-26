# GovernmentSchemesNotificationSystem (GSNS)

There are several schemes available from the Government of India [(GoI)](https://www.india.gov.in/) but most of the citizens are unaware about their advantages and details. GSNS is written in `Python3` to fetch the latest schemes from the website and notify users about the latest schemes available via email.

## Pre-Installation Requirements
- [Git](https://git-scm.com/)
- [Python 3](https://www.python.org/)

## Installation

- Clone/Download Repo
    ```bash
    git clone https://github.com/dmdhrumilmistry/GovernmentSchemesNotificationSystem.git
    ```
- Install project requirements
    ```bash
    pip install -r requirements.txt
    ```
- Start Application
    ```bash
    python main.py
    ```
    > `Note` : When you run the project for first time, it'll fetch all the schemes and save into a json file, the users will be notified about the schemes. After this, only new schemes will be saved into a new json file and notify users about it.