import pygame
from OpenGL.GL import *
import pywavefront

def cargar_textura(path):
    """
    Carga una textura desde la imagen especificada en `path` y la configura para OpenGL.
    """
    try:
        surface = pygame.image.load(path)
        surface = pygame.transform.flip(surface, False, True)  # Corrige la orientación de la textura
        texture_data = pygame.image.tostring(surface, 'RGB', 1)
        width, height = surface.get_rect().size

        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
        glGenerateMipmap(GL_TEXTURE_2D)
        return tex_id
    except Exception as e:
        print(f"Error cargando textura {path}: {e}")
        return None

def cargar_modelo_carro(path):
    """
    Carga el modelo 3D del carro desde el archivo especificado en `path` usando PyWavefront.
    """
    try:
        modelo = pywavefront.Wavefront(path, create_materials=True, collect_faces=True)
        
        # Verificar los materiales cargados:
        print("Materiales cargados:")
        for mesh in modelo.mesh_list:
            for material in mesh.materials:
                # Se asume que cada material tiene la propiedad 'name' y 'diffuse'
                print(f"Material: {material.name} - Difuso: {material.diffuse}")
        
        return modelo
    except Exception as e:
        print(f"Error cargando modelo del carro {path}: {e}")
        return None

