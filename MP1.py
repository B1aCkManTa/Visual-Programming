import json
from re import sub

blocks = {}
currentBlock = {}
isGreenFlagEvent = False


def LoadJSON():
    file = open('project_test3.json')
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
    global isGreenFlagEvent
    currentBlockRef = startBlockRef
    subProgram = ""
    while currentBlockRef is not None:
        global currentBlock
        currentBlock = blocks[currentBlockRef]
        subProgram += switcher[currentBlock['opcode']]()
        currentBlockRef = currentBlock['next']
    if isGreenFlagEvent:
        subProgram += "End"
    isGreenFlagEvent = False
    return subProgram


def Parse():
    data = LoadJSON()
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
    Number_Of_Steps = "0" if (currentBlock['inputs']['STEPS'][1][1] == "") else currentBlock['inputs']['STEPS'][1][1]
    Number_Of_Steps = float(Number_Of_Steps)
    Direction = "Backward" if (Number_Of_Steps < 0) else "Forward"
    return "MoveSteps;" + Direction + ";" + str(abs(Number_Of_Steps)) + '\n'


def TurnRight():
    value = "0" if (currentBlock['inputs']['DEGREES'][1][1] == "") else currentBlock['inputs']['DEGREES'][1][1]
    return "TurnRight;" + value + "\n"


def TurnLeft():
    value = "0" if (currentBlock['inputs']['DEGREES'][1][1] == "") else currentBlock['inputs']['DEGREES'][1][1]
    return "TurnLeft;" + value + "\n"


def GotoXY():
    valueX = "0" if (currentBlock['inputs']['X'][1][1] == "") else currentBlock['inputs']['X'][1][1]
    valueY = "0" if (currentBlock['inputs']['Y'][1][1] == "") else currentBlock['inputs']['Y'][1][1]
    return "GoToXY;" + valueX + ";" + valueY + "\n"


def ChangeXBy():
    value = "0" if (currentBlock['inputs']['DX'][1][1] == "") else currentBlock['inputs']['DX'][1][1]
    return "ChangeXBY;" + value + "\n"


def SetX():
    value = "0" if (currentBlock['inputs']['X'][1][1] == "") else currentBlock['inputs']['X'][1][1]
    return "SetX;" + value + "\n"


def ChangeYBy():
    value = "0" if (currentBlock['inputs']['DY'][1][1] == "") else currentBlock['inputs']['DY'][1][1]
    return "ChangeYBY;" + value + "\n"


def SetY():
    value = "0" if (currentBlock['inputs']['Y'][1][1] == "") else currentBlock['inputs']['Y'][1][1]
    return "SetY;" + value + "\n"


# LOOKS
def Say():
    return "Say;" + currentBlock["inputs"]["MESSAGE"][1][1] + "\n"


def SayForSecs():
    duration = "0" if (currentBlock["inputs"]["SECS"][1][1] == "") else currentBlock["inputs"]["SECS"][1][1]
    return "SayForSecs;" + currentBlock["inputs"]["MESSAGE"][1][1] + ";" + duration + "\n"


def Think():
    return "Think;" + currentBlock["inputs"]["MESSAGE"][1][1] + "\n"


def ThinkForSecs():
    duration = "0" if (currentBlock["inputs"]["SECS"][1][1] == "") else currentBlock["inputs"]["SECS"][1][1]
    return "ThinkForSecs;" + currentBlock["inputs"]["MESSAGE"][1][1] + ";" + duration + "\n"


# EVENT
def WhenFlagClicked():
    global isGreenFlagEvent
    isGreenFlagEvent = True
    return "WhenFlagClicked\nBegin\n"


def WhenKeyPressed():
    return "WhenKeyPressed;" + currentBlock["fields"]["KEY_OPTION"][0] + "\n"


# CONTROL
def Forever():
    global currentBlock
    currentBlockTmp = currentBlock
    try:
        contentRepeating = SubProgram(currentBlock["inputs"]["SUBSTACK"][1])
    except KeyError:
        contentRepeating = ""
    currentBlock = currentBlockTmp
    return "Forever\n" + contentRepeating


def If():
    global currentBlock
    currentBlockTmp = currentBlock
    try:
        condition = SubProgram(currentBlock["inputs"]["CONDITION"][1])
    except KeyError:
        condition = "False"
    currentBlock = currentBlockTmp
    try:
        thenPart = SubProgram(currentBlock["inputs"]["SUBSTACK"][1])
    except KeyError:
        thenPart = ""
    currentBlock = currentBlockTmp
    return "If;" + condition + "\nThen\n" + thenPart + "EndThen\n"


