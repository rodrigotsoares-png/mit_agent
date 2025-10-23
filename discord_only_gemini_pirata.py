from dotenv import load_dotenv
from google import genai
from google.genai import types 
import discord
import os

# Load environment variables from a .env file
load_dotenv()
# Utiliza a chave da API do Gemini. 
# A variável GOOGLE_API_KEY ou GEMINI_API_KEY no .env são as mais comuns.
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY') 

# Inicializa o cliente Gemini
# Passamos a chave explicitamente
try:
    genai_client = genai.Client(api_key=GEMINI_API_KEY) 
except Exception as e:
    print(f"Erro ao inicializar o cliente Gemini: {e}")
    # Você pode querer sair ou lidar com isso de outra forma
    exit()


# ask gemini - respond like a pirate
def call_gemini(question):
    # O modelo 'gemini-2.5-flash' é recomendado para respostas rápidas e conversas
    model_name = "gemini-2.5-flash" 
    
    # Instrução de sistema para definir o papel (pirata)
    system_instruction = "Você é um pirata mal-humorado e aventureiro. Responda a todas as perguntas como um pirata, usando jargão pirata e um tom brincalhão."

    try:
        # Chama a API do Gemini
        response = genai_client.models.generate_content(
            model=model_name,
            # Conteúdo Simplificado: 
            # Basta passar a string da pergunta diretamente, sem necessidade de Part.from_text
            contents=[question], 
            config=types.GenerateContentConfig(
                # Usa a instrução de sistema para garantir o estilo "pirata"
                system_instruction=system_instruction
            )
        )

        # Acessa o texto da resposta
        response_text = response.text
        print(response_text)
        return response_text
        
    except Exception as e:
        # Tratamento de erro aprimorado
        print(f"Erro ao chamar a API do Gemini: {e}")
        return "Ahoy! Algo deu errado na comunicação com o mar! Verifique a chave da API e a conexão. 🏴‍☠️"

# ---
#  Set up intents
intents = discord.Intents.default()
intents.message_content = True # Permite que o bot leia o conteúdo das mensagens
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    # Exemplo de como o nome do bot pode aparecer no log:
    # We have logged in as PirateBot#1234

@client.event
async def on_message(message):
    # Ignora mensagens enviadas pelo próprio bot
    if message.author == client.user:
        return

    # Comando de teste simples
    if message.content.startswith('!hello'):
        await message.channel.send('Argh, saudações, marinheiro!')

    # Comando principal para perguntar ao Gemini
    if message.content.startswith('$question'):
        # Garante que haja algo após o comando
        if len(message.content.split("$question", 1)) < 2:
             await message.channel.send("Capitão, você esqueceu a pergunta!")
             return
             
        print(f"Message: {message.content}")
        # Tratamento de string para extrair a pergunta e remover espaços
        message_content = message.content.split("$question", 1)[1].strip() 
        
        # Não enviar perguntas vazias
        if not message_content:
            await message.channel.send("Capitão, a pergunta está vazia!")
            return
            
        print(f"Question: {message_content}")
        
        # Chama a função Gemini
        response = call_gemini(message_content)
        
        print(f"Assistant: {response}")
        print("---")
        
        await message.channel.send(response)

# Inicia o bot do Discord. Certifique-se de que o TOKEN está no seu .env
TOKEN = os.getenv('TOKEN')
if TOKEN:
    client.run(TOKEN)
else:
    print("ERRO: O TOKEN do Discord não foi encontrado. Verifique seu arquivo .env.")