import numpy as np

def setup_lighting():
    """
    Retorna una configuración de iluminación utilizando numpy, sin depender de OpenGL.
    
    La configuración incluye:
        - ambient_light: luz ambiental.
        - light_position: posición de la luz.
        - diffuse_light: luz difusa.
        - specular_light: luz especular.
    """
    config = {
        "ambient_light": np.array([0.3, 0.3, 0.3, 1.0], dtype=np.float32),
        "light_position": np.array([0.0, 10.0, 5.0, 1.0], dtype=np.float32),
        "diffuse_light": np.array([1.0, 1.0, 1.0, 1.0], dtype=np.float32),
        "specular_light": np.array([0.5, 0.5, 0.5, 1.0], dtype=np.float32)
    }
    return config
