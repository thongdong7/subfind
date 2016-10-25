from subfind_web.bootstrap import container


class ReleaseService(object):
    def list(self):
        return container.get('DataProvider').data
