
import math
import numpy as np
import codecs, json

import ServiceSavedModel

datafileLocation = ""

n = 5
speeds = {}
for expId in range(1, 1465):
    filename = f"lei_2020_extracted_data/lei_2020_expId={expId}"
    timesExp, positionsExp, orientationsExp, coloursExp = ServiceSavedModel.loadModel(f"{datafileLocation}{filename}.json", loadSwitchValues=False)
    distances = []
    for t in timesExp:
        if t == timesExp[-1]:
            continue
        for i in range(n):
            distances.append(math.dist(positionsExp[t][i], positionsExp[t+1][i]))

    speed = np.average(distances)
    print(f"{expId}: {speed}")
    speeds[expId] = speed

path = "lei_2020_speeds.json"
with open(path, "w") as outfile:
        json.dump(speeds, outfile)

    
