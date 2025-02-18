import time
import random
import pygame
from curvas import get_track_offset

class GameLogic:
    def __init__(self):
        # Posición y velocidades del coche
        self.car_x = 0.0
        self.car_z = 0.0
        self.car_speed_x = 0.0
        self.car_speed_z = 0.0
        
        # Estado de la pista y obstáculos
        self.track_length = 50
        self.obstacles = []
        
        # Vidas y colisiones
        self.attempts = 3
        self.last_collision_time = 0
        self.intangible = False  # Indica si el coche es invulnerable tras una colisión
        
        # Límites y ajustes de movimiento
        self.max_distance = 1000
        self.acceleration = 0.5
        self.friction = 0.05

    def generate_obstacle(self):
        """
        Genera un obstáculo en la pista basado en la velocidad y distancia recorrida.
        """
        base_probability = 0.15  # Probabilidad base de generar un obstáculo
        speed_factor = min(1.0, abs(self.car_speed_z) / 0.5)
        distance_factor = min(1.0, self.car_z / 500)
        
        spawn_probability = base_probability + (speed_factor * 0.1) + (distance_factor * 0.1)
        
        if random.random() < spawn_probability:
            curve_offset = get_track_offset(self.car_z - self.track_length)
            
            # Evitar generación de obstáculos demasiado cercanos
            if self.obstacles and abs(self.car_z - self.obstacles[-1]["z"]) < 3:
                return
            
            # Generar el obstáculo con características variadas
            obstacle_type = random.choice(["pequeño", "grande", "movil"])
            size = 0.5 if obstacle_type == "pequeño" else (1.0 if obstacle_type == "grande" else 0.7)
            direction = random.choice([-0.02, 0.02]) if obstacle_type == "movil" else 0
            
            self.obstacles.append({
                "x": curve_offset + random.uniform(-2, 2),
                "z": self.car_z - self.track_length,
                "size": size,
                "type": obstacle_type,
                "direction": direction
            })

    def check_collisions(logic):
        """
        Revisa las colisiones entre el coche y los obstáculos, considerando diferentes tamaños y tipos de obstáculos.
        """
        if logic.intangible:
            if time.time() - logic.last_collision_time > 3:
                logic.intangible = False
        else:
            for obs in logic.obstacles:
                obs_x, obs_z = obs["x"], obs["z"]
                obs_size = obs["size"]  # Tamaño del obstáculo
                
                if abs(logic.car_x - obs_x) < obs_size and abs(logic.car_z - obs_z) < obs_size:
                    logic.attempts -= 1
                    logic.last_collision_time = time.time()
                    logic.intangible = True
                    logic.car_speed_z = 0.0
                    logic.car_x += random.choice([-0.5, 0.5])
                    obs["z"] += 2
                    break


    def update(self, keys):
        """
        Actualiza el estado del juego basándose en las teclas presionadas.
        Calcula la velocidad y actualiza la posición del coche, así como la longitud de la pista y los obstáculos.
        Retorna la velocidad actual y la distancia recorrida.
        """
        base_speed = -0.2
        distance_travelled = abs(self.car_z)
        speed_multiplier = 1 + (distance_travelled // 40) * 0.2
        current_speed = base_speed * speed_multiplier

        # Movimiento hacia adelante
        if keys[pygame.K_UP] and distance_travelled < self.max_distance:
            self.car_speed_z = current_speed
            self.track_length += 2
            self.generate_obstacle()
        else:
            self.car_speed_z = 0.0

        # Movimiento lateral
        if keys[pygame.K_LEFT] and self.car_x > -5:
            self.car_speed_x = -0.1
        elif keys[pygame.K_RIGHT] and self.car_x < 5:
            self.car_speed_x = 0.1
        else:
            self.car_speed_x = 0.0

        # Actualización de la posición
        self.car_x += self.car_speed_x
        self.car_z += self.car_speed_z

        return current_speed, distance_travelled

    def restart_game(self):
        """
        Reinicia el estado del juego a sus valores iniciales.
        """
        self.car_x = 0.0
        self.car_z = 0.0
        self.car_speed_x = 0.0
        self.car_speed_z = 0.0
        self.track_length = 50
        self.obstacles.clear()
        self.attempts = 3
        self.intangible = False
