import pandas as pd
import numpy as np
import math

import ServiceSavedModel
import AnimatorMatplotlib
import Animator2D

"""
Extraction of data from 
Lei, L., Escobedo, R., Sire, C., & Theraulaz, G. (2020). Computational and robotic modeling reveal parsimonious combinations of interactions between individuals in schooling fish. PLoS computational biology, 16(3), e1007194.

Data procured from: https://figshare.com/articles/dataset/Experimental_computational_and_robotic_data_from_Computational_and_robotic_modeling_reveal_parsimonious_combinations_of_interactions_between_individuals_in_schooling_fish_/11858379

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

def angleBetweenTwoVectors(vec1, vec2):
    # TODO: move to ServiceOrientations
    """
    Computes the angle between to vectors.

    Params:
        - vec1 (array of floats): the first vector
        - vec2 (array of floats): the second vector.

    Returns:
        Float representing the angle between the two vectors.
    """
    return np.arctan2(vec1[1]-vec2[1], vec1[0]-vec2[0])

def computeOrientation(row, translated=False):
    if translated == True:
        x = 'x'
        y = 'y'
    else:
        x = 'x_translated'
        y = 'y_translated'
    nextPositionDf = dfExp.loc[(dfExp['timestep'] == row['timestep'] +1) & (dfExp['exp_id'] == row['exp_id']) & (dfExp['fish_id'] == row['fish_id']) , [x, y]]
    if nextPositionDf.shape[0] == 1:
        vec1 = [nextPositionDf[x].iloc(0)[0], nextPositionDf[x].iloc(0)[0]]
        vec0 = [row[x], row[x]]
        return computeUvCoordinates(angleBetweenTwoVectors(vec0, vec1))
    return [0,0]

def getOrientationSeries(row):
    orient = computeOrientation(row, translated=False)
    return pd.Series({'u': orient[0], 'v': orient[1]})

def getOrientationSeriesTranslated(row):
    orient = computeOrientation(row, translated=True)
    return pd.Series({'u': orient[0], 'v': orient[1]})

def getTimesPositionsOrientationsColoursFromDf(df):
    x = 'x_translated'
    y = 'y_translated'
    u = 'u_translated'
    v = 'v_translated'
    n = int(np.max(df['fish_id']))
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

        dfT = df.loc[(df['timestep'] == t), ['exp_id','fish_id', 'timestep', x, y, u, v]]
        for i in range(1, n+1):
            coloursT.append("k")

            dfI = dfT.loc[(df['fish_id'] == i), ['exp_id','fish_id', 'timestep', x, y, u, v]]
            if dfI.shape[0] == 1:
                positionsT.append([dfI[x].iloc(0)[0], dfI[y].iloc(0)[0]])
                orientationsT.append([dfI[u].iloc(0)[0], dfI[v].iloc(0)[0]]) 
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
    return times, positions, orientations, colours


factor = 1
filename = "data/Lei_2020/lei_2020_fish_data.csv"
df = pd.read_csv(filename)

df['timestep'] = 0
df['x_translated'] = 0.0
df['y_translated'] = 0.0
df['u'] = 0.0
df['v'] = 0.0
df['u_translated'] = 0.0
df['v_translated'] = 0.0


print(np.max(df['exp_id']))
for expId in df['exp_id'].unique():
#for expId in [1]:
#for expId in range(2, np.max(df['exp_id'])):
    filename = f"lei_2020_extracted_data/lei_2020_expId={expId}"
    
    dfExp = df.loc[(df['exp_id'] == expId), ['exp_id', 'fish_id', 't', 'x', 'y']]

    dfExp["timestep"] = dfExp['t'].rank(method='dense').astype(int)
    dfExp["timestep"] = dfExp['timestep'] -1 # starting from 0

    dfExp['timestep'] = dfExp['timestep'].astype(int)
    dfExp['exp_id'] = dfExp['exp_id'].astype(int)
    dfExp['fish_id'] = dfExp['fish_id'].astype(int)

    #dfcur = dfExp
    #print(np.min(dfcur['x']), np.max(dfcur['x']), np.min(dfcur['y']), np.max(dfcur['y']))
    dfExp['x_translated'] = (dfExp['x'] + 1) * factor
    dfExp['y_translated'] = (dfExp['y'] + 1) * factor

    dfOrient = dfExp.apply(getOrientationSeries, axis=1)
    dfOrientTranslated = dfExp.apply(getOrientationSeriesTranslated, axis=1)
    dfExp['u'] = dfOrient['u']
    dfExp['v'] = dfOrient['v']
    dfExp['u_translated'] = dfOrientTranslated['u']
    dfExp['v_translated'] = dfOrientTranslated['v']

    #print(dfExp['u'] == dfExp['u_translated'])

    #print(dfExp.head())
    df[df['exp_id'] == expId] = dfExp
    #print(df.head())

    dfExp.to_csv(f"{filename}.csv", index=False)

    tmax = np.max(dfExp['timestep'])

    # transforming the df into positions and orientations
    times, positions, orientations, colours = getTimesPositionsOrientationsColoursFromDf(dfExp)

    simulationData = (times, np.array(positions), np.array(orientations))

    

    ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, path=f"{filename}.json")

    # Initalise the animator
    dimFactor = 2
    animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (factor*dimFactor,factor*dimFactor,factor*dimFactor), colours)

    # prepare the animator
    preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=tmax)

    preparedAnimator.saveAnimation(f"{filename}.mp4")

    # Display Animation
    #preparedAnimator.showAnimation()

df.to_csv("lei_2020_all_experiments.csv", index=False)
