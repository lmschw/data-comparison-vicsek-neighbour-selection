import pandas as pd
import numpy as np

import AnimatorMatplotlib
import Animator2D

import ServiceSavedModel


"""
Hangjian Ling et al. “Local interactions and their group-level consequences in flocking jackdaws”. 
In: Proceedings of the Royal Society B 286.1906 (2019), p. 20190865.
"""

df = pd.read_csv('data/Ling_2019/data_ling_flock1.csv')
original_df = df

# create flock assignment column
df['flock'] = 6
df['flock'] = np.where(df.index < df[df['x,m'] == "06******"].index[0], 5, df['flock'])
df['flock'] = np.where(df.index < df[df['x,m'] == "05******"].index[0], 4, df['flock'])
df['flock'] = np.where(df.index < df[df['x,m'] == "04******"].index[0], 3, df['flock'])
df['flock'] = np.where(df.index < df[df['x,m'] == "03******"].index[0], 2, df['flock'])
df['flock'] = np.where(df.index < df[df['x,m'] == "02******"].index[0], 1, df['flock'])

# clean flock assignment rows
df = df.drop(df[df['t,s'].isna()].index) 
#print(df.size)

# transform times into time steps
df["time"] = df['t,s'].rank(method='dense').astype(int)
df["time"] = df['time'] -1 # starting from 0

#print(df[df["time"] == 0])

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


"""
dfcur = df[df['flock'] == 2]
np.min(dfcur['x,m']), np.max(dfcur['x,m']), np.min(dfcur['y,m']), np.max(dfcur['y,m']), np.min(dfcur['u,m/s']), np.max(dfcur['u,m/s']), np.min(dfcur['v,m/s']), np.max(dfcur['v,m/s'])

flock 1: xmin = -25.66, xmax = 32.35, ymin = -26.07, ymax = 32.5, umin = 3.63, umax = 23.51, vmin = -12.46, vmax = 12.52
flock 2: xmin = -21.58, xmax = 38.32, ymin = -40.66, ymax = 27.62, umin = -4.82, umax = 9.65, vmin = -7.94, vmax = 16.34
flock 3: xmin = -21.58, xmax = 38.32, ymin = -40.66, ymax = 27.62, umin = -4.82, umax = 9.65, vmin = -7.94, vmax = 16.34
flock 4: xmin = -29.76, xmax = 33.17, ymin = -25.77, ymax = 32.93, umin = -5.48, umax = 12.25, vmin = -6.61, vmax = 12.52
flock 5: xmin = -37.75, xmax = 27.62, ymin = -26.59, ymax = 39.46, umin = -7.44, umax = 17.73, vmin = -13.39, vmax = 12.54 
flock 6: xmin = -22.58, xmax = 29.29, ymin = -25.19, ymax = 15.95, umin = 6.44, umax = 16.99, vmin = -4.3, vmax = 7.0 

conclusion: x and y can be increased by 50 to get coordinates between 0 and 100. 
WARNING: the third dimension has not been considered
"""
df['x,m'] = df['x,m'] + 50
df['y,m'] = df['y,m'] + 50


#print(df.head())
#print(df.tail())

# find the duration that includes all agents
#print(df['time'].value_counts())
df2 = df.groupby('time').filter(lambda x : len(x)>200)
#print(df2['time'].value_counts())

times = []
positions = []
orientations = []
colours = []

t = 0
flock = 1
n = int(np.max(df['ID']))
tmax = np.max(df['time'])



#tmax = 10

for flock in range(6, 7):
    for t in range(tmax):
        if t % 100 == 0:
            print(f"{t}/{tmax}")
        times.append(t)
        positionsT = []
        orientationsT = []
        coloursT = []

        dfT = df.loc[(df['flock'] == flock) & (df['time'] == t), ['ID','flock', 'time', 'x,m', 'y,m', 'u,m/s', 'v,m/s']]
        for i in range(n):
            coloursT.append("k")

            dfI = dfT.loc[(df['ID'] == str(i)), ['ID','flock', 'time', 'x,m', 'y,m', 'u,m/s', 'v,m/s']]
            if dfI.shape[0] == 1:
                #print(f"t = {t}, i = {i}")
                
                #positionsT[i][0] = dfI['x,m'].iloc(0)[0]
                #positionsT[i][1] = dfI['y,m'].iloc(0)[0]
                #orientationsT[i][0] = dfI['u,m/s'].iloc(0)[0]
                #orientationsT[i][1] = dfI['v,m/s'].iloc(0)[0]
                #print(positionsT[i])
                #print(orientationsT[i])
                
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
    print(colours)

    simulationData = (times, np.array(positions), np.array(orientations))

    filename = f"ling_2019_flock1_flock={flock}_tmax={tmax}"

    ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, path=f"{filename}.json")

    # Initalise the animator
    animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

    # prepare the animator
    preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=tmax)

    preparedAnimator.saveAnimation(f"{filename}.mp4")

    # Display Animation
    #preparedAnimator.showAnimation()
