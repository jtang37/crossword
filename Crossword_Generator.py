
from solve_xword import solve_phase
from copy import copy, deepcopy
from word_list import make_word_list


# Pull words from the word bank
with open('len5.txt', 'r') as file:
    lines = file.readlines()

# Convert each line to separate words and numbers
five_let = []
for line in lines:
    line_data = line.split()
    five_let.append([line_data[0], int(line_data[1])])
size = 5
# Generate the grid
row, col = size, size
xw = [[' ' for _ in range(col)] for _ in range(row)]
#xw[0][0] = 'Q'

xw =    ['■', ' ', ' ', ' ', ' ', ' '],\
        ['■', ' ', ' ', ' ', ' ', ' '],\
        ['■', ' ', ' ', ' ', ' ', ' '],\
        ['■', ' ', ' ', ' ', ' ', ' '],\
        ['■', ' ', ' ', ' ', ' ', ' ']


#define list of words and order to go through them
wordList = make_word_list(xw)


# Call the function to solve the crossword
xw, did_solve = solve_phase(xw,five_let, wordList)






# Print the crossword
print(did_solve)
for row in xw:
    print(row)
    #print(' '.join(row))
