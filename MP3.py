import turtle
from MP1 import Parse
from ConditionParser import ParseCondition
import string
import time

def ParseIntermediate(rotine):
    indents = 0
    result = ""
    rotineList = rotine.split("\n")
    for instruction in rotineList:
        if instruction == '':
            continue
        parsed = parseMapper[instruction.split(";")[0]](instruction, indents)
        result += parsed[0]
        indents = parsed[1]

    return result

def Begin(instruction, indents):
    return ("", indents + 1)

def End(instruction, indents):
    return ("", indents - 1)

def Else(instruction, indents):
    return ("\t" * indents + "else\n", indents + 1)

def MoveSteps(instruction, indents):
    instructionTokens = instruction.split(";")
    direction = "forward" if instructionTokens[1] == "Forward" else "backward"
    steps = instructionTokens[2]
    return ("\t" * indents + "turtle." + direction + "(" + steps + ")\n" + MoveText(indents), indents)

def Repeat(instruction, indents):
    instructionTokens = instruction.split(";")
    repeatitions = instructionTokens[1]
    return ("\t" * indents + "for i" + str(indents) + " in range(" + str(repeatitions) + "):\n", indents)

def TurnRight(instruction, indents):
    instructionTokens = instruction.split(";")
    degree = instructionTokens[1]
    return ("\t" * indents + "turtle.right(" + degree + ")\n" +
        "\t" * indents + "turtle.shape('icons\\\\' + str(round(float(turtle.heading())) % 360) + '.gif')\n", indents)

def TurnLeft(instruction, indents):
    instructionTokens = instruction.split(";")
    degree = instructionTokens[1]
    return ("\t" * indents + "turtle.left(" + degree + ")\n" +
        "\t" * indents + "turtle.shape('icons\\\\' + str(round(float(turtle.heading())) % 360) + '.gif')\n", indents)

def GotoXY(instruction, indents):
    instructionTokens = instruction.split(";")
    X = instructionTokens[1]
    Y = instructionTokens[2]
    return ("\t" * indents + "turtle.goto(" + X + "," + Y + ")\n" + MoveText(indents), indents)

def ChangeXBy(instruction, indents):
    instructionTokens = instruction.split(";")
    ChangeInX = instructionTokens[1]
    return ("\t" * indents + "turtle.setx(turtle.xcor+" + ChangeInX + ")\n" + + MoveText(indents), indents)

def SetX(instruction, indents):
    instructionTokens = instruction.split(";")
    X = instructionTokens[1]
    return ("\t" * indents + "turtle.setx(" + X + ")\n" + MoveText(indents), indents)

def ChangeYBy(instruction, indents):
    instructionTokens = instruction.split(";")
    ChangeInY = instructionTokens[1]
    return ("\t" * indents + "turtle.sety(turtle.ycor+" + ChangeInY + ")\n" + MoveText(indents), indents)

def SetY(instruction, indents):
    instructionTokens = instruction.split(";")
    Y = instructionTokens[1]
    return ("\t" * indents + "turtle.sety(" + Y + ")\n" + MoveText(indents), indents)

def Forever(indents):
    return ("\t" * indents + "while(True):\n", indents + 1)
    
def If(instruction, indents):
    instructionTokens = instruction.split(";")
    condition = ParseCondition(instructionTokens[1])
    return ("\t" * indents + "if " + condition + " :\n", indents + 1)
    
def Wait(instruction, indents):
    instructionTokens = instruction.split(";")
    duration = instructionTokens[1]
    return ("\t" * indents + "turtle.delay(" + (int(duration*1000)) + ")\n", indents)

def WaitUntil(instruction, indents):
    instructionTokens = instruction.split(";")
    condition = ParseCondition(instructionTokens[1])
    return ("\t" * indents + "while(!(" + condition +")):\n" + "\t" * (indents+1) + "turtle.delay(1000)\n", indents)

def RepeatUntil(instruction, indents):
    instructionTokens = instruction.split(";")
    condition = ParseCondition(instructionTokens[1])
    return ("\t" * indents + "while(!(" + condition +")):\n", indents)

def Say(instruction, indents):
    instructionTokens = instruction.split(";")
    words = instructionTokens[1]
    params = ('Arial',15,'bold')
    return (SetText(words, params, indents) + MoveText(indents), indents)

def SayForSecs(instruction, indents):
    instructionTokens = instruction.split(";")
    words = instructionTokens[1]
    duration = instructionTokens[2]
    return (SetText(words, ('Arial',15,'bold'), indents) + MoveText(indents) +
        "\t" * indents + "time.sleep(" + str(duration) + ")\n" +
        "\t" * indents + "text.clear()\n" +
        "\t" * indents + "written = ''\n", indents)

def Think(instruction, indents):
    instructionTokens = instruction.split(";")
    words = instructionTokens[1]
    params = ('Corier',15,'italic')
    return (SetText(words, params, indents) + MoveText(indents), indents)

