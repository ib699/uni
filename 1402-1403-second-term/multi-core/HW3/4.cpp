#include <omp.h> // Include OpenMP header

void conv_pool(int** mat, int** kernel, int N){
 int sum;
 // Parallelize the outer loop with OpenMP
 #pragma omp parallel for private(sum) collapse(2)
 for (int i = 1; i < N-1; i++){
 for (int j = 1; j < N-1; j++) {
 sum = 0;
 for (int k = -1; k < 2; k++)
 for (int l = -1; l < 2; l++)
 sum += mat[i+k][j+l]; // Missing semicolon in original code
 mat[i-1][j-1] = sum;
 }
 }

 // Parallelize the pooling part
 #pragma omp parallel for collapse(2)
 for (int i = 0; i < N-2; i+=2){
 for (int j = 0; j < N-2; j+=2) {
 // Assuming 'a' is meant to be 'mat' as 'a' is not defined
 mat[i/2][j/2] = (mat[i][j] + mat[i+1][j] + mat[i][j+1] + mat[i+1][j+1]) / 4;
 }
 }

 // The resize operation is not parallelized as it is a sequential step
 // equivalent operation: mat = mat[0:(N-2)/2][0:(N-2)/2]
 resize_mat(mat, 0, (N-2)/2, 0, (N-2)/2);

 return;
}