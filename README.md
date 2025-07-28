# Tarea #3

## Primera parte, Operaciones Colectivas en MPI 

El programa **"estadisticas_mpi.py"** genera un arreglo de **'N'** números aleatorios entre 0 y 100, y que son divisibles entre el número total de procesos que seteamos en el input a la terminal. **MPI_Bcast** 
le dice a los procesos cuánto trabajo hay y **MPI_Scatter** se encarga de distribuir el trabajo en varios procesos. Por último el **MPI_Gather** se encarga de calcular el mínimo, máximo y el promedio local. 


### Ejecución 

```bash
mpirun -np 4 python estadisticas_mpi.py 1000000
```
Para correr el código se puede copiar y pegar el texto anterior en la terminal. 

En este caso le estamos diciendo al código que procese un millón de números distribuidos en 4 procesos paralelos. Si por ejemplo, en vez de 4 procesos decidimos tener 3, el código tiraría un error porque un millón no se puede dividir exactamente entre 3.

### Ejemplo de salida 

```bash
Estadísticas globales del arreglo de tamaño 1000000:
  Mínimo global: 0.00
  Máximo global: 100.00
  Promedio global: 49.97
```

## Segunda parte, Medición de Latencia de Comunicaciónes Punto a Punto

El programa **"latencia_mpi.py"** mide el tiempo que tarda en enviarse y recibirse un mensaje entre dos procesos utilizando las funciones **MPI_Send** y **MPI_Recv**. El proceso con **rank = 0** envía un mensaje de 1 byte al proceso con **rank = 1**, que lo recibe y lo devuelve inmediatamente. 
Este intercambio se repite la cantidad N que escogemos en el código, y se calcula la latencia promedio por mensaje, así como una estimación de la latencia unidireccional.

### Ejecución 

