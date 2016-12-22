#coding: utf-8
import os
import numpy as np
import matplotlib.pyplot as plt
import subprocess
from scipy.stats.mstats_basic import spearmanr

def extract_binary_mcep(wav_file, mcep_file):
    cmd = "bcut +s -s 22 %s | x2x +sf | frame -p 80 | window | mcep -m 25 -a 0.42 > %s" % (wav_file, mcep_file)
    subprocess.call(cmd, shell=True)

def draw_mcep_at_frame(wav_file, mcep_file, frame, pos, title):
    # frame位置でのスペクトルを求める
    cmd = "bcut +s -s 22 %s | x2x +sf | frame -p 80 | bcut +f -l 256 -s %d -e %d | window | spec | dmp +f > spec.txt" % (wav_file, frame, frame)
    subprocess.call(cmd, shell=True)

    # frame位置でのメルケプストラムをスペクトルに変換
    cmd = "bcut +f -n 25 -s %d -e %d < %s | mgc2sp -m 25 -a 0.42 | dmp +f > mcep.txt" % (frame, frame, mcep_file)
    subprocess.call(cmd, shell=True)

    plt.subplot(pos)
    plt.title(title)

    # スペクトルとメルケプストラムを描画
    spec = np.loadtxt("spec.txt")
    plt.plot(spec[:, 1])

    mcep = np.loadtxt("mcep.txt")
    plt.plot(mcep[:, 1], "r-", lw=2)

    plt.xlabel("frequency bin")
    plt.ylabel("log magnitude")

    os.remove("spec.txt")
    os.remove("mcep.txt")

original_speaker = "clb"
target_speaker = "slt"
sid = "b0020"
frame = 50

plt.figure(figsize=(12, 4))

# オリジナルの声
wav_file = "wav/%s/arctic_%s.wav" % (original_speaker, sid)
mcep_file = "%s_%s.mcep" % (original_speaker, sid)
extract_binary_mcep(wav_file, mcep_file)
draw_mcep_at_frame(wav_file, mcep_file, frame, 131, "original (%s)" % original_speaker)
os.remove(mcep_file)

# ターゲットの声
wav_file = "wav/%s/arctic_%s.wav" % (target_speaker, sid)
mcep_file = "%s_%s.mcep" % (target_speaker, sid)
extract_binary_mcep(wav_file, mcep_file)
draw_mcep_at_frame(wav_file, mcep_file, frame, 132, "target (slt)")
os.remove(mcep_file)

# 変換した声
wav_file = "./converted_%s.wav" % sid
mcep_file = "./converted_%s.mcep" % sid
extract_binary_mcep(wav_file, mcep_file)
draw_mcep_at_frame(wav_file, mcep_file, frame, 133, "converted (%s=>%s)" % (original_speaker, target_speaker))
os.remove(mcep_file)

plt.tight_layout()
plt.show()
