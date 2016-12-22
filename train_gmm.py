#coding: utf-8
import os
import sys
import numpy as np
from sklearn import mixture
from sklearn.externals import joblib
import matplotlib.pyplot as plt

# メルケプストラム次数
# 実際はパワー項を追加して26次元ベクトルになる
m = 25

# GMMのコンポーネント数
M = 64

def make_joint_vectors(aligned_mcep_dir1, aligned_mcep_dir2, num_train, dim):
    """変換元と変換先の特徴ベクトルを結合したデータを作成して返す"""
    # 0行目はvstack()するためのダミー
    X = np.zeros((1, dim))
    Y = np.zeros((1, dim))

    # mcepファイルをロード
    for mcep_file in os.listdir(aligned_mcep_dir1)[:num_train]:
        # 対応するmcepファイルがなかったら無視する
        if not os.path.exists(os.path.join(aligned_mcep_dir2, mcep_file)):
            print "ERROR: mcep not found: %s" % os.path.join(aligned_mcep_dir2, mcep_file)
            continue

        mcep1 = np.loadtxt("%s/%s" % (aligned_mcep_dir1, mcep_file))
        mcep2 = np.loadtxt("%s/%s" % (aligned_mcep_dir2, mcep_file))
        X = np.vstack((X, mcep1))
        Y = np.vstack((Y, mcep2))

    # ダミー行を除く
    X = X[1:, :]
    Y = Y[1:, :]

    # 変換元と変換先の特徴ベクトルを結合
    Z = np.hstack((X, Y))

    return Z

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "usage: python train_gmm.py <aligned_mcep_dir1> <aligned_mcep_dir2> <gmm_file>"
        exit()

    aligned_mcep_dir1 = sys.argv[1]
    aligned_mcep_dir2 = sys.argv[2]
    gmm_file = sys.argv[3]

    # 変換元と変換先の特徴ベクトルを結合したデータを作成
    num_train = 100
    Z = make_joint_vectors(aligned_mcep_dir1, aligned_mcep_dir2, num_train, m + 1)

    # バイナリ形式で保存しておく
    np.save("Z.npy", Z)

    # 混合ガウスモデル
    g = mixture.GMM(n_components=M, covariance_type='full')
    g.fit(Z)

    # モデルをファイルに保存
    joblib.dump(g, gmm_file)

    # 最初の3コンポーネントの平均ベクトルを描画
    for k in range(3):
        plt.plot(g.means_[k, :])
    plt.xlim((0, (m+1)*2))
    plt.show()

    # 0番目のコンポーネントの共分散行列を描画
    plt.imshow(g.covars_[0])
    plt.show()
