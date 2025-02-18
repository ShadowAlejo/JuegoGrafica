import time
import random

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
