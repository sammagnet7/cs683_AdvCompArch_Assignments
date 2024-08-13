BUILD=build
CC=g++
FLAGS=-mavx512f

naive: build
	$(CC) $(FLAGS) transpose.c -o $(BUILD)/$@

tiling: build
	$(CC) $(FLAGS) transpose.c -D OPTIMIZE_TILING -o $(BUILD)/$@

prefetch: build
	$(CC) $(FLAGS) transpose.c -D OPTIMIZE_PREFETCH -o $(BUILD)/$@


tiling-prefetch: build
	$(CC) $(FLAGS) transpose.c -D OPTIMIZE_TILING_PREFETCH -o $(BUILD)/$@


all: build
	$(CC) $(FLAGS) transpose.c -D OPTIMIZE_TILING -D OPTIMIZE_PREFETCH -D OPTIMIZE_TILING_PREFETCH -o $(BUILD)/$@

clean:
	@rm -rf $(BUILD)
	@rm -f out.txt

build:
	@mkdir -p $(BUILD)