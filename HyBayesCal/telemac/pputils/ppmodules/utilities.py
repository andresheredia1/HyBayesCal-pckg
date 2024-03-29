import os, sys
import numpy as np
import struct
import subprocess
from collections import OrderedDict
from scipy import spatial
from .readMesh import *


def remove_duplicate_nodes(x, y, z):
    """ Removes duplicate nodes by keeping the unique values of (x,y,z) coordinates.
    If two nodes have the same (x,y) coordinate and a different z coordinate, this algorithm
    treats the nodes as unique. For instance, means (1,1,2) and (1,1,3) are two unique nodes.
    To avoid duplicates in the (x,y) space, use the remove_duplicate_nodes_xy function.

    :param float x:
    :param float y:
    :param float z:
    :return:
    """
    print("Removing duplicate nodes ...")

    # crop all the points to three decimals only
    x = np.around(x, decimals=3)
    y = np.around(y, decimals=3)
    z = np.around(z, decimals=3)

    # use OrderedDict to remove duplicate nodes
    # source "http://stackoverflow.com/questions/12698987"
    tmp = OrderedDict()
    for point in zip(x, y, z):
        tmp.setdefault(point[:2], point)

    # in python 3 tmp.values() is a view object that needs to be converted into a list
    mypoints = list(tmp.values())

    n_rev = len(mypoints)

    x_new = np.zeros(n_rev)
    y_new = np.zeros(n_rev)
    z_new = np.zeros(n_rev)

    for i in range(len(mypoints)):
        x_new[i] = mypoints[i][0]
        y_new[i] = mypoints[i][1]
        z_new[i] = mypoints[i][2]

    return x_new, y_new, z_new


def remove_duplicate_nodes_xy(x, y, z):
    """
    Remove duplicate nodes by keeping unique values of (x,y) coordinates only.
    The z values of the unique coordinates are assigned by a search using KDTree.
    This is hardly efficient, but it works safely (i.e., there will not be any duplicate nodes)

    :param float x:
    :param float y:
    :param float z:
    :return:
    """
    print("Removing duplicate nodes ...")

    # crop points to three decimals only
    x = np.around(x, decimals=3)
    y = np.around(y, decimals=3)
    z = np.around(z, decimals=3)

    # use OrderedDict to remove duplicate nodes
    # source "http://stackoverflow.com/questions/12698987"
    tmp = OrderedDict()
    for point in zip(x, y):
        tmp.setdefault(point[:1], point)

    # in python 3 tmp.values() is a view object that needs to be
    # converted to a list
    mypoints = list(tmp.values())

    n_rev = len(mypoints)

    x_new = np.zeros(n_rev)
    y_new = np.zeros(n_rev)
    z_new = np.zeros(n_rev)

    for i in range(len(mypoints)):
        x_new[i] = mypoints[i][0]
        y_new[i] = mypoints[i][1]

    # now that we have unique x and y, we need to assign a z to each node
    # use a cKDTree search to do this
    source = np.column_stack((x, y))
    tree = spatial.cKDTree(source)

    print("Assigning z values to unique nodes ...")
    w = [Percentage(), Bar(), ETA()]
    pbar = ProgressBar(widgets=w, maxval=n_rev).start()
    for i in range(n_rev):
        d, idx = tree.query((x_new[i], y_new[i]), k=1)
        z_new[i] = z[idx]
        pbar.update(i + 1)
    pbar.finish()

    return x_new, y_new, z_new


