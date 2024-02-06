#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-2-Clause
# Copyright (c) 2018 Jakub Červený

import sys


def gilbert3d(width, height, depth):
    """
    Generalized Hilbert ('Gilbert') space-filling curve for arbitrary-sized
    3D rectangular grids. Generates discrete 3D coordinates to fill a cuboid
    of size (width x height x depth). Even sizes are recommended in 3D.
    """

    if width >= height and width >= depth:
       yield from generate3d(0, 0, 0,
                             width, 0, 0,
                             0, height, 0,
                             0, 0, depth)

    elif height >= width and height >= depth:
       yield from generate3d(0, 0, 0,
                             0, height, 0,
                             width, 0, 0,
                             0, 0, depth)

    else: # depth >= width and depth >= height
       yield from generate3d(0, 0, 0,
                             0, 0, depth,
                             width, 0, 0,
                             0, height, 0)

def gilbertxyz2d(x,y,z,width, height, depth):
    """
    Generalized Hilbert ('Gilbert') space-filling curve for arbitrary-sized
    3D rectangular grids. Generates discrete 3D coordinates to fill a cuboid
    of size (width x height x depth). Even sizes are recommended in 3D.
    """

    if width >= height and width >= depth:
       return gilbertxyz2d_r( 0,x,y,z,
                              0, 0, 0,
                              width, 0, 0,
                              0, height, 0,
                              0, 0, depth)

    elif height >= width and height >= depth:
       return gilbertxyz2d_r( 0,x,y,z,
                              0, 0, 0,
                              0, height, 0,
                              width, 0, 0,
                              0, 0, depth)

    else: # depth >= width and depth >= height
       return gilbertxyz2d_r( 0,x,y,z,
                              0, 0, 0,
                              0, 0, depth,
                              width, 0, 0,
                              0, height, 0)

def gilbertd2xyz(idx,width, height, depth):
    """
    Generalized Hilbert ('Gilbert') space-filling curve for arbitrary-sized
    3D rectangular grids. Generates discrete 3D coordinates to fill a cuboid
    of size (width x height x depth). Even sizes are recommended in 3D.
    """

    if width >= height and width >= depth:
       return gilbertd2xyz_r( idx, 0,
                              0, 0, 0,
                              width, 0, 0,
                              0, height, 0,
                              0, 0, depth)

    elif height >= width and height >= depth:
       return gilbertd2xyz_r( idx, 0,
                              0, 0, 0,
                              0, height, 0,
                              width, 0, 0,
                              0, 0, depth)

    else: # depth >= width and depth >= height
       return gilbertd2xyz_r( idx, 0,
                              0, 0, 0,
                              0, 0, depth,
                              width, 0, 0,
                              0, height, 0)


def sgn(x):
    return -1 if x < 0 else (1 if x > 0 else 0)

def inbounds(x,y,z, x_s,y_s,z_s, ax,ay,az, bx,by,bz, cx,cy,cz):

    dx = ax+bx+cx
    dy = ay+by+cy
    dz = az+bz+cz

    if dx<0: 
        if (x>x_s) or (x<=(x_s+dx)): return False
    else:
        if (x<x_s) or (x>=(x_s+dx)): return False

    if dy<0:
        if (y>y_s) or (y<=(y_s+dy)): return False
    else:
        if (y<y_s) or (y>=(y_s+dy)): return False

    if dz<0:
        if (z>z_s) or (z<=(z_s+dz)): return False
    else:
        if (z<z_s) or (z>=(z_s+dz)): return False

    return True


