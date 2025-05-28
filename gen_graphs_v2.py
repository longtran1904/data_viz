# Re-import necessary packages after code execution reset
import os
import re
import matplotlib.pyplot as plt
import numpy as np

def run(results_dir="results"):
    # Ensure the results directory exists
    os.makedirs(results_dir, exist_ok=True)

    # Data (manually restored from earlier extraction)
    # memory_labels = ["40GB", "44GB", "48GB"] # Training 
    memory_labels = ["24GB", "36GB", "42GB"]  # Inference
    memory_labels_rev = memory_labels[::-1]
    x = np.arange(len(memory_labels_rev))

    # Throughput in 1000s of ops/sec, reversed for plotting
    # Training
    # rocksdb_isolated_k = [343.348, 345.016, 339.937][::-1]
    # rocksdb_shared_k = [270.002, 297.065, 304.338][::-1]

    # Inference
    rocksdb_isolated_k = [342.086, 341.959, 340.974][::-1]
    rocksdb_shared_k = [202.930, 246.186, 264.911][::-1]

    # YOLO runtime (sec), reversed
    # Training
    # yolo_runtime_rev = [471, 474, 472][::-1]
    # yolo_shared_runtime_rev = [530, 537, 534][::-1]

    # Inference
    yolo_runtime_rev = [281, 283, 280][::-1]
    yolo_shared_runtime_rev = [311, 332, 299][::-1]
    # Custom y-ticks
    custom_yticks = [200, 400, 600, 800, 1000]

    # Plot: Set font size globally (3x)
    plt.rcParams.update({
        'font.size': plt.rcParams['font.size'] * 4.8,
        'font.family': 'Times New Roman',
        # 'font.serif': 'Times'
    })
    # Colors
    isolated_color = '#156082'
    shared_color = '#e97131'
    # === Style Constants ===
    bar_width = 0.35
    base_font_size=plt.rcParams['font.size']

    # Plotting with only major grid lines
    fig, axs = plt.subplots(
        ncols=2,
        figsize=(28, 12),
    )

    # Subplot 1: RocksDB Throughput
    axs[0].bar(x - bar_width/2, rocksdb_isolated_k, bar_width, label='Isolated RocksDB', color=isolated_color)
    axs[0].bar(x + bar_width/2, rocksdb_shared_k, bar_width, label='Shared RocksDB', color=shared_color)

    axs[0].set_xlabel('System Memory')
    axs[0].set_ylabel('Throughput (x1000 ops/sec)')

    axs[0].set_xticks(x)
    axs[0].set_xticklabels(memory_labels_rev)
    # axs[0].set_yticks(custom_yticks)
    axs[0].legend(loc='upper center', bbox_to_anchor=(0.5, 1.25), ncol=2, columnspacing=0.5, frameon=False)
    axs[0].grid(False)  # Only major grid lines
    axs[0].text(0.5, -0.3, "(a) RocksDB", fontweight='bold', fontsize=1.15*base_font_size, ha='center', transform=axs[0].transAxes)

    # Subplot 2: YOLO Runtime
    axs[1].bar(x - bar_width/2, yolo_runtime_rev, bar_width, label='Isolated YOLO', color=isolated_color)
    axs[1].bar(x + bar_width/2, yolo_shared_runtime_rev, bar_width, label='Shared YOLO', color=shared_color)
    axs[1].set_xlabel("System Memory")
    axs[1].set_ylabel('Runtime (seconds)')

    axs[1].set_xticks(x)
    axs[1].set_xticklabels(memory_labels_rev)
    axs[1].legend(loc='upper center', bbox_to_anchor=(0.5, 1.25), ncol=2, columnspacing=0.5, frameon=False)
    axs[1].grid(False)  # Only major grid lines
    axs[1].text(0.5, -0.3, "(b) YOLO Inference", fontweight='bold', fontsize=1.15*base_font_size, ha='center', transform=axs[1].transAxes)

    for ax in axs:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    plt.subplots_adjust(
        left=0.1,   # Left margin — 0 means far left, 1 is far right
        right=0.96,  # Right margin — this is how far the plot can go to the right
        top=0.7,     # Top margin — how close the plot can get to the top
        bottom=0.15  # Bottom margin — how close the plot can get to the bottom
    )
    plt.savefig(os.path.join(results_dir, "shared.pdf"), bbox_inches="tight")
    # plt.show()