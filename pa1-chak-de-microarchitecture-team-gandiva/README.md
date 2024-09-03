# CS683 2024 Assignment 1
> **Note:** {workspace}= "pa1-chak-de-microarchitecture-team-gandiva/"

### Team members
* Soumik Dutta (23m0826)
* Sm Arif Ali (23m0822)

### System details on which we are performing all the tests:

* Processor: Intel(R) Core(TM) i7-14650HX
* Hyper threading is turned off ( Script: {workspace}/scripts/hyper_thread_toggle.sh )
*  CPU frequency: 5.2 GHz
* Cache:
    * L1 D cache: 48 KB
        * Line size: 64 B
        * Associativity: 12
        * Number of sets: 64
    * L1 I cache: 32 KB
        * Line size: 64 B
        * Associativity: 8
        * Number of sets: 64
    * L2 cache: 2 MB
        * Line size: 64 B
        * Associativity: 16
        * Number of sets: 2048
    * L3 cache: 30 MB
        * Line size: 64 B
        * Associativity: 12
        * Number of sets: 40960


### Testing values:
 * Element size: 8 Bytes [ size of Double ] 
 * Max Tile size = 55x55 (i.e. $\sqrt((48*1024/2)/8)$) [ As $2B^2<C$ where $C= 48 KByte$ ] 
 * Tile sizes: [0,4,8,16,32,48,56,64]
 * Matrix sizes: [1000,3000,5000,10000,15000,20000]
 * Averaged over 5 rounds each

# Task 1 (Matrix transpose)

## 1A: Tile it to see it
### Plots:
<img title="a title" alt="Alt text" src="./plots/part1/tiling_inst_20K_64.png">
<img title="a title" alt="Alt text" src="./plots/part1/tiling_mpki_20K_64.png">
<img title="a title" alt="Alt text" src="./plots/part1/tiling_speedup_20K_64.png">

### Description:


## 1B: Fetch it but with soft corner (software prefetching)

### Plots:
<img title="a title" alt="Alt text" src="./plots/part1/prefetch_inst_20K.png">
<img title="a title" alt="Alt text" src="./plots/part1/prefetch_mpki_20K.png">
<img title="a title" alt="Alt text" src="./plots/part1/prefetch_speedup_20K.png">

### Description:

## 1C: Tiling + Prefetching

### Plots:
<img title="a title" alt="Alt text" src="./plots/part1/tilingprefetch_inst_20K_64.png">
<img title="a title" alt="Alt text" src="./plots/part1/tilingprefetch_mpki_20K_64.png">
<img title="a title" alt="Alt text" src="./plots/part1/tilingprefetch_speedup_20K_64.png">

### Description:

## All techniques together:

### Plots:
<img title="a title" alt="Alt text" src="./plots/part1/part1_all_techniques.png">

### Description:



# Task 2 (2D convolution)

## 2A: Shhh SIMD in action

### Plots:
<img title="a title" alt="Alt text" src="./plots/part2/simd_inst_10K_8.png">
<img title="a title" alt="Alt text" src="./plots/part2/simd_inst_10K_16.png">
<img title="a title" alt="Alt text" src="./plots/part2/simd_mpki_10K_8.png">
<img title="a title" alt="Alt text" src="./plots/part2/simd_mpki_10K_16.png">
<img title="a title" alt="Alt text" src="./plots/part2/simd_speedup_10K_8.png">
<img title="a title" alt="Alt text" src="./plots/part2/simd_speedup_10K_16.png">

### Description:

## 2B: Tile it again

### Plots:
<img title="a title" alt="Alt text" src="./plots/part2/tiling_inst_10K_8.png">
<img title="a title" alt="Alt text" src="./plots/part2/tiling_inst_10K_16.png">
<img title="a title" alt="Alt text" src="./plots/part2/tiling_mpki_10K_8.png">
<img title="a title" alt="Alt text" src="./plots/part2/tiling_mpki_10K_16.png">
<img title="a title" alt="Alt text" src="./plots/part2/tiling_speedup_10K_8.png">
<img title="a title" alt="Alt text" src="./plots/part2/tiling_speedup_10K_16.png">

