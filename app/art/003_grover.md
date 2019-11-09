# Grover algorithm explained with matrices calculus

*author: [Łukasz Herok](https://lukaszherok.com)*

<br/>
**Table of contents**

[TOC]




## Introduction <a href='Introduction' /></a>
This article goes through the [Qiskit Textbook Grover's algorithm](https://community.qiskit.org/textbook/ch-algorithms/grover.html#Grover's-Algorithm)  explaining it in more details, showing how to apply quantum Gates as the matrix calculus. Before going further with this tutorial, you should get familiar with the theoretical [Introduction](https://community.qiskit.org/textbook/ch-algorithms/grover.html#1.-Introduction-) in the Qiskit Textbook.
Grover algorithm is being described as a searching algorithm for the unstructured database. 
However, this example shows, how to perform the Groover's algorithm, to make a quantum system to reveal the marked states.



## Preparation part <a id="Preparation"></a>


*(For the first time I suggest to skip directly to the [Example](#example))*


$$  \def\ket#1{\lvert #1 \rangle}\def\bra#1{\langle #1 \rvert}  $$

*Quantum Gates as matrices*

```python
import numpy as np
from qiskit.extensions import HGate, CnotGate, IdGate, XGate, CzGate, ZGate

# |0>, |1>
zero = np.array([[1.],
                 [0.]]) 

one = np.array([[0.],
                [1.]]) 

# Gates: I, Z, H, X
I = IdGate().to_matrix()
Z = ZGate().to_matrix()
H = 1./np.sqrt(2) * np.array([[1, 1],
                              [1, -1]])
X = XGate().to_matrix()

# 3-qubit Hadamard gate
Hq012 = np.kron(np.kron(H,H),H)

# 3-qubit CZ gates
p00 = zero * np.array([1, 0]) # |0><0|
p11 = one * np.array([0, 1]) # |1><1|
# control = 1 (|0><0| + |1><1|), target = 0 (Z), uninvoled =2 (I)
# 012 + 012 - qubit indexint
cz10 = np.kron(np.kron(I, p00), I) + np.kron(np.kron(Z, p11), I)
cz20 = np.kron(np.kron(I, I), p00) + np.kron(np.kron(Z, I), p11)

# 3-qubit CCZ gate
# control = (|0><0| + |1><1|), 
# target = (Z)
# control = 21
# target  = 0 
ccz210 = np.kron(np.kron(I, p00), p00) + np.kron(np.kron(Z, p11), p11)
```


*qiskit:*

```python
# initialization
import matplotlib.pyplot as plt
%matplotlib inline

# importing Qiskit
from qiskit import IBMQ, BasicAer
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute

# import basic plot tools
from qiskit.tools.visualization import plot_histogram
```


## Example <a class="anchor" id="Example"></a>

According to the [example](https://community.qiskit.org/textbook/ch-algorithms/grover.html#2.-Example--) 
we have got a three-qubit qubit system and we want to make it return our two marked states: \\( \ket{101} \\) and \\( \ket{110}  \\).

The whole procedure is as follows:

0. Prepare the quantum system
2. Create superposition of states
2. Run the oracle over the system
3. Amplify the amplitude


<br/>
**1. Prepare the quantum system**



Combine 3 qubits in state |0> to make one [qbyte](https://github.com/Qiskit/qiskit-tutorials-community/blob/master/hello_world/bitstring_compression.ipynb) register: $$ \ket{000} $$
<center>
$$ \ket{\psi_0} = \ket{0}\otimes\ket{0}\otimes\ket{0} $$
$$ \ket{\psi_0} = \ket{000} $$
</center>

<br/>*matrix:*


```python
state = np.kron(np.kron(zero, zero), zero)
state
```




    array([[1.],
           [0.],
           [0.],
           [0.],
           [0.],
           [0.],
           [0.],
           [0.]])



Note that you can treat it is as a bit string, calculating the value of the state form binary to decimal 
(eg. \\( \ket{000} = 0, \ket{101} = 5 \\) ), the result is pointing you the position of the `1` in the vector (on the 0th or 5th position accordingly).

<br/>*qiskit:*


```python
q = QuantumRegister(3)
c = ClassicalRegister(3)
circ = QuantumCircuit(q, c)

circ.draw(output='mpl')
```


<center>
<figure class="figure text-center">
  <img width="80%" src="/static/art/003/output_13_0.png" class="figure-img img-fluid rounded" alt="A generic square placeholder image with rounded corners in a figure.">
  <figcaption class="figure-caption text-center"></figcaption>
</figure>
</center>



<br/></br>
**2. Superposition**

Apply Hadamard gates to the qubits to create a uniform superposition:

<center>
$$ \ket{\psi_1} = H\ket{\psi_0} $$

 $$ \lvert \psi_1 \rangle = \frac{1}{\sqrt{8}} \left( 
    \lvert000\rangle + \lvert001\rangle + \lvert010\rangle + \lvert011\rangle + 
    \lvert100\rangle + \lvert101\rangle + \lvert110\rangle + \lvert111\rangle \right) $$
</center>

<br/>*matrix:*


```python
state = np.dot(Hq012, state)
state
```




    array([[0.35355339],
           [0.35355339],
           [0.35355339],
           [0.35355339],
           [0.35355339],
           [0.35355339],
           [0.35355339],
           [0.35355339]])



<br/>*qiskit:*


```python
circ.h(q)
circ.draw(output='mpl')
```



<center>
<figure class="figure text-center">
  <img width="80%" src="/static/art/003/output_18_0.png" class="figure-img img-fluid rounded" alt="A generic square placeholder image with rounded corners in a figure.">
  <figcaption class="figure-caption text-center"></figcaption>
</figure>
</center>


<br/></br>
** 3. Oracle **

Mark the desired states $\lvert101\rangle$ and $\lvert110\rangle$ using a phase oracle:

$$ \ket{a} = b $$

$$ \ket{\psi_2} = CZ_{10}\ket{CZ_{20}\ket{\psi_1}} $$


 $$ \lvert \psi_2 \rangle = \frac{1}{\sqrt{8}} \left( 
    \lvert000\rangle + \lvert001\rangle + \lvert010\rangle + \lvert011\rangle + 
    \lvert100\rangle - \lvert101\rangle - \lvert110\rangle + \lvert111\rangle \right) $$

you can see, that the marked states where flipped.

<br/>
*matrix:*


```python
oracle =cz20*cz10
state = np.dot(oracle, state)
state
```




    array([[ 0.35355339+0.j],
           [ 0.35355339+0.j],
           [ 0.35355339+0.j],
           [ 0.35355339+0.j],
           [ 0.35355339+0.j],
           [-0.35355339+0.j],
           [-0.35355339+0.j],
           [ 0.35355339+0.j]])



<br/>*qiskit:*


```python
circ.barrier() # for readabilty
circ.cz(q[2], q[0])
circ.cz(q[1], q[0])
circ.draw(output='mpl')
```

<center>
<figure class="figure text-center">
  <img width="80%" src="/static/art/003/output_23_0.png" class="figure-img img-fluid rounded" alt="A generic square placeholder image with rounded corners in a figure.">
  <figcaption class="figure-caption text-center"></figcaption>
</figure>
</center>


<br/><br/>
**4. Amplify probabilities**

<br/>
4a). Apply Hadamard gates to the qubits:
$$ \ket{\psi_{3a}} = H\ket{\psi_2} $$ 

$$\lvert \psi_{3a} \rangle = \frac{1}{2} \left( 
        \lvert000\rangle +\lvert011\rangle +\lvert100\rangle -\lvert111\rangle \right) $$

<br/>*matrix:*


```python
state = np.dot(Hq012, state)
state
```




    array([[ 5.00000000e-01+0.j],
           [ 0.00000000e+00+0.j],
           [ 2.77555756e-17+0.j],
           [ 5.00000000e-01+0.j],
           [ 5.00000000e-01+0.j],
           [ 0.00000000e+00+0.j],
           [ 2.77555756e-17+0.j],
           [-5.00000000e-01+0.j]])



<br/>*qiskit:*


```python
circ.barrier() # for readabilty
circ.h(q)
circ.draw(output='mpl')
```




<center>
<figure class="figure text-center">
  <img width="80%" src="/static/art/003/output_29_0.png" class="figure-img img-fluid rounded" alt="A generic square placeholder image with rounded corners in a figure.">
  <figcaption class="figure-caption text-center"></figcaption>
</figure>
</center>



<br/>
4b). Apply X gates to the qubits:
$$ \ket{\psi_{3b}} = X\ket{\psi_{3a}} $$ 
$$\lvert \psi_{3b} \rangle = \frac{1}{2} \left( 
        -\lvert000\rangle +\lvert011\rangle +\lvert100\rangle +\lvert111\rangle \right) $$


```python
Xq012 = np.kron(np.kron(X,X), X)
state = np.dot(Xq012, state)
state
```




    array([[-5.00000000e-01+0.j],
           [ 2.77555756e-17+0.j],
           [ 0.00000000e+00+0.j],
           [ 5.00000000e-01+0.j],
           [ 5.00000000e-01+0.j],
           [ 2.77555756e-17+0.j],
           [ 0.00000000e+00+0.j],
           [ 5.00000000e-01+0.j]])



<br/>*qiskit:*


```python
circ.x(q)
circ.draw(output='mpl')
```




<center>
<figure class="figure text-center">
  <img width="80%" src="/static/art/003/output_33_0.png" class="figure-img img-fluid rounded" alt="A generic square placeholder image with rounded corners in a figure.">
  <figcaption class="figure-caption text-center"></figcaption>
</figure>
</center>



<br/>
4c). Apply a doubly controlled Z gate between the 0, 1 (controls) and 2 (target) qubits

$$ \ket{\psi_{3c}} = CCZ_{012}\ket{\psi_{3b}} $$ 

$$ \lvert \psi_{3c} \rangle = \frac{1}{2} \left(-\lvert000\rangle +\lvert011\rangle  +\lvert100\rangle -\lvert111\rangle \right) $$

<br/>*matrix:*


```python
state = np.dot(ccz210, state)
state
```




    array([[-0.5+0.j],
           [ 0. +0.j],
           [ 0. +0.j],
           [ 0.5+0.j],
           [ 0.5+0.j],
           [ 0. +0.j],
           [ 0. +0.j],
           [-0.5+0.j]])



<br/>*qiskit:*


```python
# There is no ccz gate in qiskit so we need to implement it using h-ccx-h
circ.h(q[2])
circ.ccx(q[0], q[1], q[2])
circ.h(q[2])
circ.draw(output='mpl')
```




<center>
<figure class="figure text-center">
  <img width="80%" src="/static/art/003/output_38_0.png" class="figure-img img-fluid rounded" alt="A generic square placeholder image with rounded corners in a figure.">
  <figcaption class="figure-caption text-center"></figcaption>
</figure>
</center>



<br/>
4d). Apply X gates to the qubits

$$ \ket{\psi_{3d}} = X\ket{\psi_{3c}} $$

 $$\lvert \psi_{3d} \rangle = \frac{1}{2} \left( 
        -\lvert000\rangle +\lvert011\rangle +\lvert100\rangle -\lvert111\rangle \right) $$

<br/>*matrix:*


```python
state = np.dot(Xq012, state)
state
```




    array([[-0.5+0.j],
           [ 0. +0.j],
           [ 0. +0.j],
           [ 0.5+0.j],
           [ 0.5+0.j],
           [ 0. +0.j],
           [ 0. +0.j],
           [-0.5+0.j]])



<br/>*qiskit:*


```python
circ.x(q)
circ.draw(output='mpl')
```




<center>
<figure class="figure text-center">
  <img width="80%" src="/static/art/003/output_43_0.png" class="figure-img img-fluid rounded" alt="A generic square placeholder image with rounded corners in a figure.">
  <figcaption class="figure-caption text-center"></figcaption>
</figure>
</center>



<br/>
e). Apply Hadamard gates to the qubits

$$ \ket{\psi_{3e}} = H\ket{\psi_{3d}} $$
$$\lvert \psi_{3e} \rangle = \frac{1}{\sqrt{2}} \left( 
        -\lvert101\rangle -\lvert110\rangle \right) $$

<br/>*matrix:*


```python
state = np.dot(Hq012, state)
state
```




    array([[ 0.00000000e+00+0.j],
           [ 9.52420783e-18+0.j],
           [ 9.52420783e-18+0.j],
           [ 0.00000000e+00+0.j],
           [ 0.00000000e+00+0.j],
           [-7.07106781e-01+0.j],
           [-7.07106781e-01+0.j],
           [ 0.00000000e+00+0.j]])



Results 5: |101>, 6: |110>.

(look carefully that states 1 = |001>, and 2 = |010>, are almost equal to `0`).



<br/>*qiskit:*


```python
circ.h(q)
circ.draw(output='mpl')
```
<figure class="figure text-center">
  <img width="80%" src="/static/art/003/output_49_0.png" class="figure-img img-fluid rounded" alt="A generic square placeholder image with rounded corners in a figure.">
  <figcaption class="figure-caption text-center"></figcaption>
</figure>


```python
circ.measure(q, c)
backend = BasicAer.get_backend('qasm_simulator')
shots = 1024
results = execute(circ, backend=backend, shots=shots).result()
answer = results.get_counts()
plot_histogram(answer)
```
<center>
<figure class="figure text-center">
  <img width="80%" src="/static/art/003/output_50_1.png" class="figure-img img-fluid rounded" alt="A generic square placeholder image with rounded corners in a figure.">
  <figcaption class="figure-caption text-center"></figcaption>
</figure>
</center>

## Conclusion 
The example above shows how to apply Grover's procedure over the quantum system. The system returns the states that we already know. More oracles for the qubit system you can find in ["Complete 3-Qubit Grover search on a programmable quantum computer"](https://doi.org/10.1038/s41467-017-01904-7), eg.:

The real advantage of this algorithm is when we know only some constraints for the results, and we can design appropriate oracle so the algorithm can give us as output the solution. For example, for the database search, we describe only some attributes of the elements, and the system returns us the addresses of the elements that should be retrieved.

Go to the current [Jupyter Notebook](https://github.com/lukasszz/qiskit-exp/blob/master/grover/Grover4.ipynb) to evalute code in this text.

## Refferences <a href='Refferences' /> 

1. [Qiskit Textbook Grover's algorithm](https://community.qiskit.org/textbook/ch-algorithms/grover.html#Grover's-Algorithm)
2. C. Figgatt, D. Maslov, K. A. Landsman, N. M. Linke, S. Debnath & C. Monroe (2017), "Complete 3-Qubit Grover search on a programmable quantum computer", Nature Communications, Vol 8, Art 1918, [doi:10.1038/s41467-017-01904-7](https://doi.org/10.1038/s41467-017-01904-7), arXiv:1703.10535
3. Łukasz Herok, [Compressing bit strings in qubits using superposition effect](https://github.com/Qiskit/qiskit-tutorials-community/blob/master/hello_world/bitstring_compression.ipynb)
