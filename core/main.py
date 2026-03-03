import ollama
import psutil
import subprocess
import time
import spacy
import json
import os

# tha's load the spanish language

nlp=spacy.load("es_core_news_sm")

#information banks

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
#variables

clock = None
sclock = None

def multimodal(user):
    global modal
    global modalaprove
    doc=nlp(user.lower())
    lemma=[token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    modal.extend(lemma)
    with open("multimodal.json", "w", encoding="utf-8") as f:
        json.dump(lemma, f, ensure_ascii=False, indent=4)
    filter=set(modal)
    for word in filter:
        count=modal.count(word)
        if count>=5 and word not in modalaprove:
            with open("rules.txt", "a") as f:
                f.write(f"El usuario suele hablar de: {word}\n")
            with open("multimodal.json", "w", encoding="utf-8") as f:
                json.dump(modalaprove, f, ensure_ascii=False, indent=4)

def agent_view():
    distractions=["msedge.exe","chrome.exe","whatsapp.exe"]

    #psutil.process_iter watch the cpu

    for process in psutil.process_iter(['name']):
        try:
            if process.info["name"] in distractions:
                print(process.info['name'])
                return "!HEY PEREZOSO, EMPIEZA A PROGRAMAR"
    
        except:"ESO ERES TODO UN FULLSTACK"
    
    #that's watch the cpu use, it'very importatn for the comprenseation is dev is programming or he's sleeping
    cpu_usage = psutil.cpu_percent(interval=1)
    if cpu_usage < 5:
        return "ESTAS ACTIVO?"
    return "TODO BIEN SIGUE ASI"

def agent_actions():
    global clock, sclock
    distractions=["msedge.exe","chrome.exe","whatsapp.exe"]
    f_distractions=False
    silence=False

    for process in psutil.process_iter(['name']):
        try:
            if process.info["name"] in distractions:
                print(process.info['name'])
                f_distractions = True
        except:
            return "ESO ERES TODO UN FULLSTACK"
        
    
    if f_distractions:
        if clock is None:
            clock=time.time()
        s_elapsed = time.time() - clock
        if s_elapsed>=10:            
            os.system(f"taskkill /F /IM {process.info['name']}")

            return "!HEY PEREZOSO, EMPIEZA A PROGRAMAR"
    else:
        clock=None
    
    if not f_distractions:
        silence=True
        if silence:
            if sclock is None:
                sclock=time.time()
            elapsed = time.time() - sclock
            if elapsed>=10:
                user="El usuario esta aburrido o programando, di algo para seguir en actividad"
                res=agent_AI(user)
                print(f"<<AI>>:  {res}")
    if not silence:
        sclock= None
    
def agent_AI (message):
    global AI_score, instruction
    base = "Eres un asistente técnico experto."
    feedback_alert = " El usuario no está satisfecho, sé más breve." if AI_score < 105 else ""
    
    prompt_final = f"{base} {feedback_alert}\nREGLAS ADICIONALES:\n{instruction}\nUsuario: {message}"
    # that's convert the message in MINS
    doc= nlp(message.lower())

    #that process the message

    lemas= [token.lemma_ for token in doc]
    messages_for_ollama = [{'role': 'system', 'content': prompt_final}]

    history.append({'role': 'user', 'content': message})
    if len(history)>10:
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
    
def memory_agent(user,respondAI):

    global AI_score, instruction
    date = time.strftime("%d/%m/%Y %H:%M:%S")
    try:
        with open("memory_agent.txt", "a", encoding="utf-8") as BaseD:
            BaseD.write(f'\n<{date}>  <USER>  {user}  <AI>  {respondAI}  <Score>  {AI_score}')
    except:
        print("THERE IS/ARE A FAIL/S")

if __name__ == "__main__":
    while True:
        status= agent_view()
        print(status)
        if not "!" in status:
            user= input("<<YOU>>  ")
            if user.lower() in ("exit","salir"):
                break

            else:
                try:
                    respondAI=agent_AI(user)
                    print(f"<<AI>>:  {respondAI}")
                    multimodal(user)

                    feedback=input("THAT's ANSWER IS WELL (1) OR BAD (0)")

                    if feedback in ("1","0"):
                        try:
                            if feedback=="1":
                                AI_score+=1
                            else:
                                AI_score-=1
                                newlaw=input("INGRESE LA NUEVA INSTRUCCION:  ")
                                instruction += f"\n- {newlaw}"
                                with open("rules.txt", "a") as f:
                                    f.write(f"{newlaw}\n")
                            with open("Score.txt", 'w',encoding="utf-8") as archive:
                                archive.write(str(AI_score))
                        except:
                            print("THERE IS/ARE A FAIL/S")
                    agent_actions()
                except:
                    print("THERE IS/ARE A FAIL/S")

            memory_agent(user,respondAI)
            print("\n--- REPORTE DE EVOLUCIÓN (C++) ---")
            ruta_cpp = r"c:\Users\Jesus el mas guapo\OneDrive\Desktop\productivity agent\output\module_cpp\memory.exe"
            resultado = subprocess.run([ruta_cpp], capture_output=True, text=True, cwd=os.getcwd())
            print(resultado.stdout)
            time.sleep(5)
            os.system("cls")
        else:
            agent_actions()
            print("I SEE YOU >:V")
        time.sleep(5)