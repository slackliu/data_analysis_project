import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
import os
from pylab import rcParams
import seaborn as sns
import matplotlib.cm as cm
import sklearn
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier


# 导入数据
def data_source():
    source_Path = 'D:\\下载'
    # source_Path = 'D:\\Download'
    telco_file = os.path.join(source_Path, 'WA_Fn-UseC_-Telco-Customer-Churn.csv')
    telco_data = pd.read_csv(telco_file)
    return telco_data


# 数据清洗
    # 1.缺失值处理
    # 2.异常值处理
    # 3.格式一致化
    # 4.删除重复值
def process_data(dataset):
    pd.set_option('expand_frame_repr', False)       # True 是可以换行显示，False不允许换行
    pd.set_option('display.max_rows', 200)          # 显示200行
    pd.set_option('display.max_columns', 200)       # 显示200列

    # 查看数据集大小
    print('dataset.shape', dataset.shape)
    print('----dataset.head---->')
    print(dataset.head())
    # (7043, 21)

    # 获取数据类型的描述统计信息
    print('----dataset.describe----->')
    print(dataset.describe())

    # 统计缺失值数量
    print('------缺失值数量------->')
    print(dataset.isnull().sum())

    # 统计客户流失量
    print('客户流失量:')
    print(dataset['Churn'].value_counts())
    # No     5174
    # Yes    1869

    # 查看数据集类型
    print('-----dataset.info: -----')
    print(dataset.info())
    # TotalCharges数据类型为object,需要将其转化

    # 将TotalCharges数据类型转换为数值型float64
    # dataset['TotalCharges'] = dataset['TotalCharges'].apply(pd.to_numeric, errors='ignore')
    dataset['TotalCharges'] = pd.to_numeric(dataset['TotalCharges'])
    # dataset['TotalCharges'] = np.array(dataset['TotalCharges'])
    # dataset['TotalCharges'] = dataset['TotalCharges'].convert_objects(convert_numeric=True)         # 将其强行转化为数值型

    # 查看是否转换成功
    print('转换后的数据类型:')
    print(dataset.info())
    # 再次查找缺失值
    print('缺失值:----->')
    print(dataset.isnull().sum())

    # 删除缺失值
    dataset.dropna(inplace=True)
    # 查看删除后的数据大小
    print('----dataset.shape----')
    print(dataset.shape)

    # 异常值处理
    print('SeniorCitizen最小值为:', str(dataset['SeniorCitizen'].min()))
    print('SeniorCitizen最大值为:', str(dataset['SeniorCitizen'].max()))
    print('tenure最小值为:', str(dataset['tenure'].min()))
    print('tenure最大值为:', str(dataset['tenure'].max()))
    print('MonthlyCharges最小值为:', str(dataset['MonthlyCharges'].min()))
    print('MonthlyCharges最大值为:', str(dataset['MonthlyCharges'].max()))
    print('TotalCharges最小值为:', str(dataset['TotalCharges'].min()))
    print('TotalCharges最大值为:', str(dataset['TotalCharges'].max()))
    # 并无异常值

    # 数据归一化
    dataset['Churn'].replace(to_replace='Yes', value=1, inplace=True)           # 将1替代yes
    dataset['Churn'].replace(to_replace='No',  value=0, inplace=True)
    print('-----dataset.head-----')
    print(dataset.head())
    # print(dataset['Churn'].head())

    # 删除重复值
    dataset.drop_duplicates()
    print('----dataset.shape----')
    print(dataset.shape)
    return dataset


def plt_pie(dataset):
    #  查看客户流失比例  画饼图
    churn_value = dataset['Churn'].value_counts()           # 统计客户流失数量
    print('统计客户流失数量:')
    print(churn_value)
    labels = dataset['Churn'].value_counts().index          # 设置图片标签
    rcParams['figure.figsize'] = 6, 6
    plt.pie(churn_value, labels=labels, colors=['green', 'yellow'], explode=(0.1, 0), autopct='%1.1f%%', shadow=True)
    plt.title('Proportions of Customer Churn')
    plt.show()


def subplot(dataset):
    # 性别.年龄, 配偶, 亲属对客户流失率的影响
    f, axes = plt.subplots(nrows=2, ncols=2, figsize=(20, 20))
    plt.subplot(2, 2, 1)
    gender = sns.countplot(x='gender', hue='Churn', data=dataset, palette='Pastel2')   # palette 参数表示设置颜色,
    plt.xlabel('gender')
    plt.title('Churn by Gender')

    plt.subplot(2, 2, 2)
    seniorcitizen = sns.countplot(x='SeniorCitizen', hue='Churn', data=dataset, palette='Pastel2')
    plt.xlabel('senior citizen')
    plt.title('Churn by Senior Citizen')

    plt.subplot(2, 2, 3)
    parnter = sns.countplot(x='Partner', hue='Churn', data=dataset, palette='Pastel2')
    plt.xlabel('partner')
    plt.title('Churn by Partner')

    plt.subplot(2, 2, 4)
    dependents = sns.countplot(x='Dependents', hue='Churn', data=dataset,  palette='Pastel2')
    plt.xlabel('dependents')
    plt.title('Churn by Dependents')
    plt.show()


