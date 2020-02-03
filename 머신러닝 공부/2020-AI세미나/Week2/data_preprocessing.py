import pandas as pd
import numpy as np
from io import StringIO
from sklearn.impute import SimpleImputer
"""
csv파일을 읽어 들이는 함수
pd.read_csv(파일 위치)
"""
df=pd.read_csv("머신러닝 공부\2020-AI세미나\Week2\data_preprocessing.csv")

print(df)
"""
isnull().sum()을 자신이 원하는 배열 뒤에 붙이면 각 행에서 누락된 데이터의 개수를 확인 할 수 있음
"""
print(df.isnull().sum())

"""
누락 데이터가 존재하는 행 삭제
"""
print(df.dropna(axis=0))
"""
누락 데이터가 존재하는 열 삭제
"""
print(df.dropna(axis=1))
"""
모든 열이 누락 될 경우 행의 데이터 삭제
"""
print(df.dropna(how='all'))
"""
행의 실수 데이터 개수가 4개보다 작으면 삭제
"""
print(df.dropna(thresh=5))

"""
누락 데이터 대체를 위해 필요한 함수 불러들이기 - 예제에서는 sklearn의 impute 함수 중에서 가장 쉬운 SimpleImputer 함수를 사용할 예정임.
Simple impute는 하나의 범주로 데이터를 보고 취급을 함. 다중 변수에 대해서 적용을 하기 위해서는 IterativeImputer 함수를 사용해야한다.
KNN(nearest-neightbor) 기법을 통해서 적용을 하기 위해서는 KNNImputer 함수를 적용하는 것이 더욱 효율적임.
"""
import numpy as np
from sklearn.impute import SimpleImputer
print()
"""
missing_value를 설정하여 현재 내가 바꾸고 싶어하는 값 혹은 누락된 값이 표기되는 형식을 명시하고, 그에 따라서 어떠한 방식의 값으로 대체를 할 것인지 설정한다.
SimpleImputer의 경우 mean, median, most_frequent, constant 와 같은 4가지 전략이 있어서 이 중 자신이 원하는 데이터 대체 방식을 채택을 하면 된다.
"""
imr=SimpleImputer(missing_values=np.nan,strategy="constant")
imr=imr.fit(df.values)
imputed_data=imr.transform(df.values)

print("누락 데이터 대체")
print(df.values)
print(imputed_data)

"""
임의로 만들어 놓은 데이터에(옷에 대한 크기, 색, 가격을 넣은 데이터) 크기 특성을 순서에 맞게 특성 매칭을 하는 알고리즘
옷의 사이즈에 따라서 XL=3, L=2, M=1로 변환하여서 특성을 맵핑(기존의 순서적 관계도가 존재하여 맵핑이 가능한 경우)
"""
dt=pd.read_csv("머신러닝 공부\2020-AI세미나\Week2\mapping.csv")
print(dt)
size_mapping={
'XL':3,
'L':2,
'M':1
}
dt['size']=dt['size'].map(size_mapping)
print(dt)

"""
앞에서 진행한 옷의 크기와는 다르게 색에 대해서 특성을 표현하기 위해서는 색 정보에 대해서 one-hot encoder를 적용함.
one-hot encoder는 별도의 구현 없이 sklearn에서 제공하는 함수로 구현을 하였다.
"""
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
"""
one hot encoder에 categories를 통해서 어떠한 데이터를 학습을 할지 설정할 수 있음.
auto로 설정하면 자동으로 선택이 되고, 이외에는 원하는 열을 선택을 하여서 학습을 할 수 있음.
"""
ohe=OneHotEncoder(categories='auto')
col_trans=ColumnTransformer([('color_enc',ohe,['color'])],remainder='passthrough')
X_trans=col_trans.fit_transform(dt)
print("Encoded color")
print("  Blue/Green/Red")
print(X_trans)

