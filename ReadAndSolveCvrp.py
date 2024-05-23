import numpy as np

import random
import math


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

            # Selección aleatoria del primer cliente
            cliente_inicial = random.choice(clientes_no_asignados)
            ruta_actual.append(cliente_inicial)
            clientes_no_asignados.remove(cliente_inicial)

            # Llamar a encontrar_cliente_mas_cercano para inicializar cliente_mas_cercano
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
        print("Rutas iniciales: ")
        self.imprimir_rutas()
        while True:
            rutas_anteriores = self.rutas.copy()
            self.mejorar_rutas_localmente()
            self.intercambiar_nodos_entre_rutas()
            if self.rutas == rutas_anteriores:
                break

        self.fusionar_rutas()

        print("\nRutas finales: ")
        self.imprimir_rutas()
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

    def imprimir_rutas(self):
        # print("Rutas Iniciales:")
        for i, ruta in enumerate(self.rutas):
            print(f"Ruta {i + 1}: {ruta}")

        distancia_total = 0
        carga_total = 0
        for i, ruta in enumerate(self.rutas):
            distancia_ruta = self.calcular_distancia(ruta)
            carga_vehiculo = sum(self.demandas[cliente] for cliente in ruta[1:-1])
            print(f"Ruta {i + 1}: Distancia = {distancia_ruta}, Carga del vehículo = {carga_vehiculo}")
            distancia_total += distancia_ruta
            carga_total += carga_vehiculo
        print(f"Recorrido total de rutas: {distancia_total}")
        print(f"Carga total de vehiculos: {carga_total}")

class CVRPInstance:
    def __init__(self):
        self.name = ""
        self.comment = ""
        self.no_of_trucks = 0
        self.optimal_value = 0
        self.type = ""
        self.dimension = 0
        self.edge_weight_type = ""
        self.capacity = 0
        self.node_coords = {}
        self.demands = {}
        self.depot = 0
        self.distance_matrix = []

    def calculate_distance_matrix(self):
        """
        Calcula la matriz de distancias entre todos los pares de nodos.
        """
        num_nodes = self.dimension
        self.distance_matrix = [[0] * num_nodes for _ in range(num_nodes)]

        for i in range(1, num_nodes + 1):  # Ignoramos el depósito (nodo 1)
            for j in range(1, num_nodes + 1):  # Ignoramos el depósito (nodo 1)
                if i != j:
                    self.distance_matrix[i - 1][j - 1] = self.euclidean_distance(self.node_coords[i],
                                                                                 self.node_coords[j])

    @staticmethod
    def euclidean_distance(coord1, coord2):
        """
        Calcula la distancia euclidiana entre dos coordenadas.

        Args:
            coord1: Tupla (x, y) de las coordenadas del primer nodo.
            coord2: Tupla (x, y) de las coordenadas del segundo nodo.

        Returns:
            La distancia euclidiana entre las dos coordenadas.
        """
        x1, y1 = coord1
        x2, y2 = coord2
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def read_cvrp_instance(file_path):
    instance = CVRPInstance()

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("NAME"):
                instance.name = line.split(":")[1].strip()
            elif line.startswith("COMMENT"):
                instance.comment = line.split(":")[1].strip()
                # Extraer el número de camiones y el valor óptimo del comentario
                no_of_trucks_index = instance.comment.find("No of trucks")
                optimal_value_index = instance.comment.find("Optimal value")
                if no_of_trucks_index != -1:
                    no_of_trucks_substr = ''.join(filter(str.isdigit, instance.comment[no_of_trucks_index:]))
                    if no_of_trucks_substr.isdigit():
                        instance.no_of_trucks = int(no_of_trucks_substr)
                if optimal_value_index != -1:
                    optimal_value_substr = ''.join(filter(str.isdigit, instance.comment[optimal_value_index:]))
                    if optimal_value_substr.isdigit():
                        instance.optimal_value = int(optimal_value_substr)
            elif line.startswith("TYPE"):
                instance.type = line.split(":")[1].strip()
            elif line.startswith("DIMENSION"):
                instance.dimension = int(line.split(":")[1].strip())
            elif line.startswith("EDGE_WEIGHT_TYPE"):
                instance.edge_weight_type = line.split(":")[1].strip()
            elif line.startswith("CAPACITY"):
                instance.capacity = int(line.split(":")[1].strip())

            elif line.strip() == "NODE_COORD_SECTION":
                break

        for line in file:
            if line.strip() == "DEMAND_SECTION":
                break
            node_id, x, y = map(int, line.split())
            instance.node_coords[node_id] = (x, y)

        for line in file:
            if line.strip() == "DEPOT_SECTION":
                break
            node_id, demand = map(int, line.split())
            instance.demands[node_id] = demand

        for line in file:
            if line.strip() == "EOF":
                break
            if line.strip() != "-1":
                instance.depot = int(line.strip())

    instance.calculate_distance_matrix()
    return instance



