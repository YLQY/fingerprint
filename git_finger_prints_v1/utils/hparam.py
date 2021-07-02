
import yaml


# 加载Yaml文件
def load_hparam(path):

    docs = yaml.load_all(open(path,'r',encoding='utf-8'))

    hparam_dict = dict()
    for doc in docs:
        for k,v in doc.items():
            hparam_dict[k] = v
            pass
        pass

    return hparam_dict

# 创建一个自己的字典类
class Dotdict(dict):

    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self,dct = None):
        # 判断非空
        dic = dict() if not dct else dct

        for key,value in dic.items():
            if hasattr(value,'keys'):
                value = Dotdict(value)
                pass
            self[key] = value
            pass
        pass

    pass



class Hparam(Dotdict):

    def __init__(self,filepath='./config/config.yaml'):
        super(Dotdict, self).__init__()

        # 通过路径加载Yaml文件做成字典
        hp_dict = load_hparam(filepath)

        # 转化成自己的字典
        hp_dotdict = Dotdict(hp_dict)

        for k,v in hp_dotdict.items():
            setattr(self,k,v)
            pass

        pass

    __getattr__ =  Dotdict.__getitem__
    __setattr__ =  Dotdict.__setitem__
    __delattr__ =  Dotdict.__delitem__

    pass


hp = Hparam()




