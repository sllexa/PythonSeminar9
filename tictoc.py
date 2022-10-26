
field_game = [1,2,3, 4,5,6, 7,8,9]
 
victories = [[0,1,2],
             [3,4,5],
             [6,7,8],
             [0,3,6],
             [1,4,7],
             [2,5,8],
             [0,4,8],
             [2,4,6]]

def print_field():
    str_print = ""
    for i in range(0, len(field_game)):
        if i == 3 or i == 6:
            str_print += "\n"
        str_print += str(field_game[i]) + " "
    return str_print
     
def step_field(step,symbol):
    ind = field_game.index(step)
    field_game[ind] = symbol
 
def get_result():
    win = ""
    for i in victories:
        if field_game[i[0]] == "X" and field_game[i[1]] == "X" and field_game[i[2]] == "X":
            win = "X"
        if field_game[i[0]] == "O" and field_game[i[1]] == "O" and field_game[i[2]] == "O":
            win = "O"   
    return win

def check_line(sum_O,sum_X):
    step = ""
    for line in victories:
        o = 0
        x = 0
        for j in range(0,3):
            if field_game[line[j]] == "O":
                o = o + 1
            if field_game[line[j]] == "X":
                x = x + 1
        if o == sum_O and x == sum_X:
            for j in range(0,3):
                if field_game[line[j]] != "O" and field_game[line[j]] != "X":
                    step = field_game[line[j]]           
    return step
 
def AI():
    step = ""
    step = check_line(2,0)
    if step == "":
        step = check_line(0,2)        
    if step == "":
        step = check_line(1,0)           
    if step == "":
        if field_game[4] != "X" and field_game[4] != "O":
            step = 5           
    if step == "":
        if field_game[0] != "X" and field_game[0] != "O":
            step = 1            
    return step
