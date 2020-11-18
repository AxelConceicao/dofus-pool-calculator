

class Object:
    def __init__(self, name, effects):
        print(name + ': ', end='')
        self.name = name
        self.effects = effects

class Rune(Object):
    def __init__(self, name, effects):
        super().__init__(name, effects)

class Equipment(Object):
    def __init__(self, name, effects):
        super().__init__(name, effects)