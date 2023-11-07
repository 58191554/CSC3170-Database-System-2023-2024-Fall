'''
Author: Zhen Tong 120090694@link.cuhk.edu.cn
'''

import itertools
from tqdm import tqdm
import copy

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
        
    def in_FD_set(self, fd_set:set):
        for fd in fd_set:
            if (fd.alpha == self.alpha) and (fd.beta == self.beta):
                return True
        return False

class Schema:

    def __init__(self, pks = None):
        self.attrs = []
        self.pks = pks
        self.FDs = set()
        self.F_plus = set()

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
            self.F_plus.add(fd)
        else:
            self.FDs.add(fd)
            
    
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
        self.F_plus = {fd for fd in self.FDs}
        # apply the reflexivity rule /* Generate all trivial dependencies */
        # generate all the combination of attrs
        all_combinations = []
        for r in range(1, len(self.attrs) + 1):
            all_combinations.extend(list(itertools.combinations(self.attrs, r)))

        for comb_list in all_combinations:
            sub_combination = []
            for r in range(1, len(comb_list) + 1):
                sub_combination.extend(list(itertools.combinations(comb_list, r)))
            for beta in sub_combination:
                # add the trivial to F_plus
                fd = FunctionalDependency(comb_list, beta)
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

    def sub_closure(self, sub_attrs:set, F=None):
        '''
        Given a set of attributes alpha, define the closure of alpha+ under F 
        '''
        if F == None:
            F = {fd for fd in self.FDs}
        result = set()
        result_prime = set(a for a in sub_attrs)
        while len(result) != len(result_prime):
            # copy the prime to origin
            result = set(a for a in result_prime)
            # print("result = ", result)
            for fd in F:
                if fd.alpha.issubset( result) :
                    result_prime = result_prime.union(fd.beta)
                    # print("Unioned:", result_prime)
            # print("result", result)
        return result
        
    def is_extraneous(self, fd:FunctionalDependency, A:set, determinant:bool, F = None):
        alpha = copy.deepcopy(fd.alpha)
        beta = copy.deepcopy(fd.beta)
        if determinant:
            gamma = alpha.difference(A)
            gamma_plus = self.sub_closure(gamma, F)
            if beta.issubset(gamma_plus):
                return True
            else:
                return False
        else:   
            if F == None:
                F= set(i for i in self.FDs)

            F_prime = (F.difference({fd})).union({FunctionalDependency(alpha, beta.difference(A))})
            alpha_plus = self.sub_closure(alpha, F_prime)
            if A.issubset(alpha_plus):
                return True
            else:
                return False

    def canonicalCover(self):
        F_c = {fd for fd in self.FDs}
        F_c_prime = set()
        while True:
            f1f2_paris = list(itertools.combinations(F_c, 2))  
            F_c_prime = {fd for fd in F_c}                      
            for f1f2 in f1f2_paris:
                f1, f2 = f1f2
                if f1.alpha == f2.alpha and f1.beta != f2.beta:
                    new_fd = FunctionalDependency(f1.alpha, f1.beta.union(f2.beta))
                    if f1.in_FD_set(F_c_prime):
                        F_c_prime = FD_set_pop(F_c_prime, f1)
                    if f2.in_FD_set(F_c_prime):
                        F_c_prime = FD_set_pop(F_c_prime, f2)

                    F_c_prime.add(new_fd)
            
            print("phase 1")
            for fd in F_c_prime:
                fd.show()
            # find extraneous attribute in F_c_prime
            print("find extraneous attribute in F_c_prime")
            F_c_non_etx = set()
            for fd in F_c_prime:
                extraneous = False
                A_s = {a for a in fd.alpha}
                A_combinations = []
                for r in range(1, len(A_s) + 1):
                    A_combinations.extend(list(itertools.combinations(A_s, r)))
                for comb in A_combinations:
                    if self.is_extraneous(fd, set(c for c in comb), determinant=True, F=F_c_prime):
                        print("find Bad A")
                        fd.show()
                        extraneous = True
                        break
                    
                if extraneous:
                    fd.show()
                    break

                B_s = {b for b in fd.beta}
                B_combinations = []
                for r in range(1, len(B_s) + 1):
                    B_combinations.extend(list(itertools.combinations(B_s, r)))
                print("B_combinations", B_combinations)
                extraneous_Bs = set()
                for comb in B_combinations:
                    if self.is_extraneous(fd, set(c for c in comb), determinant=False, F=F_c_prime):
                        print("find BAD", comb, "in ", end=" ")
                        fd.show()
                        extraneous = True
                        extraneous_Bs = extraneous_Bs.union(set(c for c in comb))
                new_beta = (fd.beta).difference(extraneous_Bs)
                print("extraneous_Bs", extraneous_Bs)
                new_fd = FunctionalDependency(fd.alpha, new_beta)
                if new_fd.in_FD_set(F_c_non_etx)==False:
                    F_c_non_etx.add(new_fd)
                if (extraneous == False) and (fd.in_FD_set(F_c_non_etx)==False):
                    F_c_non_etx.add(fd)
                


            print("phase 2")
            for fd in F_c_non_etx:
                fd.show()

            # condition break
            # if(FD_set_equal(F_c_prime, F_c_non_etx)):
                # break

            input()
        return F_c_prime



    def bcnf_decompose(self, ):
        pass

    def nf3_decompose(self, ):
        pass


def FD_set_pop(fd_set:set, fd_pop:FunctionalDependency):
    print("pop", end=" ")
    fd_pop.show()

    fd_list = [f for f in fd_set]
    return_set = set()
    for fd in fd_list:
        if fd.alpha == fd_pop.alpha and fd.beta == fd_pop.beta:
            print("find", end=' ')
            fd.show()
            continue
        else:
            return_set.add(fd)
    return return_set

def FD_set_equal(fdset1:set, fd_set2:set):
    if len(fdset1) != len(fd_set2):
        return False

    judge = [False * len(fdset1)]
    for i, f1 in enumerate(fdset1):
        for f2 in fd_set2:
            if f1.alpha == f2.alpha and f2.beta == f2.beta:
                judge[i] = True
                break
    
    for b in judge:
        if b == False:
            return False
    return True
    


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

