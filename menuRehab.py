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
screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Menú de Juegos")

#define el tamaño de las fuentes
def crear_fuentes(HEIGHT):
    title_size = int(HEIGHT * 0.1)
    button_size = int(HEIGHT * 0.05)
    font = pygame.font.SysFont(None, title_size)
    button_font = pygame.font.SysFont(None, button_size)

    return font, button_font

#define reloj
clock = pygame.time.Clock()

#define colores
BACKGROUND = (30, 30, 30)
BUTTON = (100, 100, 200)
HOVER = (150, 150, 255)
TEXT = (255, 255, 255)

def crear_botones(WIDTH, HEIGHT):
    buttons = []
    nombres = [
        "Stroop",
        "Secuenciacion AVD",
        "Prueba fonologica",
        "Salir"
    ]

    button_width = WIDTH * 0.35
    button_height = HEIGHT * 0.09

    total_height = len(nombres) * button_height + (len(nombres) - 1) * HEIGHT * 0.03

    start_y = (HEIGHT - total_height) // 2

    for i, nombre in enumerate(nombres):
        rect = pygame.Rect(
            WIDTH // 2 - button_width // 2,
            start_y + i * (button_height + HEIGHT * 0.03),
            button_width,
            button_height
        )
        buttons.append((nombre, rect))

    return buttons

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
    global screen

    WIDTH, HEIGHT = screen.get_size()

    while True:
        WIDTH, HEIGHT = screen.get_size()

        buttons = crear_botones(WIDTH, HEIGHT)
        font, button_font = crear_fuentes(HEIGHT)

        screen.fill(BACKGROUND)

        title = font.render("Menú de Juegos", True, TEXT)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT * 0.1))
        screen.blit(title, title_rect)      

        mouse_pos = pygame.mouse.get_pos()

        for text, rect in buttons:
            color = HOVER if rect.collidepoint(mouse_pos) else BUTTON
            pygame.draw.rect(screen, color, rect)

            dibujar_texto_ajustado(screen, text, rect, button_font, TEXT)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0][1].collidepoint(event.pos):
                    stroop.main()
                elif buttons[1][1].collidepoint(event.pos):
                    secuenciacion2.main()
                elif buttons[2][1].collidepoint(event.pos):
                    prueba_fonologica.main()
                elif buttons[3][1].collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        clock.tick(60)

def main():
    #Llamo a la función en donde el paciente ingresa sus datos
    pantalla_ingreso_paciente.input_paciente()
    #Después sigue al menú
    main_menu()
    pass #no hace nada

if __name__ == "__main__":
    main()