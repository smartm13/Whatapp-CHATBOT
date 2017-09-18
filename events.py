
def get_current_app_dict(key):
    import json
    with open("current_apps.txt","r") as f:return json.loads(f.read())[key]

def set_current_app_dict(key,value):
    import json
    with open("current_apps.txt","r") as f:old=json.loads(f.read())
    old[key]=value
    new=old
    with open("current_apps.txt","w") as f:f.write(json.dumps(new))


class Event:
    def getstate(self, (s,g), given_appname):
        #serach for (s,g) in all state list with exit =0 and state.appname = give_appname
        return load((s,g),given_appname)
    def getApp(self,(s,g)):
        try:a = get_current_app_dict(g or s)
        except KeyError:
            set_current_app_dict(g or s , 'launcher')
            state=launcher_init((s,g))      #####
            save(state)
            a = get_current_app_dict(g or s)
        return a


def save(state):
    import json
    with open("states-DB.txt","r") as f:old=json.loads(f.read())
    done=0
    for i in range(len(old)):
        k=old[i]['appname']
        if old[i]['appname']==state['appname'] :
            if (old[i]['gid']==state['gid'] and old[i]['gid']) or old[i]['sender']==state['sender']:
                break
    else:
        old.append(state)
        done=1
    if not done:old[i]=state
    new=old
    with open("states-DB.txt","w") as f:f.write(json.dumps(new))

def load((sender,gid),appname):
    import json
    with open("states-DB.txt","r") as f:old=json.loads(f.read())
    for i in range(len(old)):
        if old[i]['appname']==appname:
            if (old[i]['gid']==gid and old[i]['gid']) or old[i]['sender']==sender:
                break
    else:
        print "Init not called.So state not found."
        return 0
    return old[i]

def safe_str(obj):
    """ return the byte string representation of obj """
    try:
        return str(obj)
    except UnicodeEncodeError:
        # obj is unicode
        return unicode(obj).encode('unicode_escape')

def handler(sender, msg, gid, send):
    msg=safe_str(msg)
    print "Heard ({}) :{}".format(safe_str(sender),msg)
    appn = Event().getApp((sender,gid))
    state = Event().getstate((sender,gid), appn)
    state['prams']['newmsg']=msg
    rmsgQ = appcall(state)
    for m in rmsgQ:
        m=safe_str(m)
        print "Replying ({}) :{}".format(safe_str(sender),m)
        send(m)
    return

def appcall(state):
    appname = state['appname']
    prams = state['prams']
    newstateprams, rmq= app2lib(appname)(prams)
    newstate = state
    newstate['prams'] = newstateprams
    save(newstate)
    if newstate['prams']['exit'] and not newstate['appname'] =='launcher':
        set_current_app_dict(state['gid'] or state['sender'] , 'launcher')
        Lstate=load((state['sender'],state['gid']),'launcher')
        Lstate['prams']['exit']=0
        save(Lstate)
    return rmq

def launcher(pstate):
    #generate a new state for approprait app ;//error->//and CALL that app
    msg = pstate['newmsg']
    if pstate['exit'] == 1:print('locha')
    else:pstate['exit']=0
    command = msg.split()[0]
    try:prams = msg.split()[1:]
    except: prams = []
    state = {}
    state['appname'] = command.lower()
    state['sender'] = pstate['sender']
    state['gid'] = pstate['gid']
    if load((state['sender'],state['gid']),state['appname']):
        prams.append(load((state['sender'],state['gid']),state['appname'])['prams'])
    else:prams.append(0)
    appfunc=app2lib(state['appname'] , 1)
    if not appfunc:
        return pstate,["Invalid command. :("]
    state['prams'],rmq = appfunc(prams)
    # newstateprams,rmq=app2lib(state['appname'])(state['prams'])
    # state['prams']=newstateprams
    save(state)
    if not state['prams']['exit']:
        pstate['exit']=1
        set_current_app_dict(pstate['gid'] or pstate['sender'] , state['appname'])
    return pstate,rmq

def launcher_init((sender,gid)):
    state={}
    state['appname']='launcher'
    state['sender']=sender
    state['gid']=gid
    state['prams']={'sender':sender,'gid':gid,'exit':0}
    return state


def app2lib(appname,init = 0) :
    if appname == 'launcher':
        return  launcher_init if init else launcher
    elif appname == 'echo':
        # import echo
        return echo_init if init else echo
    else:
        try:
            externalmodule=__import__(appname)
            with open(appname+".py") as check:pass
            return externalmodule.init if init else externalmodule.app
        except ImportError:
            return 0
        except IOError:
            print "Invalid attempt to open app (in-built.Module):"+appname
            return 0
        except AttributeError:
            print "Invalid Module detected:"+appname
            return 0

def echo_init(initprams):
    rmq=["Welcome to ECHO bot.","I will echo any text."]
    gamedata={}
    gamedata['exit']=0
    return gamedata,rmq

def echo(oldstate):
    msg=oldstate['newmsg']
    if msg.lower()=="exit":
        rmq=["Exited."]
        oldstate['exit']=1
    else:rmq=[msg]
    return oldstate,rmq


def helper(body):print "WAresp:-"+body

if __name__=="__main__":
    send=helper
    while True:
        gid=0
        op=raw_input("Enter sender, msg, gid:")
        try:sender, msg,gid=op.split(',')
        except:sender,msg=op.split(',')
        handler(sender,msg,gid,send)