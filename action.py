'''
Basic MCTS implementation
Graeme Best
Oregon State University
Jan 2020
'''

class Action():
    def __init__(self, id, label):
        self.id = id
        self.label = label

    def toString(self):
        return str(self.label)
    def toInt(self):
        return int(self.label)

def printActionSequence(action_sequence):
    action_list = []
    for action in action_sequence:
        print(action.toString() + ", "),
    print("")

def listActionSequence(action_sequence):
    action_list = []
    for action in action_sequence:
        action_list.append(action.label)
    return action_list




# add direction
