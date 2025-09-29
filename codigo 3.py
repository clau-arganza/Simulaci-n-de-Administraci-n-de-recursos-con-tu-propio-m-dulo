MATERIALES = ["ladrillo", "ventanas", "rejas", "cemento", "madera"]

recursos = [800, 100, 120, 500, 500]
horas=[500,200,1000]
edificios = {
        "zara":             [200, 10, 0,   100, 50],
        "tienda de cómics": [100,  2, 1,    50, 25],
        "manicomio":        [300, 30, 100, 150, 100],
    }
edificios_creados=[]
edificios_hora={}
def unir_horarios():
    for (en,ec),h in zip(edificios.items(), horas):
        edificios_hora[en]=h
        

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
        crear_edificio(edificios[nombre],nombre)    
    else:          
        print("no existe el Edificio")
    
def crear_edificio(edificio,nombre):
    suficiente=1
    for e,r in zip(edificio,recursos):
        if not r>=e:
            print ("No tienes Materiales suficientes")
            suficiente=0
    if suficiente>0:
        for x, valor in enumerate(recursos):
            valor-=edificio[x]
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

def calculo_temporal(eleccion,personal):
    if eleccion in edificios_hora:
        #print(f"{eleccion}:{edificios_hora[eleccion]}")
        tiempo=int(edificios_hora[eleccion])
        dias= round((round(tiempo/int(personal)))/8)
        print(f"Trabajando en el edificio {eleccion} un numero de {personal} trabajadores tardaron un total de {dias} dias (con una jornada de 8 hs)")

def calculo_total(personal): 
    total=0  
    for n,v in edificios_hora.items():
        total+=int(v)
    
    dias= round((round(int(total)/int(personal)))/8)
    print(f"Trabajando en los edificios un numero de {personal} trabajadores tardaron un total de {dias} dias (con una jornada de 8 hs)")  
    
def main():
    while True:
        mostrar_recursos()
        mostrar_edificios()
        unir_horarios()
        print("Tiempo de construccion de edificios por hras:")
        print(edificios_hora)
        eleccion = input("\nElige un edificio (nombre): ").lower()
        personal=int(input("Cuantos obreros quieres asignar: "))
        
    
        buscar_edificios(eleccion)
        calculo_temporal(eleccion,personal)
        calculo_total(personal)
        sino=input("quieres seguir construyendo edificios S/N").lower()
       
        if sino == "n":
            break
        
    
    
if __name__ == "__main__":
    main()