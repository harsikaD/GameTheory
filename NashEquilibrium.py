
M = [[[3, 1], [2, 3], [10, 2]],
     [[4, 5], [3, 0], [6, 4]],
     [[2, 2], [5, 4], [12, 3]],
     [[5, 6], [4, 5], [9, 7]]]
N = [[[3,2], [0,0]],
     [[0,0], [2,3]]]
L = [[0,0],
     [0,0]]

Label = [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]

for row in range(4):
    for col in range(3):
        # check row payoffs
        for r in range(4):
            if Label[row][col] == 0:
                if M[r][col][0] > M[row][col][0]:
                    # this is not a Nash Equilibrium
                    Label[row][col] = 2

        if Label[row][col] == 0:
            for c in range(3):
                if Label[row][col] == 0:
                    if M[row][c][1] > M[row][col][1]:
                        # not a Nash eq.
                        Label[row][col] = 2


        if Label[row][col] == 0:
            Label[row][col] = 1
for the_row in range(4):
    for the_col in range(3):
        if Label[the_row][the_col] == 1:
            print(M[the_row][the_col])
