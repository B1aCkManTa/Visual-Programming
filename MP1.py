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
    # Get Number of Steps.
    Number_Of_Steps = float(currentBlock["inputs"]["STEPS"][1][1])
    # Get Direction based on Positive/Negative.
    Direction = "Backward" if (Number_Of_Steps <0) else "Forward"
    # Return Corresponding Pseudocode. 
    return ("Move(" + str(abs(Number_Of_Steps)) + "," + Direction)+')'

def TurnRight():
    return ""


def TurnLeft():
    return ""


def GotoXY():
    # Get X-Coordinate
    X = float(currentBlock["inputs"]["X"][1][1])
    # Get Y-Coordinate
    Y = float(currentBlock["inputs"]["Y"][1][1])
    # Return Corresponding Pseudocode. 
    return "GoToXY("+str(X)+","+str(Y)+")"

def ChangeXBy():
    return ""


def SetX():
    return ""


def ChangeYBy():
    return ""


def SetY():
    return ""


# LOOKS
def Say():
    return "SAY " + currentBlock["inputs"]["MESSAGE"][1][1] + "\n"


def SayForSecs():
    return "SAY " + currentBlock["inputs"]["MESSAGE"][1][1] + " FOR " + currentBlock["inputs"]["SECS"][1][1] + " SECS\n"


def Think():
    return ""


def ThinkForSecs():
    return ""


# EVENT
def WhenFlagClicked():
    return ""


def WhenKeyPressed():
    return "ON " + currentBlock["fields"]["KEY_OPTION"][0] + " PRESS\n"


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
    # Get Number of Seconds.
    Seconds = float(currentBlock["inputs"]["DURATION"][1][1])
    # Return Corresponding Pseudocode. 
    return "Wait("+str(Seconds)+")"


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
