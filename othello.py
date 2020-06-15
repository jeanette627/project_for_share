
import turtle


import random


def drawsquare(down_left_x,down_left_y,edage_len): # this function is just for draw every square in checkbox, will be 64 squares in total
    turtle.penup()
    turtle.pensize(10)
    turtle.color('white')
    turtle.speed(9)
    turtle.goto(down_left_x,down_left_y)
    counter=0
    while counter < 4:
        turtle.pendown()
        turtle.forward(edage_len)
        turtle.right(90)
        counter+=1


def squares():
    screen=turtle.Screen()
    screen.bgcolor('green')
    screen.tracer(0)
    turtle.setup(1000,1000)
    turtle.setworldcoordinates(0,-900,900,0)
    w1=turtle.Turtle()  #what I did in line 28-39 is setting a loop to write the column and row number on the margin of the checkbox
    w1.hideturtle()
    for t in range(8):
        w1.penup()
        w1.goto(100+100*t,-30)
        w1.pendown()
        w1.write(t,font=("Arial", 20, "normal"))
    for j in range(8):
        w1.penup()
        w1.goto(20,-(110+100*j))
        w1.pendown()
        w1.write(j,font=("Arial", 20, "normal"))
    x_y_list=[]   # line 40-46 is setting the 64 coordinations where each square starts
    for i in range(8):
        for j in range(8):
            x_y_list+=[(100*i,-(100*j))]
    for coordinate in x_y_list:
        for i in range (8):
            drawsquare(coordinate[0]+50,coordinate[1]-50,100)
            # add 50 and minus 50 means have a blank margin warp the checkbox
    screen.update()


def neighbors(grid,row,col,color):  # find all the coordination for neighbor slots which include oppnent token in it
    opponent_list=[]
    if color==1:
        op_color=2
    elif color==2:
        op_color=1
    j=-1
    i=-1
    while i<2:
        while j <2:
            rowneighbor = row + i
            colneighbor = col + j
            if rowneighbor >=0 and rowneighbor<=7 and colneighbor>=0 and colneighbor<=7: # control the fuction can handle "inGrid" slots and "not inGrid" slots.
                if grid [rowneighbor][colneighbor] == op_color:
                    opponent_list+=[[rowneighbor,colneighbor]]
                else:
                    opponent_list=opponent_list
            j+=1
        j=-1
        i+=1
    return opponent_list


def isValidMove(board,row,col,color):  # one of the required function, if the row ,col argument is satisfied our requirment, namely, do not out of range,we will test whether it's the valid move.
    if  row not in range(0,8) or col not in range(0,8):
        return False
    opponent_list=neighbors(board,row,col,color)
    if opponent_list!=0:
        flip_needed,valid_move=linetype(board,row,col,opponent_list,color)
    else:
        return False
    if board[row][col]!=0 or [row,col] not in valid_move:  #0 is unoccupied;1 is white;2 is black.
        return False
    else:
        return True


def getValidMoves(board,color): #scan every empty slots in the checkbox and return a valid move list for specified color, and the result will return and send to the selectNextPlay function as argument
    valid_list=[]
    for i in range(8):
        for j in range(8):
            if board[i][j]==0:
                if isValidMove(board,i,j,color):
                    valid_list+=[(i,j)]
    return valid_list


def inputconvert(input_row,input_col):  #construct a function that  will convert "row, column" board coordinates to "x, y" turtle coordinates!,mainly used in the showtoken function.
    x_cor=100+100*input_col
    y_cor=-(100+100*input_row)
    return x_cor,y_cor


def showtoken(board): #(keep showing status of checkbox every action done.)
    for i in range(8):
        for j in range(8):
            if board[i][j]==1:
                turtle.penup()
                turtle.goto(inputconvert(i,j))
                turtle.pendown()
                turtle.color('white')
                turtle.dot(100)
            elif board[i][j]==2:
                turtle.penup()
                turtle.goto(inputconvert(i,j))
                turtle.pendown()
                turtle.color('black')
                turtle.dot(100)


