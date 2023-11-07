'''
Author: Zhen Tong 120090694@link.cuhk.edu.cn
'''
import utils
from utils import FunctionalDependency as FD
from utils import is_extraneous
from utils import sub_closure
from utils import Schema





if __name__ == "__main__":
    
    '''
    test get add_FD
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
    test get closure
    """
    fd1 = FD({"A"}, {"B"})
    fd2 = FD({"B"}, {"C"})
    test2 = Schema()
    fds = [fd1, fd2]
    for fd in fds:
        test2.add_FD(fd)
    test2.closure()


    """
    test Closure of Attribute Sets
    """
    # fd1 = FD({"A"}, {"B"})
    # fd2 = FD({"A"}, {"C"})
    # fd3 = FD({"C", "G"}, {"H"})
    # fd4 = FD({"C", "G"}, {"I"})
    # fd5 = FD({"B"}, {"H"})
    # fds = [fd1, fd2, fd3, fd4, fd5]
    # test = Schema()
    # for fd in fds:
    #     test.add_FD(fd, False)
    # sub_attributes = {"A", "G"}
    # sub_closure(sub_attributes, test.FDs)

    '''
    test Extraneous Attributes
    '''
    # fd1 = FD({"A", "B"}, {"C", "D"})
    # fd2 = FD({"A"}, {"E"})
    # fd3 = FD({"E"}, {"C"})
    # fds = [fd1, fd2, fd3]
    # test = Schema()
    # for fd in fds:
    #     test.add_FD(fd, False)
    # extrainous = is_extraneous(fd1, {"C"}, determinant=False, F=test.FDs)
    # print("C's extrainous in  AB -> CD is ", extrainous)

    '''
    test Canonical Cover
    '''
    # fds = [
    #     FD({"A"}, {"B", "C"}),
    #     FD({"B"}, {"C"}),
    #     FD({"A"}, {"B"}),
    #     FD({"A", "B"}, {"C"})
    # ]
    # test = Schema()
    # for fd in fds:
    #     test.add_FD(fd, False)
    # test.canonicalCover()

    """
    test BCNF Decomposition Algorithm
    """
    # fds = [
    #     FD({"course_id"}, {"title", "dept_name", "credits"}),
    #     FD({"building", "room_number"}, {"capacity"}),
    #     FD({"course_id", "sec_id", "semester", "year"}, {"building", "room_number", "time_slot_id"}),
    # ]
    # candidateK = {"course_id", "sec_id", "semester", "year"}
    # test = Schema(candidateK)
    # for fd in fds:
    #     test.add_FD(fd, False)
    # result = utils.bcnf_decompose(test)