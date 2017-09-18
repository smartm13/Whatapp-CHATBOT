#initial_stack =13
#current_stack = initial_stack

def getmove(current_stack):
    taken = findgoodmove(current_stack)
    if (taken == -1):
        taken =1
    return taken

def findgoodmove(current_stack):
    for i in range(1,4):
        if isbadpos(current_stack - i):
            return i
    return -1
def isbadpos(current_stack):
    if current_stack==1:
        return True
    return findgoodmove(current_stack) == -1



def init(li):
	d = {}
	l = []
	d['exit'] = 0
	if li[:-1]:
		d['cur_stack'] = int(li[0])
		#return d, l
	elif li[-1]:
		if li[-1]['cur_stack']>=2:
			l.append('Resuming nim. ({})'.format(li[-1]['cur_stack']))
			d=li[-1]
			d['exit']=0
		else:
			d['cur_stack'] =13
			l.append('welcome to nim')
	else:
		d['cur_stack'] =13
		l.append('welcome to nim')
	return d,l

		
		
def app(dict):
	l=[]
	msg = dict['newmsg']
	if msg.lower() == 'exit':
		dict['exit']=1
		return dict, l
	else:		
				if (not msg.isdigit()) or (int(msg) not in range(1,4)): 
					l.append("illigal input")
					return dict, l
				dict['cur_stack']-=int(msg)
				l.append("now stack has "+str(dict['cur_stack']) + " coins")
				if dict['cur_stack']<2:
					l.append("game over. you win")
					dict['exit'] = 1
					return dict, l
				else:
					comptakes = getmove(dict['cur_stack'])
					dict['cur_stack']-=comptakes
					l.append('I\'ll take '+str(comptakes) + 'now stack has '+str(dict['cur_stack']) + ' coins')
					if dict['cur_stack']<2:
						l.append('game over. you lose')
						dict['exit'] =1
						return dict, l
					else:
						l.append('How many would you take?')
						return dict, l
					
if __name__=='__main__':
	d,l=init([])
	for s in l:print(s)
	while True:
		d['newmsg'] = raw_input('eneter movie name')
		d,l=app(d)
		for s in l:print(s)

		

