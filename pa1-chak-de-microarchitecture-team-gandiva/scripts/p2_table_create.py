import subprocess
import re
from statistics import mean
import matplotlib.pyplot as plt
import pandas as pd

# Constants
BUILD_DIR = '../part2/build'
EXEC_OPTIMIZED = 'all'
EXECUTABLE = f'{BUILD_DIR}/{EXEC_OPTIMIZED}'
AVG_ITERATIONS = 5
MATRIX_SIZE = 5000  # Example matrix size
TILE_SIZE = 32     # Example tile size
KERNEL_SIZE = 8    # Example kernel size

# Techniques to track
techniques = [
    "Naive",
    "Tiled",
    "SIMD",
    "Prefetch",
    "Tiled SIMD",
    "SIMD Prefetch",
    "Tiled Prefetch",
    "SIMD Tiled Prefetch"
]

# Initialize dictionary to store times
times = {technique: [] for technique in techniques}

# Function to run the executable and capture output
def run_executable():
    try:
        result = subprocess.run([EXECUTABLE, str(MATRIX_SIZE), str(KERNEL_SIZE) ,str(TILE_SIZE)], capture_output=True, text=True)        
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running the executable: {e}")
        return None

# Parse the output and extract times
def parse_output(output):
    for technique in techniques:
        # Create a regex pattern for each technique
        pattern = fr"{technique} Convolution Time: ([\d\.]+) seconds"
        match = re.search(pattern, output)
        if match:
            time = float(match.group(1))
            times[technique].append(time)

# Run the executable AVG_ITERATIONS times and collect data
for _ in range(AVG_ITERATIONS):
    output = run_executable()
    if output:
        parse_output(output)

# Calculate the average time for each technique and round to 4 decimal places
average_times = {technique: round(mean(times[technique]), 4) for technique in techniques}

# Convert the data into a Pandas DataFrame for easy visualization
df = pd.DataFrame(list(average_times.items()), columns=["Techniques", "Time taken"])

# Plotting the table and saving as a PNG
fig, ax = plt.subplots(figsize=(12, 8))  # Increased size to fill the page
ax.axis('tight')
ax.axis('off')

# Add table name above the table
table_name = f"Matrix convolution with matrix_size:{MATRIX_SIZE}, tile size:{TILE_SIZE} and KERNEL_SIZE:{KERNEL_SIZE}"
plt.title(table_name, fontsize=16, fontweight='bold')

# Create a table and customize its appearance
the_table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')

# Bold the header and align it to the center
for (i, j), cell in the_table.get_celld().items():
    if i == 0:
        cell.set_text_props(weight='bold', ha='center', va='center')
        cell.set_facecolor('#4CAF50')
        cell.set_text_props(color='white')
    else:
        cell.set_text_props(ha='left', va='center')  # Align data to the left
        if i % 2 == 0:
            cell.set_facecolor('#f2f2f2')
        else:
            cell.set_facecolor('#e6e6e6')

# Adjust the font size to make the table fill the page
the_table.auto_set_font_size(False)
the_table.set_fontsize(12)
the_table.scale(1.2, 1.2)  # Scale the table to fill the space

plt.tight_layout(pad=0)  # Minimize padding around the plot
# Save the table as a PNG file with minimal margins and no white space
plt.savefig('matrix_convolution_table.png', bbox_inches='tight', pad_inches=0.2, dpi=300)

print("Table saved successfully as 'matrix_convolution_table.png'.")
