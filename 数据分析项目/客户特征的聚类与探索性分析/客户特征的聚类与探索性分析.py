import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabaz_score
import pickle

pd.set_option('expand_frame_repr', False)  # True 是可以换行显示，False不允许换行
pd.set_option('display.max_rows', 200)  # 显示200行
pd.set_option('display.max_columns', 200)  # 显示200列

# 读取数据
data = pd.read_csv('cluster.txt')
print(data.head())
# 平均订单数和平均消费金额属于数值型特征
numeric_features = data.iloc[:, 1:3]

# 数据标准化
sclaer = MinMaxScaler()
sclaed_numeric_features = sclaer.fit_transform(numeric_features)
print(sclaed_numeric_features)

# 训练聚类模型
n_clusters = 3
model_kmeans = KMeans(n_clusters=n_clusters, random_state=0)
model_kmeans.fit(sclaed_numeric_features)
'''
random_state=0的目的是保证每次测试时的初始值一致,这样避免由于初始值不同导致的聚类结果差异,
'''
# pickle.dump(model_kmeans, open('model_object.pkl', 'wb'))

n_samples, n_features = data.iloc[:, 1:].shape
print('samples: %d \t features: %d' % (n_samples, n_features))

# 结果评估
silhouette_s = silhouette_score(sclaed_numeric_features, model_kmeans.labels_, metric='euclidean')      # 平均轮廓系数
calinski_harabaz_s = calinski_harabaz_score(sclaed_numeric_features, model_kmeans.labels_)              # Calinski和Harabaz得分
unsupervised_data = {'silh':[silhouette_s], 'c&h':[calinski_harabaz_s]}
unsupervised_score = pd.DataFrame.from_dict(unsupervised_data)
print('\n', 'unsupervised score:', '\n', '-'*60)
print(unsupervised_score)

# 合并数据和特征
kmeans_labels = pd.DataFrame(model_kmeans.labels_, columns=['labels'])
# 组合原始数据和标签
kmeans_data = pd.concat((data, kmeans_labels), axis=1)
print(kmeans_data.head())

# 计算不同聚类类别的样本量和占比
label_count = kmeans_data.groupby(['labels'])['SEX'].count()                # 计算频数
label_count_rate = label_count / kmeans_data.shape[0]                       # 计算占比
kmeans_record_count = pd.concat((label_count, label_count_rate), axis=1)
kmeans_record_count.columns = ['record_count', 'record_rate']
print(kmeans_record_count.head())

# 计算不同聚类类别数值型特征
kmeans_numeric_features = kmeans_data.groupby(['labels'])['AVG_ORDERS', 'AVG_MONEY'].mean()
print(kmeans_numeric_features.head())

# 计算不同聚类类别分类型特征
active_list = []
sex_gb_list = []
unique_labels = np.unique(model_kmeans.labels_)
for each_label in unique_labels:
    each_data = kmeans_data[kmeans_data['labels'] == each_label]
    active_list.append(each_data.groupby(['IS_ACTIVE'])['USER_ID'].count()/each_data.shape[0])
    sex_gb_list.append(each_data.groupby(['SEX'])['USER_ID'].count()/each_data.shape[0])

kmeans_active_pd = pd.DataFrame(active_list)
kmeans_sex_gb_bd = pd.DataFrame(sex_gb_list)
kmeans_string_features = pd.concat((kmeans_active_pd, kmeans_sex_gb_bd), axis=1)
kmeans_string_features.index = unique_labels

features_all = pd.concat((kmeans_record_count, kmeans_numeric_features, kmeans_string_features), axis=1)
print(features_all.head())


fig = plt.figure(figsize=(10, 7))
titles = ['RECORD_RATE', 'AVG_ORDERS', 'AVG_MONEY', 'IS_ACTIVE', 'SEX']
line_index, col_index = 3, 5
ax_ids = np.arange(1, 16).reshape(line_index, col_index)
plt.rcParams['font.sans-serif'] = ['SimHei']


