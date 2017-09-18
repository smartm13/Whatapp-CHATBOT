import requests, json
#from pprint import pprint

def imdb(que):
	titlename=que
	url = 'http://www.omdbapi.com/?t=%s&plot=short&apikey=5ed92a6d' %(titlename)
	response = requests.get(url)
	response.raise_for_status

	moviedata=json.loads(response.text)
	#pprint(moviedata)
	resultlist=[]
	try:
		resultlist.append('Title: ' + moviedata['Title'])
		resultlist.append('Genre: ' + moviedata['Genre'])
		resultlist.append('imdbRating: ' + moviedata['imdbRating'])
		resultlist.append('Plot: ' + moviedata['Plot'])
	except:resultlist.append("Not Found")
	resultstr='\n'.join(resultlist)
	#print(resultstr)
	return resultstr
def tmdb(que):
	titlename=que
	url = 'http://api.themoviedb.org/3/search/movie?api_key=e7b8b1a89879879cda0dd1f3ae062d0a&query=%s' %(titlename)
	response = requests.get(url)
	#response.raise_for_status()

	moviedata=json.loads(response.text)
	#pprint(moviedata)
	resultlist=[]
	try:
		resultlist.append('Title: ' + moviedata['results'][0]['original_title'])
		resultlist.append('tmdbRating: ' + str(moviedata['results'][0]['vote_average']))
		resultlist.append('tmdbPopularity: ' + str(moviedata['results'][0]['popularity']))
		resultlist.append('Plot: ' + moviedata['results'][0]['overview'])
	except:resultlist.append("error Found")
	resultstr='\n'.join(resultlist)
	#print(resultstr)
	return resultstr
imdb=tmdb
#print(imdb('dark'))
#if __name__ == '__imdb__':
	
def app(dict):
	l=[]
	msg = dict['newmsg']
	if msg.lower() == 'exit':
		l.append('exiting imdb...')
		dict['exit']=1
		return dict, l
	else:
				l.append(imdb(msg))
				return dict, l

def init(li):
	d = {}
	l=[]
	d['exit'] = 0
	if li[:-1]:
		d['exit'] = 1 
		l.append(imdb(' '.join(li[:-1])))
		return d,l
	else:
		l.append('welcome to imdb')
		return d,l
		
if __name__=='__main__':
	d,l=init([0])
	for s in l:print(s)
	while True:
		d['newmsg'] = raw_input('eneter movie name')
		d,l=app(d)
		for s in l:print(s)

		
		
	

