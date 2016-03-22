__author__ = 'benjamin'


def get_quad_edge_list(_quad):
    edges = [(_quad[0], _quad[1]),  # edges of this quad
             (_quad[1], _quad[2]),
             (_quad[2], _quad[3]),
             (_quad[3], _quad[0])]

    edge_keys = []  # keys of the edges
    for e in edges:  # traverse all edges of the quad
        key = tuple(sorted(e))  # calculate corresponding edge key.
        # Keys are made up of the vertex indices belonging to the edge (ascending order!)
        edge_keys.append(key)  # add to key list

    return edge_keys


def quad_has_edge(_quad, _edge_key):
    edge_keys = get_quad_edge_list(_quad)
    if _edge_key in edge_keys:
        return True
    else:
        return False
