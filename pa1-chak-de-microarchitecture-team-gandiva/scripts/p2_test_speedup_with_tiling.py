import subprocess
import re
import numpy as np
import matplotlib.pyplot as plt
import math

################### customize #######################
FONT_SIZE = 18
AVG_ITERATIONS = 5

BUILD_DIR='../part2/build'
EXEC_OPTIMIZED='tiling' # tiling, tiling-prefetch, tiling-simd, tiling-simd-prefetch
EXECUTABLE=f'{BUILD_DIR}/{EXEC_OPTIMIZED}'

MATRIX_SIZE = [100, 300, 700, 1100]
TILE_SIZE = [4,8,16,32,64]

################### customize #######################

# Function to extract speedup from the output
def extract_speedup(output):
    match = re.search(r"Speedup: ([\d.]+)", output)
    if match:
        return float(match.group(1))
    return None

# Function to run the executable and calculate average speedup
def run_optimized_executable(matrix_size, tile_size, KERNEL_SIZE, iterations=AVG_ITERATIONS):
    speedup_sum = 0.0
    for _ in range(iterations):
        result = subprocess.run([EXECUTABLE, str(matrix_size), str(KERNEL_SIZE) ,str(tile_size)], capture_output=True, text=True)
        speedup = extract_speedup(result.stdout)

        if speedup is not None:
            speedup_sum += speedup
    
    avg_speedup = speedup_sum / iterations
    return avg_speedup

# Function to plot the results
def plot_results(matrix_size, speedups_over_matrix, tile_size, KERNEL_SIZE):

    n_bars = len(tile_size)
    bar_width = 0.11

    bar_positions = [np.arange(len(matrix_size)) + i * bar_width for i in range(n_bars)]

    plt.figure(figsize=(14, 6))

    # Plotting the bars
    for i in range(n_bars):
        label = f'Tile Size {tile_size[i]}'
        plt.bar(bar_positions[i], [speedup[i] for speedup in speedups_over_matrix], width=bar_width, label=label)

    # Adding the x-axis labels
    plt.xticks(np.arange(len(matrix_size)) + (n_bars - 1) * bar_width / 2, matrix_size, fontsize=FONT_SIZE)

    plt.yticks(fontsize=FONT_SIZE)

    plt.ylabel('Speedup', fontsize=FONT_SIZE)

    plt.xlabel('Matrix Size', fontsize=FONT_SIZE)

    plt.title(f'Speedup vs Matrix Size for optimization ({EXEC_OPTIMIZED} with KERNEL_SIZE={KERNEL_SIZE})', fontsize=FONT_SIZE)

    # Adjusting y-axis limit to make space for the labels
    plt.ylim(0, max(max(speedups_over_matrix)) * 1.3)

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

    KERNEL_SIZE = int(input("Input Kernel size in multiple of 8: "))

    speedups_over_matrix = []

    for m in MATRIX_SIZE:
        speedup_over_block=[]
        del_tiles = []

        for b in TILE_SIZE:
            if b==0:
                continue
            elif b<KERNEL_SIZE:
                del_tiles.append(b)
            else:    
                speedup_over_block.append( round(run_optimized_executable(m, b, KERNEL_SIZE),2) )

        print(f"speedup calculated for matrix size:{m}")
        speedups_over_matrix.append(speedup_over_block)
    
    # Removes the invalid tile sizes
    for b in del_tiles:
           TILE_SIZE.remove(b)

    # Plot the results
    plot_results(MATRIX_SIZE, speedups_over_matrix, TILE_SIZE, KERNEL_SIZE)

if __name__ == "__main__":
    main()
