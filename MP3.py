import turtle
from MP1 import Parse
from ConditionParser import ParseCondition
import time
import threading
import random
import keyboard

lastSaid = "\"\""
sayOrThink = "italic"
Flag = False
isGreenFlagEvent = False
isKeyPressEvent = False
key = ""

events = {}


def ParseIntermediate(rotine):
    global isKeyPressEvent
    global isGreenFlagEvent
    global key
    indents = 0
    result = ""
    rotineList = rotine.split("\n")
    for instruction in rotineList:
        if instruction == "Begin" or instruction == "End":
            parsed = parseMapper[instruction](instruction, indents)
        elif instruction == '':
            continue
        else:
            parsed = parseMapper[instruction.split(";")[0]](instruction, indents)
        result += parsed[0]
        indents = parsed[1]

    if isGreenFlagEvent:
        if "GreenFlag" in events:
            last = events["GreenFlag"]
            last += result
            events["GreenFlag"] = last
        else:
            events["GreenFlag"] = result
    elif isKeyPressEvent:
        if key in events:
            last = events[key]
            last += result
            events[key] = last
        else:
            events[key] = result
    if isKeyPressEvent or isGreenFlagEvent:
        isGreenFlagEvent = False
        isKeyPressEvent = False
        key = ""
        return result, False
    else:
        return result, True


def Begin(instruction, indents):
    return "\t" * (indents + 1) + "pass\n", indents + 1


def End(instruction, indents):
    return "", indents - 1


def Else(instruction, indents):
    return "\t" * indents + "else: \n" + \
           "\t" * (indents + 1) + "pass\n", indents + 1


# Done
def MoveSteps(instruction, indents):
    global lastSaid
    global sayOrThink
    instructionTokens = instruction.split(";")
    direction = "forward" if instructionTokens[1] == "Forward" else "backward"
    steps = instructionTokens[2]
    return ("\t" * indents + "turtle." + direction + "(" + steps + ")\n" +
            "\t" * indents + "if out_of_bounds(turtle):\n" +
            "\t" * (indents + 1) + "turtle.undo()\n" +
            "\t" * indents + "else:\n" +
            "\t" * (indents + 1) + "text." + direction + "(" + steps + ")\n" +
            "\t" * (indents + 1) + "text.clear()\n" +
            "\t" * (indents + 1) + "text.write(" + lastSaid + ", move=True ,font=('Corier',15,'" + sayOrThink + "'), align='right')\n",
            indents)


def Repeat(instruction, indents):
    instructionTokens = instruction.split(";")
    repeatitions = instructionTokens[1]
    return "\t" * indents + "for i" + str(indents) + " in range(" + str(repeatitions) + "):\n", indents


# Done
def TurnRight(instruction, indents):
    global lastSaid
    global sayOrThink
    instructionTokens = instruction.split(";")
    degree = instructionTokens[1]
    return ("\t" * indents + "turtle.right(" + degree + ")\n" +
            "\t" * indents + "text.right(" + degree + ")\n" +
            "\t" * indents + "text.clear()\n" +
            "\t" * indents + "text.write(" + lastSaid + ", move=True ,font=('Corier',15,'" + sayOrThink + "'), align='right')\n"
            , indents)


# Done
def TurnLeft(instruction, indents):
    global lastSaid
    global sayOrThink
    instructionTokens = instruction.split(";")
    degree = instructionTokens[1]
    return ("\t" * indents + "turtle.left(" + degree + ")\n" +
            "\t" * indents + "text.left(" + degree + ")\n" +
            "\t" * indents + "text.clear()\n" +
            "\t" * indents + "text.write(" + lastSaid + ", move=True ,font=('Corier',15,'" + sayOrThink + "'), align='right')\n"
            , indents)


def GotoXY(instruction, indents):
    global lastSaid
    global sayOrThink
    instructionTokens = instruction.split(";")
    X = instructionTokens[1]
    Y = instructionTokens[2]
    return ("\t" * indents + "turtle.goto(" + X + "," + Y + ")\n" +
            "\t" * indents + "if out_of_bounds(turtle):\n" +
            "\t" * (indents + 1) + "turtle.undo()\n" +
            "\t" * indents + "else:\n" +
            "\t" * (indents + 1) + "text.goto(" + X + "," + Y + ")\n" +
            "\t" * (indents + 1) + "text.clear()\n" +
            "\t" * (
                        indents + 1) + "text.write(" + lastSaid + ", move=True ,font=('Corier',15,'" + sayOrThink + "'), align='right')\n",
            indents)


