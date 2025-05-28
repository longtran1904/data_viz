# Centralized Data Visualization Tool

This repository provides a centralized interface for generating data visualizations using predefined scripts. The main entry point is `main_viz_tool.py`, which allows users to run various visualization scripts.

## Prerequisites

- Python 3.x installed on your system.

## Usage

Run the tool using the command line. Below are the steps and options available:

### Command-Line Arguments

- `--script`: Specifies which visualization script to run. This is a required argument. Possible values are:
  - `gen_graphs_container`
  - `gen_graphs_v2`
  - `gen_graphs_memory`
- `--base_dir`: Specifies the base directory for the `gen_graphs_container` and `gen_graphs_memory` scripts. This argument is optional and defaults to `TRIAL-PAPER`. Note that the tool automatically prefixes this value with `data/`.
- `--results_dir`: Specifies the directory where the generated graphs will be saved. Defaults to `results`.

### Example Commands

1. To run the `gen_graphs_container` script with the DEFAULT base directory:
   ```bash
   python main_viz_tool.py --script gen_graphs_container
   ```

2. To run the `gen_graphs_container` script with a CUSTOM base directory:
   ```bash
   python main_viz_tool.py --script gen_graphs_container --base_dir CUSTOM-DIR
   ```

3. To run the `gen_graphs_v2` script:
   ```bash
   python main_viz_tool.py --script gen_graphs_v2
   ```

4. To run the `gen_graphs_memory` script with a custom base directory and results directory:
   ```bash
   python main_viz_tool.py --script gen_graphs_memory --base_dir data/yolo_log --results_dir custom_results
   ```

## File Structure

Ensure the following file structure is maintained for the tool to work correctly:

```
data_viz/
    __init__.py
    gen_graphs_container.py
    gen_graphs_v2.py
    gen_graphs_memory.py
    main_viz_tool.py
    README.md
    data/
        yolo_log/
        rocksdb_log/
    results/
```

## Notes

- The `gen_graphs_container` and `gen_graphs_memory` scripts require a base directory to locate the necessary data files. Ensure the directory exists under the `data/` folder.
- The `gen_graphs_v2` script does not require any additional arguments.
- The `results_dir` parameter allows you to specify where the generated graphs will be saved.

## Troubleshooting

If you encounter any issues, ensure that:

- The required scripts (`gen_graphs_container.py`, `gen_graphs_v2.py`, and `gen_graphs_memory.py`) are present in the `data_viz` directory.
- The `data/` directory contains the necessary files and subdirectories.
- You are using the correct Python version and have installed all dependencies.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.