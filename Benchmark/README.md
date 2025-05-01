# IM Graph Generation Script

This script generates Influence Maximization (IM) graphs for experiments involving threshold models and influence propagation. It allows users to configure graph properties and simulate either easy or hard IM problems.

## Requirements

- Python 3.8 
- Required packages listed in `requirements.txt`

Install dependencies with:

```bash
pip3 install -r requirements.txt
```


## Argument Description
```
| Argument       | Type   | Default | Description                                                           |
|----------------|--------|---------|-----------------------------------------------------------------------|
| `--path_to_dir` | str    | `'./'`  | Path to save generated files.                                         |
| `--num_graph`   | int    | 100     | Number of graphs to generate.                                         |
| `--num_nodes`   | int    | 100     | Number of nodes in each graph.                                        |
| `--th_min`      | float  | 0.5     | Minimum threshold for filtering edges.                                |
| `--higher_deth` | float  | 0.5     | Threshold for hard IM problems. Likely a typo—should be `--higher_depth`. |
| `--hard`        | flag   | False   | Generate hard IM problems.                                            |
| `--a`           | float  | 1.5     | Coefficient `a` in hard IM generation.                                |
| `--c`           | float  | 0.4     | Coefficient `c` in hard IM generation.                                |
| `--p_high`      | float  | 0.2     | Upper bound for edge probability in easy IM problems.                 |
| `--p_low`       | float  | 0.1     | Lower bound for edge probability in easy IM problems.                 |
```

## Examples

### 1. Generate 50 graphs with 200 nodes:
```bash
python3 ./Benchmark/generate_im_graphs.py --num_graph 50 --num_nodes 200
```

### 2. Generate hard IM problems with custom coefficients:
```bash
python3 ./Benchmark/generate_im_graphs.py --hard --a 2.0 --c 0.5
```
### 3. Save graphs to a specific directory:
```bash
python3 ./Benchmark/generate_im_graphs.py --path_to_dir ./graphs/
```