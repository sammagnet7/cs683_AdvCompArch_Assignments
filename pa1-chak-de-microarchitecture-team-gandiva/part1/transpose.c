#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>


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
void naiveMatrixTranspose(double *matrix, double *transpose, int size) {
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            transpose[j * size + i] = matrix[i * size + j];
        }
    }
}

// Cache-Aware tiled Matrix Transpose
void tiledMatrixTranspose(double *matrix, double *transpose, int size, int blockSize) {
    // Students need to implement this function
}


// Prefetch Matrix Transpose
void prefetchMatrixTranspose(double *matrix, double *transpose, int size) {
    // Students need to implement this function
}


// Tiled Prefetch Matrix Transpose
void tiledPrefetchedMatrixTranspose(double *matrix, double *transpose, int size) {
    // Students need to implement this function
}



double naive(double * matrix, double *transpose, int size) {
    // Run and time the naive matrix transpose
    clock_t start = clock();
    naiveMatrixTranspose(matrix, transpose, size);

    clock_t end = clock();
    double time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("Time taken by naive matrix transpose: %f seconds\n", time_taken);

    return time_taken;
}



double tiled(double * matrix, double *transpose, int size, int blockSize) {
    // Run and time the tiled matrix transpose
    clock_t start = clock();
    tiledMatrixTranspose(matrix, transpose, size, blockSize);
    clock_t end = clock();
    double time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("Time taken by tiled matrix transpose: %f seconds\n", time_taken);

    return time_taken;
}


double prefetched(double * matrix, double *transpose, int size) {
    // Run and time the prefetch matrix transpose
    clock_t start = clock();
    prefetchMatrixTranspose(matrix, transpose, size);
    clock_t end = clock();
    double time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("Time taken by prefetch matrix transpose: %f seconds\n", time_taken);

    return time_taken;
}


double tiled_prefetched(double * matrix, double *transpose, int size) {
    // Run and time the prefetch matrix transpose
    clock_t start = clock();
    tiledPrefetchedMatrixTranspose(matrix, transpose, size);
    clock_t end = clock();
    double time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("Time taken by tiled prefetch matrix transpose: %f seconds\n", time_taken);

    return time_taken;
}


// Function to initialize the matrix with random values
void initializeMatrix(double *matrix, int size) {
    for (int i = 0; i < size * size; i++) {
        matrix[i] = rand() % 100;
    }
}


// Function to initialize the matrix with random values
void initializeResultMatrix(double *matrix, int size) {
    for (int i = 0; i < size * size; i++) {
        matrix[i] = 0.0;
    }
}


int main(int argc, char *argv[]) {
    if (argc != 3) {
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
    if (matrix == NULL || naive_transpose == NULL) {
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
    naive(matrix, transpose, size);

#endif


// TASK 1A
#ifdef OPTIMIZE_TILING
    initializeResultMatrix(optimized_transpose, size);    
    
    double naive_time = naive(matrix, naive_transpose, size);
    double tiled_time = tiled(matrix, optimized_transpose, size, blockSize);

    verify_correctness(naive_transpose, optimized_transpose, size);

    printf("The speedup obtained by blocking is %f\n", naive_time/tiled_time);

#endif


// TASK 1B
#ifdef OPTIMIZE_PREFETCH
    initializeResultMatrix(optimized_transpose, size);
    
    
    double naive_time = naive(matrix, naive_transpose, size);
    double prefetched_time = prefetched(matrix, optimized_transpose, size);
    
    verify_correctness(naive_transpose, optimized_transpose, size);

    printf("The speedup obtained by software prefetching is %f\n", naive_time/prefetched_time);
    

#endif


// TASK 1C
#ifdef OPTIMIZE_TILING_PREFETCH
    initializeResultMatrix(optimized_transpose, size);
    
    
    double naive_time = naive(matrix, naive_transpose, size);
    double prefetched_time = tiled_prefetched(matrix, optimized_transpose, size);
    
    verify_correctness(naive_transpose, optimized_transpose, size);

    printf("The speedup obtained by software prefetching is %f\n", naive_time/prefetched_time);
    

#endif

    // Free the allocated memory
    free(matrix);
    free(naive_transpose);
    free(optimized_transpose);

    return 0;
}
