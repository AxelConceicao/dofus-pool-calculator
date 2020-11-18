import sys
import colorama
from Misc import * # pylint: disable=unused-wildcard-import
from Objects import Equipment, Rune

class Mage:
    messages = {}
    files = {}
    rune = None
    equipment = None
    pool = 0.0

    def __init__(self, protocol, debug):
        self.protocol = protocol
        self.debug = debug
        self.initMethods()
        self.loadFiles()
        for name, _ in self.messages.items():
            msg = next((item for item in self.protocol['messages']
            if item['name'] == name), None)
            if msg is None:
                eprint('Could not find message with name: "' + name + '"')
                exit(1)
            else:
                self.messages[name]['id'] = msg['protocolID']

    def debugLogs(self, id, name, msg):
        print(name + ' (' + str(id) + ')')
        print(msg)

    def handle(self, id, msg):
        if not id in [d['id'] for d in self.messages.values()] : return
        name = list(self.messages.keys())[list([d['id']
        for d in self.messages.values()]).index(id)]
        if self.debug : self.debugLogs(id, name, msg)
        self.messages[name]['method'](msg)

    def objectAdded(self, msg):
        print(Style.BRIGHT + Fore.YELLOW + '[ADD] ' + Style.RESET_ALL, end='')
        try:
            name = self.files['objects'][str(msg['object']['objectGID'])]
        except:
            name = 'Unknown object'
        effects = []
        for effect in msg['object']['effects']:
            tmp = next((item for item in self.files['runes']['runes']
            if item['boost']['id'] == effect['actionId']
            or item['deboost']['id'] == effect['actionId']), None)
            if tmp:
                effects.append({
                    'id': effect['actionId'],
                    'value': effect['value'],
                    'name': tmp['name'],
                    'pool': tmp['pool']
                })
        obj = {
            'name': name,
            'UID': msg['object']['objectUID'],
            'effects': effects
        }
        if len(effects) > 1:
            self.equipment = Equipment(self.files, obj)
        else:
            self.rune = Rune(self.files, obj)
        print()

    def objectRemoved(self, msg):
        print(Style.BRIGHT + Fore.RED + '[REMOVE] ' + Style.RESET_ALL, end='')
        objectUID = msg['objectUID']
        if self.rune and self.rune.UID == objectUID:
            print(self.rune.name, end='')
            # self.rune = None
        elif self.equipment and self.equipment.UID == objectUID:
            print(self.equipment.name, end='')
            self.equipment = None
        print()

    def interfaceOpened(self, msg):
        print(Style.BRIGHT + Fore.WHITE + '[UI] Workschop opened', end='')
        print(Style.RESET_ALL)

    def craftResult(self, msg):
        print(Style.BRIGHT + Fore.CYAN + '[FM] ' + Style.RESET_ALL, end='')
        print(Style.BRIGHT, end='')
        if self.rune is None:
            print('Please add rune first', end='')
        elif self.equipment is None:
            print('Please add equipment first', end='')
        else:
            self.pool = self.equipment.getCurrentPool(self.pool, msg, self.rune)
            print('Remaining Pool: ' + Fore.YELLOW, end='')
            print("%.2f" % round(self.pool, 2), end='')
        print(Style.RESET_ALL)

    def initMethods(self):
        self.messages = {
            'ExchangeObjectAddedMessage': 
            {'id': None, 'method': self.objectAdded},
            'ExchangeObjectRemovedMessage': 
            {'id': None, 'method': self.objectRemoved},
            'ExchangeStartOkCraftWithInformationMessage': 
            {'id': None, 'method': self.interfaceOpened},
            'ExchangeCraftResultMagicWithObjectDescMessage': 
            {'id': None, 'method': self.craftResult},
        }
    
    def loadFiles(self):
        for fp in [
            {'name': 'Objects', 'filename': './json/objects.json'},
            {'name': 'Runes', 'filename':'./json/runes.json'}
        ]:
            if isFileExist(fp['filename']):
                with open(fp['filename'], 'r', encoding='utf-8') as json_file:
                    tmp = json.load(json_file)
            if tmp:
                self.files[fp['name'].lower()] = tmp
                sprint(fp['name'] + ' loaded')
            else:
                eprint('Unable to load ' + fp['filename'])
                exit(1)
        print()