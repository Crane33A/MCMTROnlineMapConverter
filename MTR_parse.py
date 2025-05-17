import json,sys
from math import floor,ceil
import svgwrite
dwg=svgwrite.Drawing('trial.svg')
def inArea(plotSet,plot):
    if plotSet[0][0]<=plot[0]<=plotSet[1][0] and plotSet[0][1]<=plot[1]<=plotSet[1][1]:
        return True
    else:
        return False
minNetLen=50
convertDistance=20
with open('MTR.json','r',encoding='utf-8') as f:
    railMap=json.load(f)[0]
stations=railMap['stations']
stationPlotList=[]
plotToID=dict([((stations[stationID]['x'],stations[stationID]['z']),stationID) for stationID in stations])
xList=[]
zList=[]
for stationID in stations:
    xList.append(stations[stationID]['x'])
    zList.append(stations[stationID]['z'])
    stationPlotList.append((stations[stationID]['x'],stations[stationID]['z']))
xMin=min(xList);xMax=max(xList)
zMin=min(zList);zMax=max(zList)

xNetMin=(floor(xMin/minNetLen)-1)*minNetLen;xNetMax=(ceil(xMax/minNetLen)+1)*minNetLen
zNetMin=(floor(zMin/minNetLen)-1)*minNetLen;zNetMax=(ceil(zMax/minNetLen)+1)*minNetLen

xWidthList=dict([(x,minNetLen) for x in range(xNetMin,xNetMax,minNetLen)])
zWidthList=dict([(z,minNetLen) for z in range(zNetMin,zNetMax,minNetLen)])

Net=dict([(((x,z),(x+minNetLen,z+minNetLen)),[]) for x in range(xNetMin,xNetMax,minNetLen) for z in range(zNetMin,zNetMax,minNetLen)])

for stationPlot in stationPlotList:
    blockX_1=floor(stationPlot[0]/minNetLen)*minNetLen
    blockX_2=blockX_1+minNetLen
    blockZ_1=floor(stationPlot[1]/minNetLen)*minNetLen
    blockZ_2=blockZ_1+minNetLen
    Net[((blockX_1,blockZ_1),(blockX_2,blockZ_2))].append(plotToID[stationPlot])

while True:
    xMerge=False
    for i in range(1,len(xWidthList)):
        x=sorted(xWidthList.keys())[i]
        canBeMerged=True
        for z in zWidthList.keys():
            if Net[((x,z),(x+xWidthList[x],z+zWidthList[z]))]:
                canBeMerged=False
                break
        if canBeMerged:
            xFormer=sorted(xWidthList.keys())[i-1]
            for z in zWidthList.copy():
                Net[((xFormer,z),(x+xWidthList[x],z+zWidthList[z]))]=Net[((xFormer,z),(xFormer+xWidthList[xFormer],z+zWidthList[z]))]+Net[((x,z),(x+xWidthList[x],z+zWidthList[z]))]
                del Net[((xFormer,z),(xFormer+xWidthList[xFormer],z+zWidthList[z]))]
                del Net[((x,z),(x+xWidthList[x],z+zWidthList[z]))]
            xWidthList[xFormer]+=xWidthList[x]
            del xWidthList[x]
            xMerge=True
            break
    if not xMerge:break
print(xWidthList)
while True:
    zMerge=False
    for i in range(1,len(zWidthList)):
        z=sorted(zWidthList.keys())[i]
        canBeMerged=True
        for x in xWidthList.keys():
            if Net[((x,z),(x+xWidthList[x],z+zWidthList[z]))]:
                canBeMerged=False
                break
        if canBeMerged:
            zFormer=sorted(zWidthList.keys())[i-1]
            for x in xWidthList.copy():
                Net[((x,zFormer),(x+xWidthList[x],z+zWidthList[z]))]=Net[((x,zFormer),(x+xWidthList[x],zFormer+zWidthList[zFormer]))]+Net[((x,z),(x+xWidthList[x],z+zWidthList[z]))]
                del Net[((x,zFormer),(x+xWidthList[x],zFormer+zWidthList[zFormer]))]
                del Net[((x,z),(x+xWidthList[x],z+zWidthList[z]))]
            zWidthList[zFormer]+=zWidthList[z]
            del zWidthList[z]
            zMerge=True
            break
    if not zMerge:break
print(zWidthList)

xConverted=dict([(sorted(xWidthList.keys())[i],i*convertDistance) for i in range(len(xWidthList))])
zConverted=dict([(sorted(zWidthList.keys())[i],i*convertDistance) for i in range(len(zWidthList))])

'''for i in Net:
    x_1=i[0][0]
    z_1=i[0][1]
    x_2=i[1][0]
    z_2=i[1][1]
    if Net[i]:
        print(i,'->',Net[i])
    #dwg.add(dwg.rect(insert=(x_1,z_1),size=(x_2-x_1,z_2-z_1),fill='white'))
for stationPlot in stationPlotList:
    dwg.add(dwg.circle(center=(stationPlot[0],stationPlot[1]),r=5,fill='red'))'''
for i in Net:
    x_1=i[0][0]
    z_1=i[0][1]
    x_2=i[1][0]
    z_2=i[1][1]
    if Net[i]:
        dwg.add(dwg.circle(center=(xConverted[x_1],zConverted[z_1]),r=5,fill='red'))
dwg.save()