### Description:

## 2C: Software Prefetching

### Plots:
<img title="a title" alt="Alt text" src="./plots/part2/prefetch_inst_10K_8.png">
<img title="a title" alt="Alt text" src="./plots/part2/prefetch_inst_10K_16.png">
<img title="a title" alt="Alt text" src="./plots/part2/prefetch_mpki_10K_8.png">
<img title="a title" alt="Alt text" src="./plots/part2/prefetch_mpki_10K_16.png">
<img title="a title" alt="Alt text" src="./plots/part2/prefetch_speedup_10K_8.png">
<img title="a title" alt="Alt text" src="./plots/part2/prefetch_speedup_10K_16.png">

### Description:

## 2D: Hum saath saath hain 

### Plots:
#### simd-prefecth
<img title="a title" alt="Alt text" src="./plots/part2/simd-prefetch_inst_10K_8.png">
<img title="a title" alt="Alt text" src="./plots/part2/simd-prefetch_inst_10K_16.png">
<img title="a title" alt="Alt text" src="./plots/part2/simd-prefetch_mpki_10K_8.png">
<img title="a title" alt="Alt text" src="./plots/part2/simd-prefetch_mpki_10K_16.png">
<img title="a title" alt="Alt text" src="./plots/part2/simd-prefetch_speedup_10K_8.png">
<img title="a title" alt="Alt text" src="./plots/part2/simd-prefetch_speedup_10K_16.png">


#### tiling-prefetch

<img title="a title" alt="Alt text" src="./plots/part2/tiling-prefetch_inst_10K_8.png">
<img title="a title" alt="Alt text" src="./plots/part2/tiling-prefetch_inst_10K_16.png">
<img title="a title" alt="Alt text" src="./plots/part2/tiling-prefetch_mpki_10K_8.png">
<img title="a title" alt="Alt text" src="./plots/part2/tiling-prefetch_mpki_10K_16.png">
<img title="a title" alt="Alt text" src="./plots/part2/tiling-prefetch_speedup_10K_8.png">
<img title="a title" alt="Alt text" src="./plots/part2/tiling-prefetch_speedup_10K_16.png">


#### tiling-simd

<img title="a title" alt="Alt text" src="./plots/part2/tiling-simd_inst_10K_8.png">
<img title="a title" alt="Alt text" src="./plots/part2/tiling-simd_inst_10K_16.png">
<img title="a title" alt="Alt text" src="./plots/part2/tiling-simd_mpki_10K_8.png">
<img title="a title" alt="Alt text" src="./plots/part2/tiling-simd_mpki_10K_16.png">
<img title="a title" alt="Alt text" src="./plots/part2/tiling-simd_speedup_10K_8.png">
<img title="a title" alt="Alt text" src="./plots/part2/tiling-simd_speedup_10K_16.png">

#### tiling-simd-prefetch
<img title="a title" alt="Alt text" src="./plots/part2/tiling-simd-prefetch_inst_10K_8.png">
<img title="a title" alt="Alt text" src="./plots/part2/tiling-simd-prefetch_inst_10K_16.png">
<img title="a title" alt="Alt text" src="./plots/part2/tiling-simd-prefetch_mpki_10K_8.png">
<img title="a title" alt="Alt text" src="./plots/part2/tiling-simd-prefetch_mpki_10K_16.png">
<img title="a title" alt="Alt text" src="./plots/part2/tiling-simd-prefetch_speedup_10K_8.png">
<img title="a title" alt="Alt text" src="./plots/part2/tiling-simd-prefetch_speedup_10K_16.png">

### Description:

## All techniques together:

### Plots:
<img title="a title" alt="Alt text" src="./plots/part2/part2_all_techniques.png">

### Description:


 