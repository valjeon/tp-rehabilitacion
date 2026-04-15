#CÒDIGO DEL MENU PRINCIPAL

import pygame
import sys
#Importa el código de los juegos
import stroop
import secuenciacion2
import prueba_fonologica
#Importa el código de la pantalla en la que el cliente ingresa su información
import pantalla_ingreso_paciente

pygame.init()
#defino el tamaño de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menú de Juegos")

#define el tamaño de las fuentes
font = pygame.font.SysFont(None, 60)
button_font = pygame.font.SysFont(None, 40)

#define reloj
clock = pygame.time.Clock()

#define colores
BACKGROUND = (30, 30, 30)
BUTTON = (100, 100, 200)
HOVER = (150, 150, 255)
TEXT = (255, 255, 255)

# CREA LOS BOTONES
buttons = []
nombres = [
    "Stroop",
    "Secuenciacion AVD",
    "Prueba fonologica",
    "Salir"
]

for i, nombre in enumerate(nombres):
    #Asigna la posición de cada botón
    rect = pygame.Rect(
        300,
        200 + i * 100,
        250,
        70
    )
    buttons.append((nombre, rect))


# FUNCION PARA AJUSTAR TEXTO DENTRO DEL BOTON
def dibujar_texto_ajustado(surface, texto, rect, font, color):
    #separa el texto cada vez que encuentra un espacio
    palabras = texto.split(" ")
    lineas = []
    linea_actual = ""


    for palabra in palabras:
        #agrega las palabras a una linea
        prueba = linea_actual + palabra + " "
        if font.size(prueba)[0] <= rect.width - 20:
            linea_actual = prueba
        else:
            lineas.append(linea_actual.strip())
            linea_actual = palabra + " "

    #agrega a lineas, la actual
    lineas.append(linea_actual.strip())

    #calcula la altura de acuerdo a la cantidad de lineas 
    total_altura = len(lineas) * font.get_height()
    
    y = rect.y + (rect.height - total_altura)//2

    
    for linea in lineas:
        texto_render = font.render(
            linea,
            True,
            color
        )
        x = rect.x + (rect.width - texto_render.get_width())//2
        #Ajusta el texto al boton
        surface.blit(
            texto_render,
            (x,y)
        )
        y += font.get_height()


def main_menu():

    while True:

        #Defino diseño de la pantalla: color, el titulo.
        screen.fill(BACKGROUND)
        title = font.render("Menú de Juegos", True, TEXT)
        screen.blit(title, (260, 100))

        mouse_pos = pygame.mouse.get_pos()

        # DIBUJAR BOTONES
        for text, rect in buttons:
            if rect.collidepoint(mouse_pos):
                color = HOVER
            else:
                color = BUTTON

            pygame.draw.rect(screen, color, rect)

            #ajusta el texto dentro del botón
            dibujar_texto_ajustado(
            screen,
            text,
            rect,
            button_font,
            TEXT
        )
        pygame.display.flip()

        # Para entrar a cada juego:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #Define qué hace cuando se presionan los botones
            if event.type == pygame.MOUSEBUTTONDOWN:

                if buttons[0][1].collidepoint(event.pos):
                    stroop.main()

                elif buttons[1][1].collidepoint(event.pos):
                    secuenciacion2.main()

                elif buttons[2][1].collidepoint(event.pos):
                    prueba_fonologica.main()

                elif buttons[3][1].collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        #limira a que el juego no corra a más que 60 fps, para mejorar el rendimiento
        clock.tick(60)

def main():
    #Llamo a la función en donde el paciente ingresa sus datos
    pantalla_ingreso_paciente.input_paciente()
    #Después sigue al menú
    main_menu()
    pass #no hace nada

if __name__ == "__main__":
    main()