from __future__ import unicode_literals
from yowsup.layers.interface.interface import YowInterfaceLayer
from yowsup.layers.protocol_media.layer import RequestUploadIqProtocolEntity
from yowsup.layers.protocol_media.mediauploader import MediaUploader
from yowsup.layers.protocol_media.layer import ImageDownloadableMediaMessageProtocolEntity
from yowsup.layers.protocol_media.layer import AudioDownloadableMediaMessageProtocolEntity
from yowsup.layers.protocol_media.layer import VideoDownloadableMediaMessageProtocolEntity
import sys,os

class MyYowsupApp(YowInterfaceLayer):
    # def requestImageUpload(self, imagePath,number):
    #     self.demoContactJid = number #only for the sake of simplicity of example, shoudn't do this
    #     self.filePath = imagePath #only for the sake of simplicity of example, shoudn't do this
    #     requestUploadEntity = RequestUploadIqProtocolEntity(RequestUploadIqProtocolEntity.MEDIA_TYPE_VIDEO, filePath = imagePath)
    #     self._sendIq(requestUploadEntity, self.onRequestUploadResult, self.onRequestUploadError)
    #
    # def onRequestUploadResult(self, resultRequestUploadIqProtocolEntity, requestUploadIqProtocolEntity):
    #     mediaUploader = MediaUploader(self.demoContactJid, self.getOwnJid(), self.filePath,
    #                                   resultRequestUploadIqProtocolEntity.getUrl(),
    #                                   resultRequestUploadIqProtocolEntity.getResumeOffset(),
    #                                   self.onUploadSuccess, self.onUploadError, self.onUploadProgress)
    #     mediaUploader.start()
    #
    # def onRequestUploadError(self, errorRequestUploadIqProtocolEntity, requestUploadIqProtocolEntity):
    #     print("Error requesting upload url")
    #
    # def onUploadSuccess(self, filePath, jid, url):
    #     #convenience method to detect file/image attributes for sending, requires existence of 'pillow' library
    #     entity = ImageDownloadableMediaMessageProtocolEntity.fromFilePath(filePath, url, None, to)
    #     self.toLower(entity)
    #
    # def onUploadError(self, filePath, jid, url):
    #     print("Upload file failed!")

    respLog=[]
#COPIED FROM CLI
    def video_send(self, number, path, caption = None):
        self.media_send(number, path, RequestUploadIqProtocolEntity.MEDIA_TYPE_VIDEO)
    def media_send(self, number, path, mediaType, caption = None):
        jid = number
        entity = RequestUploadIqProtocolEntity(mediaType, filePath=path)
        successFn = lambda successEntity, originalEntity: self.onRequestUploadResult(jid, mediaType,
                            path, successEntity, originalEntity, caption)
        errorFn = lambda errorEntity, originalEntity: self.onRequestUploadError(jid, path, errorEntity, originalEntity)
        print "in media send:"+str((jid,path))
        self._sendIq(entity, successFn, errorFn)

        self._sendIq(entity, successFn, errorFn)


    def onRequestUploadResult(self, jid, mediaType, filePath, resultRequestUploadIqProtocolEntity, requestUploadIqProtocolEntity,
                              caption = None):
        print "aat."
        if resultRequestUploadIqProtocolEntity.isDuplicate():
            self.doSendMedia(mediaType, filePath, resultRequestUploadIqProtocolEntity.getUrl(), jid,
                             resultRequestUploadIqProtocolEntity.getIp(), caption)
        else:
            successFn = lambda filePath, jid, url: self.doSendMedia(mediaType, filePath, url, jid,
                                                                    resultRequestUploadIqProtocolEntity.getIp(), caption)
            mediaUploader = MediaUploader(jid, self.getOwnJid(), filePath,
                                      resultRequestUploadIqProtocolEntity.getUrl(),
                                      resultRequestUploadIqProtocolEntity.getResumeOffset(),
                                      successFn, self.onUploadError, self.onUploadProgress, async=False)
            print "Starting upload."
            mediaUploader.start()

    def onRequestUploadError(self, jid, path, errorRequestUploadIqProtocolEntity, requestUploadIqProtocolEntity):
        self.respLog.append("Request upload for file %s for %s failed" % (path, jid))
        print ("Request upload for file %s for %s failed" % (path, jid))

    def onUploadError(self, filePath, jid, url):
        self.respLog.append("Upload file %s to %s for %s failed!" % (filePath, url, jid))
        print ("Upload file %s to %s for %s failed!" % (filePath, url, jid))

    def onUploadProgress(self, filePath, jid, url, progress):
        sys.stdout.write("%s => %s, %d%% \r" % (os.path.basename(filePath), jid, progress))
        sys.stdout.flush()
        print "wrking"

    def doSendMedia(self, mediaType, filePath, url, to, ip = None, caption = None):
        if mediaType == RequestUploadIqProtocolEntity.MEDIA_TYPE_IMAGE:
            entity = ImageDownloadableMediaMessageProtocolEntity.fromFilePath(filePath, url, ip, to, caption = caption)
        elif mediaType == RequestUploadIqProtocolEntity.MEDIA_TYPE_AUDIO:
            entity = AudioDownloadableMediaMessageProtocolEntity.fromFilePath(filePath, url, ip, to)
        elif mediaType == RequestUploadIqProtocolEntity.MEDIA_TYPE_VIDEO:
            entity = VideoDownloadableMediaMessageProtocolEntity.fromFilePath(filePath, url, ip, to, caption = caption)
        print "sending to u."
        self.toLower(entity)


def downloadyt(url):
    import youtube_dl,os
    ydl_opts = {'format': 'best[height<500]'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        #ydl.download([url])
        data =  (ydl.extract_info(url=url,download = False ))
    #path = os.getcwd()
    #files = []
    #print(title)
    #for i in os.listdir(path):
    #    if os.path.isfile(os.path.join(path, i)) and i.split()[0] == title.split()[0]:
    #        files.append(os.path.join(path, i))
#    return files[0]
    return data#"/home/smartm13/video.mp4"#files[0]


def youtb(msg):
    rsptxt=[]
    #msg=" ".join(msg)
    no=msg.split()[0]
    print "MSG GOT="+msg
    if "http://" in msg or "https://" in msg:
        #extract url
        # protocal="http://" if "https://" in msg else "https://"
        # st=msg.find(protocal)
        # end=msg.find(str(' '),st)
        # if end==-1:end=None
        url=msg.split()[1]#[st:end]
        filename=downloadyt(url)
        #wavideo=MyYowsupApp()
        #wavideo.video_send(no,filename)
        rsptxt+=["Sending video: "]+filename['url']
        # import time
        # time.sleep(10)

    else:
        rsptxt.append("No url Found. Search by text not implemented yet.")#search by text and get 1st video avail.
    # rsptxt+=["Sending video: "]+wavideo.respLog
    return rsptxt

def init(initpram): #expecting senderNo in initpram to send video independently
    d={}
    l=[]
    d['exit'] = 0
    #d['user']=initpram[0]
    if initpram[:-1]:
        d['exit'] = 1
        l.append(youtb(' '.join(initpram[:-1])))
        return d,l
    else:
        l.append('welcome to Youtube (sending-{})')#.format(d['user']))
        return d,l

def app(prams):
    l=[]
    msg = prams['newmsg']
    if msg.lower() == 'exit':
        l.append('exiting Youtube...')
        prams['exit']=1
        return prams, l
    else:
                l.append(youtb(msg))
                return prams, l
