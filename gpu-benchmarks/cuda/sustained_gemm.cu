//
// sustained_gemm.cu
// Keeps the GPU busy for several seconds by looping SGEMM many times,
// so that power/utilization sampling tools can actually observe load.
//

#include <stdio.h>
#include <stdlib.h>
#include <cuda_runtime.h>
#include <cublas_v2.h>

int main(int argc, char **argv) {
  int n = 4096;
  int num_reps = 2000;

  if (argc > 1) n = atoi(argv[1]);
  if (argc > 2) num_reps = atoi(argv[2]);

  printf("Sustained SGEMM: n=%d, num_reps=%d\n", n, num_reps);

  cublasHandle_t handle;
  cublasCreate(&handle);

  size_t bytes = (size_t)n*n*sizeof(float);
  float *h_A = (float*)malloc(bytes);
  float *h_B = (float*)malloc(bytes);
  for (int i = 0; i < n*n; i++) {
    h_A[i] = (float)(rand()%100)/100.0f;
    h_B[i] = (float)(rand()%100)/100.0f;
  }

  float *d_A, *d_B, *d_C;
  cudaMalloc(&d_A, bytes);
  cudaMalloc(&d_B, bytes);
  cudaMalloc(&d_C, bytes);
  cudaMemcpy(d_A, h_A, bytes, cudaMemcpyHostToDevice);
  cudaMemcpy(d_B, h_B, bytes, cudaMemcpyHostToDevice);

  float alpha = 1.0f, beta = 0.0f;

  cudaEvent_t start, stop;
  cudaEventCreate(&start);
  cudaEventCreate(&stop);

  cudaEventRecord(start);
  for (int r = 0; r < num_reps; r++) {
    cublasSgemm(handle, CUBLAS_OP_N, CUBLAS_OP_N, n, n, n,
                &alpha, d_A, n, d_B, n, &beta, d_C, n);
  }
  cudaEventRecord(stop);
  cudaEventSynchronize(stop);

  float ms;
  cudaEventElapsedTime(&ms, start, stop);

  double flops = 2.0 * (double)n * (double)n * (double)n * num_reps;
  double gflops = flops / (ms/1000.0) / 1e9;

  printf("Total time: %.3f ms, avg GFLOPS: %.1f\n", ms, gflops);

  cudaFree(d_A); cudaFree(d_B); cudaFree(d_C);
  free(h_A); free(h_B);
  cublasDestroy(handle);

  return 0;
}
