import pandas as pd
import numpy as np
import math
import json

import ServiceSavedModel
import AnimatorMatplotlib
import Animator2D

"""
Extraction of data from 
Lecheval, Valentin et al. (2018). Data from: Social conformity and propagation of information in collective u-turns of fish schools [Dataset]. Dryad. https://doi.org/10.5061/dryad.9m6d2

Data procured from: 
https://datadryad.org/stash/dataset/doi:10.5061/dryad.9m6d2
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
    return computeUvCoordinates(row["angle"])

def getOrientationSeries(row):
    orient = computeOrientation(row)
    return pd.Series({'u': orient[0], 'v': orient[1]})

def getTimesPositionsOrientationsColoursFromDf(df):
    x = 'x_t'
    y = 'y_t'
    u = 'u'
    v = 'v'
    n = int(np.max(df['id']))
    tmax = np.max(df['t'])

    times = []
    positions =[]
    orientations = []
    colours = []
    for t in range(tmax):
        if t % 1000 == 0:
            print(f"{t}/{tmax}")
        times.append(t)
        positionsT = []
        orientationsT = []
        coloursT = []

        dfT = df.loc[(df['t'] == t), ['t', 'id', 'x', 'y', x, y, u, v, 'angle']]
        for i in range(1, n+1):
            coloursT.append("k")

            dfI = dfT.loc[(dfT['id'] == i), ['t', 'id', 'x', 'y', x, y, u, v, 'angle']]
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
numFiles = {4: 10, 5: 10, 8: 9, 10: 14}

filenames = {
    "4-1":"data/Lecheval_2018/n=4/exp04H20150827_12h19.csv", 
    "4-2":"data/Lecheval_2018/n=4/exp04H20150829_11h49.csv", 
    "4-3":"data/Lecheval_2018/n=4/exp04H20150829_13h18.csv", 
    "4-4":"data/Lecheval_2018/n=4/exp04H20150830_14h48.csv", 
    "4-5":"data/Lecheval_2018/n=4/exp04H20150831_11h29.csv", 
    "4-6":"data/Lecheval_2018/n=4/exp04H20150901_12h48.csv", 
    "4-7":"data/Lecheval_2018/n=4/exp04H20150903_13h00.csv", 
    "4-8":"data/Lecheval_2018/n=4/exp04H20150904_13h06.csv", 
    "4-9":"data/Lecheval_2018/n=4/exp04H20150905_13h47.csv", 
    "4-10":"data/Lecheval_2018/n=4/exp04H20150905_15h25.csv",
    "5-1":"data/Lecheval_2018/n=5/exp05H20140926_10h50.csv", 
    "5-2":"data/Lecheval_2018/n=5/exp05H20141001_10h05.csv",
    "5-3":"data/Lecheval_2018/n=5/exp05H20141003_15h00.csv", 
    "5-4":"data/Lecheval_2018/n=5/exp05H20141008_15h30.csv",
    "5-5":"data/Lecheval_2018/n=5/exp05H20141010_10h38.csv", 
    "5-6":"data/Lecheval_2018/n=5/exp05H20141015_12h50.csv", 
    "5-7":"data/Lecheval_2018/n=5/exp05H20141022_11h45.csv", 
    "5-8":"data/Lecheval_2018/n=5/exp05H20141023_16h20.csv",
    "5-9":"data/Lecheval_2018/n=5/exp05H20141029_14h20.csv", 
    "5-10":"data/Lecheval_2018/n=5/exp05H20141030_11h15.csv",
    "8-1":"data/Lecheval_2018/n=8/exp08H20150821_11h04.csv", 
    "8-2":"data/Lecheval_2018/n=8/exp08H20150821_12h34.csv", 
    "8-3":"data/Lecheval_2018/n=8/exp08H20150821_14h04.csv", 
    "8-4":"data/Lecheval_2018/n=8/exp08H20150830_11h52.csv", 
    "8-5":"data/Lecheval_2018/n=8/exp08H20150830_13h18.csv", 
    "8-6":"data/Lecheval_2018/n=8/exp08H20150901_14h10.csv", 
    "8-7":"data/Lecheval_2018/n=8/exp08H20150902_11h41.csv",
    "8-8":"data/Lecheval_2018/n=8/exp08H20150903_11h28.csv", 
    "8-9":"data/Lecheval_2018/n=8/exp08H20150904_11h40.csv",
    "10-1":"data/Lecheval_2018/n=10/exp10H20141017_11h00.csv",
    "10-2":"data/Lecheval_2018/n=10/exp10H20141021_13h10iso.csv", 
    "10-3":"data/Lecheval_2018/n=10/exp10H20141023_13h05.csv",
    "10-4":"data/Lecheval_2018/n=10/exp10H20141024_11h30.csv", 
    "10-5":"data/Lecheval_2018/n=10/exp10H20141028_9h50.csv",
    "10-6":"data/Lecheval_2018/n=10/exp10H20141029_14h20.csv", 
    "10-7":"data/Lecheval_2018/n=10/exp10H20141031_13h15.csv",
    "10-8":"data/Lecheval_2018/n=10/exp10H20141031_15h00.csv",
    "10-9":"data/Lecheval_2018/n=10/exp10H20150901_11h21.csv",
    "10-10":"data/Lecheval_2018/n=10/exp10H20150902_13h05.csv", 
    "10-11":"data/Lecheval_2018/n=10/exp10H20150902_14h28.csv", 
    "10-12":"data/Lecheval_2018/n=10/exp10H20150903_14h45.csv", 
    "10-13":"data/Lecheval_2018/n=10/exp10H20150904_14h36.csv", 
    "10-14":"data/Lecheval_2018/n=10/exp10H20150905_11h53.csv"
}

speeds = {}
for n in [4, 5, 8, 10]:
    maxExpId = numFiles[n]
    for i in range(1, maxExpId):
        print(f"extracting from n={n}, i={i}")
        filepath = filenames[f"{n}-{i}"]
        df_horizontal = pd.read_csv(filepath)
        df_original = df_horizontal

        df_horizontal['t'] = df_horizontal.index + 1

        df = df_horizontal[["t", "X1", "Y1", "H1"]]
        df = df.rename(columns={"X1": "x", "Y1": "y", "H1":"angle"})
        df["id"] = 1  
        df = df[["t", "id", "x", "y", "angle"]]

        for j in range(2, n+1):
            dfJ = df_horizontal[["t", f"X{j}", f"Y{j}", f"H{j}"]]
            dfJ = dfJ.rename(columns={f"X{j}": "x", f"Y{j}": "y", f"H{j}":"angle"})
            dfJ["id"] = j
            df = pd.concat([df, dfJ])

        #print(df.head())  
        #df.add(df)

        #print(np.min(df['x']), np.max(df['x']), np.min(df['y']), np.max(df['y']))

        

        df['x_t'] = df['x'] + 352 # original values between -351.7241 and 353.0538, new values between 0.2759 and 705.0538
        df['y_t'] = df['y'] + 335 # original values between -334.8152 and 335.0937, new values between 0.1848 and 670.0937


        dfOrient = df.apply(getOrientationSeries, axis=1)
        df['u'] = dfOrient['u']
        df['v'] = dfOrient['v']

        #print(df.head(10))

        saveFilename = f"lecheval_2018_{n}-{i}"
        df.to_csv(f"{saveFilename}.csv", index=False)

        print("starting json generation")
        tmax = np.max(df['t'])

        # transforming the df into positions and orientations
        times, positions, orientations, colours = getTimesPositionsOrientationsColoursFromDf(df)

        simulationData = (times, np.array(positions), np.array(orientations))

        ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, path=f"{saveFilename}.json")

        print("computing average speed")

        distances = []
        for t in times:
            if t == times[-1]:
                continue
            for i in range(n):
                distances.append(math.dist(positions[t][i], positions[t+1][i]))
        speed = np.average(distances)
        print(f"{n}-{i}: {speed}")
        speeds[f"{n}-{i}"] = speed

        print("starting video generation")
        # Initalise the animator
        dimFactor = 1
        animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (750,750,750), colours)

        # prepare the animator
        preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=tmax)

        preparedAnimator.saveAnimation(f"{saveFilename}.mp4")

        # Display Animation
        #preparedAnimator.showAnimation()

path = "lecheval_2018_speeds.json"
with open(path, "w") as outfile:
        json.dump(speeds, outfile)
