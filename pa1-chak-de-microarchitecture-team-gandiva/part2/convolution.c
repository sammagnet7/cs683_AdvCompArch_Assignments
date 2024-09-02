#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <immintrin.h>                     // For SIMD intrinsics
const int LINE_SIZE = 64;                  // 64 Byte L1-D cache line
const int LLC_size = 3 * 1024 * 1024 * 10; // 3 MB LLC cache

int source_tile_size = 64; // Source tile size is input by user, Default 64

void naive_convolution(double *input_image, double *output_image, double *kernel, int dim, int output_dim, int kernel_size);
void tiled_convolution(double *input_image, double *output_image, double *kernel, int dim, int output_dim, int kernel_size);
void simd_convolution(double *input_image, double *output_image, double *kernel, int dim, int output_dim, int kernel_size);
void prefetch_convolution(double *input_image, double *output_image, double *kernel, int dim, int output_dim, int kernel_size);

void tiled_simd_convolution(double *input_image, double *output_image, double *kernel, int dim, int output_dim, int kernel_size);
void simd_prefetch_convolution(double *input_image, double *output_image, double *kernel, int dim, int output_dim, int kernel_size);
void tiled_prefetch_convolution(double *input_image, double *output_image, double *kernel, int dim, int output_dim, int kernel_size);
void simd_tiled_prefetch_convolution(double *input_image, double *output_image, double *kernel, int dim, int output_dim, int kernel_size);

/**
 * @brief 		Generates random numbers between values fMin and fMax.
 * @param 		fMin 	lower range
 * @param 		fMax 	upper range
 * @return 		random floating point number
 */
double fRand(double fMin, double fMax)
{

    double f = (double)rand() / RAND_MAX;
    return fMin + f * (fMax - fMin);
}

/**
 * @brief 		Initialize a matrix of given dimension with random values.
 * @param 		matrix 		pointer to the matrix
 * @param 		rows 		number of rows in the matrix
 * @param 		cols 		number of columns in the matrix
 */
void initialize_kernel(double *matrix, int rows, int cols)
{

    for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < cols; j++)
        {
            matrix[i * cols + j] = ceil(fRand(0.0001, 1.0000)); // random values between 0 and 1
        }
    }
}

/**
 * @brief 		Initialize a matrix of given dimension with random values.
 * @param 		matrix 		pointer to the matrix
 * @param 		rows 		number of rows in the matrix
 * @param 		cols 		number of columns in the matrix
 */
void initialize_matrix(double *matrix, int rows, int cols)
{

    for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < cols; j++)
        {
            matrix[i * cols + j] = fRand(0.0001, 1.0000); // random values between 0 and 1
        }
    }
}

/**
 * @brief 		Initialize result matrix of given dimension with 0.
 * @param 		matrix 		pointer to the matrix
 * @param 		rows 		number of rows in the matrix
 * @param 		cols 		number of columns in the matrix
 */
void initialize_result_matrix(double *matrix, int rows, int cols)
{

    for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < cols; j++)
        {
            matrix[i * cols + j] = 0.0;
        }
    }
}

/**
 * @brief 		Compare if two matrices of same dimension are identical
 * @param 		C 		first matrix to compare
 * @param 		D 		second matrix to compare
 * @param 		dim 	dimension of the matrices
 */
void verify_correctness(double *C, double *D, int dim)
{
    double epsilon = 1e-9;
    for (int i = 0; i < dim; i++)
    {
        for (int j = 0; j < dim; j++)
        {
            if (fabs(C[i * dim + j] - D[i * dim + j]) > epsilon)
            {
                printf("%f & %f at location (%d %d)\n", C[i * dim + j], D[i * dim + j], i, j);
                printf("Matrix convolution is incorrect!\n");
                return;
            }
        }
    }
    printf("Matrix convolution is correct!\n");
    return;
}

double measure_execution_time(void (*func)(double *, double *, double *, int, int, int), double *input_image, double *output_image, double *kernel, int dim, int output_dim, int kernel_size);

