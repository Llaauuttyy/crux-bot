from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

# Create a new chat bot named Charlie
chatbot = ChatBot('Charlie')

trainer = ListTrainer(chatbot)

trainer.train([
    "Hola, quiero que me muestres las fotos de un amigo",
    "Perfecto, escriba su nombre",
    "El nombre es Juan",
    "Estas son las fotos de Juan: "
    "joyita paaaaaaaa",
])
me = input("habla: ")
response = chatbot.get_response(me)
print(response)
# Get a response to the input text 'I would like to book a flight.'