def IfElse():
    global currentBlock
    currentBlockTmp = currentBlock
    try:
        condition = SubProgram(currentBlock["inputs"]["CONDITION"][1])
    except KeyError:
        condition = "False"
    currentBlock = currentBlockTmp
    try:
        thenPart = SubProgram(currentBlock["inputs"]["SUBSTACK"][1])
    except KeyError:
        thenPart = ""
    currentBlock = currentBlockTmp
    try:
        elsePart = SubProgram(currentBlock["inputs"]["SUBSTACK2"][1])
    except KeyError:
        elsePart = ""
    currentBlock = currentBlockTmp
    return "IfElse;" + condition + "\nThen\n" + thenPart + "EndThen\n" + "Else\n" + elsePart + "EndElse\n"


def Repeat():
    global currentBlock
    currentBlockTmp = currentBlock
    numOfRepetitions = "0" if (currentBlock["inputs"]["TIMES"][1][1] == "") else currentBlock["inputs"]["TIMES"][1][1]
    currentBlock = currentBlockTmp
    try:
        contentRepeating = SubProgram(currentBlock["inputs"]["SUBSTACK"][1])
    except KeyError:
        contentRepeating = ""
    currentBlock = currentBlockTmp
    return "Repeat;" + numOfRepetitions + "\n" + "Begin\n" + contentRepeating + "End\n"


def Wait():
    duration = "0" if (currentBlock["inputs"]["DURATION"][1][1] == "") else currentBlock["inputs"]["DURATION"][1][1]
    return "Wait;" + duration + "\n"


def WaitUntil():
    global currentBlock
    currentBlockTmp = currentBlock
    try:
        condition = SubProgram(currentBlock["inputs"]["CONDITION"][1])
    except KeyError:
        condition = "False"
    currentBlock = currentBlockTmp
    return "WaitUntill;" + condition + "\n"


def RepeatUntil():
    global currentBlock
    currentBlockTmp = currentBlock
    try:
        condition = SubProgram(currentBlock["inputs"]["CONDITION"][1])
    except KeyError:
        condition = "False"
    currentBlock = currentBlockTmp
    try:
        contentRepeating = SubProgram(currentBlock["inputs"]["SUBSTACK"][1])
    except KeyError:
        contentRepeating = ""
    currentBlock = currentBlockTmp
    return "RepeatUntill;" + condition + "\n" + "Begin\n" + contentRepeating + "End\n"


# OPERATORS
def GreaterThanOp():
    operand1 = currentBlock["inputs"]["OPERAND1"][1][1]
    operand2 = currentBlock["inputs"]["OPERAND2"][1][1]
    return "( " + str(operand1) + " ) > ( " + str(operand2) + " )"


def LessThanOp():
    operand1 = currentBlock["inputs"]["OPERAND1"][1][1]
    operand2 = currentBlock["inputs"]["OPERAND2"][1][1]
    return "( " + str(operand1) + " ) < ( " + str(operand2) + " )"


def EqualsOp():
    operand1 = currentBlock["inputs"]["OPERAND1"][1][1]
    operand2 = currentBlock["inputs"]["OPERAND2"][1][1]
    return "( " + str(operand1) + " ) = ( " + str(operand2) + " )"


def NotOp():
    global currentBlock
    currentBlockTmp = currentBlock
    try:
        subOp = SubProgram(currentBlock["inputs"]["OPERAND"][1])
    except KeyError:
        subOp = "False"
    currentBlock = currentBlockTmp
    return "Not (" + subOp + ")"


def OrOp():
    global currentBlock
    currentBlockTmp = currentBlock
    try:
        operand1 = SubProgram(currentBlock["inputs"]["OPERAND1"][1])
    except KeyError:
        operand1 = "False"
    currentBlock = currentBlockTmp
    try:
        operand2 = SubProgram(currentBlock["inputs"]["OPERAND2"][1])
    except KeyError:
        operand2 = "False"
    currentBlock = currentBlockTmp
    return "( " + operand1 + " ) OR ( " + operand2 + ")"


def AndOp():
    global currentBlock
    currentBlockTmp = currentBlock
    try:
        operand1 = SubProgram(currentBlock["inputs"]["OPERAND1"][1])
    except KeyError:
        operand1 = "False"
    currentBlock = currentBlockTmp
    try:
        operand2 = SubProgram(currentBlock["inputs"]["OPERAND2"][1])
    except KeyError:
        operand2 = "False"
    currentBlock = currentBlockTmp
    return "( " + operand1 + " ) AND ( " + operand2 + ")"


def PseudoOutput(programs):
    for index, program in enumerate(programs):
        print("PROGRAM " + str(index + 1))
        print(program)


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

    "operator_gt": GreaterThanOp,
    "operator_lt": LessThanOp,
    "operator_equals": EqualsOp,
    "operator_not": NotOp,
    "operator_or": OrOp,
    "operator_and": AndOp,
}

myPrograms = Parse()
PseudoOutput(myPrograms)