int main(int argc, char **argv)
{
    if (argc <= 3)
    {
        printf("Usage: matrix-dimension kernel-size tile-size\n\n");
        return 0;
    }

    int dim = atoi(argv[1]);
    int kernel_size = atoi(argv[2]);
    source_tile_size = atoi(argv[3]);
    int output_dim = dim - kernel_size + 1;

    if(kernel_size % 8 != 0) {
        printf("Provide Kernel size in multiple of 8\n");
        return 0;
    }

    // Allocate memory for the input and output images
    double *input_image = (double *)malloc(dim * dim * sizeof(double));
    double *output_image = (double *)malloc(output_dim * output_dim * sizeof(double));
    double *kernel = (double *)malloc(kernel_size * kernel_size * sizeof(double));
    double *optimized_op = (double *)malloc(output_dim * output_dim * sizeof(double));

    // Initialize the input image and kernel
    initialize_matrix(input_image, dim, dim);

    // Initialize the kernel
    initialize_kernel(kernel, kernel_size, kernel_size);

    // Initialize the output image
    initialize_result_matrix(output_image, output_dim, output_dim);

    // Measure execution time and perform naive convolution
    double naive_time = measure_execution_time(naive_convolution, input_image, output_image, kernel, dim, output_dim, kernel_size);

    // Print the execution times and speedups
     printf("Naive Convolution Time: %f seconds\n", naive_time);

// Measure execution time and perform tiled convolution
#ifdef OPTIMIZE_TILING

    // initialize_result_matrix(optimized_op, output_dim, output_dim);

    double tiled_time = measure_execution_time(tiled_convolution, input_image, optimized_op, kernel, dim, output_dim, kernel_size);
    double tiled_speedup = naive_time / tiled_time;
    printf("Tiled Convolution Time: %f seconds, Speedup: %fx\n", tiled_time, tiled_speedup);


    verify_correctness(output_image, optimized_op, output_dim);

#endif

// Measure execution time and perform SIMD convolution
#ifdef OPTIMIZE_SIMD

    initialize_result_matrix(optimized_op, output_dim, output_dim);

    double simd_time = measure_execution_time(simd_convolution, input_image, optimized_op, kernel, dim, output_dim, kernel_size);
    double simd_speedup = naive_time / simd_time;

    printf("SIMD Convolution Time: %f seconds, Speedup: %fx\n", simd_time, simd_speedup);
    verify_correctness(output_image, optimized_op, output_dim);

#endif

// Measure execution time and perform prefetch convolution
#ifdef OPTIMIZE_PREFETCH

    initialize_result_matrix(optimized_op, output_dim, output_dim);

    double prefetch_time = measure_execution_time(prefetch_convolution, input_image, optimized_op, kernel, dim, output_dim, kernel_size);
    double prefetch_speedup = naive_time / prefetch_time;
    printf("Prefetch Convolution Time: %f seconds, Speedup: %fx\n", prefetch_time, prefetch_speedup);

    verify_correctness(output_image, optimized_op, output_dim);

#endif

#ifdef OPTIMIZE_TILING_SIMD
    initialize_result_matrix(optimized_op, output_dim, output_dim);

    // Measure execution time and perform tiled SIMD convolution
    double tiled_simd_time = measure_execution_time(tiled_simd_convolution, input_image, optimized_op, kernel, dim, output_dim, kernel_size);
    double tiled_simd_speedup = naive_time / tiled_simd_time;
    printf("Tiled SIMD Convolution Time: %f seconds, Speedup: %fx\n", tiled_simd_time, tiled_simd_speedup);

    verify_correctness(output_image, optimized_op, output_dim);

#endif

// Measure execution time and perform SIMD prefetch convolution
#ifdef OPTIMIZE_SIMD_PREFETCH
    initialize_result_matrix(optimized_op, output_dim, output_dim);

    double simd_prefetch_time = measure_execution_time(simd_prefetch_convolution, input_image, optimized_op, kernel, dim, output_dim, kernel_size);
    double simd_prefetch_speedup = naive_time / simd_prefetch_time;
    printf("SIMD Prefetch Convolution Time: %f seconds, Speedup: %fx\n", simd_prefetch_time, simd_prefetch_speedup);

    verify_correctness(output_image, optimized_op, output_dim);

#endif

// Measure execution time and perform tiled prefetch convolution
#ifdef OPTIMIZE_TILING_PREFETCH
    initialize_result_matrix(optimized_op, output_dim, output_dim);

    double tiled_prefetch_time = measure_execution_time(tiled_prefetch_convolution, input_image, optimized_op, kernel, dim, output_dim, kernel_size);
    double tiled_prefetch_speedup = naive_time / tiled_prefetch_time;
    printf("Tiled Prefetch Convolution Time: %f seconds, Speedup: %fx\n", tiled_prefetch_time, tiled_prefetch_speedup);

    verify_correctness(output_image, optimized_op, output_dim);

#endif

// Measure execution time and perform SIMD tiled prefetch convolution
#ifdef OPTIMIZE_TILING_SIMD_PREFETCH
    initialize_result_matrix(optimized_op, output_dim, output_dim);

    double simd_tiled_prefetch_time = measure_execution_time(simd_tiled_prefetch_convolution, input_image, optimized_op, kernel, dim, output_dim, kernel_size);
    double simd_tiled_prefetch_speedup = naive_time / simd_tiled_prefetch_time;
    printf("SIMD Tiled Prefetch Convolution Time: %f seconds, Speedup: %fx\n", simd_tiled_prefetch_time, simd_tiled_prefetch_speedup);

    verify_correctness(output_image, optimized_op, output_dim);

#endif

    // Free allocated memory
    free(input_image);
    free(output_image);
    free(optimized_op);

    return 0;
}

