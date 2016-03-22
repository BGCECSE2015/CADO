import export_results
import numpy as np
from dcHelpers import resolve_manifold_edges, create_manifold_edges, generate_edge_usage_dict
from VoxelDataset import VoxelDataset
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pColors import PColors

#########################
#### DUAL CONTOURING ####
#########################

dirs = [np.array([0.0, 0.0, 1.0]), np.array([0.0, 1.0, 0.0]), np.array([1.0, 0.0, 0.0])]

# Vertices of cube
cube_verts = np.array([np.array([x, y, z])
                       for x in range(2)
                       for y in range(2)
                       for z in range(2)])

# Edges of cube
cube_edges = [[0, 1], [0, 2], [1, 3], [2, 3],
              [4, 6], [4, 5], [6, 7], [5, 7],
              [1, 5], [3, 7], [0, 4], [2, 6]]


def coarsen_dataset(coarsening_steps, fine_dataset):
    print "%d coarsening_steps left." % coarsening_steps
    minimum_number_of_inner_cells = 1

    if coarsening_steps > 0:
        fine_dataset.surround()
        # calculate coarse resolution
        coarse_res = 2 * fine_dataset._resolution

        # shrinking dimensions in coarsening step
        coarse_dims = {'min': 3 * [None], 'max': 3 * [None]}
        for d in range(3):
            coarse_dims['min'][d] = fine_dataset._dimensions['min'][d] + .5 * fine_dataset._resolution
            coarse_dims['max'][d] = fine_dataset._dimensions['max'][d] - .5 * fine_dataset._resolution

        coarse_data = set(fine_dataset._data)
        # traverse all cells (each one has 4 datavalues) and combine all 4 values into one
        number_of_cube_verts = np.size(cube_verts, 0)

        for x, y, z in fine_dataset.get_grid_iterator():
            o = np.array([float(x), float(y), float(z)])

            new_data = np.zeros(number_of_cube_verts, dtype=bool)

            for i in range(number_of_cube_verts):
                position = (o + cube_verts[i, :] * fine_dataset._resolution)
                key = tuple(position)
                new_data[i] = fine_dataset.value_at(key)

            new_o = o + fine_dataset._resolution * np.array([.5, .5, .5])
            new_key = tuple(new_o)

            if np.sum(new_data) > minimum_number_of_inner_cells:
                coarse_data.add(new_key)
            else:
                coarse_data.discard(new_key)

        coarse_dataset = VoxelDataset(coarse_dims, coarse_res, coarse_data)
        # recursively coarsen
        return coarsen_dataset(coarsening_steps - 1, coarse_dataset)
    else:
        # on last level surround structure with empty cells by extending dims
        coarse_dims = {'min': 3 * [None], 'max': 3 * [None]}
        for d in range(3):
            coarse_dims['min'][d] = fine_dataset._dimensions['min'][d] - .5 * fine_dataset._resolution
            coarse_dims['max'][d] = fine_dataset._dimensions['max'][d] + .5 * fine_dataset._resolution

        coarse_dataset = VoxelDataset(coarse_dims, fine_dataset._resolution, fine_dataset._data)

        return coarse_dataset


# Use non-linear root finding to compute intersection point
def estimate_hermite_easy(data, v0, v1, res, res_fine):
    """
    Just assumes the root lies in the middle of the edge between v0 and v1
    :param data: dataset
    :param v0: first point of edge
    :param v1: second point of edge
    :param res: not used
    :param res_fine: not used
    :return:
    """
    t0 = .5
    x0 = (1. - t0) * v0 + t0 * v1
    return x0


def estimate_hermite(data, v0, v1, res, res_fine):
    """
    Searches for the root on the edge between v0 and v1 using bisection. The dataset has more values than its actual
    resolution. We can go down to 2*res_fine. The fine dataset is not aligned with the coarse one, therefore, we cannot
    go down to res_fine.
    :param data: dataset
    :param v0: first point of edge
    :param v1: second point of edge
    :param res: starting resolution (if res = res_fine, no bisection is used. We just assume the root to be in the middle)
    :param res_fine: fine resolution
    :return:
    """
    data_v0 = data[tuple(v0)]
    data_v1 = data[tuple(v1)]

    coarse_level = (not res == res_fine)
    if coarse_level:
        res_min = res_fine * 2  # fine resolution grid is not aligned! There is no data!
    else:
        res_min = res

    x0 = .5 * (v0 + v1)
    while res != res_min:
        data_x0 = data[tuple(x0)]
        if data_v0 != data_x0:
            v1 = x0
        elif data_v1 != data_x0:
            v0 = x0
        else:
            raise Exception("something wrong in bisection!")
        x0 = .5 * (v0 + v1)
        res /= 2.0

    return x0