def adjustTriangulation(n, e, x, y, z, ikle):
    """
    Attempt to fix an invalid TIN, so that it can be processed with Matplotlib's trapezoidal map

    WARNING: The node shifting stratgy implemented here does not work!!!

    :param n:
    :param e:
    :param x:
    :param y:
    :param z:
    :param ikle:
    :return:
    """

    # this is the eps shift to be applied to the nodes
    eps = 1.0e-6

    # find area of each element
    for i in range(e):
        x1 = x[ikle[i, 0]]
        y1 = y[ikle[i, 0]]
        x2 = x[ikle[i, 1]]
        y2 = y[ikle[i, 1]]
        x3 = x[ikle[i, 2]]
        y3 = y[ikle[i, 2]]

        twoA = (x2 * y3 - x3 * y2) - (x1 * y3 - x3 * y1) + (x1 * y2 - x2 * y1)
        area = twoA / 2.0

        # assume that if area of the element is less than 1.0e-6 then
        # it will be an element that will require shifting of nodes
        if area < eps:
            # calculate edge lengths
            l12 = np.sqrt(np.power(abs(x1 - x2), 2) + np.power(abs(y1 - y2), 2))
            l23 = np.sqrt(np.power(abs(x2 - x3), 2) + np.power(abs(y2 - y3), 2))
            l31 = np.sqrt(np.power(abs(x3 - x1), 2) + np.power(abs(y3 - y1), 2))

            # print("element where node 1 is in the middle")

            if (l23 > l31) and (l23 > l12):
                # node 1 is middle, shift it by +ve delta
                x1 = x1 + eps
                y1 = y1 + eps

                # shift nodes 2 and 2 by a -ve delta
                x2 = x2 - eps
                y2 = y2 - eps

                x3 = x3 - eps
                y3 = y3 - eps

            elif (l31 > l12) and (l31 > l23):
                # node 2 is middle, shift it by +ve delta
                x2 = x2 + eps
                y2 = y2 + eps

                # shift nodes 1 and 3 by a -ve delta
                x1 = x1 - eps
                y1 = y1 - eps

                x3 = x3 - eps
                y3 = y3 - eps

            elif (l12 > l23) and (l12 > l31):
                # node 3 is middle, shift it by +ve delta
                x3 = x3 + eps
                y3 = y3 + eps

                # shift nodes 1 and 2 by a -ve delta
                x1 = x1 - eps
                y1 = y1 - eps

                x2 = x2 - eps
                y2 = y2 - eps

            else:
                # this is needed as the part of the code that removes
                # duplicate nodes allows for two nodes at the same location
                # as long as they have a different z!

                # has to be fixed in the scripts that generate the tin
                # (i.e., gis2triangle.py and gis2triangle_kd.py)

                # print("element " + str(i+1))
                # print((l12,l23,l31))

                if l12 < eps:
                    x1 = x1 + eps
                    y1 = y1 + eps
                elif l23 < eps:
                    x2 = x2 + eps
                    y2 = y2 + eps
                elif l31 < eps:
                    x3 = x3 + eps
                    y3 = y3 + eps

            # update the coordinates in the input arrays
            x[ikle[i, 0]] = x1
            y[ikle[i, 0]] = y1
            x[ikle[i, 1]] = x2
            y[ikle[i, 1]] = y2
            x[ikle[i, 2]] = x3
            y[ikle[i, 2]] = y3

            # returns the shifted x and y coordinates
    return x, y


def minverse(M):
    """
    Convert a matrix-like array into a 1d array to facilitate referencing

    :param numpy. array M:
    :return:
    """

    mm = np.reshape(M, 9)

    x1 = mm[1]
    y1 = mm[2]
    x2 = mm[4]
    y2 = mm[5]
    x3 = mm[7]
    y3 = mm[8]

    twoA = (x2 * y3 - x3 * y2) - (x1 * y3 - x3 * y1) + (x1 * y2 - x2 * y1)
    if twoA < 1.0E-6:
        print("zero area triangle used for interpolation")

    minv = np.zeros(9)

    minv[0] = (1.0 / twoA) * (y2 - y3)
    minv[1] = (1.0 / twoA) * (y3 - y1)
    minv[2] = (1.0 / twoA) * (y1 - y2)

    minv[3] = (1.0 / twoA) * (x3 - x2)
    minv[4] = (1.0 / twoA) * (x1 - x3)
    minv[5] = (1.0 / twoA) * (x2 - x1)

    minv[6] = (1.0 / twoA) * (x2 * y3 - x3 * y2)
    minv[7] = (1.0 / twoA) * (x3 * y1 - x1 * y3)
    minv[8] = (1.0 / twoA) * (x1 * y2 - x2 * y1)

    # convert minv into a 2d array
    minv_matrix = np.reshape(minv, (3, 3))

    return minv_matrix


#

# Improved point in polygon test which includes edge
# and vertex points

