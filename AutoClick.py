import os
import sys
import pyautogui
from pyclick import HumanClicker
import random
import json
import time
from enum import Enum

# window size 960*540 noxplayer


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class WindowSize(Enum):
    width = 960
    hight = 540


class StepType(Enum):
    ImgClick = 1
    BiasImgClick = 2
    ImgCheckRandomClick = 3
    mixSteps = 4
    Drag = 5
    ImgDetectClick = 6
    ImgDetectDrag = 7
    randomWait = 8
    Nope = 9


class DragType(Enum):
    rightToLeft = 1
    leftToRight = 2
    downToTop = 3
    topToDown = 4


class ImgType(Enum):
    nox = 1


class ImgStorage():
    imgUrls = {}

    @classmethod
    def init(cls, config):
        for item in config["imgType"]:
            cls.imgUrls[item["name"]] = resource_path(item["imgPath"])
    # get img url
    @classmethod
    def get(cls, cmd):
        if isinstance(cmd, ImgType):
            cmd = cmd.name
        return cls.imgUrls[cmd]


class MyRandom():
    @staticmethod
    def fkRand():
        num = random.randint(0, 3)
        return num == 0

    @staticmethod
    def clickRand(num):
        return num + random.uniform(-15, 15)

    @staticmethod
    def dragRand(num):
        return int(num + random.randint(-30, 30))

    @staticmethod
    def smallDragRand(num):
        return int(num + random.randint(-10, 10))

    @staticmethod
    def dragTimeRand(num):
        return num + random.uniform(0, 0.5)

    @staticmethod
    def timerand(num):
        return num + random.uniform(0, 0.5)

    @staticmethod
    def randomWaitRand():
        return random.uniform(0, 3)

        

    @staticmethod
    def halfWidthRand(num):
        return int(num + random.randint(50, WindowSize.width.value/2 - 120))

    @staticmethod
    def halfHightRand(num):
        return int(num + random.randint(50,  WindowSize.hight.value/2 - 120))

    @staticmethod
    def widthRand(num):
        return int(num + random.randint(300, WindowSize.width.value - 200))

    @staticmethod
    def hightRand(num):
        return int(num + random.randint(250,  WindowSize.hight.value - 170))


class MouseClick():
    hc = None

    @classmethod
    def init(cls):
        cls.hc = HumanClicker()

    @classmethod
    def click(cls, x, y):
        newX = MyRandom.clickRand(x)
        newY = MyRandom.clickRand(y)
        pyautogui.click(newX, newY)

    @classmethod
    def imgDetect(cls, step):
        imgUrl = ImgStorage.get(step.cmd)
        isFound = True
        x = 0
        y = 0
        try:
            x, y = pyautogui.locateCenterOnScreen(
                imgUrl, confidence=step.confidence, grayscale=step.grayscale)
        except:

            isFound = False
        return isFound, x, y

    @classmethod
    def imgDetectMust(cls, stop, step):
        imgUrl = ImgStorage.get(step.cmd)
        isFound = False
        canClick = True
        x = 0
        y = 0
        while not isFound:
            isFound, x, y = cls.imgDetect(step)

            if not isFound:
                if not step.must or stop():
                    canClick = False
                    break
                time.sleep(MyRandom.timerand(1))
        return (x, y), canClick

    @classmethod
    def singleClick(cls, pos, bias=(0, 0)):
        cls.click(pos[0]+bias[0], pos[1]+bias[1])

    @classmethod
    def randomClick(cls):
        x, y = cls.getStartPos()
        cls.click(MyRandom.widthRand(x), MyRandom.hightRand(y))

    @classmethod
    def getStartPos(cls):
        imgUrl = ImgStorage.get(ImgType.nox)
        location = pyautogui.locateOnScreen(imgUrl, confidence=0.8)
        return location.left, location.top

    @classmethod
    def singleDrag(cls, point1, point2, dragTime=1):
        pyautogui.moveTo(point1[0], point1[1])
        pyautogui.mouseDown(button='left')
        time.sleep(MyRandom.dragTimeRand(0))
        cls.hc.move(point2, MyRandom.dragTimeRand(dragTime))
        time.sleep(MyRandom.dragTimeRand(0))
        pyautogui.mouseUp(button='left')

    @classmethod
    def mouseDrag(cls, step):
        dType = step.cmd
        ratio = step.ratio
        dragType = DragType[dType]
        x, y = cls.getStartPos()
        if dragType == DragType.rightToLeft:
            x1 = MyRandom.dragRand(x + 80)
            y1 = MyRandom.dragRand(MyRandom.hightRand(y))
            x2 = MyRandom.dragRand(x + 500*ratio)
            y2 = MyRandom.dragRand(y1)
            cls.singleDrag((x2, y2), (x1, y2))
        elif dragType == DragType.leftToRight:
            x1 = MyRandom.dragRand(x + 80)
            y1 = MyRandom.dragRand(MyRandom.hightRand(y))
            x2 = MyRandom.dragRand(x + 500*ratio)
            y2 = MyRandom.dragRand(y1)
            cls.singleDrag((x1, y2), (x2, y2))
        elif dragType == DragType.downToTop:
            x1 = MyRandom.dragRand(MyRandom.widthRand(x))
            y1 = MyRandom.dragRand(y + WindowSize.hight.value*ratio-100)
            x2 = MyRandom.dragRand(x1)
            y2 = MyRandom.dragRand(y+120)
            cls.singleDrag((x1, y1), (x2, y2))
        elif dragType == DragType.topToDown:
            x1 = MyRandom.dragRand(MyRandom.widthRand(x))
            y1 = MyRandom.dragRand(y + WindowSize.hight.value*ratio-100)
            x2 = MyRandom.dragRand(x1)
            y2 = MyRandom.dragRand(y+120)
            cls.singleDrag((x2, y2), (x1, y1))

    @classmethod
    def randomDrag(cls):
        x, y = cls.getStartPos()
        x1 = MyRandom.dragRand(x + WindowSize.width.value/2)
        y1 = MyRandom.dragRand(y + WindowSize.hight.value/2)
        x2 = MyRandom.halfWidthRand(x1)
        y2 = MyRandom.halfHightRand(y1)
        cls.singleDrag((x1, y1), (x2, y2), 0.5)
        time.sleep(MyRandom.timerand(1))
        cls.singleDrag((MyRandom.smallDragRand(x2), MyRandom.smallDragRand(y2)),
                       (MyRandom.smallDragRand(x1), MyRandom.smallDragRand(y1)), 0.5)


