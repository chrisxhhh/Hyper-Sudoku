"""
Hyper Sudoku Solver
solve hyber sudoku using backtracking algorithm
Chris Xu
"""

import copy


class Domain:
    def __init__(self):
        tempDom = []
        for i in range(9):
            tempDom.append([1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.Vdomain = copy.deepcopy(tempDom)
        self.Hdomain = copy.deepcopy(tempDom)
        self.Sdomain = copy.deepcopy(tempDom)
        self.hyperDomain = copy.deepcopy(tempDom[0:4])


class Node:
    def __init__(self, value, i, j, domain):
        self.value = value
        # domains in domain class,
        # i: horizontal domain, j: vertical domain,  i//3*3+j//3: square domain, hyper domain added later
        self.domains = [domain.Hdomain[i], domain.Vdomain[j], domain.Sdomain[i // 3 * 3 + j // 3]]
        if i in [1, 2, 3]:
            if j in [1, 2, 3]:
                self.domains.append(domain.hyperDomain[0])
            elif j in [5, 6, 7]:
                self.domains.append(domain.hyperDomain[1])
        elif i in [5, 6, 7]:
            if j in [1, 2, 3]:
                self.domains.append(domain.hyperDomain[2])
            elif j in [5, 6, 7]:
                self.domains.append(domain.hyperDomain[3])

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
    board = []
    with open(file_name) as f:
        line = f.readlines()

    for i in range(9):
        oneLine = line[i].strip().split()
        for j in range(9):
            oneLine[j] = Node(int(oneLine[j]), i, j, domain)
        board.append(oneLine)
    return board


def produce_output():
    ...


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
                print(i, j)
                print("value: {}, domain:{}".format(value, board[i][j].domains))
                for a in range(len(board[i][j].domains)):
                    board[i][j].domains[a].remove(value)
                print("value: {}, domain:{}".format(value, board[i][j].domains))

    for i in range(9):
        for j in range(9):
            check_res = board[i][j].check_empty()
            if not check_res:
                return False
    return True

def possible_value(node):
    """
    read a node and calculate how many possible value it can have depending on its constrains
    :param node:
    :return: number of possible values
    """
    res = 0
    for i in range(1,10):
        inside = True
        for j in len(node.domains):
            if i not in node.domains[j]:
                inside = False
        if inside:
            res+=1
    return res


def select_unassigned(board):
    """

    :param board:
    :return:
    """
    nodes = []
    MRV = 10
    # apply MRV, produce a list of possible
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                possible_val = possible_value(board[i][j])
                if possible_val < MRV:
                    MRV = possible_val
                    nodes.clear()
                    nodes.append(board[i][j])
                elif possible_val == MRV:
                    nodes.append(board[i][j])
    # apply Degree on the nodes list that has min remaining value


def backtracking_search():
    ...


def backtrack():
    ...


def main():
    # file_name = input("enter the input name: ")
    domain = Domain()
    board = load_input("1", domain)

    # if after forward checking, there is a empty domain and the board is not complete then no solution
    if not forward_check(board):
        print("no solution found")
        return

    print(domain.Hdomain)


if __name__ == "__main__":
    main()
