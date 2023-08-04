# Function to solve the crossword

from copy import copy, deepcopy
from word_list import make_word_list

def solve_phase(xw, five_let, wordList):
    #set word parameters

    wordSlot = wordList[0]
    wordListNew = deepcopy(wordList)
    del wordListNew[0]


    # Input: grid, word location, word direction (1 across, 2 down)
    did_solve = False  # not solved initially
    
    # Determine the length of the word
    wordCompare = define_word(xw, wordSlot)  
    

    
    
    
    # Find the first word that fits
    for i in range(len(five_let)):  # loop through words
        test_word = five_let[i]
        
        
        does_match = does_it_match(test_word[0], wordCompare)

        if does_match:  # if a word fits, delete the word from array, call the next word
            did_solve = True  # set to True now that this step is solved
            
            # update xw
            xw_next = deepcopy(xw)
            xw_next = update_xw(xw_next, wordSlot, test_word[0])
            
            # delete word from array
            #five_let_new = copy(five_let)
            five_let_new = five_let[:i] + five_let[i + 1:]      #takes up a lot of memory
            

            # set new word
            
            
            

            if len(wordListNew) == 0:
                return xw_next, True
            
            # call function for the next word
            xw_new = deepcopy(xw_next)
            xw_new, did_solve = solve_phase(xw_next, five_let_new, wordListNew)
            
            
            if did_solve:
                return xw_new, True


    
    return xw, False


# Function to define a word
def define_word(xw, wordSlot):
    #wordSlot is [row,col,direction,length]
    length = wordSlot[3]
    row = wordSlot[0]
    col = wordSlot[1]
    direc = wordSlot[2]
    wordFrame = [' '] * length
    for i in range(length):
        if direc == 1:
            wordFrame[i] = xw[row][col+i]  # across
        else:
            wordFrame[i] = xw[row+i][col]  # down
            
    return wordFrame


# Function to update the crossword grid
def update_xw(xw_next, wordSlot, wordInput):
    length = wordSlot[3]
    row = wordSlot[0]
    col = wordSlot[1]
    direc = wordSlot[2]
    for i in range(length):
        if direc == 1:
            xw_next[row][col+i] = wordInput[i]  # across
        else:
            xw_next[row+i][col] = wordInput[i]  # down\
    return xw_next



def does_it_match(test_word, wordCompare):
    for n in range(len(test_word)):  # loop through letters in word
        if wordCompare[n] == ' ':
            continue
        elif test_word[n] != wordCompare[n]:
            return False
        else:
            continue
    return True
