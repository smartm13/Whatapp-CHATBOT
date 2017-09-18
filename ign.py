import requests, json
from pprint import pprint

def ign(que):
 #   q=que.split()
    #url='GEThttps://videogamesrating.p.mashape.com/get.php?count=5&game=%s' %('god of war')
    response = requests.get("https://videogamesrating.p.mashape.com/get.php?count=5&game=%s" %(que),
  headers={
    "X-Mashape-Key": "B3ZqqMVtsnmshfQsRPiz7y3bRZCnp1e28evjsnCjOU44qXH7V2",
    "Accept": "application/json"
  }
)
    response.raise_for_status

    gamedata=json.loads(response.text)
    #pprint((gamedata[0]))
    #print(gamedata['title'])
    resultlist=[]
    try:
        resultlist.append('Title: ' + gamedata[0]['title'])
        resultlist.append('Score: ' + gamedata[0]['score'])
        resultlist.append('Platforms: ' + str(gamedata[0]['platforms']))
        resultlist.append('Desc: ' + gamedata[0]['short_description'])
    except:resultlist.append("Not Found")
    resultstr='\n'.join(resultlist)
    return resultstr
    
def app(dict):
	l=[]
	msg = dict['newmsg']
	if msg.lower() == 'exit':
		dict['exit']=1
		return dict, l
	else:
				l.append(ign(msg))
				return dict, l


def init(li):
	d = {}
	l=[]
	d['exit'] = 0
	if li[:-1]:
		d['exit'] = 1 
		l.append(ign(' '.join(li[:-1])))
		return d,l
	else:
		l.append('welcome to ign')
		return d,l
		
if __name__=='__main__':
	d,l=init([0])
	for s in l:print(s)
	while True:
		d['newmsg'] = raw_input('eneter movie name')
		d,l=app(d)
		for s in l:print(s)

		
