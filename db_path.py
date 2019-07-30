from configparser import ConfigParser

class DbPath:

    def __init__(self):
        self.filepath = ''
        try:
            config = ConfigParser()
            config.read('./config.ini')
            self.filepath = config.get('DATABASE', 'Path')
        except Exception as e:
            print('Error Access ini file: ' + str(e)  )

    def database_path(self):
        return self.filepath