def heatmap(dataset):
    # 提取特征
    charges = dataset.iloc[:, 1:20]
    corrdf = charges.apply(lambda x: pd.factorize(x)[0])
    print(corrdf.head())

    # 构造相关矩阵
    corr = corrdf.corr()
    print('+++++++++++++++')
    print(corr)

    # 使用热地图显示相关系数
    plt.figure(figsize=(20, 16))
    ax = sns.heatmap(corr, xticklabels=corr.columns, yticklabels=corr.columns, linewidths=0.2, cmap='YlGnBu', annot=True)
    plt.title('Correlation between variables')
    plt.show()


def dummies(dataset):
    # 参考: https://blog.csdn.net/gdh756462786/article/details/79161525
    #       https://blog.csdn.net/weixin_39750084/article/details/81432619

    # 使用one-hot编码
    tel_dummies = pd.get_dummies(dataset.iloc[:, 1:21])
    print('=============')
    print(tel_dummies.head())

    # 电信用户是否流失与各变量之间的相关性
    plt.figure(figsize=(15, 8))
    tel_dummies.corr()['Churn'].sort_values(ascending=False).plot(kind='bar')
    plt.title('Correlations between Churn and variables')
    plt.show()


def countplot(dataset):
    # 网络安全服务，在线备份业务、设备保护业务、技术支持服务、网络电视、网络电影、无互联网服务队客户流失率的影响
    covariables = ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(16, 10))
    for i, item in enumerate(covariables):
        plt.subplot(2, 3, (i+1))
        ax = sns.countplot(x=item, hue='Churn', data=dataset, palette='Pastel2', order=['Yes', 'No', 'No internet service'])
        plt.xlabel(str(item))
        plt.title('Churn by' + str(item))
        i = i + 1
    plt.show()


def contract(dataset):
    # 签订合同方式对客户流失率的影响
    sns.barplot(x='Contract', y='Churn', data=dataset, palette='Pastel1', order=['Month-to-month', 'One year', 'Two year'])
    plt.title('Churn by Contract type')
    plt.show()


def paymethod(dataset):
    # 付款方式对客户流失率的影响
    plt.figure(figsize=(10, 5))
    sns.barplot(x='PaymentMethod', y='Churn', data=dataset, palette='Pastel1',
                order=['Back transfer (automatic)', 'Credit card (automatic)', 'Electronic check', 'Mailed check'])
    plt.title('Churn by PaymentMethod type')
    plt.show()


def boxplot(dataset):
    # ## 数据预处理
    datasetvar = dataset.iloc[:, 2:20]
    datasetvar.drop('PhoneService', axis=1, inplace=True)
    telcom_id = dataset['customerID']
    print(datasetvar.head())

    # 对客户的职位,月费用和总费用进行去均值和方差缩放,对数据进行标准化
    # 标准化数据,保证每个纬度的特征数据方差为1, 均值为0, 使得预测接货不会被某些纬度过大的特征值而主导
    scaler = StandardScaler(copy=False)
    a = scaler.fit_transform(datasetvar[['tenure', 'MonthlyCharges', 'TotalCharges']])
    print(a)

    # tranform()的作用是通过找中心和缩放等实现标准化
    datasetvar[['tenure', 'MonthlyCharges', 'TotalCharges']] = scaler.transform(datasetvar[['tenure', 'MonthlyCharges', 'TotalCharges']])

    # 使用箱线图查看数据是否存在异常值
    plt.figure(figsize=(8, 4))
    numbox = sns.boxplot(data=datasetvar[['tenure', 'MonthlyCharges', 'TotalCharges']], palette='Set2')
    plt.title('Check outliers of standardized tenure, MonthlyCharges and TotalCharges')
    plt.show()

    # 查看对象类型字段中存在的值
    telcomobject = datasetvar.select_dtypes(['object'])
    for i in range(0, len(telcomobject.columns)):
        print(telcomobject.columns[i], '--->', dataset[telcomobject.columns[i]].unique())
    print('---------1----------------')
    # 替换值
    datasetvar.replace(to_replace='No internet service', value='No', inplace=True)
    datasetvar.replace(to_replace='No phone service', value='No', inplace=True)
    for i in range(0, len(telcomobject.columns)):
        print(telcomobject.columns[i], '--->', dataset[telcomobject.columns[i]].unique())
    print('---------2------------------')
    # 使用Scikit-learn 标签编码, 将分类数据转换为整数编码
    for i in range(0, len(telcomobject.columns)):
        datasetvar[telcomobject.columns[i]] = LabelEncoder().fit_transform(datasetvar[telcomobject.columns[i]])
    for i in range(0, len(telcomobject.columns)):
        print(telcomobject.columns[i], '--->', dataset[telcomobject.columns[i]].unique())
    print('----------------3------------------')


if __name__ == '__main__':
    start = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(start)
    #  查询本机的cpu数量
    cpu_jobs = os.cpu_count() - 1
    date_null = pd.to_datetime('1970-01-01', format='%Y-%m-%d')
    # 设置显示行列数参数，参考链接： https://www.cnblogs.com/yesuuu/p/6100714.html
    pd.set_option('expand_frame_repr', False)       # True 是可以换行显示，False不允许换行
    pd.set_option('display.max_rows', 200)          # 显示200行
    pd.set_option('display.max_columns', 200)       # 显示200列

    dataset = data_source()
    processed_data = process_data(dataset)
    plt_pie(processed_data)
    subplot(processed_data)
    heatmap(processed_data)
    # dummies(processed_data)
    # countplot(processed_data)
    # contract(processed_data)
    # paymethod(processed_data)
    # boxplot(processed_data)


