import pygame
import sys
import paciente

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ingreso de Paciente")

font = pygame.font.SysFont(None, 48)
label_font = pygame.font.SysFont(None, 36)
button_font = pygame.font.SysFont(None, 40)

BACKGROUND = (30, 30, 30)
WHITE = (255, 255, 255)
BOX_COLOR = (200, 200, 200)
ACTIVE_COLOR = (39, 121, 245)
BUTTON = (28, 86, 173)
HOVER = (39, 121, 245)

clock = pygame.time.Clock()


def input_paciente():

    nombre = ""
    edad = ""
    id_paciente = ""

    campos = ["nombre", "edad", "id"]
    valores = {
        "nombre": nombre,
        "edad": edad,
        "id": id_paciente
    }

    activo = "nombre"

    boxes = {
        "nombre": pygame.Rect(300, 200, 250, 50),
        "edad": pygame.Rect(300, 280, 250, 50),
        "id": pygame.Rect(300, 360, 250, 50)
    }

    boton_rect = pygame.Rect(WIDTH // 2 - 80, 460, 160, 60)

    cursor_visible = True
    cursor_timer = 0

    running = True

    while running:

        dt = clock.tick(60)
        cursor_timer += dt

        if cursor_timer >= 500:
            cursor_visible = not cursor_visible
            cursor_timer = 0

        screen.fill(BACKGROUND)

        titulo = font.render("Ingreso de Paciente", True, WHITE)
        screen.blit(
            titulo,
            (
                WIDTH // 2 - titulo.get_width() // 2,
                100
            )
        )

        # Labels

        labels = {
            "nombre": "Nombre",
            "edad": "Edad",
            "id": "ID Paciente"
        }

        for campo in campos:

            label = label_font.render(
                labels[campo],
                True,
                WHITE
            )

            screen.blit(
                label,
                (
                    boxes[campo].x - 150,
                    boxes[campo].y + 10
                )
            )

            color = ACTIVE_COLOR if activo == campo else BOX_COLOR

            pygame.draw.rect(
                screen,
                color,
                boxes[campo],
                2
            )

            texto = valores[campo]

            if activo == campo and cursor_visible:
                texto += "|"

            texto_surface = button_font.render(
                texto,
                True,
                WHITE
            )

            screen.blit(
                texto_surface,
                (
                    boxes[campo].x + 10,
                    boxes[campo].y + 10
                )
            )

        # Botón continuar

        mouse_pos = pygame.mouse.get_pos()

        if boton_rect.collidepoint(mouse_pos):
            color = HOVER
        else:
            color = BUTTON

        pygame.draw.rect(
            screen,
            color,
            boton_rect
        )

        txt = button_font.render(
            "Continuar",
            True,
            WHITE
        )

        screen.blit(
            txt,
            (
                boton_rect.x + boton_rect.width // 2 - txt.get_width() // 2,
                boton_rect.y + boton_rect.height // 2 - txt.get_height() // 2
            )
        )

        pygame.display.flip()

        # Eventos

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                

            if event.type == pygame.MOUSEBUTTONDOWN:

                for campo in campos:
                    if boxes[campo].collidepoint(event.pos):
                        activo = campo

                if boton_rect.collidepoint(event.pos):

                    if (
                        valores["nombre"].strip() != ""
                        and valores["edad"].strip() != ""
                        and valores["id"].strip() != ""
                    ):

                        paciente.datos_paciente["nombre"] = valores["nombre"]
                        paciente.datos_paciente["edad"] = valores["edad"]
                        paciente.datos_paciente["id"] = valores["id"]

                        return

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_BACKSPACE:
                    valores[activo] = valores[activo][:-1]

                elif event.key == pygame.K_RETURN:

                    if activo == "nombre":
                        activo = "edad"

                    elif activo == "edad":
                        activo = "id"

                else:

                    if event.unicode.isprintable():

                        if activo == "edad":

                            if event.unicode.isdigit():
                                if len(valores[activo]) < 3:
                                    valores[activo] += event.unicode

                        else:

                            if len(valores[activo]) < 20:
                                valores[activo] += event.unicode


if __name__ == "__main__":
    input_paciente()
