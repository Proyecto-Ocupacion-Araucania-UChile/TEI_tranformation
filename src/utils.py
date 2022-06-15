import os

class Tools:

    def __init__(self, path, _current_path, name):
        self.path = os.path.join(_current_path, path)
        self.name = name

    def read_file(self):
        """
        do class method ?
        :return:
        """
        with open(f"{self.path}/'{self.name}") as f:
            return f.read()

    def verification(self):
        """
        verication of exitence of files associated
        :return:
        """
        return

class DataTools:

    def generate_id(cls):
        """
        find id if existing in JSON files, if not to create it
        :return:
        """
