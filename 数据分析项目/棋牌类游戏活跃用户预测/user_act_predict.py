import pandas as pd
import time
from sklearn import tree
from sklearn.cluster import KMeans
from sklearn.externals import joblib
from matplotlib import pylab
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_curve, accuracy_score, classification_report, silhouette_score, \
    calinski_harabaz_score
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, Binarizer
import matplotlib.pyplot as plt
import seaborn as sns
import pydot
import warnings

from sklearn.tree import export_graphviz

warnings.filterwarnings('ignore')

pd.set_option('expand_frame_repr', False)  # True 是可以换行显示，False不允许换行
pd.set_option('display.max_rows', 200)  # 显示200行
pd.set_option('display.max_columns', 200)  # 显示200列
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)


data = pd.read_csv(r'D:\下载\Game_DataMining_With_R-master\data\第8章\用户流失预测数据.csv',encoding='gb18030')

data['周活跃度'] = data['登录总次数'] / 7
data['玩牌胜率'] = data['赢牌局数'] / data['玩牌局数']
print(data.head())
# print(data.shape)
# print(data.isnull().sum())
# print(data.describe())
# print(data['用户id'].drop_duplicates())
# print(data.shape)
# 数据不存在缺失值/异常值/也无量纲问题./也没有重复值
data['是否流失'].replace(to_replace='是', value=1, inplace=True)
data['是否流失'].replace(to_replace='否', value=0, inplace=True)

data2_new = pd.get_dummies(data.iloc[:, 0:17])
print(data2_new.head())

# data2_new['是否流失'].astype(int)
# print(data2_new.info())
data3 = data2_new.iloc[:, :]

# print(data3.corr())
data4 = data3.corr()
plt.figure(figsize=(12, 10))

# plt.rcParams['font.sans-serif']=['SimHei']
# ax = sns.heatmap(data4, xticklabels=data4.columns, yticklabels=data4.columns, linewidths=0.2, cmap='BrBG_r', annot=True)
# plt.title('Correlation between featrues')
# plt.show()
#
# plt.figure(figsize=(12, 10))
# data4.corr()['是否流失'].sort_values(ascending=False).plot(kind='bar')
# plt.title('corrlations between ')
# plt.show()

cols = list(data2_new)

cols.insert(0, cols.pop(cols.index('是否流失')))
data2_new = data2_new.loc[:, cols]
# print(cols)
print(data2_new.head())
Feature = data2_new.ix[:, 1:]
Label = data2_new.ix[:, 0]
x_train, x_test, y_train, y_test = train_test_split(Feature, Label, random_state=42)
clf = tree.DecisionTreeClassifier(max_depth=4, random_state=0, splitter='best'
                                  ,max_features=8
                                  , min_samples_leaf=10, min_samples_split=5)
clf = clf.fit(x_train, y_train)

print('Train score:{:.3f}'.format(clf.score(x_train,y_train)))
print('Test score:{:.6f}'.format(clf.score(x_test,y_test)))

import graphviz
dot_data = export_graphviz(clf, out_file='tree.dot', class_names=['流失', '未流失'], feature_names=Feature, impurity=False, filled=True)
graph = graphviz.Source(dot_data)
graph.show()