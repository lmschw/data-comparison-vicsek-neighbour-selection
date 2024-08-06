import codecs, json
import numpy as np
"""
Service contains static methods to save and load models to/from json files.
"""

def saveModel(simulationData, colours, path="sample.json", modelParams=None, saveInterval=1, modes=None, switchValues=None):
    """
    Saves a model trained by the Viscek simulator implementation.

    Parameters:
        - simulationData (times, positions, orientations): the data to be saved
        - colours (array of arrays of strings): the colour assigned to each particle at every timestep
        - path (string) [optional]: the location and name of the target file
        - modelParams (dict) [optional]: a summary of the model's params such as n, k, neighbourSelectionMode etc.
        - saveInterval (int) [optional]: specifies the interval at which the saving should occur, i.e. if any time steps should be skipped
        - switchValues (array) [optional]: the switch type value assigned to each particle at every timestep
        
    Returns:
        Nothing. Creates or overwrites a file.
    """
    time, positions, orientations = simulationData
    dict = {"time": __getSpecifiedIntervals(saveInterval, time), 
            "positions": __getSpecifiedIntervals(saveInterval, positions.tolist()), 
            "orientations": __getSpecifiedIntervals(saveInterval, orientations.tolist()), 
            "colours": __getSpecifiedIntervals(saveInterval, colours)}
    # TODO check if modes is ever used and what its intention was
    if modes != None:
        dict["modes"] = modes
    if switchValues != None:
        dict["switchValues"] = switchValues
    __saveDict(path, dict, modelParams)

def loadModel(path, loadSwitchValues=False):
    """
    Loads a single model from a single file.

    Parameters:
        - path (string): the location and file name of the file containing the model data
        - loadSwitchValues (boolean) [optional]: loads the switch type values from the save file

    Returns:
        The model's params as well as the simulation data containing the time, positions, orientations and colours.
    """
    loadedJson = __loadJson(path)

    time = np.array(loadedJson["time"])
    positions = np.array(loadedJson["positions"])
    orientations = np.array(loadedJson["orientations"])
    colours = np.array(loadedJson["colours"])
    if loadSwitchValues == True:
        switchValues = np.array(loadedJson["switchValues"])
        return time, positions, orientations, colours, switchValues
    return time, positions, orientations, colours

def loadModels(paths, loadSwitchValues=False):
    """
    Loads multiple models from multiple files.

    Parameters:
        - paths (array of strings): An array containing the locations and names of the files containing a single model each
        - loadSwitchValues (boolean) [optional]: loads the switch type values from the save files
        
    Returns:
        Returns an array containing the model params for each model and a second array containing the simulation data for each model. Co-indexed.
    """
    data = []
    params = []
    coloursArr = []
    switchValuesArr = []
    for path in paths:
        if loadSwitchValues == True:
            modelParams, simulationData, colours, switchValues = loadModel(path, loadSwitchValues=loadSwitchValues)
            params.append(modelParams)
            data.append(simulationData)
            coloursArr.append(colours)
            switchValuesArr.append(switchValues)
        else:
            modelParams, simulationData, colours = loadModel(path, loadSwitchValues=loadSwitchValues)
            params.append(modelParams)
            data.append(simulationData)
            coloursArr.append(colours)
    if loadSwitchValues == True:
        return params, data, coloursArr, switchValuesArr
    return params, data, coloursArr

def saveTimestepsResults(results, path, modelParams=None, saveInterval=1):
    """
    Saves evaluator results for all timesteps.

    Parameters:
        - results (dictionary): the evaluation results per timestep
        - path (string): the location and name of the target file
        - modelParams (dict) [optional]: a summary of the model's params such as n, k, neighbourSelectionMode etc.
        - saveInterval (int) [optional]: specifies the interval at which the saving should occur, i.e. if any time steps should be skipped
    
    Returns:
        Nothing. Creates or overwrites a file.
    """
    dict = {"time": __getSpecifiedIntervals(saveInterval, list(results.keys())),
            "results": __getSpecifiedIntervals(saveInterval, list(results.values()))}
    __saveDict(path, dict, modelParams)

