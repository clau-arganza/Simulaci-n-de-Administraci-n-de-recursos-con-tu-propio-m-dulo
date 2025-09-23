MATERIALES = ["ladrillo", "ventanas", "rejas", "cemento", "madera"]

recursos = [800, 100, 120, 500, 500]
edificios = {
        "zara":             [200, 10, 1,   100, 50],
        "tienda de cómics": [100,  2, 5,    50, 25],
        "manicomio":        [300, 30, 100, 150, 100],
    }
edificios_creados=[]


def mostrar_recursos():
    print("\n=== Recursos disponibles ===")
    for nombre, cant in zip(MATERIALES, recursos):
        print(f"- {nombre}: {cant}")
    
 
def mostrar_edificios():
    print("\n=== Edificios disponibles (costes) ===")
    for (nombre, coste) in edificios.items():
        lista_materiales=""
        for m, c in zip(MATERIALES, coste):
            lista_materiales+=", "+f"{m}:{c}"
        print(f"{nombre} -> {lista_materiales}")
        

def buscar_edificios(nombre): 
    
    if nombre in edificios: 
        cant_mat=edificios[nombre]
        crear_edificio(cant_mat,nombre)    
    else:          
        print("no existe el Edificio")
    
def crear_edificio(cant_mat,nombre):
    suficiente=1
    for e,r in zip(cant_mat,recursos):
        if not r>=e:
            print ("No tienes Materiales suficientes")
            suficiente=0
    if suficiente>0:
        for x, valor in enumerate(recursos):
            valor-=cant_mat[x]
            if valor>-1 :
                recursos[x]=valor
        edificios_creados.append(nombre) 
        if  len(edificios_creados) > 1:
            print(f"\n=== Edificios creados es {edificios_creados}  ===\n")    
        else:    
            print(f"\n=== El edificio creado es {edificios_creados}  ===\n")        
        print("\n=== Materiales restantes ===")
        for nombre, cant in zip(MATERIALES, recursos):
            print(f"- {nombre}: {cant}")   
    
    
    
def main():
    while True:
        mostrar_recursos()
        mostrar_edificios()
    
        eleccion = input("\nElige un edificio (nombre): ").lower()
    
        buscar_edificios(eleccion)
        sino=input("quieres seguir construyendo edificios S/N").lower()
       
        if sino == "n":
            break
        
    
    
if __name__ == "__main__":
    main()