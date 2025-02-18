import numpy as np

def get_track_offset(z, segment_length=250, amplitude=2.0):
    """
    Calcula el desplazamiento lateral para la pista en función de la distancia z.
    
    Args:
        z (float): Distancia a lo largo de la pista (en metros).
        segment_length (float): Longitud de cada segmento de curva.
        amplitude (float): Amplitud máxima de la curva.
        
    Retorna:
        float: Desplazamiento lateral (offset) en la pista.
    """
    segment = int(z // segment_length)
    mod_z = z % segment_length
    sign = (-1) ** segment  # Alterna la dirección de la curva
    offset = sign * amplitude * np.sin(np.pi * mod_z / segment_length)
    return offset

def generate_curve_points(track_length, resolution=1, segment_length=250, amplitude=2.0):
    """
    Genera puntos de la pista junto con su desplazamiento lateral.
    
    Args:
        track_length (float): Longitud total de la pista en metros.
        resolution (float): Distancia entre puntos (en metros).
        segment_length (float): Longitud de cada segmento de curva.
        amplitude (float): Amplitud máxima de la curva.
    
    Retorna:
        tuple: Arrays (z_points, x_offsets)
    """
    z_points = np.arange(0, track_length + resolution, resolution)
    # Vectorizamos la función para aplicar a cada valor de z
    vectorized_offset = np.vectorize(get_track_offset, otypes=[float])
    x_offsets = vectorized_offset(z_points, segment_length, amplitude)
    return z_points, x_offsets
