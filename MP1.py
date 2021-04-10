import json

blocks = {}
currentBlock = {}


def LoadJSON(name):
    file = open('./Input/' + name)
    data = json.load(file)
    file.close()
    return data


def StartBlocks():
    startBlocks = []
    for key in blocks:
        if blocks[key]['topLevel']:
            startBlocks.append(key)
    return startBlocks


def SubProgram(startBlockRef):
    currentBlockRef = startBlockRef
    subProgram = ""
    while currentBlockRef is not None:
        global currentBlock
        currentBlock = blocks[currentBlockRef]
        subProgram += switcher[currentBlock['opcode']]()
        currentBlockRef = currentBlock['next']
    return subProgram


def Parse(name):
    data = LoadJSON(name)
    global blocks
    blocks = data['targets'][1]['blocks']
    startBlocks = StartBlocks()

    programs = []
    for startBlockRef in startBlocks:
        program = SubProgram(startBlockRef)
        programs.append(program)
    return programs


# MOTION
def MoveSteps():
    return ""


def TurnRight():
    return ""


def TurnLeft():
    return ""


def GotoXY():
    return ""


def ChangeXBy():
    return ""


def SetX():
    return ""


def ChangeYBy():
    inputs = currentBlock['inputs']
    yInput = inputs['DY'][1][1]
    return "CHANGE Y BY " + yInput + "\n"


def SetY():
    inputs = currentBlock['inputs']
    yInput = inputs['Y'][1][1]
    return "SET Y " + yInput + "\n"


# LOOKS
def Say():
    return ""


def SayForSecs():
    return ""


def Think():
    return ""


def ThinkForSecs():
    return ""


# EVENT
def WhenFlagClicked():
    return ""


def WhenKeyPressed():
    return ""


# CONTROL
def Forever():
    return ""


def If():
    return ""


def IfElse():
    return ""


def Repeat():
    return ""


def Wait():
    return ""


def WaitUntil():
    return ""


def RepeatUntil():
    return ""


switcher = {
    "motion_movesteps": MoveSteps,
    "motion_turnright": TurnRight,
    "motion_turnleft": TurnLeft,
    "motion_gotoxy": GotoXY,
    "motion_changexby": ChangeXBy,
    "motion_setx": SetX,
    "motion_changeyby": ChangeYBy,
    "motion_sety": SetY,

    "looks_say": Say,
    "looks_sayforsecs": SayForSecs,
    "looks_think": Think,
    "looks_thinkforsecs": ThinkForSecs,

    "event_whenflagclicked": WhenFlagClicked,
    "event_whenkeypressed": WhenKeyPressed,

    "control_forever": Forever,
    "control_if": If,
    "control_if_else": IfElse,
    "control_repeat": Repeat,
    "control_wait": Wait,
    "control_wait_until": WaitUntil,
    "control_repeat_until": RepeatUntil,
}

myPrograms = Parse('project.json')
print(myPrograms)