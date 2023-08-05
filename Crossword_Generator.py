
from solve_xword import solve_phase
from copy import copy, deepcopy
from word_list import make_word_list
import os

# Pull words from the word bank

folder_path = r"C:\Users\psatt\Desktop\Fun Projects\Crossword Generator\compileWords\CompiledWords"


wordDataBase = []
for i in range(3,22):
    file_name =  f"len{i}.txt"
    file_path = os.path.join(folder_path,file_name)
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()


    onelengthwords = []
    for line in lines:
        line_data = line.split()
        onelengthwords.append([line_data[0], int(line_data[1])])

    wordDataBase.append(onelengthwords)


# Convert each line to separate words and numbers


'''xw =    [' ', ' ', ' ',],\
        [' ', ' ', ' ',],\
        [' ', ' ', ' ',]
        '''
xw =    [' ', ' ', ' ', ' ', '■', ' ',' ', ' ', ' ', '■', '■', ' ', ' ', ' ', ' '],\
        [' ', ' ', ' ', ' ', '■', ' ',' ', ' ', ' ', '■', ' ', ' ', ' ', ' ', ' '],\
        [' ', ' ', ' ', ' ', '■', ' ',' ', ' ', ' ', '■', ' ', ' ', ' ', ' ', ' '],\
        [' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' ', ' ', ' ', ' ', '■', '■'],\
        ['■', '■', '■', ' ', ' ', ' ','■', '■', ' ', ' ', ' ', ' ', '■', '■', '■'],\
        ['■', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
        [' ', ' ', ' ', '■', ' ', ' ',' ', ' ', '■', '■', ' ', ' ', ' ', ' ', ' '],\
        [' ', ' ', ' ', ' ', '■', ' ',' ', ' ', ' ', ' ', '■', ' ', ' ', ' ', ' '],\
        [' ', ' ', ' ', ' ', ' ', '■','■', ' ', ' ', ' ', ' ', '■', ' ', ' ', ' '],\
        [' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '■'],\
        ['■', '■', '■', ' ', ' ', ' ',' ', '■', '■', ' ', ' ', ' ', '■', '■', '■'],\
        ['■', '■', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
        [' ', ' ', ' ', ' ', ' ', '■',' ', ' ', ' ', ' ', '■', ' ', ' ', ' ', ' '],\
        [' ', ' ', ' ', ' ', ' ', '■',' ', ' ', ' ', ' ', '■', ' ', ' ', ' ', ' '],\
        [' ', ' ', ' ', ' ', '■', '■',' ', ' ', ' ', ' ', '■', ' ', ' ', ' ', ' ']


#define list of words and order to go through them
wordsInPuzzle = []
wordList = make_word_list(xw)


# Call the function to solve the crossword
xw, did_solve = solve_phase(xw,wordDataBase, wordList,wordsInPuzzle)






# Print the crossword
print(did_solve)
for row in xw:
    print(row)
    #print(' '.join(row))
