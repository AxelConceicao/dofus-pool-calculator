import sys
from Misc import * # pylint: disable=unused-wildcard-import

OBJECTS_FILENAME = './json/objects.json'
ACTIONIDS_FILENAME = './json/actionIds.json'

class Mage:
    messages = {}
    objects = None
    actionIds = None

    def __init__(self, protocol, debug):
        self.protocol = protocol
        self.debug = debug
        self.initMethods()
        self.loadFiles()
        for name, _ in self.messages.items():
            obj = next((item for item in self.protocol['messages'] if item['name'] == name), None)
            if obj is None:
                eprint('Could not find message with name: "' + name + '"')
                exit(1)
            else:
                self.messages[name]['id'] = obj['protocolID']

    def debugLogs(self, id, name, msg):
        print(name + ' (' + str(id) + ')')
        print(msg)

    def handle(self, id, msg):
        if not id in [d['id'] for d in self.messages.values()] : return
        name = list(self.messages.keys())[list([d['id'] for d in self.messages.values()]).index(id)]
        if self.debug : self.debugLogs(id, name, msg)
        self.messages[name]['method'](msg)
        print('--')

    def itemAdded(self, msg):
        print(self.objects[str(msg['object']['objectGID'])] + ':')
        for effect in msg['object']['effects']:
            print(effect['actionId'])
            obj = next((item for item in self.actionIds.values() if item['id'] == str(effect['actionId'])), None)
            if obj is None:
                wprint('Could not find actionId with id: "' + str(effect['actionId']) + '"')
            else:
                print(obj['fr'])

    def itemRemoved(self, msg):
        print('itemRemoved')

    def interfaceOpened(self, msg):
        print('Interface opened')

    def craftResult(self, msg):
        print('craftResult')

    def initMethods(self):
        self.messages = {
            'ExchangeObjectAddedMessage': {'id': None, 'method': self.itemAdded},
            'ExchangeObjectRemovedMessage': {'id': None, 'method': self.itemRemoved},
            'ExchangeStartOkCraftWithInformationMessage': {'id': None, 'method': self.interfaceOpened},
            'ExchangeCraftResultMagicWithObjectDescMessage': {'id': None, 'method': self.craftResult},
        }
    
    def loadFiles(self):
        if isFileExist(OBJECTS_FILENAME):
            with open(OBJECTS_FILENAME, 'r', encoding='utf-8') as json_file:
                self.objects = json.load(json_file)
        if self.objects:
            sprint('Objects loaded')
        else:
            eprint('Unable to load objects')
            exit(1)
        if isFileExist(ACTIONIDS_FILENAME):
            with open(ACTIONIDS_FILENAME, 'r', encoding='utf-8') as json_file:
                self.actionIds = json.load(json_file)
        if self.actionIds:
            sprint('ActionIds loaded')
        else:
            eprint('Unable to load actionIds')
            exit(1)