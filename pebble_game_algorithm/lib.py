"""Library for Pebble Game Algorithm."""

import igraph
import logging
from typing import Optional, List, Set, Tuple

logger = logging.getLogger()

FREE_PEBBLE = "free_pebble"  # Vertex attribute for the number of free pebbles.
FIXED_PEBBLE = "_fixed_pebble"  # Reserved vertex attribute for fixed pebbles.


def find_free_pebble(
    g: igraph.Graph,
    root_vid: int,
) -> Optional[List[igraph._igraph.Vertex]]:
    """Finds a node with a free pebble."""
    path = []
    for (v, depth, _) in g.dfsiter(vid=root_vid, advanced=True, mode="out"):
        if len(path) > depth:
            path[depth] = v
        else:
            path.append(v)
        if v["free_pebble"] > 0:
            return path[: (depth + 1)]
    return None


def transfer_pebble(g: igraph.Graph, path: List[igraph._igraph.Vertex]) -> None:
    """Moves a pebble on a path from one end to the other end."""
    start_node = path[0]
    start_node[FREE_PEBBLE] += 1
    edges = []
    reverse_edges = []
    for node in path[1:]:
        edges.append((start_node, node))
        reverse_edges.append((node, start_node))
        start_node = node
    start_node[FREE_PEBBLE] -= 1
    g.delete_edges(edges)
    g.add_edges(reverse_edges)


def _find_cluster_helper(g: igraph.Graph, edge: Tuple[str, str]) -> None:
    """Helper function for cluster identification."""
    source, target = edge
    free_pebble = {source: 0, target: 0}

    # collects 3 pebbles.
    for root in [target, target, source]:
        root_node = g.vs.find(root)
        path = find_free_pebble(g, root_vid=root_node.index)
        if path is None:
            logger.error(f"Inconsistency Error: no pebble found!")
            raise ValueError(f"Inconsistency Error: no pebble found!")
        transfer_pebble(g, path)
        root_node[FREE_PEBBLE] -= 1
        free_pebble[root] += 1

    # restores the fixed pebbles
    for root in [source, target]:
        g.vs.find(root)[FREE_PEBBLE] += free_pebble[root]


def find_rigid_cluster(g: igraph.Graph, edge: Tuple[str, str]) -> Set[str]:
    """Identifies the rigid cluster containing the given edge."""
    _find_cluster_helper(g, edge)  # collects 3 free pebbles.

    source, target = edge
    subgraph = set()
    edge_buffer = []  # edges to be temporally deleted.

    g.vs["visited"] = False  # creates vertex arrtibute for dfsvisit status.

    for root in [source, target]:
        root_node = g.vs.find(root)
        for (v, _, parent) in g.dfsiter(vid=root_node.index, advanced=True, mode="in"):
            if parent is None:
                subgraph.add(v["name"])
            elif v["visited"]:
                subgraph.add(v["name"])
            elif root == source:
                v["visited"] = True
                edge_buffer.append((v["name"], parent["name"]))
        if root == source:
            g.delete_edges(edge_buffer)

    g.add_edges(edge_buffer)
    del g.vs["visited"]  # cleans the vertex attribute.
    return subgraph


def find_stressed_cluster(g: igraph.Graph, edge: Tuple[str, str]) -> Set[str]:
    """Identifies the stressed cluster containing the given edge."""
    _find_cluster_helper(g, edge)

    source, target = edge
    subgraph = set()
    root_node = g.vs.find(source)
    for v in g.dfsiter(vid=root_node.index, mode="out"):
        subgraph.add(v["name"])

    return subgraph


def build_edge(
    g: igraph.Graph,
    edge: Tuple[str, str],
) -> Tuple[bool, Set[str]]:
    """Builds an edge into the graph.

    Args:
        g: The current graph.
        edge: The new edge.

    Returns:
        A two-element tuple. The first element is whether the edge is independent.
        The second element is the stressed cluster introduced by the new edge.
        Of course, it is an empty set when the edge is independent.
    """

    source, target = edge

    free_pebble = {source: 0, target: 0}
    for root in [source, target, source, target]:
        root_node = g.vs.find(root)
        path = find_free_pebble(
            g,
            root_vid=root_node.index,
        )
        if path is None:
            independent = False
            break
        else:
            independent = True
        transfer_pebble(
            g,
            path,
        )
        root_node[FREE_PEBBLE] -= 1
        free_pebble[root] += 1
    for root in [source, target]:
        g.vs.find(root)[FREE_PEBBLE] += free_pebble[root]

    if independent:
        g.add_edge(source=source, target=target)  # adds edge.
        g.vs.find(source)[FREE_PEBBLE] -= 1  # reduces a free pebble.
        return (independent, set())  # stressed cluster is empty.
    else:
        logger.info(f"Edge is redundant: {edge}")
        return (independent, find_stressed_cluster(g, edge))