// Naive convolution implementation
void naive_convolution(double *input_image, double *output_image, double *kernel, int dim, int output_dim, int kernel_size)
{
    for (int i = 0; i < output_dim; i++) // ith output row is completed after each iteration
    {
        for (int j = 0; j < output_dim; j++) // Finalises the jth item value in ith row after each iteration
        {
            double sum = 0.0;
            for (int ki = 0; ki < kernel_size; ki++) // Kernel rows
            {
                for (int kj = 0; kj < kernel_size; kj++) // Kernel cols
                {
                    int x = i + ki;
                    int y = j + kj;
                    sum += input_image[x * dim + y] * kernel[ki * kernel_size + kj];
                }
            }
            output_image[i * output_dim + j] = sum;
        }
    }
}

// Tiled convolution implementation
void tiled_convolution(double *input_image, double *output_image, double *kernel, int dim, int output_dim, int kernel_size)
{
    // Students need to implement this

    int output_tile_size  = source_tile_size - kernel_size + 1; // adjusting destination tile size accroding to the source_tile_size
    input_image = (double *)__builtin_assume_aligned(input_image, LINE_SIZE);
    output_image = (double *)__builtin_assume_aligned(output_image, LINE_SIZE);

    for (int i = 0; i < output_dim; i += output_tile_size)
    {
        for (int j = 0; j < output_dim; j += output_tile_size)
        {
            // Iterate over the tile
            for (int ii = i; ii < i + output_tile_size && ii < output_dim; ii++)
            {
                for (int jj = j; jj < j + output_tile_size && jj < output_dim; jj++)
                {
                    double sum = 0.0;

                    // Perform convolution on the tile
                    for (int ki = 0; ki < kernel_size; ki++)
                    {
                        for (int kj = 0; kj < kernel_size; kj++)
                        {
                            int x = ii + ki;
                            int y = jj + kj;
                            sum += input_image[x * dim + y] * kernel[ki * kernel_size + kj];
                        }
                    }

                    output_image[ii * output_dim + jj] = sum;
                }
            }
        }
    }
}

