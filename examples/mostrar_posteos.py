import json


def leer_posteos():

    # POST: Carga la información del json y la retorna.

    with open("wto_posts.json", "r") as posteos:

        # El json.load carga la información y crea 
        # una lista de diccionarios, la cual es 
        # atrapada en lista_posteos_info.

        lista_posteos_info = json.load(posteos)

        return lista_posteos_info

        
def mostrar_posteos(lista_posteos_info):

    # PRE: Recibe lista_posteos_info que es 
    # una lista de diccionarios (llena).

    # POST: Recorre la lista y printea los datos
    #  solicitados de los diccionarios correspondientes.

    for posteo in range(len(lista_posteos_info)):

        for llave in lista_posteos_info[posteo]:

            if llave == "message":
                print(f"Publicación: {lista_posteos_info[posteo]['message']}")

            if llave == "like":
                print(f"Cantidad de likes: {lista_posteos_info[posteo]['like']['summary']['total_count']}\n")

            elif llave == "picture":
                print("Esta publicación es una foto.")
            

def main():
    mostrar_posteos(leer_posteos())

main()