def linetype(board,row,col,opponent_list,color): # find what kind of lines starting by an opponent token and we want to continuing search is,
#and while searching each line , if we find the line end by the opponent token(decided by the color argument, and we use the first one we observed) and has exact number of tokens
#matching the olor argument,that is , do not have empty slot betwwen two opponent token we found. meanwhile, i record the matching token between and if the line we searched is word,
#the record will be the token that need change their color, that is , need be flipped.
    if color==1:
        op_color=2
    elif color==2:
        op_color=1
    find=False
    valid_move=[]
    flip_needed=[]
    for coordination in opponent_list:
        matching_found= False
        if row == coordination[0] and col<coordination[1]:
            type="horizontally_right"
            matching_found= False
            y_r=col+1
            test=[]
            while not matching_found and y_r <8:
                if board[row][y_r]== op_color:
                    test+=[[row,y_r]]
                elif board[row][y_r]== color and len(test)== y_r-(col+1):
                    matching_found=True
                    flip_needed+=test
                    valid_move+=[[row,col]]
                else:
                    test=[]
                y_r+=1
        if row == coordination[0] and col>coordination[1]:
            type="horizontally_left"
            y_l=col-1
            test=[]
            while not matching_found and y_l >=0:
                if board[row][y_l]== op_color:
                    test+=[[row,y_l]]
                elif board[row][y_l]== color and len(test)== (col-1)-y_l:
                    matching_found=True
                    flip_needed+=test
                    valid_move+=[[row,col]]
                else:
                    test=[]
                y_l-=1
        if col == coordination[1] and row<coordination[0]:
            type="vertically_down"
            x_d=row+1
            test=[]
            while not matching_found and x_d <8:
                if board[x_d][col]== op_color:
                    test+=[[x_d,col]]
                elif board[x_d][col]== color and len(test)== (x_d-1)-row:
                    matching_found=True
                    flip_needed+=test
                    valid_move+=[[row,col]]
                else:
                    test=[]
                x_d+=1
        if col == coordination[1] and row>coordination[0]:
            type="vertically_up"
            x_u=row-1
            test=[]
            while not matching_found and x_u >=0:
                if board[x_u][col]== op_color:
                    test+=[[x_u,col]]
                elif board[x_u][col]== color and len(test)== row-(x_u+1):
                    matching_found=True
                    flip_needed+=test
                    valid_move+=[[row,col]]
                else:
                    test=[]
                x_u-=1
        elif abs(row-coordination[0])== 1 and abs(col-coordination[1])==1:
            if row-coordination[0]==1 and col-coordination[1]==1:
                type="diagonally_upperleft"
                x_ul=coordination[0]
                y_ul=coordination[1]
                test=[]
                while x_ul>=0 and y_ul >=0 and not matching_found:
                    if board[x_ul][y_ul] == op_color:
                        test+=[[x_ul,y_ul]]
                    elif board[x_ul][y_ul] == color and len(test)== row-(x_ul+1):
                        matching_found=True
                        flip_needed+=test
                        valid_move+=[[row,col]]
                    else:
                        test=[]
                    x_ul-=1
                    y_ul-=1

            if row-coordination[0]==-1 and col-coordination[1]==-1:
                type="diagonally_downright"
                x_dr=coordination[0]
                y_dr=coordination[1]
                test=[]
                while x_dr<8 and y_dr <8 and not matching_found:
                    if board[x_dr][y_dr] == op_color:
                            test+=[[x_dr,y_dr]]
                    elif board[x_dr][y_dr] == color and len(test)==x_dr-(row+1):
                        matching_found=True
                        flip_needed+=test
                        valid_move+=[[row,col]]
                    x_dr+=1
                    y_dr+=1
            if row-coordination[0]==1 and col-coordination[1]==-1:
                type="diagonally_upperright"
                x_ur=coordination[0]
                y_ur=coordination[1]
                test=[]
                while x_ur>=0 and y_ur<8 and not matching_found:
                    if board[x_ur][y_ur] == op_color:
                        test+=[[x_ur,y_ur]]
                    elif board[x_ur][y_ur]==color and len(test)==row-(x_ur+1):
                        matching_found=True
                        flip_needed+=test
                        valid_move+=[[row,col]]
                    else:
                        test=[]
                    x_ur-=1
                    y_ur+=1
            if row-coordination[0]==-1 and col-coordination[1]==1:
                type="diagonally_downleft"
                x_dl=coordination[0]
                y_dl=coordination[1]
                test=[]
                while x_dl<8 and y_dl >=0 and not matching_found:
                    if board[x_dl][y_dl] == op_color:
                        test+=[[x_dl,y_dl]]
                    elif board[x_dl][y_dl]==color and len(test)==x_dl-(row+1):
                        matching_found=True
                        flip_needed+=test
                        valid_move+=[[row,col]]
                    else:
                        test=[]
                    x_dl+=1
                    y_dl-=1
    return flip_needed,valid_move


