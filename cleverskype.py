'''
Created on May 18, 2013

@author: daniel
'''
import Skype4Py
import cleverbot
import time
from pprint import pprint
import utils

class CleverSkype:
    
    def __init__(self):
        pprint("Starting Cleverbot session...")
        self.cb = cleverbot.Session()
        pprint("Cleverbot session created.")
        
        #keeps track of the chats that the bot has spoken too
        self.chats = {}
        self.running = False
        pprint("Creating skype...")
        self.skype = Skype4Py.Skype()
        self.skype.Attach()
        pprint("Skype attached.")
        
    def start(self):
        """
        Used to start the bot to listen for incoming messages
        """
        
        pprint("Starting Cleverbot to receive messages.")
        self.running = True
        self.skype.OnMessageStatus = self.handleMessages
    
    #stops responding to messages
    def stop(self):
        """
        Used to stop listening to incoming messages
            
        The bot is still attached to skype    
        """
        pprint("Stopping Cleverbot from receiving messages")
        
        #reset all the chats the bot has spoken too
        self.chats = {}
        self.running = False
        self.skype.OnMessageStatus = self.doNothing     
    
    def doNothing(self,msg,status):
        pass
    
    def handleMessages(self, msg, status):
        """
        Handle incoming messages
        """
        
        if status != Skype4Py.cmsReceived:
            return;
        
        #if you are sending to yourself when testing
        if status == "SENDING":
            return
        
        #some skype clients double reply to messages we want to ignore them
        #these messages aren't displayed in UI
        if status == "READ":
            return
        
        chat = msg.Chat
        
        #if it is the first message being sent...
        chat_id = utils.get_chat_id(chat)
        
        if  chat not in self.chats.values():
            self.chats[chat_id] = chat
            pprint("Sending initial message...")
            pprint(self.sendMessage(chat_id, '%sisn\'t here right now, but feel free to talk to me, Cleverbot, in the mean time' 
                                 % (self.skype.CurrentUser.FullName), msg.FromHandle))
        else:
            pprint("Asking Cleverbot...")
            response = self.cb.Ask(msg.Body) 
            pprint("Sending Cleverbot's response...")
            pprint(self.sendMessage(chat_id, response, msg.FromHandle))
            
    def sendMessage(self, chat_id, msg, person):
        """
        Send Message to chat
        
        :param: chat_id is the string id of a chat
        
        :param: msg is a UTF-8 encoded string
        """
        try:
            self.chats[chat_id].SendMessage("Cleverbot: " + msg)
            return 'Message to %s sent' %(person)
        except KeyError:
            raise RuntimeError("No chat %s" % chat_id)
        
        
    def getSkype(self):
        """
        Exposes skype allows for stateful modules
            
        :return: Active Skype4Py instance
        """
        return self.skype
    
def main():
    cleverSkype = CleverSkype()
    skype = cleverSkype.getSkype()
      
    while 1:
        if skype.CurrentUser.OnlineStatus != Skype4Py.cusDoNotDisturb:
            
            if cleverSkype.running:
                cleverSkype.stop()
        else:
            if not cleverSkype.running:
                cleverSkype.start()
        time.sleep(0.5)  
    
if __name__ == '__main__':
    main()