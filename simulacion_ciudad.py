import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import time

# 1. Configuración inicial
MATERIALES = ["ladrillo", "ventanas", "rejas", "cemento", "madera"]
G = nx.DiGraph()
dinero = 800
# Diccionario de colores por tipo de nodo
colores_por_tipo = {
    'construcciones': 'red',
    'recursos': 'green',
    'servicios': 'blue'
}

# Definición de nodos principales y sus atributos
nodos_principales = {
    'Construcciones': 'construcciones',
    'Recursos': 'recursos',
    'Servicios': 'servicios'
}

for nodo, tipo in nodos_principales.items():
    G.add_node(nodo, tipo=tipo, color=colores_por_tipo[tipo])

# Definición de opciones y sus atributos: costo, tiempo y obreros
opciones_por_tipo = {
    'construcciones': {
        'zara': {'costo': 100, 'tiempo': 30, 'obreros': 5},
        'tienda_de_comics': {'costo': 100, 'tiempo': 25, 'obreros': 4},
        'libreria': {'costo': 100, 'tiempo': 20, 'obreros': 3}
    },
    'recursos': {
        'mineria': {'costo': 300, 'tiempo': 60, 'obreros': 10},
        'tala_arboles': {'costo': 50, 'tiempo': 15, 'obreros': 2},
        'energia': {'costo': 150, 'tiempo': 45, 'obreros': 7}
    },
    'servicios': {
        'escuela': {'costo': 100, 'tiempo': 50, 'obreros': 8},
        'biblioteca': {'costo': 100, 'tiempo': 40, 'obreros': 6},
        'parques': {'costo': 50, 'tiempo': 10, 'obreros': 2},
        'rehabilitacion': {'costo': 50, 'tiempo': 20, 'obreros': 3},
        'asilo': {'costo': 80, 'tiempo': 35, 'obreros': 5}
    }
}

pos = {
    'Construcciones': (-5, 0),
    'Recursos': (0, 0),
    'Servicios': (5, 0)
}

# Lista para llevar un registro de las construcciones en proceso
construcciones_en_proceso = []

# Función para duplicar obreros y reducir el tiempo
def duplicar_obreros(construccion):
    """Duplica el número de obreros y reduce el tiempo de construcción a la mitad."""
    if 'obreros' in construccion and 'tiempo' in construccion:
        construccion['obreros'] *= 2
        construccion['tiempo'] /= 2
        print(f"\n¡Se han duplicado los obreros para '{construccion['nombre']}'! Ahora hay {construccion['obreros']} obreros y el tiempo restante es de {construccion['tiempo']} días.")

# 3. Bucle del juego
while dinero > 0:
    print("\n--- Estado Actual ---")
    print(f"Dinero disponible: {dinero}")
    print("Opciones de gasto:")

    opciones_disponibles = {}
    for tipo, opciones in opciones_por_tipo.items():
        print(f"\nTipo: {tipo.capitalize()} (Color: {colores_por_tipo[tipo]})")
        for opcion, atributos in opciones.items():
            costo = atributos['costo']
            tiempo = atributos['tiempo']
            obreros = atributos['obreros']
            if dinero >= costo:
                print(f"  - {opcion} (Costo: {costo}, Tiempo: {tiempo} días, Obreros: {obreros})")
                opciones_disponibles[opcion] = {'costo': costo, 'tipo': tipo, 'tiempo': tiempo, 'obreros': obreros}

    if not opciones_disponibles:
        print("\n¡No tienes suficiente dinero para ninguna opción! El juego ha terminado.")
        break
    
    # Mostrar construcciones en proceso
    if construcciones_en_proceso:
        print("\n--- Construcciones en Proceso ---")
        for obra in construcciones_en_proceso:
            print(f"  - {obra['nombre']} | Tiempo restante: {obra['tiempo']} días | Obreros: {obra['obreros']}")

    eleccion = input("\nElige una opción para construir, 'obreros' para duplicar, o 'salir' para terminar: ").lower()
    
    if eleccion == 'salir':
        print("Fin del juego.")
        break

    if eleccion == 'obreros':
        if not construcciones_en_proceso:
            print("No hay construcciones en proceso para duplicar obreros.")
            continue
        
        nombre_obra = input("Ingresa el nombre de la obra para duplicar obreros: ").lower()
        
        obra_encontrada = None
        for obra in construcciones_en_proceso:
            if obra['nombre'] == nombre_obra:
                obra_encontrada = obra
                break
        
        if obra_encontrada:
            duplicar_obreros(obra_encontrada)
        else:
            print("Nombre de obra no válido.")
        continue

    if eleccion in opciones_disponibles:
        opcion_elegida = opciones_disponibles[eleccion]
        costo = opcion_elegida['costo']
        tipo = opcion_elegida['tipo']
        tiempo = opcion_elegida['tiempo']
        obreros = opcion_elegida['obreros']
        
        print(f"\nLa construcción de '{eleccion}' tardará {tiempo} días con {obreros} obreros.")
        respuesta = input("¿Quieres duplicar el número de obreros para reducir el tiempo a la mitad? (sí/no): ").lower()

        if respuesta == 'si' or respuesta == 'sí':
            tiempo /= 2
            obreros *= 2
            print(f"¡Genial! El nuevo tiempo de construcción es de {tiempo} días con {obreros} obreros.")
        
        
        # 4. Lógica de compra y actualización del grafo
        if dinero >= costo:
            dinero -= costo
            
            print(f"\nIniciando la construcción de {eleccion}...")
            
            # --- BUCLE PARA SIMULAR EL PASO DEL TIEMPO Y NOTIFICAR ---
            tiempo_transcurrido = 0
            mitad_notificada = False
            while tiempo_transcurrido < tiempo:
                # Simula el paso de 1 segundo (o 1 día de construcción)
                time.sleep(1)
                tiempo_transcurrido += 2
                
                # Revisa si se ha alcanzado la mitad del tiempo
                if not mitad_notificada and tiempo_transcurrido >= tiempo / 2:
                    print(f"¡Atención! La construcción de '{eleccion}' ha alcanzado la mitad del tiempo ({int(tiempo / 2)} días).")
                    mitad_notificada = True
            # Fin del bucle de tiempo
            
            # Agregamos la obra a la lista de construcciones en proceso
            nueva_obra = {'nombre': eleccion, 'tiempo': tiempo, 'obreros': obreros}
            construcciones_en_proceso.append(nueva_obra)
            
            # Agregamos el nuevo nodo con sus atributos
            G.add_node(eleccion, tipo=tipo, color=colores_por_tipo[tipo])
            
            # Conectamos el nuevo nodo al nodo principal de su categoría
            if tipo == 'construcciones':
                G.add_edge('Construcciones', eleccion)
            elif tipo == 'recursos':
                G.add_edge('Recursos', eleccion)
            elif tipo == 'servicios':
                G.add_edge('Servicios', eleccion)

            print(f"¡Has terminado de construir {eleccion}! Costo: {costo}. Dinero restante: {dinero}")
            
            plt.figure(figsize=(12, 10))
            
            # Actualizamos las posiciones de los nuevos nodos para que no se superpongan
            pos = nx.circular_layout(G)
            
            # Obtenemos los colores para la visualización
            node_colors = [data['color'] for node, data in G.nodes(data=True)]
            
            # Dibujamos el grafo
            nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=2000, font_size=10, font_color='white')
            plt.title("Grafo de la Red de Inversiones")
            plt.show()
        else:
            print("No tienes suficiente dinero para esa compra.")
    else:
        print("Opción no válida. Por favor, elige una de las opciones disponibles.")

print("\n--- ¡Juego Terminado! ---")
