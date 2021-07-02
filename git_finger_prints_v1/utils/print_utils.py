
from termcolor import colored



# 打印错误信息
def print_error(message):
    '''
    打印错误信息
    :param message: 提示信息
    :return: None
    '''
    print(colored(message, 'red'))
    pass


# 打印正常信息
def print_message(message):
    '''
    打印正常信息
    :param message: 提示信息
    :return: None
    '''
    print(colored(message, 'cyan'))
    pass


# 打印警告
def print_warning(message):
    """
    打印警告
    :param message: 提示信息
    :return: None
    """
    print(colored(message, 'yellow'))
    pass









