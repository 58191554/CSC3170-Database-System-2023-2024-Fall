from utils import FunctionalDependency as FD
from utils import Schema







if __name__ == "__main__":
    '''
    test 1 get closure
    '''
    # fd1 = FD(["Property_id#"], "County_name")
    # fd2 = FD(["Property_id#"], "Lot#")
    # fd3 = FD(["Property_id#"], "Area")
    # fd4 = FD(["Property_id#"], "Price")
    # fd5 = FD(["Property_id#"], "Tax_rate")
    # fd6 = FD(["County_name", "Lot#"], "Property_id#")
    # fd7 = FD(["County_name", "Lot#"], "Area")
    # fd8 = FD(["County_name", "Lot#"], "Price")
    # fd9 = FD(["County_name", "Lot#"], "Tax_rate")
    # fd10 = FD(["County_name"], "Tax_rate")
    # fd11 = FD(["Area"], "Price")
    # fds = [fd1, fd2, fd3, fd4, fd5, fd6, fd7, fd8, fd9, fd10, fd11]
    # emp_proj = Schema()
    # for fd in fds:
    #     fd.show()
    #     emp_proj.add_FD(fd)
    # print(emp_proj.attrs)

    """
    test 2 1NF
    """
    fd1 = FD(["Ssn", "Pnumber"], "Hours")
    fd2 = FD(["Ssn"], "Ename")
    fd3 = FD(["Pnumber"], "Pname")
    fd4 = FD(["Pnumber"], "Plocation")
    fds = [fd1, fd2, fd3, fd4]
    emp_proj = Schema()
    emp_proj.pk = ["Ssn", "Pnumber"]
    for fd in fds:
        fd.show()
        emp_proj.add_FD(fd)
    # print(emp_proj.attrs)
    OneNFs = emp_proj.trans1NF()
    for sch in OneNFs:
        print(sch.attrs)