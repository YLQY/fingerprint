
import abc
from core.ICore.IMusicProcessor import IMusicProcessor


class IMusicProcessorCreate(IMusicProcessor):

    # 创建指纹而且保存到数据库中
    @abc.abstractmethod
    def create_finger_prints_and_save_database(self,music_path,connector):
        raise NotImplementedError(u"出错了，你没有实现create_finger_prints_and_save_database抽象方法")



    # 处理Hash
    @abc.abstractmethod
    def _calculation_hash(self,music_path):
        raise NotImplementedError(u"出错了，你没有实现_calculation_hash抽象方法")



    # 语音的预处理，会生成频谱图
    @abc.abstractmethod
    def _pre_music(self, music_path):
        raise NotImplementedError(u"出错了，你没有实现_pre_music抽象方法")



    pass