def ChangeXBy(instruction, indents):
    global lastSaid
    global sayOrThink
    instructionTokens = instruction.split(";")
    ChangeInX = instructionTokens[1]
    return ("\t" * indents + "turtle.setx(turtle.xcor()+" + ChangeInX + ")\n" +
            "\t" * indents + "if out_of_bounds(turtle):\n" +
            "\t" * (indents + 1) + "turtle.undo()\n" +
            "\t" * indents + "else:\n" +
            "\t" * (indents + 1) + "text.setx(turtle.xcor()+" + ChangeInX + ")\n" +
            "\t" * (indents + 1) + "text.clear()\n" +
            "\t" * (
                        indents + 1) + "text.write(" + lastSaid + ", move=True ,font=('Corier',15,'" + sayOrThink + "'), align='right')\n",
            indents)


def SetX(instruction, indents):
    global lastSaid
    global sayOrThink
    instructionTokens = instruction.split(";")
    X = instructionTokens[1]
    return ("\t" * indents + "turtle.setx(" + X + ")\n" +
            "\t" * indents + "if out_of_bounds(turtle):\n" +
            "\t" * (indents + 1) + "turtle.undo()\n" +
            "\t" * indents + "else:\n" +
            "\t" * (indents + 1) + "text.setx(" + X + ")\n" +
            "\t" * (indents + 1) + "text.clear()\n" +
            "\t" * (
                        indents + 1) + "text.write(" + lastSaid + ", move=True ,font=('Corier',15,'" + sayOrThink + "'), align='right')\n",
            indents)


def ChangeYBy(instruction, indents):
    global lastSaid
    global sayOrThink
    instructionTokens = instruction.split(";")
    ChangeInY = instructionTokens[1]
    return ("\t" * indents + "turtle.sety(turtle.ycor()+" + ChangeInY + ")\n" +
            "\t" * indents + "if out_of_bounds(turtle):\n" +
            "\t" * (indents + 1) + "turtle.undo()\n" +
            "\t" * indents + "else:\n" +
            "\t" * (indents + 1) + "text.sety(turtle.ycor()+" + ChangeInY + ")\n" +
            "\t" * (indents + 1) + "text.clear()\n" +
            "\t" * (
                        indents + 1) + "text.write(" + lastSaid + ", move=True ,font=('Corier',15,'" + sayOrThink + "'), align='right')\n",
            indents)


def SetY(instruction, indents):
    global lastSaid
    global sayOrThink
    instructionTokens = instruction.split(";")
    Y = instructionTokens[1]
    return ("\t" * indents + "turtle.sety(" + Y + ")\n" +
            "\t" * indents + "if out_of_bounds(turtle):\n" +
            "\t" * (indents + 1) + "turtle.undo()\n" +
            "\t" * indents + "else:\n" +
            "\t" * (indents + 1) + "text.sety(" + Y + ")\n" +
            "\t" * (indents + 1) + "text.clear()\n" +
            "\t" * (
                        indents + 1) + "text.write(" + lastSaid + ", move=True ,font=('Corier',15,'" + sayOrThink + "'), align='right')\n",
            indents)


def Forever(instruction, indents):
    # return "\t" * indents + "pass\n", indents
    return ("\t" * indents + "while(True):\n" +
            "\t" * (indents + 1) + "pass\n", indents + 1)


def If(instruction, indents):
    instructionTokens = instruction.split(";")
    condition = ParseCondition(instructionTokens[1])
    return "\t" * indents + "if " + condition + " :\n", indents + 1


def Then(instruction, indents):
    return "\t" * indents + "pass\n", indents


def Wait(instruction, indents):
    instructionTokens = instruction.split(";")
    duration = int(instructionTokens[1])
    return "\t" * indents + "time.sleep(" + str(duration) + ")" + "\n", indents


def WaitUntil(instruction, indents):
    instructionTokens = instruction.split(";")
    condition = ParseCondition(instructionTokens[1])
    return "\t" * indents + "while(not(" + condition + ")):\n" + \
           "\t" * (indents + 1) + "time.sleep(" + str(1) + ")" + "\n", indents + 1


def RepeatUntil(instruction, indents):
    instructionTokens = instruction.split(";")
    condition = ParseCondition(instructionTokens[1])
    return "\t" * indents + "while(not(" + condition + ")):\n" + \
           "\t" * (indents + 1) + "pass\n", indents


def Say(instruction, indents):
    global lastSaid
    global sayOrThink
    sayOrThink = "bold"
    instructionTokens = instruction.split(";")
    words = '"' + instructionTokens[1] + '"'
    lastSaid = words
    return ("\t" * indents + "text.clear()\n" +
            "\t" * indents + "text.write(" + words + ", move=True ,font=('Arial',15,'bold'), align='right')\n", indents)


def SayForSecs(instruction, indents):
    global lastSaid
    global sayOrThink
    sayOrThink = "bold"
    instructionTokens = instruction.split(";")
    words = '"' + instructionTokens[1] + '"'
    lastSaid = words
    duration = int(instructionTokens[2])
    return (
        "\t" * indents + "text.clear()\n" +
        "\t" * indents + "text.write(" + words + ", move=True , font=('Arial',15,'bold'), align='right')\n" +
        "\t" * indents + "time.sleep(" + str(duration) + ")" + "\n" +
        "\t" * indents + "text.clear()\n", indents)


