/*
*				In His Exalted Name
*	Title:	Prefix Sum Sequential Code
*	Author: Ahmad Siavashi, Email: siavashi@aut.ac.ir
*	Date:	29/04/2018
*/

// Let it be.
#define _CRT_SECURE_NO_WARNINGS

#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <math.h>

#include <cuda_runtime.h>
#include <device_launch_parameters.h>

#define batch_size 64
#define BLOCK_SIZE 1024

typedef long long int ll;

void fill_array(ll *a, size_t n);
void prefix_sum(ll *a, size_t n);
void print_array(ll *a, size_t n);
cudaError_t prefix_sum_gpu(ll *a, size_t n);

__global__ void prefix_thread(ll *dev_a, ll *dev_b, size_t n){
	int i, j;
	i = blockIdx.x * blockDim.x + threadIdx.x;
	int start = i * batch_size, end = (i+1) * batch_size;
	for(j = start + 1; j < end && j < n; j++)
		dev_a[j] = dev_a[j] + dev_a[j-1];

	dev_b[i] = dev_a[j-1];
}

__global__ void calc_prefix(ll *dev_b, int num_threads){
	int j;
	for(j = 1; j < num_threads; j++)
		dev_b[j] = dev_b[j] + dev_b[j-1];
}

__global__ void add_prefix(ll *dev_a, ll *dev_b, size_t n){
	int i, j;
	i = blockIdx.x * blockDim.x + threadIdx.x + 1;
	int start = i * batch_size, end = (i+1) * batch_size;
	for(j = start; j < end && j < n; j++)
		dev_a[j] = dev_a[j] + dev_b[i-1];
}

int main(int argc, char *argv[]) {
	// Input N
	size_t n = 0;
	printf("[-] Please enter N: ");
	scanf("%uld\n", &n);

	// Allocate memory for array
	ll * a = (ll *)malloc(n * sizeof(ll));
	// Fill array with numbers 1..n
	fill_array(a, n);
	// Print array
	// print_array(a, n);
	// Compute prefix sum

	// prefix_sum(a, n);

	clock_t tStart = clock();
	prefix_sum_gpu(a, n);
	printf("Elapsed time in sec %lf\n", (double)(clock() - tStart)/CLOCKS_PER_SEC);

	// Print array
	// print_array(a, n);

	if(a[n-1] != (n*(n+1)/2))
		printf("oops! result is wrong!\n");

	// Free allocated memory
	free(a);
	return EXIT_SUCCESS;
}

cudaError_t prefix_sum_gpu(ll *a, size_t n) {
	ll *dev_a, *dev_b;
	int num_threads = ceil(n / batch_size);
	cudaError_t cudaStatus;

	if(num_threads % BLOCK_SIZE != 0){
		printf("num_threads is not dividable by BLOCK_SIZE...");
		return cudaStatus;
	}

	cudaStatus = cudaSetDevice(0);
	if(cudaStatus != cudaSuccess) printf("CUDA Device failed!");
	
	cudaStatus = cudaMalloc((void**)&dev_a, n * sizeof(ll));
	if(cudaStatus != cudaSuccess) printf("CudaMalloc failed for a!");
	
	cudaStatus = cudaMalloc((void**)&dev_b, num_threads * sizeof(ll));
	if(cudaStatus != cudaSuccess) printf("CudaMalloc failed for b!");

	cudaStatus = cudaMemcpy(dev_a, a, n * sizeof(ll), cudaMemcpyHostToDevice);
	if(cudaStatus != cudaSuccess) printf("CudaMallocHostToDevice failed for a!");

	////////

	prefix_thread<<<num_threads/BLOCK_SIZE, BLOCK_SIZE>>>(dev_a, dev_b, n);

    cudaStatus = cudaGetLastError();
    if(cudaStatus != cudaSuccess) printf("prefix_thread failed: %s\n", cudaGetErrorString(cudaStatus));

    cudaStatus = cudaDeviceSynchronize();
    if(cudaStatus != cudaSuccess) printf("prefix_thread sync failed: %s\n", cudaGetErrorString(cudaStatus));

	////////

	calc_prefix<<<1, 1>>>(dev_b, num_threads);

    cudaStatus = cudaGetLastError();
    if(cudaStatus != cudaSuccess) printf("calc_prefix failed: %s\n", cudaGetErrorString(cudaStatus));

    cudaStatus = cudaDeviceSynchronize();
    if(cudaStatus != cudaSuccess) printf("calc_prefix sync failed: %s\n", cudaGetErrorString(cudaStatus));

	////////

	add_prefix<<<num_threads/BLOCK_SIZE, BLOCK_SIZE>>>(dev_a, dev_b, n);

    cudaStatus = cudaGetLastError();
    if(cudaStatus != cudaSuccess) printf("add_prefix failed: %s\n", cudaGetErrorString(cudaStatus));

    cudaStatus = cudaDeviceSynchronize();
    if(cudaStatus != cudaSuccess) printf("add_prefix sync failed: %s\n", cudaGetErrorString(cudaStatus));

	///////

	cudaStatus = cudaMemcpy(a, dev_a, n * sizeof(ll), cudaMemcpyDeviceToHost);
	if(cudaStatus != cudaSuccess) printf("CudaMallocDeviceToHost failed for a!");

	cudaFree(dev_b);
	cudaFree(dev_a);

	return cudaStatus;
}

void prefix_sum(ll *a, size_t n) {
	int i;
	for (i = 1; i < n; ++i) {
		a[i] = a[i] + a[i - 1];
	}
}

void print_array(ll *a, size_t n) {
	int i;
	printf("[-] array: ");
	for (i = 0; i < n; ++i) {
		printf("%lld, ", a[i]);
	}
	printf("\b\b \n");
}

void fill_array(ll *a, size_t n) {
	int i;
	for (i = 0; i < n; ++i) {
		a[i] = i + 1;
	}
}
