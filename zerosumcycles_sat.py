from itertools import *
from sys import *
import pycosat


n = int(argv[1])
V = range(1,n+1) # vertices 1 ... n

E = [(u,v) for u,v in combinations(V,2)] # complete graph

k = len(V)-1
A = range(k)
group_addition = {(a,b):((a+b)%k) for a in A for b in A} # Z_k

#group_addition = {(a,b):(a^b) for a in A for b in A} # Z_2 x Z_2


E_rev = [(v,u) for (u,v) in E]
E_both = set(E+E_rev)


all_variables = []
all_variables += [('label',(u,v,a)) for u,v in E_both for a in A] 


all_variables_index = {}

_num_vars = 0
for v in all_variables:
    all_variables_index[v] = _num_vars
    _num_vars += 1

def var(L):	return 1+all_variables_index[L]
def var_label(*L): return var(('label',L))


def parse_sol(sol):
	D_labels = {}
	for (u,v) in E_both:
		for a in A:
			if var_label(u,v,a) in sol:
				D_labels[u,v] = a
	print "D",D_labels



constraints = []


print "(*) wlog",len(constraints)
if len(V) >= 4:
	constraints.append([var_label(2,1,1)])
	for i in range(1,len(V)):
		constraints.append([var_label(i,i+1,0)])


print "(*) assert labels",len(constraints)
for u,v in E_both:
	# (u,v) gets at least one label
	constraints.append([var_label(u,v,a) for a in A])
	# (u,v) gets at most one label
	for a,b in combinations(A,2):
		constraints.append([-var_label(u,v,a),-var_label(u,v,b)])


print "(*) assert no 0-sum cycles",len(constraints)
# for t from 2 to |V|
for t in range(2,len(V)+1):

	# for all zero-sum assignments of labels (i.e. t-element vector with elements from A)
	for assignment in product(A,repeat=t):
		s = 0
		for a in assignment: 
			s = group_addition[s,a]

		if s == 0:
			print "assignment",assignment
			# for all cycles of length t...
			for pi in permutations(V,t):
				# one of the edges should have other another label
				constraints.append([-var_label(pi[i-1],pi[i],assignment[i]) for i in range(t)])



print "Total number of constraints:",len(constraints)

WRITE_CNF = 1
if WRITE_CNF:
    fp = "instance.in"

    f = open(fp,"w")
    f.write("p cnf "+str(_num_vars)+" "+str(len(constraints))+"\n")
    for c in constraints:
    	f.write(" ".join(str(v) for v in c)+" 0\n")
    f.close()
    print "Created CNF-file:",fp


ct = 0
found = []
for sol in pycosat.itersolve(constraints):
	ct += 1
	print "sol",ct,":"
	parse_sol(sol)
	break	

if ct == 0:
    print "no solution!?"
else:
    print "total count:",ct



