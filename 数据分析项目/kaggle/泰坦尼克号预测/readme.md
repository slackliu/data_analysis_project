## 2019年11月25日,开始做泰坦尼克号项目  
### 什么样的人更有可能生存?
#### 一、分析思路  
1. 提出问题  
    1.1. 乘客社会等级越高,幸存率越高  
    1.2. 不同title的乘客幸存率不同  
    1.3. 未成年幸存率高于成年人  
    1.4. 女性幸存率高于男性  
    1.5. 配偶数适中的乘客幸存率更高  
    1.6 父母与子女数为1到3的乘客幸存率更高  
    1.7 共票号乘客幸存率更高  
    1.8 票价高的乘客幸存率更高  
    1.9 不同船舱的幸存率不同  
    1.10 登船港口为c的乘客幸存率高  
    
2. 理解数据  
    搞清楚每个字段的意思,明白目标是什么? 
    
3.  数据清洗   
  3.1. 缺失值处理   
  3.2. 异常值处理    
  3.3. 格式一致化处理    
  3.4. 删除重复值  
  
4.  构建模型  

5. 模型评估  

6. 提交预测结果 

### 二、步骤处理 
1. 导入数据  
    将train.csv的数据.直接导入到数据库,并再导入test.csv中的数据,将数据合并,有利于预测  
2. 理解数据  
    - PassengerId: 乘客的ID，对预测没有用处  
    - Survived：1代表幸存，0代表遇难， 
    - Pclass：船票等级,可代表乘客的社会经济状况：1代表Upper，2代表Middle，3代表Lower  
    - Name：除包含姓名外，还包含Title相关信息  
    - Sex：性别   
    - Age：年龄  
    - SibSp：兄弟姐妹及配偶的个数  
    - Parch：父母或子女的个数  
    - Ticket：船票号  
    - Fare：船票价格  
    - Cabin：舱号 
    - Embarked：登船口岸  
3. 数据清洗  
    3.1. 缺失值处理  
        3.1.1. 查看缺失值  
            SELECT sum(PassengerId is NULL) as PassengerId, sum(Survived is NULL) as Survived,
sum(Pclass is NULL) as Pclass,sum(Name is NULL) as Name,sum(Sex is NULL) as Sex,
sum(Age is NULL) as Age,sum(SibSp is NULL) as SibSp,sum(Parch is NULL) as Parch,
sum(Ticket is NULL) as Ticket,sum(Fare is NULL) as Fare,sum(Cabin is NULL) as Cabin,
sum(Embarked is NULL) as Embarked from titanic;    
            ![image]()

