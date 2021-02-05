from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot
f = with open("entrenador.txt","r")
datos_entrenamiento = []
for linea in f.readlines:
    datos_entrenamiento.append(linea)
chatbot.train(datos_entrenamiento)

