import numpy as np


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

    return instance


def calculate_distances(node_coords):
    """
    Calcula la matriz de distancias euclidianas entre todos los nodos.

    Args:
        node_coords (dict): Diccionario que contiene las coordenadas (X, Y) de cada nodo.

    Returns:
        numpy.ndarray: Matriz de distancias euclidianas.
    """
    distances = np.zeros((len(node_coords), len(node_coords)))
    for i in range(len(node_coords)):
        for j in range(i + 1, len(node_coords)):
            x1, y1 = node_coords[i + 1]
            x2, y2 = node_coords[j + 1]
            distances[i, j] = distances[j, i] = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    return distances


class CVRP:
    def __init__(self, distancias, demandas, capacidad_vehiculo):
        self.distancias = distancias
        self.demandas = demandas
        self.capacidad_vehiculo = capacidad_vehiculo
        self.num_clientes = len(distancias)
        self.rutas = []

    def encontrar_cliente_mas_cercano(self, clientes_disponibles):
        distancia_minima = float('inf')
        cliente
