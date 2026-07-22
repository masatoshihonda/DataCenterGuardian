//
// gflops_bench.cu
// Automated GEMM benchmark across matrix sizes, with/without Tensor Cores (FP16)
// Outputs CSV: n, mode, time_ms, gflops
//
// Motivation: KEHAI workload fingerprinting - measure effective GFLOPS/GB/s
// so that per-job GPU/data-center placement decisions can be cost-informed.
//

#include <stdio.h>
#include <stdlib.h>
#include <cuda_runtime.h>
#include <cublas_v2.h>
#include <cuda_fp16.h>

void checkCublas(cublasStatus_t status, const char *msg) {
  if (status != CUBLAS_STATUS_SUCCESS) {
    printf("CUBLAS error: %s\n", msg);
    exit(1);
  }
}

int main() {
  int sizes[] = {32, 64, 128, 256, 512, 1024, 2048, 4096};
  int num_sizes = sizeof(sizes)/sizeof(sizes[0]);
  int num_reps = 5;

  cublasHandle_t handle;
  checkCublas(cublasCreate(&handle), "create handle");

  cudaEvent_t start, stop;
  cudaEventCreate(&start);
  cudaEventCreate(&stop);

  printf("n,mode,time_ms,gflops\n");

  for (int s = 0; s < num_sizes; s++) {
    int n = sizes[s];
    size_t bytes_f32 = (size_t)n*n*sizeof(float);
    size_t bytes_f16 = (size_t)n*n*sizeof(half);

    float *h_A = (float*)malloc(bytes_f32);
    float *h_B = (float*)malloc(bytes_f32);
    for (int i = 0; i < n*n; i++) {
      h_A[i] = (float)(rand()%100)/100.0f;
      h_B[i] = (float)(rand()%100)/100.0f;
    }

    float *d_A, *d_B, *d_C;
    cudaMalloc(&d_A, bytes_f32);
    cudaMalloc(&d_B, bytes_f32);
    cudaMalloc(&d_C, bytes_f32);
    cudaMemcpy(d_A, h_A, bytes_f32, cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, h_B, bytes_f32, cudaMemcpyHostToDevice);

    float alpha = 1.0f, beta = 0.0f;
    double flops = 2.0 * (double)n * (double)n * (double)n;

    // ---- Mode 1: FP32, no Tensor Cores ----
    checkCublas(cublasSetMathMode(handle, CUBLAS_PEDANTIC_MATH), "set math mode fp32");

    float best_ms = 1e30f;
    for (int r = 0; r < num_reps; r++) {
      cudaEventRecord(start);
      cublasSgemm(handle, CUBLAS_OP_N, CUBLAS_OP_N, n, n, n,
                  &alpha, d_A, n, d_B, n, &beta, d_C, n);
      cudaEventRecord(stop);
      cudaEventSynchronize(stop);
      float ms;
      cudaEventElapsedTime(&ms, start, stop);
      if (r > 0 && ms < best_ms) best_ms = ms;   // skip first (warm-up), keep best of rest
      if (r == 0) best_ms = ms;
    }
    double gflops_fp32 = flops / (best_ms/1000.0) / 1e9;
    printf("%d,fp32,%f,%f\n", n, best_ms, gflops_fp32);

    // ---- Mode 2: FP16 mixed precision, Tensor Cores ----
    half *h_hA = (half*)malloc(bytes_f16);
    half *h_hB = (half*)malloc(bytes_f16);
    for (int i = 0; i < n*n; i++) {
      h_hA[i] = __float2half(h_A[i]);
      h_hB[i] = __float2half(h_B[i]);
    }
    half *d_hA, *d_hB;
    cudaMalloc(&d_hA, bytes_f16);
    cudaMalloc(&d_hB, bytes_f16);
    cudaMemcpy(d_hA, h_hA, bytes_f16, cudaMemcpyHostToDevice);
    cudaMemcpy(d_hB, h_hB, bytes_f16, cudaMemcpyHostToDevice);

    checkCublas(cublasSetMathMode(handle, CUBLAS_DEFAULT_MATH), "set math mode fp16");

    best_ms = 1e30f;
    for (int r = 0; r < num_reps; r++) {
      cudaEventRecord(start);
      cublasSgemmEx(handle, CUBLAS_OP_N, CUBLAS_OP_N, n, n, n,
                    &alpha, d_hA, CUDA_R_16F, n, d_hB, CUDA_R_16F, n,
                    &beta, d_C, CUDA_R_32F, n);
      cudaEventRecord(stop);
      cudaEventSynchronize(stop);
      float ms;
      cudaEventElapsedTime(&ms, start, stop);
      if (r > 0 && ms < best_ms) best_ms = ms;
      if (r == 0) best_ms = ms;
    }
    double gflops_fp16 = flops / (best_ms/1000.0) / 1e9;
    printf("%d,fp16,%f,%f\n", n, best_ms, gflops_fp16);

    free(h_A); free(h_B); free(h_hA); free(h_hB);
    cudaFree(d_A); cudaFree(d_B); cudaFree(d_C);
    cudaFree(d_hA); cudaFree(d_hB);
  }

  cublasDestroy(handle);
  return 0;
}
