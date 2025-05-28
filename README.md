# Centralized Data Visualization Tool

This tool provides a centralized interface for generating data visualizations using predefined scripts. It supports two main scripts: `gen_graphs_container` and `gen_graphs_v2`.

## Prerequisites

- Python 3.x installed on your system.
- Required Python packages installed (if any dependencies are needed, ensure they are installed).

## Usage

Run the tool using the command line. Below are the steps and options available:

### Command-Line Arguments

- `--script`: Specifies which visualization script to run. This is a required argument. Possible values are:
  - `gen_graphs_container`
  - `gen_graphs_v2`
- `--base_dir`: Specifies the base directory for the `gen_graphs_container` script. This argument is optional and defaults to `TRIAL-PAPER`. Note that the tool automatically prefixes this value with `data/`.

### Example Commands

1. To run the `gen_graphs_container` script with the default base directory:
   ```bash
   python main_viz_tool.py --script gen_graphs_container
   ```

2. To run the `gen_graphs_container` script with a custom base directory:
   ```bash
   python main_viz_tool.py --script gen_graphs_container --base_dir CUSTOM-DIR
   ```

3. To run the `gen_graphs_v2` script:
   ```bash
   python main_viz_tool.py --script gen_graphs_v2
   ```

## File Structure

Ensure the following file structure is maintained for the tool to work correctly:

```
data_viz/
    __init__.py
    gen_graphs_container.py
    gen_graphs_v2.py
    main_viz_tool.py
    data/
        results/
```

## Notes

- The `gen_graphs_container` script requires a base directory to locate the necessary data files. Ensure the directory exists under the `data/` folder.
- The `gen_graphs_v2` script does not require any additional arguments.

## Troubleshooting

If you encounter any issues, ensure that:

- The required scripts (`gen_graphs_container.py` and `gen_graphs_v2.py`) are present in the `data_viz` directory.
- The `data/` directory contains the necessary files and subdirectories.
- You are using the correct Python version and have installed all dependencies.