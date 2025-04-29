"""
This is a VERY simple demo of what an encryption scheme that is using the CVP
as it's "hard" problem would look like
"""
import time
import numpy as np
import random
import matplotlib.pyplot as plt
from pyscript import document
from pyodide.ffi import create_proxy
import math
import olll

#a list containing pairs of good/bad basis vectors in R^2
basis_pairs = [
    [[np.array([1, 0]), np.array([0, 1])],[np.array([101, 100]), np.array([100, 99])]],
    [[np.array([2, 1]), np.array([1, 2])],[np.array([5, 8]), np.array([11, 17])]],
    [[np.array([3, 0]), np.array([0, 1])],[np.array([6, 1]), np.array([3, 1])]],
]

#convert basis pairs into dtype=np.floar64
basis_pairs = [
    [
        [np.array(vec, dtype=np.float64) for vec in basis]
        for basis in pair
    ]
    for pair in basis_pairs
]

steps = {
    'good_babai': 0,
    'bad_babai': 0,
    'gauss': 0
}

user_in = document.getElementById("cvp-input")
bad_basis_display = document.getElementById("bad-basis")
good_basis_display = document.getElementById("good-basis")
compairison_display = document.getElementById("num-steps")

def add_noise(vec, epsilon=0.1):
    noise = np.random.uniform(-epsilon, epsilon, size=vec.shape)
    return vec + noise

# Functions from user-provided python file
def gaussian_reduction(v_1, v_2):
    steps['gauss'] += 1
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

def babais_algorithm(basis, point, good):
    basis = np.array(basis)
    basis_star = gram_schmidt_orthogonalization(basis)
    c_list = [0] * len(basis)
    v = np.copy(point)
    for i in reversed(range(len(basis))):
        if good:
            steps["good_babai"] += 1
        else:
            steps["bad_babai"] += 1
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
    for i in range(0,len(m),2):# skips odd indexes 
        if len(m) - i == 1:
            list_of_ascii_pairs.append([ord(m[i]), 32])
        else:
            list_of_ascii_pairs.append([ord(m[i]), ord(m[i+1])]) # makes a list of ascii pairs
    
    encrypted = []
    for pair in list_of_ascii_pairs:
        point = np.dot(pair, basis)
        encrypted_point = add_noise(point)
        encrypted.append(encrypted_point)
    
    return encrypted

def decrypt(c, basis, good=True):
    start = time.time()
    decrypted = []
    if not good:
        basis = gaussian_reduction(basis[0],basis[1])#reduce down to a good basis
    for point in c:
        closest_point = babais_algorithm(basis, point, good)
        actual = np.linalg.solve(basis, closest_point)#take the point off the lattice 
        decrypted.append(np.round(actual))

    text = ""
    for pair in decrypted:
        for c in pair:
            x = max(32, min(126, c))#limit to ascii range to avoid full failure 
            text += chr(int(x))#convert back to text there may be errors
    end = time.time()
    return end - start, text

def display(event):
    steps['good_babai'] = 0
    steps['bad_babai'] = 0
    steps['gauss'] = 0

    good_basis, bad_basis = set_up()
    
    message = user_in.value
    cypher = encrypt(message, good_basis)

    decrypt(cypher, good_basis)
    decrypt(cypher, bad_basis, good=False)

    steps_good = steps["good_babai"]
    steps_bad = steps["bad_babai"] + steps["gauss"]

    good_basis_display.innerText = str(good_basis) + " Number of steps to decrypt: " + str(steps_good)
    bad_basis_display.innerText = str(bad_basis) + " Number of steps to decrypt: " + str(steps_bad)

    canvas = document.getElementById("lattice-canvas")
    ctx = canvas.getContext("2d")
    width = canvas.width
    height = canvas.height

    #clear the old canvas 
    ctx.fillStyle = "white"
    ctx.fillRect(0, 0, canvas.width, canvas.height)
    
    # draw the lattice onto the canvas 
    print(good_basis)
    for x in range(0, width, 10):
        for y in range(0, height, 10):
            point = x * good_basis[0] + y * good_basis[1]
            ctx.beginPath()
            ctx.arc(x, y, 2, 0, 2 * math.pi)
            ctx.fillStyle = "black"
            ctx.fill()
    
    # draw the noisy points onto the lattice
    for point in cypher:
        ctx.beginPath()
        ctx.arc(point[0], point[1], 2, 0, 2 * math.pi)
        ctx.fillStyle = "red"
        ctx.fill()


    canvas = document.getElementById("basis-canvas")
    ctx = canvas.getContext("2d")
    width = canvas.width
    height = canvas.height
    
    #clear the old canvas 
    ctx.fillStyle = "white"
    ctx.fillRect(0, 0, canvas.width, canvas.height)

    origin_x = 50  
    origin_y = height - 50 
    scale = 40 

    for b in good_basis:
        end_x = origin_x + b[0] * scale
        end_y = origin_y - b[1] * scale  # subtract since canvas y increases downward

        # Draw the vector as an arrow
        ctx.beginPath()
        ctx.moveTo(origin_x, origin_y)
        ctx.lineTo(end_x, end_y)
        ctx.strokeStyle = "blue"
        ctx.lineWidth = 2
        ctx.stroke()

        # Draw arrowhead
        headlen = 10
        angle = math.atan2(origin_y - end_y, end_x - origin_x)

        ctx.beginPath()
        ctx.moveTo(end_x, end_y)
        ctx.lineTo(end_x - headlen * math.cos(angle - math.pi / 6),
                   end_y + headlen * math.sin(angle - math.pi / 6))
        ctx.lineTo(end_x - headlen * math.cos(angle + math.pi / 6),
                   end_y + headlen * math.sin(angle + math.pi / 6))
        ctx.lineTo(end_x, end_y)
        ctx.fillStyle = "blue"
        ctx.fill()
    
    origin_x = width // 2 - 50

    for b in bad_basis:
        end_x = origin_x + b[0] * scale
        end_y = origin_y - b[1] * scale  # subtract since canvas y increases downward

        # Draw the vector as an arrow
        ctx.beginPath()
        ctx.moveTo(origin_x, origin_y)
        ctx.lineTo(end_x, end_y)
        ctx.strokeStyle = "red"
        ctx.lineWidth = 2
        ctx.stroke()

        # Draw arrowhead
        headlen = 10
        angle = math.atan2(origin_y - end_y, end_x - origin_x)

        ctx.beginPath()
        ctx.moveTo(end_x, end_y)
        ctx.lineTo(end_x - headlen * math.cos(angle - math.pi / 6),
                   end_y + headlen * math.sin(angle - math.pi / 6))
        ctx.lineTo(end_x - headlen * math.cos(angle + math.pi / 6),
                   end_y + headlen * math.sin(angle + math.pi / 6))
        ctx.lineTo(end_x, end_y)
        ctx.fillStyle = "red"
        ctx.fill()

    # could not get the plot to display
    """
    fig, ax = plt.subplots()
    ax.bar(['Good Babai', 'Bad Babai'], 
           [steps['good_babai'], steps['bad_babai'] + steps['gauss']], 
           color=['blue', 'red'])
    ax.set_ylabel('Steps')
    ax.set_title('Decryption Step Count Comparison')

    filename = "steps_plot.png"
    fig.savefig(filename)
    plt.close(fig)

    img_element = document.getElementById("steps-plot")
    img_element.setAttribute("src", filename)
    """
        


run_button = document.getElementById("run-cvp")
run_cvp_proxy = create_proxy(display)
run_button.addEventListener("click", run_cvp_proxy)