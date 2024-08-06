import numpy as np
import random
import math
from heapq import nlargest
from heapq import nsmallest

import ServiceSavedModel

datafileLocation = "lei_2020_extracted_data/"

def isInDomain(position, radius, centerPoint):
    return ((position[0] - centerPoint[0])**2 + (position[1] - centerPoint[1])**2) <= radius **2 

def prettyPrintFitsCounter(fitsCounter, total):
    return f"'N':{np.round(fitsCounter.get("N")/total*100, 1)}%,'F':{np.round(fitsCounter.get("F")/total*100, 1)}%,'LOD':{np.round(fitsCounter.get("LOD")/total*100, 1)}%,'HOD':{np.round(fitsCounter.get("HOD")/total*100, 1)}%"

def normalizeOrientations(orientations):
    """
    Normalises the orientations of all particles for the current time step

    Parameters:
        - orientations (array): The current orientations of all particles

    Returns:
        The normalised orientations of all particles as an array.
    """
    return orientations/(np.sqrt(np.sum(orientations**2,axis=1))[:,np.newaxis])

def checkWhichMechanismFits(n, k, i, best, positions, orientations):  
    neighbours = []
    currentParticlePosition = positions[i]
    currentParticleOrientation = orientations[i]
    fits = {"N": False, "F": False, "LOD": False, "HOD": False}
    candidates = [j for j in range(n) if j != i]
    positionDifferences = {candidateIdx: math.dist(currentParticlePosition, positions[candidateIdx]) for candidateIdx in candidates}
    orientationDifferences = {candidateIdx: math.dist(currentParticleOrientation, orientations[candidateIdx]) for candidateIdx in candidates}

    nearestNeighbours = nsmallest(k, positionDifferences, positionDifferences.get)
    if (k == 1 and nearestNeighbours[0] == best) or (nearestNeighbours == best):
        fits["N"] = True
    farthestNeighbours = nlargest(k, positionDifferences, positionDifferences.get)
    if (k == 1 and farthestNeighbours[0] == best) or (farthestNeighbours == best):
        fits["F"] = True
    lodNeighbours = nsmallest(k, orientationDifferences, orientationDifferences.get)
    if (k == 1 and lodNeighbours[0] == best) or (lodNeighbours == best):
        fits["LOD"] = True
    hodNeighbours = nsmallest(k, orientationDifferences, orientationDifferences.get)
    if (k == 1 and hodNeighbours[0] == best) or (hodNeighbours == best):
        fits["HOD"] = True
    return fits


def printOverallFitsCounter(startExp, stopExp):
    overallFitsCounter = {'N': [], 'F': [], 'LOD': [], 'HOD': []}
    for expId in range(startExp, stopExp):
        filename = f"lei_2020_expId={expId}"

        times, positions, orientations, colours = ServiceSavedModel.loadModel(f"{datafileLocation}{filename}.json", loadSwitchValues=False)

        n = 5
        k = 1
        fitsCounter = {"N": 0, "F": 0, "LOD": 0, "HOD": 0}
        # check which selection mechanism gets us closest to the new orientation for every agent at every time step
        bestSelectionMechanisms = []
        for t in times:
            if t == times[-1]:
                continue
            bestSelectionMechanismsT = []
            for i in range(n):

                orientationI = orientations[t][i]
                nextOrientationI = orientations[t+1][i]

                best = -1
                bestDiff = -1
                for j in range(5):
                    if j == i:
                        continue
                    newOrientation = orientationI + orientations[t][j]
                    diff = math.dist(nextOrientationI, newOrientation)
                    if best == -1:
                        best = j
                        bestDiff = diff
                    else:
                        if bestDiff > diff:
                            best = j
                            bestDiff = diff
                fits = checkWhichMechanismFits(n, k, i, best, positions[t], orientations[t])
                if fits["N"] == True:
                    fitsCounter["N"] = fitsCounter["N"] + 1
                if fits["F"] == True:
                    fitsCounter["F"] = fitsCounter["F"] + 1
                if fits["LOD"] == True:
                    fitsCounter["LOD"] = fitsCounter["LOD"] + 1
                if fits["N"] == True:
                    fitsCounter["HOD"] = fitsCounter["HOD"] + 1

                bestSelectionMechanismsT.append(fits)
            bestSelectionMechanisms.append(bestSelectionMechanismsT)

        print(f"expId={expId}, total: {n * t}. results:{prettyPrintFitsCounter(fitsCounter, n*t)}")
        overallFitsCounter['N'].append(fitsCounter['N']/(n*t))
        overallFitsCounter['F'].append(fitsCounter['F']/(n*t))
        overallFitsCounter['LOD'].append(fitsCounter['LOD']/(n*t))
        overallFitsCounter['HOD'].append(fitsCounter['HOD']/(n*t))

    print(f"N: {np.average(overallFitsCounter["N"])*100}%")
    print(f"F: {np.average(overallFitsCounter["F"])*100}%")
    print(f"LOD: {np.average(overallFitsCounter["LOD"])*100}%")
    print(f"HOD: {np.average(overallFitsCounter["HOD"])*100}%")

