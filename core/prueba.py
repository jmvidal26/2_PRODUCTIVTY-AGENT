import pygame
import sys
import random
pygame.init()
screen = pygame.display.set_mode((1200, 800))
clocking = pygame.time.Clock()
    #load the font
font = pygame.font.SysFont('arial', 20)
running=True
pos_x = 28
pos_y = 45
h_rect=50
x=45
y=60
radio_redondeado = 15
text=""
control_lines=60
space_count=[]

#THEMES

themes={"google":{"color_bg":"#FFFFFF","color_txt":"#e0e1dd","color_sur":"#34a853","color_ai":"#4285f4","color_extra":"#ea4335"},
        "Deep_sea_knight":{"color_bg":"#0b0e14","color_txt":"#e0e1dd","color_sur":"#415a77","color_ai":"#00b4d8","color_extra":"#1b263b"},
        "futuristic":{"color_bg":"#240046","color_txt":"#ffffff","color_sur":"#7b2cbf","color_ai":"#c77dff","color_extra":"#3c396c"},
        "jesvid":{"color_bg":"#0d1117","color_txt":"#f0f6fc","color_sur":"#ff8c00","color_ai":"#1f6feb","color_extra":"#30363d"}
}

select=["google","Deep_sea_knight","futuristic","jesvid"]
theme_select=random.choice(select)
theme=themes[theme_select]

while running:
  for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False




        
        if event.type == pygame.KEYDOWN:
            mods = pygame.key.get_mods()
            if event.key == pygame.K_RETURN and (mods & pygame.K_LSHIFT or mods & pygame.K_RSHIFT):
                text += "\n"
                h_rect += 28
            elif event.key == pygame.K_RETURN:
                wait=True
            
            elif event.key == pygame.K_BACKSPACE:
                if len(text) > 0:
                    if text[-1] == "\n":
                        h_rect -= 25 
                    
                    text = text[:-1]
    #IN THIS CONTIDITIONAL WE CAN WRITE 
            else:                    #LIMIT FOR MORE OPTIMIZATION
                character = event.unicode

                text+=character

                current_lines = text.split("\n")
                last_line = current_lines[-1]

                if len(last_line) > control_lines and character == " ":
                    text += "\n"
                    h_rect+=28    
                
                elif len(last_line) >= 100:
                    text += "\n"
                    h_rect+=28

        screen.fill(theme['color_bg'])
        

        w_rect, z = font.size(text)

       

        text_ = font.render(text, True, theme["color_txt"])
        lines=text.split("\n")

        max_w = 0
        for l in lines:
            w_l, _ = font.size(l)
            if w_l > max_w: 
                max_w = w_l

        pygame.draw.rect(screen, (theme["color_sur"]), (pos_x, pos_y, (max_w+28), h_rect), border_radius=radio_redondeado)

        for i,line in enumerate(lines):
            surface = font.render(line, True, theme["color_txt"])
            extra=font.get_height()+5
            screen.blit(surface ,(x, y + i * extra))
        pygame.display.flip()
        clocking.tick(60)
pygame.quit()