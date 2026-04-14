import pygame
import sys
import stroop
import secuenciacion2
import prueba_fonologica
import pantalla_ingreso_paciente

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menú de Juegos")

font = pygame.font.SysFont(None, 60)
button_font = pygame.font.SysFont(None, 40)

clock = pygame.time.Clock()

BACKGROUND = (30, 30, 30)
BUTTON = (100, 100, 200)
HOVER = (150, 150, 255)
TEXT = (255, 255, 255)

# -------------------------
# BOTONES
# -------------------------

buttons = []

nombres = [
    "Stroop",
    "Secuenciacion AVD",
    "Prueba fonologica",
    "Salir"
]

for i, nombre in enumerate(nombres):

    rect = pygame.Rect(
        300,
        200 + i * 100,
        250,
        70
    )

    buttons.append((nombre, rect))

# -------------------------
# FUNCION PARA AJUSTAR TEXTO DENTRO DEL BOTON
# -------------------------

def dibujar_texto_ajustado(surface, texto, rect, font, color):

    palabras = texto.split(" ")
    lineas = []
    linea_actual = ""

    for palabra in palabras:

        prueba = linea_actual + palabra + " "

        if font.size(prueba)[0] <= rect.width - 20:
            linea_actual = prueba
        else:
            lineas.append(linea_actual.strip())
            linea_actual = palabra + " "

    lineas.append(linea_actual.strip())

    total_altura = len(lineas) * font.get_height()
    y = rect.y + (rect.height - total_altura)//2

    for linea in lineas:

        texto_render = font.render(
            linea,
            True,
            color
        )
        x = rect.x + (rect.width - texto_render.get_width())//2
        surface.blit(
            texto_render,
            (x,y)
        )

        y += font.get_height()


def main_menu():

    while True:

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

            dibujar_texto_ajustado(
            screen,
            text,
            rect,
            button_font,
            TEXT
        )
        pygame.display.flip()

        # EVENTOS

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

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

        clock.tick(60)

def main():
    pantalla_ingreso_paciente.input_paciente()
    main_menu()
    pass

if __name__ == "__main__":
    main()