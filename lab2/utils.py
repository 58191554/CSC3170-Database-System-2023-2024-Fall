'''
Author: Zhen Tong 120090694@link.cuhk.edu.cn
'''


class FunctionalDependency:

    def __init__(self, master_attrs, slave):
        self.master_attrs = master_attrs
        self.slave = slave

    def show(self):
        for i, master in enumerate(self.master_attrs):
            if i < len(self.master_attrs)-1:
                print(master, end=", ")
            else :
                print(master, end=" -> ")
        print(self.slave)
        

class Schema:

    def __init__(self, attrs:list, pk = None, FDs = None):
        self.attrs = []
        self.pk = pk
        if FDs != None:
            self.FDs = FDs
        else:
            self.FDs = []

    def add_FD(self, master_list:list, slave:str):
        for master in master_list:
            if master not in self.attrs:
                print("Error, add_FD() master not in attributes set")
                return False
        if slave not in self.attrs:
            print("Error, add_FD() slave not in attributes set")
            return False
        FD = FunctionalDependency(master_list, slave)
        self.FDs.append(FD)


def get_closure(FDs:list):
    """
    input: a list of Functional Dependency
    output: the colsure list of it. 
    """
    for FD in FDs:
        pass