import random
import time
import os

def closestSquaredDistance(x, y):
    """
    The O(n log n) implementation of 2-D closest pair

    input:   two lists of x- and corresponding y-coordinates
             corrects for (ignores) duplicates points
    returns: a tuple of L2-distance and the closest pair:
             (dist, [point1, point2])
    """

    def l2dist(p1, p2):
        return pow(pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2), 0.5)

    def closestSplitPair(Px, Py, delta):
        # screen only x-coordinates within delta distance from mean(x)
        # using Px (sorted by x-coordinates)
        x_mean = Px[len(Px) // 2][0]

        # only relevent points (within delta from x_mean), sorted by y-coordinate
        # O(n)
        Sy = [(x, y) for x, y in Py if abs(x - x_mean) <= delta]
        if len(Sy) < 2:
            return None, None

        # find the closest pair within 8 points
        min_dist = pow(pow(Sy[0][1] - Sy[-1][1], 2) + pow((2 * delta), 2), .5)

        pair = (None, None)
        for i in range(len(Sy)):
            j = i + 1
            while j < min(i + 9, len(Sy)):
                dist = l2dist(Sy[i], Sy[j])
                if dist < min_dist:
                    min_dist = dist
                    pair = (Sy[i], Sy[j])
                j += 1

        return pair

    def closestPair(Px, Py):

        if len(Px) == 2: return Px[0], Px[1]
        if len(Px) == 3:
            dist1 = l2dist(Px[0], Px[1])
            dist2 = l2dist(Px[1], Px[2])
            dist3 = l2dist(Px[0], Px[2])
            return sorted(list(zip([dist1, dist2, dist3],
                                   [(Px[0], Px[1]), (Px[1], Px[2]),
                                    (Px[0], Px[2])])))[0][1]

        # split (sorted) data into left and right of x-coordinates
        # this is O(n), due to Py provided (sorted by y)-- Qy,Ry also sorted
        ns = len(Px) // 2

        Qx, Rx = Px[:ns], Px[ns:]
        Qy, Ry = [], []

        x_median = Px[ns][0]
        for (x, y) in Py:
            if x <= x_median:
                Qy.append((x, y))
            else:
                Ry.append((x, y))

        # recursively find the closest pair on each side
        (p1, q1) = closestPair(Qx, Qy)
        (p2, q2) = closestPair(Rx, Ry)

        d1, d2 = l2dist(p1, q1), l2dist(p2, q2)
        delta = min(d1, d2)

        # look for closest pair in between the two sides
        (p3, q3) = closestSplitPair(Px, Py, delta)

        if not p3 or not q3:
            d3 = float("inf")
        else:
            d3 = l2dist(p3, q3)

        min_pairs = list(zip([d1, d2, d3], [(p1, q1), (p2, q2), (p3, q3)]))

        return sorted(min_pairs)[0][1]

    # make sure no duplicates
    points = list(set(zip(x, y)))

    # sort by x- and y- coordinates
    # O(n log n)
    Px = sorted(points)
    Py = sorted(points, key=lambda x: x[1])

    (p1, p2) = closestPair(Px, Py)

    return l2dist(p1, p2), [p1, p2]

if __name__ == '__main__':
    N = 1000
    M = 50

    for k in range(M):
        os.system('cls')
        print(f'running with set size of {N}, over {M} iterations...')
        print(f'iteration {k+1}')

        # generate random points
        x = [random.randint(-1000, 1000) for _ in range(N)]
        y = [random.randint(-1000, 1000) for _ in range(N)]

        # initialize timers
        base_time = 0
        algo_time = 0

        # find the closest pair
        start = time.time()
        min_dist = float('inf')
        for i in range(len(x)):
            for j in range(i+1, len(x)):
                # points need to be distinct
                if (x[i], y[i]) == (x[j], y[j]):
                    continue
                min_dist = min(min_dist,
                               pow(pow(x[i] - x[j], 2) + pow(y[i] - y[j], 2), .5))
        base_time += time.time() - start

        # test algorithm O(n log n)
        start = time.time()
        dist, pair = closestSquaredDistance(x, y)
        algo_time += time.time() - start
        # print(time.time() - start)

        if dist != min_dist:
            print('!!mismatch!!')
            print(f'x={x}')
            print(f'y={y}')
            break
    # contrast running time
    os.system('cls')
    print(f'running with set size of {N}, over {M} iterations... Done!')
    print(f'naive approach: average of {1000*base_time / (k+1)}msec per iteration')
    print(f'algorithm:      average of {1000*algo_time / (k+1)}msec per iteration')