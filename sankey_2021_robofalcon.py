import rdata

#result = pyreadr.read_r('data/ALLrobofalcon-data.rda')
converted = rdata.read_rda('data/Sankey_2021_robofalcon/ALLrobofalcon-data.rda')
#converted = rdata.read_rda("data/Sankey_2021_robofalcon/names-list.rda")
#print(result.keys())
print("test")
print(converted["dat"].keys())
print(converted["dat"].head())
print(converted["dat"].tail())

print(converted["dat"].count())

#print(converted["dat"][converted["dat"]["unique.flight"] == 1.0])

"""
Columns
condition, small.big, ind.flight, wind.direct.site, group.num, wind.speed.site, flight.time, 
Date, pigeon, speed, support.wind, cross.wind, focal_head, diff_head, lon, lat, dist2cent, turn2home, turn2falcpos, turn2falchead, dist2pred, dist2home, 
nn1cent - nn33cent, nn1head - nn33head, nn1futr - nn33futrm, nn1dist, dist2site, unique.flight, study.flight
"""