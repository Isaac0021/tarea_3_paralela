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

```bash
mpirun -np 2 python latencia_mpi.py
```

Para correr el codigo se puede copiar y pegar el anterior. 

Este input en la terminal define que tenemos dos procesos y se tiene que correr el archivo latencia_mpi.py. Si le damos otra cantidad de procesos que no sea dos, tirará un error. 


### Ejemplo de salida

```bash
Mensaje de 1 byte transmitido 10000 veces.
Latencia promedio por mensaje (ida y vuelta): 1.08 microsegundos
Latencia estimada unidireccional: 0.54 microsegundos
```

## Análisis

En las pruebas de comunicación punto a punto usando MPI_Send y MPI_Recv, la latencia promedio obtenida fue de aproximadamente 3.2 microsegundos ida y vuelta, equivalente a unos 1.6 microsegundos unidireccionalmente. Este valor refleja un tiempo de transmisión muy bajo, pero no constante: se observaron pequeñas variaciones asociadas a la carga de la CPU, el sistema operativo y la administración de procesos. En sistemas más ocupados o con hardware menos optimizado para HPC, esta latencia podría aumentar significativamente.
Es importante destacar que en mensajes muy pequeños (como el de 1 byte en este experimento), la latencia está dominada por el tiempo de configuración y envío, no por la transferencia de datos. Para mensajes más grandes, el tiempo de transmisión total estaría influenciado tanto por la latencia como por el ancho de banda disponible.

En cuanto a las operaciones colectivas (MPI_Bcast, MPI_Scatter, MPI_Reduce), su rendimiento fue notablemente eficiente al manejar grandes volúmenes de datos. Procesar un millón de elementos distribuidos en 4 procesos permitió dividir la carga de trabajo de manera equilibrada, obteniendo un mínimo de 0.00, un máximo de 100.00 y un promedio global muy cercano al valor teórico esperado (~50). El uso de estas operaciones redujo la complejidad del código y minimizó el número de llamadas de comunicación necesarias.

Comparando ambos enfoques:

Punto a punto es más flexible y permite un control fino del flujo de mensajes, pero requiere programar manualmente la lógica de envío/recepción y puede volverse complejo en sistemas con muchos procesos.
Colectivas simplifican y optimizan patrones comunes de comunicación, aprovechando implementaciones internas altamente optimizadas de MPI, lo que suele traducirse en menor latencia global y mejor escalabilidad en sistemas grandes.
En resumen, las pruebas muestran que la elección entre comunicación punto a punto o colectiva depende del patrón de comunicación requerido: para intercambios simples y controlados entre pocos procesos, punto a punto es suficiente; para distribuir y recolectar grandes volúmenes de datos en sistemas con muchos procesos, las operaciones colectivas son más adecuadas y eficientes.
