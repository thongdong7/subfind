class EventManager(object):
    def __init__(self):
        self.data = {}

    def register(self, name, listener):
        if name not in self.data:
            self.data[name] = []

        self.data[name].append(listener)

    def notify(self, name, event):
        for listener in self.data.get(name, []):
            listener(event)