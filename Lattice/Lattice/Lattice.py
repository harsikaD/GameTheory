import numpy as np
import random


# lattice class, every cell in ractangular array has 8 neighbours
class Lattice(object):
    # randomly intialising the required values
    array = np.arange(20)
    no_of_cols = -1
    no_of_rows = -1

    # ====================================================================================================
    # Constructor, takes the required data and intialises a lattice(basically an array) where each data element
    # is filled uniformly randomly
    # PARAMS:
    #       no_of_rows, no_of_cols : dimensions of the lattice
    #       file_name : file where the scores are written, a sample file is already provided
    # RETURN:
    #       void
    # ====================================================================================================
    def __init__(self, no_of_rows, no_of_cols, file_name):
        # computes the total no of scores and intialises a linear array for this size
        no_of_cells = no_of_rows*no_of_cols

        # fill each cell with -16, later we will see this as a condition of emptyness
        array = np.full(no_of_cells, -16.0)
        self.no_of_cols = no_of_cols
        self.no_of_rows = no_of_rows

        # loads scores from the file
        scores =np.loadtxt(file_name, delimiter = ',')

        # assert the logical things
        assert len(scores) == no_of_cells , 'len(scores) != no_of_cells, kindly correct data and pass again'

        # each score has to go in some uniformly randomly selected cell,
        for score in scores:

            # wait for an empty cell to be generated
            cell_value = -1
            cell = -1
            while cell_value != -16:
                cell = random.randint(0, no_of_cells -1 )
                cell_value = array[cell]

            # once generated, fill with the considered score
            array[cell] = score

        # reshape this array as was required by the lattice inputs
        self.array = array.reshape(no_of_rows, no_of_cols)

    # ====================================================================================================
    # function to get nieghbours scores as list, to find the right threshold there
    # PARAMS:
    #       row_idx, col_idx : cell coordinates for which neighbours scores has to be found out
    # RETURN:
    #       list of neighbours scores
    # ====================================================================================================
    def get_neighbours_scores(self, row_idx, col_idx):
        # assert if it is right cell or not
        assert row_idx < self.no_of_rows and col_idx < self.no_of_cols, "wrong row_idx or col_idx passed"

        # neighbours scores will be collected in this list
        neighbours_scores = []

        # given this cell, go step forward and backward horizontally
        for row_diff in [-1,0,1 ]:
            neighbour_row_idx = row_idx + row_diff

            # if the cell is at the extreme position
            if neighbour_row_idx < 0:
                neighbour_row_idx = self.no_of_rows + neighbour_row_idx

            if neighbour_row_idx == self.no_of_rows:
                neighbour_row_idx = 0

            # go one step backward and forward vertically
            for col_diff in [-1,0,1]:
                if col_diff == 0 and row_diff ==0:
                    continue

                neighbour_col_idx = col_idx + col_diff

                # if the cell is at extreme position
                if neighbour_col_idx < 0:
                    neighbour_col_idx = self.no_of_cols + neighbour_col_idx

                if neighbour_col_idx == self.no_of_cols:
                    neighbour_col_idx = 0

                # fill the score
                neighbours_scores.append( self.array[neighbour_row_idx, neighbour_col_idx])
        # return the required list
        return neighbours_scores

# Testing code
'''
l = Lattice(3,4,'Sample_test.txt')
print(l.array)
neighbours = l.get_neighbours_scores(2,1)
print(neighbours)
print(0)
'''