// SIMD convolution implementation
void simd_convolution(double *input_image, double *output_image, double *kernel, int dim, int output_dim, int kernel_size)
{
    double temp[4];
    int remainder = kernel_size % 4;
    int simd_width = kernel_size - remainder;

    for (int i = 0; i < output_dim; i++)
    {
        for (int j = 0; j < output_dim; j++)
        {
            __m256d sum = _mm256_setzero_pd();
            double scalar_sum = 0;

            for (int ki = 0; ki < kernel_size; ki++)
            {
                int x = i + ki;

                for (int kj = 0; kj < simd_width; kj += 4)
                { // Process 4 elements at a time
                    int y = j + kj;

                    // Load 4 pixels from the input image
                    __m256d input_vec = _mm256_loadu_pd(&input_image[x * dim + y]);

                    // Load 4 kernel values
                    __m256d kernel_vec = _mm256_loadu_pd(&kernel[ki * kernel_size + kj]);

                    // Multiply and accumulate
                    __m256d result_vec = _mm256_mul_pd(input_vec, kernel_vec);

                    // Horizontal sum to get the scalar result
                    // sum += _mm256_reduce_add_pd(result_vec);
                    sum = _mm256_add_pd(result_vec, sum);
                }
                for (int kj = simd_width; kj < kernel_size; kj++)
                {
                    int y = j + kj;
                    scalar_sum += input_image[x * dim + y] * kernel[ki * kernel_size + kj];
                }
            }
            _mm256_storeu_pd(temp, sum);
            output_image[i * output_dim + j] = temp[0] + temp[1] + temp[2] + temp[3] + scalar_sum;
        }
    }
}

// Prefetch convolution implementation
void prefetch_convolution(double *input_image, double *output_image, double *kernel, int dim, int output_dim, int kernel_size)
{
    // Students need to implement this
    int image_stride = 4;
    int kernel_stride = 4;
    input_image = (double *)__builtin_assume_aligned(input_image, LINE_SIZE);
    output_image = (double *)__builtin_assume_aligned(output_image, LINE_SIZE);

    for (int i = 0; i < output_dim; i++) // ith output row is completed after each iteration
    {
        for (int j = 0; j < output_dim; j++) // Finalises the jth item value in ith row after each iteration
        {
            double sum = 0.0;
            _mm_prefetch((char *)&input_image[(i + 7) * dim + j], _MM_HINT_T0);
            // _mm_prefetch((char *)&input_image[(i + kernel_size - 2) * dim + j], _MM_HINT_T0);
            // _mm_prefetch((char *)&input_image[(i)*dim + j + ((j / 8) + 1) * 8], _MM_HINT_T0);
            // _mm_prefetch((char *)&input_image[(i + 1) * dim + j + ((j / 8) + 1) * 8], _MM_HINT_T0);

            for (int ki = 0; ki < kernel_size; ki++) // Kernel rows
            {
                for (int kj = 0; kj < kernel_size; kj++) // Kernel cols
                {
                    int x = i + ki;
                    int y = j + kj;
                    sum += input_image[x * dim + y] * kernel[ki * kernel_size + kj];
                }
            }
            output_image[i * output_dim + j] = sum;
        }
    }
}

// Bonus Tasks
// Tiled SIMD convolution implementation
void tiled_simd_convolution(double *input_image, double *output_image, double *kernel, int dim, int output_dim, int kernel_size)
{
    int output_tile_size  = source_tile_size - kernel_size + 1; // adjusting destination tile size accroding to the source_tile_size
    int remainder = kernel_size % 4;
    int simd_width = kernel_size - remainder;
    double temp[4];

    // Align the input and output images to cache line size
    input_image = (double *)__builtin_assume_aligned(input_image, 64);
    output_image = (double *)__builtin_assume_aligned(output_image, 64);

    // Iterate over the output image in tiles
    for (int i = 0; i < output_dim; i += output_tile_size)
    {
        for (int j = 0; j < output_dim; j += output_tile_size)
        {
            // Process each tile
            for (int ii = i; ii < i + output_tile_size && ii < output_dim; ii++)
            {
                for (int jj = j; jj < j + output_tile_size && jj < output_dim; jj++)
                {
                    __m256d sum = _mm256_setzero_pd();
                    double scalar_sum = 0;

                    // Perform SIMD convolution within the tile
                    for (int ki = 0; ki < kernel_size; ki++)
                    {
                        int x = ii + ki;

                        for (int kj = 0; kj < simd_width; kj += 4)
                        { // Process 4 elements at a time
                            int y = jj + kj;

                            // Load 4 pixels from the input image
                            __m256d input_vec = _mm256_loadu_pd(&input_image[x * dim + y]);

                            // Load 4 kernel values
                            __m256d kernel_vec = _mm256_loadu_pd(&kernel[ki * kernel_size + kj]);

                            // Multiply and accumulate
                            __m256d result_vec = _mm256_mul_pd(input_vec, kernel_vec);
                            sum = _mm256_add_pd(result_vec, sum);
                        }

                        // Handle the remainder part that cannot be processed by SIMD
                        for (int kj = simd_width; kj < kernel_size; kj++)
                        {
                            int y = jj + kj;
                            scalar_sum += input_image[x * dim + y] * kernel[ki * kernel_size + kj];
                        }
                    }

                    _mm256_storeu_pd(temp, sum);
                    output_image[ii * output_dim + jj] = temp[0] + temp[1] + temp[2] + temp[3] + scalar_sum;
                }
            }
        }
    }
}

