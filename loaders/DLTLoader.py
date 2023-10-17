import sys
sys.path.append('libs/python-dlt')

from dlt import dlt


class DLTLoader:
    def __init__(self, filename):
        self.msgs = dlt.load(filename)
        self.msgs.generate_index()  # let it read all the messages

    def get_messages(self):
        return self.msgs