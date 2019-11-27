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

</br>


### 二、步骤处理 
1. **导入数据**   
    将train.csv的数据.直接导入到数据库,并再导入test.csv中的数据,将数据合并,有利于预测  
2. **理解数据**  
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
    
</br>

3. **数据清洗**  
    3.1. 缺失值处理     
         3.1.1. 查看缺失值      
    ``` SQL SELECT sum(PassengerId is NULL) as PassengerId, sum(Survived is NULL) as Survived,
        sum(Pclass is NULL) as Pclass,sum(Name is NULL) as Name,sum(Sex is NULL) as Sex,
        sum(Age is NULL) as Age,sum(SibSp is NULL) as SibSp,sum(Parch is NULL) as Parch,
        sum(Ticket is NULL) as Ticket,sum(Fare is NULL) as Fare,sum(Cabin is NULL) as Cabin,
        sum(Embarked is NULL) as Embarked from titanic;  ```  
   查询结果:发现survived有418个缺失值,age有263个缺失值,Fare有1个缺失值,cabin有1014个缺失值,     
![image](https://github.com/slackliu/data_analysis/blob/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E9%A1%B9%E7%9B%AE/kaggle/%E6%B3%B0%E5%9D%A6%E5%B0%BC%E5%85%8B%E5%8F%B7%E9%A2%84%E6%B5%8B/images/sql_chaxunqueshizhi.png)  

</br>

3.1.2. 补充缺失值  
            1. Embarked有2个缺失值,查看其具体情况.  
               ``` SQL  SELECT * from titanic WHERE Embarked is NULL;```  
* 查询结果:
                ![image](https://github.com/slackliu/data_analysis/blob/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E9%A1%B9%E7%9B%AE/kaggle/%E6%B3%B0%E5%9D%A6%E5%B0%BC%E5%85%8B%E5%8F%B7%E9%A2%84%E6%B5%8B/images/SQL_embarked_%E7%BC%BA%E5%A4%B1%E5%80%BC%E6%83%85%E5%86%B5.png)  
                
        发现其票价都为80,而且Pclass为1,假设票价,舱位,Pclass相同者在同一登船港口上船,这也比较符合实际情况,头等舱顾客总是提前登机嘛~   
        
        查询Pclass为1各个登船港口的乘客信息,并将其保存到Embarked.csv文件中,根据Embarked.csv中的数据画出箱型图
            SELECT * from titanic WHERE Embarked = 'c' and Pclass = 1;
            SELECT * from titanic WHERE Embarked = 's' and Pclass = 1;
            SELECT * from titanic WHERE Embarked = 'q' and Pclass = 1;
            画箱型图的代码为:    
            '''python
            import numpy as np
            import pandas as pd
            import matplotlib as mpl
            import matplotlib.pyplot as plt
            import seaborn as sns
            import warnings
            warnings.filterwarnings('ignore')
            df = pd.read_csv(r"C:\Users\admin\Desktop\Embarked.csv")
            plt.figure(figsize=(10, 8), dpi=100)
            xlabels = ['S', 'C', 'Q']
            sns.boxplot(x='Embarked', y='Fare', data=df, notch=False)
            plt.yticks(range(0, 600)[::20])
            plt.title('Box Plot of Fare', fontsize=22)
            plt.show()
            '''    
            得到箱型图:  
            ![image](https://github.com/slackliu/data_analysis/blob/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E9%A1%B9%E7%9B%AE/kaggle/%E6%B3%B0%E5%9D%A6%E5%B0%BC%E5%85%8B%E5%8F%B7%E9%A2%84%E6%B5%8B/images/Fare%E7%AE%B1%E5%9E%8B%E5%9B%BE.png)  
            * 由此可以得出Pclass为1,登船港口为C的中位数为80,因此我们将Embarked缺失的值补充为C  
         2.Fare缺失值只有一个,查看具体情况  
         select * from titanic where Fare is null;  
         ![image](https://github.com/slackliu/data_analysis/blob/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E9%A1%B9%E7%9B%AE/kaggle/%E6%B3%B0%E5%9D%A6%E5%B0%BC%E5%85%8B%E5%8F%B7%E9%A2%84%E6%B5%8B/images/Fare%E7%BC%BA%E5%A4%B1%E5%85%B7%E4%BD%93%E6%83%85%E5%86%B5.png)  
         查询登船港口为S,Pclass为3的乘客的基本信息,并将其导入到Fare.csv文件中,由此画出箱线图,  
         SELECT * from titanic WHERE Pclass = 3 and Embarked = 's' AND Fare IS NOT NULL;  
         """ python
         import numpy as np
         import pandas as pd
         import matplotlib as mpl
         import matplotlib.pyplot as plt
         import seaborn as sns
         import warnings
         warnings.filterwarnings('ignore')
         df = pd.read_csv(r"C:\Users\admin\Desktop\Fare.csv")
         plt.figure(figsize=(10, 8), dpi=100)
         xlabels = ['S', ]
         sns.boxplot(x='Embarked', y='Fare', data=df, notch=False)
         plt.yticks(range(0, 60)[::3])
         plt.title('Box Plot of Fare', fontsize=22)
         plt.show()
         """  
         得到箱线图:  
         ![image](https://github.com/slackliu/data_analysis/blob/master/%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E9%A1%B9%E7%9B%AE/kaggle/%E6%B3%B0%E5%9D%A6%E5%B0%BC%E5%85%8B%E5%8F%B7%E9%A2%84%E6%B5%8B/images/Fare%E5%88%86%E5%B8%83%E7%AE%B1%E7%BA%BF%E5%9B%BE.png)
         由此得知其中位数为12,将Fare缺失的值补充为12.  
      3. 补充Age缺失值  
      ``` SQL select count(*) from Titanic where age is null;```  
      由于Age缺失值较多，需要通过其他的变量来预测，暂时不进行缺失值的填补，先进行特征抽取。
         
4. **数据计算**  
    从以下几点分析问题:   
    1. 船舱等级与幸存率之间的关系   
    2. 女性幸存率高于男性  
    3. 配偶数适中的乘客幸存率更高  
    4. 父母与子女数为1到3的乘客幸存率更高  
    5. 不同船舱的幸存率不同  
    6. 登船港口为c的乘客幸存率高  
    7. 不同title与幸存率之间的关系  
    8. 未成年幸存率高于成年人  
    
    

