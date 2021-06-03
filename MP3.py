import turtle
from MP1 import Parse

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
    return ("\t" * indents + "turtle." + direction + "(" + steps + ")\n", indents)

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

# def GotoXY(x,y):
#     turtle.goto(x,y)

# def ChangeXBy(value):
#     turtle.setx(turtle.xcor+value)

# def SetX(value):
#     turtle.setx(value)

# def ChangeYBy(value):
#     turtle.sety(turtle.ycor+value)

# def SetY(value):
#     turtle.sety(value)


parseMapper = {
    "MoveSteps": MoveSteps,
    "Begin": Begin,
    "End": End,
    "EndThen": End,
    "EndElse": End,
    "Else": Else,
    "Repeat": Repeat
}


screen = turtle.getscreen()
scratchName = "scratch.gif"
turtle.addshape(scratchName)

turtle.shape(scratchName)
turtle.speed(1)
turtle.penup()

codeList = ["MoveSteps;Forward;100"] #Parse()
code = ""
for subcode in codeList:
    code += ParseIntermediate(subcode) + "\n"

exec(code)

screen.mainloop()
