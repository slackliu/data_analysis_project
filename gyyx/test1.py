import pandas as pd
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('expand_frame_repr', False)  # True 是可以换行显示，False不允许换行
pd.set_option('display.max_rows', 200)  # 显示200行
pd.set_option('display.max_columns', 200)  # 显示200列


df = pd.DataFrame({'Sp':['a','b','c','d','e','f'], 'Mt':['s1', 's1', 's2','s2','s2','s3'], 'Value':[1,2,3,4,5,6], 'Count':[3,2,5,10,10,6]})
print(df)

a = df.groupby('Mt').apply(lambda t: t[t.Count==t.Count.max()])
print(a)