def point_in_poly(x, y, poly):
    """
    Check if a point is located within a polygon.

    This function was adapted from
    http://geospatialpython.com/2011/08/point-in-polygon-2-on-line.html

    :param float x:
    :param float y:
    :param poly:
    :return:
    """
    # check if point is a vertex
    if (x, y) in poly:
        return "IN"

    # check if point is on a boundary
    for i in range(len(poly)):
        p1 = None
        p2 = None
        if i == 0:
            p1 = poly[0]
            p2 = poly[1]
        else:
            p1 = poly[i - 1]
            p2 = poly[i]
        if p1[1] == p2[1] and p1[1] == y and min(p1[0], p2[0]) < x < max(p1[0], p2[0]):
            return "IN"

    n = len(poly)
    inside = False

    p1x, p1y = poly[0]
    for i in range(n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    else:
                        xints = 10 ** 5
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x, p1y = p2x, p2y

    if inside:
        return "IN"
    else:
        return "OUT"


def ptInTriangle(pt, tri):
    """
    Check if a point is located within a triangle

    Adapted Python version of ptInTriangle from:
    http://stackoverflow.com/questions/2049582

    :example:
        pt =  np.array([0.5, 0.0])
        tri = np.array([[1.0, 1.0], [1.0, 0.0], [0.0, 0.0]]  )
        print(ptInTriangle(pt, tri))

    :param list or np.array pt:
    :param list or np.array tri:
    :return:
    """
    px = pt[0]
    py = pt[1]

    p0x = tri[0, 0]
    p0y = tri[0, 1]

    p1x = tri[1, 0]
    p1y = tri[1, 1]

    p2x = tri[2, 0]
    p2y = tri[2, 1]

    dX = px - p2x
    dY = py - p2y
    dX21 = p2x - p1x
    dY12 = p1y - p2y
    D = dY12 * (p0x - p2x) + dX21 * (p0y - p2y)
    s = dY12 * dX + dX21 * dY
    t = (p2y - p0y) * dX + (p0x - p2x) * dY

    if D < 0:
        return (s <= 0) and (t <= 0) and (s + t >= D)
    else:
        return (s >= 0) and (t >= 0) and (s + t <= D)


def idwm(elev, x, y):
    """
    Uses an input xyz array (elev), and a coordinate x,y, to output the z values of the
    input coordinate using  Pad Prodanovic's fortran code idwm.f90

    :param np.array elev:
    :param float x:
    :param float y:
    :return:
    """
    # define presets
    # set min_prev vars to large numbers
    min1cur = 99999.9
    min2cur = 99999.9
    min3cur = 99999.9
    min4cur = 99999.9

    min1pre = 99999.9
    min2pre = 99999.9
    min3pre = 99999.9
    min4pre = 99999.9

    # initialize min_loc
    min1loc = -1
    min2loc = -1
    min3loc = -1
    min4loc = -1

    # finds min and max of the elev data
    # print(np.amin(elev[2,:]), np.amax(elev[2,:]))

    # number of points in the elev data
    n = len(elev[0, :])

    dist = np.zeros(n)
    xdist = np.subtract(elev[0, :], x)
    ydist = np.subtract(elev[1, :], y)

    dist = np.sqrt(np.power(xdist, 2.0) + np.power(ydist, 2.0))

    # TODO - fix this computationally very expensive loop
    for i in range(n):
        # quadrant 1
        if elev[0, i] >= x and elev[1, i] >= y:
            if dist[i] < min1pre:
                min1cur = dist[i]
                min1loc = i

        # quadrant 2
        if elev[0, i] < x and elev[1, i] >= y:
            if dist[i] < min2pre:
                min2cur = dist[i]
                min2loc = i

        # quadrant 3
        if elev[0, i] < x and elev[1, i] < y:
            if dist[i] < min3pre:
                min3cur = dist[i]
                min3loc = i

        # quadrant 4
        if elev[0, i] > x and elev[1, i] < y:
            if dist[i] < min4pre:
                min4cur = dist[i]
                min4loc = i

        min1pre = min1cur
        min2pre = min2cur
        min3pre = min3cur
        min4pre = min4cur

    # fix division by zero error (if the point (x,y) is exactly on a node of elev array)
    if min1cur < 1.0E-6:
        min1cur = 1.0E-6

    if min2cur < 1.0E-6:
        min2cur = 1.0E-6

    if min3cur < 1.0E-6:
        min3cur = 1.0E-6

    if min4cur < 1.0E-6:
        min4cur = 1.0E-6

    # calculate the weights
    den = (1.0 / (min1cur ** 2)) + (1.0 / (min2cur ** 2)) + (1.0 / (min3cur ** 2)) + \
          (1.0 / (min4cur ** 2))

    w1 = (1.0 / (min1cur ** 2)) / den
    w2 = (1.0 / (min2cur ** 2)) / den
    w3 = (1.0 / (min3cur ** 2)) / den
    w4 = (1.0 / (min4cur ** 2)) / den

    # if minxloc is negative, do not let Python use the last
    # item in the array in the calculation (which is what it would do)

    if min1loc < 0:
        tmp1 = 0.0
    else:
        tmp1 = elev[2, min1loc]

    if min2loc < 0:
        tmp2 = 0.0
    else:
        tmp2 = elev[2, min2loc]

    if min3loc < 0:
        tmp3 = 0.0
    else:
        tmp3 = elev[2, min3loc]

    if min4loc < 0:
        tmp4 = 0.0
    else:
        tmp4 = elev[2, min4loc]

    z = w1 * tmp1 + w2 * tmp2 + w3 * tmp3 + w4 * tmp4

    return z


def CCW(x1, y1, x2, y2, x3, y3):
    """
    Check if points are counter-clockwise (CCW)

    :param float x1:
    :param float y1:
    :param float x2:
    :param float y2:
    :param float x3:
    :param float y3:
    :return bool:
    """
    return (y3 - y1) * (x2 - x1) > (y2 - y1) * (x3 - x1)


def getIPOBO_IKLE(adcirc_file):
    """
    Takes in an adcirc file and returns the IPOBO and IKLE arrays. Also generates temp.cli
    file for use with Telemac. This version uses the output from bnd_extr_stbtel.f90 Fortran.

    Note: This function returns ikle and the ipobo arrays that are one based, as this is
    what telemac needs.

    :param str adcirc_file: name of an adcirc grd file
    :return:
    """

    try:
        # this only works when the paths are sourced
        pputils_path = os.environ["PPUTILS"]
    except KeyError:
        pputils_path = os.getcwd()

    # reads the adcirc file (note the ikle here is zero based)
    n, e, x, y, z, ikle = readAdcirc(adcirc_file)

    # make sure the elements are oriented CCW going through each element
    for i in range(len(ikle)):
        # if the element is not CCW then must change its orientation
        if not CCW(x[ikle[i, 0]], y[ikle[i, 0]], x[ikle[i, 1]], y[ikle[i, 1]],
                   x[ikle[i, 2]], y[ikle[i, 2]]):
            t0 = ikle[i, 0]
            t1 = ikle[i, 1]
            t2 = ikle[i, 2]

            # switch orientation
            ikle[i, 0] = t2
            ikle[i, 2] = t0

    # the above returns ikle that is zero based, but telemac will need them to be
    # one-based; conversion is done below
    ikle[:, 0] = ikle[:, 0] + 1
    ikle[:, 1] = ikle[:, 1] + 1
    ikle[:, 2] = ikle[:, 2] + 1

    # temporary ipobo.txt (this is the output from the bnd_extr_stbtel.f90)
    temp_ipobo = "ipobo.txt"

    # generate the ppIPOB array by running a pre-compiled binary of bnd_extr_stbtel.f90
    # determine if the system is 32 or 64 bit
    archtype = struct.calcsize("P") * 8
    # get the current directory
    curdir = os.getcwd()

    if os.name == "posix":
        # if OS is Linux, determine processor type (requires Linux!)
        proctype = os.uname()[4][:]

        if proctype == "i686":
            callstr = pputils_path + "/boundary/bin/bnd_extr_stbtel_32"
        elif proctype == "x86_64":
            callstr = pputils_path + "/boundary/bin/bnd_extr_stbtel_64"
        elif proctype == "armv7l":
            callstr = pputils_path + "/boundary/bin/bnd_extr_stbtel_pi32"

        # make sure the binary is allowed to be executed
        subprocess.call(["chmod", "+x", callstr])

        # execute the binary
        # print("Executing bnd_extr_stbtel program ...")
        subprocess.call([callstr, adcirc_file, temp_ipobo])

    if os.name == "nt":
        # nt corresponds to windows [still to update]
        callstr = ".\\boundary\\bin\\bnd_extr_stbtel_32.exe"
        subprocess.call([callstr, adcirc_file, temp_ipobo])

    # read the ipobo.txt file, populate the ppIPOB variable, and write the *.cli file
    # read the ipobo.txt file as a master list
    line = list()
    with open("ipobo.txt", "r") as f1:
        for i in f1:
            line.append(i)

    # write temp.cli file
    fcli = open("temp.cli", "w")
    cli_base = str("2 2 2 0.000 0.000 0.000 0.000 2 0.000 0.000 0.000 ")

    # write final *.cli file
    for i in range(len(line)):
        fcli.write(cli_base + str(int(line[i])) + " " + str(i + 1) + "\n")

    # close the *.cli file
    fcli.close()

    # note the temp.cli gets renamed in the main script
    # now store the ppIPOB array
    ppIPOB = np.zeros(n, dtype=np.int32)
    ipob_count = 0

    # return the ppIPOB array that is one-based
    for i in range(len(line)):
        ipob_count = ipob_count + 1
        ppIPOB[int(line[i]) - 1] = ipob_count

    # remove the ipobo.txt file
    os.remove("ipobo.txt")

    return n, e, x, y, z, ikle, ppIPOB
