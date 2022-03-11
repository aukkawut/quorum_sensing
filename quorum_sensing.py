import numpy as np
def createGrid(W,H):
    '''
    This function will initialize the grid of the experiment

    Arguments: 
        W, the width of the grid
        H, the hight of the grid

    Return: 
        grid, grid containing a tensor (which is 5 matrices). grid[0] is signal, grid[1] is timer of refractory,
             grid[2] is initialize status,grid[3] is state (suscept or refract), and grid[4] is the done timer 
    '''
    grid = np.zeros((6,H,W))
    return grid
def eight_neighbors(pos, grid):
    '''
    This function will return their 8 neighbors value
    
    Arguments:  
        pos, array of position that we are currently at i.e. [0,2] means x[0][2]
        grid, grid containing a tensor (which is 5 matrices). grid[0] is signal, grid[1] is timer of refractory,
             grid[2] is initialize status,grid[3] is state (suscept or refract), and grid[4] is the done timer
    
    Return: 
        value, a list of 8 neighbors value
    '''
    value = []
    for i in range(max(0, pos[0] - 1), min(grid.shape[1], pos[0] + 2)):
        for j in range(max(0, pos[1] - 1), min(grid.shape[2], pos[1] + 2)):
            if (i, j) != pos:
                value.append(grid[0][i][j])
    return value
def four_neighbors(pos, grid):
    '''
    This function will return their 4 neighbors value
    
    Arguments:  
        pos, array of position that we are currently at i.e. [0,2] means x[0][2]
        grid, grid containing a tensor (which is 5 matrices). grid[0] is signal, grid[1] is timer of refractory,
             grid[2] is initialize status,grid[3] is state (suscept or refract), grid[4] is the done timer, and grid[5] is estimated size
    
    Return: 
        value, a list of 4 neighbors value
    '''
    value = []
    i,j = pos
    if i > 0:
        value.append(grid[0][i-1][j])
    if i+1 < grid.shape[1]:
        value.append(grid[0][i+1][j])
    if j > 0:
        value.append(grid[0][i][j-1])
    if j+1 < grid.shape[2]:
        value.append(grid[0][i][j+1])
    return value
def update8(grid,P,R,size):
    '''
    This function will return the updated grid after 1 iteration with 8 neighbors model
    
    Arguments:  
        grid, grid containing a tensor (which is 5 matrices). grid[0] is signal, grid[1] is timer of refractory,
             grid[2] is initialize status,grid[3] is state (suscept or refract), and grid[4] is the done timer
        P,  probability of sending a signal for itself
        R,  refractory time
        size, size of the quorum
    
    Return: 
        grid, grid containing a tensor (which is 5 matrices). grid[0] is signal, grid[1] is timer of refractory,
             grid[2] is initialize status,grid[3] is state (suscept or refract), grid[4] is the done timer, and grid[5] is estimated size
        size, size of the quorum (mean of grid[5])
    '''
    grid_ref = np.copy(grid)
    for i in range(H):
        for j in range(W):
            if grid_ref[4][i][j] >= 1/P: #Done
                pass
            elif grid_ref[3][i][j] == 0: #susceptible
                if 1 in eight_neighbors((i,j),grid_ref):
                    grid[0][i][j] = 1
                    grid[1][i][j] = R
                    grid[3][i][j] = 1
                    grid[5][i][j] = grid[5][i][j] + 1
                elif grid_ref[2][i][j] == 0 and (np.random.uniform()>P):
                    grid[0][i][j] = 1
                    grid[1][i][j] = R
                    grid[2][i][j] = 1
                    grid[3][i][j] = 1
                    grid[5][i][j] = grid[5][i][j] + 1
                else:
                    grid[4][i][j] = grid[4][i][j] + 1
            else: #refractory
                grid[0][i][j] = 0
                grid[1][i][j] =  grid[1][i][j] - 1
                if (grid[1][i][j] <= 0):
                    grid[3][i][j] = 0
                    grid[1][i][j] = 0
    size = grid[5].max()
    sums = grid[5].sum()
    return grid,size,sums
def update4(grid,P,R,size):
    '''
    This function will return the updated grid after 1 iteration with 4 neighbors model
    
    Arguments:  
        grid, grid containing a tensor (which is 5 matrices). grid[0] is signal, grid[1] is timer of refractory,
             grid[2] is initialize status,grid[3] is state (suscept or refract), and grid[4] is the done timer
        P,  probability of sending a signal for itself
        R,  refractory time
        size, size of the quorum
    Return: 
        grid, grid containing a tensor (which is 5 matrices). grid[0] is signal, grid[1] is timer of refractory,
             grid[2] is initialize status,grid[3] is state (suscept or refract), grid[4] is the done timer, and grid[5] is estimated size
        size, size of the quorum
    '''
    grid_ref = np.copy(grid)
    for i in range(H):
        for j in range(W):
            if grid_ref[4][i][j] >= 1/P: #Done
                pass
            elif grid_ref[3][i][j] == 0: #susceptible
                if 1 in four_neighbors((i,j),grid_ref):
                    grid[0][i][j] = 1
                    grid[1][i][j] = R
                    grid[3][i][j] = 1
                    grid[5][i][j] = grid[5][i][j] + 1
                elif grid_ref[2][i][j] == 0 and (np.random.uniform()>P):
                    grid[0][i][j] = 1
                    grid[1][i][j] = R
                    grid[2][i][j] = 1
                    grid[3][i][j] = 1
                    grid[5][i][j] = grid[5][i][j] + 1
                else:
                    grid[4][i][j] = grid[4][i][j] + 1
            else:
                grid[0][i][j] = 0
                grid[1][i][j] =  grid[1][i][j] - 1
                if (grid[1][i][j] <= 0):
                    grid[3][i][j] = 0
                    grid[1][i][j] = 0
    size = grid[5].max()
    sums = grid[5].sum()
    return grid,size,sums
if __name__ == '__main__':
#initial param is the worst!!! Like, I miss my intro to programming class style.
    W = int(input('Enter width of the grid: '))
    H = int(input('Enter height of the grid: '))
    grid = createGrid(W,H)
    size = 0
    P = float(input('Enter the probability: '))
    R = int(input('Enter refractory time: '))
    S = int(input('Enter 4/8 neighbors: '))
    tol = 0 #add convergence condition -> 10000 iterations
    if S == 4:
        while(True):
            count = 0
            grid, size, sums = update4(grid,P,R,size)
            if grid[4].sum() >= H*W/P:
                break
            tol = tol + 1
            if tol % 100 == True:
                print("Current Concensus: ", str(grid[4].sum()/(H*W)))
                print("Current Size: ", str(size))
                print("Current Sum:",str(sums))
    else:
        while(True):
            count = 0
            grid, size, sums = update8(grid,P,R,size)
            if grid[4].sum() >= H*W/P:
                break
            tol = tol + 1
            if tol % 100 == True:
                print("Current Concensus: ", str(grid[4].sum()/(H*W)))
                print("Current Size: ", str(size))
                print("Current Sum:",str(sums))
    print('The estimated size is: ' + str(size))
    print('The estimated sum is: ' + str(sums))
    print('The real size is: ' + str(H*W))
    print('The difference is: '+ str(np.abs(size-H*W)) + '\n that is ' + str(np.abs(size-H*W)/(H*W)*100) +'% error')
