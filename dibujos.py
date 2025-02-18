from OpenGL.GL import *

def draw_model_wavefront(scene, override_color=None):
    """
    Dibuja un modelo 3D cargado con PyWavefront usando los valores del material
    definidos en el archivo MTL. Si se proporciona un override_color, se usará ese
    color en lugar del definido en el material.
    """
    for mesh in scene.mesh_list:
        if not hasattr(mesh, 'materials') or not mesh.materials:
            glColor3f(1, 1, 1)
        else:
            mat = mesh.materials[0]
            if override_color is not None:
                r, g, b = override_color
                glColor3f(r, g, b)
            else:
                try:
                    # Usamos el color difuso definido en el material (MTL)
                    r, g, b = mat.diffuse[:3]
                    glColor3f(r, g, b)
                except AttributeError:
                    glColor3f(1, 1, 1)
        glBegin(GL_TRIANGLES)
        for face in mesh.faces:
            for vertex_i in face:
                x, y, z = scene.vertices[vertex_i]
                glVertex3f(x, y, z)
        glEnd()

def draw_text(message, x, y, font, screen, color=(255, 255, 255)):
    """
    Dibuja un texto en la pantalla.
    Se requiere pasar el objeto font y la superficie screen de pygame.
    """
    glDisable(GL_DEPTH_TEST)
    text_surface = font.render(message, True, color)
    screen.blit(text_surface, (x, y))
    glEnable(GL_DEPTH_TEST)


def draw_cube():
    """
    Dibuja un cubo wireframe que se usa como fallback o para representar obstáculos.
    """
    vertices = [
        [-0.5, -0.5, -0.5],
        [ 0.5, -0.5, -0.5],
        [ 0.5,  0.5, -0.5],
        [-0.5,  0.5, -0.5],
        [-0.5, -0.5,  0.5],
        [ 0.5, -0.5,  0.5],
        [ 0.5,  0.5,  0.5],
        [-0.5,  0.5,  0.5]
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ]
    glBegin(GL_LINES)
    for edge in edges:
        glNormal3f(0, 1, 0)
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def draw_obstacles(logic):
    """
    Dibuja todos los obstáculos almacenados en el objeto de lógica del juego.
    """
    glBindTexture(GL_TEXTURE_2D, 0)
    glColor3f(1, 0, 0)
    for obs in logic.obstacles:
        glPushMatrix()
        glTranslatef(obs["x"], 0, obs["z"])  # Corregido para usar claves en el diccionario
        glScalef(obs["size"], obs["size"], obs["size"])  # Ajusta el tamaño según el tipo de obstáculo
        draw_cube()
        glPopMatrix()

def draw_car(logic, car_model):
    """
    Dibuja el coche según el estado de la lógica del juego. Si el modelo está disponible,
    se dibuja usando PyWavefront; de lo contrario, se dibuja un cubo.
    Se aplica un override de color si el coche es intangible.
    """
    glPushMatrix()
    glTranslatef(logic.car_x, 0.0, logic.car_z)
    glRotatef(180, 0, 1, 0)
    glScalef(0.5, 0.5, 0.5)
    if car_model:
        if logic.intangible:
            draw_model_wavefront(car_model, override_color=(1.0, 1.0, 0.0))
        else:
            draw_model_wavefront(car_model)
    else:
        if logic.intangible:
            glColor3f(1, 1, 0)
        else:
            glColor3f(1, 0, 0)
        draw_cube()
    glPopMatrix()

