import random
import math

class CVRP:
    def __init__(self, distancias, demandas, capacidad_vehiculo):
        self.distancias = distancias
        self.demandas = demandas
        self.capacidad_vehiculo = capacidad_vehiculo
        self.num_clientes = len(distancias)  # Incluyendo el depósito
        self.rutas = []
        self.cargas = []

        print("Demandas inicializadas: ")
        print(self.demandas)

    def encontrar_cliente_mas_cercano(self, cliente_actual, clientes_disponibles):
        distancia_minima = float('inf')
        cliente_mas_cercano = None
        for cliente in clientes_disponibles:
            distancia = self.distancias[cliente_actual - 1][cliente - 1]
            if distancia < distancia_minima:
                distancia_minima = distancia
                cliente_mas_cercano = cliente
        return cliente_mas_cercano

    def construir_rutas(self):
        clientes_no_asignados = list(range(2, self.num_clientes + 1))
        self.rutas = []
        self.cargas = []

        while clientes_no_asignados:
            print(f"\nClientes no asignados: {clientes_no_asignados}")
            ruta_actual = [1]
            capacidad_restante = self.capacidad_vehiculo

            cliente_inicial = random.choice(clientes_no_asignados)
            print(f"Cliente inicial seleccionado: {cliente_inicial} con demanda {self.demandas[cliente_inicial - 1]}")
            if self.demandas[cliente_inicial - 1] > capacidad_restante:
                print(f"Demanda del cliente inicial {cliente_inicial} excede la capacidad restante")
                continue
            ruta_actual.append(cliente_inicial)
            capacidad_restante -= self.demandas[cliente_inicial - 1]
            clientes_no_asignados.remove(cliente_inicial)
            print(f"Ruta actual: {ruta_actual}, Capacidad restante: {capacidad_restante}")

            while capacidad_restante > 0 and clientes_no_asignados:
                cliente_mas_cercano = self.encontrar_cliente_mas_cercano(ruta_actual[-1], clientes_no_asignados)
                if cliente_mas_cercano is None or self.demandas[cliente_mas_cercano - 1] > capacidad_restante:
                    print(f"Cliente {cliente_mas_cercano} no puede ser añadido (demanda excede la capacidad restante)")
                    break
                print(f"Cliente actual: {ruta_actual[-1]}, Cliente más cercano: {cliente_mas_cercano}, Distancia mínima: {self.distancias[ruta_actual[-1] - 1][cliente_mas_cercano - 1]}")
                print(f"Cliente más cercano encontrado: {cliente_mas_cercano} con demanda {self.demandas[cliente_mas_cercano - 1]}")
                ruta_actual.append(cliente_mas_cercano)
                capacidad_restante -= self.demandas[cliente_mas_cercano - 1]
                clientes_no_asignados.remove(cliente_mas_cercano)
                print(f"Ruta actual: {ruta_actual}, Capacidad restante: {capacidad_restante}")

            ruta_actual.append(1)
            self.rutas.append(ruta_actual)
            self.cargas.append(self.capacidad_vehiculo - capacidad_restante)
            print(f"Ruta finalizada: {ruta_actual}, Carga de la ruta: {self.capacidad_vehiculo - capacidad_restante}")

        # Verificar si todos los clientes han sido asignados
        clientes_asignados = set()
        for ruta in self.rutas:
            clientes_asignados.update(ruta[1:-1])
        no_asignados = set(range(2, self.num_clientes + 1)) - clientes_asignados
        if no_asignados:
            print(f"Clientes no asignados al final de la construcción: {no_asignados}")
            for cliente in no_asignados:
                self.rutas.append([1, cliente, 1])
                self.cargas.append(self.demandas[cliente - 1])

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
                        nueva_ruta1 = self.rutas[i][:]
                        nueva_ruta2 = self.rutas[j][:]
                        nueva_ruta1[nueva_ruta1.index(cliente_ruta1)] = cliente_ruta2
                        nueva_ruta2[nueva_ruta2.index(cliente_ruta2)] = cliente_ruta1
                        carga_nueva_ruta1 = sum(self.demandas[cliente - 1] for cliente in nueva_ruta1[1:-1])
                        carga_nueva_ruta2 = sum(self.demandas[cliente - 1] for cliente in nueva_ruta2[1:-1])
                        if carga_nueva_ruta1 <= self.capacidad_vehiculo and carga_nueva_ruta2 <= self.capacidad_vehiculo:
                            if self.calcular_distancia(nueva_ruta1) + self.calcular_distancia(nueva_ruta2) < self.calcular_distancia(self.rutas[i]) + self.calcular_distancia(self.rutas[j]):
                                self.rutas[i] = nueva_ruta1
                                self.rutas[j] = nueva_ruta2
                                self.cargas[i] = carga_nueva_ruta1
                                self.cargas[j] = carga_nueva_ruta2
                                break

    def calcular_distancia(self, ruta):
        distancia_total = 0
        for i in range(len(ruta) - 1):
            distancia_total += self.distancias[ruta[i] - 1][ruta[i + 1] - 1]
        return distancia_total

    def rutas_iguales(self, rutas1, rutas2):
        if len(rutas1) != len(rutas2):
            return False
        for ruta1, ruta2 in zip(rutas1, rutas2):
            if ruta1 != ruta2:
                return False
        return True

    def resolver(self):
        self.construir_rutas()
        print("\nRutas iniciales: ")
        self.imprimir_rutas()
        while True:
            rutas_anteriores = self.rutas.copy()  # Copia superficial
            cargas_anteriores = self.cargas.copy()  # Copia superficial
            self.mejorar_rutas_localmente()
            self.intercambiar_nodos_entre_rutas()
            if self.rutas_iguales(self.rutas, rutas_anteriores) and self.cargas == cargas_anteriores:
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
                    nueva_ruta = [1] + self.rutas[i][1:-1] + self.rutas[j][1:-1] + [1]
                    carga_total = sum(self.demandas[cliente - 1] for cliente in nueva_ruta[1:-1])
                    if carga_total <= self.capacidad_vehiculo:
                        self.rutas.append(nueva_ruta)
                        del self.rutas[j]
                        del self.rutas[i]
                        self.cargas.append(carga_total)
                        del self.cargas[j]
                        del self.cargas[i]
                        fusion = True
                        break
                if fusion:
                    break

    def imprimir_rutas(self):
        for i, ruta in enumerate(self.rutas):
            print(f"Ruta {i + 1}: {ruta}")

        distancia_total = 0
        carga_total = 0
        for i, ruta in enumerate(self.rutas):
            distancia_ruta = self.calcular_distancia(ruta)
            carga_vehiculo = sum(self.demandas[cliente - 1] for cliente in ruta[1:-1])
            print(f"Ruta {i + 1}: Distancia = {distancia_ruta}, Carga del vehículo = {carga_vehiculo}")
            distancia_total += distancia_ruta
            carga_total += carga_vehiculo
        print(f"Recorrido total de rutas: {distancia_total}")
        print(f"Carga total de vehículos: {carga_total}")
