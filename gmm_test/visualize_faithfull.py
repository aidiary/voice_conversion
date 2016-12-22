#coding:utf-8
import numpy as np
import matplotlib.pyplot as plt

def scale(X):
    """データ行列Xを属性ごとに標準化したデータを返す"""
    # 属性の数（=列の数）
    col = X.shape[1]

    # 属性ごとに平均値と標準偏差を計算
    mu = np.mean(X, axis=0)
    sigma = np.std(X, axis=0)

    # 属性ごとデータを標準化
    for i in range(col):
        X[:,i] = (X[:,i] - mu[i]) / sigma[i]

    return X

# faithful.txtデータをロード
data = np.genfromtxt("faithful.txt")
X_train = scale(data)
N = len(X_train)

# 散布図をプロット
plt.plot(X_train[:, 0], X_train[:, 1], 'gx')
plt.xlim(-2.5, 2.5)
plt.ylim(-2.5, 2.5)
plt.grid()
plt.show()
