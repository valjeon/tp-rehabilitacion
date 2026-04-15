import pygame
import random
import time
#importa listas donde se describe una actividad diaria como secuencia
from actividades import actividades
from guardar_datos import guardar_resultado

pygame.init()
#Defino las constantes y el formato de la pantalla
WIDTH, HEIGHT = 900, 600
X_BOTONES = 80
ANCHO_BOTONES = 350
X_SECUENCIA = 450
ANCHO_SECUENCIA = 200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Secuenciación AVD")
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 40)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (100, 150, 255)
GREEN = (100, 200, 100)
RED = (200, 100, 100)
BUTTON = (100, 150, 255)
HOVER = (150, 180, 255)

clock = pygame.time.Clock()

#Función para ajustar los textos a los botones y pantalla
def dibujar_texto_ajustado(surface, texto, rect, font, color):
    palabras = texto.split(" ")
    lineas = []
    linea_actual = ""

    for palabra in palabras:

        prueba = linea_actual + palabra + " "

        if font.size(prueba)[0] <= rect.width - 20:
            linea_actual = prueba
        else:
            lineas.append(linea_actual)
            linea_actual = palabra + " "

    lineas.append(linea_actual)

    altura_total = len(lineas) * font.get_height()

    y = rect.centery - altura_total // 2

    for linea in lineas:

        texto_render = font.render(
            linea.strip(),
            True,
            color
        )

        x = rect.x + 10

        surface.blit(texto_render, (x, y))

        y += font.get_height()



def nueva_actividad():
    #defino variables
    global actividad_actual
    global pasos_correctos
    global pasos
    global seleccionados
    global inicio_tiempo

    #elige una actividad dentro del archivo de actividades  ej: cepillarse los dientes
    actividad_actual = random.choice(
        list(actividades.keys())
    )

    pasos_correctos = actividades[actividad_actual]
    #guarda el orden correcto de la actividad
    pasos = pasos_correctos.copy()
    #desordena los pasos
    random.shuffle(pasos)

    seleccionados = []
    #guarda el tiempo de inicio de la ronda
    inicio_tiempo = time.time()