def Think(instruction, indents):
    global lastSaid
    global sayOrThink
    sayOrThink = "italic"
    instructionTokens = instruction.split(";")
    words = '"' + instructionTokens[1] + '"'
    lastSaid = words
    return ("\t" * indents + "text.clear()\n" +
            "\t" * indents + "text.write(" + words + ", move=True ,font=('Corier',15,'italic'), align='right')\n",
            indents)


def ThinkForSecs(instruction, indents):
    global lastSaid
    global sayOrThink
    sayOrThink = "italic"
    instructionTokens = instruction.split(";")
    words = '"' + instructionTokens[1] + '"'
    lastSaid = words
    duration = int(instructionTokens[2])
    return (
        "\t" * indents + "text.clear()\n" +
        "\t" * indents + "text.write(" + words + ", move=True , font=('Corier',15,'italic'), align='right')\n" +
        "\t" * indents + "time.sleep(" + str(duration) + ")" + "\n" +
        "\t" * indents + "text.clear()\n", indents)


def WhenKeyPressed(instruction, indents):
    global isKeyPressEvent
    global key
    isKeyPressEvent = True
    instructionTokens = instruction.split(";")
    Key = instructionTokens[1].replace(" ", "")
    key = Key
    return "", indents


def WhenFlagClicked(instruction, indents):
    global Flag
    # global greenFlagExists
    global isGreenFlagEvent
    isGreenFlagEvent = True
    return "", 0


def exec_GreenFlagEvent(x, y):
    exec(events["GreenFlag"])


def out_of_bounds(turtle):
    return not (-width // 2 < turtle.xcor() < width // 2 and -height // 2 < turtle.ycor() < height // 2)


def initialize_events():
    executableCode = ""
    for event in events.keys():
        if event != "GreenFlag" and event != "any":
            executableCode += "def " + event + "_():\n" + "\texec(events[\"" + event + "\"])\n" + "turtle.onkeypress(" + event + "_, \"" + event + "\")\n"
        elif event == "any":
            executableCode += "def " + event + "():\n" + "\texec(events[\"" + event + "\"])\n" + "turtle.onkeypress(" + event + ")\n"
        elif event == "GreenFlag":
            turtle.onclick(exec_GreenFlagEvent)
    executableCode += "turtle.listen()"
    exec(executableCode)


parseMapper = {
    "MoveSteps": MoveSteps,
    "Begin": Begin,
    "End": End,
    "EndThen": End,
    "EndElse": End,
    "Else": Else,
    "Repeat": Repeat,
    "TurnRight": TurnRight,
    "TurnLeft": TurnLeft,
    "GoToXY": GotoXY,
    "ChangeXBY": ChangeXBy,
    "SetX": SetX,
    "ChangeYBY": ChangeYBy,
    "SetY": SetY,
    "Forever": Forever,
    "If": If,
    "Then": Then,
    "IfElse": If,
    "Wait": Wait,
    "WaitUntill": WaitUntil,
    "RepeatUntill": RepeatUntil,
    "Say": Say,
    "SayForSecs": SayForSecs,
    "Think": Think,
    "ThinkForSecs": ThinkForSecs,
    "WhenFlagClicked": WhenFlagClicked,
    "WhenKeyPressed": WhenKeyPressed
}

screen = turtle.getscreen()
width, height = screen.window_width() - 30, screen.window_height() - 30  # -30 to account for window borders, etc.
scratchName = "scratch.gif"
turtle.shape("turtle")
turtle.color('red', 'green')
turtle.penup()
turtle.shapesize(3, 3, 2)
text = turtle.Turtle()
text.hideturtle()
text.penup()
text.left(90)
text.forward(70)
text.right(90)
text.forward(60)
text.color('blue', 'black')

# codeList = ["Repeat;10\nBegin\nSay;HELLOOOO\nTurnRight;90\nMoveSteps;Forward;45\nEnd"] #Parse()
# codeList = [
#     "WhenFlagClicked\nIfElse;( 40 ) > ( 50 )\nThen\nRepeat;3\nBegin\nThink;Hmm...\nTurnRight;15\nMoveSteps;Forward;15.0\nEnd\nEndThen\nElse\nRepeat;1\nBegin\nSay;Hello!\nTurnRight;45\nMoveSteps;Forward;40.0\nEnd\nEndElse",
#     "WhenKeyPressed;a\nMoveSteps;Forward;10.0"]  # Parse()
codeList = Parse('project.json')
nonEventCode = ""
for subcode in codeList:
    code, isNonEventCode = ParseIntermediate(subcode)
    if isNonEventCode:
        nonEventCode += code + "\n"
initialize_events()
print(nonEventCode)
exec(nonEventCode)

# def up_():
#     print("jjj")
#     exec(events["up"])
# turtle.onkeypress(up_, "a")
# turtle.listen()
screen.mainloop()

