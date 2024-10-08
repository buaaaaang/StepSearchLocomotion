import numpy as np

from transformationUtil import *
from pygameScene import pygameScene
from dataGenerater import dataGenerater
from inertializationManager import inertializationManager


folderPaths = ["./walkingData"]
idleFilePath = "./idleData"
dataFtn = dataGenerater(
    folderPaths, idleFilePath, rotationInterpolation=5, translationInterpolation=7
)
file = dataFtn.file

scene = pygameScene(frameTime=file.frameTime, speed=200)
manager = inertializationManager(
    file,
    dataFtn.getNextData,
    halfLife=0.15,
    handleContact=True,
    unlockRadius=30,
    compare=False,
)

isMoving = False

while scene.running:
    cameraCenter = scene.cameraCenter.copy()
    scene.highLightPoint = cameraCenter
    cameraCenter[1] = 0
    position = toCartesian(dataFtn.currentJointsPosition[0])
    position[1] = 0
    direction = cameraCenter - position
    distance = np.linalg.norm(cameraCenter - position)
    if isMoving:
        isMoving = scene.controlIsMoving or (distance > 40)
    else:
        isMoving = scene.controlIsMoving
    dataFtn.setObjective(direction, isMoving)
    scene.updateScene(manager.getNextSceneInput())
