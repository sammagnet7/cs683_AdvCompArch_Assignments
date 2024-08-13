BUILD=build
CC=g++
FLAGS=-mavx512f

naive: build
	$(CC) $(FLAGS) convolution.c -o $(BUILD)/$@

tiling: build
	$(CC) $(FLAGS) convolution.c -D OPTIMIZE_TILING -o $(BUILD)/$@

prefetch: build
	$(CC) $(FLAGS) convolution.c -D OPTIMIZE_PREFETCH -o $(BUILD)/$@

simd: build
	$(CC) $(FLAGS) convolution.c -D OPTIMIZE_SIMD -o $(BUILD)/$@

tiling-prefetch: build
	$(CC) $(FLAGS) convolution.c -D OPTIMIZE_TILING_PREFETCH -o $(BUILD)/$@

tiling-simd: build
	$(CC) $(FLAGS) convolution.c -D OPTIMIZE_TILING_SIMD -o $(BUILD)/$@

simd-prefetch: build
	$(CC) $(FLAGS) convolution.c -D OPTIMIZE_SIMD_PREFETCH -o $(BUILD)/$@

tiling-simd-prefetch: build
	$(CC) $(FLAGS) convolution.c -D OPTIMIZE_TILING_SIMD_PREFETCH -o $(BUILD)/$@

all: build
	$(CC) $(FLAGS) convolution.c -D OPTIMIZE_TILING -D OPTIMIZE_SIMD -D OPTIMIZE_PREFETCH -D OPTIMIZE_TILING_PREFETCH -D OPTIMIZE_TILING_SIMD -D OPTIMIZE_SIMD_PREFETCH -D OPTIMIZE_TILING_SIMD_PREFETCH -o $(BUILD)/$@

clean:
	@rm -rf $(BUILD)
	@rm -f out.txt

build:
	@mkdir -p $(BUILD)