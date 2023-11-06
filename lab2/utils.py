'''
Author: Zhen Tong 120090694@link.cuhk.edu.cn
'''

import itertools
from tqdm import tqdm


class FunctionalDependency:

    def __init__(self, alpha:set, beta:set):
        self.alpha = alpha
        self.beta = beta

    def show(self):
        for i, alpha in enumerate(self.alpha):
            if i < len(self.alpha)-1:
                print(alpha, end=", ")
            else :
                print(alpha, end=" -> ")
        for j, beta in enumerate(self.beta):
            if j < len(self.beta)-1:
                print(beta, end=", ")
            else:
                print(beta)
        

class Schema:

    def __init__(self, pks = None):
        self.attrs = []
        self.pks = pks
        self.FDs = []
        self.F_plus = []

    def add_FD(self, fd:FunctionalDependency, add2closure = False):
        if self.exist_fd(fd, in_closure=add2closure):
            return False
        
        for alpha in fd.alpha:
            if alpha not in self.attrs:
                self.attrs.append(alpha)

        for beta in fd.beta:
            if beta not in self.attrs:
                self.attrs.append(beta)
        
        if add2closure:
            self.F_plus.append(fd)
        else:
            self.FDs.append(fd)
            
    
    def trans1NF(self):
        """
        output: 1NF schema list
        """
        fd_kind_dict = {}
        for fd in self.FDs:

            # Check if the masters are all pks
            if(is_subset(fd.alpha, self.pks)):

                master_name = ""
                for master in fd.alpha:
                    master_name += master
                fd.show()
                if master_name in fd_kind_dict.keys():
                    fd_kind_dict[master_name].append(fd)
                else:
                    fd_kind_dict[master_name] = [fd]
                    print("new masters = ", master_name)
            
            # Else, the msters have part not pks, find the master of the non-pks
            else:
                non_pk_masters = subtract_set(fd.alpha, self.pks)
                new_masters = self.find_pks_masters(non_pk_masters) 

        
        oneNFs = []
        for fds in fd_kind_dict.values():
            sch = Schema()
            for fd in fds:
                sch.add_FD(fd)
            oneNFs.append(sch)
        return oneNFs

    
    def exist_fd(self, new_fd:FunctionalDependency, in_closure = False):
        # find the fd in clousure
        if in_closure:
            for fd in self.F_plus:
                if fd.alpha == new_fd.alpha and fd.beta == new_fd.beta:
                    return True
            else:
                return False

        # find the fd in FDs
        else:
            for fd in self.FDs:
                if fd.alpha == new_fd.alpha and fd.beta == new_fd.beta:
                    return True
            else:
                return False

            
    def closure(self, update = True):
        """
        input: update = True when you want to compute the new closure again.
        output: the colsure list of it. 
        """
        
        if update==False:
            return self.FDs
        
        # TODO update closure
        self.F_plus = [fd for fd in self.FDs]
        # apply the reflexivity rule /* Generate all trivial dependencies */
        # generate all the combination of attrs
        all_combinations = []
        for r in range(1, len(self.attrs) + 1):
            all_combinations.extend(list(itertools.combinations(self.attrs, r)))

        for comb_list in all_combinations:
            sub_combination = []
            for r in range(1, len(comb_list) + 1):
                sub_combination.extend(list(itertools.combinations(comb_list, r)))
            # print("subset size = ", len(sub_combination))
            for beta in sub_combination:
                # add the trivial to F_plus
                fd = FunctionalDependency(comb_list, beta)
                # fd.show()
                self.add_FD(fd, add2closure=True)
        
        print("The Closure Size is: ", len(self.F_plus))

        # apply the augmentation rule on f in F+
        F_plus_copy= []
        while len(F_plus_copy) != len(self.F_plus):
            # update the copy
            F_plus_copy= [fd for fd in self.F_plus]
            for fd in tqdm(F_plus_copy):
                # apply the augmentation rule on f
                alpha = fd.alpha
                beta = fd.beta
                for gamma in all_combinations:
                    new_alpha = set(alpha).union(set(gamma))
                    new_beta = set(beta).union(set(gamma))
                    new_fd = FunctionalDependency(new_alpha, new_beta)
                    self.add_FD(new_fd, add2closure=True)
            print("After augmentation, the Closure Size is: ", len(self.F_plus))

            # transitivity
            all_pairs = list(itertools.combinations(self.F_plus, 2))
            for pair in tqdm(all_pairs):
                f1, f2 = pair
                if f1.beta == f2.alpha:
                    new_fd = FunctionalDependency(f1.alpha, f2.beta)
                    self.add_FD(new_fd, add2closure=True)
                if f2.beta == f1.alpha:
                    new_fd = FunctionalDependency(f2.alpha, f1.beta)
                    self.add_FD(new_fd, add2closure=True)
            print("After transitivity, the Closure Size is: ", len(self.F_plus))

            input()
        print("finish with size = ", len(self.F_plus))
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