def tworesolution_dual_contour(data, resolutions, dims):
    # fine_dataset = VoxelDataset.from_filename('GE_white_big.vtk') # use for GE bracket
    fine_dataset = VoxelDataset(dims, resolutions['fine'], data)  # use for topy files
    print "++ Aligning Dataset ++"
    fine_dataset.align()
    fine_dataset.surround()

    pre_coarsening_steps = 0
    if pre_coarsening_steps > 0:
        print "PRESMOOTHING OF DATASET APPLIED!"
        print "++ Precoarsening of dataset ++"
        print "coarsening steps: %d" % (pre_coarsening_steps)
        fine_dataset = coarsen_dataset(pre_coarsening_steps, fine_dataset)

    print "++ Fine Resolution DC ++"
    print "resolution: %d" % (fine_dataset._resolution)
    [dc_verts_fine, dc_quads_fine, dc_manifold_edges_fine, not_resolved_edges_fine] = dual_contour(fine_dataset,
                                                                                                   resolutions['fine'],
                                                                                                   is_coarse_level=False,
                                                                                                   do_manifold_treatment=False)

    # compute necessary coarsening steps from given coarse resolution.
    print "fine quads produced: %d" % (dc_quads_fine.__len__())

    coarsening_steps = int(np.log(resolutions['coarse']) / np.log(2)) - pre_coarsening_steps
    if coarsening_steps > 0:
        print "++ Coarsening Dataset ++"
        assert type(coarsening_steps) is int  # coarsening steps have to be integer!
        coarse_dataset = coarsen_dataset(coarsening_steps, fine_dataset)
    else:
        coarse_dataset = fine_dataset

    print "++ Coarse Resolution DC ++"
    print "resolution: %d" % (coarse_dataset._resolution)
    [dc_verts_coarse, dc_quads_coarse, dc_manifold_edges_coarse, not_resolved_edges_coarse] = dual_contour(
        coarse_dataset,
        resolutions['fine'],
        is_coarse_level=True,
        do_manifold_treatment=True)

    print "coarse quads produced: %d" % (dc_quads_coarse.__len__())
    dc_verts = {'fine': dc_verts_fine, 'coarse': dc_verts_coarse}
    dc_quads = {'fine': dc_quads_fine, 'coarse': dc_quads_coarse}
    dc_manifolds = {'fine': dc_manifold_edges_fine, 'coarse': dc_manifold_edges_coarse}

    print "checking for remaining non-manifold edges on coarse level:"
    nonmanifold = []
    edge_usage = generate_edge_usage_dict(dc_quads_coarse)
    for edge_identifier, used_by_quads in edge_usage.items():
        if used_by_quads.__len__() != 2:
            nonmanifold.append(np.array(edge_identifier))

    try:
        assert nonmanifold.__len__() == 0 and not_resolved_edges_coarse.__len__() == 0
    except AssertionError as e:
        import traceback, os.path
        top = traceback.extract_stack()[-1]
        print '\n'
        print ', '.join([os.path.basename(top[0]), str(top[1])])
        print "ERROR found. exporting intermediate results."
        export_results.export_as_csv(dc_verts_fine, './PYTHON/NURBSReconstruction/DualContouring/plotting/dc_verts_fine')
        export_results.export_as_csv(dc_quads_fine, './PYTHON/NURBSReconstruction/DualContouring/plotting/dc_quads_fine')
        export_results.export_as_csv(dc_verts_coarse, './PYTHON/NURBSReconstruction/DualContouring/plotting/dc_verts_coarse')
        export_results.export_as_csv(dc_quads_coarse, './PYTHON/NURBSReconstruction/DualContouring/plotting/dc_quads_coarse')
        export_results.export_as_csv(np.array(nonmanifold), './PYTHON/NURBSReconstruction/DualContouring/plotting/dc_non_manifold_edges')
        export_results.export_as_csv([coarse_dataset._dimensions['min'], coarse_dataset._dimensions['max']],
                                     './PYTHON/NURBSReconstruction/DualContouring/plotting/dc_dimensions')
        print "dc_non_manifold_edges references all the vertices connected by a non-manifold edge."
        print PColors.FAIL + "ERROR: Not all manifold edges have been successfully resolved! Aborting." + PColors.ENDC
        quit()

    datasets = {'fine': fine_dataset, 'coarse': coarse_dataset}

    return dc_verts, dc_quads, dc_manifolds, datasets


