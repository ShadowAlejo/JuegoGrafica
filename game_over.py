import pygame

def handle_game_over(logic, font, screen):
    """
    Muestra en pantalla el mensaje de "GAME OVER" y espera a que el usuario presione 'R' para reiniciar.
    
    Args:
        logic: Instancia de GameLogic, que debe disponer de un método restart_game().
        font: Objeto pygame.font.Font para renderizar el texto.
        screen: Superficie de pantalla de pygame.
    """
    # Renderizar los textos de "GAME OVER" y "Presiona 'R' para reiniciar"
    game_over_text = font.render("GAME OVER", True, (255, 0, 0))
    restart_text = font.render("Presiona 'R' para reiniciar", True, (255, 255, 255))
    
    # Calcular posiciones para centrar los textos en pantalla
    screen_rect = screen.get_rect()
    game_over_rect = game_over_text.get_rect(center=(screen_rect.centerx, screen_rect.centery - 30))
    restart_rect = restart_text.get_rect(center=(screen_rect.centerx, screen_rect.centery + 30))
    
    # Mostrar los textos en pantalla
    screen.blit(game_over_text, game_over_rect)
    screen.blit(restart_text, restart_rect)
    pygame.display.flip()
    
    # Esperar a que el usuario presione 'R' para reiniciar
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    logic.restart_game()
                    waiting = False
