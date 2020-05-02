import random
import time

k = 10
alpha = 8
beta = 25
num_correct = 80
num_byzantine = 0

class Node():
    def __init__(self, color, _id, byz):
        self.color = color
        self.id = _id
        self.conf = 1
        self.weight_red = 0
        self.weight_blue = 0
        self.byz = byz
        self.committed = False

    def init_neighbors(self, neighbors):
        self.neighbors = neighbors[:]
        del self.neighbors[self.id]

    def get_color(self, color_of_sampling_node, id_of_sampling_node):
        if not self.byz:
            return self.color
        else:
            # Byz node
            ''' Strategy #1: 
            Byz nodes will always answer with 0 to all correct nodes in index 
            range (0, num_correct//2), and 1 to the other half.
            '''
            if id_of_sampling_node <= num_correct//2:
                return 0
            else:
                return 1

    def sample(self):
        global k
        global alpha
        global beta
        global num_correct
        sample = random.sample(self.neighbors, k)
        sample = [i.get_color(self.color, self.id) for i in sample]
        if sample.count(0) >= alpha:
            self.weight_red += 1 
            if self.color == 0:
                self.conf += 1
            elif self.color == 1:
                self.conf = 1
        elif sample.count(1) >= alpha:
            self.weight_blue += 1 
            if self.color == 1:
                self.conf += 1
            elif self.color == 0:
                self.conf = 1
        else:
            self.conf = 1

        if self.weight_red > self.weight_blue:
            self.color = 0
        elif self.weight_blue > self.weight_red:
            self.color = 1

        if self.conf == beta:
            self.committed = True
            return 1
        else:
            return 0


def main():
    global num_correct
    global num_byzantine
    for trial in range(1):
        nodes = []
        for i in range(num_correct):
            nodes.append(Node(i%2, i, False))
        for i in range(num_byzantine):
            nodes.append(Node(0, num_correct+i, True))
        for i in range(num_correct+num_byzantine):
            nodes[i].init_neighbors(nodes)
        num_committed = 0
        _round = 0
        while(True):
            time.sleep(0.05)
            print(_round, int(100*(num_byzantine/(num_correct+num_byzantine))), [n.conf for n in nodes[:num_correct]])
            print(_round, int(100*(num_byzantine/(num_correct+num_byzantine))), [n.color for n in nodes[:num_correct]])
            print(_round, int(100*(num_byzantine/(num_correct+num_byzantine))), [n.weight_red for n in nodes[:num_correct]])
            print(_round, int(100*(num_byzantine/(num_correct+num_byzantine))), [n.weight_blue for n in nodes[:num_correct]])
            print("---------------")
            _round += 1
            for i in range(num_correct):
                if nodes[i].committed:
                    continue
                num_committed += nodes[i].sample()
            if num_committed == num_correct:
                break
        num_red = [i.color for i in nodes[:num_correct]].count(0)
        num_blue = [i.color for i in nodes[:num_correct]].count(1)
        if not (num_red == num_correct or num_blue == num_correct):
            print("Failure on trial", trial, num_red, num_blue)
        print(100*(num_byzantine/(num_correct+num_byzantine)), num_red, num_blue)


if __name__=="__main__":
    main()