def main():
    #defino variables
    global mensaje
    global mensaje_tiempo
    global actividad_actual
    global pasos_correctos
    global pasos
    global seleccionados
    global inicio_tiempo

    tiempos=[]
    estado = "jugando"
    #defino la cantidad de rondas a jugar
    TOTAL_RONDAS = 5
    #inicializo variables
    ronda_actual = 1
    aciertos=0
    errores=0

    #Llamo a la función que elige la actividad
    nueva_actividad()
    mensaje = ""
    mensaje_tiempo = 0
    running = True

    while running:
        
        screen.fill(WHITE)
        titulo = big_font.render(
            f"Ordená los pasos: {actividad_actual}",
            True,
            (0, 0, 0)
        )
        screen.blit(titulo, (180, 20))
        #Muestra la ronda en la que está
        texto_ronda = font.render(
            f"Ronda {ronda_actual} / {TOTAL_RONDAS}",
            True,
            (0, 0, 0)
        )
        screen.blit(texto_ronda, (20, 20))
        
        #Botones de los pasos

        botones = []
        mouse_pos = pygame.mouse.get_pos()

        for i, paso in enumerate(pasos):
            #ubica los botones uno abajo del otro espacionados
            rect = pygame.Rect(
                80,
                100 + i * 80,
                ANCHO_BOTONES,
                70
            )
            if rect.collidepoint(mouse_pos) and paso not in seleccionados:
                color = HOVER
            elif paso in seleccionados:
                color = (60, 90, 180)  #Pone el botón más oscuro cuando el mouse está ahí
            else:
                color = BLUE
            pygame.draw.rect(screen, color, rect)

            dibujar_texto_ajustado(
                screen,
                paso,
                rect,
                font,
                WHITE
            )

            botones.append(rect)

        # SECUENCIA ELEGIDA
        sec_titulo = font.render(
            "Secuencia elegida:",
            True,
            (0, 0, 0)
        )
        screen.blit(sec_titulo, (520, 100))

        #ubica los pasos elegidos en columna
        for i, paso in enumerate(seleccionados):
            rect = pygame.Rect(
                520,
                140 + i * 70,
                ANCHO_SECUENCIA,
                60
            )
            dibujar_texto_ajustado(
                screen,
                f"{i+1}. {paso}",
                rect,
                font,
                (0, 0, 0)
            )

        # MENSAJE
        if estado == "resultado":
            color = GREEN if mensaje == "Correcto" else RED
            msg = big_font.render(
                mensaje,
                True,
                color
            )
            screen.blit(
                msg,
                (
                    WIDTH//2 - msg.get_width()//2,
                    420
                )
            )
            
            mouse_pos = pygame.mouse.get_pos()

            boton_reintentar = pygame.Rect(
                WIDTH//2 - 170,
                500,
                150,
                60
            )
            boton_menu = pygame.Rect(
                WIDTH//2 + 20,
                500,
                150,
                60
            )


            color1 = HOVER if boton_reintentar.collidepoint(mouse_pos) else BUTTON
            color2 = HOVER if boton_menu.collidepoint(mouse_pos) else BUTTON

            pygame.draw.rect(screen, color1, boton_reintentar)
            pygame.draw.rect(screen, color2, boton_menu)

            txt1 = font.render("Reintentar", True, WHITE)
            txt2 = font.render("Menú", True, WHITE)

            screen.blit(
                txt1,
                (
                    boton_reintentar.x + 15,
                    boton_reintentar.y + 15
                )
            )

            screen.blit(
                txt2,
                (
                    boton_menu.x + 35,
                    boton_menu.y + 15
                )
            )
        if estado == "fin":
            
            screen.fill(WHITE)

            if tiempos:
                #hace un promedio de lo que tardó en cada ronda
                promedio = round(sum(tiempos) / len(tiempos), 2)
            else:
                promedio = 0

            titulo = big_font.render(
                "Resultados finales",
                True,
                (0, 0, 0)
            )

            txt3 = font.render(
                f"Tiempo promedio: {promedio} s",
                True,
                (0, 0, 0)
            )

            screen.blit(txt3, (WIDTH//2 - 120, 350))

            screen.blit(
                titulo,
                (
                    WIDTH//2 - titulo.get_width()//2,
                    150
                )
            )

            txt1 = font.render(
                f"Aciertos: {aciertos}",
                True,
                GREEN
            )

            txt2 = font.render(
                f"Errores: {errores}",
                True,
                RED
            )

            screen.blit(txt1, (WIDTH//2 - 80, 250))
            screen.blit(txt2, (WIDTH//2 - 80, 300))

            mouse_pos = pygame.mouse.get_pos()

            boton_menu = pygame.Rect(
                WIDTH//2 - 75,
                400,
                150,
                60
            )

            color = HOVER if boton_menu.collidepoint(mouse_pos) else BUTTON

            pygame.draw.rect(screen, color, boton_menu)

            txt = font.render("Menú", True, WHITE)

            screen.blit(
                txt,
                (
                    boton_menu.x + 35,
                    boton_menu.y + 15
                )
            )
                


        if estado == "mostrando_resultado":

            if time.time() - mensaje_tiempo > 1:

                if ronda_actual < TOTAL_RONDAS:
                    ronda_actual += 1
                    nueva_actividad()
                    mensaje = ""
                    estado = "jugando"

                else:

                    estado = "fin"
                    if tiempos:
                        promedio = round(sum(tiempos) / len(tiempos), 2)
                    else:
                        promedio = 0
                    #guarda los resultados en el archivo del paciente
                    guardar_resultado("secuenciacion_resumen", {
                        "aciertos": aciertos,
                        "errores": errores,
                        "tiempo_promedio": promedio,
                        "tiempos_rondas": tiempos
                    })
        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return
            
            if event.type == pygame.MOUSEBUTTONDOWN:

                if estado == "jugando":

                    for i, rect in enumerate(botones):

                        if rect.collidepoint(event.pos):

                            paso = pasos[i]

                            if paso not in seleccionados:

                                seleccionados.append(paso)

                                if len(seleccionados) == len(pasos_correctos):
                                    tiempo_total = round(time.time() - inicio_tiempo, 2)
                                    tiempos.append(tiempo_total)

                                    correcto = seleccionados == pasos_correctos
                                    #cuenta la cantidad de rondas correctas e incorrectas
                                    if correcto:
                                        mensaje = "Correcto"
                                        aciertos += 1 
                                    else:
                                        mensaje = "Incorrecto"
                                        errores += 1 

                                    mensaje_tiempo = time.time()
                                    estado = "mostrando_resultado"

                #define qué hacen los clicks en resultado
                elif estado == "resultado":

                    if boton_reintentar.collidepoint(event.pos):
                        if ronda_actual < TOTAL_RONDAS:
                            ronda_actual += 1
                            nueva_actividad()
                            mensaje = ""
                            estado = "jugando"
                        else:
                            mensaje = "Fin de la ronda"
                            estado = "fin"

                    if boton_menu.collidepoint(event.pos):
                        return   # vuelve al menú
                    
                elif estado == "fin":
                    if boton_menu.collidepoint(event.pos):

                        return

        clock.tick(60)