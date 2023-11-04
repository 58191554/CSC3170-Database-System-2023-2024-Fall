from utils import FunctionalDependency as FD








if __name__ == "__main__":
    '''
    test 1 get closure
    '''
    fd1 = FD(["Property_id#"], "County_name")
    fd2 = FD(["Property_id#"], "Lot#")
    fd3 = FD(["Property_id#"], "Area")
    fd4 = FD(["Property_id#"], "Price")
    fd5 = FD(["Property_id#"], "Tax_rate")
    fd6 = FD(["County_name", "Lot#"], "Property_id#")
    fd7 = FD(["County_name", "Lot#"], "Area")
    fd8 = FD(["County_name", "Lot#"], "Price")
    fd9 = FD(["County_name", "Lot#"], "Tax_rate")
    fd10 = FD(["County_name"], "Tax_rate")
    fd11 = FD(["Area"], "Price")
    fds = [fd1, fd2, fd3, fd4, fd5, fd6, fd7, fd8, fd9, fd10, fd11]
    for fd in fds:
        fd.show()