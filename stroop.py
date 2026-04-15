import pygame
import random
import time
#importa la función para guardar los resultados del juego en el archivo del paciente
from guardar_datos import guardar_resultado

pygame.init()
#Define la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Efecto Stroop")
#Define los colores
colors = {
    "ROJO": (255, 0, 0),
    "VERDE": (0, 255, 0),
    "AZUL": (0, 0, 255),
    "AMARILLO": (255, 255, 0)
}
#Define las fuentes y el tamaño del texto
font = pygame.font.SysFont(None, 80)
button_font = pygame.font.SysFont(None, 40)

#–--------------------------------
#DEFINE CUANTAS RONDAS TIENE EL JUEGO
trials = 10
#---------------------------------
results = []

#DEFINE LAS MÉTRICAS
MAX_promedio_incongruente = 850
MIN_promedio_incongruente = 750


#Función para crear botones
def create_buttons():
    buttons = []
    names = list(colors.keys())
    for i, name in enumerate(names):
        #posiciona los botones uno al lado del otro, espaciándolos
        rect = pygame.Rect(150 + i*130, 450, 120, 50)
        buttons.append((name, rect))
    return buttons

buttons = create_buttons()
#define el boton para salir del juego
quit_button = pygame.Rect(WIDTH - 140, 20, 120, 40)

#Función que formatea la pantalla
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
    
    # Botón salir
    mouse = pygame.mouse.get_pos()
    color_btn = (200, 80, 80) if quit_button.collidepoint(mouse) else (150, 50, 50)
    pygame.draw.rect(screen, color_btn, quit_button)

    quit_text = button_font.render("Salir", True, (255, 255, 255))
    quit_rect = quit_text.get_rect(center=quit_button.center)
    screen.blit(quit_text, quit_rect)

    pygame.display.flip()

#Ajusta el texto para que entre dentro de la pantalla
def render_text_fit(text, max_width):
    size = 40
    while size > 10:
        font = pygame.font.SysFont(None, size)
        surface = font.render(text, True, (0, 0, 0))
        if surface.get_width() <= max_width - 10:
            return surface
        size -= 1
    return surface

#Hace que devuelva "correcto" o "incorrecto" una vez que se juega una ronda
def show_feedback(correct):
    screen.fill((255, 255, 255))
    msg = "CORRECTO" if correct else "INCORRECTO"
    color = (0, 255, 0) if correct else (255, 0, 0)
    text = font.render(msg, True, color)
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, rect)
    pygame.display.flip()
    #se muestra el mensaje por 300 ms
    pygame.time.delay(300)

#Devuelve un color random entre rojo, verde, azul y amarillo
def get_random_stimulus():
    word = random.choice(list(colors.keys()))
    color_name = random.choice(list(colors.keys()))
    return word, colors[color_name], color_name

