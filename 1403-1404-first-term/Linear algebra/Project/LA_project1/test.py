import numpy as np

# def row_echelon(A):
#     #CHNAGE THIS PART
#     """ Define an algorithm to find the row-echelon form of the input matrix, row-echelon form of a matrix is not unique, so any true row-echelon form is acceptable."""
#

def row_echelon(matrix):
    # Convert the input matrix to a numpy array
    A = np.array(matrix, dtype=float)
    rows, cols = A.shape

    pivot_row = 0

    for col in range(cols):
        if pivot_row >= rows:
            break

        # Find the pivot in the current column
        max_row = np.argmax(np.abs(A[pivot_row:rows, col])) + pivot_row

        # If the pivot is zero, continue to the next column
        if A[max_row, col] == 0:
            continue

        # Swap the current row with the pivot row
        A[[pivot_row, max_row]] = A[[max_row, pivot_row]]

        # Eliminate all entries below the pivot
        for r in range(pivot_row + 1, rows):
            A[r] -= (A[r, col] / A[pivot_row, col]) * A[pivot_row]

        # Move to the next row
        pivot_row += 1

    return A

# #DO NOT CHANGE THIS PART
# C = np.array([[0.5,0.1,0.1]
#               ,[0.2,0.5,0.3]
#               ,[0.1,0.3,0.4]])
# d = np.array([[7900]
#               ,[3950]
#               ,[1975]])
# A = np.array([[0.5,-0.1,-0.1,7900]
#               ,[-0.2,0.5,-0.3,3950]
#               ,[-0.1,-0.3,0.6,1975]])
# print(row_echelon(A))
# """Notice that any true row echelon form is acceptable. an example is given below:
# expected_output = ([[1,-0.2,-0.2,15800]
#                 ,[0,23,-17,355500]
#                 ,[0,0,1,24750]])
# """

# def reduce(A):
#    #CHNAGE THIS PART
#   """ Define an algorithm to find the reduced-row-echelon form of the input matrix
#      ATTENTION : Assume  the input matrix is already in row-echelon form!"""

def reduce(A):
    """
    Define an algorithm to find the reduced-row-echelon form of the input matrix.
    ATTENTION: Assume the input matrix is already in row-echelon form!
    """
    rows, cols = A.shape
    A = A.astype(float)  # Ensure the matrix is of float type
    for i in range(rows - 1, -1, -1):  # Start from the last row and go upwards
        # Find the pivot (first non-zero entry) in the current row
        pivot_col = np.argmax(A[i] != 0) if np.any(A[i] != 0) else -1

        if pivot_col != -1:
            # Normalize the pivot row to make the pivot equal to 1
            A[i] = A[i] / A[i, pivot_col]

            # Eliminate all entries above the pivot
            for j in range(i - 1, -1, -1):
                if A[j, pivot_col] != 0:
                    A[j] -= A[i] * A[j, pivot_col]

    return A

# #DO NOT CHANGE THIS PART
# B = np.array([[1,-0.2,-0.2,15800]
#                 ,[0,23,-17,355500]
#                 ,[0,0,1,24750]])
# print(reduce(B))
# """expected_output = ([[1,0,0,27500]
#                 ,[0,1,0,33750]
#                 ,[0,0,1,24750]])"""


# def is_consistent(A):
#     #CHNAGE THIS PART
#    """ Make sure the system has a solution or not """

def is_consistent(A):
    rows, cols = A.shape
    A = A.astype(float)  # Ensure the matrix is of float type
    for i in range(rows):
        if A[i, i] == 0:
            for j in range(i + 1, rows):
                if A[j, i] != 0:
                    A[[i, j]] = A[[j, i]]
                    break

        for j in range(i + 1, rows):
            if A[j, i] != 0:
                factor = A[j, i] / A[i, i]
                A[j] -= factor * A[i]

    for i in range(rows):
        if np.all(A[i, :-1] == 0) and A[i, -1] != 0:
            return False

    return True

# #e.g.
# # DO NOT CHANGE THIS CELL
#
# print(is_consistent(B))
# """
# expected_output: true
# """

# def solve(A):
#     #CHNAGE THIS PART
#   """ Find the solution, A is the augmented matrix """

def solve(A):
    """ Find the solution, A is the augmented matrix """
    # Step 1: Convert to row echelon form
    A_reduced = row_echelon(A)

    # Step 2: Check for consistency
    if not is_consistent(A):
        return "This system has no solution."

    # Step 3: Convert to reduced row echelon form
    A_reduced = reduce(A_reduced)

    # Step 4: Extract solutions
    rows, cols = A_reduced.shape
    solutions = np.zeros((rows, 1))

    for i in range(rows):
        if np.all(A_reduced[i, :-1] == 0) and A_reduced[i, -1] != 0:
            return "This system has no solution."
        elif np.any(A_reduced[i, :-1] != 0):
            solutions[i] = A_reduced[i, -1]  # The last column contains the solutions for non-zero rows

    return solutions


# e.g.
# DO NOT CHANGE THIS CELL


B = np.array([[1, 0, 0, 27500],
              [0, 1, 0, 33750],
              [0, 0, 1, 24750]])
print(solve(B))
"""
Expected_output = [[27500],
                   [33750],
                   [24750]]

"""

# more examples:

A = np.array([[1, 2, -1, 0],
              [3, 6, 0, 4],
              [2, 4, 1, 3]])

print(solve(A))
""" expected output:
this system has no answer"""

D = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])
print(solve(D))
""" expected output:
x1 = -1 , x2 = 2"""

E = np.array([[1, 2, 3, 4],
              [0, 1, 2, 5]])
print(solve(E))
""" expected output:
x1 = -6 , x2 = 5 , x3 = 0"""
