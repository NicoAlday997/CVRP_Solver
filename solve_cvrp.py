import numpy as np

class CVRP:
    def __init__(self, distancias, demandas, capacidad_vehiculo):
        self.distancias = distancias
        self.demandas = demandas
        self.capacidad_vehiculo = capacidad_vehiculo
        self.num_clientes = len(distancias)
        self.rutas = []

    def encontrar_cliente_mas_cercano(self, clientes_disponibles):
        distancia_minima = float('inf')
        cliente_mas_cercano = None
        for cliente in clientes_disponibles:
            distancia = self.distancias[0][cliente]  # Distancia desde el depósito al cliente
            if distancia < distancia_minima:
                distancia_minima = distancia
                cliente_mas_cercano = cliente
        return cliente_mas_cercano

    def construir_rutas(self):
        clientes_no_asignados = list(range(1, self.num_clientes))

        while clientes_no_asignados:
            ruta_actual = [0]
            capacidad_restante = self.capacidad_vehiculo

            cliente_mas_cercano = self.encontrar_cliente_mas_cercano(clientes_no_asignados)
            while cliente_mas_cercano is not None and capacidad_restante >= self.demandas[cliente_mas_cercano]:
                ruta_actual.append(cliente_mas_cercano)
                capacidad_restante -= self.demandas[cliente_mas_cercano]
                clientes_no_asignados.remove(cliente_mas_cercano)
                cliente_mas_cercano = self.encontrar_cliente_mas_cercano(clientes_no_asignados)

            ruta_actual.append(0)  # Regresar al depósito al final
            self.rutas.append(ruta_actual)

    def mejorar_rutas_localmente(self):
        for ruta in self.rutas:
            for i in range(1, len(ruta) - 1):
                for j in range(i + 1, len(ruta) - 1):
                    nueva_ruta = ruta[:i] + [ruta[j]] + ruta[i + 1:j] + [ruta[i]] + ruta[j + 1:]
                    distancia_original = self.calcular_distancia(ruta)
                    distancia_nueva = self.calcular_distancia(nueva_ruta)
                    if distancia_nueva <= distancia_original:
                        ruta[:] = nueva_ruta
                        break

    def intercambiar_nodos_entre_rutas(self):
        for i in range(len(self.rutas)):
            for j in range(i + 1, len(self.rutas)):
                for cliente_ruta1 in self.rutas[i][1:-1]:
                    for cliente_ruta2 in self.rutas[j][1:-1]:
                        if self.demandas[cliente_ruta1] + sum(
                                self.demandas[cliente] for cliente in self.rutas[j][1:-1]) <= self.capacidad_vehiculo \
                                and self.demandas[cliente_ruta2] + sum(
                                self.demandas[cliente] for cliente in self.rutas[i][1:-1]) <= self.capacidad_vehiculo:
                            nueva_ruta1 = self.rutas[i][:]  # Copiar ruta 1
                            nueva_ruta2 = self.rutas[j][:]  # Copiar ruta 2
                            nueva_ruta1[nueva_ruta1.index(cliente_ruta1)] = cliente_ruta2
                            nueva_ruta2[nueva_ruta2.index(cliente_ruta2)] = cliente_ruta1
                            if self.calcular_distancia(nueva_ruta1) + self.calcular_distancia(nueva_ruta2) < \
                                    self.calcular_distancia(self.rutas[i]) + self.calcular_distancia(self.rutas[j]):
                                self.rutas[i] = nueva_ruta1
                                self.rutas[j] = nueva_ruta2
                                break

    def calcular_distancia(self, ruta):
        distancia_total = 0
        for i in range(len(ruta) - 1):
            distancia_total += self.distancias[ruta[i]][ruta[i + 1]]
        return distancia_total

    def resolver(self):
        self.construir_rutas()
        while True:
            rutas_anteriores = self.rutas.copy()
            self.mejorar_rutas_localmente()
            self.intercambiar_nodos_entre_rutas()
            if self.rutas == rutas_anteriores:
                break

        self.fusionar_rutas()

        # Calcular y mostrar el costo y la carga para cada ruta
        for i, ruta in enumerate(self.rutas):
            distancia_ruta = self.calcular_distancia(ruta)
            carga_vehiculo = sum(self.demandas[cliente] for cliente in ruta[1:-1])
            print(f"Ruta {i + 1}: Distancia = {distancia_ruta}, Carga del vehículo = {carga_vehiculo}")

        return self.rutas

    def fusionar_rutas(self):
        fusion = True
        while fusion:
            fusion = False
            for i in range(len(self.rutas)):
                for j in range(i + 1, len(self.rutas)):
                    nueva_ruta = [0] + self.rutas[i][1:-1] + self.rutas[j][1:-1] + [0]
                    carga_total = sum(self.demandas[cliente] for cliente in nueva_ruta)
                    if carga_total <= self.capacidad_vehiculo:
                        self.rutas.append(nueva_ruta)
                        del self.rutas[i]
                        del self.rutas[j - 1]
                        fusion = True
                        break
                if fusion:
                    break
    def imprimir_rutas_iniciales(self):
        print("Rutas Iniciales:")
        for i, ruta in enumerate(self.rutas):
            print(f"Ruta {i + 1}: {ruta}")


# Matriz de distancias
distance_matrix = [
    [0, 4.5, 5.8, 7.1, 6.7, 10],
    [4.5, 0, 3.2, 5.8, 2.2, 5.7],
    [5.8, 3.2, 0, 2.8, 3.6, 5.1],
    [7.1, 5.8, 2.8, 0, 6.4, 7.1],
    [6.7, 2.5, 3.6, 6.4, 0, 3.6],
    [10, 5.7, 5.1, 7.1, 3.6, 0]
]
demands = [0, 8, 6, 4, 7, 5]  # Demanda del cliente i
capacity = 12

cvrp_solver = CVRP(distance_matrix, demands, capacity)
cvrp_solver2 = CVRP(distance_matrix, demands, capacity)
cvrp_solver2.construir_rutas()
cvrp_solver2.imprimir_rutas_iniciales()
print()
print("Solucion:")
solucion = cvrp_solver.resolver()
print(solucion)