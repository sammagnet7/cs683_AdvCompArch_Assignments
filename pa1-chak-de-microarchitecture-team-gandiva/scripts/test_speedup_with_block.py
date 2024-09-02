import subprocess
import re
import numpy as np
import matplotlib.pyplot as plt
import math

BUILD_DIR='../part1/build'
EXEC_OPTIMIZED='tiling-prefetch'
EXECUTABLE=f'{BUILD_DIR}/{EXEC_OPTIMIZED}'

# Function to extract speedup from the output
def extract_speedup(output):
    match = re.search(r"The speedup obtained by .* is ([\d.]+)", output)
    if match:
        return float(match.group(1))
    return None

# Function to run the executable and calculate average speedup
def run_optimized_executable(matrix_size, block_size, iterations=10):
    speedup_sum = 0.0
    for _ in range(iterations):
        #'taskset','-c','1',
        result = subprocess.run([EXECUTABLE, str(matrix_size), str(block_size)], capture_output=True, text=True)
        speedup = extract_speedup(result.stdout)
        if speedup is not None:
            speedup_sum += speedup
    return speedup_sum / iterations

# Function to plot the results
def plot_results(matrix_sizes, block_sizes, avg_speedups):
    NUM_COLORS = len(matrix_sizes)
    cm = plt.get_cmap('gist_rainbow')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_prop_cycle(color=[cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])

    for idx, m in enumerate(matrix_sizes):
        ax.plot( block_sizes[idx], avg_speedups[idx], marker='o', label=f'Matrix Size {m}')
            
    plt.xlabel('Block Size')
    plt.ylabel('Average Speedup')
    plt.title('Speedup vs Block Size for Different Matrix Sizes')
    plt.grid(True)
    # Move the legend outside of the plot
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.show()

def main():
    # Get user input for max_matrix_size and max_block_size
    max_matrix_size = int(input("Enter the max matrix size: "))
    max_block_size = int(input("Enter the max block size: "))

    matrix_sizes = []
    block_sizes_list = []
    avg_speedups = []

    # Outer loop over matrix sizes
    m = 8  # Starts from 8*8 matrix
    while m <= max_matrix_size:
        matrix_sizes.append(m)
        block_sizes = []
        speedups = []

        # Middle loop over block sizes
        b = 2 
        while b <= min(m, max_block_size):
            block_sizes.append(b)

            # Inner loop to run the executable multiple times
            avg_speedup = run_optimized_executable(m, b)
            speedups.append(avg_speedup)

            b *= 2

        block_sizes_list.append(block_sizes)
        avg_speedups.append(speedups)

        m = math.floor(1.75 * m)

    # Plot the results
    plot_results(matrix_sizes, block_sizes_list, avg_speedups)

if __name__ == "__main__":
    main()
