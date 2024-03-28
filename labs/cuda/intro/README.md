# Dezvoltarea de aplicații CUDA

## Utilizând cluster-ul

1. Conectați-vă mai întâi pe `fep8.grid.pub.ro` folosind contul de pe
  `curs.upb.ro`.
  Urmăriți următorul tutorial pentru ca să vă conectați de pe **dispozitivele
  personale** [fără parolă].
    ```bash
    $ ssh prenume.numeID@fep8.grid.pub.ro
2. Clonați acest repository.
    Observație: mențineți clona la curent cu schimbările recente (e.g. `git pull`)
    ```bash
    [prenume.numeID@fep8 ~]$ git clone https://gitlab.cs.pub.ro/asc/asc-public.git
    ```
3. Navigați către aplicația cu care lucrați.
    ```bash
    [prenume.numeID@fep8 hello]$ cd asc-public/labs/cuda/intro/tutorials/hello
    ```
4. Compilați sursele.
    ```bash
    [prenume.numeID@fep8 hello]$ make
    Submitted batch job 339551
    [prenume.numeID@fep8 hello]$ cat slurm-339551.out
    make[1]: Entering directory `/export/home/acs/stud/m/prenume.numeID/asc-public/labs/cuda/intro/tutorials/hello'
    nvcc   hello.cu -o hello
    make[1]: Leaving directory `/export/home/acs/stud/m/prenume.numeID/asc-public/labs/cuda/intro/tutorials/hello'
    [prenume.numeID@fep8 hello]$ make run
    Submitted batch job 339559
    [prenume.numeID@fep8 hello]$ cat slurm-339559.out
    [HOST] Hello from the host!
    [HOST] You have 1 CUDA-capable GPU(s)
    [GPU] Hello from the GPU!
    [GPU] Hello from the GPU!
    [GPU] The value is 11
    [GPU] The value is 11
    ```
    *Notă*: În caz în care fișierul `slurm-ID.out` nu a fost creat, verificați
    statusul job-ului vostru.
    ```bash
    [prenume.numeID@fep8 hello]$ squeue -j 339347
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
            339347        xl     wrap cucu.bau PD       0:00      1 (Priority)
    ```

## Utilizând procesorul grafic personal

Urmăriți instrucțiunile pe o mașină UNIX-like.

1. Clonați acest repository.
    Observație: mențineți clona la curent cu schimbările recente (e.g. `git pull`)
    ```bash
    $ git clone https://gitlab.cs.pub.ro/asc/asc-public.git
    ```
2. Navigați către aplicația cu care lucrați.
    ```bash
    $ cd asc-public/labs/cuda/intro/tutorials/hello
    ```
3. Compilați sursele.
    ```bash
    $ make LOCAL=y
    nvcc   hello.cu -o hello
    $ ./hello
    [HOST] Hello from the host!
    [HOST] You have 1 CUDA-capable GPU(s)
    [GPU] Hello from the GPU!
    [GPU] Hello from the GPU!
    [GPU] The value is 11
    [GPU] The value is 11
    ```
    **Observație**! Dacă întâmpinați următoarea problemă:

    > ERROR: No supported gcc/g++ host compiler found, but clang-14 is available.
    > Use 'nvcc -ccbin clang-14' to use that instead.

    Rulați așă comanda de `make`:
    ```bash
    make NVCC="nvcc -ccbin clang-14" LOCAL=y
    ```

## Aplicații

0. Rulați exemplele din [tutorials](tutorials/) conform pașilor de mai sus.
1. Rezolvați problemele din [exercises](exercises/) urmărind `TODO`-urile.
  Acestea sunt (în ordine ascendentă a dificultății):
    1. [vector-addition](exercises/vector-addition/)
    2. [indices](exercises/indices/)
    3. [swap](exercices/swap/)
    

[fără parolă]: https://askubuntu.com/questions/46930/how-can-i-set-up-password-less-ssh-login
