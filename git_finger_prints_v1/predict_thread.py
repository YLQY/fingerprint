
from utils.print_utils import print_error,print_message,print_warning
from core.STFT.STFTMusicProcessPredict import STFTMusicProcessPredict
from database.MySQLConnector import MySQLConnector
import os
from utils.hparam import hp
import threading
import numpy as np
def predict(all_path):

    # 获取数据库的连接
    connector = MySQLConnector()

    # 获取核心的预测处理器
    music_processor = STFTMusicProcessPredict()

    # 一个一个的预测数据
    for path in os.listdir(all_path):

        try:
            # 获取音频的相对路径
            # music_path = os.path.join(hp.fingerprint.path.query_path,path)
            music_path = path
            # 预测歌曲
            music_info = music_processor.predict_music(music_path=music_path, connector=connector)

            # 根据music_info输出
            print_message("预测歌曲："+str(music_info['music_id']) + " --- 线性匹配个数为：" + str(music_info['max_hash_count'])+ " --- 歌曲偏移：" + str(music_info['music_offset']))

            pass
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
        predict(self.all_path)
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

















