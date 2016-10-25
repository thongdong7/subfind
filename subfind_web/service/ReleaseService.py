from subfind_web.bootstrap import container


class ReleaseService(object):
    def __init__(self):
        self.config = container.get('Config')
        self.sub_finder = container.get('SubFinder')
        self.data_provider = container.get('DataProvider')

    def list(self):
        return self.data_provider.data

    def scan_all(self):
        self.sub_finder.scan(self.config['src'])

        self.data_provider.build_data()

        return True
