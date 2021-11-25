# Pebble-Game-Algorithm
Python implementation of the 2-D rigidity pebble game algorithm

Firstly, let's review the Laman theorem from graph theory 

Theorem: *A generic network in two dimensions with N sites and B bonds (defining a graph) does not have a redundant bond if no subset of the network containing n sites and b bonds (defining a subgraph) violates b <= 2n-3.*

Second, We can deduce a property of a generically stressed network.

Corollary: *A generic network in two dimensions with N sites and B bonds is generically stressed if B > 2N - 3 and no subset of the network containing n sites and b bonds violates b <= 2n-3.*

References:
1. A MATLAB implementation of the pebble game algorithm: https://github.com/BlueBirdHouse/PebbleGame/
2. Jacobs, D. J., & Thorpe, M. F. (1995). Generic Rigidity Percolation: The Pebble Game. Phys. Rev. Lett., 75, 4051–4054. doi:10.1103/PhysRevLett.75.4051
3. Jacobs, D. J., & Thorpe, M. F. (1996). Generic rigidity percolation in two dimensions. Phys. Rev. E, 53, 3682–3693. doi:10.1103/PhysRevE.53.3682
4. python-igraph: https://github.com/igraph/python-igraph
