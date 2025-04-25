import time, sys

def zigzag():
    i = 0
    indent = 0
    indentIncreasing = True
    while i<2:
        print(' '*indent, end='')
        print('********')
        time.sleep(0.1)

        if indentIncreasing:
            indent += 1
            if indent == 20:
                indentIncreasing = False #change direction
                i += 1
        
        else:
            indent -= 1
            if indent == 0:
                indentIncreasing = True

zigzag()
