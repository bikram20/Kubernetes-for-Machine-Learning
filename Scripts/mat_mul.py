#!/usr/bin/python3
import torch
import time

#Size of the matrices. You need to adjust the size based on your GPU. 
#The arithmatic may not be that simple in reality (other processes running, reserved memory etc.), 
#but matrices size gives an idea of how much GPU RAM you need, 
#eg. 2 input and 1 output matrices with each element a FP32 or FP16.
N_cpu = 10000
N_cudacore = 25000
N_tensorcore = 25000

#Computation on CPU
#Create random matrices. These are 32-bit floating point
A = torch.rand(N_cpu, N_cpu)
B = torch.rand(N_cpu, N_cpu)

#Perform matrix multiplication on CPU
start_time = time.time()
result_cpu = torch.matmul(A, B)
time_cpu = time.time() - start_time
print(f"Matrices dimension: {N_cpu}, Time taken on CPU: {time_cpu} seconds")

#This is executed on CUDA cores on the GPU
if torch.cuda.is_available():
    device = torch.device('cuda')
    #torch.cuda.empty_cache()
    A_gpu = torch.rand(N_cudacore, N_cudacore, device=device)
    B_gpu = torch.rand(N_cudacore, N_cudacore, device=device)

    # Perform matrix multiplication on GPU
    start_time = time.time()
    result_gpu = torch.matmul(A_gpu, B_gpu)
    result_cpu_from_gpu = result_gpu.cpu()
    time_gpu = time.time() - start_time
    print(f"Matrices dimension: {N_cudacore}, Time taken on CUDA cores: {time_gpu} seconds")
else:
    print("GPU not available.")


#Pytorch uses tensor cores on the GPU for FP16 computation
if torch.cuda.is_available():
    device = torch.device('cuda')
    # Create random matrices in half precision (FP16). This can fail, because pytorch needs to allocate memory for this task on GPU RAM, and then less memory is available for matrix multiplication. 
    A_fp16 = torch.rand(N_tensorcore, N_tensorcore, device=device, dtype=torch.half)
    B_fp16 = torch.rand(N_tensorcore, N_tensorcore, device=device, dtype=torch.half)

    # Create random matrices in standard precision (FP32) on CPU. This can get really slow, as the computation is done on CPU.
    #A_cpu = torch.rand(N_tensorcore, N_tensorcore, dtype=torch.float32)
    #B_cpu = torch.rand(N_tensorcore, N_tensorcore, dtype=torch.float32)
    # Convert to half precision (FP16) and move to GPU
    #A_fp16 = A_cpu.half().to(device)
    #B_fp16 = B_cpu.half().to(device)

    # Perform matrix multiplication on Tensor Cores
    start_time = time.time()
    result_fp16 = torch.matmul(A_fp16, B_fp16).float()  # Convert FP16 result to FP32 for comparison
    time_fp16 = time.time() - start_time
    print(f"Matrices dimension: {N_tensorcore}, Time taken on Tensor Cores (FP16): {time_fp16} seconds")
else:
    print("GPU not available.")
