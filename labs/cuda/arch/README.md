# Arhitectura CUDA

## Recapitulare

Înainte să vă apucați de acest laborator vă rugăm să verificați că sunteți
familiari cu dezvoltarea folosind cluster-ul/unitatea personală a surselor
din acest repo.

Recitiți [descrierea laboratorului introductiv](../intro/README.md) în
acest sens.

## Exerciții

0. Rulați exemplele din [tutorials](tutorials/).
1. Rezolvați problemele din [exercises](exercises/) urmărind `TODO`-urile.
    1. Pentru [benchmark](exercises/benchmark/)-ing încercați să măsurați
      performanța maximă a unității GPU, înregistrând numărul de GFLOPS.
        * Masurati timpul petrecut in kernel.
          > Hint: Folositi evenimente CUDA.
        * Realizați un profiling pentru funcțiile implementate folosind
        utilitarul `nvprof`.
    2. Pentru [matrix_multiply](exercises/matrix_multiply/):
        * Completați funcția `matrix_multiply_simple` care va realiza
          înmulțirea a două matrice primite prin parametrii.
        * Completați funcția `matrix_multiply` care va realiza o înmulțire
          optimizată a două matrice, folosind Blocked Matrix Multiplication.
            > Hint: Se va folosi directiva `__shared__` pentru a aloca memorie
              partajată între thread-uri. Pentru sincronizarea thread-urilor
              va folosi funcția `__syncthreads`.
        * Măsurați timpul petrecut în kernel
            > Hint: Folositi evenimente CUDA.
        * Realizați un profiling pentru funcțiile implementate folosind
        utilitarul `nvprof`.
