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
def plot_results(matrix_size, mpki_over_matrix, block_size):

    n_bars = len(block_size)
    bar_width = 0.12

    bar_positions = [np.arange(len(matrix_size)) + i * bar_width for i in range(n_bars)]

    plt.figure(figsize=(14, 6))

    # Plotting the bars
    for i in range(n_bars):
        label = 'naive approach' if block_size[i] == 0 else f'Block Size {block_size[i]}'
        plt.bar(bar_positions[i], [mpki[i] for mpki in mpki_over_matrix], width=bar_width, label=label)

    # Adding the x-axis labels
    plt.xticks(np.arange(len(matrix_size)) + (n_bars - 1) * bar_width / 2, matrix_size)

    plt.ylabel('MPKI')

    plt.xlabel('Matrix Size')

    plt.title('MPKI vs Matrix Size for Different Block Sizes')

    # Adjusting y-axis limit to make space for the labels
    plt.ylim(0, max(max(mpki_over_matrix)) * 1.2)

    # Adding legends outside the plot
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), fancybox=True, shadow=True, ncol=4)

    # Adding values on top of bars
    for i in range(n_bars):
        for j in range(len(matrix_size)):
            plt.text(bar_positions[i][j], mpki_over_matrix[j][i] + max(max(mpki_over_matrix)) * 0.05, 
                 str(mpki_over_matrix[j][i]), ha='center', va='bottom', rotation='vertical')

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2) 

    # Display the plot
    plt.show()

def main():

    #matrix_size = [5000,10000,15000,20000,250000,30000]
    #block_size = [0,4,8,16,32,48,64,96,128,152]

    matrix_size = [200, 250, 300, 350, 400, 450, 500, 550, 600, 1000]
    block_size = [0,4,8,16,32,64,128,]

    mpki_over_matrix = []

    for m in matrix_size:    
        mpki_over_block=[]   
        for b in block_size:
                if(b==0):
                    mpki_over_block.append( round(run_perf_stat('naive', m, b),2)  )
                else:
                    mpki_over_block.append( round(run_perf_stat('tiling', m, b),2) )

        print(f"mpki calculated for matrix size:{m}")
        mpki_over_matrix.append(mpki_over_block)

    # Plot the results
    plot_results(matrix_size, mpki_over_matrix, block_size)

if __name__ == "__main__":
    main()