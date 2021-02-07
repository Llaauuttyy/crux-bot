from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

# Create a new chat bot named Charlie
chatbot = ChatBot('Charlie')

trainer = ListTrainer(chatbot)

trainer.train([
    "Hola",
    "Hola, soy crux. En que te puedo ayudar?",
    "Quiero que me muestres las fotos de un amigo",
    "Perfecto, escriba su nombre",
    "El nombre es Juan",
    "Estas son las fotos de Juan: ",
    "Muchas gracias",
    "Quiero que me imprimas mi lista de amigos",
    "Tu lista de amigos es la siguiente: ",
    "Quiero que le des me gusta a la foto de un amigo",
    "Necesito que me digas el nombre de tu amigo y la fecha de la foto",
    "Quiero que actualices los datos de mi perfil"
    "Datos de perfil actualizados"
])

end_program = False
while not end_program:
    me = input("User: ")
    response = chatbot.get_response(me)
    print("Crux: ",response)
    if yo == "Bye":
        print("Crux: Bye")
        end_program = True

f = with open("entrenador.txt","r")
datos_entrenamiento = []
for linea in f.readlines:
    datos_entrenamiento.append(linea)
chatbot.train(datos_entrenamiento)