# file_path = "instances/A-n64-k9.txt"
# cvrp_instance = read_cvrp_instance(file_path)
# if cvrp_instance is not None:
#     print("Nombre:", cvrp_instance.name)
#     print("Comentario:", cvrp_instance.comment)
#     print("Número de camiones:", cvrp_instance.no_of_trucks)
#     print("Valor óptimo:", cvrp_instance.optimal_value)
#     print("Tipo:", cvrp_instance.type)
#     print("Dimensión:", cvrp_instance.dimension)
#     print("Tipo de peso de arista:", cvrp_instance.edge_weight_type)
#     print("Capacidad:", cvrp_instance.capacity)
#     print("Coordenadas de los nodos:", cvrp_instance.node_coords)
#     print("Demandas de los nodos:", cvrp_instance.demands)
#     print("Depósito:", cvrp_instance.depot)
#     #print("\nMatriz de distancias:")
#     #for row in cvrp_instance.distance_matrix:
#     #    print(row)
# else:
#     print("Error: No se pudo leer la instancia.")
def resolver_cvrp(cvrp_instance):
    cvrp_solver = CVRP(cvrp_instance.distance_matrix, list(cvrp_instance.demands.values()), cvrp_instance.capacity)
    cvrp_solver.resolver()
    rutas = cvrp_solver.rutas
    distancia_total = sum(cvrp_solver.calcular_distancia(ruta) for ruta in rutas)
    return rutas, distancia_total

file_path = "instances/A-n64-k9.txt"
cvrp_instance = read_cvrp_instance(file_path)
if cvrp_instance is not None:
    print("Datos de la instancia:")
    print(f"Nombre: {cvrp_instance.name}")
    print(f"Comentario: {cvrp_instance.comment}")
    print(f"Número de camiones: {cvrp_instance.no_of_trucks}")
    print(f"Valor óptimo: {cvrp_instance.optimal_value}")
    print(f"Tipo: {cvrp_instance.type}")
    print(f"Dimensión: {cvrp_instance.dimension}")
    print(f"Tipo de peso de arista: {cvrp_instance.edge_weight_type}")
    print(f"Capacidad: {cvrp_instance.capacity}")
    print(f"Coordenadas de los nodos: {cvrp_instance.node_coords}")
    print(f"Demandas de los nodos: {cvrp_instance.demands}")
    print(f"Depósito: {cvrp_instance.depot}")

    rutas, distancia_total = resolver_cvrp(cvrp_instance)
    print("\nRutas finales:")
    for i, ruta in enumerate(rutas):
        print(f"Ruta {i + 1}: {ruta}")
    print(f"Distancia total recorrida: {distancia_total}")
else:
    print("Error: No se pudo leer la instancia.")


def resolver_cvrp(cvrp_instance):
    # Construir rutas iniciales
    cvrp_solver = CVRP(cvrp_instance.distance_matrix, list(cvrp_instance.demands.values()), cvrp_instance.capacity)
    cvrp_solver.resolver()

    # Guardar resultados
    rutas = cvrp_solver.rutas
    distancia_total = cvrp_solver.calcular_distancia(rutas)

    return rutas, distancia_total


cvrp_solver = CVRP(cvrp_instance.distance_matrix, list(cvrp_instance.demands.values()), cvrp_instance.capacity)
cvrp_solver.resolver()