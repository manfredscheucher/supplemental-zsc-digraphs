import argparse
from itertools import combinations, permutations, product
import pycosat


def parse_args():
    parser = argparse.ArgumentParser(
        description="SAT encoding: Zero-Sum Cycles in Complete Digraphs (Z_k group)"
    )
    parser.add_argument("n", type=int, help="Number of vertices")
    parser.add_argument(
        "--output", "-o", default="instance.in", metavar="FILE",
        help="Write DIMACS CNF to FILE (default: instance.in)"
    )
    parser.add_argument(
        "--no-cnf", action="store_true",
        help="Skip writing the CNF file"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    n = args.n

    V = list(range(1, n + 1))          # vertices 1 … n
    k = len(V) - 1                     # group order (Z_k)
    A = range(k)

    E = [(u, v) for u, v in combinations(V, 2)]   # undirected edges
    E_rev = [(v, u) for (u, v) in E]
    E_both = sorted(E + E_rev)                    # all directed edges, deterministic order

    # Variable index: ('label', (u, v, a)) -> SAT variable number (1-based)
    all_variables_index = {
        ('label', (u, v, a)): i
        for i, (u, v, a) in enumerate(
            (u, v, a) for u, v in E_both for a in A
        )
    }
    num_vars = len(all_variables_index)

    def var(label_tuple):
        return 1 + all_variables_index[('label', label_tuple)]

    def var_label(u, v, a):
        return var((u, v, a))

    def parse_sol(sol):
        sol_set = set(sol)
        D_labels = {}
        for (u, v) in E_both:
            for a in A:
                if var_label(u, v, a) in sol_set:
                    D_labels[u, v] = a
        print("D", D_labels)

    constraints = []

    # Symmetry breaking (wlog)
    print(f"(*) wlog {len(constraints)}")
    if len(V) >= 4:
        constraints.append([var_label(2, 1, 1)])
        for i in range(1, len(V)):
            constraints.append([var_label(i, i + 1, 0)])

    # Each directed edge gets exactly one label
    print(f"(*) assert labels {len(constraints)}")
    for u, v in E_both:
        constraints.append([var_label(u, v, a) for a in A])          # at least one
        for a, b in combinations(A, 2):
            constraints.append([-var_label(u, v, a), -var_label(u, v, b)])  # at most one

    # No zero-sum cycles
    print(f"(*) assert no 0-sum cycles {len(constraints)}")
    for t in range(2, len(V) + 1):
        for assignment in product(A, repeat=t):
            if sum(assignment) % k == 0:
                print("assignment", assignment)
                for pi in permutations(V, t):
                    constraints.append(
                        [-var_label(pi[i - 1], pi[i], assignment[i]) for i in range(t)]
                    )

    print(f"Total number of constraints: {len(constraints)}")

    if not args.no_cnf:
        with open(args.output, "w") as f:
            f.write(f"p cnf {num_vars} {len(constraints)}\n")
            for c in constraints:
                f.write(" ".join(str(v) for v in c) + " 0\n")
        print(f"Created CNF file: {args.output}")

    sol = next(pycosat.itersolve(constraints), None)
    if sol is None:
        print("no solution!?")
    else:
        print("sol 1:")
        parse_sol(sol)


if __name__ == "__main__":
    main()
