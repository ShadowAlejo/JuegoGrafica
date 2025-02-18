import numpy as np

def configure_perspective(width, height, fov=45, near=0.1, far=100.0):
    """
    Crea una matriz de proyección perspectiva utilizando numpy.

    Args:
        width (int): Ancho de la ventana.
        height (int): Altura de la ventana.
        fov (float): Campo de visión en grados.
        near (float): Plano cercano.
        far (float): Plano lejano.

    Retorna:
        np.ndarray: Matriz de proyección 4x4.
    """
    aspect = width / height
    f = 1.0 / np.tan(np.radians(fov) / 2.0)
    projection_matrix = np.zeros((4, 4), dtype=np.float32)
    projection_matrix[0, 0] = f / aspect
    projection_matrix[1, 1] = f
    projection_matrix[2, 2] = (far + near) / (near - far)
    projection_matrix[2, 3] = (2 * far * near) / (near - far)
    projection_matrix[3, 2] = -1.0
    return projection_matrix

def update_camera_view(camera_position, target_position, up_vector=(0.0, 1.0, 0.0)):
    """
    Calcula la matriz de vista (lookAt) utilizando numpy.

    Args:
        camera_position (tuple): Posición de la cámara (eye).
        target_position (tuple): Punto al que la cámara está mirando.
        up_vector (tuple): Vector 'up' que define la orientación vertical.

    Retorna:
        np.ndarray: Matriz de vista 4x4.
    """
    eye = np.array(camera_position, dtype=np.float32)
    target = np.array(target_position, dtype=np.float32)
    up = np.array(up_vector, dtype=np.float32)

    # Calcular el vector forward y normalizarlo
    forward = target - eye
    forward = forward / np.linalg.norm(forward)

    # Calcular el vector side y normalizarlo
    side = np.cross(forward, up)
    side = side / np.linalg.norm(side)

    # Corregir el vector up
    up_corrected = np.cross(side, forward)

    # Construir la matriz de vista (lookAt)
    view_matrix = np.identity(4, dtype=np.float32)
    view_matrix[0, 0:3] = side
    view_matrix[1, 0:3] = up_corrected
    view_matrix[2, 0:3] = -forward
    view_matrix[0, 3] = -np.dot(side, eye)
    view_matrix[1, 3] = -np.dot(up_corrected, eye)
    view_matrix[2, 3] = np.dot(forward, eye)
    return view_matrix
