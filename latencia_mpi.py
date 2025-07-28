from mpi4py import MPI
import numpy as np
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Solo deben ejecutarse dos procesos
if size != 2:
    if rank == 0:
        print("Este programa requiere exactamente 2 procesos.")
    sys.exit()

# Número de repeticiones y tamaño del mensaje
N = 10000
mensaje = bytearray(1)  # mensaje de 1 byte

# Proceso 0 mide el tiempo
if rank == 0:
    inicio = MPI.Wtime()
    for _ in range(N):
        comm.Send([mensaje, MPI.BYTE], dest=1, tag=0)
        comm.Recv([mensaje, MPI.BYTE], source=1, tag=1)
    fin = MPI.Wtime()

    tiempo_total = fin - inicio
    latencia_promedio = (tiempo_total / N) * 1e6  # microsegundos (ida y vuelta)
    latencia_unidireccional = latencia_promedio / 2

    print(f"Mensaje de 1 byte transmitido {N} veces.")
    print(f"Latencia promedio por mensaje (ida y vuelta): {latencia_promedio:.2f} microsegundos")
    print(f"Latencia estimada unidireccional: {latencia_unidireccional:.2f} microsegundos")

# Proceso 1 responde los mensajes
elif rank == 1:
    for _ in range(N):
        comm.Recv([mensaje, MPI.BYTE], source=0, tag=0)
        comm.Send([mensaje, MPI.BYTE], dest=0, tag=1)