// SIMD prefetch convolution implementation
void simd_prefetch_convolution(double *input_image, double *output_image, double *kernel, int dim, int output_dim, int kernel_size)
{
    double temp[4];
    int remainder = kernel_size % 4;
    int simd_width = kernel_size - remainder;

    for (int i = 0; i < output_dim; i++)
    {
        for (int j = 0; j < output_dim; j++)
        {
            __m256d sum = _mm256_setzero_pd();
            double scalar_sum = 0;

            for (int ki = 0; ki < kernel_size; ki++)
            {
                int x = i + ki;
                _mm_prefetch((char *)&input_image[(i)*dim + j + ((j / 8) + 1) * 8], _MM_HINT_T0);
                _mm_prefetch((char *)&input_image[(i + 1) * dim + j + ((j / 8) + 1) * 8], _MM_HINT_T0);

                for (int kj = 0; kj < simd_width; kj += 4)
                { // Process 4 elements at a time
                    int y = j + kj;

                    // Load 4 pixels from the input image
                    __m256d input_vec = _mm256_loadu_pd(&input_image[x * dim + y]);

                    // Load 4 kernel values
                    __m256d kernel_vec = _mm256_loadu_pd(&kernel[ki * kernel_size + kj]);

                    // Multiply and accumulate
                    __m256d result_vec = _mm256_mul_pd(input_vec, kernel_vec);

                    // Horizontal sum to get the scalar result
                    // sum += _mm256_reduce_add_pd(result_vec);
                    sum = _mm256_add_pd(result_vec, sum);
                }
                for (int kj = simd_width; kj < kernel_size; kj++)
                {
                    int y = j + kj;
                    scalar_sum += input_image[x * dim + y] * kernel[ki * kernel_size + kj];
                }
            }
            _mm256_storeu_pd(temp, sum);
            output_image[i * output_dim + j] = temp[0] + temp[1] + temp[2] + temp[3] + scalar_sum;
        }
    }
}

// Tiled prefetch convolution implementation
void tiled_prefetch_convolution(double *input_image, double *output_image, double *kernel, int dim, int output_dim, int kernel_size)
{
    // Students need to implement this
    int output_tile_size  = source_tile_size - kernel_size + 1; // adjusting destination tile size accroding to the source_tile_size
    input_image = (double *)__builtin_assume_aligned(input_image, LINE_SIZE);
    output_image = (double *)__builtin_assume_aligned(output_image, LINE_SIZE);

    for (int i = 0; i < output_dim; i += output_tile_size)
    {
        for (int j = 0; j < output_dim; j += output_tile_size)
        {
            // Iterate over the tile
            for (int ii = i; ii < i + output_tile_size && ii < output_dim; ii++)
            {
                for (int jj = j; jj < j + output_tile_size && jj < output_dim; jj++)
                {
                    double sum = 0.0;
                    _mm_prefetch((const char *)&input_image[(ii + 4) * dim + jj], _MM_HINT_T1);
                    _mm_prefetch((const char *)&input_image[(ii + 5) * dim + jj], _MM_HINT_T1);
                    _mm_prefetch((const char *)&input_image[(ii + 6) * dim + jj], _MM_HINT_T1);
                    _mm_prefetch((const char *)&input_image[(ii + 7) * dim + jj], _MM_HINT_T1);
                    // Perform convolution on the tile
                    for (int ki = 0; ki < kernel_size; ki++)
                    {
                        for (int kj = 0; kj < kernel_size; kj++)
                        {
                            int x = ii + ki;
                            int y = jj + kj;
                            sum += input_image[x * dim + y] * kernel[ki * kernel_size + kj];
                        }
                    }

                    output_image[ii * output_dim + jj] = sum;
                }
            }
        }
    }
}

