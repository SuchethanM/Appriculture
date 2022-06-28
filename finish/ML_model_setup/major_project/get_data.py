import pandas as pd
import numpy as np
from temp_data import myfun
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import pickle
import joblib
from sklearn.tree import DecisionTreeRegressor
df = pd.read_csv("crop_data.csv")
# print(df.head())
tf = pd.read_csv("temperature.csv")
temparr = myfun(tf)


df = df[df["State_Name"]=="Karnataka"]
df = df[df["Crop_Year"]>1999]
df = df.drop("State_Name",axis=1)

# print(df.head())
# print()
district_name = df["District_Name"].unique()
# print(district_name)
crops = df["Crop"].unique()
# print(crops)
season = df["Season"].unique()
# print(season)
print(len(district_name),len(crops),len(season))
combined = list(district_name)+list(crops)+list(season)
# f = open("pre_pro.pkl","wb")
# pickle.dump(combined,f)
# f.close()

m = len(df)
# print(len(df))
df = df.dropna(axis=0)
# print(m-len(df))
print(len(combined))
k=0
data = []
X=[]
print(df.tail(5))
j=0
yr=2000
y=[]
for i in df[df.columns].values:
    # print(i)
    p = [combined.index(i[0])+1 , i[1] ,combined.index(i[2])+1,combined.index(i[3])+1,i[4],i[5]]
    data.append(p+temparr[i[1]-2000])
    h = [combined.index(i[0]) + 1, i[1], combined.index(i[2]) + 1, combined.index(i[3]) + 1, i[4]]
    X.append(h+temparr[i[1]-2000])
    y.append(i[5])

# print(X[-89])
X = np.array(X)
y = np.array(y)

# print(X[0])
print(X.shape,y.shape)
x_train,x_test,y_train,y_test = train_test_split(X,y,test_size=0.4)
print(x_train.shape,y_train.shape)

regressor = RandomForestRegressor(n_estimators=100,random_state=0)
regressor.fit(x_train,y_train)
ypred = regressor.predict(x_test)
score=r2_score(y_test,ypred)
print(score)
# if score>0.97:
#     joblib.dump(regressor,"./random_forest.joblib")


#
# deces  = DecisionTreeRegressor(random_state=0)
# deces.fit(x_train,y_train)
# y_predic = deces.predict(x_test)
# print(r2_score(y_test,y_predic))

# print(x_test[50])
# my = [30, 2023, 90, 47, 4073.0, 94.1, 25.8, 12.02, 1.44]
# my = np.array(my)
# print(regressor.predict([my]))



# preprocessing.MinMaxScaler()


