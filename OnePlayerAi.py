from tkinter import N, NE
import numpy as np
from TetrisBattle.settings import *
from TetrisBattle.envs.tetris_env import TetrisSingleEnv
from TetrisBattle.tetris import Tetris, Player, Judge, get_infos, freeze, Buffer

# A function that assigne a score to the passed board


def score1(board):
    hights = np.empty(10)
    hights, std1 = m_d_hight(board)
    NumHoles, clear1 = n_holes(board)

    return 0.82*(NumHoles) + -.48*std1 + 0.8*(hights.max() - hights.min()) + -0.7*clear1

# checks what rows would be cleard from the passed board then returns them as well as an assigned score on them based on if there is a tetris (4-rows) or not 


def clearr(board):
    lines = []
    line = 0
    for i in range(20):
        full = True
        for j in range(10):
            if int(board[i][j]) == 0:
                full = False
                break
        if full:
            line += 1
            lines.append(j)
    if line >= 4:
        return int(((line % 4) + (line//4 ** 4))), lines ## returns the score, the lines array
    return int(line), lines

# a function that counts the number of holes in the board


def n_holes(board):
    # get the lines that would be cleard in this board
    sc, lines = clearr(board)
    holes = 0
    for i in range(10):
        occupied = 0  # Set the 'Occupied' flag to 0 for each new column
        for j in range(20):  # Scan from top to bottom
            if int(board[j][i]) == 1 and not (j in lines):
                occupied = 1  # If a block is found, set the 'Occupied' flag to 1
            if int(board[j][i]) == 0 and occupied == 1:

                holes += 1  # If a hole is found, add one to the count
    return holes, sc

# The hight function that checks the current hights of the passed board and returns an array of the hights and the Standard deviation of list


def m_d_hight(board):
    hights = np.empty(10)
    for i in range(10):
        for j in range(20):  # Scan from top to bottom
            if int(board[j][i]) == 1:

                hights[i] = (int(20-j)+1)
                break
            if j == 19:
                hights[i] = (int(20-j))
    return hights, hights.std()



# A function that takes the current grid, the pieces list, and the current depth in the evaluating tree
# as it stop at depth when the depth 1. it returns a sorted array with all the possible moves and 
# their scores 
def CreatAllMovesD2 (grid, Pl, NextIndex):
    piecer = Pl [NextIndex]
    hights, std1 =  m_d_hight(grid)
    steps = [] 

    if piecer == 'I':
        for i in range (2):
            if i == 0:
                for j in range (10):
                    gridc = grid.copy()
                    ss=[4]
                    if (j-5)<0:
                        for asd in range(5-j):
                            ss.append(6)
                    else:
                        for asd in range(j-5):
                            ss.append(5)
                    for z in range(4):
                        if (z+1 + hights[j] >19):
                            break
                        gridc[int(20-(hights[j]+z))][int(j)]=1
                    if NextIndex == 1:
                        steps.append([score1(gridc), ss])
                    else : 
                        steps.append([score1(gridc)+ 0.787* CreatAllMovesD2(gridc, Pl, NextIndex+1)[0][0], ss])

            else:
                for j in range (7):
                    gridc = grid.copy()
                    ss=[]
                    if (j-4)<0:
                        for asd in range(4-j):
                            ss.append(6)
                    else:
                        for asd in range(j-4):
                            ss.append(5)
                    for z in range(4):
                        gridc[20-int(max(hights[0+j:4+j]))][int(z)]=1                           
                    if NextIndex == 1:
                        steps.append([score1(gridc), ss])
                    else : 
                        steps.append([score1(gridc)+ 0.787* CreatAllMovesD2(gridc, Pl, NextIndex+1)[0][0], ss])

    if piecer == 'O':
        for j in range (8):
            ss=[]
            gridc = grid.copy()
            if (j-5)<0:
                for asd in range(5-j):
                    ss.append(6)
            else:
                for asd in range (j-5):
                    ss.append(5)
            gridc[20- int(max(hights[0+j:2+j]))][j]=1
            gridc[20- int(max(hights[0+j:2+j]))][j+1]=1
            gridc[20- int(max(hights[0+j:2+j]) +1)][j]=1
            gridc[20- int(max(hights[0+j:2+j])+1)][j+1]=1
            if NextIndex == 1:
                steps.append([score1(gridc), ss])
            else : 
                steps.append([score1(gridc)+ 0.787* CreatAllMovesD2(gridc, Pl, NextIndex+1)[0][0], ss])

    if piecer == 'L':
        for i in range (4):
            if i == 0:
                for j in range (8):
                    gridc= grid.copy()
                    ss = []
                    if (j-4)<0:
                        for asd in range (4-j):
                            ss.append(6)
                    if (j-4)>0:
                        for asd in range (j-4):
                            ss.append(5)
                    if gridc[20- int(max(hights[0+j:3+j]))][j]!= 1 and gridc[20- int(max(hights[0+j:3+j]))][j+1]!=1 and gridc[20- int(max(hights[0+j:3+j]))][j+2] !=1 and gridc[20- int(max(hights[0+j:3+j]+1))][j+2] !=1 :                    
                        gridc[20- int(max(hights[0+j:3+j]))][j]=1
                        gridc[20- int(max(hights[0+j:3+j]))][j+1]=1
                        gridc[20- int(max(hights[0+j:3+j]))][j+2]=1
                        gridc[20- int(max(hights[0+j:3+j])+1)][j+2]=1

                        if NextIndex == 1:
                            steps.append([score1(gridc), ss])
                        else : 
                            steps.append([score1(gridc)+ 0.787* CreatAllMovesD2(gridc, Pl, NextIndex+1)[0][0], ss])


            if i == 1:
                for j in range (9):
                    gridc= grid.copy()
                    ss = [4]
                    if (j-4)<0:
                        for asd in range (4-j):
                            ss.append(6)
                    if (j-4)>0:
                        for asd in range (j-4):
                            ss.append(5)
                    hm = int(max([hights[0+j], 3, hights[1+j]+2 ]))

                    if hights[1+j]<= (hm-2) and gridc[(20 - hm)][j]!= 1 and gridc[(20- hm)][j+1] !=1 and gridc[(20- hm+1)][j+1] !=1 and gridc[(20- hm+2)][j+1]!=1:                    
                        gridc[20- hm][j]=1
                        gridc[20- hm][j+1]=1
                        gridc[20- hm+1][j+1]=1
                        gridc[20- hm+2][j+1]=1
 
                        if NextIndex == 1:
                            steps.append([score1(gridc), ss])
                        else : 
                            steps.append([score1(gridc)+ 0.787* CreatAllMovesD2(gridc, Pl, NextIndex+1)[0][0], ss])


            if i ==2:
                for j in range (8):
                    gridc= grid.copy()
                    ss = [4,4]
                    if (j-4)<0:
                        for asd in range (4-j):
                            ss.append(6)
                    if (j-4)>0:
                        for asd in range (j-4):
                            ss.append(5)
                    hm = int(max(hights[0+j:3+j]))
                    if hm != hights[0+j] and (hm == hights[1+j] or hm == hights [2+j]):
                        hm -=1
                    if gridc[20- int(max(hights[0+j:3+j]))][j]!= 1 and gridc[20- int(max(hights[0+j:3+j]))-1][j+1]!=1 and gridc[20- int(max(hights[0+j:3+j]))-1][j+2] !=1 and gridc[20- int(max(hights[0+j:3+j])+1)][j] !=1 :                    
                        gridc[20- int(max(hights[0+j:3+j]))][j]=1
                        gridc[20- int(max(hights[0+j:3+j])+1)][j+1]=1
                        gridc[20- int(max(hights[0+j:3+j])+1)][j+2]=1
                        gridc[20- int(max(hights[0+j:3+j])+1)][j]=1

                        if NextIndex == 1:
                            steps.append([score1(gridc), ss])
                        else : 
                            steps.append([score1(gridc)+ 0.787* CreatAllMovesD2(gridc, Pl, NextIndex+1)[0][0], ss])


            if i ==3:
                for j in range(9):
                    gridc= grid.copy()
                    ss=[3]
                    if (j-5<0):
                        for asd in range (5-j):
                            ss.append(6)
                    if (j-5>0):
                        for asd in range (j-5):
                            ss.append(5)
                    if gridc[20- int(max(hights[0+j:2+j]))][j]!= 1 and gridc[20- int(max(hights[0+j:2+j]))][j+1]!=1 and gridc[20- int(max(hights[0+j:2+j])) -1][j] !=1 and gridc[20- int(max(hights[0+j:2+j])+2)][j] !=1 :
                        gridc[20- int(max(hights[0+j:2+j]))][j]= 1 
                        gridc[20- int(max(hights[0+j:2+j]))][j+1]=1 
                        gridc[20- int(max(hights[0+j:2+j])) -1][j] =1
                        gridc[20- int(max(hights[0+j:2+j])+2)][j] =1

                        if NextIndex == 1:
                            steps.append([score1(gridc), ss])
                        else : 
                            steps.append([score1(gridc)+ 0.787* CreatAllMovesD2(gridc, Pl, NextIndex+1)[0][0], ss])

    if piecer == 'J':
        for i in range (4):
            if i == 0:
                for j in range (8):
                    gridc= grid.copy()
                    ss = []
                    if (j-4)<0:
                        for asd in range (4-j):
                            ss.append(6)
                    if (j-4)>0:
                        for asd in range (j-4):
                            ss.append(5)
                    if gridc[20- int(max(hights[0+j:3+j]))][j]!= 1 and gridc[20- int(max(hights[0+j:3+j]))][j+1]!=1 and gridc[20- int(max(hights[0+j:3+j]))][j+2] !=1 and gridc[20- int(max(hights[0+j:3+j]+1))][j] !=1 :                    
                        gridc[20- int(max(hights[0+j:3+j]))][j]=1
                        gridc[20- int(max(hights[0+j:3+j]))][j+1]=1
                        gridc[20- int(max(hights[0+j:3+j]))][j+2]=1
                        gridc[20- int(max(hights[0+j:3+j])+1)][j]=1

                        if NextIndex == 1:
                            steps.append([score1(gridc), ss])
                        else : 
                            steps.append([score1(gridc)+ 0.787* CreatAllMovesD2(gridc, Pl, NextIndex+1)[0][0], ss])

            if i == 1:
                for j in range (9):
                    gridc= grid.copy()
                    ss = [3]
                    if (j-5)<0:
                        for asd in range (5-j):
                            ss.append(6)
                    if (j-5)>0:
                        for asd in range (j-5):
                            ss.append(5)
                    
                    hm = int( max (hights[0+j], hights[1+j] -2))

                    if gridc[(20 - hm)][j]!= 1 and gridc[(20- hm-1)][j] !=1 and gridc[(20- hm-2)][j] !=1 and gridc[(20- hm-2)][j+1]!=1 and (hm+2) >= hights[j+1]:                    
                        gridc[20- hm][j]=1
                        gridc[20- hm-1][j]=1
                        gridc[20- hm-2][j]=1
                        gridc[20- hm-2][j+1]=1

                        if NextIndex == 1:
                            steps.append([score1(gridc), ss])
                        else : 
                            steps.append([score1(gridc)+ 0.787* CreatAllMovesD2(gridc, Pl, NextIndex+1)[0][0], ss])

            if i ==2:
                for j in range (8):
                    gridc= grid.copy()
                    ss = [4,4]
                    if (j-4)<0:
                        for asd in range (4-j):
                            ss.append(6)
                    if (j-4)>0:
                        for asd in range (j-4):
                            ss.append(5)
                    hm = int(max(hights[0+j:3+j]))
                    if hm != hights[2+j] and (hm == hights[1+j] or hm == hights [0+j]):
                        hm -=1
                    if gridc[20- hm][j+2]!= 1 and gridc[20- hm-1][j+1]!=1 and gridc[20- hm-1][j+2] !=1 and gridc[20- hm-1][j] !=1 :                    
                        gridc[20- hm][+2]=1
                        gridc[20- hm-1][j+1]=1
                        gridc[20- hm-1][j+2]=1
                        gridc[20- hm-1][j]=1

                        if NextIndex == 1:
                            steps.append([score1(gridc), ss])
                        else : 
                            steps.append([score1(gridc)+ 0.787* CreatAllMovesD2(gridc, Pl, NextIndex+1)[0][0], ss])

            if i ==3:
                for j in range(9):
                    gridc= grid.copy()
                    ss=[4]
                    if (j-4<0):
                        for asd in range (4-j):
                            ss.append(6)
                    if (j-4>0):
                        for asd in range (j-4):
                            ss.append(5)
                    hm = int(max (hights[0+j:2+j]))
                    if gridc[20- hm][j]!= 1 and gridc[20- hm][j+1]!=1 and gridc[20- hm -1 ][j+1] !=1 and gridc[20- hm -2][j+1] !=1 :
                        gridc[20- hm][j]= 1 
                        gridc[20- hm][j+1]=1 
                        gridc[20- hm -1][j+1] =1
                        gridc[20- hm -2][j+1] =1

                        if NextIndex == 1:
                            steps.append([score1(gridc), ss])
                        else : 
                            steps.append([score1(gridc)+ 0.787* CreatAllMovesD2(gridc, Pl, NextIndex+1)[0][0], ss])

    if piecer == 'S':
        for i in range (2):
            if i == 0:
                for j in range(8):
                    gridc= grid.copy()
                    ss=[]
                    if (j-4)<0:
                        for asd in range(4-j):
                            ss.append(6)
                    if (j-4) >0:
                        for asd in range (j-4):
                            ss.append(5)
                    hm = int(max (hights[0+j], hights[1+j], (hights[2+j]-1) ))
                    if  gridc[20-hm][j] != 1 and gridc[20-hm][j+1] !=1 and gridc[20-hm-1][j+1] != 1 and gridc[20-hm-1][j+2] != 1:
                        gridc[20-hm][j] = 1
                        gridc[20-hm][j+1] = 1
                        gridc[20-hm-1][j+1] = 1
                        gridc[20-hm-1][j+2] = 1

                        if NextIndex == 1:
                            steps.append([score1(gridc), ss])
                        else : 
                            steps.append([score1(gridc)+ 0.787* CreatAllMovesD2(gridc, Pl, NextIndex+1)[0][0], ss])

            if i == 1:
                for j in range (9):
                    gridc = grid.copy()
                    ss = [4]
                    if (j-4)<0:
                        for asd in range (4-j):
                            ss.append(6)
                    if (j-4) >0:
                        for asd in range (j-4):
                            ss.append(5)
                    hm = int (max ([hights[0+j], hights[1+j] +1 ]))
                    if gridc[20 - hm][j]!=1 and gridc[20 -hm][j+1]!=1 and gridc[20 -hm -1][j]!=1 and gridc[20-hm+1][j+1]!=1:
                        gridc[20-hm][j]=1
                        gridc[20-hm][j+1]=1
                        gridc[20-hm-1][j]=1
                        gridc[20-hm+1][j+1]=1

                        if NextIndex == 1:
                            steps.append([score1(gridc), ss])
                        else : 
                            steps.append([score1(gridc)+ 0.787* CreatAllMovesD2(gridc, Pl, NextIndex+1)[0][0], ss])

    if piecer == 'Z':
        for i in range (2):
            if i == 0:
                for j in range(8):
                    gridc= grid.copy()
                    ss=[]
                    if (j-4)<0:
                        for asd in range(4-j):
                            ss.append(6)
                    if (j-4) >0:
                        for asd in range (j-4):
                            ss.append(5)
                    hm = int(max ([hights[0+j],1+ hights[1+j], 1+ hights[2+j] ]))
                    if  gridc[20-hm][j] != 1 and gridc[20-hm][j+1] !=1 and gridc[20-hm+1][j+1] != 1 and gridc[20-hm+1][j+2] != 1:
                        gridc[20-hm][j] = 1
                        gridc[20-hm][j+1] = 1
                        gridc[20-hm+1][j+1] = 1
                        gridc[20-hm+1][j+2] = 1

                        if NextIndex == 1:
                            steps.append([score1(gridc), ss])
                        else : 
                            steps.append([score1(gridc)+ 0.787* CreatAllMovesD2(gridc, Pl, NextIndex+1)[0][0], ss])

            if i == 1:
                for j in range (9):
                    gridc = grid.copy()
                    ss = [4]
                    if (j-4)<0:
                        for asd in range (4-j):
                            ss.append(6)
                    if (j-4) >0:
                        for asd in range (j-4):
                            ss.append(5)
                    hm = int (max ([hights[0+j] , hights[1+j] -1]))
                    if gridc[int(20-hm)][j]!=1 and gridc[int(20-hm-1)][j]!=1 and gridc[int(20-hm-1)][j+1]!=1 and gridc[int(20-hm-2)][j+1]!=1:
                        gridc[20-hm][j]=1
                        gridc[20-hm-1][j]=1
                        gridc[20-hm-1][j+1]=1
                        gridc[20-hm-2][j+1]=1

                        if NextIndex == 1:
                            steps.append([score1(gridc), ss])
                        else : 
                            steps.append([score1(gridc)+ 0.787* CreatAllMovesD2(gridc, Pl, NextIndex+1)[0][0], ss])

    if piecer == "T":
        for i in range(4):
            if i == 0:
                for j in range (8):
                    gridc = grid.copy()
                    ss=[]
                    if (j-4)<0:
                        for asd in range (4-j):
                            ss.append(6)
                    if (j-4) > 0:
                        for asd in range (j-4):
                            ss.append(5)
                    hm = int (max (hights[0+j:3+j]))
                    if gridc[20-hm][j] != 1 and gridc[20-hm][j+1] != 1 and gridc[20-hm][j+2] != 1 and gridc[20-hm-1][j+1] != 1:
                        gridc[20-hm][j] = 1
                        gridc[20-hm][j+1] = 1
                        gridc[20-hm][j+2] = 1
                        gridc[20-hm-1][j+1] = 1
                        if NextIndex == 1:
                            steps.append([score1(gridc), ss])
                        else : 
                            steps.append([score1(gridc)+ 0.787* CreatAllMovesD2(gridc, Pl, NextIndex+1)[0][0], ss])

            if i == 1: 
                for j in range (9):
                    gridc = grid.copy()
                    ss= [4]
                    if (j-4)< 0:
                        for asd in range (4-j):
                            ss.append(6)
                    if (j-4) >0:
                        for asd in range (j-4):
                            ss.append(5)
                    hm = int (max ([hights[j+0],hights[j+1] +1]) )

                    if gridc [20-hm][j] != 1 and gridc [20-hm][j+1] != 1 and gridc[20-hm-1][j+1] != 1 and gridc[20-hm+1][j+1] != 1 :
                        gridc[20-hm][j]= 1
                        gridc[20-hm][j+1]= 1
                        gridc[20-hm-1][j+1]= 1
                        gridc[20-hm+1][j+1]= 1
                        if NextIndex == 1:
                            steps.append([score1(gridc), ss])
                        else : 
                            steps.append([score1(gridc)+ 0.787* CreatAllMovesD2(gridc, Pl, NextIndex+1)[0][0], ss])

            if i == 2: 
                for j in range (8):
                    gridc = grid.copy()
                    ss = [4,4]
                    if (j-4)<0 :
                        for asd in range (4-j):
                            ss.append(6)
                    if (j-4)>0: 
                        for asd in range (j-4):
                            ss.append(5)

                    hm = int (max ([hights[j],hights[j+1]+1,hights[j+2]]))
                    if gridc[20-hm][j+1] != 1 and gridc[20-hm][j] != 1 and gridc[20-hm][j+2] != 1 and gridc[20-hm+1][j+1] != 1:
                        gridc[20-hm][j] = 1
                        gridc[20-hm][j+1] = 1       
                        gridc[20-hm][j+2] = 1
                        gridc[20-hm+1][j+1] = 1
                        if NextIndex == 1:
                            steps.append([score1(gridc), ss])
                        else : 
                            steps.append([score1(gridc)+ 0.787* CreatAllMovesD2(gridc, Pl, NextIndex+1)[0][0], ss])

            if i == 3:
                for j in range(9):
                    gridc = grid.copy()
                    ss= [3]
                    if (j-5) <0 :
                        for asd in range (5-j):
                            ss.append(6)
                    if (j-5) >0:
                        for asd in range (j-5):
                            ss. append(5)

                    hm = int (max ([hights[j], hights[j+1] -1]))
                    if gridc[20-hm][j] != 1 and gridc[20-hm-1][j] != 1 and gridc[20-hm-2][j] != 1 and gridc [20-hm-1][j+1] != 1:
                         gridc[20-hm][j] = 1
                         gridc[20-hm-1][j] = 1
                         gridc[20-hm-2][j] = 1
                         gridc[20-hm-1][j+1] = 1
                         if NextIndex == 1:
                            steps.append([score1(gridc), ss])
                         else : 
                            steps.append([score1(gridc)+ 0.787* CreatAllMovesD2(gridc, Pl, NextIndex+1)[0][0], ss])

    # sort all the moves
    steps.sort()
    return steps

def step(action):
    # A function that plays the current move @action
    env.step(0)
    env.step(0)
    env.step(0)
    return env.step(action)

if __name__ == "__main__":

    import time

    env = TetrisSingleEnv(gridchoice="none", obs_type="grid", mode="human")
    ob = env.reset()

    start = time.time()

    last = 0
    for i in range(100000):
        ob, reward, done, infos, b_list = step(0)

        if (b_list[0] == 'S' or b_list[0] == 'Z') and i == 0:
            ob, reward, done, infos, b_list = step(1)

        ss = CreatAllMovesD2(ob, b_list,0)
        if len(ss) > 0:
            for k in range(len(ss[0][1])):
                step(ss[0][1][k])
        step(2)

        if done:
            print(time.time() - start)
            print(infos)
            ob = env.reset()
            time.sleep(2)
