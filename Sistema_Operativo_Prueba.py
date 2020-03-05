import simpy
import random
import numpy as np
import matplotlib.pyplot as plt

Total = []
def sistema_operativo(env, name, ram, cpu, cant_memoria, cant_procesos):
    prosesos_restantes = cant_procesos
    #print("%s esta solicitando %s de memoria" % (name, cant_memoria))
    yield ram.get(cant_memoria)
    print("%s esta listo para ser recibido por el CPU en %s" % (name, env.now))
    tiempoInicial = env.now
    
    with cpu.request() as req:
        inicio = env.now
        yield req
        
        
        while prosesos_restantes >= 0:
            prosesos_restantes = prosesos_restantes - 3
            yield env.timeout(1)
            print("%s ejecuto 3 procesos en %s" %(name, env.now))
        
            
            
            
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
for i in range(201):
    cant_memoria = random.randint(1,10)
    cant_procesos = random.randint(1,10)
    env.process(sistema_operativo(env, "proceso %s" % i, ram, cpu, cant_memoria, cant_procesos))

env.run()


mi_path = "Tiempos.txt"
x = open(mi_path, "a+")
promedio = 0
for j in range(201):
    promedio = promedio + Total[i]
print("Promedio de tiempo por proceso %s" % (promedio/200))

var = np.array([61,118,241,376,506])
varianza = var.std()
print("Varianza: %s" % (varianza))



q = [61, 118, 241, 376, 506]
#q = [37.7, 37.7, 43.4, 43.3, 44.2]
w = [25, 50, 100, 150, 200]
plt.plot (w, q)
plt.title("Procesos con respecto a tiempo")
#plt.legend()
plt.show()

            
    
    