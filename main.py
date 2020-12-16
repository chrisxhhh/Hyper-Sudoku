"""
Hyper Sudoku Solver
solve hyber sudoku using backtracking algorithm
Chris Xu
"""

import copy


class Domain:
    """
    contain 30 domains shared by each cell on the board
    """
    def __init__(self):
        tempDom = []
        for i in range(9):
            tempDom.append([1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.Vdomain = copy.deepcopy(tempDom)   # vertical domains
        self.Hdomain = copy.deepcopy(tempDom)   # horizontal domains
        self.Sdomain = copy.deepcopy(tempDom)   # square domains
        self.hyperDomain = copy.deepcopy(tempDom[0:4])  # the extra 4 hyper domains


class Node:
    """
    represent one cell one the board
    contain information like value, position and domains

    """
    def __init__(self, value, i, j, domain):
        self.value = value
        self.i = i  # row
        self.j = j  # col
        self.group = i // 3 * 3 + j // 3 # square domain number
        self.group2 = -1  # hyper square domain number. -1 if there is no hyper group

        # domains in domain class,
        self.domains = [domain.Hdomain[i], domain.Vdomain[j], domain.Sdomain[i // 3 * 3 + j // 3]]

        # edit hyper square domains
        if i in [1, 2, 3]:
            if j in [1, 2, 3]:
                self.domains.append(domain.hyperDomain[0])
                self.group2 = 0
            elif j in [5, 6, 7]:
                self.domains.append(domain.hyperDomain[1])
                self.group2 = 1
        elif i in [5, 6, 7]:
            if j in [1, 2, 3]:
                self.domains.append(domain.hyperDomain[2])
                self.group2 = 2
            elif j in [5, 6, 7]:
                self.domains.append(domain.hyperDomain[3])
                self.group2 = 3

    def __repr__(self):
        return str(self.value)

    def check_empty(self):
        """
        check all domains
        if empty return false, otherwise true
        """
        if self.value == 0:
            for i in range(len(self.domains)):
                if len(self.domains[i]) == 0:
                    return False
        return True


def load_input(file_name, domain):
    """
    load the input file and construct the board
    :return: a list of nodes.
    """
    board = []
    with open(file_name) as f:
        line = f.readlines()

    for i in range(9):
        oneLine = line[i].strip().split()
        for j in range(9):
            oneLine[j] = Node(int(oneLine[j]), i, j, domain)
        board.append(oneLine)
    return board


def produce_output(board):
    """
    read the result board and write into Output3.txt
    If Output3.txt doesn't exist in current directory, create one first
    Output3.txt is emptyed first anyway
    """
    with open("Output.txt", mode="w") as output:
        output.truncate(0)
        for i in range(9):
            str_line = [str(x) for x in board[i]]
            output.write(' '.join(str_line) + "\n")


def forward_check(board):
    """
    apply Forward Checking to cells that already have a number
    and reduce the domain of their neighbors.
    warning: This function only work if the input game state did not violate the rules
    such as same number appear twice in one row
    return false when empty cell has a empty domain, otherwise true
    """
    for i in range(9):
        for j in range(9):
            if board[i][j].value != 0:
                value = board[i][j].value
                # print(i, j)
                # print("value: {}, domain:{}".format(value, board[i][j].domains))
                for a in range(len(board[i][j].domains)):
                    board[i][j].domains[a].remove(value)
                # print("value: {}, domain:{}".format(value, board[i][j].domains))

    for i in range(9):
        for j in range(9):
            check_res = board[i][j].check_empty()
            if not check_res:
                return False
    return True


def possible_value(node):
    """
    read a node and calculate how many possible value it can have depending on its constrains
    return a number of possible values
    """
    num = 0
    res = []
    for i in range(1, 10):
        inside = True
        for j in range(len(node.domains)):
            if i not in node.domains[j]:
                inside = False
        if inside:
            num += 1
            res.append(i)
    return num, res


def select_unassigned(board):
    """
    this function select the next optimal cell for back tracking algorithm
    return a list of nodes with most minimum remaining value and max number of neighbors:
    """
    nodes = []
    MRV = 10
    # apply MRV, produce a list of possible
    for i in range(9):
        for j in range(9):
            if board[i][j].value == 0:
                possible_val = possible_value(board[i][j])[0]
                if possible_val < MRV:
                    MRV = possible_val
                    nodes.clear()
                    nodes.append(board[i][j])
                elif possible_val == MRV:
                    nodes.append(board[i][j])

    # apply Degree on the nodes list that has min remaining value
    max_neighbor = 0
    nodes_with_max_neighbor = []
    for val in range(len(nodes)):
        neighbor = 0
        row = nodes[val].i
        col = nodes[val].j
        group = nodes[val].group
        group2 = nodes[val].group2
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    if i == row or j == col:
                        neighbor += 1
                    if group == board[i][j].group:
                        neighbor += 1
                    if group2 == board[i][j].group2:
                        neighbor += 1
        if max_neighbor < neighbor:
            nodes_with_max_neighbor.clear()
            nodes_with_max_neighbor.append(nodes[val])
            max_neighbor = neighbor
        elif max_neighbor == neighbor:
            nodes_with_max_neighbor.append(nodes[val])
    return nodes_with_max_neighbor


def check_complete(board):
    for i in range(9):
        for j in range(9):
            if board[i][j].value == 0:
                return False
    return True


def backtrack(board):
    """
    fill the board using backtracking algorithm
    if no result found, return False, otherwise return the complete board
    """
    if check_complete(board): return board
    var = select_unassigned(board)[0]
    for val in possible_value(var)[1]:
        var.value = val
        for i in range(len(var.domains)):
            var.domains[i].remove(val)
        res = backtrack(board)
        if res != False:
            return res
        var.value = 0
        for i in range(len(var.domains)):
            var.domains[i].append(val)
    return False


def main():
    file_name = input("enter the input name: ")
    domain = Domain()
    board = load_input(file_name, domain)

    # if after forward checking, there is a empty domain and the board is not complete then no solution
    if not forward_check(board):
        print("no solution found")
        return
    res = backtrack(board)
    if res == False:
        print("no result found")
    else:
        produce_output(res)


if __name__ == "__main__":
    main()
