import sys
from copy import deepcopy


f = open("cfg.txt", "r")
Lines = f.readlines()

successors = {}

# put into array
for line in Lines:
    x = line.split(" => ")

    x[1] = x[1].replace('\n','')

    temp = []
    for y in x[1]:
        if y != " ":
            temp.append(int(y))

    successors[int(x[0])] = temp

predecessors = deepcopy(successors)
for k in predecessors.keys():
   predecessors[k] = []

# get predecessors
for k,v in successors.items():
    for y in v:
       predecessors.setdefault(y, []).append(k) 

# dominators
dominators = {}
dominators = deepcopy(predecessors)
for k in dominators.keys():
   dominators[k] = []

dominators.setdefault(0, []).append(0)
for m in predecessors.keys():
    if m != 0:
        for z in predecessors.keys():
            dominators.setdefault(m, []).append(z)

temp = {}
while temp != dominators:
    temp = deepcopy(dominators)
    for m in predecessors.keys():
       if m != 0: 
           temp_list = []
           for x in predecessors[m]:
               temp_list.append(dominators[x])
           if temp_list:
               temp_list_dom = temp_list[0]
               for z in range(0,len(temp_list)-1):
                   temp_list_dom = list(set(temp_list[z]) & set(temp_list[z+1]))
               dominators[m] = []
               for z in temp_list_dom:
                   dominators.setdefault(m, []).append(z) 
           dominators[m] = list(set().union(dominators[m],[m]))

for k,v in dominators.items():
    v.remove(k)
    if not predecessors[k]:
        v.clear()

p = open("dom.txt", "w")
for k,v in sorted(dominators.items()):
    p.write("DOM(" + str(k) + ') = ')
    for x in v:
        p.write(str(x) + ' ')
    p.write("\n")

# dominator tree now
dominator_tree = deepcopy(dominators)
temp_dict = {}
for k,v in dominators.items():
    if len(v) != 0:
        temp_list = sorted(v)
        temp_dict[k] = temp_list[len(v)-1]

for k in dominator_tree.keys():
    dominator_tree[k] = []

for k,v in temp_dict.items():
    dominator_tree.setdefault(v, []).append(k)

p = open("dtree.txt", "w")
for k,v in sorted(dominator_tree.items()):
    if v:
        p.write(str(k) + ' => ')
        for x in v:
            p.write(str(x) + ' ')
        p.write("\n")