def gilbertd2xyz_r(dst_idx, cur_idx,
                   x, y, z,
                   ax, ay, az,
                   bx, by, bz,
                   cx, cy, cz):

    w = abs(ax + ay + az)
    h = abs(bx + by + bz)
    d = abs(cx + cy + cz)

    (dax, day, daz) = (sgn(ax), sgn(ay), sgn(az)) # unit major direction ("right")
    (dbx, dby, dbz) = (sgn(bx), sgn(by), sgn(bz)) # unit ortho direction ("forward")
    (dcx, dcy, dcz) = (sgn(cx), sgn(cy), sgn(cz)) # unit ortho direction ("up")

    _dx = dax+dbx+dcx
    _dy = day+dby+dcy
    _dz = daz+dbz+dcz
    _di = dst_idx - cur_idx

    # trivial row/column fills
    if h == 1 and d == 1:
        return (x + dax*_di, y + day*_di, z + daz*_di)

    if w == 1 and d == 1:
        return (x + dbx*_di, y + dby*_di, z + dbz*_di)

    if w == 1 and h == 1:
        return (x + dcx*_di, y + dcy*_di, z + dcz*_di)

    (ax2, ay2, az2) = (ax//2, ay//2, az//2)
    (bx2, by2, bz2) = (bx//2, by//2, bz//2)
    (cx2, cy2, cz2) = (cx//2, cy//2, cz//2)

    w2 = abs(ax2 + ay2 + az2)
    h2 = abs(bx2 + by2 + bz2)
    d2 = abs(cx2 + cy2 + cz2)

    # prefer even steps
    if (w2 % 2) and (w > 2): (ax2,ay2,az2) = (ax2+dax, ay2+day, az2+daz)
    if (h2 % 2) and (h > 2): (bx2,by2,bz2) = (bx2+dbx, by2+dby, bz2+dbz)
    if (d2 % 2) and (d > 2): (cx2,cy2,cz2) = (cx2+dcx, cy2+dcy, cz2+dcz)

    # wide case, split in w only
    if (2*w > 3*h) and (2*w > 3*d):
        nxt_idx = cur_idx + abs( (ax2+ay2+az2)*(bx+by+bz)*(cx+cy+cz) )
        if (cur_idx <= dst_idx) and (dst_idx < nxt_idx):
            return gilbertd2xyz_r(dst_idx,cur_idx,
                                  x, y, z,
                                  ax2, ay2, az2,
                                  bx, by, bz,
                                  cx, cy, cz)
        cur_idx = nxt_idx
 
        #nxt_idx = cur_idx + abs( ((ax-ax2)+(ay-ay2)+(az-az2))*(bx+by+bz)*(cx+cy+cz) )
        #if (cur_idx <= dst_idx) and (dst_idx < nxt_idx):
        return gilbertd2xyz_r(dst_idx,cur_idx,
                              x+ax2, y+ay2, z+az2,
                              ax-ax2, ay-ay2, az-az2,
                              bx, by, bz,
                              cx, cy, cz)

    # do not split in d
    elif 3*h > 4*d:
        nxt_idx = cur_idx + abs( (bx2+by2+bz2)*(cx+cy+cz)*(ax2+ay2+az2) )
        if (cur_idx <= dst_idx) and (dst_idx < nxt_idx):
            return gilbertd2xyz_r(dst_idx,cur_idx,
                                  x, y, z,
                                  bx2, by2, bz2,
                                  cx, cy, cz,
                                  ax2, ay2, az2)
        cur_idx = nxt_idx

        nxt_idx = cur_idx + abs( (ax+ay+az)*((bx-bx2)+(by-by2)+(bz-bz2))*(cx+cy+cz) )
        if (cur_idx <= dst_idx) and (dst_idx < nxt_idx):
            return gilbertd2xyz_r(dst_idx,cur_idx,
                                  x+bx2, y+by2, z+bz2,
                                  ax, ay, az,
                                  bx-bx2, by-by2, bz-bz2,
                                  cx, cy, cz)
        cur_idx = nxt_idx

        return gilbertd2xyz_r(dst_idx,cur_idx,
                              x+(ax-dax)+(bx2-dbx),
                              y+(ay-day)+(by2-dby),
                              z+(az-daz)+(bz2-dbz),
                              -bx2, -by2, -bz2,
                              cx, cy, cz,
                              -(ax-ax2), -(ay-ay2), -(az-az2))

    # do not split in h
    elif 3*d > 4*h:
        nxt_idx = cur_idx + abs( (cx2+cy2+cz2)*(ax2+ay2+az2)*(bx+by+bz) )
        if (cur_idx <= dst_idx) and (dst_idx < nxt_idx):
            return gilbertd2xyz_r(dst_idx,cur_idx,
                                  x, y, z,
                                  cx2, cy2, cz2,
                                  ax2, ay2, az2,
                                  bx, by, bz)
        cur_idx = nxt_idx

        nxt_idx = cur_idx + abs( (ax+ay+az)*(bx+by+bz)*((cx-cx2)+(cy-cy2)+(cz-cz2)) )
        if (cur_idx <= dst_idx) and (dst_idx < nxt_idx):
            return gilbertd2xyz_r(dst_idx,cur_idx,
                                  x+cx2, y+cy2, z+cz2,
                                  ax, ay, az,
                                  bx, by, bz,
                                  cx-cx2, cy-cy2, cz-cz2)
        cur_idx = nxt_idx

        return gilbertd2xyz_r(dst_idx,cur_idx,
                              x+(ax-dax)+(cx2-dcx),
                              y+(ay-day)+(cy2-dcy),
                              z+(az-daz)+(cz2-dcz),
                              -cx2, -cy2, -cz2,
                              -(ax-ax2), -(ay-ay2), -(az-az2),
                              bx, by, bz)

    # regular case, split in all w/h/d
    else:
        nxt_idx = cur_idx + abs( (bx2+by2+bz2)*(cx2+cy2+cz2)*(ax2+ay2+az2) )
        if (cur_idx <= dst_idx) and (dst_idx < nxt_idx):
            return gilbertd2xyz_r(dst_idx,cur_idx,
                                  x, y, z,
                                  bx2, by2, bz2,
                                  cx2, cy2, cz2,
                                  ax2, ay2, az2)
        cur_idx = nxt_idx

        nxt_idx = cur_idx + abs( (cx+cy+cz)*(ax2+ay2+az2)*((bx-bx2)+(by-by2)+(bz-bz2)) )
        if (cur_idx <= dst_idx) and (dst_idx < nxt_idx):
            return gilbertd2xyz_r(dst_idx,cur_idx,
                                  x+bx2, y+by2, z+bz2,
                                  cx, cy, cz,
                                  ax2, ay2, az2,
                                  bx-bx2, by-by2, bz-bz2)
        cur_idx = nxt_idx

        nxt_idx = cur_idx + abs( (ax+ay+az)*(-bx2-by2-bz2)*(-(cx-cx2)-(cy-cy2)-(cz-cz2)) )
        if (cur_idx <= dst_idx) and (dst_idx < nxt_idx):
            return gilbertd2xyz_r(dst_idx, cur_idx,
                                  x+(bx2-dbx)+(cx-dcx),
                                  y+(by2-dby)+(cy-dcy),
                                  z+(bz2-dbz)+(cz-dcz),
                                  ax, ay, az,
                                  -bx2, -by2, -bz2,
                                  -(cx-cx2), -(cy-cy2), -(cz-cz2))
        cur_idx = nxt_idx

        nxt_idx = cur_idx + abs( (-cx-cy-cz)*(-(ax-ax2)-(ay-ay2)-(az-az2))*((bx-bx2)+(by-by2)+(bz-bz2)) )
        if (cur_idx <= dst_idx) and (dst_idx < nxt_idx):
            return gilbertd2xyz_r(dst_idx,cur_idx,
                                  x+(ax-dax)+bx2+(cx-dcx),
                                  y+(ay-day)+by2+(cy-dcy),
                                  z+(az-daz)+bz2+(cz-dcz),
                                  -cx, -cy, -cz,
                                  -(ax-ax2), -(ay-ay2), -(az-az2),
                                  bx-bx2, by-by2, bz-bz2)
        cur_idx = nxt_idx

        return gilbertd2xyz_r(dst_idx,cur_idx,
                              x+(ax-dax)+(bx2-dbx),
                              y+(ay-day)+(by2-dby),
                              z+(az-daz)+(bz2-dbz),
                              -bx2, -by2, -bz2,
                              cx2, cy2, cz2,
                              -(ax-ax2), -(ay-ay2), -(az-az2))

def gilbertxyz2d_r(cur_idx,
                   x_dst,y_dst,z_dst,
                   x, y, z,
                   ax, ay, az,
                   bx, by, bz,
                   cx, cy, cz):

    w = abs(ax + ay + az)
    h = abs(bx + by + bz)
    d = abs(cx + cy + cz)

    (dax, day, daz) = (sgn(ax), sgn(ay), sgn(az)) # unit major direction ("right")
    (dbx, dby, dbz) = (sgn(bx), sgn(by), sgn(bz)) # unit ortho direction ("forward")
    (dcx, dcy, dcz) = (sgn(cx), sgn(cy), sgn(cz)) # unit ortho direction ("up")

    # trivial row/column fills
    if h == 1 and d == 1:
        return cur_idx + (dax*(x_dst-x)) + (day*(y_dst-y)) + (daz*(z_dst-z)); 
        #for i in range(0, w):
        #    yield(x, y, z)
        #    (x, y, z) = (x + dax, y + day, z + daz)
        #return

    if w == 1 and d == 1:
        return cur_idx + (dbx*(x_dst-x)) + (dby*(y_dst-y)) + (dbz*(z_dst-z)); 
        #for i in range(0, h):
        #    yield(x, y, z)
        #    (x, y, z) = (x + dbx, y + dby, z + dbz)
        #return

    if w == 1 and h == 1:
        return cur_idx + (dcx*(x_dst-x)) + (dcy*(y_dst-y)) + (dcz*(z_dst-z)); 
        #for i in range(0, d):
        #    yield(x, y, z)
        #    (x, y, z) = (x + dcx, y + dcy, z + dcz)
        #return

    (ax2, ay2, az2) = (ax//2, ay//2, az//2)
    (bx2, by2, bz2) = (bx//2, by//2, bz//2)
    (cx2, cy2, cz2) = (cx//2, cy//2, cz//2)

    w2 = abs(ax2 + ay2 + az2)
    h2 = abs(bx2 + by2 + bz2)
    d2 = abs(cx2 + cy2 + cz2)

    # prefer even steps
    if (w2 % 2) and (w > 2):
       (ax2, ay2, az2) = (ax2 + dax, ay2 + day, az2 + daz)

    if (h2 % 2) and (h > 2):
       (bx2, by2, bz2) = (bx2 + dbx, by2 + dby, bz2 + dbz)

    if (d2 % 2) and (d > 2):
       (cx2, cy2, cz2) = (cx2 + dcx, cy2 + dcy, cz2 + dcz)

    # wide case, split in w only
    if (2*w > 3*h) and (2*w > 3*d):
        if inbounds(x_dst,y_dst,z_dst,
                    x,y,z,
                    ax2,ay2,az2,
                    bx,by,bz,
                    cx,cy,cz):
            return gilbertxyz2d_r(cur_idx,
                                  x_dst,y_dst,z_dst,
                                  x, y, z,
                                  ax2, ay2, az2,
                                  bx, by, bz,
                                  cx, cy, cz)
        cur_idx += abs( (ax2+ay2+az2)*(bx+by+bz)*(cx+cy+cz) )

        return gilbertxyz2d_r(cur_idx,
                              x_dst,y_dst,z_dst,
                              x+ax2, y+ay2, z+az2,
                              ax-ax2, ay-ay2, az-az2,
                              bx, by, bz,
                              cx, cy, cz)

    # do not split in d
    elif 3*h > 4*d:
        if inbounds(x_dst,y_dst,z_dst,
                    x,y,z,
                    bx2,by2,bz2,
                    cx,cy,cz,
                    ax2,ay2,az2):
            return gilbertxyz2d_r(cur_idx,
                                  x_dst,y_dst,z_dst,
                                  x, y, z,
                                  bx2, by2, bz2,
                                  cx, cy, cz,
                                  ax2, ay2, az2)
        cur_idx += abs( (bx2+by2+bz2)*(cx+cy+cz)*(ax2+ay2+az2) )

        if inbounds(x_dst,y_dst,z_dst,
                    x+bx2,y+by2,z+bz2,
                    ax,ay,az,
                    bx-bx2,by-by2,bz-bz2,
                    cx,cy,cz):
            return gilbertxyz2d_r(cur_idx,
                                  x_dst,y_dst,z_dst,
                                  x+bx2, y+by2, z+bz2,
                                  ax, ay, az,
                                  bx-bx2, by-by2, bz-bz2,
                                  cx, cy, cz)
        cur_idx += abs( (ax+ay+az)*((bx-bx2)+(by-by2)+(bz-bz2))*(cx+cy+cz) )

        return gilbertxyz2d_r(cur_idx,
                              x_dst,y_dst,z_dst,
                              x+(ax-dax)+(bx2-dbx),
                              y+(ay-day)+(by2-dby),
                              z+(az-daz)+(bz2-dbz),
                              -bx2, -by2, -bz2,
                              cx, cy, cz,
                              -(ax-ax2), -(ay-ay2), -(az-az2))

    # do not split in h
    elif 3*d > 4*h:
        if inbounds(x_dst,y_dst,z_dst,
                    x,y,z,
                    cx2,cy2,cz2,
                    ax2,ay2,az2, bx,by,bz):
            return gilbertxyz2d_r(cur_idx,
                                  x_dst,y_dst,z_dst,
                                  x, y, z,
                                  cx2, cy2, cz2,
                                  ax2, ay2, az2,
                                  bx, by, bz)
        cur_idx += abs( (cx2+cy2+cz2)*(ax2+ay2+az2)*(bx+by+bz) )

        if inbounds(x_dst,y_dst,z_dst,
                    x+cx2,y+cy2,z+cz2,
                    ax,ay,az, bx,by,bz,
                    cx-cx2,cy-cy2,cz-cz2):
            return gilbertxyz2d_r(cur_idx,
                                  x_dst,y_dst,z_dst,
                                  x+cx2, y+cy2, z+cz2,
                                  ax, ay, az,
                                  bx, by, bz,
                                  cx-cx2, cy-cy2, cz-cz2)
        cur_idx += abs( (ax+ay+az)*(bx+by+bz)*((cx-cx2)+(cy-cy2)+(cz-cz2)) )

        if inbounds(x_dst,y_dst,z_dst,
                    x+(ax-dax)+(cx2-dcx),y+(ay-day)+(cy2-dcy),z+(az-daz)+(cz2-dcz),
                    -cx2,-cy2,-cz2,
                    -(ax-ax2),-(ay-ay2),-(az-az2),
                    bx,by,bz):
            return gilbertxyz2d_r(cur_idx,
                                  x_dst,y_dst,z_dst,
                                  x+(ax-dax)+(cx2-dcx),
                                  y+(ay-day)+(cy2-dcy),
                                  z+(az-daz)+(cz2-dcz),
                                  -cx2, -cy2, -cz2,
                                  -(ax-ax2), -(ay-ay2), -(az-az2),
                                  bx, by, bz)

    # regular case, split in all w/h/d
    else:
        if inbounds(x_dst,y_dst,z_dst,
                    x,y,z,
                    bx2,by2,bz2,
                    cx2,cy2,cz2,
                    ax2,ay2,az2):
          return gilbertxyz2d_r(cur_idx,x_dst,y_dst,z_dst,
                                x, y, z,
                                bx2, by2, bz2,
                                cx2, cy2, cz2,
                                ax2, ay2, az2)
        cur_idx += abs( (bx2+by2+bz2)*(cx2+cy2+cz2)*(ax2+ay2+az2) )

        if inbounds(x_dst,y_dst,z_dst,
                    x+bx2, y+by2, z+bz2,
                    cx, cy, cz,
                    ax2, ay2, az2,
                    bx-bx2, by-by2, bz-bz2):
            return gilbertxyz2d_r(cur_idx,
                                  x_dst,y_dst,z_dst,
                                  x+bx2, y+by2, z+bz2,
                                  cx, cy, cz,
                                  ax2, ay2, az2,
                                  bx-bx2, by-by2, bz-bz2)
        cur_idx += abs( (cx+cy+cz)*(ax2+ay2+az2)*((bx-bx2)+(by-by2)+(bz-bz2)) )

        if inbounds(x_dst,y_dst,z_dst,
                    x+(bx2-dbx)+(cx-dcx),
                    y+(by2-dby)+(cy-dcy),
                    z+(bz2-dbz)+(cz-dcz),
                    ax, ay, az,
                    -bx2, -by2, -bz2,
                    -(cx-cx2), -(cy-cy2), -(cz-cz2)):
            return gilbertxyz2d_r(cur_idx,
                                  x_dst,y_dst,z_dst,
                                  x+(bx2-dbx)+(cx-dcx),
                                  y+(by2-dby)+(cy-dcy),
                                  z+(bz2-dbz)+(cz-dcz),
                                  ax, ay, az,
                                  -bx2, -by2, -bz2,
                                  -(cx-cx2), -(cy-cy2), -(cz-cz2))
        cur_idx += abs( (ax+ay+az)*(-bx2-by2-bz2)*(-(cx-cx2)-(cy-cy2)-(cz-cz2)) )

        if inbounds(x_dst,y_dst,z_dst,
                    x+(ax-dax)+bx2+(cx-dcx),
                    y+(ay-day)+by2+(cy-dcy),
                    z+(az-daz)+bz2+(cz-dcz),
                    -cx, -cy, -cz,
                    -(ax-ax2), -(ay-ay2), -(az-az2),
                    bx-bx2, by-by2, bz-bz2):
            return gilbertxyz2d_r(cur_idx,
                                  x_dst,y_dst,z_dst,
                                  x+(ax-dax)+bx2+(cx-dcx),
                                  y+(ay-day)+by2+(cy-dcy),
                                  z+(az-daz)+bz2+(cz-dcz),
                                  -cx, -cy, -cz,
                                  -(ax-ax2), -(ay-ay2), -(az-az2),
                                  bx-bx2, by-by2, bz-bz2)
        cur_idx += abs( (-cx-cy-cz)*(-(ax-ax2)-(ay-ay2)-(az-az2))*((bx-bx2)+(by-by2)+(bz-bz2)) )

        return gilbertxyz2d_r(cur_idx,
                              x_dst,y_dst,z_dst,
                              x+(ax-dax)+(bx2-dbx),
                              y+(ay-day)+(by2-dby),
                              z+(az-daz)+(bz2-dbz),
                              -bx2, -by2, -bz2,
                              cx2, cy2, cz2,
                              -(ax-ax2), -(ay-ay2), -(az-az2))



def generate3d(x, y, z,
               ax, ay, az,
               bx, by, bz,
               cx, cy, cz):

    w = abs(ax + ay + az)
    h = abs(bx + by + bz)
    d = abs(cx + cy + cz)

    (dax, day, daz) = (sgn(ax), sgn(ay), sgn(az)) # unit major direction ("right")
    (dbx, dby, dbz) = (sgn(bx), sgn(by), sgn(bz)) # unit ortho direction ("forward")
    (dcx, dcy, dcz) = (sgn(cx), sgn(cy), sgn(cz)) # unit ortho direction ("up")

    # trivial row/column fills
    if h == 1 and d == 1:
        for i in range(0, w):
            yield(x, y, z)
            (x, y, z) = (x + dax, y + day, z + daz)
        return

    if w == 1 and d == 1:
        for i in range(0, h):
            yield(x, y, z)
            (x, y, z) = (x + dbx, y + dby, z + dbz)
        return

    if w == 1 and h == 1:
        for i in range(0, d):
            yield(x, y, z)
            (x, y, z) = (x + dcx, y + dcy, z + dcz)
        return

    (ax2, ay2, az2) = (ax//2, ay//2, az//2)
    (bx2, by2, bz2) = (bx//2, by//2, bz//2)
    (cx2, cy2, cz2) = (cx//2, cy//2, cz//2)

    w2 = abs(ax2 + ay2 + az2)
    h2 = abs(bx2 + by2 + bz2)
    d2 = abs(cx2 + cy2 + cz2)

    # prefer even steps
    if (w2 % 2) and (w > 2):
       (ax2, ay2, az2) = (ax2 + dax, ay2 + day, az2 + daz)

    if (h2 % 2) and (h > 2):
       (bx2, by2, bz2) = (bx2 + dbx, by2 + dby, bz2 + dbz)

    if (d2 % 2) and (d > 2):
       (cx2, cy2, cz2) = (cx2 + dcx, cy2 + dcy, cz2 + dcz)

    # wide case, split in w only
    if (2*w > 3*h) and (2*w > 3*d):
       yield from generate3d(x, y, z,
                             ax2, ay2, az2,
                             bx, by, bz,
                             cx, cy, cz)

       yield from generate3d(x+ax2, y+ay2, z+az2,
                             ax-ax2, ay-ay2, az-az2,
                             bx, by, bz,
                             cx, cy, cz)

    # do not split in d
    elif 3*h > 4*d:
       yield from generate3d(x, y, z,
                             bx2, by2, bz2,
                             cx, cy, cz,
                             ax2, ay2, az2)

       yield from generate3d(x+bx2, y+by2, z+bz2,
                             ax, ay, az,
                             bx-bx2, by-by2, bz-bz2,
                             cx, cy, cz)

       yield from generate3d(x+(ax-dax)+(bx2-dbx),
                             y+(ay-day)+(by2-dby),
                             z+(az-daz)+(bz2-dbz),
                             -bx2, -by2, -bz2,
                             cx, cy, cz,
                             -(ax-ax2), -(ay-ay2), -(az-az2))

    # do not split in h
    elif 3*d > 4*h:
       yield from generate3d(x, y, z,
                             cx2, cy2, cz2,
                             ax2, ay2, az2,
                             bx, by, bz)

       yield from generate3d(x+cx2, y+cy2, z+cz2,
                             ax, ay, az,
                             bx, by, bz,
                             cx-cx2, cy-cy2, cz-cz2)

       yield from generate3d(x+(ax-dax)+(cx2-dcx),
                             y+(ay-day)+(cy2-dcy),
                             z+(az-daz)+(cz2-dcz),
                             -cx2, -cy2, -cz2,
                             -(ax-ax2), -(ay-ay2), -(az-az2),
                             bx, by, bz)

    # regular case, split in all w/h/d
    else:
       yield from generate3d(x, y, z,
                             bx2, by2, bz2,
                             cx2, cy2, cz2,
                             ax2, ay2, az2)

       yield from generate3d(x+bx2, y+by2, z+bz2,
                             cx, cy, cz,
                             ax2, ay2, az2,
                             bx-bx2, by-by2, bz-bz2)

       yield from generate3d(x+(bx2-dbx)+(cx-dcx),
                             y+(by2-dby)+(cy-dcy),
                             z+(bz2-dbz)+(cz-dcz),
                             ax, ay, az,
                             -bx2, -by2, -bz2,
                             -(cx-cx2), -(cy-cy2), -(cz-cz2))

       yield from generate3d(x+(ax-dax)+bx2+(cx-dcx),
                             y+(ay-day)+by2+(cy-dcy),
                             z+(az-daz)+bz2+(cz-dcz),
                             -cx, -cy, -cz,
                             -(ax-ax2), -(ay-ay2), -(az-az2),
                             bx-bx2, by-by2, bz-bz2)

       yield from generate3d(x+(ax-dax)+(bx2-dbx),
                             y+(ay-day)+(by2-dby),
                             z+(az-daz)+(bz2-dbz),
                             -bx2, -by2, -bz2,
                             cx2, cy2, cz2,
                             -(ax-ax2), -(ay-ay2), -(az-az2))


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('width', type=int)
    parser.add_argument('height', type=int)
    parser.add_argument('depth', type=int)
    parser.add_argument('--op', type=str, required=False)
    args = parser.parse_args()

    w = args.width
    h = args.height
    d = args.depth

    n = w*h*d

    if args.op == "d2xyz":

        for idx in range(n):
            (x,y,z) = gilbertd2xyz(idx,w,h,d)
            print(x,y,z)
        sys.exit(0)

    elif args.op == "xyz2d":

        for x in range(w):
            for y in range(h):
                for z in range(d):
                    idx = gilbertxyz2d(x,y,z,w,h,d)
                    print(idx,x,y,z)
        sys.exit(0)



    for x, y, z in gilbert3d(args.width, args.height, args.depth):
        print(x, y, z)
