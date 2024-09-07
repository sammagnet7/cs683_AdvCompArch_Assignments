#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <stdint.h>
#include <immintrin.h>

#define MIN(a, b) ((a) < (b) ? (a) : (b))
const int LINE_SIZE = 64;              // 64 Byte L1-D cache line
const int LLC_size = 30 * 1024 * 1024; // 30 MB LLC cache

void verify_correctness(double *C, double *D, int dim)
{
    double epsilon = 1e-9;
    for (int i = 0; i < dim; i++)
    {
        for (int j = 0; j < dim; j++)
        {
            if (fabs(C[i * dim + j] - D[i * dim + j]) > epsilon)
            {
                printf("%f & %f at (%d %d)\n", C[i * dim + j], D[i * dim + j], i, j);
                printf("The two matrices are NOT identical\n");
                return;
            }
        }
    }
    printf("The matrix operation is correct!\n");
    return;
}

// Naive Matrix Transpose
void naiveMatrixTranspose(double *matrix, double *transpose, int size)
{
    for (int i = 0; i < size; i++)
    {
        for (int j = 0; j < size; j++)
        {
            transpose[j * size + i] = matrix[i * size + j];
        }
    }
}

// Cache-Aware tiled Matrix Transpose
void tiledMatrixTranspose(double *matrix, double *transpose, int size, int blockSize)
{
    // Students need to implement this function
    for (int ii = 0; ii < size; ii += blockSize)
    {
        for (int jj = 0; jj < size; jj += blockSize)
        {
            for (int i = ii; i < MIN(ii + blockSize, size); i++)
            {
                for (int j = jj; j < MIN(jj + blockSize, size); j++)
                {
                    transpose[j * size + i] = matrix[i * size + j];
                }
            }
        }
    }
}
void flushCache()
{
    // Create a buffer large enough to fill the LLC
    size_t buffer_size = LLC_size;
    char *buffer = (char *)malloc(buffer_size);
    if (!buffer)
    {
        perror("malloc failed");
        return;
    }

    // Access each cache line to flush the LLC
    for (size_t i = 0; i < buffer_size; i += LINE_SIZE)
    {
        // Invalidates from every level of the cache hierarchy in the cache coherence domain the cache line that contains the linear address specified with the memory operand.
        _mm_clflush(&buffer[i]);
    }

    free(buffer);
}
// Prefetch Matrix Transpose
void prefetchMatrixTranspose(double *matrix, double *transpose, int size)
{
    // Students need to implement this function

    matrix = (double *)__builtin_assume_aligned(matrix, LINE_SIZE); // 64 Bytes long cache line
    transpose = (double *)__builtin_assume_aligned(transpose, LINE_SIZE);

    for (int i = 0; i < size; i++)
    {
        for (int j = 0; j < size; j++)
        {
            _mm_prefetch((char *)&matrix[i * size + (j + 16)], _MM_HINT_T0);
            _mm_prefetch((char *)&transpose[(j + 8) * size + i], _MM_HINT_T0);

            transpose[j * size + i] = matrix[i * size + j];
        }
    }
}

// Tiled Prefetch Matrix Transpose
void tiledPrefetchedMatrixTranspose(double *matrix, double *transpose, int size, int blockSize)
{
    // Students need to implement this function
    // Ensure the matrix and transpose are aligned to 64 bytes (cache line size)
    matrix = (double *)__builtin_assume_aligned(matrix, LINE_SIZE);
    transpose = (double *)__builtin_assume_aligned(transpose, LINE_SIZE);

    int elements_in_line = LINE_SIZE / 8;         // size(double)=>8
    int src_pf_distance = (elements_in_line * 4); // 4 lines
    int dest_pf_distance = 8;

    for (int ii = 0; ii < size; ii += blockSize)
    {
        for (int jj = 0; jj < size; jj += blockSize)
        {
            for (int i = ii; i < ii + blockSize && i < size; i++)
            {
                for (int j = jj; j < jj + blockSize && j < size; j += 4) // Unroll by 4
                {
                    // Row wise pre fetch
                    _mm_prefetch((char *)&matrix[i * size + (j + 8)], _MM_HINT_T0);
                    _mm_prefetch((char *)&matrix[i * size + (j + 16)], _MM_HINT_T0);
                    _mm_prefetch((char *)&matrix[i * size + (j + 24)], _MM_HINT_T0);
                    _mm_prefetch((char *)&matrix[i * size + (j + 32)], _MM_HINT_T0);

                    // Column wise pre fetch
                    _mm_prefetch((char *)&transpose[((j + 14)) * size + i], _MM_HINT_T0);

                    transpose[j * size + i] = matrix[i * size + j];
                    if (j + 1 < size)
                        transpose[(j + 1) * size + i] = matrix[i * size + (j + 1)];
                    if (j + 2 < size)
                        transpose[(j + 2) * size + i] = matrix[i * size + (j + 2)];
                    if (j + 3 < size)
                        transpose[(j + 3) * size + i] = matrix[i * size + (j + 3)];
                }
            }
        }
    }
}

