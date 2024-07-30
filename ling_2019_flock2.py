import pandas as pd
import numpy as np

import AnimatorMatplotlib
import Animator2D

import ServiceSavedModel


"""
Hangjian Ling et al. “Local interactions and their group-level consequences in flocking jackdaws”. 
In: Proceedings of the Royal Society B 286.1906 (2019), p. 20190865.
"""

df = pd.read_csv('data/Ling_2019/data_ling_flock2.csv')
original_df = df

# transform times into time steps
df["time"] = df['t,s'].rank(method='dense').astype(int)
df["time"] = df['time'] -1 # starting from 0

# transform positions, orientations and accelerations into floats
df['x,m'] = df['x,m'].astype(float)
df['y,m'] = df['y,m'].astype(float)
df['z,m'] = df['z,m'].astype(float)
df['u,m/s'] = df['u,m/s'].astype(float)
df['v,m/s'] = df['v,m/s'].astype(float)
df['w,m/s'] = df['w,m/s'].astype(float)
df['ax,m/s2'] = df['ax,m/s2'].astype(float)
df['ay,m/s2'] = df['ay,m/s2'].astype(float)
df['az,m/s2'] = df['az,m/s2'].astype(float)

dfcur = df
print(np.min(dfcur['x,m']), np.max(dfcur['x,m']), np.min(dfcur['y,m']), np.max(dfcur['y,m']), np.min(dfcur['u,m/s']), np.max(dfcur['u,m/s']), np.min(dfcur['v,m/s']), np.max(dfcur['v,m/s']))

"""
dfcur = df[df['flock'] == 2]
np.min(dfcur['x,m']), np.max(dfcur['x,m']), np.min(dfcur['y,m']), np.max(dfcur['y,m']), np.min(dfcur['u,m/s']), np.max(dfcur['u,m/s']), np.min(dfcur['v,m/s']), np.max(dfcur['v,m/s'])

max: 53.68 - move by  46
conclusion: x and y can be increased by 50 to get coordinates between 0 and 100. 
WARNING: the third dimension has not been considered
"""
df['x,m'] = df['x,m'] + 46
df['y,m'] = df['y,m'] + 46


#print(df.head())
#print(df.tail())


times = []
positions = []
orientations = []
colours = []

t = 0
flock = 1
n = int(np.max(df['ID']))
tmax = np.max(df['time'])



#tmax = 10

for t in range(tmax):
    if t % 100 == 0:
        print(f"{t}/{tmax}")
    times.append(t)
    positionsT = []
    orientationsT = []
    coloursT = []

    dfT = df.loc[(df['time'] == t), ['ID','time', 'x,m', 'y,m', 'u,m/s', 'v,m/s']]
    for i in range(n):
        coloursT.append("k")

        dfI = dfT.loc[(df['ID'] == str(i)), ['ID','time', 'x,m', 'y,m', 'u,m/s', 'v,m/s']]
        if dfI.shape[0] == 1:
            positionsT.append([dfI['x,m'].iloc(0)[0], dfI['y,m'].iloc(0)[0]])
            orientationsT.append([dfI['u,m/s'].iloc(0)[0], dfI['v,m/s'].iloc(0)[0]]) 
        else:
            positionsT.append([-100, -100])
            orientationsT.append([0,0])

        if dfI.shape[0] > 1:
            print("more than 1 row selected")
            print(dfI)
    
    """"
    normOrientations = (np.sqrt(np.sum(np.array(orientationsT)**2,axis=1))[:,np.newaxis])
    for j in range(len(orientationsT)):
        if normOrientations[j] != 0:
            orientationsT[j] = orientationsT[j]/normOrientations[j]
            """
    positions.append(positionsT)
    orientations.append(orientationsT)
    colours.append(coloursT)

    #print(df[df['ID'] == i and df['flock'] == flock and df['time'] == t])
    #positionsT[0] = ['']

simulationData = (times, np.array(positions), np.array(orientations))

filename = f"ling_2019_flock2_tmax={tmax}"

ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, path=f"{filename}.json")

# Initalise the animator
animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

# prepare the animator
preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=tmax)

preparedAnimator.saveAnimation(f"{filename}.mp4")

# Display Animation
#preparedAnimator.showAnimation()
