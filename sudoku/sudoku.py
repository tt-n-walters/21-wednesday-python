import time
import os

def display_puzzle():
    buffer = ""
    for j in range(len(puzzle)):
        row = puzzle[j]
        if j % 3 == 0:
            buffer += " +-------+-------+-------+\n"
        for i in range(len(row)):
            number = row[i]
            if i % 3 == 0:
                buffer += " |"
            buffer += " "
            if number > 0:
                buffer += str(number)
            else:
                buffer += " "
        buffer += " |\n"
    buffer += " +-------+-------+-------+\n"
    # os.system("cls")
    print(buffer)

tries = 0
# a heuristic backtracking recursion based solving algorithm
def solve_puzzle():
    global tries
    tries += 1
    display_puzzle()
    # loop through every row and column
    for row in range(9):
        for col in range(9):
            number = puzzle[row][col]
            if number == 0:
                # check every possible value
                for n in range(1, 10):
                    if check_position(row, col, n):
                        puzzle[row][col] = n
                        solve_puzzle()

                # un-doing the mistake
                puzzle[row][col] = 0
                return

    display_puzzle()
    print(tries)
    exit()

def check_position(row, column, number):
    # check the row
    if number in puzzle[row]:
        return False
    
    # check the column
    for row_list in puzzle:
        if number == row_list[column]:
            return False

    # check the section
    section_x = column // 3
    section_y = row // 3
    for row in puzzle[section_y*3 : section_y*3 + 3]:
        if number in row[section_x*3 : section_x*3 + 3]:
            return False
    
    return True

file = open("sudoku/puzzles.txt", "r")
puzzle_strings = file.read().splitlines()
file.close()

puzzle_string = puzzle_strings[0]

puzzle = []

# split string into 9 equally sized pieces
for i in range(9):
    start_index = i * 9
    end_index = i * 9 + 9
    row = puzzle_string[start_index : end_index]
    puzzle.append(row)


# split each piece into 9 numbers
for j in range(9):
    row_string = puzzle[j]

    row = []
    for i in range(9):
        number = int(row_string[i])
        row.append(number)

    puzzle[j] = row

print(puzzle)
display_puzzle()
solve_puzzle()
