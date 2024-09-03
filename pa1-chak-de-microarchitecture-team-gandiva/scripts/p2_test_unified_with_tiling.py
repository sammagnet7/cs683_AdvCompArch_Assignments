import subprocess
import re
import numpy as np
import matplotlib.pyplot as plt
import math

################### customize #######################
FONT_SIZE = 18
AVG_ITERATIONS = 2

BUILD_DIR='../part2/build'
EXEC_NAIVE='naive'
EXEC_OPTIMIZED=['tiling','tiling-prefetch', 'tiling-simd', 'tiling-simd-prefetch'] # tiling, tiling-prefetch, tiling-simd, tiling-simd-prefetch

MATRIX_SIZE = [1000, 3000, 5000]
TILE_SIZE = [0,16,32,48,64] # Add 0 for naive approach

################### customize #######################

# Function to extract Instructions from the output
def extract_instr(output):
    match = re.search(r"Instructions: ([\d.]+)", output)
    if match:
        return int(match.group(1))
    return None

def extract_speedup(output):
    match = re.search(r"Speedup:([\d.]+)", output)
    if match:
        return float(match.group(1))
    return None

def extract_mpki(output):
    match = re.search(r"MPKI: ([\d.]+)", output)
    if match:
        return float(match.group(1))
    return None

# Function to run the perf stat command and calculate average Instructions
def run_perf_stat(executable, matrix_size, tile_size, KERNEL_SIZE, iterations=AVG_ITERATIONS):
    instr_sum = 0
    mpki_sum = 0.0
    speedup_sum = 0.0
    for _ in range(iterations):
        bash_command = f"""
        perf stat -x, -e instructions,L1-dcache-load-misses {BUILD_DIR}/{executable} {matrix_size} {KERNEL_SIZE} {tile_size} 2>&1 | 
        gawk --bignum '/instructions/ {{instructions=$1}}
        /L1-dcache-load-misses/ {{misses=$1}}
        /Speedup/ {{label=$(NF-1); speedup=$NF}}
        END {{
            mpki = ((misses * 1000) / instructions); 
            printf "\\nInstructions: %d\\n", instructions;
            printf "\\nMPKI: %.2f\\n", mpki;
            printf label speedup;
        }}'
        """
        result = subprocess.run(bash_command, shell=True, capture_output=True, text=True)
        instr = extract_instr(result.stdout)
        mpki = extract_mpki(result.stdout)
        speedup = extract_speedup(result.stdout)

        if instr is not None:
            instr_sum += instr
        if mpki is not None:
            mpki_sum += mpki
        if speedup is not None:
            speedup_sum += speedup

    instr_avg = instr_sum / iterations
    instr_avg = round(instr_avg / 1000000000, 2)# Billion instructions
    mpki_avg = round(mpki_sum / iterations, 2)
    avg_speedup = round(speedup_sum / iterations, 2)
    print(f"{executable} {matrix_size} {tile_size}, instructions {instr_avg}" )
    return instr_avg, mpki_avg, avg_speedup

# Function to plot the results
def plot_results_inst(executable, matrix_size, instr_over_matrix, tile_size, KERNEL_SIZE):

    n_bars = len(tile_size)
    bar_width = 0.11

    bar_positions = [np.arange(len(matrix_size)) + i * bar_width for i in range(n_bars)]

    plt.figure(figsize=(14, 8))

    # Plotting the bars
    for i in range(n_bars):
        label = 'naive approach' if tile_size[i] == 0 else f'Tile Size {tile_size[i]}'
        plt.bar(bar_positions[i], [instr[i] for instr in instr_over_matrix], width=bar_width, label=label)

    # Adding the x-axis labels
    plt.xticks(np.arange(len(matrix_size)) + (n_bars - 1) * bar_width / 2, matrix_size, fontsize=FONT_SIZE)

    plt.yticks(fontsize=FONT_SIZE)

    plt.ylabel('Number of Instructions in Billion ', fontsize=FONT_SIZE)

    plt.xlabel('Matrix Size', fontsize=FONT_SIZE)

    plt.title(f'Number of Instructions vs Matrix Size for optimization ({executable} with KERNEL_SIZE={KERNEL_SIZE})', fontsize=FONT_SIZE)

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

    # Save/Display the plot
    plt.savefig(f"{executable}_inst_10K_{KERNEL_SIZE}.png")