pie_fracs = features_all['record_rate'].tolist()
for ind in range(len(pie_fracs)):
    ax = fig.add_subplot(line_index, col_index, ax_ids[:, 0][ind])
    init_labels = ['', '', '']
    init_labels[ind] = 'cluster_{0}'.format(ind)
    init_colors = ['lightgray', 'lightgray', 'lightgray']
    init_colors[ind] = 'g'
    ax.pie(x=pie_fracs, autopct='%3.0f %%', labels=init_labels, colors=init_colors)
    ax.set_aspect('equal')
    if ind == 0:
        ax.set_title(titles[0])


avg_orders_label = 'AVG_ORDERS'
avg_orders_fraces = features_all[avg_orders_label]
for ind, frace in enumerate(avg_orders_fraces):
    ax = fig.add_subplot(line_index, col_index, ax_ids[:, 1][ind])
    ax.bar(x=unique_labels, height=[0, avg_orders_fraces[ind], 0])
    ax.set_ylim((0, max(avg_orders_fraces) * 1.2))
    ax.set_xticks([])
    ax.set_yticks([])
    if ind == 0:
        ax.set_title(titles[1])
    avg_orders_values = '{:.2f}'.format(frace)
    ax.text(unique_labels[1], frace + 0.4, s=avg_orders_values, ha='center', va='top')
    ax.text(unique_labels[1], -0.4, s=avg_orders_label, ha='center', va='bottom')


avg_money_label = 'AVG_MONEY'
avg_money_frace = features_all[avg_money_label]
for ind, frace in enumerate(avg_money_frace):
    ax = fig.add_subplot(line_index, col_index, ax_ids[:, 2][ind])
    ax.bar(x=unique_labels, height=[0, avg_money_frace[ind], 0])
    ax.set_ylim((0, max(avg_money_frace) * 1.2))
    ax.set_xticks([])
    ax.set_yticks([])
    if ind == 0:
        ax.set_title(titles[2])
    ax.text(unique_labels[1], frace + 4, s='{:.0f}'.format(frace), ha='center', va='top')
    ax.text(unique_labels[1], -4, s=avg_money_label, ha='center', va='bottom')


activity_labels = ['不活跃', '活跃']
x_ticket = [i for i in range(len(activity_labels))]
activity_data = features_all[activity_labels]
ylim_max = np.max(np.max(activity_data))
for ind, each_data in enumerate(activity_data.values):
    ax = fig.add_subplot(line_index, col_index, ax_ids[:, 3][ind])
    ax.bar(x=x_ticket, height=each_data)
    ax.set_ylim((0, ylim_max * 1.2))
    ax.set_xticks([])
    ax.set_yticks([])
    if ind == 0:
        ax.set_title(titles[3])
    activity_values = ['{:.1f}'.format(i) for i in each_data]
    for i in range(len(x_ticket)):
        ax.text(x_ticket[i], each_data[i] + 0.05, s=activity_values[i], ha='center', va='top')
        ax.text(x_ticket[i], -0.05, s=activity_labels[i], ha='center', va='bottom')


sex_data = features_all.iloc[:, -3]
x_ticket = [i for i in range(len(sex_data))]
sex_labels = ['SEX_{}'.format(i) for i in range(3)]
ylim_max = np.max(np.max(sex_data))
for ind, each_data in enumerate(sex_data.values):
    ax = fig.add_subplot(line_index, col_index, ax_ids[:, 4][ind])
    ax.bar(x=x_ticket, height=each_data)
    ax.set_ylim((0, ylim_max * 1.2))
    ax.set_xticks([])
    ax.set_yticks([])
    if ind == 0:
        ax.set_title(titles[4])
    print(each_data)
    sex_values = ['{:.2f}'.format(i) for i in each_data]
    for i in range(len(x_ticket)):
        ax.text(x_ticket[i], each_data[i] + 0.1, s=sex_values[i], ha='center', va='top')
        ax.text(x_ticket[i], -0.1, s=sex_labels[i], ha='center', va='bottom')


plt.show()





