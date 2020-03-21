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

class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}

    def inc(self, numOccur):
        self.count += numOccur

    def disp(self, ind=1):
        print(' ' * ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.disp(ind+1)

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

# 数据格式化
def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet['products_name']:
        trans = trans[0].split(',')
        fset = frozenset(trans)
        retDict.setdefault(fset, 0)
        retDict[fset] += 1
    return  retDict

# 更新头指针表
def updateHeader(nodeToTest, targetNode):
    while(nodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode

# FP树的生长函数
def updateTree(items, myTree, headerTable, count):
    if items[0] in myTree.children:
        myTree.children[items[0]].inc(count)
    else:
        myTree.children[items[0]] = treeNode(items[0], count, myTree)
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] = myTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], myTree.children[items[0]])
    if len(items) > 1:
        updateTree(items[1:], myTree.children[items[0]], headerTable, count)

def createTree(dataSet, minSup):
    headerTable = {}
    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + 1

    lessThanMinsup = list(filter(lambda k:headerTable[k] < minSup, headerTable.keys()))
    for k in lessThanMinsup:
        del(headerTable[k])
    freqItemSet = set(headerTable.keys())

    if len(freqItemSet) == 0:
        return None, None
    for k in headerTable:
        headerTable[k] = [headerTable[k], None]
    myTree = treeNode('φ', 1, None)

    # 第二次遍历数据集,构建fp-tree
    for tranSet, count in dataSet.items():
        localD = {}
        for item in tranSet:
            if item in freqItemSet:
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p:(p[1], p[0]), reverse=True)]
            updateTree(orderedItems, myTree, headerTable, count)
    return  myTree, headerTable




data_new = data_process(data)

reDict = createInitSet(data_new)

myTree, headerTable = createTree(reDict, minSup=3)
print(headerTable)
myTree.disp()







































