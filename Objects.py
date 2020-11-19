

class Object:
    def __init__(self, files, obj):
        self.files = files
        self.name = obj['name']
        self.UID = obj['UID']
        self.effects = obj['effects']
        self.display()

    def isBoost(self, id):
        if next((item for item in self.files['runes']['runes']
        if item['boost']['id'] == id), None):
            return True

    def getName(self, id):
        tmp = next((item for item in self.files['runes']['runes']
        if item['boost']['id'] == id or item['deboost']['id'] == id), None)
        if tmp:
            return tmp['name']
        return 'Unknown stat'

    def displayEffects(self, effects):
        tmp = []
        for effect in effects:
            if not 'name' in effect:
                effect['name'] = self.getName(effect['id'])
            space = '' if effect['name'][0] == '%' else ' '
            dash = '' if self.isBoost(effect['id']) else '-'
            tmp.append(dash + str(effect['value']) + space + effect['name'])
        print(', '.join(tmp), end='')

    def display(self):
        print(self.name + ': ', end='')
        self.displayEffects(self.effects)

class Rune(Object):
    def __init__(self, files, obj):
        super().__init__(files, obj)

    def getPoolOf(self, modif):
        tmp = next((item for item in self.files['runes']['runes']
        if item['boost']['id'] == modif['id']), None)
        if tmp:
            return tmp['pool'] * abs(modif['value'])
        else:
            tmp = next((item for item in self.files['runes']['runes']
            if item['deboost']['id'] == modif['id']), None)
            if tmp:
                return (tmp['pool'] * abs(modif['value'])) / 2
            else:
                return 0

    def getPool(self):
        return self.getPoolOf(self.effects[0])

class Equipment(Object):
    def __init__(self, files, obj):
        super().__init__(files, obj)

    def compareStats(self, effects):
        modifs = []
        trash = []
        for i in range(0, len(self.effects)):
            find = False
            for effect in effects:
                if self.effects[i]['id'] == effect['actionId']:
                    find = True
                    if self.effects[i]['value'] != effect['value']:
                        modifs.append({
                            'id': effect['actionId'],
                            'value': effect['value'] - self.effects[i]['value']
                        })
                        self.effects[i]['value'] = effect['value']
            if find is False:
                modifs.append({
                    'id': self.effects[i]['id'],
                    'value': -self.effects[i]['value']
                })
                trash.append(self.effects[i]['id'])
        self.effects = [d for d in self.effects if not d['id'] in trash]
        for effect in effects:
            find = False
            for i in range(0, len(self.effects)):
                if self.effects[i]['id'] == effect['actionId']:
                    find = True
            if find is False:
                tmp = next((item for item in self.files['runes']['runes']
                if item['boost']['id'] == effect['actionId']
                or item['deboost']['id'] == effect['actionId']), None)
                if tmp:
                    self.effects.append({
                        'id': effect['actionId'],
                        'value': effect['value'],
                        'name': tmp['name'],
                        'pool': tmp['pool']
                    })
                    modifs.append({
                        'id': effect['actionId'],
                        'value': effect['value'],
                    })
        return modifs

    def getCurrentPool(self, pool, msg, rune):
        modifs = self.compareStats(msg['objectInfo']['effects'])
        self.displayEffects(modifs)
        if msg['magicPoolStatus'] in [2, 3]:
            for modif in modifs:
                if modif['value'] < 0:
                    pool += rune.getPoolOf(modif)
            pool -= rune.getPool()
        if pool < 0: pool = 0.0
        return pool

        # magicPoolStatus == 1: = reliquat
        # magicPoolStatus == 2: + reliquat
        # magicPoolStatus == 3: - reliquat
