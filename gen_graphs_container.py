import os
import re
import matplotlib.pyplot as plt
import numpy as np

def run(base_dir="TRIAL-PAPER", results_dir="results"):
    # Ensure the results directory exists
    os.makedirs(results_dir, exist_ok=True)

    # Set this to your local SHARE directory path
    BASE_DIR = base_dir

    # Helper to extract RocksDB throughput (ops/sec)
    def extract_rocksdb_throughput(filepath):
        with open(filepath, 'r') as f:
            lines = f.readlines()
        for line in reversed(lines):
            if "ops/sec" in line:
                parts = line.strip().split()
                for i, part in enumerate(parts):
                    if part == "ops/sec":
                        try:
                            return float(parts[i - 1])
                        except:
                            continue
        return None

    # Helper to extract YOLO runtime from program_log.txt
    def extract_runtime_seconds(filepath):
        with open(filepath, 'r') as f:
            lines = f.readlines()
        for line in lines:
            if "Elapsed (wall clock) time" in line:
                match = re.search(r'(\d+):(\d+\.\d+)', line)
                if match:
                    minutes = int(match.group(1))
                    seconds = float(match.group(2))
                    return minutes * 60 + seconds
        return None

    # Memory configurations
    mem_configs = ["MEM-24GB", "MEM-32GB", "MEM-40GB"]
    rocksdb_config = ["ROCKSDB-MEM-16", "ROCKSDB-MEM-24", "ROCKSDB-MEM-32"]

    # Collected data
    rocksdb_isolated = []
    rocksdb_shared = []
    yolo_runtime_isolated = []
    yolo_runtime_shared = []

    for idx, mem in enumerate(mem_configs):
        base = os.path.join(BASE_DIR, f"YOLO-MEM-8-{rocksdb_config[idx]}", "inference")

        # RocksDB throughput
        isolated_rdb = os.path.join(base, "isolated-rocksdb", "num_threads_8", "isolated-rocksdb.out")
        shared_rdb = os.path.join(base, "shared-rocksdb-yoloinference", "num_threads_8", "shared-rocksdb-yoloinference.out")
        rocksdb_isolated.append(extract_rocksdb_throughput(isolated_rdb))
        rocksdb_shared.append(extract_rocksdb_throughput(shared_rdb))

        # YOLO runtimes
        iso_yolo_log = os.path.join(base, "isolated-yolo-inference", "num_threads_8", "program_log.txt")
        shared_yolo_log = os.path.join(base, "shared-rocksdb-yoloinference", "num_threads_8", "program_log.txt")
        yolo_runtime_isolated.append(extract_runtime_seconds(iso_yolo_log))
        yolo_runtime_shared.append(extract_runtime_seconds(shared_yolo_log))

    # Reverse data order for plotting
    memory_labels = ["24GB", "32GB", "40GB"]
    memory_labels_rev = memory_labels[::-1]
    x = np.arange(len(memory_labels_rev))
    width = 0.35

    rocksdb_isolated_k = [v / 1e3 for v in rocksdb_isolated][::-1]
    rocksdb_shared_k = [v / 1e3 for v in rocksdb_shared][::-1]
    yolo_runtime_rev = yolo_runtime_isolated[::-1]
    yolo_shared_runtime_rev = yolo_runtime_shared[::-1]

    # Custom y-ticks for throughput
    custom_yticks = [200, 400, 600, 800, 1000]

    # Plot: Set font size globally (3x)
    plt.rcParams.update({
        'font.size': plt.rcParams['font.size'] * 4.8,
        'font.family': 'Times New Roman',
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
    axs[0].legend(loc='upper center', bbox_to_anchor=(0.5, 1.25), ncol=2, columnspacing=0.5, frameon=False)
    axs[0].grid(False)  # Only major grid lines
    axs[0].text(0.5, -0.3, "(a) Container RocksDB", fontweight='bold', fontsize=1.15*base_font_size, ha='center', transform=axs[0].transAxes)

    # Subplot 2: YOLO Runtime
    axs[1].bar(x - bar_width/2, yolo_runtime_rev, bar_width, label='Isolated YOLO', color=isolated_color)
    axs[1].bar(x + bar_width/2, yolo_shared_runtime_rev, bar_width, label='Shared YOLO', color=shared_color)
    axs[1].set_xlabel("System Memory")
    axs[1].set_ylabel('Runtime (seconds)')

    axs[1].set_xticks(x)
    axs[1].set_xticklabels(memory_labels_rev)
    axs[1].legend(loc='upper center', bbox_to_anchor=(0.5, 1.25), ncol=2, columnspacing=0.5, frameon=False)
    axs[1].grid(False)  # Only major grid lines
    axs[1].text(0.5, -0.3, "(b) Container YOLO", fontweight='bold', fontsize=1.15*base_font_size, ha='center', transform=axs[1].transAxes)

    for ax in axs:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    plt.subplots_adjust(
        left=0.1,   # Left margin — 0 means far left, 1 is far right
        right=0.96,  # Right margin — this is how far the plot can go to the right
        top=0.7,     # Top margin — how close the plot can get to the top
        bottom=0.15  # Bottom margin — how close the plot can get to the bottom
    )
    plt.savefig(os.path.join(results_dir, "container.pdf"), bbox_inches="tight")
    # plt.show()