def selectNextPlay(board): # function build for computer player to find a random slot among the valid slots
    valid_list=getValidMoves(board,1)
    if len(valid_list)!=0:
        p=random.randint(0,len(valid_list)-1)
        board[valid_list[p][0]][valid_list[p][1]]=1
        flip_needed,valid_move=linetype(board,valid_list[p][0],valid_list[p][1],neighbors(board,valid_list[p][0],valid_list[p][1],1),1)
        for j in flip_needed:
            board[j[0]][j[1]]=1
    return board


def main(): #main fun has a loop which i set for control the status of game(operational or stopped)
    squares()
    token=[]
    for i in range(8):
        token+=[[0,0,0,0,0,0,0,0]]
    token[3][3]=1
    token[3][4]=2
    token[4][3]=2
    token[4][4]=1
    showtoken(token)
    done=False
    while not done:
        valid_list_black=getValidMoves(token,2)
        if len(valid_list_black)==0:
            valid_list_white=getValidMoves(token,1)
            if len(valid_list_white)!=0:
                u=selectNextPlay(token)
                showtoken(u)
            else:
                done=True
                white=0
                black=0
                for row in token:
                    white+=str(row).count('1')
                    black+=str(row).count('2')
                turtle.penup()
                turtle.goto(100,-450)
                turtle.pendown()
                turtle.color('red')
                if white>black:
                    turtle.write("you lose! white token is:"+str(white)+"black token is:"+str(black),font=("Arial", 20, "normal")) #show the result in terminal
                elif white<black:
                    turtle.write("you win! white token is:"+str(white)+"black token is:"+str(black),font=("Arial", 20, "normal"))
                elif white==black:
                    turtle.write("tie! white token is:"+str(white)+"black token is:"+str(black),font=("Arial", 20, "normal"))
        elif len(valid_list_black)!=0:
            t=turtle.textinput('enter',"Enter row,col")
            if t=='':
                done=True
                turtle.bye()
            else:
                user_done=False
                while not user_done:
                    if isValidMove(token,int(t[0]),int(t[2]),2):
                        token[int(t[0])][int(t[2])]=2
                        flip_needed,valid_move=linetype(token,int(t[0]),int(t[2]),neighbors(token,int(t[0]),int(t[2]),2),2)
                        for cor in flip_needed:
                            token[cor[0]][cor[1]]=2
                        showtoken(token)
                        user_done=True
                    else:
                        t=turtle.textinput("enter1",t+"is not a valid move"+" reenter row,col")
                valid_list_white=getValidMoves(token,2)
                if len(valid_list_white)!=0:
                    v=selectNextPlay(token)
                    showtoken(v)


if __name__ == '__main__':
    main()