def draw_track(logic, road_texture_id, track_width=10, resolution=1, tex_scale=10):
    """
    Dibuja la pista curvada adaptando la textura a la curvatura real.
    
    Para forzar que la imagen se adapte a las curvas, se calcula la longitud de arco a lo largo de
    la pista y, además, se calcula el vector normal local para cada punto de la curva. Esto permite
    determinar correctamente los vértices izquierdo y derecho de la pista y mapear la textura de 
    forma que se mantenga su orientación a lo largo de las curvas.
    
    Args:
        logic: Objeto de la lógica del juego, que contiene la longitud de la pista (logic.track_length).
        road_texture_id: ID de la textura cargada para la pista.
        track_width (float): Ancho total de la pista.
        resolution (float): Distancia en metros entre puntos para generar la curva.
        tex_scale (float): Factor de escala para el mapeo de la textura en el eje v.
    """
    from curvas import generate_curve_points
    import math

    glBindTexture(GL_TEXTURE_2D, road_texture_id)
    glColor3f(1, 1, 1)

    # Generar puntos de la pista
    total_length = logic.track_length + 10
    z_points, x_offsets = generate_curve_points(total_length, resolution=resolution)

    # Calcular la longitud de arco acumulada a lo largo de la pista
    arc_lengths = [0.0]
    for i in range(1, len(z_points)):
        dx = x_offsets[i] - x_offsets[i - 1]
        dz = z_points[i] - z_points[i - 1]
        arc_segment = math.sqrt(dx * dx + dz * dz)
        arc_lengths.append(arc_lengths[-1] + arc_segment)

    # Calcular el vector normal para cada vértice usando diferencias finitas
    n = len(z_points)
    normals = []
    for i in range(n):
        # Calculamos la derivada (tangente) en el punto i:
        if i == 0:
            dx = x_offsets[i+1] - x_offsets[i]
            dz = z_points[i+1] - z_points[i]
        elif i == n - 1:
            dx = x_offsets[i] - x_offsets[i-1]
            dz = z_points[i] - z_points[i-1]
        else:
            dx = (x_offsets[i+1] - x_offsets[i-1]) / 2.0
            dz = (z_points[i+1] - z_points[i-1]) / 2.0
        
        # En nuestro sistema, el centro de la pista es: C = (x_offsets[i], -z_points[i])
        # La tangente T = (dx, -dz) (ya que usamos -z para los vértices)
        # Un vector normal (a la izquierda) es: N = (T_z, -T_x) = (-(-dz), -dx) = (dz, -dx)
        length = math.sqrt(dx * dx + dz * dz)
        if length != 0:
            nx = dz / length
            ny = -dx / length
        else:
            nx, ny = 0, 0
        normals.append((nx, ny))
    
    # Dibujar la pista usando GL_QUAD_STRIP con mapeo de textura basado en la longitud de arco
    glBegin(GL_QUAD_STRIP)
    for i, (z, arc) in enumerate(zip(z_points, arc_lengths)):
        # Centro de la pista en coordenadas 3D (usamos -z para la profundidad)
        center_x = x_offsets[i]
        center_z = -z
        
        # Desplazar el centro usando el vector normal para obtener los bordes
        nx, ny = normals[i]
        left_x = center_x - (track_width / 2) * nx
        left_z = center_z - (track_width / 2) * ny
        right_x = center_x + (track_width / 2) * nx
        right_z = center_z + (track_width / 2) * ny

        # Asignar la coordenada de textura: u=0 para el borde izquierdo, u=1 para el derecho;
        # v se basa en la longitud de arco
        v_coord = arc / tex_scale
        glTexCoord2f(0.0, v_coord)
        glVertex3f(left_x, -0.5, left_z)
        glTexCoord2f(1.0, v_coord)
        glVertex3f(right_x, -0.5, right_z)
    glEnd()

def draw_barriers(logic):
    """
    Dibuja las barreras a lo largo de la pista.
    Se generan en intervalos definidos por la longitud de la pista.
    """
    glBindTexture(GL_TEXTURE_2D, 0)
    glColor3f(1, 0, 0)
    glBegin(GL_QUADS)
    for i in range(0, logic.track_length, 10):
        glNormal3f(0, 1, 0)
        # Barrera izquierda
        glVertex3f(-5.5, -0.5, -i - 10)
        glVertex3f(-5.3, -0.5, -i - 10)
        glVertex3f(-5.3,  0.5, -i)
        glVertex3f(-5.5,  0.5, -i)
        # Barrera derecha
        glVertex3f(5.3, -0.5, -i - 10)
        glVertex3f(5.5, -0.5, -i - 10)
        glVertex3f(5.5,  0.5, -i)
        glVertex3f(5.3,  0.5, -i)
    glEnd()
