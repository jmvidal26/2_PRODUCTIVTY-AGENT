import os
import ollama
import subprocess
import time
import spacy
import json
import sys
import os
venv_path = os.path.join(os.getcwd(), '.venv', 'Lib', 'site-packages')
if venv_path not in sys.path:
    sys.path.append(venv_path)

try:
    from google import genai
    print("¡Módulo genai cargado con éxito!")
except ImportError:
    import google.genai as genai
    print("¡Módulo genai cargado con éxito (alternativo)!")
from dotenv import load_dotenv    
import socket






#============================================================#
#------------------------VERSION-0.05.0-----by JesVid.DEV----#
#============================================================#
#-------------------------PROtOTYPE_UI-----------------------#
#============================================================#
#============================================================#


#============================================================#
#-------------------INFORMATION BANKS------------------------#
#============================================================#

if os.path.exists("rules.txt"):
    with open("rules.txt", "r", encoding="utf-8") as f:
        instruction = f.read()
else:
    instruction = ""

if os.path.exists("Score.txt"):
    with open("Score.txt", 'r',encoding="utf-8") as archive:
        AI_score=int(archive.read())
else:
    AI_score=100

if os.path.exists("chat_history.json"):
    with open("chat_history.json", "r", encoding="utf-8") as f:
        history = json.load(f)
else:
    history = []

if os.path.exists("multimodal.json"):
    with open("multimodal.json", "r", encoding="utf-8") as f:
        modal= json.load(f)  
else:
    modal=[]  

if os.path.exists("multimodalA.json"):
    with open("multimodalA.json", "r", encoding="utf-8") as f:
        modalaprove= json.load(f)  
else:
    modalaprove=[]  

#============================================================#
#-------------------------VARIABLES--------------------------#
#============================================================#

clock = None
sclock = None
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# tha's load the spanish language

nlp=spacy.load("es_core_news_sm")
load_dotenv()

#============================================================#
#---------------------CONnECTION-FEATURE---------------------#
#============================================================#

def connect(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, port))
        return True
    except socket.error:
        return False






#============================================================#
#-----------------------MODE-FEATURE-------------------------#
#============================================================#

def multimodal(user):
    global modal
    global modalaprove
    doc=nlp(user.lower())
#TAKE THE MOST IMPORTANT WORDS
    lemma=[token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
#SAFE THE IMPORTANT WORDS IN MODAL
    modal.extend(lemma)
    with open("multimodal.json", "w", encoding="utf-8") as f:
        json.dump(modal, f, ensure_ascii=False, indent=4)

#COUNT THE MODES AND, IF THIS IS SAFE A CONCURRENCE TOPIC
    filter=set(modal)
    for word in filter:
        count=modal.count(word)
        if count>=5 and word not in modalaprove:
            with open("rules.txt", "a") as f:
                f.write(f"El usuario suele hablar de: {word}\n")
                modalaprove.append(word)
            with open("multimodalA.json", "w", encoding="utf-8") as f:
                json.dump(modalaprove, f, ensure_ascii=False, indent=4)












#============================================================#
#----------------------AI_CHAT-FEATURE-----------------------#
#============================================================#

def agent_AI (message):
    global AI_score, instruction
    base = "Eres un asistente técnico experto."
    feedback_alert = " El usuario no está satisfecho, sé más breve." if AI_score < 105 else ""
    
    prompt_final = f"{base} {feedback_alert}\nREGLAS ADICIONALES:\n{instruction}\nUsuario: {message}"
    # that's convert the message in MINS and process the msj, but 
    doc= nlp(message.lower())

    #that process the message

    lemas= [token.lemma_ for token in doc]
    messages_for_ollama = [{'role': 'system', 'content': prompt_final}]

    history.append({'role': 'user', 'content': message})
    if len(history)>20:
        history.pop(0)
    
    messages_for_ollama.extend(history)

    try:
        #practice hashmaps
        respond=ollama.chat(model='gemma2:2b', messages=messages_for_ollama)
        respondA=respond['message']['content']
        history.append({'role': 'assistant', 'content': respondA})
        with open("chat_history.json", "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=4)

        return respondA
    
    except Exception as e:
        return f"fail with ollama model {str(e)}"

def agent_WIFI (message):
    global AI_score, instruction
    api_key = os.getenv("GEMINI_API_KEY")
    client=genai.Client(api_key=api_key)

    base = "Eres un asistente técnico experto."
    feedback_alert = " El usuario no está satisfecho, sé más breve." if AI_score < 105 else ""
    
    prompt_final = f"{base} {feedback_alert}\nREGLAS ADICIONALES:\n{instruction}\nUsuario: {message}"
    
    try:
        respond = client.models.generate_content(model='gemini-1.5-flash',config={'system_instruction': prompt_final},contents=message)

        respond_text = respond.text

        history.append({'role': 'user', 'content': message})
        history.append({'role': 'assistant', 'content': respond_text})

        if len(history) > 20:
            history.pop(0)

        history.append({'role': 'user', 'content': message})
        history.append({'role': 'assistant', 'content': respond_text})

        with open("chat_history.json", "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=4)

        return respond_text
    
    except Exception as e:
        return f"fail with gemini model {str(e)}"








#============================================================#
#----------------------MEMORY-FEATURE------------------------#
#============================================================#    
    
def memory_agent(user,respondAI):

    global AI_score, instruction
    date = time.strftime("%d/%m/%Y %H:%M:%S")
    try:
        with open("memory_agent.txt", "a", encoding="utf-8") as BaseD:
            BaseD.write(f'\n<{date}>  <USER>  {user}  <AI>  {respondAI}  <Score>  {AI_score}')
    except Exception as e:
        print(f"THERE IS/ARE A FAIL/S {e}")












#============================================================#
#----------------------RUN\TESTING_MODULE--------------------#
#============================================================#

if __name__ == "__main__":

    user = ""
    respondAI = "No request processed."
    if os.path.exists("ask.txt"):
        with open("ask.txt","r",encoding="utf-8") as f:
            user=f.read()
        wifi=connect()
        try:
            if not wifi:
                respondAI=agent_AI(user)
            elif wifi:
                respondAI=agent_WIFI(user)
            multimodal(user)
            with open("response.txt","w",encoding="utf-8") as f:
                f.write(f"{respondAI}")
            with open("finished.txt","w",encoding="utf-8") as f:
                f.write(f"")

            os.remove("ask.txt")
        except Exception as e:
            print(f"THERE IS/ARE A FAIL/S {e}")

    memory_agent(user,respondAI)
    print("\n--- REPORTE DE EVOLUCIÓN (C++) ---")
    ruta_cpp = os.path.join(BASE_PATH, "output", "module_cpp", "memory.exe")
    resultado = subprocess.run([ruta_cpp], capture_output=True, text=True, cwd=os.getcwd())
    print(resultado.stdout)