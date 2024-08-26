import subprocess
import re
import numpy as np
import matplotlib.pyplot as plt
import math

executable='./build/prefetch'

# Function to extract speedup from the output
def extract_speedup(output):
    match = re.search(r"The speedup obtained by .* is ([\d.]+)", output)
    if match:
        return float(match.group(1))
    return None

# Function to run the executable and calculate average speedup
def run_tiling_executable(matrix_size, iterations=10):
    speedup_sum = 0.0
    for _ in range(iterations):
        #'taskset','-c','1',
        result = subprocess.run([executable, str(matrix_size), "0"], capture_output=True, text=True)
        speedup = extract_speedup(result.stdout)
        if speedup is not None:
            speedup_sum += speedup
    return speedup_sum / iterations

# Function to plot the results
def plot_results(matrix_sizes, avg_speedups):

    plt.plot( matrix_sizes, avg_speedups, marker='o', color='green')
            
    plt.xlabel('Matrix Size')
    plt.ylabel('Average Speedup')
    plt.title('Speedup vs Matrix Size')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    # Get user input for max_matrix_size and max_block_size
    max_matrix_size = int(input("Enter the max matrix size: "))

    matrix_sizes = []
    avg_speedups = []

    # Outer loop over matrix sizes
    m = 100  # Starts from 8*8 matrix
    while m <= max_matrix_size:
        matrix_sizes.append(m)
        # Inner loop to run the executable multiple times
        avg_speedup = run_tiling_executable(m)
        avg_speedups.append(avg_speedup)

        m = math.floor(2.5 * m)

    # Plot the results
    plot_results(matrix_sizes, avg_speedups)

if __name__ == "__main__":
    main()
