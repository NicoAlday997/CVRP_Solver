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


# Ejemplo de uso
file_path = "instances/A-n32-k5.txt"
cvrp_instance = read_cvrp_instance(file_path)
if cvrp_instance is not None:
    print("Nombre:", cvrp_instance.name)
    print("Comentario:", cvrp_instance.comment)
    print("Número de camiones:", cvrp_instance.no_of_trucks)
    print("Valor óptimo:", cvrp_instance.optimal_value)
    print("Tipo:", cvrp_instance.type)
    print("Dimensión:", cvrp_instance.dimension)
    print("Tipo de peso de arista:", cvrp_instance.edge_weight_type)
    print("Capacidad:", cvrp_instance.capacity)
    print("Coordenadas de los nodos:", cvrp_instance.node_coords)
    print("Demandas de los nodos:", cvrp_instance.demands)
    print("Depósito:", cvrp_instance.depot)
else:
    print("Error: No se pudo leer la instancia.")
