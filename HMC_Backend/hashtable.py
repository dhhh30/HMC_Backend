
#Hash Table

class HashTable:
    #initialize
    def __init__(self, capacitance):
        self.values = capacitance * [None]
    #return length
    def __len__(self):
        return len(self.values)
    #set an item
    def __setitem__(self, key,value):
        index = hash(key) % len(self)
        self.values[index]=(value)
    #get an item
    def __getitem__(self, key):
        index = hash(key) % len(self)
        return self.values[index]
    