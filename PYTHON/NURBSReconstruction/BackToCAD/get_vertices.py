def get_vertices(patch_ids, vertex_list):
	"""
	Extracts the relevant vertices for a single patch from the vertex list.
	:param patch_ids: list of vertex ids of current patch
	:param vertex_list: list of all vertices
	:return: list of vertices of the current patch in lexicographical order
	"""
	vertices = []
	for v_id in patch_ids:
		vertices.append(vertex_list[v_id])
	return vertices
