# Christian Daniel Perez De Leon
# Creado el 1/03/2020
# Ultima modificacion 4/03/2020



import simpy
import random
import numpy as np
import matplotlib.pyplot as plt

Total = []                              #Lista donde se va a guardar el Promedio de cada Proceso
Procesos_a_ejecutarse = 200             # En esta variable se establece el numero de procesos que se ejecutaran en el simulador


def sistema_operativo(env, name, ram, cpu, cant_memoria, cant_procesos, tiempo_espera):   #Funcion para simular el Sistema Operativo
    prosesos_restantes = cant_procesos                                                    #Se almacena la cantidad de procesos en la variable para poder hacer operaciones con el
    
    yield env.timeout(tiempo_espera)                                                      #Tiempo en el que se va a tradar en aparecer un nuevo proceso
    tiempoInicial = env.now
    #print("%s esta solicitando %s de memoria" % (name, cant_memoria))
    yield ram.get(cant_memoria)                                                           # Se solicita cierta cantidad de memoria RAM. Si ya no hay espacio, el proceso queda en espera
    print("%s esta listo para ser recibido por el CPU en %s" % (name, env.now))
    terminar = False
    u = 0
    
    while terminar == False:                                                               #Siclo para cada proceso en donde saldra unicamente cuando su cantidad de procesos sea 0
        
        with cpu.request() as req:
            inicio = env.now
            yield req
        
       
            prosesos_restantes = prosesos_restantes - 3                                    #Se restan la cantidad de procesos ejecutados por la CPU a la cantidad de procesos que tiene el proceso
            yield env.timeout(1)
            print("%s ejecuto 3 procesos en %s" %(name, env.now))
            
            if prosesos_restantes <= 0:                                                    #Si el proceso tiene 0 o menos procesos por ejecutarse, el proceso termino
                terminar = True
            else:                                                                          #Si no, escoge un numero al azar, si sale 1, va al proceso de entrada/salida, si sale 2, regresa a la cola para ejecutar otros 3 procesos en la CPU
                u = random.randint(1,2)
                if u == 1:
                    yield env.timeout(1)
                    print("%s esta en operaciones de entrada/salida en %s" % (name, env.now))
            
   
    print("%s termino sus procesos en %s" %(name, env.now))
    
    yield ram.put(cant_memoria)                                                            #Antes de salir del proceso se devuelve el espacio que este utilizo de RAM
    
    tiempoFinal = env.now
    tiempoTotal = tiempoFinal - tiempoInicial                                              #Calcula el tiempo promedio de este proceso y lo mete en la lista
    print(tiempoTotal)
    Total.append(tiempoTotal)
    

random.seed(10)


env = simpy.Environment()
ram = simpy.Container(env, init=100, capacity = 100)               #Container para la RAM y Resource para el CPU
cpu = simpy.Resource(env, 2)
for i in range(Procesos_a_ejecutarse + 1):                         #Segun la cantidad de procesos descritos en la variable Procesos_a_ejecutarse, se ejecutara el simulador
    tiempo_espera = random.expovariate(1.0/10)
    cant_memoria = random.randint(1,10)
    cant_procesos = random.randint(1,10)
    env.process(sistema_operativo(env, "proceso %s" % i, ram, cpu, cant_memoria, cant_procesos, tiempo_espera))

env.run()

promedio = 0
for j in range(Procesos_a_ejecutarse + 1):                        # Se calcula el promedio total de todos los tiempos promedios
    promedio = promedio + Total[i]

print("Promedio de tiempo por proceso %s" % (promedio/Procesos_a_ejecutarse))

var = np.asarray(Total)
varianza = var.std()                                              #Convierte la lista a un array y le aplica la funcion str() para calcular la desviacion estandar
print("Varianza : %s" % (varianza))




#Se ingresa en q los tiempos promedios para cada tanda de procesos y se utiliza matplotlib.pyplot para graficar cant. procesos-tiempo

q = [7.1, 44.6, 120.8, 187.8, 250.6]
w = [25, 50, 100, 150, 200]

#Descomentar la parte siguiente para graficar

#print("Promedios de cada corrida: %s" % (q) )
#plt.plot (q, w)
#plt.title("Procesos con respecto a tiempo")
#plt.xlabel("Tiempo")
#plt.ylabel("Procesos ejecutados")
#plt.show()


            
    
    