def loadTimestepsResults(path):
    """
    Loads the evaluation results from a single file.

    Parameters:
        - path (string): the location and file name of the file containing the model data

    Returns:
        The model's params as well as the evaluation data as a {time: results} dictionary
    """
    loadedJson = __loadJson(path)
    modelParams = loadedJson["modelParams"]
    time = np.array(loadedJson["time"])
    results = np.array(loadedJson["results"])
    data = {time[i]: results[i] for i in range(len(time))}
    return modelParams, data

def saveConnectionTrackingInformation(data, path="sample.json"):
    """
    Saves a model trained by the Viscek simulator implementation.

    Parameters:
        - data (dict): the data to be saved
        - path (string) [optional]: the location and name of the target file
        - saveInterval (int) [optional]: specifies the interval at which the saving should occur, i.e. if any time steps should be skipped
        
    Returns:
        Nothing. Creates or overwrites a file.
    """
    __saveDict(path, data)

def loadConnectionTrackingInformation(path):
    """
    Loads a single model from a single file.

    Parameters:
        - path (string): the location and file name of the file containing the model data
        - loadSwitchValues (boolean) [optional]: loads the switch type values from the save file

    Returns:
        The model's params as well as the simulation data containing the time, positions, orientations and colours.
    """
    loadedJson = __loadJson(path)

    neighbours = loadedJson["neighbours"]
    distances = loadedJson["distances"]
    localOrders = loadedJson["localOrders"]
    orientationDifferences = loadedJson["orientationDifferences"]
    selected = loadedJson["selected"]
    return neighbours, distances, localOrders, orientationDifferences, selected

def loadConnectionTrackingInformations(paths):
    """
    Loads multiple instances of connection tracking information from multiple files.

    Parameters:
        - paths (array of strings): An array containing the locations and names of the files containing a single model each
        
    Returns:
        Returns an array containing the model params for each model and a second array containing the simulation data for each model. Co-indexed.
    """
    neighbours = []
    distances = []
    localOrders = []
    orientationDifferences = []
    selected = []
    for path in paths:
        neighs, dists, los, ods, sels = loadConnectionTrackingInformation(path)
        neighbours.append(neighs)
        distances.append(dists)
        localOrders.append(los)
        orientationDifferences.append(ods)
        selected.append(sels)
    return neighbours, distances, localOrders, orientationDifferences, selected
    
    
def __getSpecifiedIntervals(interval, lst):
    """
    Selects the data within the list which coincides with the specified interval, e.g. every third data point.

    Parameters:
        - interval (int): which data points should be considered, e.g. 3 would indicate indices 0, 3, 6 etc.
        - lst (list): the data to be reduced according to the intervals
    
    Returns:
        A reduced list containing only the data points of the original list at the specified intervals.
    """
    return [lst[idx] for idx in range(0, len(lst)) if idx % interval == 0]

def __saveDict(path, dict, modelParams=None):
    """
    Saves the values of a dictionary to a file at the specified path.

    Parameters:
        - path (string): the location and name of the target file
        - dict (dictionary): the dictionary containing the data to be saved
        - modelParams (dict) [optional]: a summary of the model's params such as n, k, neighbourSelectionMode etc.

    Returns:
        Nothing. Creates or overwrites a file.
    """
    if modelParams != None:
        paramsDict = {"modelParams": modelParams}
        paramsDict.update(dict)
        dict = paramsDict
        
    with open(path, "w") as outfile:
        json.dump(dict, outfile)

def __loadJson(path):
    """
    Loads data as JSON from a single file.

    Parameters:
        - path (string): the location and file name of the file containing the data

    Returns:
        All the data from the file as JSON.
    """
    obj_text = codecs.open(path, 'r', encoding='utf-8').read()
    return json.loads(obj_text)
