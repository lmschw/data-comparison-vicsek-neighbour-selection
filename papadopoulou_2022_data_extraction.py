import pandas as pd
import numpy as np
import math

import ServiceSavedModel
import AnimatorMatplotlib
import Animator2D

"""
Extraction of data from 

Data procured from: 

"""

def computeUvCoordinates(angle):
    """
    Computes the (u,v)-coordinates based on the angle.

    Params:
        - angle (float): the angle in radians

    Returns:
        An array containing the [u, v]-coordinates corresponding to the angle.
    """
    # compute the uv-coordinates
    U = np.cos(angle)
    V = np.sin(angle)
    
    return [U,V]

def computeOrientation(row):
    return computeUvCoordinates(row["dirAngl"])

def getOrientationSeries(row):
    orient = computeOrientation(row)
    return pd.Series({'u': orient[0], 'v': orient[1]})

def getTimesPositionsOrientationsColoursFromDf(df):
    x = 'x_translated'
    y = 'y_translated'
    u = 'u'
    v = 'v'
    n = int(np.max(df['id']))
    tmax = np.max(df['timestep'])

    times = []
    positions =[]
    orientations = []
    colours = []
    for t in range(tmax):
        if t % 100 == 0:
            print(f"{t}/{tmax}")
        times.append(t)
        positionsT = []
        orientationsT = []
        coloursT = []

        dfT = df.loc[(df['timestep'] == t), ['datetime', 'id','time', 'timestep', 'posx', 'posy', x, y, u, v, 'dirAngl']]
        for i in range(1, n+1):
            coloursT.append("k")

            dfI = dfT.loc[(dfT['id'] == i), ['datetime', 'id','time', 'timestep', 'posx', 'posy', x, y, u, v, 'dirAngl']]
            if dfI.shape[0] == 1:
                positionsT.append([dfI[x].iloc(0)[0], dfI[y].iloc(0)[0]])
                orientationsT.append([dfI[u].iloc(0)[0], dfI[v].iloc(0)[0]]) 
            else:
                positionsT.append([-100, -100])
                orientationsT.append([0,0])

            if dfI.shape[0] > 1:
                print("more than 1 row selected")
                #print(dfI)
        
        """"
        normOrientations = (np.sqrt(np.sum(np.array(orientationsT)**2,axis=1))[:,np.newaxis])
        for j in range(len(orientationsT)):
            if normOrientations[j] != 0:
                orientationsT[j] = orientationsT[j]/normOrientations[j]
                """
        positions.append(positionsT)
        orientations.append(orientationsT)
        colours.append(coloursT)
    return times, positions, orientations, colours

factor = 1
baseSaveFilename = "papadopoulou_2022_self_c_extracted"
filename = "data/papadopoulou_2022/all_self_c.csv"
df = pd.read_csv(filename)
df_original = df

df["expId"] = df['datetime'].rank(method='dense').astype(int)
df["expId"] = df['expId']

df["timestep"] = df['time'].rank(method='dense').astype(int)
df["timestep"] = df['timestep'] -1

df['x_translated'] = df['posx'] + 1 # original values between -0.6038 and -0.593386, new values between 0.3962 and 0.40661400000000003
df['y_translated'] = df['posy'] - 51 # original values between 51.366656 and 51.376064, new values between 0.366655999999999 and 0.3760639999999995


dfOrient = df.apply(getOrientationSeries, axis=1)
df['u'] = dfOrient['u']
df['v'] = dfOrient['v']

df2 = df[['datetime', 'time', 'timestep', 'id', 'posx', 'posy', 'x_translated', 'y_translated', 'u', 'v', 'dirAngl']]

print(df2.head(10))

df2.to_csv(f"{baseSaveFilename}_all.csv", index=False)

for expId in df['expId'].unique():
    saveFilename = f"{baseSaveFilename}_{expId}"
    dfExp = df[df['expId'] == expId]
    tmax = np.max(dfExp['timestep'])

    # transforming the df into positions and orientations
    times, positions, orientations, colours = getTimesPositionsOrientationsColoursFromDf(dfExp)

    simulationData = (times, np.array(positions), np.array(orientations))



    ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, path=f"{saveFilename}.json")

    # Initalise the animator
    dimFactor = 1
    animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (factor*dimFactor,factor*dimFactor,factor*dimFactor), colours)

    # prepare the animator
    preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=tmax)

    preparedAnimator.saveAnimation(f"{saveFilename}.mp4")

    # Display Animation
    #preparedAnimator.showAnimation()
