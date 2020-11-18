

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

class Equipment(Object):
    def __init__(self, files, obj):
        super().__init__(files, obj)