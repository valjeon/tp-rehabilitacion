import random
import pygame
import os
import guardar_datos 
from datos_fonologicos import ejemplo1

ANCHO = 800
ALTO = 600
X = 50
WIDTH = 700

pygame.init()

pantalla = pygame.display.set_mode((800, 600)) #defino el tamaño de la pantalla del juego
pygame.display.set_caption("Prueba de Denominación Fonológica") #Título de la pestaña de pygame


def dibujar_texto_ajustado(surface, texto,y,font, color):

    rect = pygame.Rect(100, y, 600, 100)
    lineas = []
    palabras = texto.split(" ")
    linea = ""
    for p in palabras:
        prueba = linea + p + " "
        if font.size(prueba)[0] <= rect.width:
            linea = prueba
        else:
            lineas.append(linea)
            linea = p + " "

    lineas.append(linea)

    total_altura = len(lineas) * font.get_height()
    y_offset = rect.y + (rect.height - total_altura) // 2

    for linea in lineas:
        render = font.render(linea.strip(), True, color)
        x_texto = rect.x + (rect.width - render.get_width()) // 2

        surface.blit(render, (x_texto, y_offset))
        y_offset += font.get_height()
    
#Defino una función que haga el juego con las fotos dadas como datos
def selecciones():
    carpeta = os.path.dirname(__file__)
    foto_juego = random.choice(ejemplo1) #selecciona una de las fotos dadas en las posibles
    opciones = foto_juego["opciones"] #selecciona las opciones posibles en las que distinguir la foto
    #Todos los comandos para buscar las fotos en mi carpeta
    ruta = os.path.join(carpeta, foto_juego["imagen"])
    imagen = pygame.image.load(ruta)
    imagen = pygame.transform.scale(imagen, (300, 300))

    return foto_juego, opciones, imagen #la función devuelve todo para ya dejar listo el juego

