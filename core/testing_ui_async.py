import asyncio
from ntpath import exists
import spacy
import pygame
import os
import time
import random
import math 

#============================================================#
#------------------------VERSION-0.02.8-----by JesVid.DEV----#
#============================================================#
#-------------------------PROTOTYPE_UI-----------------------#
#============================================================#
#============================================================#


                #=================================#
                #------------FRIEND-MODE----------#
                #=================================#

async def Mevak():
#CALL THE PROCESS WITHOUT INTERRUMPTIONS
    process = await asyncio.create_subprocess_exec('python', 'actions.py',stdout=asyncio.subprocess.PIPE,stderr=asyncio.subprocess.PIPE)
    
#WAIT THAT FINISHED IN THE BACKGROUND
    stdout, stderr = await process.communicate()
    
    if process.returncode == 0:
        print("Mevak terminó con éxito")
    else:
        print(f"Error en Mevak: {stderr.decode()}")


                #=================================#
                #-------FRIEND-MODE-SUPORT--------#
                #=================================#

async def MVK_unlock():
    await Mevak()

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
    global waiting, writting,pon
    await call_brain()
    waiting = False
    pon=True
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
    font2 = pygame.font.SysFont('arial', 40)
    running=True
    pos_x = 28
    pos_y = 45
    h_rect=50
    x=45
    y=60
    radio_redondeado = 15
    control_lines=60
    space_count=[]
    #text user
    input_text=""
    nlp=spacy.load("es_core_news_sm")
    feedback=""
    #RECTS OF WAITNIG LOOP

    anim=0
    bars= [100,100,100]

    #THEMES

    themes={"google":{"color_bg":"#FFFFFF","color_txt":"#e0e1dd","color_sur":"#34a853","color_ai":"#4285f4","color_extra":"#ea4335"},
            "Deep_sea_knight":{"color_bg":"#0b0e14","color_txt":"#e0e1dd","color_sur":"#415a77","color_ai":"#00b4d8","color_extra":"#1b263b"},
            "futuristic":{"color_bg":"#240046","color_txt":"#ffffff","color_sur":"#7b2cbf","color_ai":"#c77dff","color_extra":"#3c396c"},
            "jesvid":{"color_bg":"#0d1117","color_txt":"#f0f6fc","color_sur":"#ff8c00","color_ai":"#1f6feb","color_extra":"#30363d"}
    }

    select=["google","Deep_sea_knight","futuristic","jesvid"]
    theme_select=random.choice(select)
    theme=themes[theme_select]


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
    trate=False
    last_input_time = time.time()


    running=True
    while running:

        current_time = time.time()
        time_elapsed = current_time - last_input_time
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                last_input_time = current_time
    #SAFE THE REQUEST
                if event.type == pygame.KEYDOWN and writting and not waiting:
                    mods = pygame.key.get_mods()
                    if event.key == pygame.K_RETURN and (mods & pygame.K_LSHIFT):
                        input_text += "\n"
                        h_rect += 28
                    elif event.key == pygame.K_RETURN:
                        #OPTIMIZATION WITH NATURAL LANGUAGE PROCESSING
                        if nlp:
                            doc = nlp(input_text.lower())
                            lemas = [token.lemma_ for token in doc]
                            with open("ask.txt", "w", encoding="utf-8") as f:
                                f.write(" ".join(lemas))

                        with open("provitional.txt", "w", encoding="utf-8") as f:
                            f.write(f"{input_text}")
                        
                        writting=False
                        waiting=True

                        asyncio.create_task(brain_unlock())

    #IN THIS CONTIDITIONAL WE CAN DELETE            
                    elif event.key == pygame.K_BACKSPACE:
                        if len(input_text) > 0:
                            if input_text[-1] == "\n": h_rect -= 28
                            input_text = input_text[:-1]
                    
    #IN THIS CONTIDITIONAL WE CAN WRITE 
                    else:
                    #LIMIT FOR MORE OPTIMIZATION
                        if len(input_text) < 500:
                            input_text += event.unicode
                            # Auto-wrap logic
                            lines = input_text.split("\n")
                            if len(lines[-1]) > control_lines and event.unicode == " ":
                                input_text += "\n"
                                h_rect += 28

                elif pon and not waiting:
                    if event.key == pygame.K_SPACE and not new_rule:
                        writting, pon = True, False
                        input_text = ""
                    elif event.key == pygame.K_0 and not new_rule:
                        AI_score -= 1
                        new_rule = True
                        feedback = ""
                    elif event.key == pygame.K_1 and not new_rule:
                        AI_score += 1
                        writting, pon = True, False
                        input_text = ""
                    if new_rule:
                        if event.key == pygame.K_RETURN:
                            with open("rules.txt", "a") as f:
                                f.write(f"{feedback}\n")
                            new_rule = False
                            writting, pon = True, False
                            input_text = ""
                        elif event.key != pygame.K_0:
                            feedback += event.unicode

        if writting and input_text == "" and time_elapsed > 250:
            last_input_time = current_time
            asyncio.create_task(MVK_unlock())

        if waiting and os.path.exists("finished.txt"):
            waiting = False
            pon = True
            if os.path.exists("response.txt"):
                with open("response.txt", "r", encoding="utf-8") as f:
                    display_text = f.read()
            for f in ["finished.txt", "response.txt", "provitional.txt", "ask.txt"]:
                if os.path.exists(f): os.remove(f)

        if waiting:
            anim += 0.1
            cx, cy = 150, 400
            colors = [theme["color_sur"], theme["color_extra"], theme["color_ai"]]
            for i in range(3):
                bars[i] = 70 + 30 * math.sin(anim + i*2)
                pygame.draw.rect(screen, colors[i], (cx + (i * 55), cy - (bars[i]/2), 40, bars[i]), border_radius=8)
            
            dots = (pygame.time.get_ticks() // 500) % 4
            tw = font2.render("Esperando" + "."*dots, True, theme["color_txt"])
            screen.blit(tw, (320, 370))
                                
            if os.path.exists("finished.txt"):
                waiting=False
                h_rect=50
                anim=0

        screen.fill(theme['color_bg'])

        if writting:
            text=input_text
            lines = input_text.split("\n")
            max_w = 0
            for l in lines:
                w_l, _ = font.size(l)
                max_w = max(max_w, w_l)
            
            if input_text:
                pygame.draw.rect(screen, theme["color_sur"], (pos_x, pos_y, max_w + 30, h_rect), border_radius=radio_redondeado)
                for i, line in enumerate(lines):
                    surface = font.render(line, True, theme["color_txt"])
                    screen.blit(surface, (x, y + i * 25))
        
        elif pon:
            
            current_display = feedback if new_rule else display_text
            
            surf = font.render(current_display[:100] , True, theme["color_txt"])
            screen.blit(surf, (x, y))

        else:
            cx, cy = 150, 400
            colors = [theme["color_sur"], theme["color_extra"], theme["color_ai"]]
            for i in range(3):
                bar_y = cy - (bars[i] / 2)
                pygame.draw.rect(screen, colors[i], (cx + (i * 55), bar_y, 40, bars[i]), border_radius=8)
                points = (pygame.time.get_ticks() // 500) % 4
                text_wait = "Esperando" + "." * points

            text_w=font2.render(text_wait, True, theme["color_txt"])
            screen.blit(text_w,(320,370))

        pygame.display.flip()
        await asyncio.sleep(0.01)
        clocking.tick(60)
    pygame.quit()
    with open("Score.txt", 'w', encoding="utf-8") as f:
        f.write(str(AI_score))
if __name__=="__main__":
    asyncio.run(main())


