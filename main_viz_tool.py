import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import argparse
from data_viz import gen_graphs_container, gen_graphs_v2, gen_graphs_memory

def main():
    parser = argparse.ArgumentParser(description="Centralized Data Visualization Tool")
    parser.add_argument(
        "--script",
        type=str,
        required=True,
        choices=["gen_graphs_container", "gen_graphs_v2", "gen_graphs_memory"],
        help="Choose which visualization script to run",
    )
    parser.add_argument(
        "--base_dir",
        type=str,
        default="TRIAL-PAPER",
        help="Base directory for gen_graphs_container (only required for gen_graphs_container)"
    )
    parser.add_argument(
        "--results_dir",
        type=str,
        default="results",
        help="Directory to save the generated graphs"
    )
    args = parser.parse_args()    
    
    if args.script == "gen_graphs_container":
        gen_graphs_container.run(base_dir=args.base_dir, results_dir=args.results_dir)
    elif args.script == "gen_graphs_v2":
        gen_graphs_v2.run(results_dir=args.results_dir)
    elif args.script == "gen_graphs_memory":
        gen_graphs_memory.run(base_dir=args.base_dir, results_dir=args.results_dir)

    print(f"Graphs generated and saved in {args.results_dir}")        

if __name__ == "__main__":
    main()