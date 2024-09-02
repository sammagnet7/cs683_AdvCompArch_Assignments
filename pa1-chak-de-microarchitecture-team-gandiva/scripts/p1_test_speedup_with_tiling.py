import subprocess
import re
import numpy as np
import matplotlib.pyplot as plt
import math

################### customize #######################
FONT_SIZE = 18
AVG_ITERATIONS = 5

BUILD_DIR='../part1/build'
EXEC_OPTIMIZED='tiling'
EXECUTABLE=f'{BUILD_DIR}/{EXEC_OPTIMIZED}'

MATRIX_SIZE = [5000,10000,15000,20000,250000,30000]
TILE_SIZE = [4,8,16,32,48,56,64,128]

################### customize #######################

# Function to extract speedup from the output
def extract_speedup(output):
    match = re.search(r"The speedup obtained by .* is ([\d.]+)", output)
    if match:
        return float(match.group(1))
    return None

# Function to run the executable and calculate average speedup
def run_optimized_executable(matrix_size, block_size, iterations=AVG_ITERATIONS):
    speedup_sum = 0.0
    for _ in range(iterations):
        result = subprocess.run([EXECUTABLE, str(matrix_size), str(block_size)], capture_output=True, text=True)
        speedup = extract_speedup(result.stdout)
        if speedup is not None:
            speedup_sum += speedup
    return speedup_sum / iterations

# Function to plot the results
def plot_results(matrix_size, speedups_over_matrix, tile_size):

    n_bars = len(tile_size)
    bar_width = 0.11

    bar_positions = [np.arange(len(matrix_size)) + i * bar_width for i in range(n_bars)]

    plt.figure(figsize=(14, 6))

    # Plotting the bars
    for i in range(n_bars):
        label = f'Block Size {tile_size[i]}'
        plt.bar(bar_positions[i], [speedup[i] for speedup in speedups_over_matrix], width=bar_width, label=label)

    # Adding the x-axis labels
    plt.xticks(np.arange(len(matrix_size)) + (n_bars - 1) * bar_width / 2, matrix_size, fontsize=FONT_SIZE)

    plt.yticks(fontsize=FONT_SIZE)

    plt.ylabel('Speedup', fontsize=FONT_SIZE)

    plt.xlabel('Matrix Size', fontsize=FONT_SIZE)

    plt.title(f'Speedup vs Matrix Size for optimization ({EXEC_OPTIMIZED})', fontsize=FONT_SIZE)

    # Adjusting y-axis limit to make space for the labels
    plt.ylim(0, max(max(speedups_over_matrix)) * 1.2)

    # Adding legends outside the plot
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), fancybox=True, shadow=True, ncol=4, fontsize=FONT_SIZE)

    # Adding values on top of bars
    for i in range(n_bars):
        for j in range(len(matrix_size)):
            plt.text(bar_positions[i][j], speedups_over_matrix[j][i] + max(max(speedups_over_matrix)) * 0.03, 
                 str(speedups_over_matrix[j][i]), ha='center', va='bottom', rotation='vertical', fontsize=FONT_SIZE)

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2) 

    # Display the plot
    plt.show()

def main():

    speedups_over_matrix = []

    for m in MATRIX_SIZE:
        speedup_over_block=[]
        for b in TILE_SIZE:
            if b==0:
                continue
            speedup_over_block.append( round(run_optimized_executable(m, b),2) )

        print(f"speedup calculated for matrix size:{m}")
        speedups_over_matrix.append(speedup_over_block)
    
    # Plot the results
    plot_results(MATRIX_SIZE, speedups_over_matrix, TILE_SIZE)

if __name__ == "__main__":
    main()
