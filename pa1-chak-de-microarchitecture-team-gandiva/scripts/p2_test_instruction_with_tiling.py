import subprocess
import re
import numpy as np
import matplotlib.pyplot as plt
import math

################### customize #######################
FONT_SIZE = 18
AVG_ITERATIONS = 5

BUILD_DIR='../part2/build'
EXEC_NAIVE='naive'
EXEC_OPTIMIZED='tiling' # tiling, tiling-prefetch, tiling-simd, tiling-simd-prefetch

MATRIX_SIZE = [1000, 3000, 5000, 10000, 15000, 20000]
TILE_SIZE = [0,4,8,16,32,48,56,64] # Add 0 for naive approach

################### customize #######################

# Function to extract Instructions from the output
def extract_instr(output):
    match = re.search(r"Instructions: ([\d.]+)", output)
    if match:
        return int(match.group(1))
    return None

# Function to run the perf stat command and calculate average Instructions
def run_perf_stat(executable, matrix_size, tile_size, KERNEL_SIZE, iterations=AVG_ITERATIONS):
    instr_sum = 0
    for _ in range(iterations):
        bash_command = f"""
        perf stat -x, -e instructions,L1-dcache-load-misses {BUILD_DIR}/{executable} {matrix_size} {KERNEL_SIZE} {tile_size} 2>&1 | 
        gawk --bignum '/instructions/ {{instructions=$1}}
        /L1-dcache-load-misses/ {{misses=$1}}
        END {{
            printf "\\nInstructions: %d\\n", instructions;
        }}'
        """
        result = subprocess.run(bash_command, shell=True, capture_output=True, text=True)
        instr = extract_instr(result.stdout)

        if instr is not None:
            instr_sum += instr

    instr_avg = instr_sum / iterations

    return (round(instr_avg / 1000000000, 2)) # Billio instructions

# Function to plot the results
def plot_results(matrix_size, instr_over_matrix, tile_size, KERNEL_SIZE):

    n_bars = len(tile_size)
    bar_width = 0.11

    bar_positions = [np.arange(len(matrix_size)) + i * bar_width for i in range(n_bars)]

    plt.figure(figsize=(14, 6))

    # Plotting the bars
    for i in range(n_bars):
        label = 'naive approach' if tile_size[i] == 0 else f'Tile Size {tile_size[i]}'
        plt.bar(bar_positions[i], [instr[i] for instr in instr_over_matrix], width=bar_width, label=label)

    # Adding the x-axis labels
    plt.xticks(np.arange(len(matrix_size)) + (n_bars - 1) * bar_width / 2, matrix_size, fontsize=FONT_SIZE)

    plt.yticks(fontsize=FONT_SIZE)

    plt.ylabel('Number of Instructions in Billion ', fontsize=FONT_SIZE)

    plt.xlabel('Matrix Size', fontsize=FONT_SIZE)

    plt.title(f'Number of Instructions vs Matrix Size for optimization ({EXEC_OPTIMIZED} with KERNEL_SIZE={KERNEL_SIZE})', fontsize=FONT_SIZE)

    # Adjusting y-axis limit to make space for the labels
    plt.ylim(0, max(max(instr_over_matrix)) * 1.2)

    # Adding legends outside the plot
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), fancybox=True, shadow=True, ncol=4, fontsize=FONT_SIZE)

    # Adding values on top of bars
    for i in range(n_bars):
        for j in range(len(matrix_size)):
            plt.text(bar_positions[i][j], instr_over_matrix[j][i] + max(max(instr_over_matrix)) * 0.03, 
                 str(instr_over_matrix[j][i]), ha='center', va='bottom', rotation='vertical', fontsize=FONT_SIZE)

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2) 

    # Display the plot
    plt.show()


def main():

    KERNEL_SIZE = int(input("Input Kernel size in multiple of 8: "))

    instr_over_matrix = []

    for m in MATRIX_SIZE:    
        instr_over_block=[] 
        del_tiles = []
  
        for b in TILE_SIZE:
                if b==0:
                    instr_over_block.append( round(run_perf_stat(EXEC_NAIVE, m, b, KERNEL_SIZE),2)  )
                elif b<KERNEL_SIZE:
                    del_tiles.append(b)
                    continue
                else:
                    instr_over_block.append( round(run_perf_stat(EXEC_OPTIMIZED, m, b, KERNEL_SIZE),2) )

        print(f"Number of Instructions calculated for matrix size:{m}")
        instr_over_matrix.append(instr_over_block)

    # Removes invalid tile sizes
    for b in del_tiles:
           TILE_SIZE.remove(b)

    # Plot the results
    plot_results(MATRIX_SIZE, instr_over_matrix, TILE_SIZE, KERNEL_SIZE)

if __name__ == "__main__":
    main()