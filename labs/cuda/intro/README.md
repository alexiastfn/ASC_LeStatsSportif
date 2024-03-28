# Dezvoltarea de aplicații CUDA

1. Conectați-vă mai întâi pe `fep8.grid.pub.ro` folosind contul de pe
  `curs.upb.ro`.
  Urmăriți următorul tutorial pentru ca să vă conectați de pe **dispozitivele
  personale** [fără parolă].
    ```bash
    $ ssh prenume.numeID@fep8.grid.pub.ro
2. Clonați acest repository.
    ```bash
    [prenume.numeID@fep8 ~]$ git clone https://gitlab.cs.pub.ro/asc/asc-public.git
    ```
3. Navigați către aplicația cu care lucrați.
    ```bash
    [prenume.numeID@fep8 hello]$ cd asc-public/labs/lab-04/tutorials/hello/
    ```
4. Setați containerul pe care îl veți folosi.
    ```bash
    [prenume.numeID@fep8 hello]$ IMG=docker://gitlab.cs.pub.ro:5050/asc/asc-public/cuda-labs:1.11.4
    [prenume.numeID@fep8 hello]$ export IMG
    ```
5. Verificați că vă puteți connecta la un nod din partiția `xl` și ajustați
  limita de timp în acord cu nevoile voastre.
    ```bash
    [prenume.numeID@fep8 hello]$ srun -A asc --gres gpu:1 --time 00:05:00 --pty -p xl /bin/bash
    [prenume.numeID@wnxyz hello]$ nvidia-smi
    Wed Mar 27 23:33:34 2024
    +-----------------------------------------------------------------------------------------+
    | NVIDIA-SMI 550.54.15              Driver Version: 550.54.15      CUDA Version: 12.4     |
    |-----------------------------------------+------------------------+----------------------+
    | GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
    | Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
    |                                         |                        |               MIG M. |
    |=========================================+========================+======================|
    |   0  Tesla P100-PCIE-16GB           On  |   00000000:0D:00.0 Off |                    0 |
    | N/A   25C    P0             24W /  250W |       0MiB /  16384MiB |      0%      Default |
    |                                         |                        |                  N/A |
    +-----------------------------------------+------------------------+----------------------+

    +-----------------------------------------------------------------------------------------+
    | Processes:                                                                              |
    |  GPU   GI   CI        PID   Type   Process name                              GPU Memory |
    |        ID   ID                                                               Usage      |
    |=========================================================================================|
    |  No running processes found                                                             |
    +-----------------------------------------------------------------------------------------+
    ```
6. Alegeți între
  - rularea cu `apptainer`
    ```bash
    [prenume.numeID@wnxyz ~]$ apptainer run --nv $IMG
    Apptainer> make
    nvcc hello.cu -o hello
    Apptainer> ./hello
    [HOST] Hello from the host!
    [HOST] You have 1 CUDA-capable GPU(s)
    [GPU] Hello from the GPU!
    [GPU] Hello from the GPU!
    [GPU] The value is 11
    [GPU] The value is 11
    ```
  - sau cu `singularity`.
    ```bash
    [prenume.numeID@wnxyz ~]$ singularity exec --nv $IMG make
    nvcc hello.cu -o hello
    [prenume.numeID@wnxyz ~]$ singularity exec --nv $IMG ./hello
    [HOST] Hello from the host!
    [HOST] You have 1 CUDA-capable GPU(s)
    [GPU] Hello from the GPU!
    [GPU] Hello from the GPU!
    [GPU] The value is 11
    [GPU] The value is 11
    ```

Pentru a minimiza consumul de resurse luați încalcul rularea neinteractivă.

```bash
[prenume.numeID@fep8 hello]$ sbatch -A asc --gres gpu:1 --time 00:05:00 -p xl --wrap="singularity exec --nv $IMG make"
Submitted batch job 337784
[prenume.numeID@fep8 hello]$ cat slurm-337784.out
nvcc hello.cu -o hello
[prenume.numeID@fep8 hello]$ sbatch -A asc --gres gpu:1 --time 00:05:00 -p xl --wrap="singularity exec --nv $IMG ./hello"
Submitted batch job 337860
[prenume.numeID@fep8 hello]$ cat slurm-337860.out
[HOST] Hello from the host!
[HOST] You have 1 CUDA-capable GPU(s)
[GPU] Hello from the GPU!
[GPU] Hello from the GPU!
[GPU] The value is 11
[GPU] The value is 11
```

## Aplicații

0. Rulați exemplele din <tutorials/> conform pașilor de mai sus.
1. Rezolvați problemele din <exercices/> urmărind `TODO`-urile.

[fără parolă]: https://askubuntu.com/questions/46930/how-can-i-set-up-password-less-ssh-login
