# Functional Dependency Analysis Tool

## Introduction

This Python script provides a tool for analyzing functional dependencies in a relational database schema. The script includes functionalities for checking if a schema is in 1NF, 2NF, 3NF, or Boyce-Codd Normal Form (BCNF), decomposing a schema into BCNF, and finding the canonical cover of a set of functional dependencies.

## Author

- **Zhen Tong**
- Email: 120090694@link.cuhk.edu.cn

## Classes

### 1. `FunctionalDependency`

This class represents a functional dependency with attributes `alpha` and `beta`. It includes methods to display the functional dependency, check if it is in a set of functional dependencies, and determine if it is trivial.

### 2. `Schema`

This class represents a relational database schema with attributes `attrs` (list of attributes), `cks` (candidate keys), `FDs` (set of functional dependencies), and `F_plus` (closure of functional dependencies). It includes methods to add functional dependencies, check for the existence of a functional dependency, compute the closure, find the canonical cover, check if the schema is in BCNF, and remove attributes.

### 3. `bcnf_decompose`

This function takes a schema and decomposes it into a set of schemas that are in Boyce-Codd Normal Form (BCNF). It iteratively checks each sub-schema for BCNF violation and decomposes if needed.

### 4. `FD_set_pop` and `FD_set_equal`

These functions are utility functions for manipulating sets of functional dependencies.

### 5. `is_extraneous` and `sub_closure`

These functions are used for analyzing extraneous attributes and computing closures, respectively, in the process of finding the canonical cover.

## How to Use

1. Instantiate a `Schema` object and add functional dependencies using the `add_FD` method.

```python
R = Schema()
fd1 = FunctionalDependency({'A'}, {'B'})
R.add_FD(fd1)
```

2. Compute the closure of the functional dependencies using the `closure` method.

```python
R.closure()
```

3. Check if the schema is in BCNF using the `is_bcnf` method.

```python
bcnf, violating_fd = R.is_bcnf()
```

4. Decompose the schema into BCNF using the `bcnf_decompose` function.

```python
result_schemas = bcnf_decompose(R)
```

5. Find the canonical cover of the functional dependencies using the `canonicalCover` method.

```python
canonical_cover = R.canonicalCover()
```

6. Remove attributes from the schema using the `remove` method.

```python
R.remove({'C', 'D'})
```

## Note

- The script uses the `itertools` and `tqdm` libraries, so make sure to install them before running the script.
- The `closure` method generates all trivial dependencies and applies augmentation and transitivity rules to compute the closure.
- The `bcnf_decompose` function iteratively decomposes the schema until all sub-schemas are in BCNF.
- The `canonicalCover` method finds the canonical cover of the functional dependencies using the augmentation and extraneous attribute rules.

# Test Documentation

## Introduction

This section provides test cases for the functional dependencies analysis tool. The tests cover various aspects of the script, including adding functional dependencies, computing closures, analyzing extraneous attributes, finding the canonical cover, and decomposing a schema into Boyce-Codd Normal Form (BCNF).


## Test Cases

### 1. Adding Functional Dependencies

```python
fd1 = FD({"A"}, {"B"})
fd2 = FD({"B"}, {"C"})
test = Schema()
fds = [fd1, fd2]
for fd in fds:
    test.add_FD(fd)
test.attrs  # Expected output: ['A', 'B', 'C']
```

### 2. Computing Closure

```python
fd1 = FD({"A"}, {"B"})
fd2 = FD({"B"}, {"C"})
test2 = Schema()
fds = [fd1, fd2]
for fd in fds:
    test2.add_FD(fd)
test2.closure()
# Expected output:
# The Closure Size is:  9
# After augmentation, the Closure Size is:  25
# After transitivity, the Closure Size is:  36
```

### 3. Closure of Attribute Sets

```python
fd1 = FD({"A"}, {"B"})
fd2 = FD({"A"}, {"C"})
fd3 = FD({"C", "G"}, {"H"})
fd4 = FD({"C", "G"}, {"I"})
fd5 = FD({"B"}, {"H"})
fds = [fd1, fd2, fd3, fd4, fd5]
test = Schema()
for fd in fds:
    test.add_FD(fd, False)
sub_attributes = {"A", "G"}
sub_closure(sub_attributes, test.FDs)
# Expected output: {'A', 'G', 'B', 'C', 'H', 'I'}
```

### 4. Extraneous Attributes

```python
fd1 = FD({"A", "B"}, {"C", "D"})
fd2 = FD({"A"}, {"E"})
fd3 = FD({"E"}, {"C"})
fds = [fd1, fd2, fd3]
test = Schema()
for fd in fds:
    test.add_FD(fd, False)
is_extraneous(fd1, {"C"}, determinant=False, F=test.FDs)
# Expected output: True
```

### 5. Canonical Cover

```python
fds = [
    FD({"A"}, {"B", "C"}),
    FD({"B"}, {"C"}),
    FD({"A"}, {"B"}),
    FD({"A", "B"}, {"C"})
]
test = Schema()
for fd in fds:
    test.add_FD(fd, False)
test.canonicalCover()
# Expected output:
# The canonical cover is:
# A -> B
# B -> C
```

### 6. BCNF Decomposition Algorithm

```python
fds = [
    FD({"course_id"}, {"title", "dept_name", "credits"}),
    FD({"building", "room_number"}, {"capacity"}),
    FD({"course_id", "sec_id", "semester", "year"}, {"building", "room_number", "time_slot_id"}),
]
candidateK = {"course_id", "sec_id", "semester", "year"}
test = Schema(candidateK)
for fd in fds:
    test.add_FD(fd, False)
result = utils.bcnf_decompose(test)
# Check the result manually
```

## Note

- Uncomment the specific test cases you want to execute.
- Make sure to import the necessary classes and functions from the `utils` module.
- Check the expected output comments for each test case.