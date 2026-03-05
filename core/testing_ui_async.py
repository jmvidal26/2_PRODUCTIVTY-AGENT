import asyncio
import spacy
import pygame
import os
import sys
import time

#============================================================#
#------------------------VERSION-0.01.3-----by JesVid.DEV----#
#============================================================#
#-------------------------PROtOTYPE_UI-----------------------#
#============================================================#
#============================================================#


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
    global waiting, writting
    await call_brain()
    waiting = False

#============================================================#
#-------------------------RUN/DEBUGGIN-----------------------#
#============================================================#

async def main():
                    #=================================#
                    #-----------VARIABLES-------------#
                    #=================================#
    #prototype 1
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    clocking = pygame.time.Clock()
    #load the font
    font = pygame.font.SysFont('arial', 20)
    #text user
    input_text=""
    nlp=spacy.load("es_core_news_sm")
    feedback=""

                    #=================================#
                    #-----------BANKS.INFO------------#
                    #=================================#

    if os.path.exists("Score.txt"):
        with open("Score.txt", 'r',encoding="utf-8") as archive:
            AI_score=int(archive.read())
    else:
        AI_score=100

                    #=================================#
                    #--------------FLAGS--------------#
                    #=================================#

    waiting=False
    writting=True
    pon=False
    new_rule=False

    running=True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and not pon:

    #SAFE THE REQUEST
                if event.key == pygame.K_RETURN:
                    #OPTIMIZATION WITH NATURAL LANGUAGE PROCESSING
                    doc=nlp(input_text.lower())
                    lemas= [token.lemma_ for token in doc]
                    with open("ask.txt", "w", encoding="utf-8") as f:
                        f.write(" ".join(lemas))
                    with open("provitional.txt", "w", encoding="utf-8") as f:
                        f.write(f"{input_text}")
                    writting=False

                    waiting=True

                    asyncio.create_task(brain_unlock())

    #IN THIS CONTIDITIONAL WE CAN DELETE            
                elif event.key == pygame.K_BACKSPACE and writting:
                    input_text = input_text[:-1]
    #IN THIS CONTIDITIONAL WE CAN WRITE 
                else:
                    #LIMIT FOR MORE OPTIMIZATION
                    if len(input_text) < 100 and writting:
                        input_text += event.unicode


            elif event.type == pygame.KEYDOWN and pon:
                if event.key == pygame.K_SPACE and not new_rule:
                    writting=True
                    pon=False 
                elif event.key== pygame.K_0 and not new_rule:
                    AI_score-=1
                    new_rule=True
                    feedback = ""
                if new_rule:
                    if event.key == pygame.K_RETURN:
                        if os.path.exists("rules.txt"):
                            with open("rules.txt", "a") as f:
                                    f.write(f"{feedback}\n")
                        writting=True
                        pon=False       
                    else:
                        feedback+= event.unicode

                elif event.key== pygame.K_1 and not new_rule:
                    AI_score+=1
                    writting=True
                    pon=False         
                with open("Score.txt", 'w',encoding="utf-8") as archive:
                            archive.write(str(AI_score))
                os.remove("finished.txt")
                os.remove("response.txt")
                os.remove("provitional.txt")


        if waiting and not writting and not pon:
            puntos = (pygame.time.get_ticks() // 500) % 4
            text = "Esperando" + "." * puntos

        elif not waiting and not writting and not pon:
            if os.path.exists("finished.txt") and os.path.exists("response.txt"):
                with open("response.txt","r",encoding="utf-8") as f:
                    text=f.read()
                    pon=True
        elif not waiting and not writting and pon:
            text=feedback

                  
                        

        elif not waiting and writting:
            text=input_text

        screen.fill("white")
        text_ = font.render(text, True, "black")
        screen.blit(text_, (60,60))
        pygame.display.flip()
        await asyncio.sleep(0)
        clocking.tick(60)
    pygame.quit()

if __name__=="__main__":
    asyncio.run(main())


