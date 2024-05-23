import math

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
        num_nodes = self.dimension
        self.distance_matrix = [[0] * num_nodes for _ in range(num_nodes)]
        for i in range(1, num_nodes + 1):
            for j in range(1, num_nodes + 1):
                if i != j:
                    self.distance_matrix[i - 1][j - 1] = self.euclidean_distance(self.node_coords[i], self.node_coords[j])

    @staticmethod
    def euclidean_distance(coord1, coord2):
        x1, y1 = coord1
        x2, y2 = coord2
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def read_cvrp_instance(file_path):
    instance = CVRPInstance()
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith("NAME"):
                instance.name = line.split(":")[1].strip()
            elif line.startswith("COMMENT"):
                instance.comment = line.split(":")[1].strip()
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
            elif line == "NODE_COORD_SECTION":
                break

        #print("Leyendo NODE_COORD_SECTION")
        for line in file:
            line = line.strip()
            if line == "DEMAND_SECTION":
                break
            node_id, x, y = map(int, line.split())
            instance.node_coords[node_id] = (x, y)
            #print(f"Leído nodo: {node_id}, Coordenadas: ({x}, {y})")

        #print("Leyendo DEMAND_SECTION")
        for line in file:
            line = line.strip()
            if line == "DEPOT_SECTION":
                break
            node_id, demand = map(int, line.split())
            instance.demands[node_id] = demand
            #print(f"Leído nodo: {node_id}, Demanda: {demand}")

        #print("Leyendo DEPOT_SECTION")
        for line in file:
            line = line.strip()
            if line == "EOF":
                break
            if line != "-1":
                instance.depot = int(line)
                #
                print(f"Leído depósito: {instance.depot}")

    instance.calculate_distance_matrix()
    return instance