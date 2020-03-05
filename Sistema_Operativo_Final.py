import simpy
import random
import numpy as np
import matplotlib.pyplot as plt

Total = []
Procesos_a_ejecutarse = 200


def sistema_operativo(env, name, ram, cpu, cant_memoria, cant_procesos, tiempo_espera):
    prosesos_restantes = cant_procesos
    
    yield env.timeout(tiempo_espera)
    tiempoInicial = env.now
    #print("%s esta solicitando %s de memoria" % (name, cant_memoria))
    yield ram.get(cant_memoria)
    print("%s esta listo para ser recibido por el CPU en %s" % (name, env.now))
    terminar = False
    u = 0
    
    while terminar == False:
        
        with cpu.request() as req:
            inicio = env.now
            yield req
        
       
            prosesos_restantes = prosesos_restantes - 3
            yield env.timeout(1)
            print("%s ejecuto 3 procesos en %s" %(name, env.now))
            
            if prosesos_restantes <= 0:
                terminar = True
            else:
                u = random.randint(1,2)
                if u == 1:
                    yield env.timeout(1)
                    print("%s esta en operaciones de entrada/salida en %s" % (name, env.now))
            
   
    print("%s termino sus procesos en %s" %(name, env.now))
    
    yield ram.put(cant_memoria)
    
    tiempoFinal = env.now
    tiempoTotal = tiempoFinal - tiempoInicial
    print(tiempoTotal)
    Total.append(tiempoTotal)
    

random.seed(10)


env = simpy.Environment()
ram = simpy.Container(env, init=100, capacity = 100)
cpu = simpy.Resource(env, 1)
for i in range(Procesos_a_ejecutarse + 1):
    tiempo_espera = random.expovariate(1.0/10)
    cant_memoria = random.randint(1,10)
    cant_procesos = random.randint(1,10)
    env.process(sistema_operativo(env, "proceso %s" % i, ram, cpu, cant_memoria, cant_procesos, tiempo_espera))

env.run()


mi_path = "Tiempos.txt"
x = open(mi_path, "a+")
promedio = 0
for j in range(Procesos_a_ejecutarse + 1):
    promedio = promedio + Total[i]

print("Promedio de tiempo por proceso %s" % (promedio/Procesos_a_ejecutarse))

var = np.asarray(Total)
varianza = var.std()
print("Varianza : %s" % (varianza))


#q = [74, 143, 258, 435, 575]
q = [74, 123, 274, 439, 568]
w = [25, 50, 100, 150, 200]
plt.plot (q, w)
plt.title("Procesos con respecto a tiempo")
plt.xlabel("Tiempo")
plt.ylabel("Procesos ejecutados")
plt.show()

            
    
    