def prueba_fonologica():
    #carpeta = os.path.dirname(__file__)
    fuente = pygame.font.SysFont(None, 40)

    tiempo_inicio_jugada = 0 #las dos  variables donde voy a contabilizar cuanto tarda en el juego el paciente
    tiempo_total_jugando = 0
    tiempos_respuesta = []
    correctas=0
    incorrectas=0

    #Acá defino todo para la primera parte del juego en la ventana de inicio
    estado = "intro"
    foto_juego, opciones, imagen = None, None, None
    botones_fin = [] #Donde van a guardarse los datos para seleccionar en el pygame
    ciclos = 0 #Porque quiero que la persona haga 10 ciclos para evaluar su condición antes de ver si quiere seguir jugando o no

    # Variables para el mensaje correcto/incorrecto
    tiempo_mensaje = 0
    duracion_mensaje = 500
    rect_volver = None
    running = True

    fuente_grande = pygame.font.SysFont(None, 60) #Otra vez hay dos mensajes de tamaño distinto que quiero que estén en la pantalla
    fuente_chica = pygame.font.SysFont(None, 40)


    while running:
        pantalla.fill((255, 255, 255))
        mouse_pos = pygame.mouse.get_pos() #Ve donde se posiciona el mouse

        # -------- EVENTOS --------
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #Cuando selecciona que quiere salir, cambio el estado a falso que detiene el while
                print("click detectado")
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if estado == "intro": #Cosa de que cuando arranca la prueba le muestre la pantalla de "bienvenida"
                    if rect_comenzar.collidepoint(mouse_pos):
                        foto_juego, opciones, imagen = selecciones() #Le paso todo para que haga una seleccion random entre los de ejemplo1
                        tiempo_inicio_jugada = pygame.time.get_ticks()
                        estado = "jugando" #le cambio el estado para ir a la siguiente vista en el juego y poder jugar efectivamente

                elif estado == "jugando":
                    for rect, texto, texto_rect, opcion in botones:
                        if rect.collidepoint(mouse_pos):
                            ciclos += 1 #cuento que va con la primera foto
                            tiempo_respuesta = pygame.time.get_ticks() - tiempo_inicio_jugada
                            tiempos_respuesta.append(tiempo_respuesta / 1000)  # in seconds
                            if opcion == foto_juego["correcta"]: #le paso la clave que es correcta con respecto a la imagen elegida
                                correctas+=1
                                estado = "correcto" #le pongo este estado para que le aparezca despues el mensaje de que está bien
                            else:
                                incorrectas+=1
                                estado = "incorrecto" #caso de que este mal, le pongo la pantala que dice incorrecto
                            tiempo_mensaje = pygame.time.get_ticks()

                elif estado == "fin_ciclos": #una vez que hace 10 ciclos, consideramos que se evaluo la condición, le pregunto al paciente qué quiere hacer
                    for rect, texto_btn, texto_rect_btn, opcion in botones_fin:
                        if rect.collidepoint(mouse_pos):
                            if opcion == "Si":
                                ciclos = 0  # Reiniciar contador cosa de que si quiere seguir jugando pueda
                                foto_juego, opciones, imagen = selecciones() #Se repite el juego nuevamente
                                tiempo_inicio_jugada = pygame.time.get_ticks() #Si quiere volver a jugar, le seteo donde arranca nuevamente
                                estado = "jugando" #Para que vuelva al juego
                            elif opcion == "No":
                                estado = "final" #Le pongo los resultados en la pantalla

                elif estado == "final":
                    if rect_volver.collidepoint(mouse_pos):
                        datos = {
                                "correctas": correctas,
                                "incorrectas": incorrectas,
                                "tiempos_respuesta": tiempos_respuesta,
                                "tiempo_promedio": sum(tiempos_respuesta) / len(tiempos_respuesta) if tiempos_respuesta else 0
                            }
                
                        guardar_datos.guardar_resultado(
                                "Prueba Fonológica",
                                datos
                        )
                        return

        # Parte de visuales del pygame
        if estado == "intro": 
            #Le pongo lo que quiero que muestre en esa "bienvenida" a la prueba
            y = 140
            espacio = 30

            dibujar_texto_ajustado(
                pantalla,
                "Comenzarás una prueba de denominación fonológica",
                y,
                fuente_grande,
                (0, 0, 0)
            )

            y += 100 + espacio

            dibujar_texto_ajustado(
                pantalla,
                "Recordá que tenés que elegir la palabra que corresponde a la foto que aparece en la pantalla",
                y,
                fuente_chica,
                (0, 0, 0)
            )

            y += 100 + espacio

            dibujar_texto_ajustado(
                pantalla,
                "¿Estás listo?",
                y,
                fuente_chica,
                (0, 0, 0)
            )

            # Botón Comenzar para que pueda elegir cuando arrancar concretamente, le defino posición y colores
            ancho_boton = 250
            alto_boton = 60
            x_boton = (pantalla.get_width() - ancho_boton) // 2
            y_boton = 500
            rect_comenzar = pygame.Rect(x_boton, y_boton, ancho_boton, alto_boton)

            color_boton = (100, 180, 255)
            pygame.draw.rect(pantalla, color_boton, rect_comenzar, border_radius=15)
            pygame.draw.rect(pantalla, (0,0,0), rect_comenzar, 2, border_radius=15)

            fuente_btn = pygame.font.SysFont(None, 40)
            texto_boton = fuente_btn.render("Comenzar", True, (0, 0, 0))
            pantalla.blit(texto_boton, texto_boton.get_rect(center=rect_comenzar.center))

        elif estado == "jugando":
            # Donde pongo la imagen que eligio automáticament e
            x = (pantalla.get_width() - imagen.get_width()) // 2
            pantalla.blit(imagen, (x, 130))
            y = 30
            dibujar_texto_ajustado(
                pantalla,
                "¿Qué opción es la correcta?",
                y,
                fuente_chica,
                (0, 0, 0)
            )
            # Botones de opciones
            botones = []
            ancho_boton = 180
            alto_boton = 60
            espacio = 20
            y_botones = 500
            total_ancho = len(opciones)*ancho_boton + (len(opciones)-1)*espacio
            x_base = (pantalla.get_width() - total_ancho)//2

            for i, opcion in enumerate(opciones): #los ubico equiespaciados y centrados, formateando su texto
                x = x_base + i*(ancho_boton + espacio)
                rect = pygame.Rect(x, y_botones, ancho_boton, alto_boton)
                texto = fuente.render(opcion, True, (0, 0, 0))
                texto_rect = texto.get_rect(center=rect.center)
                botones.append((rect, texto, texto_rect, opcion))

                color = (100, 180, 255)
                pygame.draw.rect(pantalla, color, rect, border_radius=15)
                pygame.draw.rect(pantalla, (0, 0, 0), rect, 2, border_radius=15)
                pantalla.blit(texto, texto_rect)

        elif estado in ["correcto", "incorrecto"]: #Le seteo como quiero que se vea en la pantalla que aparece después de elegir la opción
        
                y = 180
                dibujar_texto_ajustado(
                    pantalla,
                    "¡Correcto!" if estado == "correcto" else "¡Incorrecto!",
                    y,
                    fuente_grande,
                    (0, 180, 0) if estado == "correcto" else (255, 0, 0)
                )
                y += 120
                dibujar_texto_ajustado(
                    pantalla,
                    "Siguiente pregunta...",
                    y,
                    fuente_chica,
                    (0, 0, 0)
                )
            # Le doy un tiempo de 3 segundos para poder leer ese mensaje y seguir que lo registro con un ticks y luego pasa automáticamente
                if pygame.time.get_ticks() - tiempo_mensaje > duracion_mensaje:
                    if ciclos >= 5: #si veo que pasaron esos ciclos que yo evaluo, paro y sino sigo
                        estado = "fin_ciclos"
                    else:
                        foto_juego, opciones, imagen = selecciones()
                        estado = "jugando"

        elif estado == "fin_ciclos": #una vez que ya vio 5 fotos, le pregunto si desea seguir o no
            y = 60
            dibujar_texto_ajustado(
                pantalla,
                "¡Has completado 5 pruebas!",
                y,
                fuente_grande,
                (0, 0, 0)
            )
            y += 60
            dibujar_texto_ajustado(
                pantalla,
                "¿Deseas seguir jugando?",
                y,
                fuente_grande,
                (0, 0, 0)
            )

            # BOTONES SI / NO para que elegir
            botones_fin = []
            opciones_fin = ["Si", "No"]
            ancho_boton = 120
            alto_boton = 60
            espacio = 40
            y_botones = 400
            total_ancho = len(opciones_fin)*ancho_boton + (len(opciones_fin)-1)*espacio
            x_base = (pantalla.get_width() - total_ancho)//2

            for i, opcion in enumerate(opciones_fin): #ubicación equiespaciada y bien dentro de la pantalla final
                x = x_base + i*(ancho_boton + espacio)
                rect = pygame.Rect(x, y_botones, ancho_boton, alto_boton)
                texto_btn = fuente.render(opcion, True, (0, 0, 0))
                texto_rect_btn = texto_btn.get_rect(center=rect.center)
                botones_fin.append((rect, texto_btn, texto_rect_btn, opcion))

                color = (0, 180, 0) if opcion == "Si" else (220, 0, 0)
                pygame.draw.rect(pantalla, color, rect, border_radius=15)
                pygame.draw.rect(pantalla, (0, 0, 0), rect, 2, border_radius=15)
                pantalla.blit(texto_btn, texto_rect_btn)
        
        elif estado == "final":
            y = 60
            dibujar_texto_ajustado(
                pantalla,
                "¡Enhorabuena! La prueba ya terminó",
                y,
                fuente_grande,
                (0, 0, 0)
            )
            y += 90
            dibujar_texto_ajustado(
                pantalla,
                "Tus resultados fueron los siguientes:",
                y,
                fuente_chica,
                (0, 0, 0)
            )
            
            #Armo una tabla para presentarlos
            
            y = 220
            ancho = 500
            alto = 50
            x = (pantalla.get_width() - ancho) // 2
            col1_w = int(ancho * 0.5)
            #Hago una lista con los datos que quiero mostrarle
            datos = [
                ("Correctas", correctas),
                ("Incorrectas", incorrectas),
                ("Tiempo prom. (s)", f"{sum(tiempos_respuesta)/len(tiempos_respuesta):.2f}") #Lo divido porque está en ms por el ticks y le pongo dos decimales
            ]

            #boton para volver
            ancho_boton = 220
            alto_boton = 60
            x_boton = (pantalla.get_width() - ancho_boton) // 2
            y_boton = 500

            rect_volver = pygame.Rect(x_boton, y_boton, ancho_boton, alto_boton)

            pygame.draw.rect(pantalla, (100, 180, 255), rect_volver, border_radius=15)
            pygame.draw.rect(pantalla, (0, 0, 0), rect_volver, 2, border_radius=15)

            texto_volver = fuente_chica.render("Volver", True, (0, 0, 0))
            pantalla.blit(texto_volver, texto_volver.get_rect(center=rect_volver.center))


            for i, (texto1, texto2) in enumerate(datos):

                fila_y = y + i * alto
                rect = pygame.Rect(x, fila_y, ancho, alto)

                # border
                pygame.draw.rect(pantalla, (0, 0, 0), rect, 2)

                # column split
                col1_w = int(ancho * 0.5)

                pygame.draw.line(
                    pantalla,
                    (0, 0, 0),
                    (x + col1_w, fila_y),
                    (x + col1_w, fila_y + alto),
                    2
                )

                # color logic
                if texto1 == "Correctas":
                    color = (0, 180, 0)
                elif texto1 == "Incorrectas":
                    color = (220, 0, 0)
                else:
                    color = (0, 0, 0)

                # render
                t1 = fuente_chica.render(str(texto1), True, color)
                t2 = fuente_chica.render(str(texto2), True, (0, 0, 0))

                # LEFT CELL (label)
                pantalla.blit(
                    t1,
                    t1.get_rect(midleft=(x + 15, fila_y + alto // 2))
                )

                # RIGHT CELL (value) → constrained inside right half
                right_cell_left = x + col1_w
                right_cell_width = ancho - col1_w

                pantalla.blit(
                    t2,
                    t2.get_rect(midleft=(right_cell_left + 15, fila_y + alto // 2))
                )
                    
        
        pygame.display.flip()

    return

def main():
    prueba_fonologica()