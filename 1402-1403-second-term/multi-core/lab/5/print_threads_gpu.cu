#include <stdio.h>
#include <cuda_runtime.h>

__global__ void ThreadDetails(int *block, int *warp, int *local_index) {
    int block_id = blockIdx.x;
    int thread_id = threadIdx.x;
    int thread = block_id * blockDim.x + thread_id;
    int warp_id = thread_id / warpSize;

    block[thread] = block_id;
    warp[thread] = warp_id;
    local_index[thread] = thread_id;
}

int main(int argc, char **argv) {
    int size = 64 * 2;

    int *h_block = (int *)malloc(size * sizeof(int));
    int *h_warp = (int *)malloc(size * sizeof(int));
    int *h_local_index = (int *)malloc(size * sizeof(int));

    int *d_block, *d_warp, *d_local_index;
    cudaMalloc((void **)&d_block, size * sizeof(int));
    cudaMalloc((void **)&d_warp, size * sizeof(int));
    cudaMalloc((void **)&d_local_index, size * sizeof(int));

    ThreadDetails<<<2, 64>>>(d_block, d_warp, d_local_index);
    cudaDeviceSynchronize();

    cudaMemcpy(h_block, d_block, size * sizeof(int), cudaMemcpyDeviceToHost);
    cudaMemcpy(h_warp, d_warp, size * sizeof(int), cudaMemcpyDeviceToHost);
    cudaMemcpy(h_local_index, d_local_index, size * sizeof(int), cudaMemcpyDeviceToHost);

    for (int i = 0; i < size; i++) {
        printf("Calculated Thread: %d,\tBlock: %d,\tWarp %d,\tThread %d\n", i, h_block[i], h_warp[i], h_local_index[i]);
    }

    free(h_block);
    free(h_warp);
    free(h_local_index);
    cudaFree(d_block);
    cudaFree(d_warp);
    cudaFree(d_local_index);

    return 0;
}
