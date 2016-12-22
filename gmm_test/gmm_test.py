#coding:utf-8
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import sklearn.mixture

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

# GMMを学習
n_components = 2
gmm = sklearn.mixture.GMM(n_components, covariance_type='full')
gmm.fit(X_train)

# 結果を表示
print "*** weights"
print gmm.weights_

print "*** means"
print gmm.means_

print "*** covars"
print gmm.covars_

# 訓練データを描画
plt.plot(X_train[:, 0], X_train[:, 1], 'gx')

# 推定したガウス分布を描画
x = np.linspace(-2.5, 2.5, 1000)
y = np.linspace(-2.5, 2.5, 1000)
X, Y = np.meshgrid(x, y)

# 各ガウス分布について
for k in range(n_components):
    # 平均を描画
    plt.plot(gmm.means_[k][0], gmm.means_[k][1], 'ro')
    # ガウス分布の等高線を描画
    Z = mlab.bivariate_normal(X, Y,
                              np.sqrt(gmm.covars_[k][0][0]), np.sqrt(gmm.covars_[k][1][1]),
                              gmm.means_[k][0], gmm.means_[k][1],
                              gmm.covars_[k][0][1])
    plt.contour(X, Y, Z)

# メッシュ上の各点での対数尤度の等高線を描画
XX = np.array([X.ravel(), Y.ravel()]).T
Z = gmm.score_samples(XX)[0]
Z = Z.reshape(X.shape)
CS = plt.contour(X, Y, Z)
CB = plt.colorbar(CS)

plt.xlim(-2.5, 2.5)
plt.ylim(-2.5, 2.5)
plt.show()
