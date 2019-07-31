from configparser import ConfigParser
import os

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
        # create folder if does not exist
        self.__dest_folder_exist(self.filepath)
        return self.filepath

    def __dest_folder_exist(self, name):
        # remove last item in path, and check if folder exists
        # if it does not, then check if root exists and then create
        this_folder = os.path.dirname(name)
        if this_folder > '':
            if not os.path.exists(this_folder):
                self.__dest_folder_exist(this_folder)
            os.makedirs(this_folder, exist_ok=True)
        return


