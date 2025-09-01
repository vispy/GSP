# Experiment to handle intellisense in VSCode
import matplotlib.figure
import numpy as np

import matplotlib
import matplotlib.pyplot as plt

import time

"""
Library to display point clouds using GSP.
"""

def display_benchmark_pure_matplotlib(figure=matplotlib.figure.Figure, log_enabled=False, max_bench_delay_seconds=10.0) -> float:
    """
    Benchmark the performance of pure Matplotlib rendering.

    Args:
        figure (matplotlib.figure.Figure): The Matplotlib figure to use for rendering.
        log_enabled (bool): Whether to log the benchmark results. default is False.
        max_bench_delay_seconds (float): Maximum time to wait for the benchmark in seconds. default is 10.

    Returns:
        float: The average time taken for one rendering in seconds.
    """
    plt.show(block=False)
    if log_enabled:
        print(f"Starting Matplotlib rendering benchmark for a maximum {max_bench_delay_seconds} seconds...")
    bench_count = 0

    max_bench_count = 1000

    start_time = time.perf_counter()
    for _ in range(max_bench_count):
        # count the number of renderings
        bench_count += 1
        if log_enabled:
            # print a dot without a newline
            print(".", end="", flush=True)

        # Render the figure
        figure.canvas.draw()
        figure.canvas.flush_events()

        # break of the loop after max_bench_delay_seconds
        if time.perf_counter() - start_time > max_bench_delay_seconds:
            if log_enabled:
                print("")
            break

    # measure the elapsed time for {bench_count} renderings
    elapsed_time = time.perf_counter() - start_time

    # print the elapsed time and the FPS
    if log_enabled:
        print(f"Matplotlib rendering benchmark: {bench_count} renderings took {elapsed_time:.2f}s; {bench_count / (elapsed_time):.2f} FPS")

    # calculate the average rendering time
    rendering_time = elapsed_time / bench_count
    return rendering_time

