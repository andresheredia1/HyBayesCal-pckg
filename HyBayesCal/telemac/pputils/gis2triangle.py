#!/usr/bin/env python3
#
# +!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!
#                                                                       #
#                                 gis2triangle_kd.py                    # 
#                                                                       #
# +!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!+!
#
# Author: Pat Prodanovic, Ph.D., P.Eng., modularized by Sebastian Schwindt
#
# Date: June 29, 2015 / July 22, 2022

from progressbar import ProgressBar, Bar, Percentage, ETA
from ppmodules.utilities import *


def gis2triangle(nodes_csv, boundary_csv, lines_csv=None, out_poly="out.poly", holes_csv=None, duplicates_flag=True):
    """ Functions takes a text file of the geometry generated in qgis (or any other gis or cad software) and produces
    geometry files used by the triangle mesh generator program (i.e., it writes a *.poly geometry file for use with
    a triangle mesh generator. This script is significantly slower than gis2triangle_kd.py, as it uses a semi brute
    force method to search for nodes. This script should only be used only when gis2triangle_kd.py script does not
    produce satisfactory results.

    :param str nodes_csv: full path to and name of nodes CSV file. The nodes file consist of x,y,z or x,y,z,size; The
                          size parameter is an optional input, and is used by gmsh as an extra parameter that forces
                          an element size around particular nodes (not relevant for triangle). The nodes file must be
                          comma separated, and have no header lines.
    :param str boundary_csv: full path to and name of boundary CSV file. The boundary file is represents a closed line
                          around nodes.csv the first and last nodes are identical. It has the columns shapeid,x,y of
                          for all lines in the file. The boundary is defined with a distinct id (i.e., shapeid of 0).
    :param str lines_csv: full path to and name of lines CSV file. The lines file can include open or closed polylines.
                          The file has the columns shapeid,x,y, where x,y have to match nodes.csv. Every line has to
                          have an individual (integer) shapeid. If no constraint lines are in the mesh, use the default
                          value of ``None``.
    :param str holes_csv: optional full path to and name of holes CSV file (default is ``None``). The holes file is
                          generated by placing a single node marker inside a closed line constraint. The holes file must
                          include x and y coordinates within the hole boundary. If the mesh does not have any holes
                          (islands) skip this argument. Note that a triangle hole has a different format than gmsh.
    :param str out_poly: name of output adcirc grid file (will be saved to where nodes_csv lives) containing the TIN.
    :param bool duplicates_flag: optional boolen flag (default: ``True``) to ignore removal of duplicate nodes in
                        nodes.csv. By default, duplicate nodes are removed from nodes.csv.
    :returns: None
    """

    # find out if the nodes file is x,y,z or x,y,x,size
    with open(nodes_csv, 'r') as f:
        line = next(f)  # read 1 line
        n_attr = len(line.split(','))

    # to create the output file
    fout = open(out_poly, "w")

    # use numpy to read the file
    # each column in the file is a row in data read by no.loadtxt method
    nodes_data = np.loadtxt(nodes_csv, delimiter=',', skiprows=0, unpack=True)
    boundary_data = np.loadtxt(boundary_csv, delimiter=',', skiprows=0, unpack=True)
    if lines_csv:
        lines_data = np.loadtxt(lines_csv, delimiter=',', skiprows=0, unpack=True)
    if holes_csv:
        holes_data = np.loadtxt(holes_csv, delimiter=',', skiprows=0, unpack=True)

    # master nodes in the file (from the nodes file)
    x = nodes_data[0, :]
    y = nodes_data[1, :]
    z = nodes_data[2, :]
    if n_attr == 4:
        size = nodes_data[3, :]
    else:
        size = np.zeros(len(x))

    # to check for duplicate nodes
    # crop all the points to three decimals only
    x = np.around(x, decimals=3)
    y = np.around(y, decimals=3)
    z = np.around(z, decimals=3)
    size = np.around(size, decimals=3)

    # this is a method from ppmodules/utilities.py that removes duplicates
    if duplicates_flag:
        x, y, z = remove_duplicate_nodes(x, y, z)

    # n is the number of nodes
    n = len(x)

    # creates node numbers from the nodes file
    node = np.zeros(n, dtype=np.int32)

    # when I made the change to python 3, had to use np.column_stack
    # http://stackoverflow.com/questions/28551279/error-running-scipy-kdtree-example

    # to create the tuples of the master points
    points = np.column_stack((x, y))
    tree = spatial.cKDTree(points)

    # if node is part of boundary or lines, then it is not embedded
    is_node_emb = np.zeros(n, dtype=np.int32)
    for i in range(0, n):
        node[i] = i + 1
        is_node_emb[i] = 1

    # boundary data
    shapeid_bnd = boundary_data[0, :]
    x_bnd = boundary_data[1, :]
    y_bnd = boundary_data[2, :]

    # round boundary nodes to three decimals
    x_bnd = np.around(x_bnd, decimals=3)
    y_bnd = np.around(y_bnd, decimals=3)

    # number of nodes in the boundary file
    n_bnd = len(x_bnd)

    # count lines from boundary lines
    count_bnd = 0

    # lines data
    if lines_csv:
        shapeid_lns = lines_data[0, :]
        x_lns = lines_data[1, :]
        y_lns = lines_data[2, :]

        # round lines nodes to three decimals
        x_lns = np.around(x_lns, decimals=3)
        y_lns = np.around(y_lns, decimals=3)

        # number of nodes in the lines file
        n_lns = len(x_lns)

    count_lns = 0

    # writes *.poly geometry file for use in triangle mesh generator
    # writes the *.poly header data for nodes
    fout.write(str(n) + " " + str("2 1 0") + "\n")

    # writes the nodes in triangle format
    for i in range(0, n):
        fout.write(str(i + 1) + " " + str("{:.3f}".format(x[i])) +
                   str(" ") + str("{:.3f}".format(y[i])) + str(" ") +
                   str("{:.3f}".format(z[i])) + "\n")

    ############################################################################
    # BOUNDARY LINES
    # index of the minimum, for each boundary node
    minidx = np.zeros(n_bnd, dtype=np.int32)
    # distance between each boundary node and node in the master nodes file

    # write the boundary in gmsh format
    for i in range(0, n_bnd - 1):
        if i == 0:
            count_bnd = count_bnd + 1
        else:
            count_bnd = count_bnd + 1

    # the lines numbering continues from the boundary numbering
    count_lns = count_bnd + 1

    # CONSTRAINT LINES
    if lines_csv:
        # index for the minimum, for each lines node
        minidx_lns = np.zeros(n_lns, dtype=np.int32)
        # distance between each lines node and node in the master nodes file
        dist_lns = np.zeros(n)

        cur_lns_shapeid = shapeid_lns[0]
        prev_lns_shapeid = shapeid_lns[0]

        # write the constraint lines
        for i in range(0, n_lns - 1):
            if i > 0:
                cur_lns_shapeid = shapeid_lns[i]
                prev_lns_shapeid = shapeid_lns[i - 1]
                if cur_lns_shapeid - prev_lns_shapeid < 0.001:
                    count_lns = count_lns + 1
    ############################################################################

    # this is really inefficient, but all of the loops above (between ####) are
    # simply to count the number of lines in the file (boundary nodes and
    # constraint lines together.

    # this is a cheating way to do this, but it will have to do for now.
    # discovered through debug testing
    if lines_csv:
        fout.write(str(count_lns - 1) + " 0" + "\n")
    else:
        fout.write(str(count_lns) + " 0" + "\n")

    # now repeat the loops between the #### are write the lines (boundary and
    # constraint)
    count_bnd = 0
    count_lns = 0
    ############################################################################
    # BOUNDARY LINES
    print('Assigning z values to each boundary vertex ...')
    # index of the minimum, for each boundary node
    minidx = np.zeros(n_bnd, dtype=np.int32) - 1

    pt_bnd = list()

    for i in range(0, n_bnd):
        pt_bnd.append(x_bnd[i])
        pt_bnd.append(y_bnd[i])

        # find the index of the min point
        d, minidx_temp = tree.query(pt_bnd, 1)

        minidx[i] = minidx_temp
        if minidx[i] < 0:
            print('Python outputs a negative index ... converting to positive')
            print('Negative index of ', minidx[i], ' converted to')
            minidx[i] = minidx[i] * -1 + 1
            print(minidx[i], '\n')

        # fout.write(str(i) + " " + str(minidx[i]) + "\n")

        # fill in the is_node_emb array
        is_node_emb[minidx[i]] = 0

        # remove the node to search for
        pt_bnd.remove(x_bnd[i])
        pt_bnd.remove(y_bnd[i])

    # write the boundary in triangle format
    for i in range(0, n_bnd - 1):
        if i == 0:
            fout.write(str(i + 1) + str(" ") + str(node[minidx[0]])
                       + str(" ") + str(node[minidx[1]]) + "\n")
            count_bnd = count_bnd + 1
        else:
            fout.write(str(i + 1) + str(" ") + str(node[minidx[i]])
                       + str(" ") + str(node[minidx[i + 1]]) + "\n")
            count_bnd = count_bnd + 1

    # the lines numbering continues from the boundary numbering
    count_lns = count_bnd + 1

    # CONSTRAINT LINES
    print('Assigning z values to each breakline vertex ...')
    if lines_csv:
        w = [Percentage(), Bar(), ETA()]
        pbar = ProgressBar(widgets=w, maxval=n_lns).start()
        # index for the minimum, for each lines node
        minidx_lns = np.zeros(n_lns, dtype=np.int32) - 1

        pt_lns = list()

        for i in range(0, n_lns):
            pt_lns.append(x_lns[i])
            pt_lns.append(y_lns[i])

            # find the index of each lines point
            d, minidx_lns_temp = tree.query(pt_lns, 1)

            minidx_lns[i] = minidx_lns_temp

            # fout.write(str(i) + " " + str(minidx_lns[i]) + "\n")

            # fill in the is_node_emb array
            is_node_emb[minidx_lns[i]] = 0

            # to remove the node to search for
            pt_lns.remove(x_lns[i])
            pt_lns.remove(y_lns[i])

            # update the pbar
            pbar.update(i + 1)

        cur_lns_shapeid = shapeid_lns[0]
        prev_lns_shapeid = shapeid_lns[0]
        pbar.finish()

        # write the constraint lines
        for i in range(0, n_lns):
            if i > 0:
                cur_lns_shapeid = shapeid_lns[i]
                prev_lns_shapeid = shapeid_lns[i - 1]
                if (cur_lns_shapeid - prev_lns_shapeid < 0.001):
                    # if (node[minidx_lns[i-1]] != node[minidx_lns[i]]):
                    # fout.write(str(cur_lns_shapeid) + " " + str(prev_lns_shapeid) + " ")
                    fout.write(str(count_lns) + str(" ") +
                               str(node[minidx_lns[i - 1]]) + str(" ") + str(node[minidx_lns[i]]) + "\n")
                    count_lns = count_lns + 1
    ############################################################################

    # lastly, write the holes
    print('Writing holes data ...')
    # holes data
    if holes_csv:
        # find out how many holes
        n_hls = len(open(holes_csv).readlines())

        # counters for hole points
        shapeid_hls1 = -1
        shapeid_hls = -1

        if n_hls == 1:
            master = list()
            with open(holes_csv, 'r') as f:
                for line in f:
                    master.append(line)
            tmp = master[0].split(',')
            shapeid_hls1 = shapeid_hls1 + 1
            x_hls1 = float(tmp[0])
            y_hls1 = float(tmp[1])
            fout.write(str(n_hls) + '\n')
            fout.write(str(shapeid_hls1) + ' ' + str(x_hls1) + ' ' + str(y_hls1) + '\n')
        else:
            x_hls = holes_data[0, :]
            y_hls = holes_data[1, :]

            # round lines nodes to three decimals
            x_hls = np.around(x_hls, decimals=3)
            y_hls = np.around(y_hls, decimals=3)

            # n_hls = len(x_hls)
            fout.write(str(n_hls) + '\n')
            for i in range(n_hls):
                shapeid_hls = shapeid_hls + 1
                fout.write(str(shapeid_hls) + ' ' + str(x_hls[i]) + ' ' + str(y_hls[i]) + '\n')
    else:
        fout.write(str(0))
