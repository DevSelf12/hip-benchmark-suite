#include <hip/hip_runtime.h>
#include <iostream>
#include <vector>
#include <cstdlib>

__global__ void vector_add(const float* A, const float* B, float* C, int N) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < N) {
        C[idx] = A[idx] + B[idx];
    }
}

int main() {
    const int N = 1 << 20;
    size_t bytes = N * sizeof(float);

    std::vector<float> h_A(N, 1.0f);
    std::vector<float> h_B(N, 2.0f);
    std::vector<float> h_C(N, 0.0f);

    float *d_A, *d_B, *d_C;
    hipMalloc(&d_A, bytes);
    hipMalloc(&d_B, bytes);
    hipMalloc(&d_C, bytes);

    hipMemcpy(d_A, h_A.data(), bytes, hipMemcpyHostToDevice);
    hipMemcpy(d_B, h_B.data(), bytes, hipMemcpyHostToDevice);

    int block = 256;
    int grid = (N + block - 1) / block;

    hipLaunchKernelGGL(vector_add, dim3(grid), dim3(block), 0, 0, d_A, d_B, d_C, N);
    hipDeviceSynchronize();

    hipMemcpy(h_C.data(), d_C, bytes, hipMemcpyDeviceToHost);

    bool ok = true;
    for (int i = 0; i < N; ++i) {
        if (h_C[i] != 3.0f) {
            ok = false;
            break;
        }
    }

    std::cout << "[vector_add_hip] N=" << N << " result=" << (ok ? "PASS" : "FAIL") << "\n";

    hipFree(d_A);
    hipFree(d_B);
    hipFree(d_C);
    return ok ? 0 : 1;
}
