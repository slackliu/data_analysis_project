# 电信用户流失预测2019年12月10日

### 提出问题
1. 哪些用户可能流失?  
2. 流失概率更高的用户有什么共同特征？    

### 理解数据

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
--------- | -------- | --------|
--------- | -------- | --------|





		
1			
2			
3			
4			
5			
6			
7			
8			
9			
10	OnlineSecurity	String	在线安全
11	OnlineBackup	String	在线备份
12	DeviceProtection	String	设备保护
13	TechSupport	String	技术支持
14	StreamingTV	String	
15	Contract	String	合同
16	PaperlessBilling	String	账单
17	PaymentMethod	String	付款方式
18	MonthlyCharges	Integer	月费用
19	TotalCharges	Integer	总费用
20	Churn	String	流失