def dual_contour(dataset, res_fine, is_coarse_level, do_manifold_treatment):
    """
    Applies the dual contouring algorithm to the dataset
    :param dataset: input dataset
    :param res_fine: resolution of the finest level
    :param is_coarse_level: bool gives information whether this is the coarse level
    :param do_manifold_treatment: bool states whether manifold edges should be resolved
    :return: vertices, quads and manifold edges
    """

    # Compute vertices
    dc_verts = []
    vindex = {}

    res = dataset._resolution

    print "+ generating vertices +"
    voxel_count = 0
    voxel_total = dataset.get_total_voxels()
    number_of_cube_verts = np.size(cube_verts, 0)
    for x, y, z in dataset.get_grid_iterator():
        if voxel_count % ((voxel_total + 100) / 100) == 0:
            print "%d%% generating vertices: processing voxel %d of %d." % (
                100 * voxel_count / voxel_total, voxel_count, voxel_total)
        voxel_count += 1
        o = np.array([float(x), float(y), float(z)])

        cube_signs = np.zeros(number_of_cube_verts, dtype=bool)
        # Get signs for cube
        for i in range(number_of_cube_verts):
            position = (o + cube_verts[i, :] * res)
            key = tuple(position)
            cube_signs[i] = dataset[key]

        if all(cube_signs) or not any(cube_signs):
            continue

        # Estimate hermite data
        h_data = []
        for e in cube_edges:
            if cube_signs[e[0]] != cube_signs[e[1]]:
                h_data.append(
                    estimate_hermite(dataset, o + cube_verts[e[0]] * res, o + cube_verts[e[1]] * res, res, res_fine))

        counter = 0
        v = np.array([0.0, 0.0, 0.0])

        for p in h_data:
            v += np.array(p)
            counter += 1

        v /= 1.0 * counter

        # Emit one vertex per every cube that crosses
        vindex[tuple(o)] = len(dc_verts)
        dc_verts.append(v)

    dc_quads = []
    if is_coarse_level:
        # Construct faces
        print "+ generating faces +"
        voxel_count = 0
        for x, y, z in dataset.get_grid_iterator():
            if voxel_count % ((voxel_total + 100) / 100) == 0:
                print "%d%% generating faces: processing voxel %d of %d." % (
                    100 * voxel_count / voxel_total, voxel_count, voxel_total)
            voxel_count += 1
            if not (x, y, z) in vindex:
                continue

            # Emit one edge per each edge that crosses
            o = np.array([float(x), float(y), float(z)])
            for i in range(3):
                for j in range(i):
                    if tuple(o + res * dirs[i]) in vindex and \
                                    tuple(o + res * dirs[j]) in vindex and \
                                    tuple(o + res * (dirs[i] + dirs[j])) \
                                    in vindex:
                        k = 3 - (i + j)  # normal id
                        c = True
                        d = True
                        key_ij = tuple(o + res * dirs[i] + res * dirs[j])
                        key_ijk = tuple(o + res * dirs[i] + res * dirs[j] + res * dirs[k])
                        if dataset.point_is_inside(key_ij):
                            c = dataset[key_ij]
                        if dataset.point_is_inside(key_ijk):
                            d = dataset[key_ijk]
                        if c != d:
                            dc_quads.append([vindex[tuple(o)],
                                             vindex[tuple(o + res * dirs[i])],
                                             vindex[tuple(o + res * dirs[i] + res * dirs[j])],
                                             vindex[tuple(o + res * dirs[j])]])

    dc_manifold_edges = []
    if do_manifold_treatment:
        print "+ manifold treatment +"
        dc_verts, dc_quads, dc_manifold_edges, not_resolved_edges = resolve_manifold_edges(dc_verts, vindex, dc_quads,
                                                                                           dataset)
    else:
        dc_manifold_edges = []
        not_resolved_edges = []

    return np.array(dc_verts), np.array(dc_quads), dc_manifold_edges, not_resolved_edges
