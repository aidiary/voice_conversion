#coding: utf-8
import os
import numpy as np
import matplotlib.pyplot as plt

def draw_mcep(mcep_file1, mcep_file2, loc, order):
    mcep1 = np.loadtxt(mcep_file1)
    mcep2 = np.loadtxt(mcep_file2)
    plt.subplot(loc)
    plt.plot(mcep1[:, order], label=mcep_file1)
    plt.plot(mcep2[:, order], label=mcep_file2)
    plt.xlabel("frame")
    plt.title("%dth-order mcep" % order)
    plt.tight_layout()

if __name__ == "__main__":
    plt.figure(figsize=(8, 8))

    mcep_file1 = "mcep/clb/arctic_a0028.mcep"
    mcep_file2 = "mcep/slt/arctic_a0028.mcep"

    # オリジナル（左側）
    draw_mcep(mcep_file1, mcep_file2, 321, 0)
    draw_mcep(mcep_file1, mcep_file2, 323, 1)
    draw_mcep(mcep_file1, mcep_file2, 325, 2)

    mcep_file1 = "aligned_mcep_clb_slt/clb/arctic_a0028.mcep"
    mcep_file2 = "aligned_mcep_clb_slt/slt/arctic_a0028.mcep"

    # アラインメント後（右側）
    draw_mcep(mcep_file1, mcep_file2, 322, 0)
    draw_mcep(mcep_file1, mcep_file2, 324, 1)
    draw_mcep(mcep_file1, mcep_file2, 326, 2)

    plt.show()
