import pygame
from pygame.locals import *
from OpenGL.GL import *
import pywavefront

# Importar módulos para carga de recursos, lógica del juego, iluminación, dibujos, colisiones, perspectiva y fin del juego
from cargar_recursos import cargar_textura, cargar_modelo_carro
from logica_juego import GameLogic
from iluminacion import setup_lighting
from dibujos import (
    draw_model_wavefront,
    draw_text,
    draw_cube,
    draw_obstacles,
    draw_car,
    draw_track,
    draw_barriers
)
from colisiones import check_collisions
from perspectiva import configure_perspective, update_camera_view
from game_over import handle_game_over

# CARGAR RECURSOS E INICIALIZAR LA LÓGICA DEL JUEGO

car_model = cargar_modelo_carro("Car.obj")
logic = GameLogic()

# BUCLE PRINCIPAL DEL JUEGO

def main():
    global road_texture_id, font, screen
    pygame.init()
    screen = pygame.display.set_mode((900, 700), DOUBLEBUF | OPENGL)
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 30)

    # Configurar la matriz de proyección usando la nueva implementación basada en numpy
    projection_matrix = configure_perspective(900, 700)
    glMatrixMode(GL_PROJECTION)
    glLoadMatrixf(projection_matrix.T)  # Transponer para columna mayor
    glMatrixMode(GL_MODELVIEW)

    glEnable(GL_DEPTH_TEST)
    glClearColor(0.5, 0.5, 0.5, 1.0)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_NORMALIZE)

    lighting_config = setup_lighting()

    # Configurar la iluminación (se puede optimizar, ya que setup_lighting se invoca dos veces)
    setup_lighting()
    glEnable(GL_TEXTURE_2D)

    # Cargar la textura de la pista
    road_texture_id = cargar_textura("track_texture.png")
    if road_texture_id is None:
        print("Error: No se pudo cargar la textura de la pista.")
        road_texture_id = 0

    running = True
    while running:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Verificar si se terminó el juego
        if logic.attempts <= 0:
            handle_game_over(logic, font, screen)
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Actualizar el estado del juego
        keys = pygame.key.get_pressed()
        current_speed, distance_travelled = logic.update(keys)
        check_collisions(logic)

        # Calcular y cargar la matriz de vista (lookAt) basada en la posición del coche
        camera_position = (logic.car_x, 1.5, logic.car_z + 5.0)
        target_position = (logic.car_x, 0.0, logic.car_z)
        view_matrix = update_camera_view(camera_position, target_position)
        glLoadMatrixf(view_matrix.T)  # Cargar la matriz de vista

        # Dibujar los elementos del juego utilizando las funciones del módulo 'dibujos'
        draw_track(logic, road_texture_id, track_width=10, resolution=1, tex_scale=10)
        draw_barriers(logic)
        draw_obstacles(logic)
        draw_car(logic, car_model)
        draw_text(f"Distancia: {min(distance_travelled, logic.max_distance):.1f} m", 10, 10, font, screen)
        draw_text(f"Velocidad: {abs(current_speed):.2f} m/s", 10, 40, font, screen)

        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

if __name__ == "__main__":
    main()