def plot_results_mpki(executable,matrix_size, mpki_over_matrix, tile_size, KERNEL_SIZE):

    n_bars = len(tile_size)
    bar_width = 0.11

    bar_positions = [np.arange(len(matrix_size)) + i * bar_width for i in range(n_bars)]

    plt.figure(figsize=(14, 8))

    # Plotting the bars
    for i in range(n_bars):
        label = 'naive approach' if tile_size[i] == 0 else f'Tile Size {tile_size[i]}'
        plt.bar(bar_positions[i], [mpki[i] for mpki in mpki_over_matrix], width=bar_width, label=label)

    # Adding the x-axis labels
    plt.xticks(np.arange(len(matrix_size)) + (n_bars - 1) * bar_width / 2, matrix_size, fontsize=FONT_SIZE)

    plt.yticks(fontsize=FONT_SIZE)

    plt.ylabel('MPKI', fontsize=FONT_SIZE)

    plt.xlabel('Matrix Size', fontsize=FONT_SIZE)

    plt.title(f'MPKI vs Matrix Size for optimization ({executable} with KERNEL_SIZE={KERNEL_SIZE})', fontsize=FONT_SIZE)

    # Adjusting y-axis limit to make space for the labels
    plt.ylim(0, max(max(mpki_over_matrix)) * 1.2)

    # Adding legends outside the plot
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), fancybox=True, shadow=True, ncol=4, fontsize=FONT_SIZE)

    # Adding values on top of bars
    for i in range(n_bars):
        for j in range(len(matrix_size)):
            plt.text(bar_positions[i][j], mpki_over_matrix[j][i] + max(max(mpki_over_matrix)) * 0.03, 
                 str(mpki_over_matrix[j][i]), ha='center', va='bottom', rotation='vertical', fontsize=FONT_SIZE)

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2) 

    # Save/Display the plot
    plt.savefig(f"{executable}_mpki_10K_{KERNEL_SIZE}.png")

def plot_results_speedup(executable,matrix_size, speedups_over_matrix, tile_size, KERNEL_SIZE):

    n_bars = len(tile_size)
    bar_width = 0.11

    bar_positions = [np.arange(len(matrix_size)) + i * bar_width for i in range(n_bars)]

    plt.figure(figsize=(14, 8))

    # Plotting the bars
    for i in range(n_bars - 1):
        label = f'Tile Size {tile_size[i+1]}'
        plt.bar(bar_positions[i], [speedup[i] for speedup in speedups_over_matrix], width=bar_width, label=label)

    # Adding the x-axis labels
    plt.xticks(np.arange(len(matrix_size)) + (n_bars - 1) * bar_width / 2, matrix_size, fontsize=FONT_SIZE)

    plt.yticks(fontsize=FONT_SIZE)

    plt.ylabel('Speedup', fontsize=FONT_SIZE)

    plt.xlabel('Matrix Size', fontsize=FONT_SIZE)

    plt.title(f'Speedup vs Matrix Size for optimization ({executable} with KERNEL_SIZE={KERNEL_SIZE})', fontsize=FONT_SIZE)

    # Adjusting y-axis limit to make space for the labels
    plt.ylim(0, max(max(speedups_over_matrix)) * 1.3)

    # Adding legends outside the plot
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), fancybox=True, shadow=True, ncol=4, fontsize=FONT_SIZE)

    # Adding values on top of bars
    for i in range(n_bars-1):
        for j in range(len(matrix_size)):
            plt.text(bar_positions[i][j], speedups_over_matrix[j][i] + max(max(speedups_over_matrix)) * 0.03, 
                 str(speedups_over_matrix[j][i]), ha='center', va='bottom', rotation='vertical', fontsize=FONT_SIZE)

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2) 

    # Save/Display the plot
    plt.savefig(f"{executable}_speedup_10K_{KERNEL_SIZE}.png")


def main():

    KERNEL_SIZE = int(input("Input Kernel size in multiple of 8: "))

    for execs in EXEC_OPTIMIZED:
        over_matrix = {'instruction':[],
                        'mpki':[],
                        'speedup':[]}
        for m in MATRIX_SIZE:    
            over_block_inst=[]
            over_block_mpki=[]
            over_block_speedup=[]
            del_tiles = []
    
            for b in TILE_SIZE:
                    if b==0:
                        instruction, mpki, speedup = run_perf_stat(EXEC_NAIVE, m, b, KERNEL_SIZE)
                        over_block_inst.append(instruction)
                        over_block_mpki.append(mpki)
                    elif b<KERNEL_SIZE:
                        del_tiles.append(b)
                        continue
                    else:
                        instruction, mpki, speedup = run_perf_stat(execs, m, b, KERNEL_SIZE)
                        over_block_inst.append(instruction)
                        over_block_mpki.append(mpki)
                        over_block_speedup.append(speedup)
            print(f"Calculated for matrix size:{m} program {execs}")
            over_matrix['instruction'].append(over_block_inst)
            over_matrix['mpki'].append(over_block_mpki)
            over_matrix['speedup'].append(over_block_speedup)

        # Removes invalid tile sizes
        for b in del_tiles:
               TILE_SIZE.remove(b)

        # Plot the results
        plot_results_inst(execs, MATRIX_SIZE, over_matrix['instruction'], TILE_SIZE, KERNEL_SIZE)
        plot_results_mpki(execs, MATRIX_SIZE, over_matrix['mpki'], TILE_SIZE, KERNEL_SIZE)
        plot_results_speedup(execs, MATRIX_SIZE, over_matrix['speedup'],TILE_SIZE, KERNEL_SIZE)

if __name__ == "__main__":
    main()