// SIMD tiled prefetch convolution implementation

void simd_tiled_prefetch_convolution(double *input_image, double *output_image, double *kernel, int dim, int output_dim, int kernel_size)
{
    int output_tile_size  = source_tile_size - kernel_size + 1; // adjusting destination tile size accroding to the source_tile_size
    int remainder = kernel_size % 4;
    int simd_width = kernel_size - remainder;
    double temp[4];

    // Align the input and output images to cache line size
    input_image = (double *)__builtin_assume_aligned(input_image, 64);
    output_image = (double *)__builtin_assume_aligned(output_image, 64);

    // Iterate over the output image in tiles
    for (int i = 0; i < output_dim; i += output_tile_size)
    {
        for (int j = 0; j < output_dim; j += output_tile_size)
        {
            // Process each tile
            for (int ii = i; ii < i + output_tile_size && ii < output_dim; ii++)
            {
                for (int jj = j; jj < j + output_tile_size && jj < output_dim; jj++)
                {
                    __m256d sum = _mm256_setzero_pd();
                    double scalar_sum = 0;

                    // Perform SIMD convolution within the tile
                    for (int ki = 0; ki < kernel_size; ki++)
                    {
                        int x = ii + ki;

                        _mm_prefetch((char *)&input_image[(x)*dim + ((jj + 24) & (dim - 1))], _MM_HINT_T0);

                        for (int kj = 0; kj < simd_width / 2; kj += 8)
                        { // Process 4 elements at a time
                            int y = jj + kj;

                            // Load 4 pixels from the input image
                            __m256d input_vec1 = _mm256_loadu_pd(&input_image[x * dim + y]);

                            // Load 4 kernel values
                            __m256d kernel_vec1 = _mm256_loadu_pd(&kernel[ki * kernel_size + kj]);

                            // Multiply and accumulate
                            __m256d result_vec1 = _mm256_mul_pd(input_vec1, kernel_vec1);
                            sum = _mm256_add_pd(result_vec1, sum);

                            // Unroll 2
                            __m256d input_vec2 = _mm256_loadu_pd(&input_image[x * dim + y + 4]);
                            __m256d kernel_vec2 = _mm256_loadu_pd(&kernel[ki * kernel_size + kj + 4]);
                            __m256d result_vec2 = _mm256_mul_pd(input_vec2, kernel_vec2);
                            sum = _mm256_add_pd(result_vec2, sum);
                        }

                        // Handle the remainder part that cannot be processed by SIMD
                        for (int kj = simd_width; kj < kernel_size; kj++)
                        {
                            int y = jj + kj;
                            scalar_sum += input_image[x * dim + y] * kernel[ki * kernel_size + kj];
                        }
                    }

                    _mm256_storeu_pd(temp, sum);
                    output_image[ii * output_dim + jj] = temp[0] + temp[1] + temp[2] + temp[3] + scalar_sum;
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
        _mm_clflush(&buffer[i]);
    }

    free(buffer);
}
// Function to measure execution time of a convolution function
double measure_execution_time(void (*func)(double *, double *, double *, int, int, int), double *input_image, double *output_image, double *kernel, int dim, int output_dim, int kernel_size)
{
    flushCache();
    clock_t start, end;
    start = clock();
    func(input_image, output_image, kernel, dim, output_dim, kernel_size);
    end = clock();
    return (double)(end - start) / CLOCKS_PER_SEC;
}