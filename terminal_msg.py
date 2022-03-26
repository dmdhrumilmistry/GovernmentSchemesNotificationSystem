from PyTerminalColor.TerminalColor import TerminalColor
colorize = TerminalColor(style='BOLD')


def error(message: str):
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


def warn(message: str):
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


def success(message: str):
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


def info(message: str):
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
