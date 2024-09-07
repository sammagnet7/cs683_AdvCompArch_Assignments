import subprocess
import re
import numpy as np
import matplotlib.pyplot as plt

# Global variables
FONT_SIZE = 18
AVG_ITERATIONS = 2
BUILD_DIR = '../part1/build'
MATRIX_SIZE = [1000, 3000, 5000]
TILE_SIZE = 32   # Optimal value 32, found after testing

techniques = [
    "tiling",
    "prefetch",
    "tiling-prefetch",
]

# Function to extract speedup from the output
def extract_speedup(output):
    match = re.search(r"The speedup obtained by .* is ([\d.]+)", output)
    if match:
        return float(match.group(1))
    return None

# Function to run the executable and calculate average speedup
def run_optimized_executable(matrix_size, tile_size, executable, iterations=AVG_ITERATIONS):
    speedup_sum = 0.0
    for _ in range(iterations):
        result = subprocess.run([executable, str(matrix_size), str(tile_size)], capture_output=True, text=True)
        speedup = extract_speedup(result.stdout)
        if speedup is not None:
            speedup_sum += speedup
    return speedup_sum / iterations

# Function to plot the results
def plot_results(matrix_size, speedups_over_matrix, techniques):

    n_bars = len(techniques)
    bar_width = 0.11

    bar_positions = [np.arange(len(matrix_size)) + i * bar_width for i in range(n_bars)]

    plt.figure(figsize=(14, 6))

    # Plotting the bars
    for i in range(n_bars):
        label = techniques[i]
        plt.bar(bar_positions[i], [speedup[i] for speedup in speedups_over_matrix], width=bar_width, label=label)

    # Adding the x-axis labels
    plt.xticks(np.arange(len(matrix_size)) + (n_bars - 1) * bar_width / 2, matrix_size, fontsize=FONT_SIZE)

    plt.yticks(fontsize=FONT_SIZE)

    plt.ylabel('Speedup', fontsize=FONT_SIZE)

    plt.xlabel('Matrix Size', fontsize=FONT_SIZE)

    plt.title(f'Transpose Speedup vs Matrix size vs Optimization techniques (Tile size:{TILE_SIZE})', fontsize=FONT_SIZE)

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
    plt.savefig("part1_all_techniques.png")

# Main script to collect speedup data and plot it
if __name__ == "__main__":
    speedups_over_matrix = []

    for matrix_size in MATRIX_SIZE:
        speedups_over_techniques = []
        for technique in techniques:
            executable = f'{BUILD_DIR}/{technique}'
            avg_speedup = run_optimized_executable(matrix_size, TILE_SIZE, executable)
            speedups_over_techniques.append(( round(avg_speedup,2) ))
        speedups_over_matrix.append(speedups_over_techniques)

    # Plot the results
    plot_results(MATRIX_SIZE, speedups_over_matrix, techniques)
