'''
Created on May 18, 2013

@author: daniel
'''
import Skype4Py
import cleverbot
import time
from pprint import pprint

class CleverSkype:
    
    def __init__(self):
        self.cb = cleverbot.Session()
        #keeps track of whether the first message has been sent or not
        self.messageIndex = 0;
        self.running = False
        self.skype = Skype4Py.Skype()
        self.skype.Attach()
        
    def start(self):
        self.running = True
        self.skype.OnMessageStatus = self.handleMessages
    
    #stops responding to messages
    def stop(self):
        self.messageIndex = 0
        self.running = False
        self.skype.OnMessageStatus = self.doNothing     
    
    def doNothing(self,msg,status):
        pass
    
    def handleMessages(self, msg, status):
        if status != Skype4Py.cmsReceived:
            return;
        
        #if you are sending to yourself when testing
        if status == "SENDING":
            return
        
        #some skype clients double reply to messages we want to ignore them
        #these messages aren't displayed in UI
        if status == "READ":
            return
        
        #if it is the first message being sent...
        if self.messageIndex == 0:
            msg.Chat.SendMessage('%s isn\'t here right now, but feel free to talk to me, Cleverbot, in the mean time' 
                                 % (self.skype.CurrentUser.FullName))
        else:
            response = self.cb.Ask(msg.Body) 
            msg.Chat.SendMessage(response)
        
        self.messageIndex = self.messageIndex + 1
        
    def getSkype(self):
        #returns skype instance
        return self.skype
        

def main():
    cleverSkype = CleverSkype()
    skype = cleverSkype.getSkype()
      
    while True:
        if skype.CurrentUser.OnlineStatus != Skype4Py.cusDoNotDisturb:
            if cleverSkype.running:
                pprint("stopping...")
                cleverSkype.stop()
            time.sleep(1)
        else:
            if not cleverSkype.running:
                pprint("starting...")
                cleverSkype.start()
            time.sleep(1)  
    
if __name__ == '__main__':
    main()