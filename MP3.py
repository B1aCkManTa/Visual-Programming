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
greenFlagExists = False


def ParseIntermediate(rotine):
    if greenFlagExists:
        indents = 1
    else:
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

    return result


def Begin(instruction, indents):
    return "\t" * (indents+1) + "pass\n", indents + 1


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
            "\t" * indents + "text." + direction + "(" + steps + ")\n" +
            "\t" * indents + "text.clear()\n" +
            "\t" * indents + "text.write(" + lastSaid + ", move=True ,font=('Corier',15,'" + sayOrThink + "'), align='right')\n",
            indents)


def Repeat(instruction, indents):
    instructionTokens = instruction.split(";")
    repeatitions = instructionTokens[1]
    return "\t" * indents + "for i" + str(indents) + " in range(" + str(repeatitions) + "):\n", indents


# Done
def TurnRight(instruction, indents):
    instructionTokens = instruction.split(";")
    degree = instructionTokens[1]
    return ("\t" * indents + "turtle.right(" + degree + ")\n" +
            "\t" * indents + "text.right(" + degree + ")\n", indents)


# Done
def TurnLeft(instruction, indents):
    instructionTokens = instruction.split(";")
    degree = instructionTokens[1]
    return ("\t" * indents + "turtle.left(" + degree + ")\n" +
            "\t" * indents + "text.left(" + degree + ")\n", indents)


def GotoXY(instruction, indents):
    global lastSaid
    global sayOrThink
    instructionTokens = instruction.split(";")
    X = instructionTokens[1]
    Y = instructionTokens[2]
    return ("\t" * indents + "turtle.goto(" + X + "," + Y + ")\n" +
            "\t" * indents + "text.goto(" + X + "," + Y + ")\n" +
            "\t" * indents + "text.clear()\n" +
            "\t" * indents + "text.write(" + lastSaid + ", move=True ,font=('Corier',15,'" + sayOrThink + "'), align='right')\n",
            indents)


def ChangeXBy(instruction, indents):
    global lastSaid
    global sayOrThink
    instructionTokens = instruction.split(";")
    ChangeInX = instructionTokens[1]
    return ("\t" * indents + "turtle.setx(turtle.xcor()+" + ChangeInX + ")\n" +
            "\t" * indents + "text.setx(turtle.xcor()+" + ChangeInX + ")\n" +
            "\t" * indents + "text.clear()\n" +
            "\t" * indents + "text.write(" + lastSaid + ", move=True ,font=('Corier',15,'" + sayOrThink + "'), align='right')\n",
            indents)


def SetX(instruction, indents):
    global lastSaid
    global sayOrThink
    instructionTokens = instruction.split(";")
    X = instructionTokens[1]
    return ("\t" * indents + "turtle.setx(" + X + ")\n" +
            "\t" * indents + "text.setx(" + X + ")\n" +
            "\t" * indents + "text.clear()\n" +
            "\t" * indents + "text.write(" + lastSaid + ", move=True ,font=('Corier',15,'" + sayOrThink + "'), align='right')\n",
            indents)


def ChangeYBy(instruction, indents):
    global lastSaid
    global sayOrThink
    instructionTokens = instruction.split(";")
    ChangeInY = instructionTokens[1]
    return ("\t" * indents + "turtle.sety(turtle.ycor()+" + ChangeInY + ")\n" +
            "\t" * indents + "text.sety(turtle.ycor()+" + ChangeInY + ")\n" +
            "\t" * indents + "text.clear()\n" +
            "\t" * indents + "text.write(" + lastSaid + ", move=True ,font=('Corier',15,'" + sayOrThink + "'), align='right')\n",
            indents)


def SetY(instruction, indents):
    global lastSaid
    global sayOrThink
    instructionTokens = instruction.split(";")
    Y = instructionTokens[1]
    return ("\t" * indents + "turtle.sety(" + Y + ")\n" +
            "\t" * indents + "text.sety(" + Y + ")\n" +
            "\t" * indents + "text.clear()\n" +
            "\t" * indents + "text.write(" + lastSaid + ", move=True ,font=('Corier',15,'" + sayOrThink + "'), align='right')\n",
            indents)


