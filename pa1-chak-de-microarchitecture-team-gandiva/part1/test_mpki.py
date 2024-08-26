import subprocess
import re
import numpy as np
import matplotlib.pyplot as plt
import math

# Function to extract MPKI from the output
def extract_mpki(output):
    match = re.search(r"MPKI: ([\d.]+)", output)
    if match:
        return float(match.group(1))
    return None

# Function to run the perf stat command and calculate average MPKI
def run_perf_stat(executable, matrix_size, block_size, iterations=10):
    mpki_sum = 0.0
    for _ in range(iterations):
        bash_command = f"""
        perf stat -x, -e instructions,L1-dcache-load-misses ./build/{executable} {matrix_size} {block_size} 2>&1 | 
        gawk --bignum '/instructions/ {{instructions=$1}}
        /L1-dcache-load-misses/ {{misses=$1}}
        END {{
            mpki = ((misses * 1000) / instructions); 
            printf "\\nMPKI: %.2f\\n", mpki;
        }}'
        """
        result = subprocess.run(bash_command, shell=True, capture_output=True, text=True)
        mpki = extract_mpki(result.stdout)
        if mpki is not None:
            mpki_sum += mpki
    return mpki_sum / iterations

# Function to plot the results
def plot_results(matrix_sizes, naive_mpki, optimized_mpki, block_size):
    plt.plot(matrix_sizes, naive_mpki, marker='o', label='Naive', color='red')
    plt.plot(matrix_sizes, optimized_mpki, marker='o', label='optimized', color='green')

    plt.xlabel('Matrix Size')
    plt.ylabel('Average MPKI')
    plt.title(f'Average MPKI vs Matrix Size (Block Size = {block_size})')
    plt.grid(True)
    # Move the legend outside of the plot
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.show()

def main():
    # Get user input for max_matrix_size and fixed block_size
    max_matrix_size = int(input("Enter the max matrix size: "))
    block_size = int(input("Enter the block size (fixed): "))

    matrix_sizes = []
    naive_mpki = []
    optimized_mpki = []

    # Loop over matrix sizes
    m = 2
    while m <= max_matrix_size:
        matrix_sizes.append(m)

        # Run the command and calculate average MPKI for naive and optimized
        avg_mpki_naive = run_perf_stat('naive', m, block_size)
        avg_mpki_optimized = run_perf_stat('prefetch', m, block_size)

        naive_mpki.append(avg_mpki_naive)
        optimized_mpki.append(avg_mpki_optimized)

        m = math.floor(2.5 * m)

    # Plot the results
    plot_results(matrix_sizes, naive_mpki, optimized_mpki, block_size)

if __name__ == "__main__":
    main()