double naive(double *matrix, double *transpose, int size)
{
    // Run and time the naive matrix transpose
    flushCache();
    clock_t start = clock();
    naiveMatrixTranspose(matrix, transpose, size);

    clock_t end = clock();
    double time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("Time taken by naive matrix transpose: %f seconds\n", time_taken);

    return time_taken;
}

double tiled(double *matrix, double *transpose, int size, int blockSize)
{
    // Run and time the tiled matrix transpose
    flushCache();
    clock_t start = clock();
    tiledMatrixTranspose(matrix, transpose, size, blockSize);
    clock_t end = clock();
    double time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("Time taken by tiled matrix transpose: %f seconds\n", time_taken);

    return time_taken;
}

double prefetched(double *matrix, double *transpose, int size)
{
    // Run and time the prefetch matrix transpose
    flushCache();
    clock_t start = clock();
    prefetchMatrixTranspose(matrix, transpose, size);
    clock_t end = clock();
    double time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("Time taken by prefetch matrix transpose: %f seconds\n", time_taken);

    return time_taken;
}

double tiled_prefetched(double *matrix, double *transpose, int size, int blockSize)
{
    // Run and time the prefetch matrix transpose
    flushCache();
    clock_t start = clock();
    tiledPrefetchedMatrixTranspose(matrix, transpose, size, blockSize);
    clock_t end = clock();
    double time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("Time taken by tiled prefetch matrix transpose: %f seconds\n", time_taken);

    return time_taken;
}

// Function to initialize the matrix with random values
void initializeMatrix(double *matrix, int size)
{
    for (int i = 0; i < size * size; i++)
    {
        matrix[i] = rand() % 100;
    }
}

// Function to initialize the matrix with random values
void initializeResultMatrix(double *matrix, int size)
{
    for (int i = 0; i < size * size; i++)
    {
        matrix[i] = 0.0;
    }
}

int main(int argc, char *argv[])
{
    if (argc != 3)
    {
        fprintf(stderr, "Usage: %s <matrix_size> <block_size>\n", argv[0]);
        return 1;
    }

    int size = atoi(argv[1]);
    int blockSize = atoi(argv[2]);

    // Allocate memory for the matrices
    double *matrix = (double *)malloc(size * size * sizeof(double));
    double *naive_transpose = (double *)malloc(size * size * sizeof(double));
    double *optimized_transpose = (double *)malloc(size * size * sizeof(double));

    // Check if memory allocation was successful
    if (matrix == NULL || naive_transpose == NULL)
    {
        fprintf(stderr, "Memory allocation failed\n");
        return 1;
    }

    // Seed the random number generator
    srand(time(NULL));

    // Initialize the matrix with random values
    initializeMatrix(matrix, size);

    // Initialize the result matrix with zeros
    initializeResultMatrix(naive_transpose, size);

#ifdef NAIVE
    naive(matrix, naive_transpose, size);

#endif

// TASK 1A
#ifdef OPTIMIZE_TILING
    initializeResultMatrix(optimized_transpose, size);

    double naive_time = naive(matrix, naive_transpose, size);
    double tiled_time = tiled(matrix, optimized_transpose, size, blockSize);

    verify_correctness(naive_transpose, optimized_transpose, size);

    printf("The speedup obtained by blocking is %f\n", naive_time / tiled_time);

#endif

// TASK 1B
#ifdef OPTIMIZE_PREFETCH
    initializeResultMatrix(optimized_transpose, size);

    double naive_time = naive(matrix, naive_transpose, size);
    double prefetched_time = prefetched(matrix, optimized_transpose, size);

    verify_correctness(naive_transpose, optimized_transpose, size);

    printf("The speedup obtained by software prefetching is %f\n", naive_time / prefetched_time);

#endif

// TASK 1C
#ifdef OPTIMIZE_TILING_PREFETCH
    initializeResultMatrix(optimized_transpose, size);

    double naive_time = naive(matrix, naive_transpose, size);
    double prefetched_time = tiled_prefetched(matrix, optimized_transpose, size, blockSize);

    verify_correctness(naive_transpose, optimized_transpose, size);

    printf("The speedup obtained by software prefetching is %f\n", naive_time / prefetched_time);

#endif

    // Free the allocated memory
    free(matrix);
    free(naive_transpose);
    free(optimized_transpose);

    return 0;
}
