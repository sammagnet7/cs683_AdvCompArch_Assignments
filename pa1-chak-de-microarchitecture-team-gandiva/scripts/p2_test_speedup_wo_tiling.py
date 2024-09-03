import subprocess
import re
import numpy as np
import matplotlib.pyplot as plt
import math

################### customize #######################
FONT_SIZE = 18
AVG_ITERATIONS = 5

BUILD_DIR='../part2/build'
EXEC_OPTIMIZED='prefetch'   # prefetch simd simd-prefetch
EXECUTABLE=f'{BUILD_DIR}/{EXEC_OPTIMIZED}'

MATRIX_SIZE = [1000, 3000, 5000, 10000, 15000]

################### customize #######################

# Function to extract speedup from the output
def extract_speedup(output):
    match = re.search(r"Speedup: ([\d.]+)", output)
    if match:
        return float(match.group(1))
    return None

# Function to run the executable and calculate average speedup
def run_optimized_executable(matrix_size, KERNEL_SIZE, iterations=AVG_ITERATIONS):
    speedup_sum = 0.0
    for _ in range(iterations):
        result = subprocess.run([EXECUTABLE, str(matrix_size), str(KERNEL_SIZE), "0"], capture_output=True, text=True)
        speedup = extract_speedup(result.stdout)
        if speedup is not None:
            speedup_sum += speedup
    avg_speedup = speedup_sum / iterations
    return avg_speedup

# Function to plot the results
def plot_results(matrix_size, speedups_over_matrix, KERNEL_SIZE):

    bar_width = 30

    plt.figure(figsize=(14, 6))

    bars = plt.bar(matrix_size, speedups_over_matrix, color='skyblue', edgecolor='black', width=bar_width, label=f'{EXEC_OPTIMIZED}')

    # Adding the x-axis labels
    plt.xticks(matrix_size, fontsize=FONT_SIZE)

    plt.yticks(fontsize=FONT_SIZE)

    plt.ylabel('Speedup', fontsize=FONT_SIZE)

    plt.xlabel('Matrix Size', fontsize=FONT_SIZE)

    plt.title(f'Speedup vs Matrix Size for optimization ({EXEC_OPTIMIZED} with KERNEL_SIZE={KERNEL_SIZE})', fontsize=FONT_SIZE)

    # Adjusting y-axis limit to make space for the labels
    plt.ylim(0, max(speedups_over_matrix) * 1.3)

    # Adding legends outside the plot
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), fancybox=True, shadow=True, ncol=4, fontsize=FONT_SIZE)

    # Add text labels on the bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval+0.03, round(yval, 2), 
                 ha='center', va='bottom', rotation='vertical', fontsize=FONT_SIZE)

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2) 

    # Display the plot
    plt.savefig("simd_speedup_15K.png")

def main():
    
    KERNEL_SIZE = int(input("Input Kernel size in multiple of 8: "))

    speedups_over_matrix = []

    for m in MATRIX_SIZE:
        speedups_over_matrix.append( round(run_optimized_executable(m,KERNEL_SIZE),2) )

        print(f"speedup calculated for matrix size:{m}")
    
    # Plot the results
    plot_results(MATRIX_SIZE, speedups_over_matrix, KERNEL_SIZE)

if __name__ == "__main__":
    main()
