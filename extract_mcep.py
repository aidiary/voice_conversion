#coding: utf-8
import os
import sys

# wav_dirに含まれるwavファイルからメルケプストラム特徴量を抽出し、
# mcep_dirにテキスト形式で保存する
# 実行にはSPTKコマンドをパスに追加する必要がある

# メルケプストラム次数
# 実際はパワー項を追加して26次元ベクトルになる
m = 25

# all-pass constant
a = 0.42

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "usage: python extract_mcep.py <wav_dir> <mcep_dir>"
        exit()

    wav_dir = sys.argv[1]
    mcep_dir = sys.argv[2]

    if not os.path.exists(mcep_dir):
        os.makedirs(mcep_dir)

    for wav_file in os.listdir(wav_dir):
        wav_path = os.path.join(wav_dir, wav_file)
        mcep_path = os.path.join(mcep_dir, wav_file.replace(".wav", ".mcep"))

        print "%s => %s" % (wav_path, mcep_path)

        # SPTKのコマンドでWAVEファイルからメルケプストラムを抽出
        # bcutはrawファイルへの変換
        # numpyから読み込みやすいようにテキスト形式で出力する
        command = "bcut +s -s 22 %s | x2x +sf | frame -l 400 -p 80 | window -l 400 -L 512 | mcep -l 512 -m %d -a %f | x2x +fa%d > %s" % (wav_path, m, a, m+1, mcep_path)
        os.system(command)
