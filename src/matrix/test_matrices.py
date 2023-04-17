import sys
from create_matrices import *
import matrix_vx
import matrix_wx
import matrix_wxi

sequence = "GAGUGACAGAUAUUGUAACUACACUCUCAGU"

#sys.setrecursionlimit(19000)
matrix = create_matrices(len(sequence))
fill_matrices(matrix)

for j in range(len(sequence)):
    print("j =", j)
    for i in range(j+1):
        print("i = ", i)
        matrix_vx.matrix_vx(i, j, matrix, sequence)
        matrix_wx.matrix_wx(i, j, matrix, sequence)
        matrix_wxi.matrix_wxi(i, j, matrix, sequence)

print("## VX ##")
for line in matrix["vx"]: print([round(x, 2) for x in line])
# print("\n## WX ##")
# for line in matrix["wx"]: print(line)
# print("\n## WXi ##")
# for line in matrix["wxi"]: print(line)
# print("\n## Whx ##")
# for line in matrix["whx"]: print(line)
# print("\n## vhx ##")
# for line in matrix["vhx"]: print(line)
# print("\n## yhx ##")
# for line in matrix["yhx"]: print(line)
# print("\n## zhx ##")
# for line in matrix["zhx"]: print(line)

