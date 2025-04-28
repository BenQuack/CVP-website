import math
import numpy as np

def gaussian_reduction(v_1, v_2):
    if magnitude(v_2) < magnitude(v_1):
        # swap v_1 and v_2
        v_1, v_2 = v_2, v_1
    m = mue(v_1, v_2)
    if m == 0:
        return v_1, v_2
    else:
        return gaussian_reduction(v_1, v_2 - m * v_1)
    
def magnitude(v):
    return math.sqrt(sum(int(x)**2 for x in v))

def mue(v_1,v_2):
    return round(np.dot(v_1,v_2)/magnitude(v_1)**2)

def babais_algorithm(basis, point):
    basis = np.array(basis)
    basis_star = gram_schmidt_orthogonalization(basis)
    c_list = [0] * len(basis)
    v = np.copy(point)
    #compute values of c and populate c_list
    for i in reversed(range(len(basis))):
        c = round(mue(basis_star[i],v))
        c_list[i] = c
        v = v - c * basis[i]
    
    closest_vector = np.zeros_like(point)
    for i in range(len(basis)):
        closest_vector += c_list[i] * basis[i]
    return closest_vector

def gram_schmidt_orthogonalization(basis):
    orthogonal_basis = []
    for v in basis:
        u = np.copy(v)
        for w in orthogonal_basis:
            u -= projection(u,w)
        orthogonal_basis.append(u)
    return orthogonal_basis

# a projection of v_1 onto v_2
def projection(v_1, v_2):
    return (np.dot(v_1, v_2)/np.dot(v_2, v_2)) * v_2

def run_reduction_input():
    v_1_a_input = input("enter the the first integer of vector 1: ")
    v_1_b_input = input("enter the the second integer of vector 1: ")
    v_2_a_input = input("enter the the first integer of vector 2: ")
    v_2_b_input = input("enter the the second integer of vector 2: ")
    print(f"reduced basis: {gaussian_reduction(np.array(v_1_a_input, v_1_b_input),np.array(v_2_a_input, v_2_b_input))}")

def run_reduction_hw():
    print(f"reduced basis: {gaussian_reduction(np.array([1, 5]),np.array([6, 21]))}")
    print(f"reduced basis: {gaussian_reduction(np.array([3, 8]),np.array([5, 14]))}")
    print(f"reduced basis: {gaussian_reduction(np.array([53, 88]),np.array([107, 205]))}")

def run_babais_hw():
    basis = np.array([[53, 88], [107, 205]],dtype=np.float64)
    point = np.array([151, 33],dtype=np.float64)
    print(babais_algorithm(basis, point))

run_reduction_hw()

run_babais_hw()

