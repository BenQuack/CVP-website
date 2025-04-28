import numpy as np
import matplotlib.pyplot as plt
import math
from js import document
from pyodide.ffi import create_proxy

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


# Fixed lattice basis
basis = np.array([[3, 1], [1, 3]])

def generate_lattice(basis, size=10):
    """Generate a lattice from basis vectors."""
    points = []
    for i in range(-size, size+1):
        for j in range(-size, size+1):
            point = i * basis[0] + j * basis[1]
            points.append(point)
    return np.array(points)

async def run_cvp(event):
    input_text = document.getElementById("cvp_input").value
    coords = [float(x.strip()) for x in input_text.split(",")]
    point = np.array(coords)
    
    # Add small random noise
    noise = np.random.normal(0, 0.3, size=2)
    noisy_point = point + noise
    
    # Find the closest lattice vector
    closest = babais_algorithm(basis, noisy_point)
    
    # Plot everything
    points = generate_lattice(basis, size=10)
    fig, ax = plt.subplots(figsize=(6,6))
    
    ax.scatter(points[:,0], points[:,1], color='blue', label='Lattice Points')
    ax.scatter(noisy_point[0], noisy_point[1], color='red', label='Noisy Point')
    ax.scatter(closest[0], closest[1], color='green', label='Closest Lattice Vector')
    
    ax.plot([noisy_point[0], closest[0]], [noisy_point[1], closest[1]], 'k--', label='Error Correction')
    
    ax.set_xlim(-20, 20)
    ax.set_ylim(-20, 20)
    ax.set_aspect('equal')
    ax.grid(True)
    ax.legend()
    
    display = document.getElementById("cvp_plot")
    display.innerHTML = ""
    from pyscript import display as pyscript_display
    pyscript_display(fig, target="cvp_plot")

# Hook up button
button = document.getElementById("run_cvp")
button.addEventListener("click", create_proxy(run_cvp))

