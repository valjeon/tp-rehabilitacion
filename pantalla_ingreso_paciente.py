import pygame
import paciente

pygame.init()
#define las dimensiones de la pantalla y el título
screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Ingreso de Paciente")

#defin3 las fuentes a utilizar
def crear_fuentes(HEIGHT):
    font = pygame.font.SysFont(None, int(HEIGHT * 0.08))
    label_font = pygame.font.SysFont(None, int(HEIGHT * 0.05))
    button_font = pygame.font.SysFont(None, int(HEIGHT * 0.06))
    return font, label_font, button_font

#define colores
BACKGROUND = (30, 30, 30)
WHITE = (255, 255, 255)
BOX_COLOR = (200, 200, 200)
ACTIVE_COLOR = (39, 121, 245)
BUTTON = (28, 86, 173)
HOVER = (39, 121, 245)

clock = pygame.time.Clock()

def crear_boxes(WIDTH, HEIGHT):
    box_width = WIDTH * 0.3
    box_height = HEIGHT * 0.08
    start_y = HEIGHT * 0.3
    spacing = HEIGHT * 0.12
    campos = ["nombre", "edad", "id"]
    boxes = {}
    for i, campo in enumerate(campos):
        boxes[campo] = pygame.Rect(
            WIDTH // 2 - box_width // 2,
            start_y + i * spacing,
            box_width,
            box_height
        )
    return boxes

def crear_boton(WIDTH, HEIGHT):
    return pygame.Rect(
        WIDTH * 0.35,
        HEIGHT * 0.75,
        WIDTH * 0.3,
        HEIGHT * 0.1
    )

def input_paciente():
    WIDTH, HEIGHT = screen.get_size()
    font, label_font, button_font = crear_fuentes(HEIGHT)
    boxes = crear_boxes(WIDTH, HEIGHT)
    boton_rect = crear_boton(WIDTH, HEIGHT)
    #defino qué datos le va a pedir
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
    #define los tamaños de los espacios en donde se va a escribir
    
    cursor_visible = True
    cursor_timer = 0

    running = True

    while running:
        WIDTH, HEIGHT = screen.get_size()
        font, label_font, button_font = crear_fuentes(HEIGHT)
        boxes = crear_boxes(WIDTH, HEIGHT)
        boton_rect = crear_boton(WIDTH, HEIGHT)

        #hace que el cursor dentro de los espacios donde se escribe, parpadee
        dt = clock.tick(60)
        cursor_timer += dt
        if cursor_timer >= 500:
            cursor_visible = not cursor_visible
            cursor_timer = 0

        #Colorea la pantalla y le agrega el título
        screen.fill(BACKGROUND)
        titulo = font.render("Ingreso de Paciente", True, WHITE)
        screen.blit(
            titulo,
            (
                WIDTH // 2 - titulo.get_width() // 2,
                100
            )
        )

        #Asigna el nombre a lo que se pide
        labels = {
            "nombre": "Nombre",
            "edad": "Edad",
            "id": "ID Paciente"
        }

        for campo in campos:
            #asigna el font, color a cada tipo de dato
            label = label_font.render(
                labels[campo],
                True,
                WHITE
            )
            #muestra en pantalla los espacios
            label_x = boxes[campo].x - label.get_width() - 20
            screen.blit(
                label,
                (
                    label_x,
                    boxes[campo].y + (boxes[campo].height - label.get_height()) // 2
                )
            )

            #cambia de color, para que en la caja que se esta completando se muestre de otro
            color = ACTIVE_COLOR if activo == campo else BOX_COLOR
            pygame.draw.rect(
                screen,
                color,
                boxes[campo],
                2
            )

            texto = valores[campo]
            #Muestra el cursor después de lo que se está escribiendo
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

        # Botón continuar, hace lo mismo para otros botones
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

        #dibuja el boton ubicándolo en el centro de la pantalla
        screen.blit(
            txt,
            (
                boton_rect.x + boton_rect.width // 2 - txt.get_width() // 2,
                boton_rect.y + boton_rect.height // 2 - txt.get_height() // 2
            )
        )

        pygame.display.flip()

        # Define lo que se hace cuando ya se llenaron los datos
        for event in pygame.event.get():

            if event.type == pygame.VIDEORESIZE:
                
                WIDTH, HEIGHT = screen.get_size()
                font, label_font, button_font = crear_fuentes(HEIGHT)
                boxes = crear_boxes(WIDTH, HEIGHT)
                boton_rect = crear_boton(WIDTH, HEIGHT)

            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:

                for campo in campos:
                    if boxes[campo].collidepoint(event.pos):
                        activo = campo

                #procesa lo que se ingresó
                if boton_rect.collidepoint(event.pos):

                    if (
                        valores["nombre"].strip() != ""
                        and valores["edad"].strip() != ""
                        and valores["id"].strip() != ""
                    ):
                        #guarda lo ingresado
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
                            #la edad no puede tener más de 3 digitos
                            if event.unicode.isdigit():
                                if len(valores[activo]) < 3:
                                    valores[activo] += event.unicode

                        else:
                            #el id puede no puede tener más de 20 caracteres
                            if len(valores[activo]) < 20:
                                valores[activo] += event.unicode


if __name__ == "__main__":
    #Llama a la función
    input_paciente()