class Step():
    confidence = 0.8
    times = 1
    ratio = 1
    bias = (0, 0)
    waitTime = 0.5
    clickDelay = 0
    delay = None
    grayscale = False
    must = True

    def __init__(self, jsonObj):
        self.type = StepType[jsonObj["type"]]
        self.cmd = jsonObj["cmd"]
        if "confidence" in jsonObj:
            self.confidence = jsonObj["confidence"]
        if "biasX" in jsonObj and "biasY" in jsonObj:
            self.bias = (jsonObj["biasX"], jsonObj["biasY"])
        if "times" in jsonObj:
            self.times = jsonObj["times"]
        if "waitTime" in jsonObj:
            self.waitTime = jsonObj["waitTime"]
        if "delay" in jsonObj:
            self.delay = jsonObj["delay"]
        if "grayscale" in jsonObj:
            self.grayscale = jsonObj["grayscale"]
        if "imgCmd" in jsonObj:
            self.imgCmd = jsonObj["imgCmd"]
        if "ratio" in jsonObj:
            self.ratio = jsonObj["ratio"]
        if "must" in jsonObj:
            self.must = jsonObj["must"]
        if "clickDelay" in jsonObj:
            self.clickDelay = jsonObj["clickDelay"]

    def detectImgThenClick(self, stop, isRandomClick=False):

        pos, canClick = MouseClick.imgDetectMust(stop, self)
        if self.clickDelay > 0:
            time.sleep(MyRandom.timerand(self.clickDelay))

        if canClick:
            if isRandomClick:
                MouseClick.randomClick()
            else:
                MouseClick.singleClick(pos, self.bias)

    def singleAct(self, stop):

        if self.type == StepType.ImgClick:
            self.detectImgThenClick(stop)
        elif self.type == StepType.ImgDetectClick:
            MouseClick.imgDetectMust(stop, self)
            self.detectImgThenClick(stop)

        elif self.type == StepType.BiasImgClick:
            self.detectImgThenClick(stop)
        elif self.type == StepType.ImgCheckRandomClick:
            self.detectImgThenClick(stop, isRandomClick=True)
        elif self.type == StepType.Drag:
            MouseClick.mouseDrag(self)
            if MyRandom.fkRand():
                MouseClick.randomDrag()
        elif self.type == StepType.ImgDetectDrag:
            MouseClick.imgDetectMust(stop, self)
            MouseClick.mouseDrag(self)
            if MyRandom.fkRand():
                MouseClick.randomDrag()
        elif self.type == StepType.ImgDetectDrag:
            MouseClick.mouseDrag(self)
            if MyRandom.fkRand():
                MouseClick.randomDrag()
        elif self.type == StepType.randomWait:
             time.sleep(MyRandom.randomWaitRand())
            

        if stop():
            return
        print("act:%s" % self.cmd)
        time.sleep(MyRandom.timerand(self.waitTime))

    def act(self, stop):
        if self.delay != None:
            time.sleep(MyRandom.timerand(self.delay))
        for _ in range(self.times):
            self.singleAct(stop)
            if stop():
                return


class Process():
    steps = []

    def __init__(self):
        MouseClick.init()
        self.configInit()

    def configInit(self):
        with open(resource_path('config.json')) as f:
            config = json.load(f)
        ImgStorage.init(config)
        for item in config["steps"]:
            step = Step(item)
            if step.type == StepType.mixSteps:
                for mixSteps in config["mixSteps"][step.cmd]:
                    mixStep = Step(mixSteps)
                    self.steps.append(mixStep)

            else:
                self.steps.append(step)

    def start(self, stop):
        while True:
            for step in self.steps:
                step.act(stop)
                if stop():
                    return