def Forever(indents):
    return ("\t" * indents + "while(True):\n" +
            "\t" * (indents + 1) + "pass\n", indents + 1)


def If(instruction, indents):
    instructionTokens = instruction.split(";")
    condition = ParseCondition(instructionTokens[1])
    return "\t" * indents + "if " + condition + " :\n", indents + 1


def Then(instruction, indents):
    return ("\t" * indents + "pass\n", indents)


def Wait(instruction, indents):
    instructionTokens = instruction.split(";")
    duration = int(instructionTokens[1])
    return ("\t" * indents + "time.sleep(" + str(duration) + ")" + "\n", indents)


def WaitUntil(instruction, indents):
    instructionTokens = instruction.split(";")
    condition = ParseCondition(instructionTokens[1])
    return ("\t" * indents + "while(!(" + condition + ")):\n" +
            "\t" * indents + "time.sleep(" + str(1) + ")" + "\n", indents)


def RepeatUntil(instruction, indents):
    instructionTokens = instruction.split(";")
    condition = ParseCondition(instructionTokens[1])
    return "\t" * indents + "while(!(" + condition + ")):\n" + \
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
    instructionTokens = instruction.split(";")
    Key = instructionTokens[1]
    if Key == "any":
        Key = "a"
    return "\t" * indents + "keyboard.wait(" + "\"" + str(Key.split(" ")[0]) + "\"" + ")\n", indents


def WhenFlagClicked(instruction, indents):
    global Flag
    global counter
    global greenFlagExists
    if not greenFlagExists:
        greenFlagExists = True
        return "turtle.onclick(foo)\n" + \
               "while True:\n" + \
               "\t" * 1 + "Flag = False\n" + \
               "\t" * 1 + "while(not Flag):\n" + \
               "\t" * 2 + "turtle.onclick(foo)\n" + \
               "\t" * 2 + "time.sleep(0.25)\n", 1
    return "", 1


def EndFlagClicked(instruction, indents):
    return "", indents


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
    "WaitUntil": WaitUntil,
    "RepeatUntil": RepeatUntil,
    "Say": Say,
    "SayForSecs": SayForSecs,
    "Think": Think,
    "ThinkForSecs": ThinkForSecs,
    "WhenFlagClicked": WhenFlagClicked,
    "WhenKeyPressed": WhenKeyPressed,
    "EndFlagClicked": EndFlagClicked
}


def foo(x, y):
    global Flag
    Flag = True


screen = turtle.getscreen()
scratchName = "scratch.gif"
# turtle.addshape(scratchName)

turtle.shape("turtle")
turtle.color('red', 'green')
turtle.penup()
# turtle.speed(1)
# turtle.penup()

# turtle_height = turtle.shapesize()[0]
# turtle_width = turtle.shapesize()[1]
turtle.shapesize(4, 4, 3)
text = turtle.Turtle()
text.hideturtle()
text.penup()
# text.pendown()
text.left(90)
text.forward(70)
text.right(90)
text.forward(60)
text.color('blue', 'black')
# text.forward(200)
# timer = threading.Timer(2.0, text.clear)
# text.write("Hello World", move=False, font=('Courier', 15, 'normal'), align='left')
# timer.start()

# codeList = ["Repeat;10\nBegin\nSay;HELLOOOO\nTurnRight;90\nMoveSteps;Forward;45\nEnd"] #Parse()
# codeList = [
#     "WhenFlagClicked\nIfElse;( 40 ) > ( 50 )\nThen\nRepeat;3\nBegin\nThink;Hmm...\nTurnRight;15\nMoveSteps;Forward;15.0\nEnd\nEndThen\nElse\nRepeat;1\nBegin\nSay;Hello!\nTurnRight;90\nMoveSteps;Forward;40.0\nEnd\nEndElse",
#     "WhenFlagClicked\nMoveSteps;Forward;90.0"]  # Parse()
codeList = Parse()
code = ""
for subcode in codeList:
    code += ParseIntermediate(subcode) + "\n"
print(code)
exec(code)

# turtle.write("Hello Turtle", move=False, font=('Courier', 15, 'normal'), align='left')
# print("out")


# def foo(x,y):
#     print("Hello")
#     global Flag
#     Flag = True

# turtle.onclick(foo)

# print("in")
screen.mainloop()
