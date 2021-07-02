

from core.ICore.IMusicProcessorPredict import IMusicProcessorPredict
import numpy as np
import librosa
from utils.hparam import hp
from utils.data_utils import start_time,end_time
import matplotlib.pyplot as plt

class STFTMusicProcessPredict(IMusicProcessorPredict):

    # 预测歌曲
    def predict_music(self,music_path,connector):

        if hp.fingerprint.show_time:
            start = start_time()

        # 计算Hash
        hash = list(self._calculation_hash(music_path=music_path))

        if hp.fingerprint.show_time:
            end_time(start,"计算Hash费时")

        # 看是否开启了显示时间
        if hp.fingerprint.show_time:
            start = start_time()
        # todo 这个方法没有调用
        # 根据Hash再数据库中查找，[hash,offset]
        match_hash_list = set(connector.find_match_hash(hashes=hash))

        if hp.fingerprint.show_plot.predict_plot.hash_plot:
            self._show_line_plot(match_hash_list)

        if hp.fingerprint.show_time:
            end_time(start,"在数据库中查找花费")

        return self._align_match(match_hash_list)

    # 匹配的核心
    def _align_match(self,match_hash_list):

        # 最终返回的歌曲id
        music_id = -1
        # 最终返回的歌曲的offset
        music_offset = -1
        # 返回的歌曲的hash个数
        max_hash_count = -1
        # 处理结果
        result = {}

        # 这个指纹是那首歌曲的，这个指纹在数据库中的偏移，这个指纹在query中的偏移
        for matches in match_hash_list:

            music_id_fk,offset_database,offset_query = matches

            offset = int(int(offset_database) - int(offset_query))

            # 如果offset不存在字典里，则添加进去
            if offset not in result:
                result[offset] = {}

            if music_id_fk not in result[offset]:
                result[offset][music_id_fk] = 0

            # 统计在当前偏移下歌曲的出现次数
            result[offset][music_id_fk] += 1

            if result[offset][music_id_fk] > max_hash_count:
                # 赋值歌曲匹配的最大个数
                max_hash_count = result[offset][music_id_fk]
                # 赋值歌曲id
                music_id = music_id_fk
                # 赋值歌曲的offset
                music_offset = offset
                pass
            pass

        return {
            "music_id":music_id,
            "music_offset":music_offset,
            "max_hash_count":max_hash_count
        }


    # 计算指纹
    def _calculation_hash(self,music_path):
        """
        计算指纹
        :param music_path: 音频路径
        :return: 指纹[(hash,t1),(hash,t1)]
        """
        # 语音的预处理，会生成频谱图
        spectrogram = self._pre_music(music_path)

        # 处理频谱图
        spectrogram = self._spectrogram_handle(spectrogram)

        # 通过频谱图得到peakes
        peakes = self._fingerprint(spectrogram)

        # 通过peakes得到Hash
        return self._generate_hashes(peakes)

    # 语音的预处理，会生成频谱图
    def _pre_music(self, music_path):
        """
        语音的预处理，会生成频谱图
        :param music_path: 音频路径
        :return: 频谱图
        """
        # 加载歌曲
        y, sr = librosa.load(music_path, sr=hp.fingerprint.core.stft.sr)

        # 做短时傅里叶变化
        arr2D = librosa.stft(
            y,
            n_fft=hp.fingerprint.core.stft.n_fft,
            hop_length=hp.fingerprint.core.stft.hop_length,
            win_length=hp.fingerprint.core.stft.win_length
        )

        # 得到频谱矩阵
        return np.abs(arr2D)

    # 绘制线性关系的图
    def _show_line_plot(self,match_hash):
        # [1,t1,t2]
        print(match_hash)

        c = [item[0] for item in match_hash]

        x_and_y = [(item[1],item[2]) for item in match_hash]

        x = [int(item[0]) for item in x_and_y]
        y = [int(item[1]) for item in x_and_y]

        plt.scatter(x,y,c=c,marker='o')

        plt.show()

        pass

    pass















