import pygame
import random
import time
import json
import os



pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Efecto Stroop")

colors = {
    "ROJO": (255, 0, 0),
    "VERDE": (0, 255, 0),
    "AZUL": (0, 0, 255),
    "AMARILLO": (255, 255, 0)
}

font = pygame.font.SysFont(None, 80)
button_font = pygame.font.SysFont(None, 40)

trials = 10
results = []

# Crear botones
def create_buttons():
    buttons = []
    names = list(colors.keys())

    for i, name in enumerate(names):
        rect = pygame.Rect(150 + i*130, 450, 120, 50)
        buttons.append((name, rect))
    
    return buttons

buttons = create_buttons()

def draw_screen(word, color):
    screen.fill((255, 255, 255))

    # Palabra estímulo
    text = font.render(word, True, color)
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    screen.blit(text, rect)

    # Dibujar botones
    for name, rect in buttons:
        pygame.draw.rect(screen, colors[name], rect)
        label = render_text_fit(name, rect.width)
        label_rect = label.get_rect(center=rect.center)
        screen.blit(label, label_rect)

    pygame.display.flip()

def render_text_fit(text, max_width):
    size = 40
    while size > 10:
        font = pygame.font.SysFont(None, size)
        surface = font.render(text, True, (0, 0, 0))
        if surface.get_width() <= max_width - 10:
            return surface
        size -= 1
    return surface

def show_feedback(correct):
    screen.fill((255, 255, 255))
    msg = "CORRECTO" if correct else "INCORRECTO"
    color = (0, 255, 0) if correct else (255, 0, 0)

    text = font.render(msg, True, color)
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, rect)

    pygame.display.flip()
    pygame.time.delay(300)

def get_random_stimulus():
    word = random.choice(list(colors.keys()))
    color_name = random.choice(list(colors.keys()))
    return word, colors[color_name], color_name

def get_participant_name():
    name = ""

    input_box = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 25, 300, 50)

    # Botón OK
    button_rect = pygame.Rect(WIDTH//2 - 60, HEIGHT//2 + 60, 120, 50)
    cursor_visible = True
    cursor_timer = 0

    while True:
        screen.fill((30, 30, 30))

        dt = pygame.time.Clock().tick(60)  # controla FPS
        cursor_timer += dt

        if cursor_timer >= 500:  # cada 500 ms
            cursor_visible = not cursor_visible
            cursor_timer = 0

        # Título
        title = font.render("Ingrese su nombre", True, (255, 255, 255))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3))

        # Caja de texto
        pygame.draw.rect(screen, (255, 255, 255), input_box, 2)
        display_text = name
        if cursor_visible:
            display_text += "|"

        text_surface = button_font.render(display_text, True, (255, 255, 255))
        screen.blit(text_surface, (input_box.x + 10, input_box.y + 10))

        # Botón OK
        mouse_pos = pygame.mouse.get_pos()

        # Efecto hover
        if button_rect.collidepoint(mouse_pos):
            button_color = (39, 121, 245)
        else:
            button_color = (28, 86, 173)

        pygame.draw.rect(screen, button_color, button_rect)

        ok_text = button_font.render("OK", True, (0, 0, 0))
        screen.blit(ok_text, (
            button_rect.x + button_rect.width//2 - ok_text.get_width()//2,
            button_rect.y + button_rect.height//2 - ok_text.get_height()//2
        ))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    # Solo agregar caracteres imprimibles (letras, números, espacio)
                    if event.unicode.isprintable():
                        if len(name) < 15:
                            name += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos) and name.strip() != "":
                    return name
def main():
    
    participant = get_participant_name()
    if participant is None:
        pygame.quit()
        return

    running = True
    trial_count = 0

    while running and trial_count < trials:
        word, color, correct_answer = get_random_stimulus()

        answered = False
        start_time = time.time()

        while not answered:
            draw_screen(word, color)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    answered = True

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    for name, rect in buttons:
                        if rect.collidepoint(mouse_pos):
                            reaction_time = time.time() - start_time
                            user_answer = name
                            correct = user_answer == correct_answer

                            trial_data = {
                                "trial": trial_count + 1,
                                "word": word,
                                "color_correct": correct_answer,
                                "response": user_answer,
                                "correct": correct,
                                "reaction_time_sec": round(reaction_time, 3),
                                "condition": "congruente" if word == correct_answer else "incongruente"
                            }

                            results.append(trial_data)
                            print(trial_data)

                            show_feedback(correct)

                            answered = True
                            break

        trial_count += 1

    # Guardar JSON

    base_path = os.path.dirname(os.path.abspath(__file__))
    print(base_path)
    data_folder = os.path.join(base_path, "datos")

    os.makedirs(data_folder, exist_ok=True)

    filename = os.path.join(data_folder, f"{participant}.json")
    data = {
        "participant": participant,
        "trials": results
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


    pygame.quit()

if __name__ == "__main__":
    main()