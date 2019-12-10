# 电信用户流失预测2019年12月10日

### 提出问题
1. 哪些用户可能流失?  
2. 流失概率更高的用户有什么共同特征？    

### 理解数据

字段名  | 数据类型  |  字段描述
--------- | --------|
User_id  | 用户ID |
Merchant_id  | 商户ID |
Coupon_id  | 优惠券ID：null表示无优惠券消费，此时Discount_rate和Date_received字段无意义 |
Discount_rate  | 优惠率：x \in [0,1]代表折扣率；x:y表示满x减y。单位是元 |
Distance  | user经常活动的地点离该merchant的最近门店距离是x*500米（如果是连锁店，则取最近的一家门店），x\in[0,10]；null表示无此信息，0表示低于500米，10表示大于5公里； |
Date_received  | 领取优惠券日期 |
Date  | 消费日期：如果Date=null & Coupon_id != null，该记录表示领取优惠券但没有使用，即负样本；如果Date!=null & Coupon_id = null，则表示普通消费日期；如果Date!=null & Coupon_id != null，则表示用优惠券消费日期，即正样本； |




		
1	customerID	Integer	用户ID
2	gender	String	性别
3	SeniorCitizen	Integer	老年人
4	Partner	String	配偶
5	Dependents	String	家属
6	tenure	Integer	职位
7	PhoneService	String	电话服务
8	MultipleLines	String	多线
9	InternetService	String	互联网服务
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
