import os
import psutil
import time
import asyncio
import random
import json
import spacy






#============================================================#
#--------------------MONITORING-FEATURE----------------------#
#============================================================#
 
def agent_view():
    distractions=["msedge.exe","chrome.exe","whatsapp.exe"]
    
#psutil.process_iter watch the cpu

    for process in psutil.process_iter(['name']):
        try:
            if process.info["name"] in distractions:
                print(process.info['name'])
                if os.path.exists("eyes.txt"):
                    with open("eyes.txt",'w',encoding="utf-8") as f:
                        f.write(f"{process.info['name']}")
                else:
                    with open("eyes.txt",'w',encoding="utf-8") as f:
                        f.write(f"{process.info['name']}")  
        except Exception as e:
            return f"ERROR {e}"
    
#that's watch the cpu use, it'very importatn for the comprenseation is dev is programming or he's sleeping
    cpu_usage = psutil.cpu_percent(interval=1)
    if cpu_usage < 5:
        return "ESTAS ACTIVO?"
    return "TODO BIEN SIGUE ASI"







#============================================================#
#-----------------------ACTIONS-FEATURE----------------------#
#============================================================#

def agent_actions():
            
    if os.path.exists("eyes.txt"):
        with open("eyes.txt","r",encoding="utf-8") as f:
            process=f.read()          
            os.system(f"taskkill /F /IM {process}")
        if os.path.exists("eye.txt"):
            os.remove("eyes.txt")
    else:
        with open("ears.txt","w",encoding="utf-8") as f:
            f.write("")






                #=================================#
                #--------------ASYNC--------------#
                #=================================#

async def call_brain():
#CALL THE PROCESS WITHOUT INTERRUMPTIONS
    process = await asyncio.create_subprocess_exec('python', 'brain.py',stdout=asyncio.subprocess.PIPE,stderr=asyncio.subprocess.PIPE)
    
#WAIT THAT FINISHED IN THE BACKGROUND
    stdout, stderr = await process.communicate()
    
    if process.returncode == 0:
        print("Brain terminó con éxito")
    else:
        print(f"Error en Brain: {stderr.decode()}")

                #=================================#
                #----------ASYNC-SUPORT-----------#
                #=================================#

async def brain_unlock():
    await call_brain()









#============================================================#
#-----------------------TALKING-FEATURE----------------------#
#============================================================#

async def Mevak():
    nlp=spacy.load("es_core_news_sm")
    if os.path.exists("ears.txt"):
        

#CHOOSE THE TOPIC OF THE CONVERSATION           
        choose=random.randint(0,2)
        if choose==0 and os.path.exists("chat_history.json"):
            user="Habale al usuario del ultimo tema"
        elif choose==0 and not os.path.exists("chat_history.json"):
            user="El usuario esta muy callado y si le hablas?"
        elif choose==1:
            if os.path.exists("multimodalA.json"):
                with open("multimodalA.json", "r",encoding="utf-8") as f:
                    modalaprove= json.load(f)
                    topic=random.choice(modalaprove)
            else:
                topic="mejora de el horario para una mejor vida cotidiana"
            user=f"Habla con el usuario sobre {topic}"
        elif choose==2:
            if os.path.exists("news.json"):
                with open("news.json", "r",encoding="utf-8") as f:
                    news= json.load(f)
            else:
                user="google"
            user=f"Habla sobre este tema: {news}"

            doc=nlp(user.lower())
            lemas= [token.lemma_ for token in doc]
            with open("ask.txt", "w", encoding="utf-8") as f:
                    f.write(" ".join(lemas))

            asyncio.create_task(brain_unlock())

            if os.path.exists("ears.txt"):
                os.remove("ears.txt")


if __name__=="__main__":
    clock=None
    sclock=None

    agent_view()

    agent_actions()

    asyncio.run(Mevak())