#PRIMERA PANTALLA con instrucciones, antes de que empiece el juego
def show_instructions():
    waiting = True
    start_button = pygame.Rect(300, 400, 200, 60)
    #el loop se mantiene hasta que el usuario presiona el botón para empezar
    while waiting:
        screen.fill((255, 255, 255))
        # Para el título, lo escribe centrado
        title = font.render("Efecto Stroop", True, (0, 0, 0))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))
        #Lo que se muestra en la pantalla
        instructions = [
            "Seleccione el COLOR de la palabra,",
            "NO el significado del texto.",
            "",
            "Haga clic en el botón correcto lo más rápido posible."
        ]
        #Escribe las instrucciones centradas
        for i, line in enumerate(instructions):
            txt = button_font.render(line, True, (0, 0, 0))
            screen.blit(txt, (WIDTH//2 - txt.get_width()//2, 180 + i*40))

        # Cambia el color del botón según si el mouse está sobre él o no
        mouse = pygame.mouse.get_pos()
        color = (150, 180, 255) if start_button.collidepoint(mouse) else (100, 150, 255)

        pygame.draw.rect(screen, color, start_button)
        #Dibuja el botón de "Comenzar"
        button_text = button_font.render("Comenzar", True, (255, 255, 255))
        screen.blit(button_text, (
            start_button.x + (start_button.width - button_text.get_width()) // 2,
            start_button.y + 15
        ))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False #si el usuario cierra la ventana, se termina la función

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return True #Devuelve True cuando el usuario hace click en "Comenzar"


def main():
    
    #Muestra la pantalla de las instrucciones
    if not show_instructions():
            return
    #Inicializo las variables a utilizar
    correct_count = 0
    reaction_times=[]
    running = True
    trial_count = 0
    accuracy = 0
    avg_reaction = 0
    
    while running and trial_count < trials: 
        #Mientras que la cantidad de rondas sea menor a la definida antes
        word, color, correct_answer = get_random_stimulus()
        #recibe los valores random de la función
        answered = False
        #marca el tiempo de comienzo
        start_time = time.time()

        while not answered:
            #dibuja en la pantalla
            draw_screen(word, color)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    answered = True

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # Si hace click en salir
                    if quit_button.collidepoint(mouse_pos):
                        #guardar_resultado("stroop_parcial", results)
                        return  # vuelve al menú / termina el juego
                    
                    for name, rect in buttons:
                        if rect.collidepoint(mouse_pos):
                            #cuando selecciona una opción de las mostradas
                            reaction_time = time.time() - start_time
                            #guarda el tiempo de reacción obteniendo el tiempo en el momento y restándole el de cuando empezó la ronda
                            user_answer = name
                            #Si la opción elegida coincide con la correcta
                            correct = user_answer == correct_answer
                            if correct:
                                #suma 1 al total de correctas
                                correct_count += 1

                            #va guardando los tiempos de reacción en un vector
                            reaction_times.append(reaction_time)

                            #guarda en una lista, los datos de la ronda
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
                            #muestra la pantalla de "correcto"
                            show_feedback(correct)
                            answered = True
                            #sale del loop
                            break
        #una vez que termina la ronda, suma 1 a la cantidad total            
        trial_count += 1

        #cuando se llega a la cantidad definida de rondas
        if trial_count == trials:

            #calcula la precisión en base a las respuestas correctas y el total de rondas
            accuracy = round((correct_count / trials) * 100, 2)
            #hace un promedio de los tiempos de respuesta
            avg_reaction = round(sum(reaction_times) / len(reaction_times), 3)

            #guarda los resultados del juego en el archivo del paciente
            guardar_resultado("stroop_resumen", {
                    "total_trials": trials,
                    "aciertos": correct_count,
                    "errores": trials - correct_count,
                    "accuracy_percent": accuracy,
                    "reaction_times": reaction_times,
                    "average_reaction_time": avg_reaction
                })
            
            running_results = True

            while running_results:
                #muestra los resultados una vez finalizadas las rondas
                screen.fill((255, 255, 255))
                title = font.render("Resultados Stroop", True, (0, 0, 0))
                centro = WIDTH//2 - title.get_width()//2
                screen.blit(title, (centro, 100))

                txt1 = button_font.render(f"Aciertos: {correct_count}", True, (0, 0, 0))
                txt2 = button_font.render(f"Precisión: {accuracy}%", True, (0, 0, 0))
                txt3 = button_font.render(f"Tiempo promedio: {avg_reaction}s", True, (0, 0, 0))
                #según las métricas definidas, te dice cómo fue el rendimiento
                if avg_reaction > MAX_promedio_incongruente:
                    txt4 = button_font.render(f"Tuvo un rendimiento más bajo que el promedio", True, (255, 0, 0))
                elif MIN_promedio_incongruente <= avg_reaction <= MAX_promedio_incongruente:
                    txt4 = button_font.render(f"Tuvo un rendimiento dentro del promedio", True, (0, 255, 0))
                else:
                    txt4 = button_font.render(f"Tuvo un rendimiento mejor que el promedio!!!", True, (0, 0, 255))

                screen.blit(txt1, (centro, 200))
                screen.blit(txt2, (centro, 250))
                screen.blit(txt3, (centro, 300))
                screen.blit(txt4, (centro, 350))

                #define el botón para volver al menú
                menu_button = pygame.Rect(300, 420, 250, 60)
                mouse = pygame.mouse.get_pos()
                color = (150, 180, 255) if menu_button.collidepoint(mouse) else (100, 150, 255)
                pygame.draw.rect(screen, color, menu_button)
                txt = button_font.render("Volver al menú", True, (255, 255, 255))
                txt_rect = txt.get_rect(center=menu_button.center)
                screen.blit(txt, txt_rect)

                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if menu_button.collidepoint(event.pos):
                            return 

    return 

if __name__ == "__main__":
    main()