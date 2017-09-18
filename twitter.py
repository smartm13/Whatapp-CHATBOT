

def tw(str):
	import twitter
	my_auth = twitter.OAuth('276076944-N9CrSIpJWjFV5iWh0ze8LDmk1QvFCV73apWxP20Y','qVFr2W4RH5lMFyIKztLZYcSQZ3iMNS94RW2tPMUdLHiRk','WV2XzLQbk7VBs5MTC7LQhUggS','wwJRaF1VlufS25AeIMUHL6hfVglJ19unWNGd0FYvdXOsL1mI6K')
	twit = twitter.Twitter(auth=my_auth)
	o=twit.statuses.update(status=str)
	return '@'+o['user']['screen_name']+' tweeted: '+o['text']


def app(dict):
	l=[]
	msg = dict['newmsg']
	if msg.lower() == 'exit':
		l.append('exiting twitter...')
		dict['exit']=1
		return dict, l
	else:
				l.append(tw(msg))
				return dict, l

def init(li):
	d = {}
	l=[]
	d['exit'] = 0
	if li[:-1]:
		d['exit'] = 1
		l.append(tw(' '.join(li[:-1])))
		return d,l
	else:
		l.append('welcome to twitter')
		return d,l

if __name__=='__main__':
	d,l=init([])
	for s in l:print(s)
	while True:
		d['newmsg'] = raw_input('eneter movie name')
		d,l=app(d)
		for s in l:print(s)

