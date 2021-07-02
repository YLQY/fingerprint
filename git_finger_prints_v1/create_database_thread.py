
import os
from utils.print_utils import print_message,print_error,print_warning
from utils.hparam import hp
from database.MySQLConnector import MySQLConnector
from core.STFT.STFTMusicProcessCreate import STFTMusicProcessCreate
import numpy as np
import threading


def create_database(all_path):
    # 获取数据库的连接
    connector = MySQLConnector()

    # 短时傅里叶变化的处理器
    music_processor = STFTMusicProcessCreate()

    # 获取到歌曲的路径
    for path in all_path:

        try:
            # 获得歌曲的路径
            # music_path = os.path.join(hp.fingerprint.path.music_path, path)
            music_path = path

            # 创建指纹而且保存到数据库中
            music_processor.create_finger_prints_and_save_database(
                music_path=music_path,
                connector=connector
            )

        # 异常处理
        except BaseException as e:
            print_error("Error :" + str(path) + "\n" + str(e))
            continue
        pass

    pass


class MyThread(threading.Thread):

    def __init__(self,all_path):
        super(MyThread, self).__init__()
        self.all_path = all_path
        pass

    def run(self) -> None:
        create_database(self.all_path)
        pass




if __name__ == '__main__':
    # 拿到全部歌曲的路径
    path_list = []
    for path in os.listdir(hp.fingerprint.path.music_path):
        path = os.path.join(hp.fingerprint.path.music_path,path)
        path_list.append(path)

    # 等分路径
    path_list = np.array_split(path_list, hp.fingerprint.thread_num)
    print_message(path_list)

    # 一个一个的开启线程
    thread_list = []
    for path in path_list:
        t = MyThread(path)
        thread_list.append(t)

    for thread_ in thread_list:
        thread_.run()










