import pygame
import random
 
pygame.init()
#set up
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Zombie Game")
player = pygame.Rect(400, 300, 50, 50)
zombie = pygame.Rect(0, 0, 50, 50)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 72)
font_score = pygame.font.Font(None, 42)
text = font.render("Game Over", True, (255, 0, 0))
last_shot = 0
fire_rate = 250
running = True
game_over = False
max_spawn = 2
score = 0
zombies=[]
bullets=[]
#main game loop
while running:
    keys = pygame.key.get_pressed()
    clock.tick(60)
    screen.fill((255, 255, 255))
    if not game_over:
        pygame.draw.rect(screen, (0, 100, 255), player)
        #bullet shoot
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            if pygame.time.get_ticks() - last_shot > fire_rate:
                player_pos = pygame.math.Vector2(player.centerx, player.centery)
                mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())
                direction = mouse_pos - player_pos
                direction.normalize_ip()
                bullet = {"pos": player_pos, "dir": direction}
                bullets.append(bullet)
                last_shot = pygame.time.get_ticks()
        #zombie spawn
        zsp = {
            1: (0,0),
            2: (0,600),
            3: (800,0),
            4: (800, 600)
        }
        if len(zombies) < max_spawn:
          zombie_spawn =  pygame.math.Vector2(zsp[random.randint(1, 4)])
          zombie = {"pos": zombie_spawn}
          zombies.append(zombie)
        #zombie logic
        for zombie in zombies[:]:
            if zombie["pos"].x < player.centerx:
                zombie["pos"].x += 2
            if zombie["pos"].x > player.centerx:
                zombie["pos"].x -= 2
            if zombie["pos"].y < player.centery:
                zombie["pos"].y += 2
            if zombie["pos"].y > player.centery:
                zombie["pos"].y -= 2
            pygame.draw.rect(screen, (0,225,0), (int(zombie["pos"].x), int(zombie["pos"].y), 50, 50))
        for zombie in zombies:
            zombie_rect = pygame.Rect(zombie["pos"].x, zombie["pos"].y, 50, 50)
            if zombie_rect.colliderect(player):
                game_over = True
        #zombie and bullet colision
        for zombie in zombies[:]:
            zombie_rect = pygame.Rect(zombie["pos"].x, zombie["pos"].y, 50, 50)
            for bullet in bullets[:]:
                bullet_rect = pygame.Rect(bullet["pos"].x, bullet["pos"].y, 10, 10)
                if bullet_rect.colliderect(zombie_rect):
                    zombies.remove(zombie)
                    bullets.remove(bullet)
                    score += 100
        #bullet logic
        for bullet in bullets[:]:
            bullet["pos"] += bullet["dir"] * 12
            pygame.draw.circle(screen, (255,0,0), (int(bullet["pos"].x), int(bullet["pos"].y)), 7)
            if not screen.get_rect().collidepoint(bullet["pos"].x, bullet["pos"].y):
                bullets.remove(bullet)
        #player movement
        if keys[pygame.K_a]:
            player.x -= 5
        if keys[pygame.K_d]:
            player.x += 5
        if keys[pygame.K_w]:
            player.y -= 5
        if keys[pygame.K_s]:
            player.y += 5
        player.clamp_ip(screen.get_rect())
        #score = more zombies
        max_spawn = 2 + score // 1000
        #score
        score_render = font_score.render(f"Score: {score}", True, (255, 0, 0))
        screen.blit(score_render, (0, 0))
    #quit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #game over text
    if game_over:
        screen.blit(text, (300, 250))
    #restart game
    if game_over and keys[pygame.K_SPACE]:
        last_shot = 0
        running = True
        max_spawn = 2
        score = 0
        zombies=[]
        bullets=[]
        game_over = False
    pygame.display.flip()
pygame.quit()