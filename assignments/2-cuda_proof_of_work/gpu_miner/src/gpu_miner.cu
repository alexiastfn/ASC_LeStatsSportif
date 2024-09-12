#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "../include/utils.cuh"

__constant__ BYTE difficulty[SHA256_HASH_SIZE] =
    "0000099999999999999999999999999999999999999999999999999999999999";

// TODO: Implement function to search for all nonces from 1 through MAX_NONCE
// (inclusive) using CUDA Threads
__global__ void findNonce(uint64_t *gpu_nonce, size_t *gpu_current_length,
                          BYTE *gpu_block_hash, BYTE *gpu_block_content) {
  char nonce_string[NONCE_SIZE];
  BYTE gpu_block_content_copy[BLOCK_SIZE];
  d_strcpy((char *)gpu_block_content_copy, (char *)gpu_block_content);
  BYTE gpu_block_hash_copy[BLOCK_SIZE];

  int index = blockIdx.x * blockDim.x + threadIdx.x;
  int stride = blockDim.x * gridDim.x;

  for (uint64_t i = index; i <= MAX_NONCE; i += stride) {
    if (gpu_block_hash[0] != 0) break;

    intToString(i, nonce_string);
    d_strcpy((char *)gpu_block_content_copy + *gpu_current_length,
             nonce_string);

    apply_sha256(gpu_block_content_copy,
                 d_strlen((const char *)gpu_block_content_copy),
                 gpu_block_hash_copy, 1);

    if (compare_hashes(gpu_block_hash_copy, difficulty) <= 0) {
      d_strcpy((char *)gpu_block_hash, (char *)gpu_block_hash_copy);
      *gpu_nonce = i;
      break;
    }
  }
}

int main(int argc, char **argv) {
  BYTE hashed_tx1[SHA256_HASH_SIZE], hashed_tx2[SHA256_HASH_SIZE],
      hashed_tx3[SHA256_HASH_SIZE], hashed_tx4[SHA256_HASH_SIZE],
      tx12[SHA256_HASH_SIZE * 2], tx34[SHA256_HASH_SIZE * 2],
      hashed_tx12[SHA256_HASH_SIZE], hashed_tx34[SHA256_HASH_SIZE],
      tx1234[SHA256_HASH_SIZE * 2], top_hash[SHA256_HASH_SIZE],
      block_content[BLOCK_SIZE];
  BYTE block_hash[SHA256_HASH_SIZE] =
      "0000000000000000000000000000000000000000000000000000000000000000";
  uint64_t nonce = 0;
  uint64_t *gpu_nonce;
  BYTE *gpu_block_content;
  BYTE *gpu_block_hash;
  size_t *gpu_current_length;
  size_t current_length;

  // Top hash
  apply_sha256(tx1, strlen((const char *)tx1), hashed_tx1, 1);
  apply_sha256(tx2, strlen((const char *)tx2), hashed_tx2, 1);
  apply_sha256(tx3, strlen((const char *)tx3), hashed_tx3, 1);
  apply_sha256(tx4, strlen((const char *)tx4), hashed_tx4, 1);
  strcpy((char *)tx12, (const char *)hashed_tx1);
  strcat((char *)tx12, (const char *)hashed_tx2);
  apply_sha256(tx12, strlen((const char *)tx12), hashed_tx12, 1);
  strcpy((char *)tx34, (const char *)hashed_tx3);
  strcat((char *)tx34, (const char *)hashed_tx4);
  apply_sha256(tx34, strlen((const char *)tx34), hashed_tx34, 1);
  strcpy((char *)tx1234, (const char *)hashed_tx12);
  strcat((char *)tx1234, (const char *)hashed_tx34);
  apply_sha256(tx1234, strlen((const char *)tx34), top_hash, 1);

  // prev_block_hash + top_hash
  strcpy((char *)block_content, (const char *)prev_block_hash);
  strcat((char *)block_content, (const char *)top_hash);
  current_length = strlen((char *)block_content);

  cudaEvent_t start, stop;
  startTiming(&start, &stop);

  cudaMalloc((void **)&gpu_nonce, sizeof(uint64_t));
  cudaMalloc((void **)&gpu_block_content, BLOCK_SIZE);
  cudaMalloc((void **)&gpu_block_hash, SHA256_HASH_SIZE);
  cudaMalloc((void **)&gpu_current_length, sizeof(size_t));

  cudaMemcpy((void *)gpu_current_length, (void *)&current_length,
             sizeof(size_t), cudaMemcpyHostToDevice);
  cudaMemcpy((void *)gpu_nonce, (void *)&nonce, sizeof(uint64_t),
             cudaMemcpyHostToDevice);
  cudaMemcpy((void *)gpu_block_content, (void *)block_content, BLOCK_SIZE,
             cudaMemcpyHostToDevice);
  cudaMemset(gpu_block_hash, 0, 1);

  int blockSize = 256;
  int numBlocks = (MAX_NONCE + blockSize - 1) / blockSize;
  findNonce<<<numBlocks, blockSize>>>(gpu_nonce, gpu_current_length,
                                      gpu_block_hash, gpu_block_content);

  cudaDeviceSynchronize();

  cudaMemcpy((void *)&nonce, (void *)gpu_nonce, sizeof(uint64_t),
             cudaMemcpyDeviceToHost);
  cudaMemcpy((void *)block_hash, (void *)gpu_block_hash, SHA256_HASH_SIZE,
             cudaMemcpyDeviceToHost);

  cudaFree(gpu_nonce);
  cudaFree(gpu_block_content);
  cudaFree(gpu_block_hash);
  cudaFree(gpu_current_length);
  float seconds = stopTiming(&start, &stop);
  printResult(block_hash, nonce, seconds);

  return 0;
}
