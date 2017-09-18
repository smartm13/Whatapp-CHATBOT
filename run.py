from yowsup.stacks import  YowStackBuilder
from layer import EchoLayer
from yowsup.layers.auth import AuthError
from yowsup.layers import YowLayerEvent
from yowsup.layers.network import YowNetworkLayer


class YowsupEchoStack(object):
    def __init__(self, credentials, encryptionEnabled = True):
        stackBuilder = YowStackBuilder()

        self.stack = stackBuilder\
            .pushDefaultLayers(encryptionEnabled)\
            .push(EchoLayer)\
            .build()

        self.stack.setCredentials(credentials)

    def start(self):
        self.stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        try:
            self.stack.loop()
        except AuthError as e:
            print("Authentication Error: %s" % e.message)


if __name__=="__main__":
    #from yowsup.demos import echoclient
    credentials = ("917069144898", "DinPhulXbC98ro9bF62CT3VbMPo=") #<-enter new no.&pass here. this one is banned already.
    if not credentials:
        print("Error: You must specify a configuration method")
        exit(1)
    try:
    #self.printInfoText()
        stack = YowsupEchoStack(credentials)
        stack.start()
    except KeyboardInterrupt:
        print("\nYowsdown")
        exit(0)
