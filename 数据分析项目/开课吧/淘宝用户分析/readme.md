## 2020年2月11日开始项目
### 1.数据来源及说明
数据集包含2014年11月18日至2014年12月18日，8477名随机用户共1048575条行为数据，数据集的每一行表示一条用户行为，共6列。  
列字段包含如下：  
user_id：用户身份  
item_id：商品ID  
behavior_type：用户行为类型（包含点击、收藏、加购物车、购买四种行为，分别用数字1、2、3、4表示）  
user_geohash：地理位置（有空值）  
item_category：品类ID（商品所属的品类）  
time：用户行为发生的时间  

### 2.提出问题
1.整体用户的购物情况  
pv（总访问量）、日均访问量、uv（用户总数）、有购买行为的用户数量、用户的购物情况、复购率分别是多少？  
2.用户行为转化漏斗  
点击————加购物车————收藏—————购买 各个环节转化率如何？购物车遗弃率是多少？如何提高？
3.购买率高和购买率为0的人群有什么特征？
4.基于时间维度了解用户的行为习惯
5.基于RFM模型的用户分析

### 3.数据清洗
#### 1.导入数据
使用Navicat将数据集导入MySQL  
#### 2.缺失值处理
item_category列表示地理位置信息，由于数据存在大量缺失值，且位置信息被加密处理，因此后续不对item_category列进行分析。
![image](https://github.com/slackliu/data_analysis/blob/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E9%A1%B9%E7%9B%AE/%E5%BC%80%E8%AF%BE%E5%90%A7/%E6%B7%98%E5%AE%9D%E7%94%A8%E6%88%B7%E5%88%86%E6%9E%90/images/1.jpg)
#### 3.数据一致化处理
由于time字段的时间包含（年月日小时），为了方便分析，将该字段拆分为两个字段，分别为日期（date）和时间（time）
![image](https://github.com/slackliu/data_analysis/blob/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E9%A1%B9%E7%9B%AE/%E5%BC%80%E8%AF%BE%E5%90%A7/%E6%B7%98%E5%AE%9D%E7%94%A8%E6%88%B7%E5%88%86%E6%9E%90/images/2.jpg)

由于behavior_type列的四种行为类型分别用1,2,3,4表示点击、收藏、加购物车、购买四种行为，为了方便查看数据，将1,2,3,4替换为‘pv’、‘fav’、‘cart’、‘buy’。
![image](https://github.com/slackliu/data_analysis/blob/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E9%A1%B9%E7%9B%AE/%E5%BC%80%E8%AF%BE%E5%90%A7/%E6%B7%98%E5%AE%9D%E7%94%A8%E6%88%B7%E5%88%86%E6%9E%90/images/3.jpg)

通过查询表结构，可以看到date列不是日期类型。
![image](https://github.com/slackliu/data_analysis/blob/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E9%A1%B9%E7%9B%AE/%E5%BC%80%E8%AF%BE%E5%90%A7/%E6%B7%98%E5%AE%9D%E7%94%A8%E6%88%B7%E5%88%86%E6%9E%90/images/4.jpg)
所以需要将date列改为date类型。
![image](https://github.com/slackliu/data_analysis/blob/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E9%A1%B9%E7%9B%AE/%E5%BC%80%E8%AF%BE%E5%90%A7/%E6%B7%98%E5%AE%9D%E7%94%A8%E6%88%B7%E5%88%86%E6%9E%90/images/5.jpg)

### 4.构建模型和分析问题
#### 1.总体用户购物情况
1. pv（总访问量）
![image](https://github.com/slackliu/data_analysis/blob/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E9%A1%B9%E7%9B%AE/%E5%BC%80%E8%AF%BE%E5%90%A7/%E6%B7%98%E5%AE%9D%E7%94%A8%E6%88%B7%E5%88%86%E6%9E%90/images/6.jpg)

2. 日均访问量
![image](https://github.com/slackliu/data_analysis/blob/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E9%A1%B9%E7%9B%AE/%E5%BC%80%E8%AF%BE%E5%90%A7/%E6%B7%98%E5%AE%9D%E7%94%A8%E6%88%B7%E5%88%86%E6%9E%90/images/7.jpg)
3.uv（用户总数）
![image](https://github.com/slackliu/data_analysis/blob/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E9%A1%B9%E7%9B%AE/%E5%BC%80%E8%AF%BE%E5%90%A7/%E6%B7%98%E5%AE%9D%E7%94%A8%E6%88%B7%E5%88%86%E6%9E%90/images/8.jpg)
4. 有购买行为的用户数量  
![image](https://github.com/slackliu/data_analysis/blob/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E9%A1%B9%E7%9B%AE/%E5%BC%80%E8%AF%BE%E5%90%A7/%E6%B7%98%E5%AE%9D%E7%94%A8%E6%88%B7%E5%88%86%E6%9E%90/images/9.jpg)

5. 用户的购物情况
![image](https://github.com/slackliu/data_analysis/blob/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E9%A1%B9%E7%9B%AE/%E5%BC%80%E8%AF%BE%E5%90%A7/%E6%B7%98%E5%AE%9D%E7%94%A8%E6%88%B7%E5%88%86%E6%9E%90/images/10.jpg)

6. 复购率：产生两次货两次以上购买的用户占购买用户的比例
![image](https://github.com/slackliu/data_analysis/blob/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E9%A1%B9%E7%9B%AE/%E5%BC%80%E8%AF%BE%E5%90%A7/%E6%B7%98%E5%AE%9D%E7%94%A8%E6%88%B7%E5%88%86%E6%9E%90/images/11.jpg)

#### 2.用户行为转化漏斗
在购物环节中收藏和加入购物车两个环节没有先后之分，所以将这两个环节放到一起作为购物环节的一步，最终得到用户购物行为各个环节转化率：  
![image](https://github.com/slackliu/data_analysis/blob/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E9%A1%B9%E7%9B%AE/%E5%BC%80%E8%AF%BE%E5%90%A7/%E6%B7%98%E5%AE%9D%E7%94%A8%E6%88%B7%E5%88%86%E6%9E%90/images/12.jpg)
![image](https://github.com/slackliu/data_analysis/blob/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E9%A1%B9%E7%9B%AE/%E5%BC%80%E8%AF%BE%E5%90%A7/%E6%B7%98%E5%AE%9D%E7%94%A8%E6%88%B7%E5%88%86%E6%9E%90/images/13.jpg)
![image](https://github.com/slackliu/data_analysis/blob/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E9%A1%B9%E7%9B%AE/%E5%BC%80%E8%AF%BE%E5%90%A7/%E6%B7%98%E5%AE%9D%E7%94%A8%E6%88%B7%E5%88%86%E6%9E%90/images/14.jpg)

不同的行业转化率会有差异，据2012年的一项研究表明，在整个互联网范围内，平均转化率为2.13%（数据来源于《精益数据分析》），图中所示购买行为的转化率为1.04%，与行业平均值存在较大差异，淘宝移动端用户行为的转化率还有很大的增长空间。

#### 3.购买率高和购买率为0的人群有什么特征  
购买率高的用户特征：
![image](https://github.com/slackliu/data_analysis/blob/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E9%A1%B9%E7%9B%AE/%E5%BC%80%E8%AF%BE%E5%90%A7/%E6%B7%98%E5%AE%9D%E7%94%A8%E6%88%B7%E5%88%86%E6%9E%90/images/15.jpg)
![image](https://github.com/slackliu/data_analysis/blob/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E9%A1%B9%E7%9B%AE/%E5%BC%80%E8%AF%BE%E5%90%A7/%E6%B7%98%E5%AE%9D%E7%94%A8%E6%88%B7%E5%88%86%E6%9E%90/images/16.jpg)
由以上结果可以看出，购买率高的用户点击率反而不是最多的，这些用户收藏数和加购物车的次数也是很少，一般点击不超过5次就直接购买，由此可以推断出这些用户为理智型消费者，有明确的购物目的，属于缺啥买啥型，很少会被店家广告或者促销吸引。

购买率为0的用户特征：
![image](https://github.com/slackliu/data_analysis/blob/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E9%A1%B9%E7%9B%AE/%E5%BC%80%E8%AF%BE%E5%90%A7/%E6%B7%98%E5%AE%9D%E7%94%A8%E6%88%B7%E5%88%86%E6%9E%90/images/17.jpg)
由以上结果可以看出，购买率为低的用户分为两类，  
第一类是点击次数少的，一方面的原因是这类用户可能是不太会购物或者不太喜欢上网的用户，可以加以引导，另一方面是从商品的角度考虑，是否商品定价过高或者设计不合理。  
第二类用户是点击率高、收藏或者加购物车也多的用户，此类用户可能正为商家的促销活动做准备，下单欲望较少且自制力强，思虑多或者不会支付，购物难度大。

#### 4.基于时间维度了解用户的行为习惯
1.一天中用户的活跃时段分步
![image](https://github.com/slackliu/data_analysis/blob/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E9%A1%B9%E7%9B%AE/%E5%BC%80%E8%AF%BE%E5%90%A7/%E6%B7%98%E5%AE%9D%E7%94%A8%E6%88%B7%E5%88%86%E6%9E%90/images/18.jpg)
![image](https://github.com/slackliu/data_analysis/blob/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E9%A1%B9%E7%9B%AE/%E5%BC%80%E8%AF%BE%E5%90%A7/%E6%B7%98%E5%AE%9D%E7%94%A8%E6%88%B7%E5%88%86%E6%9E%90/images/19.jpg)
可以看出，每天0点到5点用户活跃度快速降低，降到一天中的活跃量最低值，6点到10点用户活跃度快速上升，10点到18点影虎活跃度较平稳，17点到23点用户活跃度快速上升，达到一天中的最高值。

2.一周用户活跃时段分步
由于第一周和第五周数据不全，因此这两周的数据不再此次分析中。
![image](https://github.com/slackliu/data_analysis/blob/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E9%A1%B9%E7%9B%AE/%E5%BC%80%E8%AF%BE%E5%90%A7/%E6%B7%98%E5%AE%9D%E7%94%A8%E6%88%B7%E5%88%86%E6%9E%90/images/20.jpg)
![image](https://github.com/slackliu/data_analysis/blob/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E9%A1%B9%E7%9B%AE/%E5%BC%80%E8%AF%BE%E5%90%A7/%E6%B7%98%E5%AE%9D%E7%94%A8%E6%88%B7%E5%88%86%E6%9E%90/images/21.jpg)
由以上结果可以看出，每周活跃度比较稳定，每周五活跃度会有小幅降低，但是周末回慢慢回升，其中周五用户活跃度突增，这是由于双十二电商大促销活动引起。

### 5.基于RFM模型找出有价值的用户
RFM模型是衡量客户价值和客户创利能力的重要工具和手段，其中由3个要素构成数据Fenix最好的指标，分别是：  
R——Recency（最近一次购买时间）
F——Frequency（消费频率）
M——Money（消费金额）
由于数据源没有相关的金额数据，暂且通过R和F的数据对客户价值进行打分。
（1）计算R——Recency  
由于数据集包含的时间是从2014年11月18日至2014年12月18日，这里选取2014年12月19日作为计算日期，统计客户最近发生购买行为的日期距离2014年12月19日间隔几天，再对间隔时间进行排名，间隔天数越少，客户价值越大，排名越靠前。
![image](https://github.com/slackliu/data_analysis/blob/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E9%A1%B9%E7%9B%AE/%E5%BC%80%E8%AF%BE%E5%90%A7/%E6%B7%98%E5%AE%9D%E7%94%A8%E6%88%B7%E5%88%86%E6%9E%90/images/22.jpg)
（2）计算F——Frequency  
先统计每位用户的购买频率，再对购买评率进行排名，频率越大，客户价值越大，排名越靠前。
![image](https://github.com/slackliu/data_analysis/blob/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E9%A1%B9%E7%9B%AE/%E5%BC%80%E8%AF%BE%E5%90%A7/%E6%B7%98%E5%AE%9D%E7%94%A8%E6%88%B7%E5%88%86%E6%9E%90/images/23.jpg)
（3）对用户进行评分  
对4330名有购买行为的用户按照排名进行分组，共计划分为4组，对排在前四分之一的用户打4分，前二分之一的用户打3分，排在前四分之三的用户打2分，剩余的用户打1分，按照这个规则分别对用户时间间隔排名打分和购买频率排名打分，最后把两个分数合并在一起作为该名用户的最终评分。  
计算脚本如下：  
'''
SELECT r.user_id,r.recent,r.recent_rank,f.frequency,f.freq_rank,
CONCAT(  --  对客户购买行为的日期排名和频率排名进行打分
CASE WHEN r.recent_rank <= (4330/4) THEN '4'
WHEN r.recent_rank > (4330/4) AND r.recent_rank <= (4330/2) THEN '3'
WHEN r.recent_rank > (4330/2) AND r.recent_rank <= (4330/43) THEN '2'
ELSE '1' END,
CASE WHEN f.freq_rank <= (4330/4) THEN '4'
WHEN f.freq_rank > (4330/4) AND f.freq_rank <= (4330/2) THEN '3'
WHEN f.freq_rank > (4330/2) AND f.freq_rank <= (4330/43) THEN '2'
ELSE '1' END
) AS user_value
FROM
--  对每位用户最近发生购买行为的间隔时间进行排名（间隔天数越少，客户价值越大）
(SELECT a.,(@rank := @rank + 1) AS recent_rank
FROM  --  统计客户最近发生购买行为的日期距离'2014-12-19'间隔几天
(SELECT user_id,DATEDIFF('2014-12-19',MAX(date)) AS recent
FROM user
WHERE behavior_type = 'buy'
GROUP BY user_id
ORDER BY recent) AS a,
(SELECT @rank := 0) AS b)
AS r,
-- 对每位用户的购买频率进行排名（频率越大，客户价值越大）
(SELECT a.,(@rank2 := @rank2 + 1) AS freq_rank
FROM   --  统计每位用户的购买频率
(SELECT user_id,COUNT(behavior_type) AS frequency
FROM user
WHERE behavior_type = 'buy'
GROUP BY user_id
ORDER BY frequency DESC) AS a,
(SELECT @rank2 := 0) AS b)
AS f
WHERE r.user_id = f.user_id;
'''

![image](https://github.com/slackliu/data_analysis/blob/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E9%A1%B9%E7%9B%AE/%E5%BC%80%E8%AF%BE%E5%90%A7/%E6%B7%98%E5%AE%9D%E7%94%A8%E6%88%B7%E5%88%86%E6%9E%90/images/24.jpg)
通过打分可以了解每位顾客的特性，从而实现差异化营销，比如对于user_value = 44 的用户，为重点用户需要关注，对于user_value = 41这类忠诚度高且购买能力不足的用户，可以适当给与折扣或捆绑销售来增加用户的购买频率。


### 5.结论
1.总体转化率只有1%，用户点击后收藏和加购物车的转化率为5%，需要提高用户的购买意愿，可通过活动促销、精准营销等方式。  
2.购买率高且点击量少的用户属于理智型购物者，有明确购物目标，受促销和广告影响小，而购买率低的用户可分为等待型用户和克制型用户，下单欲望小且自制力强，购物难度大。  
3.大部分用户的主要活跃时间在10点到23点，在19点到23点达到一天的顶峰，每周五的活跃度有所下降，但周末开始回升，可以根据用户的活跃时间段精准推送商家的折扣优惠或促销活动，提高购买率。

4.通过R和F的数据对用户行为进行打分，对每位用户进行精准化营销，还可以通过R和F的数据进行检测，推测客户消费的异动情况，挽回流失客户。










































