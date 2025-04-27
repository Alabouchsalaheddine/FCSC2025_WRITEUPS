import math
import sys

# (Optional) Point class for clarity
class point:
    def __init__(self, P):
        self.coordinates = [int(round(c)) for c in P]
    def __str__(self):
        return f"[{', '.join(str(x) for x in self.coordinates)}]"

def minimumDistanceOnCube(length, P_obj, Q_obj):
    """
    Calculates the square of the minimum surface distance between points P and Q
    on a cube of side length 'length'.

    This method effectively calculates the straight-line distance in the three
    primary ways the cube can be unfolded or "flattened" along an axis.

    Args:
        length: The side length of the cube (L).
        P_obj: A point object for the first point (x1, y1, z1).
        Q_obj: A point object for the second point (x2, y2, z2).

    Returns:
        The square of the shortest distance (integer).
    """
    L = int(length)
    x1, y1, z1 = P_obj.coordinates
    x2, y2, z2 = Q_obj.coordinates

    # Squared direct differences
    dx_sq = (x1 - x2)**2
    dy_sq = (y1 - y2)**2
    dz_sq = (z1 - z2)**2

    # Calculate squared effective distances when flattened/unfolded along each axis
    # This finds the shortest path along that dimension in the 2D net.
    x_wrap_sq = min(x1 + x2, 2 * L - x1 - x2)**2
    y_wrap_sq = min(y1 + y2, 2 * L - y1 - y2)**2
    z_wrap_sq = min(z1 + z2, 2 * L - z1 - z2)**2

    # Candidate distances squared in the three primary unfoldings:
    # 1. Flattened along X (wrap X, direct Y, Z):
    dist_sq_cand1 = dy_sq + dz_sq + x_wrap_sq
    # 2. Flattened along Y (wrap Y, direct X, Z):
    dist_sq_cand2 = dx_sq + dz_sq + y_wrap_sq
    # 3. Flattened along Z (wrap Z, direct X, Y):
    dist_sq_cand3 = dx_sq + dy_sq + z_wrap_sq

    # The minimum surface distance squared is the minimum of these candidates.
    min_dist_sq = min(dist_sq_cand1, dist_sq_cand2, dist_sq_cand3)

    # Return the integer result
    return int(round(min_dist_sq))

# --- Main execution block for interacting with the server ---
if __name__=="__main__":
    L = 32 # Challenge uses L=32
    try:
        for _ in range(1000): # Server runs 1000 iterations
            # Read Alice
            alice_line = sys.stdin.readline().strip()
            if not alice_line: break
            try:
                alice_coords_str = alice_line.split('=')[1].strip().replace('[','').replace(']','')
                alice_coords = [int(c) for c in alice_coords_str.split(',')]
                Alice = point(alice_coords)
            except Exception as e:
                # print(f"Error parsing Alice: {alice_line} | Error: {e}", file=sys.stderr)
                exit(1)

            # Read Bob
            bob_line = sys.stdin.readline().strip()
            if not bob_line: break
            try:
                bob_coords_str = bob_line.split('=')[1].strip().replace('[','').replace(']','')
                bob_coords = [int(c) for c in bob_coords_str.split(',')]
                Bob = point(bob_coords)
            except Exception as e:
                # print(f"Error parsing Bob: {bob_line} | Error: {e}", file=sys.stderr)
                exit(1)



            # Calculate distance using the unfolding principle (via wrap-around formulas)
            distance_sq = minimumDistanceOnCube(L, Alice, Bob)

            # Send result
            print(distance_sq)
            sys.stdout.flush()

    except EOFError:
        pass # Server closed connection
    except Exception as e:
        # print(f"Runtime error: {e}", file=sys.stderr)
        pass