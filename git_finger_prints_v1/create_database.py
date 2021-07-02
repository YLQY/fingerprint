
import os
from utils.print_utils import print_message,print_error,print_warning
from utils.hparam import hp
from database.MySQLConnector import MySQLConnector
from core.STFT.STFTMusicProcessCreate import STFTMusicProcessCreate


def create_database():

    # 获取数据库的连接
    connector = MySQLConnector()

    # 短时傅里叶变化的处理器
    music_processor = STFTMusicProcessCreate()

    # 获取到歌曲的路径
    for path in os.listdir(hp.fingerprint.path.music_path):

        try:
            # 获得歌曲的路径
            music_path = os.path.join(hp.fingerprint.path.music_path,path)

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




if __name__ == '__main__':
    create_database()










