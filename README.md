# Visual-Programming Mini-Project 1 Team 2

Here is a discription of the functionality and implementation of the project.

## Execution

The file `MP1.py` contains all the code implementation of the project and is the only thing that need to be executed. The code acts on a file named `project.json` that holds a `JSON` representation of a **Scratch 3/online** code. the `project.json` file has to be in the same directory which `MP1.py` is run from. When the file is run, the console will print a list of strings signifying the textual representations of parallel sub-programs present in the **Scratch** code.

---

## Used Libraries

### `json`

A library that (from its name) is used to load `JSON` files and represent the `JSON` objects as maps.

---

## Global Variables

### `blocks`

A map object that maps a key of instruction ID (`string`) to its corresponding `JSON` object that represents the instruction (`map`).

### `currentBlock`

The map object that represents the instruction that is being currently processed.

### `switcher`

A map object that maps a key of an instruction's op-code (`string`) to its corresponding parser function that parses its `JSON` object and return its textual representation (`function`)

---

## Defined Functions

### `LoadJson()`

A function that loads the prementioned `JSON` file and returns the `JSON` object contained in the file.

### `StartBlocks()`

This function parses `blocks` to get the starting block of all sub-programs and returns a list of instruction ID's (`string`) of said blocks.

### `SubProgram(startBlockRef)`

This function is the heart of parsing. It takes as an argument `startBlockRef` which is the ID of the start block of the sub-program, then iterating over the sequence of instructions in this sub-program using `currentBlock` and using `switcher` to parse each instruction using its appropriate function, and return the textual representation of the whole sub-program by appending the representations of all the sequence of instructions.

### `Parse()`

The only function that gets called directly in the start of the execution. This function loads the `JSON` file, parse it, then return the said list of textual representations of sub-programs.

This is done by calling `LoadJson()` first, then it assigns `blocks` using the previous result and calls `StartBlocks()`, after that it iterates over the result of `StartBlocks()` and call `SubProgram(startBlockRef)` on each one and appends the result to the list of programs, and finally it returns the list of programs.

### `MoveSteps(), TurnRight(), TurnLeft(), GotoXY(), ChangeXBy(), SetX(), ChangeYBy(), SetY(), Say(), SayForSecs(), Think(), ThinkForSecs(), WhenFlagClicked(), WhenKeyPressed(), Forever(), If(), IfElse(), Repeat(), Wait(), WaitUntil(), RepeatUntil(), GreaterThanOp(), LessThanOp(), EqualsOp(), NotOp(), OrOp(), AndOp()`

These are the parsing functions which are direcly responsible for parsing each instruction. Each function parses an instruction with the corresponding op-code (according to `switcher`) which is being held in `currentBlock` and returns the textual representation of the instruction `string`.
