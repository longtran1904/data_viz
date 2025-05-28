import os
import matplotlib.pyplot as plt

def extract_and_plot_memory_log(input_path, output_path, graph_title, output_filename):
    # Ensure the output directory exists
    os.makedirs(output_path, exist_ok=True)

    # Read the memory log file
    memory_values = []
    with open(input_path, 'r') as file:
        for line in file:
            if "memory.current" in line or "memory.swap" in line:
                parts = line.split(":")
                if len(parts) > 1:
                    value = parts[1].strip().split()[0]  # Extract the numeric value
                    memory_values.append(int(value) / (1024 ** 3))  # Convert bytes to GB

    # Generate a time series graph
    plt.figure(figsize=(10, 6))
    plt.plot(memory_values, label=graph_title, color="blue")
    plt.title(graph_title)
    plt.xlabel("Time (seconds)")
    plt.ylabel("Memory Usage (GB)")
    plt.legend()
    plt.grid(True)

    # Save the graph to the results folder
    output_file = os.path.join(output_path, output_filename)
    plt.savefig(output_file)
    plt.close()

    print(f"Graph saved to {output_file}")

def safe_convert_to_gb(value):
    try:
        # Attempt to convert the value to an integer and then to GB
        return int(value) / (1024 ** 3)
    except (ValueError, TypeError):
        # If conversion fails, return None
        return None

def extract_and_plot_combined_memory_logs(input_path_current, input_path_swap, input_path_max, output_path, graph_title, output_filename):
    # Ensure the output directory exists
    os.makedirs(output_path, exist_ok=True)

    # Read the memory.current log file
    memory_current_values = []
    with open(input_path_current, 'r') as file:
        for line in file:
            if "memory.current" in line:
                parts = line.split(":")
                if len(parts) > 1:
                    value = parts[1].strip().split()[0]  # Extract the numeric value
                    memory_current_values.append(int(value) / (1024 ** 3))  # Convert bytes to GB

    # Read the memory.swap log file
    memory_swap_values = []
    with open(input_path_swap, 'r') as file:
        for line in file:
            if "memory.swap" in line:
                parts = line.split(":")
                if len(parts) > 1:
                    value = parts[1].strip().split()[0]  # Extract the numeric value
                    memory_swap_values.append(int(value) / (1024 ** 3))  # Convert bytes to GB

    # Read the memory.max log file and find the point where values become 0
    memory_max_values = []
    max_value = None
    zero_encountered = False
    with open(input_path_max, 'r') as file:
        for line in file:
            if "memory.max" in line:
                parts = line.split(":")
                if len(parts) > 1:
                    value = parts[1].strip().split()[0]  # Extract the numeric value
                    gb_value = safe_convert_to_gb(value)
                    if gb_value is not None:  # Only process valid numeric values
                        memory_max_values.append(gb_value)
                        if gb_value == 0:
                            zero_encountered = True
                    else:
                        memory_max_values.append(0)  # Append zero for invalid values
                        zero_encountered = True

    def filter_after_zero(data, memory_max_values):

        # Find the index where the max values stop being 0
        start_index = 0
        for i, value in enumerate(memory_max_values):
            if value == 0 and memory_max_values[i+1] != 0:
                start_index = i
                break

        return data[start_index:]

    memory_current_values = filter_after_zero(memory_current_values, memory_max_values)
    memory_swap_values = filter_after_zero(memory_swap_values, memory_max_values)
    memory_max_values = filter_after_zero(memory_max_values, memory_max_values)

    # Generate a combined time series graph
    plt.figure(figsize=(10, 6))
    plt.plot(memory_current_values, label="Memory Current Usage", color="blue")
    plt.plot(memory_swap_values, label="Memory Swap Usage", color="green")
    plt.plot(memory_max_values, label="Memory Max Usage", color="red")
    plt.title(graph_title)
    plt.xlabel("Time (seconds)")
    plt.ylabel("Memory Usage (GB)")
    plt.legend(loc="best")
    plt.grid(True)

    # Save the graph to the results folder
    output_file = os.path.join(output_path, output_filename)
    plt.savefig(output_file)
    plt.close()
    
def run(base_dir="data/yolo_log", results_dir="results"):
    BASE_DIR = base_dir    
    app = os.path.basename(BASE_DIR)
    
    input_log_path_current = os.path.join(BASE_DIR, "memory.current.log")
    input_log_path_swap = os.path.join(BASE_DIR, "memory.swap.log")
    input_log_path_max = os.path.join(BASE_DIR, "memory.max.log")
    output_dir = results_dir

    extract_and_plot_combined_memory_logs(
        input_log_path_current,
        input_log_path_swap,
        input_log_path_max,
        output_dir,
        f"Memory, Swap, and Max Usage Over Time of {app}",
        f"memory_usage_timeseries_{app}.pdf"
    )

if __name__ == "__main__":
    run()