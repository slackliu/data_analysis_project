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
解决问题:判断,当数据中有空格时,返回Nan,否则返回原值.
#### 2. 异常值处理
无异常值
#### 3. 格式一致化处理

#### 4. 删除重复值
无重复值

### 四、数据可视化
#### 1. 查看客户流失比例
![image](https://github.com/slackliu/data_analysis/blob/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E9%A1%B9%E7%9B%AE/kaggle/%E7%94%B5%E4%BF%A1%E7%94%A8%E6%88%B7%E6%B5%81%E5%A4%B1%E9%A2%84%E6%B5%8B/iamges/%E5%AE%A2%E6%88%B7%E6%B5%81%E5%A4%B1%E6%AF%94%E4%BE%8B.png)
- 由上图可知流失客户占了整体客户群的四分之一.  

#### 2. 性别、老年人、配偶、亲属对流客户流失率的影响
![image](https://github.com/slackliu/data_analysis/blob/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E9%A1%B9%E7%9B%AE/kaggle/%E7%94%B5%E4%BF%A1%E7%94%A8%E6%88%B7%E6%B5%81%E5%A4%B1%E9%A2%84%E6%B5%8B/iamges/%E6%80%A7%E5%88%AB_%E5%B9%B4%E9%BE%84_%E4%BA%B2%E5%B1%9E%E5%AF%B9%E6%B5%81%E5%A4%B1%E7%8E%87%E7%9A%84%E5%BD%B1%E5%93%8D.png)
- 由上图可知,性别对客户流失率并无影响,老年人中流失率普遍高于其他年龄.未婚人群中的流失率也明显高于已婚人士, 独立人群中的客户流失率明显低于未独立人群

#### 3. 查看各个因素之间的相关性
![image](https://github.com/slackliu/data_analysis/blob/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E9%A1%B9%E7%9B%AE/kaggle/%E7%94%B5%E4%BF%A1%E7%94%A8%E6%88%B7%E6%B5%81%E5%A4%B1%E9%A2%84%E6%B5%8B/iamges/%E7%83%AD%E5%8A%9B%E5%9B%BE.png)
- 由上图可知, 多线,互联网服务, 在线安全,在线备份,设备保护,技术支持,网络电视和网络电影之间存在较强的相关性,多线业务和电话服务之间也有很强的相关性，

#### 4.各个因素对客户流失率的影响
![image](https://github.com/slackliu/data_analysis/blob/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E9%A1%B9%E7%9B%AE/kaggle/%E7%94%B5%E4%BF%A1%E7%94%A8%E6%88%B7%E6%B5%81%E5%A4%B1%E9%A2%84%E6%B5%8B/iamges/%E7%94%B5%E4%BF%A1%E7%94%A8%E6%88%B7%E6%98%AF%E5%90%A6%E6%B5%81%E5%A4%B1%E4%B8%8E%E5%90%84%E5%8F%98%E9%87%8F%E4%B9%8B%E9%97%B4%E7%9A%84%E7%9B%B8%E5%85%B3%E6%80%A7.png)
- 由上图可知: 电话服务和性别对客户流失率影响不大

#### 5. 网络安全服务、在线备份业务、设备保护业务、技术支持服务、网络电视、网络电影和无互联网服务对客户流失率的影响
![image](https://github.com/slackliu/data_analysis/blob/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E9%A1%B9%E7%9B%AE/kaggle/%E7%94%B5%E4%BF%A1%E7%94%A8%E6%88%B7%E6%B5%81%E5%A4%B1%E9%A2%84%E6%B5%8B/iamges/%E7%BD%91%E7%BB%9C%E5%AE%89%E5%85%A8%E6%9C%8D%E5%8A%A1%E3%80%81%E5%9C%A8%E7%BA%BF%E5%A4%87%E4%BB%BD%E4%B8%9A%E5%8A%A1%E3%80%81%E8%AE%BE%E5%A4%87%E4%BF%9D%E6%8A%A4%E4%B8%9A%E5%8A%A1%E3%80%81%E6%8A%80%E6%9C%AF%E6%94%AF%E6%8C%81%E6%9C%8D%E5%8A%A1%E3%80%81%E7%BD%91%E7%BB%9C%E7%94%B5%E8%A7%86%E3%80%81%E7%BD%91%E7%BB%9C%E7%94%B5%E5%BD%B1%E5%92%8C%E6%97%A0%E4%BA%92%E8%81%94%E7%BD%91%E6%9C%8D%E5%8A%A1%E5%AF%B9%E5%AE%A2%E6%88%B7%E6%B5%81%E5%A4%B1%E7%8E%87%E7%9A%84%E5%BD%B1%E5%93%8D.png)
- 由上图可知: 在网络安全服务、在线备份业务、设备保护业务、技术支持服务、网络电视和网络电影六个变量中，没有互联网服务的客户流失率都相对较低。

#### 6. 签订合同方式对客户流失率的影响
![image](https://github.com/slackliu/data_analysis/blob/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E9%A1%B9%E7%9B%AE/kaggle/%E7%94%B5%E4%BF%A1%E7%94%A8%E6%88%B7%E6%B5%81%E5%A4%B1%E9%A2%84%E6%B5%8B/iamges/%E5%90%88%E5%90%8C%E7%AD%BE%E8%AE%A2%E6%96%B9%E5%BC%8F%E5%AF%B9%E5%AE%A2%E6%88%B7%E6%B5%81%E5%A4%B1%E7%8E%87%E7%9A%84%E5%BD%B1%E5%93%8D.png)
- 由图上可知,签订合同方式时间越长客户流失率越低

#### 7. 付款方式对客户流失率的影响
![image](https://github.com/slackliu/data_analysis/blob/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E9%A1%B9%E7%9B%AE/kaggle/%E7%94%B5%E4%BF%A1%E7%94%A8%E6%88%B7%E6%B5%81%E5%A4%B1%E9%A2%84%E6%B5%8B/iamges/%E4%BB%98%E6%AC%BE%E6%96%B9%E5%BC%8F%E5%AF%B9%E5%AE%A2%E6%88%B7%E6%B5%81%E5%A4%B1%E7%8E%87%E7%9A%84%E5%BD%B1%E5%93%8D.png)
- 由图上可以看出，在四种支付方式中，使用Electronic check的用户流流失率最高，其他三种支付方式基本持平，因此可以推断电子账单在设计上影响用户体验。

#### 8. 查看是否存在异常值
![image](https://github.com/slackliu/data_analysis/blob/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E9%A1%B9%E7%9B%AE/kaggle/%E7%94%B5%E4%BF%A1%E7%94%A8%E6%88%B7%E6%B5%81%E5%A4%B1%E9%A2%84%E6%B5%8B/iamges/%E5%90%A6%E5%AD%98%E5%9C%A8%E5%BC%82%E5%B8%B8%E5%80%BC.png)
- 不存在明显异常值

### 五、总结和建议总结
#### 1. 总结：  
- 用户角度：老年用户、未婚用户、无亲属用户、经济不独立用户更容易流失。  
- 电话服务角度：对流失率影响相对较小。  
- 网络服务角度：办理光纤网络、且不开通的网络的各项服务的用户流失率较高。  
- 合同角度：签订的合同期较短，是电子账单支付的客户容易流失。
#### 2. 提出建议：  
- 用户方面：提早获取用户信息，在注册时就要求客户把个人信息完善完整，以便提供更适合的服务。建议加强对以上类型用户加强监控，针对该老年、有亲属的用户推出新的亲情套餐，加强用户联系，获取更多用户数量；而对于未婚用户，可能是年轻人工作地点不固定，推出包含流量全国通用包的套餐，以便用户在不用的地区上网，无需因为省内流量的限制而放弃使用现有套餐。  
- 网络服务：使用网络用户流失率高，建议加快网络建设，提高光纤网络速度，提高用户体验。同时在市场活动中，将用户的信息安全、设备安全作为主要推广点，更大限度激活用户的‘啊哈时刻’；而服务、娱乐类业务则需要继续改进，可选择各项网络服务与互联网相关行业合作，推出联合产品互利共赢。  
- 合同方面：针对签订的合同期限较短，建议推出年付费用户xx折、一次性付满两年的用户费用xx折的活动，将月付费用户转化为年付费甚至两年付费用户，提高用户在网时长，以达到更高的用户留存。 针对电子支票的流失严重问题，建议与选择与银行合作，在用户付款时推出使用某银行信用卡支付则赠送礼品或立减活动，使得用户更愿意选择流失率较小的信用卡支付方式进行支付。  
 


### 六、预测
算法还没看
