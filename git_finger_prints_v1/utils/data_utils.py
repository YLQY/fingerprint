

import time
from utils.print_utils import print_message,print_warning,print_error


# 开始计时
def start_time():
    """
    # 开始计时
    :return: 开始的时间
    """
    return time.time()

# 结束计时
def end_time(start_time,message):
    """
    结束计时
    :param start_time: 开始的时间
    :param message: 函数的功能
    :return: 空
    """
    dur = time.time() - start_time
    print_warning(message + "："+str(dur)+"s")
    pass













