#coding:utf-8
#ランダムフォレストによる特徴選択

from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from itertools import compress
import numpy as np

class RandomForestC():
    def __init__(self):
        self.data=pd.read_csv('data/connected_train.csv')
        self.min = 1e-15
    def model_create(self):
        self.model=RandomForestClassifier(n_jobs=-1,verbose=1,n_estimators=200)
    def cross_validation(self,K=10):
        print('全体の長さ：'+str(len(self.data)))
        print('分割長：'+str(1.0*len(self.data)/K))
        split_length=int(1.0*len(self.data)/K)
        splited_data=[]
        for i in range(K):
            splited_data.append(self.data.ix[i*split_length:(i+1)*split_length])

        score=0
        #実際にK-Fold開始
        for i in range(K):
            logloss=0
            print(str(i+1)+'\tof\t'+str(K))
            bfilter=[True] * K
            bfilter[i]=False
            #compressでboolによるフィルタ
            train=list(compress(splited_data,bfilter))
            train=self.df_merge(train)
            test=splited_data[i]

            #モデル初期化
            self.model_create()
            #訓練
            self.fit(train.ix[:,6:],train[['tyuou','keihintohoku','keiyou','uchibou','saikyoukawagoe']])
            #予測
            pred=self.predict(test.ix[:,6:])
            for i in ('tyuou','keihintohoku','keiyou','uchibou','saikyoukawagoe'):
                logloss+=self.logloss(pred,test[i].as_matrix())
            logloss/=5
            print('途中スコア：'+str(logloss))
            score+=logloss
        score/=K
        print('最終スコア：'+str(score))


    def df_merge(self,data):
        tmp=pd.DataFrame()
        for i in data:
            tmp=tmp.append(i)
        return tmp
    def fit(self,x_train,y_train):
        tname=('tyuou','keihintohoku','keiyou','uchibou','saikyoukawagoe')
        for i in range(5):
            self.model.fit(x_train,y_train[tname[i]])
    def predict(self,x_test):
        pred=self.model.predict_proba(x_test)
        return pred
    def logloss(self,pred,act):
        logloss=0
        for i in range(len(act)):
            if pred[i,act[i]] < self.min:
                logloss+=np.log(self.min)
            else:
                logloss+=np.log(pred[i,act[i]])
        logloss/=len(act)
        logloss*=-1
        return logloss


if __name__=='__main__':
    myclass=RandomForestC()
    myclass.cross_validation(K=10)