import json
import os
import random
from datetime import datetime
from datetime import timedelta
from datetime import date
from datetime import time

class SimpleMotd():
    time_period = "day"
    folder = "messages"
    selection_type = "random"
    last_message = ""
    last_datetime = datetime.now()

    def __init__(self, external_config_json_file=None):
        attrs = {}
        config_json_file = ""
        # checking wheter external configuration file provided
        if external_config_json_file is not None:
            config_json_file = external_config_json_file
        else:
            config_json_file = os.path.join(os.path.dirname(__file__),'config.json')
        # opening the file
        try:
            with open(config_json_file, "r") as file:
                attrs = json.load(file)
        except IOError as e:
            print("simplemotds Error: could not open", config_json_file, str(e))
            self.time_period = "day"
            self.folder = "messages"
            self.selection_type = "random"
            self.last_datetime = datetime.now()
            self.last_message = ''
            return
        # checking values
        time_period = attrs.get('time-period', None)
        folder = attrs.get('folder', None)
        selection_type = attrs.get('selection-type', None)
        if time_period is not None:
            if time_period == 'day' or time_period == 'month' \
              or time_period == 'week' or time_period == 'hour' \
              or time_period == 'minute':
                self.time_period = time_period
        if folder is not None:
            if folder == "./messages" or folder == "messages" or \
              folder == "messages/":
                self.folder = os.path.join(os.path.dirname(__file__), 'messages')
            else:
                self.folder = folder
        if selection_type is not None:
            if selection_type == 'random' or \
              selection_type == 'alphabetically-desc' or \
              selection_type == 'alphabetically-asc' or \
              selection_type == 'modification-asc' or \
              selection_type == 'modification-desc':
                self.selection_type = selection_type

    def getMotdContent(self):
        if not self.checkTimePeriod():
            with open(os.path.join(self.folder, self.last_message)) as file:
                return file.read()
        # new message
        filename = self.getNextMessageFileName()
        with open(os.path.join(self.folder, filename)) as file:
            self.last_datetime = datetime.now()
            self.last_message = filename
            return file.read()
        return None # error

    def getMotdFile(self):
        if not self.checkTimePeriod():
            with open(os.path.join(self.folder, self.last_message)) as file:
                return file
        filename = self.getNextMessageFileName()
        with open(os.path.join(self.folder, filename)) as file:
            self.last_datetime = datetime.now()
            self.last_message = filename
            return file
        return None # error

    def getMotdFileName(self):
        if not self.checkTimePeriod():
            return self.last_message
        self.last_datetime = datetime.now()
        self.last_message = self.getNextMessageFileName()
        return self.last_message

    def ForceNextMessage(self):
        self.last_message = ''
        return self.getMotdFileName()
        
    # selection Message methods
    def getNextMessageFileName(self):
        if self.selection_type == 'random':
            return self.getNextRandomMessageFileName()
        if self.selection_type == 'alphabetically-desc':
            return self.getNextAlphabeticallyFileName(False)
        if self.selection_type == 'alphabetically-desc':
            return self.getNextAlphabeticallyFileName(True)
        if self.selection_type == 'modification-asc':
            return self.getNextModificationFileName(True)
        if self.selection_type == 'modification-desc':
            return self.getNextModificationFileName(False)
        
    # helpers
    def getMessagesFileNames(self):
        file_names = []
        try:
            for p,d,file_names in os.walk(self.folder):
                pass
        except OSError:
            print ("Can't os.walk() on",self.folder)
            return []
        else:
            return file_names

    def getNextIndexFileNamesList(self, file_names):
        index = file_names.index(self.last_message)
        if index+1 == len(file_names):
            return 0
        return index + 1
        
    def getNextRandomMessageFileName(self):
        file_names = self.getMessagesFileNames()
        return file_names[int(random.random()*len(file_names))]

    def getNextAlphabeticallyFileName(self, asc=True):
        file_names = self.getMessagesFileNames()
        file_names.sort()
        if asc == False:
            file_names.reverse()

        if len(file_names == 0):
            # no files
            return ''
        if self.last_message == '':
            return file_names[0]
        index = self.getNextIndexFileNamesList(file_names)
        return file_names[index]
            
    def getNextModificationFileName(self, asc=True):
        mods = []
        file_names = self.getMessagesFileNames()
        for f in file_names:
            mods.append((os.path.getmtime(os.path.join(self.folder, f)), f))
        mods.sort()
        if asc == False:
            mods.reverse()

        if len(mods == 0):
            return ''
        file_names = []
        for f in mods:
            file_names.append(f[1])
            
        if self.last_message == '':
            return file_names[0]
        index = self.getNextIndexFileNamesList(file_names)
        return file_names[index]
    
    def checkTimePeriod(self):
        ''' Returns true when enough time has passed to get a new message 
        '''
        if self.last_message == '':
            # no message previously selected so need to get one
            return True

        now = datetime.now()
        if self.time_period == 'month':
            return ((now - self.last_datetime).days >= 30)
        elif self.time_period == 'week':
            return ((now - self.last_datetime).days >= 7)
        elif self.time_period == 'day':
            return ((now - self.last_datetime).days >= 1)
        elif self.time_period == 'hour':
            return ((now - self.last_datetime).total_seconds() >= 3600)
        elif self.time_period == 'minute':
            return ((now - self.last_datetime).total_seconds() >= 60)
        
        return True
        
