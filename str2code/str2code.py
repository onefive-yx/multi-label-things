import pandas as pd
from sklearn.preprocessing import LabelEncoder

names = ['Foodtruck', 'Genbase']
for name in names:
    for t in ['train', 'test']:
        for s in ['attributes', 'labels']:
            # 读取 CSV 文件
            df = pd.read_csv(f'./{name}_syb/{name}-{t}-{s}.csv')

            # 使用 LabelEncoder 转换字符串特征
            label_encoders = {}
            for col in df.columns:
                if df[col].dtype == 'object':
                    le = LabelEncoder()
                    df[col] = le.fit_transform(df[col])
                    label_encoders[col] = le
            # 查看转换后的数据
            print(df)
            df.to_csv(f'./{name}/{name}-{t}-{s}.csv', index=False)