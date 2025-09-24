import networkx as nx
import matplotlib.pyplot as plt

# 1. Configuración inicial
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

# Definición de opciones y costos
opciones_por_tipo = {
    'construcciones': {
        'zara': 100,
        'tienda_de_comics': 100,
        'libreria': 100
    },
    'recursos': {
        'mineria': 300,
        'tala_arboles': 50,
        'energia': 150
    },
    'servicios': {
        'escuela': 100,
        'biblioteca': 100,
        'parques': 50,
        'rehabilitacion': 50,
        'asilo': 80
    }
}

pos = {
    'Construcciones': (-5, 0),
    'Recursos': (0, 0),
    'Servicios': (5, 0)
}


# 3. Bucle del juego
while dinero > 0:
    print("\n--- Estado Actual ---")
    print(f"Dinero disponible: {dinero}")
    print("Opciones de gasto:")

    opciones_disponibles = {}
    for tipo, opciones in opciones_por_tipo.items():
        print(f"\nTipo: {tipo.capitalize()} (Color: {colores_por_tipo[tipo]})")
        for opcion, costo in opciones.items():
            if dinero >= costo:
                print(f"  - {opcion} (Costo: {costo})")
                opciones_disponibles[opcion] = {'costo': costo, 'tipo': tipo}

    if not opciones_disponibles:
        print("\n¡No tienes suficiente dinero para ninguna opción! El juego ha terminado.")
        break
        
    eleccion = input("\nElige una opción para construir (o 'salir' para terminar): ").lower()
    
    if eleccion == 'salir':
        print("Fin del juego.")
        break

    if eleccion in opciones_disponibles:
        opcion_elegida = opciones_disponibles[eleccion]
        costo = opcion_elegida['costo']
        tipo = opcion_elegida['tipo']
        
        # 4. Lógica de compra y actualización del grafo
        if dinero >= costo:
            dinero -= costo
            
            # Agregamos el nuevo nodo con sus atributos
            G.add_node(eleccion, tipo=tipo, color=colores_por_tipo[tipo])
            
            # Conectamos el nuevo nodo al nodo principal de su categoría
            if tipo == 'construcciones':
                G.add_edge('Construcciones', eleccion)
            elif tipo == 'recursos':
                G.add_edge('Recursos', eleccion)
            elif tipo == 'servicios':
                G.add_edge('Servicios', eleccion)

            print(f"¡Has construido {eleccion}! Dinero restante: {dinero}")
            
            # Visualización del grafo actualizada
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