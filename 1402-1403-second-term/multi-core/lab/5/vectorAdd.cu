/*
*	In His Exalted Name
*	Vector Addition - Sequential Code
*	Ahmad Siavashi, Email: siavashi@aut.ac.ir
*	21/05/2018
*/

#include <stdlib.h>
#include <stdio.h>
#include <time.h>

#include <cuda_runtime.h>
#include <device_launch_parameters.h>

#define BLOCK_SIZE 1024

// 0 -> one thread = one add
// 1 -> one thread = n add
#define MOD 0

void fillVector(int * v, size_t n);
void addVector(int * a, int *b, int *c, size_t n);
void printVector(int * v, size_t n);
cudaError_t addVectorGPU(const int* a, const int* b, int *c, size_t n, int num_blocks);

__global__ void addKernel1(int *c, const int *a, const int *b){
	int i = blockIdx.x * blockDim.x + threadIdx.x;
	c[i] = a[i] + b[i];
}

__global__ void addKernel2(int *c, const int *a, const int *b, size_t n){
	int i = threadIdx.x;
	int start = i * (n / BLOCK_SIZE), end = (i+1) * (n / BLOCK_SIZE);
	for(int j = start; j < end && j < n; j++)
		c[j] = a[j] + b[j];
}

cudaError_t addVectorGPU(const int* a, const int* b, int *c, size_t size, int num_blocks){
	int *dev_a, *dev_b, *dev_c;
	cudaError_t cudaStatus;

	cudaStatus = cudaSetDevice(0);
	if(cudaStatus != cudaSuccess) printf("CUDA Device failed!");
	
	cudaStatus = cudaMalloc((void**)&dev_c, size * sizeof(int));
	if(cudaStatus != cudaSuccess) printf("CudaMalloc failed for c!");
	
	cudaStatus = cudaMalloc((void**)&dev_a, size * sizeof(int));
	if(cudaStatus != cudaSuccess) printf("CudaMalloc failed for a!");
	
	cudaStatus = cudaMalloc((void**)&dev_b, size * sizeof(int));
	if(cudaStatus != cudaSuccess) printf("CudaMalloc failed for b!");

	cudaStatus = cudaMemcpy(dev_a, a, size * sizeof(int), cudaMemcpyHostToDevice);
	if(cudaStatus != cudaSuccess) printf("CudaMallocHostToDevice failed for a!");

	cudaStatus = cudaMemcpy(dev_b, b, size * sizeof(int), cudaMemcpyHostToDevice);
	if(cudaStatus != cudaSuccess) printf("CudaMallocHostToDevice failed for b!");

	if(MOD == 0){
		printf("Using addKernel1...\n");
		if(size % num_blocks != 0 || size/num_blocks > BLOCK_SIZE) {
			printf("size, num_blocks not valid: %d, %d\n", (int)size, num_blocks);
			return cudaStatus;
		}

		addKernel1 <<<num_blocks, size/num_blocks>>> (dev_c, dev_a, dev_b);

	} else if(MOD == 1) {
		printf("Using addKernel2...\n");
		addKernel2 <<<1, BLOCK_SIZE>>> (dev_c, dev_a, dev_b, size);
	}

    cudaStatus = cudaGetLastError();
    if(cudaStatus != cudaSuccess) printf("addKernel failed: %s\n", cudaGetErrorString(cudaStatus));

    cudaStatus = cudaDeviceSynchronize();
    if(cudaStatus != cudaSuccess) printf("addKernel sync failed: %s\n", cudaGetErrorString(cudaStatus));

	cudaStatus = cudaMemcpy(c, dev_c, size * sizeof(int), cudaMemcpyDeviceToHost);
	if(cudaStatus != cudaSuccess) printf("CudaMallocDeviceToHost failed for c!");

	cudaFree(dev_c);
	cudaFree(dev_b);
	cudaFree(dev_a);

	return cudaStatus;
}

int main()
{
	const int vectorSize = 102400, num_blocks = 100; // num_blocks is used for mod=0 only
	int a[vectorSize], b[vectorSize], c[vectorSize];
	
	fillVector(a, vectorSize);
	fillVector(b, vectorSize);
	
	// printf("Calling serial...\n\n");
	// addVector(a, b, c, vectorSize);

	//printVector(c, vectorSize);

	printf("Calling GPU...\n\n");
	addVectorGPU(a, b, c, vectorSize, num_blocks);

	printVector(c, vectorSize);


	return EXIT_SUCCESS;
}

// Fills a vector with data
void fillVector(int * v, size_t n) {
	int i;
	for (i = 0; i < n; i++) {
		v[i] = i;
	}
}

// Adds two vectors
void addVector(int * a, int *b, int *c, size_t n) {
	int i;
	for (i = 0; i < n; i++) {
		c[i] = a[i] + b[i];
	}
}

// Prints a vector to the stdout.
void printVector(int * v, size_t n) {
	int i;
	printf("[-] Vector elements: ");
	for (i = 0; i < n; i++) {
		printf("%d, ", v[i]);
	}
	printf("\b\b  \n");
}
