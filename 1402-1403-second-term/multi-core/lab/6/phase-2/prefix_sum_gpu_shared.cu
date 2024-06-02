#define _CRT_SECURE_NO_WARNINGS

#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <cuda_runtime.h>

void fill_array(int *a, size_t n);
void print_array(int *a, size_t n);
__global__ void prefix_sum_hillis_steele(int *data, int *block_sums, int n);
__global__ void add_block_sums(int *data, int *block_sums, int n);

int main(int argc, char *argv[]) {
    // Input N
    size_t n = 0;
    printf("[-] Please enter N: ");
    scanf("%zu", &n);

    clock_t tStart = clock();
    // Allocate memory for array on host
    int *h_a = (int *)malloc(n * sizeof(int));
    // Fill array with numbers 1..n
    fill_array(h_a, n);

    // Allocate memory for array on device
    int *d_a, *d_block_sums;
    int blockSize = 256;
    int gridSize = (n + blockSize - 1) / blockSize;

    cudaMalloc((void**)&d_a, n * sizeof(int));
    cudaMalloc((void**)&d_block_sums, gridSize * sizeof(int));

    // Copy array from host to device
    cudaMemcpy(d_a, h_a, n * sizeof(int), cudaMemcpyHostToDevice);

    // Launch kernel for block-level scan
    prefix_sum_hillis_steele<<<gridSize, blockSize>>>(d_a, d_block_sums, n);

    if (gridSize > 1) {
        prefix_sum_hillis_steele<<<1, blockSize>>>(d_block_sums, NULL, gridSize);
        add_block_sums<<<gridSize, blockSize>>>(d_a, d_block_sums, n);
    }

    // Copy result back to host
    cudaMemcpy(h_a, d_a, n * sizeof(int), cudaMemcpyDeviceToHost);

    // Print array
    // print_array(h_a, n);

    // Free allocated memory
    free(h_a);
    cudaFree(d_a);
    cudaFree(d_block_sums);

    printf("Elapsed time in sec %lf", (double)(clock() - tStart) / CLOCKS_PER_SEC);
    return EXIT_SUCCESS;
}

__global__ void prefix_sum_hillis_steele(int *data, int *block_sums, int n) {
    __shared__ int temp[256];
    int tid = threadIdx.x;
    int gid = threadIdx.x + blockIdx.x * blockDim.x;

    if (gid < n) {
        temp[tid] = data[gid];
    } else {
        temp[tid] = 0;
    }
    __syncthreads();

    int offset = 1;
    while (offset < blockDim.x) {
        int t = 0;
        if (tid >= offset) {
            t = temp[tid - offset];
        }
        __syncthreads();
        if (tid >= offset) {
            temp[tid] += t;
        }
        __syncthreads();
        offset *= 2;
    }

    if (gid < n) {
        data[gid] = temp[tid];
    }

    if (block_sums != NULL && tid == blockDim.x - 1) {
        block_sums[blockIdx.x] = temp[tid];
    }
}

__global__ void add_block_sums(int *data, int *block_sums, int n) {
    int gid = threadIdx.x + blockIdx.x * blockDim.x;

    if (blockIdx.x > 0 && gid < n) {
        data[gid] += block_sums[blockIdx.x - 1];
    }
}

void fill_array(int *a, size_t n) {
    int i;
    for (i = 0; i < n; ++i) {
        a[i] = i + 1;
    }
}

void print_array(int *a, size_t n) {
    int i;
    printf("[-] array: ");
    for (i = 0; i < n; ++i) {
        printf("%d, ", a[i]);
    }
    printf("\b\b \n");
}

