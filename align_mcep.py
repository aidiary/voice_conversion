#coding: utf-8
import os
import sys
import numpy as np

# Dynamic Time Warping Library
# pip install dtwでインストール可能
from dtw import dtw

# extract_mcep.pyでメルケプストラムを抽出済みであることが前提
# 二人分のメルケプストラムディレクトリを入力（mcep_dir1, mcep_dir2）として指定する
# 二人の対応するメルケプストラムファイル同士でDTWを適用し、
# アラインメントを取ったメルケプストラム（aligned_mcep_dir1, aligned_mcep_dir2）を出力する

def draw_mcep(mcep_file1, mcep_file2):
    pass

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print "usage: python align_mcep.py <mcep_dir1> <mcep_dir2> <aligned_mcep_dir1> <aligned_mcep_dir2>"
        exit()

    mcep_dir1 = sys.argv[1]
    mcep_dir2 = sys.argv[2]
    aligned_mcep_dir1 = sys.argv[3]
    aligned_mcep_dir2 = sys.argv[4]

    if not os.path.exists(aligned_mcep_dir1):
        os.makedirs(aligned_mcep_dir1)

    if not os.path.exists(aligned_mcep_dir2):
        os.makedirs(aligned_mcep_dir2)

    for mcep_file in os.listdir(mcep_dir1):
        # 対応するmcepファイルがなかったら無視する
        if not os.path.exists(os.path.join(mcep_dir2, mcep_file)):
            print "ERROR: mcep not found: %s" % os.path.join(mcep_dir2, mcep_file)
            continue

        print mcep_file

        # オリジナルのmcepを読み込み
        mcep1 = np.loadtxt(os.path.join(mcep_dir1, mcep_file))
        mcep2 = np.loadtxt(os.path.join(mcep_dir2, mcep_file))

        # DTWで同期を取る
        dist, cost, path = dtw(mcep1, mcep2)
        aligned_mcep1 = mcep1[path[0]]
        aligned_mcep2 = mcep2[path[1]]

        # 同期を取ったmcepをテキスト形式で書き込み
        np.savetxt(os.path.join(aligned_mcep_dir1, mcep_file), aligned_mcep1, fmt="%0.6f")
        np.savetxt(os.path.join(aligned_mcep_dir2, mcep_file), aligned_mcep2, fmt="%0.6f")
