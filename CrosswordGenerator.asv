
%% This script is meant to automatically create a crossword puzzle in an mxn grid

%{
Inputs: 
- grid size, 
- max # black squares, 
- word bank

Key rules of xword:
- no entry shorter than 3 letters
- theme entries must be longer than other entries
- no repeated words (including words within phrases)
- words must go down and across directions
- no isolated areas
- black squares are symmetrical rotationally

Optional rules
- include all letters of the alphabet
- 30 black squares maximum
- minimum 3 letter words
- avoid regions connected via only one word
- don't cross two "weird" words

1. create grid
2. populate grid with black squares
3. define each word and word crossings
4. fill grid with words


Word bank:
each word: length, frequency used, word score (high score is with weird
letters. divide by word length)


Generate a grid using a word bank:
- create algorithm to walk through picking words

%}

clear all
close all
clc
tic

%% pull words from word bank
% Open the file for reading
% fileID = fopen('Word Bank.txt', 'r');
fileID = fopen('len5.txt', 'r');

% Read the lines from the file
lines = textscan(fileID, '%s', 'Delimiter', '\n');

% Close the file
fclose(fileID);

% Convert each line to separate words and numbers
words_bank = cell(length(lines{1}), 2);
for i = 1:length(lines{1})
    % Split the line by tabs
    line_data = strsplit(lines{1}{i}, ' ');

    % Fill the columns with word and number
    words_bank{i, 1} = line_data{1};
    words_bank{i, 2} = str2double(line_data{2});
end

%% Create array of 3 letter words
% Initialize an empty cell array to store the 3-letter words
threeLet = {};

% Loop through each word in the cell array
for i = 1:size(words_bank, 1)
    tempword = words_bank{i, 1};

    % Check if the word has 3 letters
    if numel(tempword) == 5
        threeLet{end+1,1} = tempword; %#ok<AGROW>
    end
end






%% generate grid
row = 5;
col = 5;

xw = char(zeros(row,col));

for i = 1:row
    for j = 1:col
        xw(i,j) = ' ';
    end
end


% xw(1,1) = '■';







%% populate grid
%look at 1 across and define the best word
% seed = threeLet(1); %best word from word bank

% solveword(xw,1,1)

[xw,didSolve] = solveWord(xw,1,1,threeLet);

toc

%% Functions

function [xw,didSolve] = solveWord(xw, loc, dir,threeLet)
%Input: grid, word location, word direction (1 across, 2 down)
didSolve = 0; %not solved initially


% determine length of word
% XXXXXXXXXXXX

%define word
word = defineWord(xw,loc,dir);


%find first word that fits
for i = 1:length(threeLet)  %loop through words


    testWord = threeLet{i};

    doesMatch = 1;
    for n = 1:5 %loop through letters in word
        if word(n) == ' '
            continue
        elseif testWord(n) ~= word(n)
            doesMatch = 0;
            break
        else
            continue
        end
    end

    if doesMatch == 1 %if a word fits, delete the word from array, call the next word
        didSolve = 1;   %set to 1 now that this step is solved
      
        %update xw
        xwNext = updateXW(xw,loc,dir,testWord);

        %delete word from array
        threeLetNew = threeLet;
        index_to_delete = strcmp(threeLet, testWord);
        threeLetNew(index_to_delete) = [];

        %set new row and direction
        if dir == 1
            dirNew = 2;
            locNew = loc;
        else
            dirNew = 1;
            locNew = loc + 1;
        end
        
        if locNew == 6
            return
        end


        %call function for next word
        [xwNew,didSolve] = solveWord(xwNext,locNew,dirNew,threeLetNew);
       xw
    end


    if didSolve == 1
        xw = xwNew;
        return
    end

end
end

function word = defineWord(xw,loc,dir)
word = char(zeros(1,5));
for i = 1:length(word)
    if dir == 1
        word(i) = xw(loc,i); %across
    else
        word(i) = xw(i,loc); %down
    end
end
end

function xw = updateXW(xw,loc,dir,word)
for i = 1:length(word)
    if dir == 1
        xw(loc,i) = word(i); %across
    else
        xw(i,loc) = word(i); %down
    end
end
end
