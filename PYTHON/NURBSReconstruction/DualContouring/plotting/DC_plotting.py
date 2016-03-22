from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection


def plot_surface(axis, quads, verts, color, alpha):
    for q in quads:
        vtx = verts[q]
        x = vtx[:, 0].tolist()
        y = vtx[:, 1].tolist()
        z = vtx[:, 2].tolist()
        vtx = [zip(x, y, z)]
        poly = Poly3DCollection(vtx)
        poly.set_color(color)
        poly.set_edgecolor('k')
        poly.set_alpha(alpha)
        axis.add_collection3d(poly)

def plot_hairs(axis, quads_objs, verts, params, color):
    lines_data = []
    points_data_x = []
    points_data_y = []
    points_data_z = []
    for i in range(verts.__len__()):
        q_id = int(params[i][0])
        q = quads_objs[q_id]
        v = verts[i]
        base_v, d = q.projection_onto_plane(v)

        lines_data.append([v.tolist(),base_v.tolist()])
        points_data_x.append(v[0])
        points_data_y.append(v[1])
        points_data_z.append(v[2])
    line = Line3DCollection(lines_data)
    line.color(color)
    axis.add_collection3d(line)
    #axis.scatter(points_data_x, points_data_y, points_data_z,color='k')


def plot_edge(axis, edges, verts, color, linewidth):
    lines_data = []
    for e in edges:
        v0 = verts[e[0]]
        v1 = verts[e[1]]
        lines_data.append([v0.tolist(),v1.tolist()])

    line = Line3DCollection(lines_data)
    line.color(color)
    line.set_linewidth(linewidth)
    axis.add_collection3d(line)