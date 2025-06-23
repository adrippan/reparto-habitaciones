#!/usr/bin/env python3
import heapq
import json
import sys

def repartoHabitaciones(h, g):
    def cota_optimista(estado):
        asig, habs = estado
        habitaciones_vacias = len(habs) - len(set(asig))
        return habitaciones_vacias

    def branch(estado):
        asig, habs = estado
        hijos = []
        idx = len(asig)
        for hab, capacidad in enumerate(habs):
            if g[idx] <= capacidad:
                chico = (idx % 2 == 0)
                habs_chicos = [h for pos, h in enumerate(asig) if pos % 2 == 0]
                habs_chicas = [h for pos, h in enumerate(asig) if pos % 2 != 0]
                if (chico and hab not in habs_chicas) or (not chico and hab not in habs_chicos):
                    habs_new = habs.copy()
                    habs_new[hab] -= g[idx]
                    opt = cota_optimista((asig + [hab], habs_new))
                    hijos.append((opt, (asig + [hab], habs_new)))
        return hijos

    def is_complete(estado):
        return len(estado[0]) == len(g)

    A = []
    fx = 0
    ini = ([], h.copy())
    heapq.heappush(A, (-cota_optimista(ini), ini))

    while A and -A[0][0] > fx:
        _, s = heapq.heappop(A)
        for child_score, child in branch(s):
            if is_complete(child):
                if child_score > fx:
                    fx, x = child_score, child
            else:
                if child_score > fx:
                    heapq.heappush(A, (-child_score, child))
    return x, fx

def impirmir_asignacion(asignacion, vacias, capacidades_restantes, mapping):
    for i, hab in enumerate(asignacion):
        grupo_original = i // 2
        genero = "CHICOS" if i % 2 == 0 else "CHICAS"
        print(f"G{grupo_original+1}: {genero} en habitación {mapping.get(str(hab), hab)}")
    print(f"Número de habitaciones vacías: {vacias}")
    print("Capacidades restantes por habitación:", capacidades_restantes)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: repartoHabitaciones.py [h] [g] [mapping]")
        print('Ejemplo: repartoHabitaciones.py "[20,6,8]" "[20,3,4]" "{\"0\":\"C\",\"1\":\"A\"}"')
        sys.exit(1)
    h = json.loads(sys.argv[1])
    g = json.loads(sys.argv[2])
    mapping = json.loads(sys.argv[3])
    sol, vacias = repartoHabitaciones(h, g)
    impirmir_asignacion(sol[0], vacias, sol[1], mapping)
