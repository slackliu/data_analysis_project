import pandas as pd
from datetime import datetime
import numpy as np
import os

"""
特征值处理
"""


# 读取数据
def get_source_data():
    # 源数据路径
    data_source_Path = 'E:\BaiduNetdiskDownload\O2O_data'
    off_train_file = os.path.join(data_source_Path, 'ccf_offline_stage1_train.csv')
    on_train_file = os.path.join(data_source_Path, 'ccf_online_stage1_train.csv')
    off_test_file = os.path.join(data_source_Path, 'ccf_offline_stage1_test_revised.csv')

    # 读入源数据
    off_train = pd.read_csv(off_train_file)
    on_train = pd.read_csv(on_train_file)
    off_test = pd.read_csv(off_test_file)

    # print(off_train.info())
    # print(off_train.head(3))
    return off_train, on_train, off_test


# 缺失值处理
def null_process_offline(dataset,predict=False):
    print(dataset.isnull().sum())
    dataset.distance.fillna(11, inpalce=True)
    dataset.Distance = dataset.Distance.astype(int)
    dataset.Coupon_id.fillna(0, inplace=True)
    dataset.Coupon_id = dataset.Coupon_id.astype(int)
    dataset.Date_received.fillna(date_null, inplace=True)




def null_process_online(dataset):
    pass


# 表设计：https://blog.csdn.net/runnerchen1/article/details/88356226
# 主程序
if __name__ == '__main__':

    # datetime : https://blog.csdn.net/qq_32607273/article/details/81809986
    start = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    print(start)

    #  查询本机的cpu数量
    cpu_jobs = os.cpu_count() - 1
    date_null = pd.to_datetime('1970-01-01', format='%Y-%m-%d')
    # 设置显示行列数参数，参考链接： https://www.cnblogs.com/yesuuu/p/6100714.html
    pd.set_option('expand_frame_repr', False)       # True 是可以换行显示，False不允许换行
    pd.set_option('display.max_rows', 200)          # 显示200行
    pd.set_option('display.max_columns', 200)       # 显示200列

    # 预处理后数据的存放路径
    Processed_Path = 'E:\BaiduNetdiskDownload\O2O_data'

    # 读入源数据
    off_train, on_train, off_test = get_source_data()

    # 源数据处理
    off_train = null_process_offline(off_train, predict=False)
    on_train = null_process_online(on_train)
    off_test = null_process_offline(off_test, predict=True)





