import abc
import hashlib
import numpy as np
from utils.print_utils import print_message
from utils.hparam import hp
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import generate_binary_structure,binary_erosion,iterate_structure
import matplotlib.pyplot as plt

# 音乐的处理器
class IMusicProcessor():

    # 计算Hash
    @abc.abstractmethod
    def _calculation_hash(self,music_path):
        raise NotImplementedError(u"出错了，你没有实现_calculation_hash抽象方法")


    # 语音的预处理，会生成频谱图
    @abc.abstractmethod
    def _pre_music(self, music_path):
        raise NotImplementedError(u"出错了，你没有实现_pre_music抽象方法")


    # 处理频谱图
    def _spectrogram_handle(self, spectrogram):
        """
        处理频谱图
        :param spectrogram: 频谱图
        :return: 处理之后的频谱图
        """

        # 得到除去0之外的最小值
        min_ = np.min(spectrogram[np.nonzero(spectrogram)])

        # 用得到的最小值，替换全0
        spectrogram[spectrogram == 0] = min_

        # 获取能量对数
        spectrogram = 10 * np.log10(spectrogram)

        # 防止取对数之后，有负无穷的存在
        spectrogram[spectrogram == np.inf] = 0

        # 返回处理之后的频谱图
        return spectrogram

    # 通过频谱图得到peakes
    def _fingerprint(self, spectrogram):
        """
        通过频谱图得到peakes
        :param spectrogram: 频谱图
        :return: 局部最大值点集合
        """
        # maximun_filter
        struct = generate_binary_structure(2,1)
        neighborhood = iterate_structure(struct,hp.fingerprint.core.neighborhood)
        # 取得局部最大值点
        local_max = maximum_filter(spectrogram,footprint=neighborhood) == spectrogram

        # 获取局部最大的能量值
        amps = spectrogram[local_max]

        # 拉平
        amps = amps.flatten()

        # 拿到局部最大值点的时间和频率两个维度
        j,i = np.where(local_max)

        # 得到局部最大值点
        peakes = list(zip(i,j,amps))

        # 过滤了阈值之后的东西
        peakes = [item for item in peakes if item[2] > hp.fingerprint.core.amp_min]

        # 画图函数星座图
        if hp.fingerprint.show_plot.create_database.planisphere_plot:
            self._draw_planisphere_plot(peakes)
            pass

        # 时间
        time_id = [item[0] for item in peakes]

        # 频率
        freq_id = [item[1] for item in peakes]

        # 包装起来
        peakes = list(zip(time_id,freq_id))

        return peakes

    # 通过peakes得到Hash
    def _generate_hashes(self, peakes):
        """
        通过peakes得到Hash
        :param peakes: 局部最大值点
        :return: Hash[(hash,t1),(hash,t1)]
        """
        # 对时间排序
        peakes = sorted(peakes)

        # 锚点
        for i in range(len(peakes)):
            # 紧邻点
            for j in range(1,hp.fingerprint.core.near_num):
                # 防止下表越界
                if i + j < len(peakes):
                    # 两个点的时间
                    t1 = peakes[i][0]
                    t2 = peakes[i + j][0]

                    # 两个点的频率
                    f1 = peakes[i][1]
                    f2 = peakes[i + j][1]

                    # 计算时间间隔
                    t_delta = t2 - t1
                    if hp.fingerprint.core.min_time_delta<=t_delta<=hp.fingerprint.core.max_time_delta:
                        # 计算Hash
                        hash_str = "%s|%s|%s" % (f1,f2,t_delta)
                        # 生成Hash
                        hash_str = hashlib.sha1(hash_str.encode("utf-8"))
                        yield hash_str.hexdigest(),t1
                    pass
                pass
            pass

        pass

    # 绘图函数
    def _draw_planisphere_plot(self,peakes):

        x_and_y = [(item[1],item[0]) for item in peakes]

        # x坐标
        x = [item[0] for item in x_and_y]
        # y坐标
        y = [item[1] for item in x_and_y]

        plt.scatter(x, y,marker='x')
        plt.show()

        pass

    pass














