'''
Author: Zhen Tong 120090694@link.cuhk.edu.cn
'''


import itertools

from utils import FunctionalDependency as FD
from utils import Schema







if __name__ == "__main__":
    
    '''
    test 1 get add_FD
    '''
    # fd1 = FD(["Property_id#"], ["County_name"])
    # fd2 = FD(["Property_id#"], ["Lot#"])
    # fd3 = FD(["Property_id#"], ["Area"])
    # fd4 = FD(["Property_id#"], ["Price"])
    # fd5 = FD(["Property_id#"], ["Tax_rate"])
    # fd6 = FD(["County_name", "Lot#"], ["Property_id#"])
    # fd7 = FD(["County_name", "Lot#"], ["Area"])
    # fd8 = FD(["County_name", "Lot#"], ["Price"])
    # fd9 = FD(["County_name", "Lot#"], ["Tax_rate"])
    # fd10 = FD(["County_name"], ["Tax_rate"])
    # fd11 = FD(["Area"], ["Price"])
    # fds = [fd1, fd2, fd3, fd4, fd5, fd6, fd7, fd8, fd9, fd10, fd11]
    # emp_proj = Schema()
    # for fd in fds:
    #     fd.show()
    #     emp_proj.add_FD(fd)
    # print(emp_proj.attrs)

    """
    test 2 get closure
    """
    fd1 = FD({"A"}, {"B"})
    fd2 = FD({"B"}, {"C"})
    test2 = Schema()
    fds = [fd1, fd2]
    for fd in fds:
        test2.add_FD(fd)
    test2.closure()
    # all_pairs = list(itertools.combinations(fds, 2))
    # for pair in all_pairs:
    #     # print(pair)
    #     f1, f2 = pair
    #     f1.show()
    #     f2.show()
    #     if f1.beta == f2.alpha:
    #         new_fd = FD(f1.alpha, f2.beta)
    #         new_fd.show()
    #     if f2.beta == f1.alpha:
    #         new_fd = FD(f2.alpha, f1.beta)
    #         new_fd.show()


    '''
    test 3 1NF
    '''

    # fd1 = FD(["Ssn", "Pnumber"], ["Hours"])
    # fd2 = FD(["Ssn"], ["Ename"])
    # fd3 = FD(["Pnumber"], ["Pname"])
    # fd4 = FD(["Pnumber"], ["Plocation"])
    # fds = [fd1, fd2, fd3, fd4]
    # emp_proj = Schema()
    # emp_proj.pk = ["Ssn", "Pnumber"]
    # for fd in fds:
        # fd.show()
        # emp_proj.add_FD(fd)
    # print(emp_proj.attrs)
    # emp_proj.closure(update=True)


    # OneNFs = emp_proj.trans1NF()
    # for sch in OneNFs:
        # print(sch.attrs)
