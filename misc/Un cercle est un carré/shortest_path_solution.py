#!/usr/bin/env python3
# Install with:
#    pip install pwntools --break-system-packages

from pwn import *
import math
import numpy as np
from collections import deque, defaultdict

# ─── Your cube‐surface code ───────────────────────────────────────────────────

def build_face_data(L):
    face_normals = {
        0: np.array([ 1,  0,  0]),
        1: np.array([-1,  0,  0]),
        2: np.array([ 0,  1,  0]),
        3: np.array([ 0, -1,  0]),
        4: np.array([ 0,  0,  1]),
        5: np.array([ 0,  0, -1]),
    }
    face_axes = {
        0: (np.array([0,1,0]), np.array([0,0,1])),
        1: (np.array([0,1,0]), np.array([0,0,1])),
        2: (np.array([1,0,0]), np.array([0,0,1])),
        3: (np.array([1,0,0]), np.array([0,0,1])),
        4: (np.array([1,0,0]), np.array([0,1,0])),
        5: (np.array([1,0,0]), np.array([0,1,0])),
    }
    face_const = {
        0: (0, +L), 1: (0, 0),
        2: (1, +L), 3: (1, 0),
        4: (2, +L), 5: (2, 0),
    }
    return face_normals, face_axes, face_const

def build_adjacency(face_normals, face_const):
    def rotation_matrix(axis, theta):
        axis = axis / np.linalg.norm(axis)
        a = math.cos(theta/2)
        b,c,d = -axis * math.sin(theta/2)
        return np.array([
            [a*a + b*b - c*c - d*d,   2*(b*c - a*d),       2*(b*d + a*c)],
            [2*(b*c + a*d),           a*a + c*c - b*b - d*d, 2*(c*d - a*b)],
            [2*(b*d - a*c),           2*(c*d + a*b),       a*a + d*d - b*b - c*c]
        ])
    adj = {}
    for A,(iA,cA) in face_const.items():
        nA = face_normals[A]
        for B,(iB,cB) in face_const.items():
            if A==B or iA==iB: continue
            # shared edge axis
            e_axis = ({0,1,2} - {iA, iB}).pop()
            p0 = np.zeros(3); p0[iA]=cA; p0[iB]=cB
            dir_e = np.zeros(3); dir_e[e_axis]=1
            nB = face_normals[B]
            found=False
            for axis_dir in (dir_e, -dir_e):
                for sign in (+1,-1):
                    M=rotation_matrix(axis_dir, sign*math.pi/2)
                    if np.allclose(M.dot(nB), nA, atol=1e-6):
                        adj[(A,B)]=(p0,axis_dir,M)
                        found=True; break
                if found: break
            if not found:
                raise RuntimeError(f"Can't orient {B}→{A}")
    return adj

def shortest_on_surfaces(L, p1, p2):
    fn, fa, fc = build_face_data(L)
    adj = build_adjacency(fn, fc)
    nbrs = defaultdict(list)
    for (A,B) in adj: nbrs[A].append(B)

    def faces_of_point(p):
        out=[]
        for f,(i,c) in fc.items():
            if abs(p[i]-c)<1e-8: out.append(f)
        return out

    def find_paths(fa_, fb_):
        res=[]
        def dfs(path):
            if len(path)>4: return
            if path[-1]==fb_:
                res.append(path.copy()); return
            for nb in nbrs[path[-1]]:
                if nb not in path:
                    path.append(nb); dfs(path); path.pop()
        dfs([fa_]); return res

    P1=np.array(p1,float); P2=np.array(p2,float)
    best=float('inf')
    for f1 in faces_of_point(P1):
        uA,vA=fa[f1]
        p1loc=(P1.dot(uA),P1.dot(vA))
        for f2 in faces_of_point(P2):
            for path in find_paths(f1,f2):
                P=P2.copy()
                for i in range(len(path)-1,0,-1):
                    A,B=path[i-1],path[i]
                    p0,axis_dir,M=adj[(A,B)]
                    P=p0 + M.dot(P-p0)
                p2loc=(P.dot(uA),P.dot(vA))
                dx,dy=p1loc[0]-p2loc[0],p1loc[1]-p2loc[1]
                best=min(best,dx*dx+dy*dy)
    return best

def minimumDistanceOnCube(L, p1, p2):
    return int(round(shortest_on_surfaces(L, p1, p2)))

# ─── End of cube code ───────────────────────────────────────────────────────

# Default connection parameters (override via HOST=... PORT=... DEBUG)
HOST = args.HOST or "chall.fcsc.fr"
PORT = int(args.PORT or 2054)

if args.DEBUG:
    context.log_level = 'debug'

# Connect
io = remote(HOST, PORT)

# Loop until server closes
try:
    while True:
        # read Alice line
        line = io.recvline(timeout=5)
        if not line:
            break
        line = line.decode().strip()
        if not line.startswith("Alice"):
            # maybe some banner or intermediary text: print and continue
            print(line)
            continue

        # parse coords
        def parse_coords(s):
            # expect "Alice = [x, y, z]" or "Bob   = [...]"
            arr = s.split('=',1)[1].strip()
            arr = arr.strip('[]')
            return [float(c) for c in arr.split(',')]

        A = parse_coords(line)
        # read Bob
        line2 = io.recvline().decode().strip()
        print(line)      # echo server lines
        print(line2)
        B = parse_coords(line2)

        # compute and send
        d2 = minimumDistanceOnCube(int(32), A, B)
        io.sendlineafter(b"Distance: ", str(d2).encode())

        # print server response(s)
        # assume server sends back at least one line per reply
        #resp = io.recvline(timeout=5)
        #if not resp:
        #    break
        #print(resp.decode().strip())

except EOFError:
    pass
finally:
    io.close()
