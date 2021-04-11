import json

blocks = {}
currentBlock = {}


def LoadJSON(name):
    file = open('project.json')
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
    return "Move" + Direction + " " + str(abs(Number_Of_Steps)) +'\n'

def TurnRight():
    return "TurnRight " + currentBlock["inputs"]["DEGREES"][1][1] + "\n"


def TurnLeft():
    return "TurnLeft " + currentBlock["inputs"]["DEGREES"][1][1] + "\n"


def GotoXY():
    # Get X-Coordinate
    X = float(currentBlock["inputs"]["X"][1][1])
    # Get Y-Coordinate
    Y = float(currentBlock["inputs"]["Y"][1][1])
    # Return Corresponding Pseudocode. 
    return "GoToXY "+str(X)+","+str(Y)+"\n"

def ChangeXBy():
    return "ChangeXBY " + currentBlock["inputs"]["DX"][1][1] +"\n"


def SetX():
    return "SetX " + currentBlock["inputs"]["X"][1][1] +"\n"


def ChangeYBy():
    inputs = currentBlock['inputs']
    yInput = inputs['DY'][1][1]
    return "ChangeYBY " + yInput + "\n"

def SetY():
    inputs = currentBlock['inputs']
    yInput = inputs['Y'][1][1]
    return "SetY " + yInput + "\n"


# LOOKS
def Say():
    return "Say " + currentBlock["inputs"]["MESSAGE"][1][1] + "\n"


def SayForSecs():
    return "SayFOR " + currentBlock["inputs"]["MESSAGE"][1][1] + " ; " + currentBlock["inputs"]["SECS"][1][1] + "\n"


def Think():
    return "Think " + currentBlock["inputs"]["MESSAGE"][1][1] + "\n"


def ThinkForSecs():
    return "ThinkFOR " + currentBlock["inputs"]["MESSAGE"][1][1] + " ; " + currentBlock["inputs"]["SECS"][1][1] + "\n"


# EVENT
def WhenFlagClicked():
    return "OnFlagClicked\n"


def WhenKeyPressed():
    return "OnPress " + currentBlock["fields"]["KEY_OPTION"][0] + "\n"


# CONTROL
def Forever():
    contentRepeating = SubProgram(currentBlock["inputs"]["SUBSTACK"][1])
    return "Forever "+ contentRepeating + "\n"


def If():
    global currentBlock
    currentBlockTmp = currentBlock
    condition = SubProgram(currentBlock["inputs"]["CONDITION"][1])
    currentBlock = currentBlockTmp
    thenPart = SubProgram(currentBlock["inputs"]["SUBSTACK"][1])
    return "If "+ condition + "Then\n" + thenPart 


def IfElse():
    global currentBlock
    currentBlockTmp = currentBlock
    condition = SubProgram(currentBlock["inputs"]["CONDITION"][1])
    currentBlock = currentBlockTmp
    thenPart = SubProgram(currentBlock["inputs"]["SUBSTACK"][1])
    currentBlock = currentBlockTmp
    elsePart = SubProgram(currentBlock["inputs"]["SUBSTACK2"][1])
    return "IfElse "+ condition + "Then\n " + thenPart +"Else\n"+ elsePart


def Repeat():
    numOfRepetitions = currentBlock["inputs"]["TIMES"][1][1]
    contentRepeating = SubProgram(currentBlock["inputs"]["SUBSTACK"][1])
    return "Repeat "+ contentRepeating + " ; " + numOfRepetitions + "\n"


def Wait():
    # Get Number of Seconds.
    Seconds = float(currentBlock["inputs"]["DURATION"][1][1])
    # Return Corresponding Pseudocode. 
    return "Wait "+str(Seconds)+"\n"


def WaitUntil():
    condition = SubProgram(currentBlock["inputs"]["CONDITION"][1])
    return "WaitUntill "+ condition + "\n"


def RepeatUntil():
    global currentBlock
    currentBlockTmp = currentBlock
    condition = SubProgram(currentBlock["inputs"]["CONDITION"][1])
    currentBlock = currentBlockTmp
    contentRepeating = SubProgram(currentBlock["inputs"]["SUBSTACK"][1])
    return "RepeatUntill  "+ contentRepeating + " ; " + condition + "\n"


# OPERATORS
def GreaterThanOp():
    operand1 = currentBlock["inputs"]["OPERAND1"][1][1]
    operand2 = currentBlock["inputs"]["OPERAND2"][1][1]
    return "( "+ str(operand1) + " ) > ( " + str(operand2) + " )\n"
    # return ""

def LessThanOp():
    operand1 = currentBlock["inputs"]["OPERAND1"][1][1]
    operand2 = currentBlock["inputs"]["OPERAND2"][1][1]
    return "( "+ str(operand1) + " ) < ( " + str(operand2) + " )\n"
    # return ""


def EqualsOp():
    operand1 = currentBlock["inputs"]["OPERAND1"][1][1]
    operand2 = currentBlock["inputs"]["OPERAND2"][1][1]
    return "( "+ str(operand1) + " ) = ( " + str(operand2) + " )\n"
    # return ""


def NotOp():
  return "Not ("+ SubProgram(currentBlock["inputs"]["OPERAND"][1]) +")\n"
  # return ""


def OrOp():
    global currentBlock
    currentBlockTmp = currentBlock
    operand1 = SubProgram(currentBlock["inputs"]["OPERAND1"][1])
    currentBlock = currentBlockTmp
    operand2 = SubProgram(currentBlock["inputs"]["OPERAND2"][1])
    return "( "+ operand1 + " ) OR ( " + operand2 + ")\n"
    # return ""


def AndOp():
    global currentBlock
    currentBlockTmp = currentBlock
    operand1 = SubProgram(currentBlock["inputs"]["OPERAND1"][1])
    currentBlock = currentBlockTmp
    operand2 = SubProgram(currentBlock["inputs"]["OPERAND2"][1])
    return "( "+ operand1 + " ) AND ( " + operand2 + ")\n"
    # return ""



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
    "operator_gt" : GreaterThanOp,
    "operator_lt" : LessThanOp,
    "operator_equals" : EqualsOp,
    "operator_not" : NotOp,
    "operator_or" : OrOp,
    "operator_and" : AndOp,
}

myPrograms = Parse('project.json')
print(myPrograms)