def printSuccessfulFitsForSingleExp(expId):
    
    filename = f"lei_2020_expId={expId}"

    times, positions, orientations, colours = ServiceSavedModel.loadModel(f"{datafileLocation}{filename}.json", loadSwitchValues=False)

    print(len(times))
    n = 5
    k = 1
    overallFits = {'N': [], 'F': [], 'LOD': [], 'HOD': []}
    # check which selection mechanism gets us closest to the new orientation for every agent at every time step
    for t in times:
        if t == times[-1]:
            continue
        for i in range(n):
            orientationI = orientations[t][i]
            nextOrientationI = orientations[t+1][i]

            best = -1
            bestDiff = -1
            for j in range(n):
                if j == i:
                    continue
                newOrientation = orientationI + orientations[t][j]
                diff = math.dist(nextOrientationI, newOrientation)
                if best == -1:
                    best = j
                    bestDiff = diff
                else:
                    if bestDiff > diff:
                        best = j
                        bestDiff = diff
            fits = checkWhichMechanismFits(n, k, i, best, positions[t], orientations[t])
            if fits["N"] == True:
                overallFits["N"].append(t)
            if fits["F"] == True:
                overallFits["F"].append(t)
            if fits["LOD"] == True:
                overallFits["LOD"].append(t)
            if fits["N"] == True:
                overallFits["HOD"].append(t)


    print(f"N: {overallFits["N"]}" )
    print(f"F: {overallFits["F"]}" )
    print(f"LOD: {overallFits["LOD"]}" )
    print(f"HOD: {overallFits["HOD"]}" )


def printOverallFitsCounterIgnoringTurn(startExp, stopExp):
    n = 5
    k = 1
    radius = 0.5
    speed = 0.8
    centerPoint = [1,1]
    
    overallFitsCounter = {'N': [], 'F': [], 'LOD': [], 'HOD': []}
    for expId in range(startExp, stopExp):
        pickedWall = 0
        filename = f"lei_2020_expId={expId}"

        times, positions, orientations, colours = ServiceSavedModel.loadModel(f"{datafileLocation}{filename}.json", loadSwitchValues=False)

        
        fitsCounter = {"N": 0, "F": 0, "LOD": 0, "HOD": 0}
        # check which selection mechanism gets us closest to the new orientation for every agent at every time step
        bestSelectionMechanisms = []
        for t in times:
            if t == times[-1]:
                continue
            bestSelectionMechanismsT = []
            for i in range(n):

                orientationI = orientations[t][i]
                nextOrientationI = orientations[t+1][i]
                newPosition = positions[t][i] + (speed*orientations[t][i])

                if not isInDomain(newPosition, radius, centerPoint):
                    pickedWall += 1
                else:
                    best = -1
                    bestDiff = -1
                    for j in range(5):
                        if j == i:
                            continue
                        newOrientation = orientationI + orientations[t][j]
                        diff = math.dist(nextOrientationI, newOrientation)
                        if best == -1:
                            best = j
                            bestDiff = diff
                        else:
                            if bestDiff > diff:
                                best = j
                                bestDiff = diff
                    fits = checkWhichMechanismFits(n, k, i, best, positions[t], orientations[t])
                    if fits["N"] == True:
                        fitsCounter["N"] = fitsCounter["N"] + 1
                    if fits["F"] == True:
                        fitsCounter["F"] = fitsCounter["F"] + 1
                    if fits["LOD"] == True:
                        fitsCounter["LOD"] = fitsCounter["LOD"] + 1
                    if fits["N"] == True:
                        fitsCounter["HOD"] = fitsCounter["HOD"] + 1

                    bestSelectionMechanismsT.append(fits)
            bestSelectionMechanisms.append(bestSelectionMechanismsT)

        numChoices = n*t-pickedWall
        print(f"expId={expId}, total: {n * t}. num choices: {numChoices}. results:{prettyPrintFitsCounter(fitsCounter, numChoices)}")
        if numChoices > 0:
            overallFitsCounter['N'].append(fitsCounter['N']/numChoices)
            overallFitsCounter['F'].append(fitsCounter['F']/numChoices)
            overallFitsCounter['LOD'].append(fitsCounter['LOD']/numChoices)
            overallFitsCounter['HOD'].append(fitsCounter['HOD']/numChoices)

    print(f"N: {np.round(np.average(overallFitsCounter["N"])*100, 2)}%")
    print(f"F: {np.round(np.average(overallFitsCounter["F"])*100, 2)}%")
    print(f"LOD: {np.round(np.average(overallFitsCounter["LOD"])*100, 2)}%")
    print(f"HOD: {np.round(np.average(overallFitsCounter["HOD"])*100, 2)}%")

printOverallFitsCounterIgnoringTurn(1, 1464)




