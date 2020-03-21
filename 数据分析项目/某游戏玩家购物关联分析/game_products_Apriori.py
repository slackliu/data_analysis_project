import pandas as pd
import time
import sklearn.preprocessing
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('expand_frame_repr', False)  # True 是可以换行显示，False不允许换行
pd.set_option('display.max_rows', 200)  # 显示200行
pd.set_option('display.max_columns', 200)  # 显示200列

data = pd.read_csv(r'D:\下载\Game_DataMining_With_R-master\data\第9章\玩家购物数据.csv')
# print(data.head(20))
# print(data.info())
# print(data.shape)

def data_process(data):
# 创建一个新的矩阵,里面存放每个游戏玩家买的物品,按player_id分,无重复值.
    data['product_name'] = data['product_name'].apply(lambda x:',' + x)
    # print(data.head())
    data_new = data.groupby(by='player_id')['product_name'].sum()
    data_new = data_new.apply(lambda x : [x[1:]])
    # data_new = data.groupby('player_id')['product_name'].apply(list)
    # print(data_new.head())

    data_1 = {'player_id':data_new.index, 'products_name':data_new.values}
    data_2 = pd.DataFrame(data_1)
    # print(data_2.head())
    return data_2

def createC1(dataset):
    """    构建所有候选项的集合     """
    C1 =  []
    for transaction in dataset['products_name']:
        transaction = transaction[0].split(',')
        # print(temp)
        for item in transaction:
            # print(item)
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return list(map(frozenset, C1))
#
def scanD(D, Ck, minSupport):
    """"  生成符合最小支持度的项集  """
    ssCnt = {}
    for tid in D['products_name']:
        tid = tid[0].split(',')
        # print(tid)
        # print(len(tid))
        # print(Ck)
        for can in Ck:
            # print(can)
            # time.sleep(1)
            if can.issubset(tid):
                # print(can.issubset(tid))
                if can not in ssCnt.keys():
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1
    numItems = float(len(D['products_name']))
    retList = []
    supportData = {}
    for key in ssCnt:
        # print(ssCnt[key])
        support = ssCnt[key] / numItems
        # print(support)
        if support >= minSupport:
            retList.insert(0, key)
        supportData[key] = support
    return retList, supportData

def aprioriGen(Lk, k):
    '''  创建符合置信度的项集Ck  '''
    retList = []
    lenLk = len(Lk)
    # print('-----')
    # print(Lk)
    for i in range(lenLk):
        for j in range(i + 1, lenLk):
            L1 = list(Lk[i])[:k-2]
            L2 = list(Lk[j])[:k-2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                retList.append(Lk[i] | Lk[j])

    # print('---')
    print(retList)
    return retList

def apriori(dataSet, minSupport = 0.01):
    C1 = createC1(dataSet)
    L1, supportData = scanD(dataSet, C1, minSupport)
    L = [L1]
    k = 2
    while (len(L[k-2]) >0 ):
        Ck = aprioriGen(L[k-2], k)
        Lk, supK = scanD(dataSet, Ck, minSupport)
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData

dataSet = data_process(data)
# print(dataSet.head())
C1 = createC1(dataSet)
print('所有候选项集C1: \n', C1)

# D = map(set, dataSet)
# print('数据集D: \n', D)

L1, supportData = scanD(dataSet, C1, 0.01)
print('符合最小支持度的频繁1项集L1: \n', L1)

L, suppData = apriori(dataSet)
print('所有符合最小支持度的项集L: \n', L)
print('频繁2项集: \n', aprioriGen(L[0], 2))
L3 = aprioriGen(L[1], 3)
print('频繁3项集: \n', L3)
# L4 = aprioriGen(L[1], 4)
# print(L4)
L, suppData = apriori(dataSet, minSupport=0.1)
print('所有符合最小支持度为0.01的项集L: \n', L)









































