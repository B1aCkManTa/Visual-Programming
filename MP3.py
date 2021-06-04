import turtle
from MP1 import Parse
from ConditionParser import ParseCondition

def ParseIntermediate(rotine):
    indents = 0
    result = ""
    rotineList = rotine.split("\n")
    for instruction in rotineList:
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
    return ("\t" * indents + "turtle." + direction + "(" + steps + ")\n" +
        "\t" * indents + "text." + direction + "(" + steps + ")\n", indents)

def Repeat(instruction, indents):
    instructionTokens = instruction.split(";")
    repeatitions = instructionTokens[1]
    return ("\t" * indents + "for i" + str(indents) + " in range(" + str(repeatitions) + "):\n", indents)

def TurnRight(instruction, indents):
    instructionTokens = instruction.split(";")
    degree = instructionTokens[1]
    return ("\t" * indents + "turtle.right(" + degree + ")\n", indents)

def TurnLeft(instruction, indents):
    instructionTokens = instruction.split(";")
    degree = instructionTokens[1]
    return ("\t" * indents + "turtle.left(" + degree + ")\n", indents)

def GotoXY(instruction, indents):
    instructionTokens = instruction.split(";")
    X = instructionTokens[1]
    Y = instructionTokens[2]
    return ("\t" * indents + "turtle.goto(" + X + "," + Y + ")\n" +
        "\t" * indents + "text.goto(" + X + "," + Y + ")\n", indents)

def ChangeXBy(instruction, indents):
    instructionTokens = instruction.split(";")
    ChangeInX = instructionTokens[1]
    return ("\t" * indents + "turtle.setx(turtle.xcor+" + ChangeInX + ")\n" +
        "\t" * indents + "text.setx(turtle.xcor+" + ChangeInX + ")\n", indents)

def SetX(instruction, indents):
    instructionTokens = instruction.split(";")
    X = instructionTokens[1]
    return ("\t" * indents + "turtle.setx(" + X + ")\n", indents)

def ChangeYBy(instruction, indents):
    instructionTokens = instruction.split(";")
    ChangeInY = instructionTokens[1]
    return ("\t" * indents + "turtle.sety(turtle.ycor+" + ChangeInY + ")\n", indents)

def SetY(instruction, indents):
    instructionTokens = instruction.split(";")
    Y = instructionTokens[1]
    return ("\t" * indents + "turtle.sety(" + Y + ")\n", indents)

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
    return ("\t" * indents + "text.write(" + words + ", font=('Arial',15,'bold'), align='left)\n", indents)

def SayForSecs(instruction, indents):
    instructionTokens = instruction.split(";")
    words = instructionTokens[1]
    duration = instructionTokens[2]
    return ("\t" * indents + "text.write(" + words + ", font=('Arial',15,'bold'), align='left)\n" +
        "\t" * indents + "turtle.delay(" + (int(duration) * 1000) + " *)\n" +
        "\t" * indents + "text.clear()\n", indents)

def Think(instruction, indents):
    instructionTokens = instruction.split(";")
    words = instructionTokens[1]
    return ("\t" * indents + "text.write(" + words + ", font=('Corier',15,'italic'), align='left)\n", indents)

def ThinkForSecs(instruction, indents):
    instructionTokens = instruction.split(";")
    words = instructionTokens[1]
    duration = instructionTokens[2]
    return ("\t" * indents + "text.write(" + words + ", font=('Corier',15,'italic'), align='left)\n" +
        "\t" * indents + "turtle.delay(" + (int(duration) * 1000) + " *)\n" +
        "\t" * indents + "text.clear()\n", indents)


    
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
    "ThinkForSecs": ThinkForSecs
}


screen = turtle.getscreen()
scratchName = "scratch.gif"
turtle.addshape(scratchName)

turtle.shape(scratchName)
turtle.speed(1)
turtle.penup()

turtle_height = turtle.shapesize()[0]
turtle_width = turtle.shapesize()[1]

text = turtle.Turtle()
text.hideturtle()
text.penup()

text.write("Hello Turtle", move=False, font=('Courier', 15, 'normal'), align='left')
text.write("Hello World", move=False, font=('Courier', 15, 'normal'), align='left')

codeList = ["MoveSteps;Forward;100"] #Parse()
code = ""
for subcode in codeList:
    code += ParseIntermediate(subcode) + "\n"

exec(code)

screen.mainloop()
