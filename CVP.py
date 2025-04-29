"""
This is a VERY simple demo of what an encryption scheme that is using the CVP
as it's "hard" problem would look like
"""
import numpy as np
import random
import matplotlib.pyplot as plt
from pyscript import document
import math

#a list containing pairs of good/bad basis vectors in R^2
basis_pairs = [
    [[np.array([1, 0]), np.array([0, 1])],[np.array([101, 100]), np.array([100, 99])]],
    [[np.array([2, 1]), np.array([1, 2])],[np.array([5, 8]), np.array([11, 17])]],
    [[np.array([1, 1]), np.array([-1, 2])],[np.array([20, 19]), np.array([-1, 1])]],
    [[np.array([3, 0]), np.array([0, 1])],[np.array([6, 1]), np.array([3, 1])]],
    [[np.array([2, 2]), np.array([-2, 3])],[np.array([10, 4]), np.array([4, 3])]],
    [[np.array([1, 2]), np.array([3, 1])],[np.array([10, 7]), np.array([7, 5])]]
]

bad_basis_display = document.getElementById("bad-basis")
good_basis_display = document.getElementById("good-basis")

def add_noise(vec, epsilon=0.4):
    noise = np.random.uniform(-epsilon, epsilon, size=vec.shape)
    return vec + noise

# Functions from user-provided python file
def gaussian_reduction(v_1, v_2):
    if magnitude(v_2) < magnitude(v_1):
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

def projection(v_1, v_2):
    return (np.dot(v_1, v_2)/np.dot(v_2, v_2)) * v_2

def set_up():
    random.shuffle(basis_pairs)
    good_basis = basis_pairs[0][0]#[0] is the good basis [1] is the bad basis
    bad_basis = basis_pairs[0][1]
    return good_basis, bad_basis

def encrypt(m, basis):
    list_of_ascii_pairs = []
    for i in range(len(m),2):# skips odd indexes 
        if i - len(m) == 1:
            list_of_ascii_pairs[i/2] = [ord(m[i]), 32]
        else:
            list_of_ascii_pairs[i/2] = [ord(m[i]), ord(m[i+1])] # makes a list of ascii pairs
    
    encrypted = []
    for pair in list_of_ascii_pairs:
        point = np.dot(pair, basis)
        encrypted_point = add_noise(point)
        encrypted.append(encrypted_point)
    return encrypted