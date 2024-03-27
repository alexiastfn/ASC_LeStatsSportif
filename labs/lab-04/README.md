# Dezvoltarea de aplicații CUDA

Pentru acest laborator vă rugăm să vă conectați mai întâi pe `fep8.grid.pub.ro`
folosind contul de pe `curs.upb.ro`.

```bash
$ ssh prenume.numeID@fep8.grid.pub.ro
$ git clone https://gitlab.cs.pub.ro/asc/asc-public.git
```

Urmăriți următorul tutorial pentru logare ca să vă conectați de pe **dispozitivele
personale** [fără parolă].

## Utilizare interactivă

Verificați că vă puteți connecta la un nod din partiția `xl`.

```bash
[prenume.numeID@fep8 ~]$ srun -A asc --gres gpu:1 --time 00:05:00 --pty -p xl /bin/bash
[prenume.numeID@wnxyz ~]$ nvidia-smi
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

Navigați TODO

```bash
[prenume.numeID@wnxyz ~]$ cd asc-public/
```

[fără parolă]: https://askubuntu.com/questions/46930/how-can-i-set-up-password-less-ssh-login
