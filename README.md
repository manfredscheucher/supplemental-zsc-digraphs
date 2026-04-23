# supplemental-zsc-digraphs

SAT-based computation of **n(A)** — the smallest complete digraph on n vertices whose edges can be labeled with elements of an abelian group A such that every cycle has non-zero sum.

Supplemental code to:

> Tamás Mészáros, Raphael Steiner —
> *Zero-sum cycles in complete digraphs*,
> European Journal of Combinatorics, 2021.
> [doi:10.1016/j.ejc.2021.103399](https://dl.acm.org/doi/abs/10.1016/j.ejc.2021.103399) · [arXiv:2103.04359](https://arxiv.org/abs/2103.04359)

The paper acknowledges: *"We would like to thank Manfred Scheucher very much for implementing and solving a SAT-model to compute the values of n(A) for groups of small order."*

## Files

- `zerosumcycles_sat.py` — refactored Python 3 version with `argparse` (refactored with Claude)
- `zerosumcycles_sat_py2.py` — original Python 2 script

## Usage

```
python3 zerosumcycles_sat.py <n> [--output FILE] [--no-cnf]
```

| Argument | Description |
|---|---|
| `n` | Number of vertices |
| `--output FILE` | Write DIMACS CNF to FILE (default: `instance.in`) |
| `--no-cnf` | Skip writing the CNF file |

## Example

```
$ python3 zerosumcycles_sat.py 4
(*) wlog 0
(*) assert labels 3
(*) assert no 0-sum cycles 15
assignment (0, 0, 0)
...
Total number of constraints: 87
Created CNF file: instance.in
sol 1:
D {(1, 2): 0, (2, 1): 1, ...}
```

## Dependencies

```
pip install pycosat
```
