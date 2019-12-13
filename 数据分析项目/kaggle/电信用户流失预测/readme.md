# 电信用户流失预测2019年12月10日

### 一、提出问题
1. 哪些用户可能流失?  
2. 流失概率更高的用户有什么共同特征？    

### 二、理解数据

字段名  | 数据类型  | 字段描述|
--------- | --------| --------|
customerID | Integer| 用户ID|
gender | String| 性别|
SeniorCitizen | Integer| 老年人|
Partner | String| 配偶|
Dependents | String| 家属|
tenure | Integer| 职位|
PhoneService | String| 电话服务|
MultipleLines | String| 多线|
InternetService | String| 互联网服务|
OnlineSecurity | String | 在线安全 |
OnlineBackup | String | 在线备份 |
DeviceProtection | String | 设备保护 |
TechSupport | String | 技术支持 |
StreamingTV | String | -------- |
StreamingMovies | String | -------- |
Contract | String | 合同 |
PaperlessBilling | String | 账单 |
PaymentMethod | String | 付款方式 |
MonthlyCharges | Integer | 月费用 |
TotalCharges | Integer | 总费用 |
Churn | String | 流失 |
		
### 三、数据清洗
#### 0. 导入数据
导入数据函数为:data_source()  
注意数据文件路径.  
#### 1. 缺失值处理
转换数据类型过程中遇到object转为float不成功的问题，因为数据中含有空格，to_numeric不能讲空格转换，convert_numeric却不再支持,
#### 2. 异常值处理
无异常值
#### 3. 格式一致化处理

#### 4. 删除重复值
无重复值



1. 性别对流失率的影响  

![image](https://github.com/slackliu/data_analysis/blob/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E9%A1%B9%E7%9B%AE/kaggle/%E7%94%B5%E4%BF%A1%E7%94%A8%E6%88%B7%E6%B5%81%E5%A4%B1%E9%A2%84%E6%B5%8B/iamges/%E6%80%A7%E5%88%AB%E5%AF%B9%E6%B5%81%E5%A4%B1%E7%8E%87%E7%9A%84%E5%BD%B1%E5%93%8D.png)  

- 可见性别对流失率没什么影响

2. 年龄对流失率的影响
是否为老年人对流失量的影响:  

![image](https://github.com/slackliu/data_analysis/blob/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E9%A1%B9%E7%9B%AE/kaggle/%E7%94%B5%E4%BF%A1%E7%94%A8%E6%88%B7%E6%B5%81%E5%A4%B1%E9%A2%84%E6%B5%8B/iamges/%E5%B9%B4%E9%BE%84%E5%AF%B9%E6%B5%81%E5%A4%B1%E7%8E%87%E7%9A%84%E5%BD%B1%E5%93%8D.png)  

