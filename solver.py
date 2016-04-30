from collections import namedtuple

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
 
app = Flask(__name__)

OpInfo = namedtuple('OpInfo', 'prec assoc')
L, R = 'Left Right'.split()
 
ops = {
 '^': OpInfo(prec=4, assoc=R),
 '*': OpInfo(prec=3, assoc=L),
 '/': OpInfo(prec=3, assoc=L),
 '+': OpInfo(prec=2, assoc=L),
 '-': OpInfo(prec=2, assoc=L),
 '(': OpInfo(prec=9, assoc=L),
 ')': OpInfo(prec=0, assoc=L),
 }
 
NUM, LPAREN, RPAREN = 'NUMBER ( )'.split()
 
 
def get_input(inp = None):
    'Inputs an expression and returns list of (TOKENTYPE, tokenvalue)'
 
    if inp is None:
        inp = input('expression: ')
    tokens = inp.strip().split()
    tokenvals = []
    for token in tokens:
        if token in ops:
            tokenvals.append((token, ops[token]))
        #elif token in (LPAREN, RPAREN):
        #    tokenvals.append((token, token))
        else:    
            tokenvals.append((NUM, token))
    return tokenvals
 
def shunting(tokenvals):
    outq, stack = [], []
    for token, val in tokenvals:
        note = action = ''
        if token is NUM:
            outq.append(val)
        elif token in ops:
            t1, (p1, a1) = token, val
            while stack:
                t2, (p2, a2) = stack[-1]
                if (a1 == L and p1 <= p2) or (a1 == R and p1 < p2):
                    if t1 != RPAREN:
                        if t2 != LPAREN:
                            stack.pop()
                            outq.append(t2)
                        else:    
                            break
                    else:        
                        if t2 != LPAREN:
                            stack.pop()
                            outq.append(t2)
                        else:    
                            stack.pop()
                            break
                else:
                    break
            if t1 != RPAREN:
                stack.append((token, val))

    while stack:
        t2, (p2, a2) = stack[-1]
        stack.pop()
        outq.append(t2)
    return outq
 
def is_number(s):
    try:
        complex(s) # for int, long, float and complex
    except ValueError:
        return False

    return True

@app.route('/solve', methods=['GET', 'POST'])
def solver():
        a = [x.encode('utf-8') for x in request.args.get('exp')]
        a = " ".join(a)
        expression = shunting(get_input(a))
        stack = []
	for t1 in expression:
		if(is_number(t1)):
			stack.append(float(t1))
		else:
			t3 = stack[-1]
			stack.pop()
			t2 = stack[-1]
			stack.pop()
			if t1 == '*':
				stack.append(t2*t3+0.0)

			elif t1 == '/':
				if(t3 !=0):
					stack.append(t2/t3+0.0)
			elif t1 == '+':
				stack.append(t2+t3+0.0)
			elif t1 == '-':
				stack.append(t2-t3+0.0)
			elif t1 == '^':
				stack.append(t2**t3+0.0)

        print stack[0]
	return str(stack[0])

@app.route('/database', methods=['GET', 'POST'])
def database():
    #do nothing
    i = 3

if __name__ == '__main__':
    app.run()
