from cvrp_instance import read_cvrp_instance
from cvrp import CVRP

def resolver_cvrp(cvrp_instance):
    cvrp_solver = CVRP(cvrp_instance.distance_matrix, list(cvrp_instance.demands.values()), cvrp_instance.capacity)
    cvrp_solver.resolver()
    rutas = cvrp_solver.rutas
    distancia_total = sum(cvrp_solver.calcular_distancia(ruta) for ruta in rutas)
    cargas = [sum(cvrp_instance.demands[nodo] for nodo in ruta if nodo != 0) for ruta in rutas]
    distancias = [cvrp_solver.calcular_distancia(ruta) for ruta in rutas]
    return rutas, distancias, cargas, distancia_total

# Función principal para ejecutar múltiples veces y obtener los mejores resultados
def ejecutar_multiple_veces(cvrp_instance, n):
    mejor_rutas = None
    mejor_distancias = None
    mejor_cargas = None
    menor_distancia_total = float('inf')

    for _ in range(n):

        cvrp_solver = CVRP(cvrp_instance.distance_matrix, list(cvrp_instance.demands.values()), cvrp_instance.capacity)
        rutas = cvrp_solver.resolver()
        distancias = [cvrp_solver.calcular_distancia(ruta) for ruta in rutas]
        cargas = [sum(cvrp_instance.demands[nodo] for nodo in ruta[1:-1]) for ruta in rutas]
        distancia_total = sum(distancias)

        if distancia_total < menor_distancia_total:
            mejor_rutas = rutas
            mejor_distancias = distancias
            mejor_cargas = cargas
            menor_distancia_total = distancia_total

    return mejor_rutas, mejor_distancias, mejor_cargas, menor_distancia_total


if __name__ == "__main__":
    file_path = "instances/A-n32-k5.txt"
    cvrp_instance = read_cvrp_instance(file_path)
    # print("Matriz de distancia:")
    # for row in cvrp_instance.distance_matrix:
    #     print(row)
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
        print(f"Demanda total: {sum(cvrp_instance.demands.values())}")
        print(f"Depósito: {cvrp_instance.depot}")

        n = 1  # Número de veces que quieres ejecutar el algoritmo
        mejores_rutas, mejores_distancias, mejores_cargas, menor_distancia = ejecutar_multiple_veces(cvrp_instance, n)

        print("\nMejor conjunto de rutas:")
        carga_total = 0
        for i, (ruta, distancia, carga) in enumerate(zip(mejores_rutas, mejores_distancias, mejores_cargas)):
            print(f"Ruta {i + 1}: {ruta}")
            print(f"Ruta {i + 1}: Distancia = {distancia}, Carga del vehículo = {carga}")
            carga_total += carga

        print(f"\nRecorrido total de rutas: {menor_distancia}")
        print(f"Carga total de vehículos: {carga_total}")
    else:
        print("Error: No se pudo leer la instancia.")