from mpi4py import MPI
import numpy as np
import sys

# Inicializar el comunicador
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Validar argumentos para correr el codigo
if len(sys.argv) != 2:
    if rank == 0:
        print("Uso: mpirun -np <num_procesos> python estadisticas_mpi.py <tamano_arreglo>")
    sys.exit()

N = int(sys.argv[1])

# Verificar que N sea divisible entre el número de procesos
if N % size != 0:
    if rank == 0:
        print("Error: El tamaño del arreglo debe ser divisible entre el número de procesos.")
    sys.exit()

# Cada proceso maneja una porción de este tamaño
local_size = N // size

# Solo el proceso 0 genera el arreglo completo
if rank == 0:
    arreglo_completo = np.random.uniform(0, 100, N).astype('float64')
else:
    arreglo_completo = None

# Arreglo local que recibirá cada proceso
sub_arreglo = np.empty(local_size, dtype='float64')

# Difundir el tamaño del arreglo
comm.bcast(N, root=0)

# Repartir los datos entre procesos
comm.Scatter(arreglo_completo, sub_arreglo, root=0)

# Calcular estadísticas locales
local_min = np.min(sub_arreglo)
local_max = np.max(sub_arreglo)
local_avg = np.mean(sub_arreglo)

# Reducir al proceso raíz para obtener estadísticas globales
global_min = comm.reduce(local_min, op=MPI.MIN, root=0)
global_max = comm.reduce(local_max, op=MPI.MAX, root=0)
global_sum = comm.reduce(np.sum(sub_arreglo), op=MPI.SUM, root=0)

if rank == 0:
    global_avg = global_sum / N
    print(f"Estadísticas globales del arreglo de tamaño {N}:")
    print(f"  Mínimo global: {global_min:.2f}")
    print(f"  Máximo global: {global_max:.2f}")
    print(f"  Promedio global: {global_avg:.2f}")

