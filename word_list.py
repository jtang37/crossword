# functino to make a list of words (x,y,direction,length) from a grid
from copy import copy, deepcopy

def make_word_list(grid):
    wordslist = []
    word = []
    for row in range(len(grid)):    #loop through rows
        for col in range(len(grid[0])):    #loop through cols
            #go through each cell
            #if "■" go next
            #else check across
                #is there a non black square before it
                #loop through to find where the next black square is
        
            if grid[row][col] == '■':   #no word if square is black
                continue

            #define across word
            if col == 0 or grid[row][col-1] == '■':
                direc = 1
                length = 1
                
                while col+length < len(grid[0]) and grid[row][col+length] != '■':
                    length = length + 1
                    
                word = [row,col,direc,length]
                wordslist = wordslist + [word]

            #define down word
            if row == 0 or grid[row-1][col] == '■':
                direc = 2
                length = 1
                
                while row+length < len(grid) and grid[row+length][col] != '■':
                    length = length + 1
                    
                word = [row,col,direc,length]
                wordslist = wordslist + [word]


    downacross = 2
    wordlistOrdered = deepcopy(wordslist)
    
    for i in range(len(wordlistOrdered)):
        
        if downacross == 1:
            downacross = 2
        else:
            downacross = 1
        
        for j in range(len(wordslist)):
            if wordslist[j][2] == downacross:
                wordlistOrdered[i] = deepcopy(wordslist[j])
                wordslist[j][2] = 0
                break
        
    return wordlistOrdered
