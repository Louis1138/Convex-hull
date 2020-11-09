from time import time
from random import seed

import tqdm as tqdm

from exhaustive import exhaustive
from graham import graham
from jarvis import jarvis
from shamos import shamos
from eddy_floyd import eddy_floyd
from utils import *

import matplotlib.pyplot as plt


def benchmark(sizes=(10, 100, 1000, 10000), runs=100, method=exhaustive):
    """
    For each size in the 'sizes' list, compute the average time over a given number of runs to find the convex hull
    for a dataset of that size,
    the range used for max and min for the create_points function is always 10 times the highest value in the 'sizes'
    list.

    :param sizes: list of problem sizes to consider (default is (10, 100, 1000, 10000, 100000))
    :param method: the name of the algorithm to use (default is exhaustive)
    :param runs: the number of repetition to perform for computing average (default is 100)
    :return: nothing
    """
    # print(method.__name__)
    seed(0)
    results = []
    with tqdm.tqdm(total=len(sizes) * runs, desc="Progress (" + method.__name__[:6] + ")") as bar:
        for s in sizes:
            tot = 0.0
            for _ in range(runs):
                points = create_points(s, 0, max(sizes) * 10)
                t0 = time.time()
                method(points,  show=False, save=False, detailed=False)
                tot += (time.time() - t0)
                bar.update(1)
            # print("size %d time: %0.5f" % (s, tot / float(runs)))
            results.append(tot / float(runs))
    return {'sizes': sizes, 'avg time': results}


def main():
    """
    A sample main program.

    :return: nothing
    """
    algorithms = [exhaustive, graham, jarvis, shamos, eddy_floyd]

    results = {}

    for algorithm in algorithms:
        if algorithm is exhaustive:
            sizes = range(2, 9, 2)
            runs = 10
        else:
            sizes = (*range(10, 11, 1), *range(1000, 10001, 1000))
#            runs = 100
            runs = 7
        results[algorithm] = benchmark(sizes=sizes, runs=runs, method=algorithm)
        plt.plot(results[algorithm]['sizes'], results[algorithm]['avg time'], label=str(algorithm.__name__))

    plt.legend()
    plt.title("Convex hull algorithms execution time (s)")
    plt.xlabel("Number of points")
    plt.ylabel("Time (s)")
    plt.savefig("convex_hull.png")
    plt.close()


if __name__ == "__main__":
    main()