def ThinkForSecs(instruction, indents):
    instructionTokens = instruction.split(";")
    words = instructionTokens[1]
    duration = instructionTokens[2]
    return (SetText(words, ('Corier',15,'italic'), indents) + MoveText(indents) +
        "\t" * indents + "time.sleep(" + str(duration) + ")\n" +
        "\t" * indents + "text.clear()\n" +
        "\t" * indents + "written = ''\n", indents)

def WhenFlagClicked(instruction, indents):
    return ('', indents)

def WhenKeyPressed(instruction, indents):
    return ('', indents)

    
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
    "GotoXY": GotoXY,
    "ChangeXBy": ChangeXBy,
    "SetX": SetX,
    "ChangeYBy": ChangeYBy,
    "SetY": SetY,
    "Forever": Forever,
    "If": If,
    "IfElse": If,
    "Wait": Wait,
    "WaitUntil": WaitUntil,
    "RepeatUntil": RepeatUntil,
    "Say": Say,
    "SayForSecs": SayForSecs,
    "Think": Think,
    "ThinkForSecs": ThinkForSecs,
    "WhenFlagClicked": WhenFlagClicked,
    "WhenKeyPressed": WhenKeyPressed
}

eventMapper = {}
for event in list(string.ascii_lowercase) + ['space', 'up_arrow', 'down_arrow', 'left_arrow', 'right_arrow', 'empty', 'flag', 'any']:
    eventMapper[event] = ''


def MoveText(indents):
    tabs = "\t" * indents
    return tabs + "text.clear()\n" + tabs + "text.goto(turtle.xcor() + turtle_width / 2, turtle.ycor() + turtle_height / 2)\n" + tabs + "text.write(written, font=font, align='left')\n"

def SetText(words, params, indents):
    tabs = "\t" * indents
    return tabs + "written = '" + words + "'\n" + tabs + "font = " + str(params) + "\n"


screen = turtle.getscreen()
scratchName = "icons\\0.gif"
turtle.addshape("flag.gif")
for angle in range(360):
    turtle.addshape("icons\\" + str(angle) + ".gif")

flag = turtle.Turtle(shape='flag.gif')
flag.speed(0)
flag.penup()
flag.goto((screen.screensize()[0] - 70, screen.screensize()[1] - 30))

turtle.shape(scratchName)
turtle.speed(0)
turtle.penup()

turtle_height = turtle.shapesize()[0] * 70
turtle_width = turtle.shapesize()[1] * 70

text = turtle.Turtle()
text.hideturtle()
text.speed(0)
text.penup()

written = ""
font = ("Ariel", 15, "bold")

def handle_click(xpos, ypos):
    if xpos >= flag.xcor() - 35 and xpos <= flag.xcor() + 35 and ypos >= flag.ycor() - 35 and ypos <= flag.ycor() + 35:
        exec(eventMapper['flag'])

for input in list(string.ascii_lowercase) + ['space', 'up_arrow', 'down_arrow', 'left_arrow', 'right_arrow']:
    # exec("def handle_" + input + "():\n\tglobal key\n\tglobal pause\n\tif key == 'any' or key == '" + input + "':\n\t\tpause = False\n\t\tkey = ''")
    exec("def handle_" + input + "():\n\texec(eventMapper['" + input + "'])\n")

for input in list(string.ascii_lowercase):
    turtle.onkeypress(globals()["handle_" + input], input)

screen.onkeypress(globals()["handle_space"], 'space')
screen.onkeypress(globals()["handle_up_arrow"], 'Up')
screen.onkeypress(globals()["handle_down_arrow"], 'Down')
screen.onkeypress(globals()["handle_left_arrow"], 'Left')
screen.onkeypress(globals()["handle_right_arrow"], 'Right')

screen.onclick(handle_click)

screen.listen()

codeList = Parse() # ['WhenFlagClicked\nTurnLeft;30\n', 'WhenFlagClicked\nMoveSteps;Forward;100\n', 'WhenKeyPressed;space\nThink;Hmm', 'SayForSecs;Hi There;1', 'WhenKeyPressed;a\nSay;World']
for subcode in codeList:
    code = "global written\nglobal font\n" + ParseIntermediate(subcode)
    if subcode.startswith('WhenFlagClicked'):
        eventMapper['flag'] += code
    elif subcode.startswith('WhenKeyPressed'):
        eventMapper[subcode.split('\n')[0].split(';')[1]] += code
    else:
        eventMapper['empty'] += code

for event in list(string.ascii_lowercase) + ['space', 'up_arrow', 'down_arrow', 'left_arrow', 'right_arrow']:
    eventMapper[event] += eventMapper['any']

print(eventMapper)
exec(eventMapper['empty'])

screen.mainloop()
