import turtle
import math
import random
import sympy as sp
import numpy
import re

disallowedX = []
allowedx = []

def parse_math_expression(expr_str):
    # Define the symbol 'x' for the variable in the expression
    x = sp.symbols('x')
    
    # Parse the input expression
    parsed_expr = sp.sympify(expr_str)
    
    # Simplify the expression
    simplified_expr = sp.simplify(parsed_expr)
    
    # Create a Python function from the simplified expression
    f = sp.lambdify(x, simplified_expr, 'numpy')
    
    return f

#defualt settings
windowWidth = 1000
windowHeight = 500
scale = 50
xintdelay = 20
verbose = False
label = True
step = 1

raw = input("Enter Function: ")
rawList = re.split(r'[=,!]', raw)
rawFunc = rawList[0]
for i in range(len(rawList)):
    if rawList[i] == "height":
        windowHeight = int(rawList[i+1])
    if rawList[i] == "width":
        windowWidth = int(rawList[i+1])
    if rawList[i] == "scale":
        scale = int(rawList[i+1])
    if rawList[i] == "xintdelay":
        xintdelay = int(rawList[i+1])
    if rawList[i] == "verbose":
        verbose = bool(rawList[i+1])
    if rawList[i] == "label":
        label = bool(rawList[i+1])
    if rawList[i] == "step":
        step = bool(rawList[i+1])

f = parse_math_expression(rawFunc)

#init
window = turtle.Screen()
window.setup(width = windowWidth, height = windowHeight)
pointer = turtle.Turtle()
pointer.speed(-1)

nullWidth = -1*(windowWidth/2)
nullHeight = -1*(windowHeight/2)
allowx = True
sincex = 0

for i in range(int(windowWidth)):
    try:
        test = round(f(((nullWidth + i)/scale)) * scale)
        if verbose: print(f"Tested {i}")
        allowedx.append((nullWidth+i)/scale)
    except:
        if verbose: print(f"Error at x={(nullWidth + i)/scale}, ({i})")
        disallowedX.append(int(i))
        

#vertical axis
pointer.penup()
pointer.goto(0, windowHeight/2)
pointer.pendown()
pointer.goto(0, nullHeight)
pointer.penup()

#horzizontal axis
pointer.goto(nullWidth, 0)
pointer.pendown()
pointer.goto(windowWidth/2, 0)
pointer.penup()

#add axis labels
for i in range(int(windowHeight/scale)):
    pointer.goto(0, (math.floor((nullHeight + (i+1) * scale)/scale))*scale)
    pointer.pendown()
    pointer.write(math.floor((nullHeight + (i+1) * scale)/scale), align="right", font=("Arial", 12, "normal"))
    pointer.penup()

for i in range(int(windowWidth/(scale))):
    if math.floor((nullWidth + (i+1) * scale)/(scale)) != 0:
        pointer.goto(math.floor(((nullWidth + (i+1) * scale)/scale)*scale), -25)
        pointer.pendown()
        pointer.write(math.floor((nullWidth + (i+1) * scale)/(scale)), align="center", font=("Arial", 12, "normal"))
        pointer.penup()

#initialize pointer
try:
    if verbose == True: print(f(nullWidth))
    if f(nullWidth) < windowHeight/2:
        pointer.goto(nullWidth, nullHeight)
    elif f(nullWidth) > windowHeight/2:
        pointer.goto(nullWidth, windowHeight/2)
    else:
        pointer.goto(nullWidth, f(nullWidth))
except: 
    pointer.goto(nullWidth, nullHeight)

#graph f(x)
scaledDisX = []
dele = ", "
for i in range(len(disallowedX)):
    if ((nullWidth + disallowedX[i])/scale) > min(allowedx) and ((nullWidth + disallowedX[i])/scale) < max(allowedx):
        scaledDisX.append(str((nullWidth + disallowedX[i])/scale))
stringScaledDisX = dele.join(scaledDisX)
pointer.goto(nullWidth + 15, windowHeight/2 - 25)
if stringScaledDisX != '':
    print(f"Graphing over domain x ∈ [{min(allowedx)}, {max(allowedx)}] \\ {{{stringScaledDisX}}}")
    pointer.pendown()
    pointer.write(f"{rawFunc} for x ∈ [{min(allowedx)}, {max(allowedx)}] \\ {{{stringScaledDisX}}}", align="left", font=("Arial", 12, "normal"))
    pointer.penup()
else:
    print(f"Graphing over domain x ∈ [{min(allowedx)}, {max(allowedx)}]")
    pointer.pendown()
    pointer.write(f"{rawFunc} for x ∈ [{min(allowedx)}, {max(allowedx)}]", align="left", font=("Arial", 12, "normal"))
    pointer.penup()
pointer.pencolor("blue")
for i in range(int(windowWidth/step)):
    ex = nullWidth + i + step
    if i not in disallowedX and i + step not in disallowedX:
        y = round(f(((nullWidth + i)/scale)) * scale)
        if verbose: print(f"({ex}, {y})")
        if y < windowHeight and y > nullHeight:
            next = round(f(((nullWidth + i + step)/scale)) * scale)
            pointer.penup()
            pointer.goto(ex, y)
            pointer.pendown()
            pointer.goto(ex + step, next)
            previous = y
            if ex == 0 and y != 0:
                pointer.write(f"({ex/scale}, {y/scale})", align="center", font=("Arial", 12, "normal"))
            if previous * next < 0 and allowx == True:
                pointer.write(f"({ex/scale}, {0})", align="center", font=("Arial", 12, "normal"))
                allowx = False
            if y == 0 and ex != 0 and allowx == True:
                pointer.write(f"({ex/scale}, {0})", align="center", font=("Arial", 12, "normal"))
                allowx = False
            if y == 0 and ex == 0 and allowx == True:
                pointer.write(f"({0}, {0})", align="right", font=("Arial", 12, "normal"))
                allowx = False
            if allowx == False:
                sincex = sincex + 1
            if sincex > xintdelay:
                allowx = True
                sincex = 0
            
            pointer.penup()
        else:
            pointer.penup()
    else:
        pointer.penup()

window.exitonclick()