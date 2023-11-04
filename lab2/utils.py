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

    def __init__(self, pks = None):
        self.attrs = []
        self.pks = pks
        self.FDs = []
        self.F_plus = None

    def add_FD(self, fd:FunctionalDependency):
        for master in fd.master_attrs:
            if master not in self.attrs:
                self.attrs.append(master)
        if fd.slave not in self.attrs:
            self.attrs.append(fd.slave)
        self.FDs.append(fd)
    
    def trans1NF(self):
        """
        output: 1NF schema list
        """
        fd_kind_dict = {}
        for fd in self.FDs:

            # Check if the masters are all pks
            if(is_subset(fd.master_attr, self.pks)):

                master_name = ""
                for master in fd.master_attrs:
                    master_name += master
                fd.show()
                if master_name in fd_kind_dict.keys():
                    fd_kind_dict[master_name].append(fd)
                else:
                    fd_kind_dict[master_name] = [fd]
                    print("new masters = ", master_name)
            
            # Else, the msters have part not pks, find the master of the non-pks
            else:
                non_pk_masters = subtract_set(fd.master_attrs, self.pks)
                new_masters = self.find_pks_masters(non_pk_masters) 

        
        oneNFs = []
        for fds in fd_kind_dict.values():
            sch = Schema()
            for fd in fds:
                sch.add_FD(fd)
            oneNFs.append(sch)
        return oneNFs

    def find_pks_masters(self, non_pk_attrs):
        """
        input: a list of non-pk attributes
        output a list of [pk masters list] (2-nest list)
        """
        pk_masters_set = []
        for m in non_pk_attrs:
            pk_masters = []
            for fd in self.closure():
                if m == fd.slave and is_subset(fd.master_attrs, self.pks):
                    pk_masters+=fd.master_attrs
                    break
            pk_masters_set.append(pk_masters)
        return pk_masters_set
            
    def closure(self, update = False):
        """
        output: the colsure list of it. 
        """
        
        if self.F_plus == None or update:
            # TODO get closure
        
        return self.F_plus



def is_subset(l1:list, l2:list):
    for i in l1:
        if i not in l2:
            return False
    return True

def subtract_set(l1:list, l2:list):
    l_subtract = []
    for i in l1:
        if i not in l2:
            l_subtract.append(i)
    return l_subtract

