

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

    def display(self):
        print(self.name + ': ', end='')
        tmp = []
        for effect in self.effects:
            space = '' if effect['name'][0] == '%' else ' '
            dash = '' if self.isBoost(effect['id']) else '- '
            tmp.append(dash + str(effect['value']) + space + effect['name'])
        print(', '.join(tmp), end='')

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
        for effect in effects:
            for i in range(0, len(self.effects)):
                if self.effects[i]['id'] == effect['actionId']:
                    if self.effects[i]['value'] != effect['value']:
                        modifs.append({
                            'id': effect['actionId'],
                            'value': effect['value'] - self.effects[i]['value']
                        })
                        self.effects[i]['value'] = effect['value']
        return modifs

    def getCurrentPool(self, pool, msg, rune):
        print(msg['magicPoolStatus'], end=' ')
        modifs = self.compareStats(msg['objectInfo']['effects'])
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
