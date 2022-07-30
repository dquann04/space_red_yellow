import pygame
pygame.font.init()
pygame.mixer.init()
GUN_SOUND = pygame.mixer.Sound("/Users/quankento/Desktop/12_beginner_projects/PygameForBeginners-main/Assets/Gun+Silencer.mp3")
HIT_SOUND = pygame.mixer.Sound("/Users/quankento/Desktop/12_beginner_projects/PygameForBeginners-main/Assets/Grenade+1.mp3")
HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)
WHITE = (255, 255, 255)
BLUE = (113,201,221,255)
ORANGE = (238,148,74,255)
FPS = 144
VEL = 5
BULLET_VEL = 10
DISPLAY_WIDTH, DISPLAY_HEIGTH = 1500, 1000
WIDTH, HEIGHT = 70, 60
WIN = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGTH))
pygame.display.set_caption("Quan is so dep zai")
SPACESHIP_RED = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("/Users/quankento/Downloads/Subject 3.png"), (WIDTH, HEIGHT)), 270)
SPACESHIP_YELLOW = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("/Users/quankento/Downloads/Subject 4.png"), (WIDTH, HEIGHT)), 90)
SPACE = pygame.transform.scale(pygame.image.load("/Users/quankento/Downloads/wp8969186.jpg"), (DISPLAY_WIDTH, DISPLAY_WIDTH))
BORDER = pygame.Rect(DISPLAY_WIDTH//2 - 1, 0, 2, DISPLAY_HEIGTH)
red_bullets = []
yellow_bullets = []
RED_HIT = pygame.USEREVENT + 1
YELLOW_HIT = pygame.USEREVENT + 2
MAX_BULLETS = 10

def draw_display(red, yellow, 
                 red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    red_health_text = HEALTH_FONT.render(f"HEALTH: {red_health}", 1, BLUE)
    yellow_health_text = HEALTH_FONT.render(f"HEALTH: {yellow_health}", 1, BLUE)
    WIN.blit(red_health_text, (10, 10))
    WIN.blit(yellow_health_text, (DISPLAY_WIDTH - 10 - yellow_health_text.get_width(), 10))
    WIN.blit(SPACESHIP_RED, (red.x, red.y))
    WIN.blit(SPACESHIP_YELLOW, (yellow.x, yellow.y))
    pygame.draw.rect(WIN, WHITE, BORDER)
    for bullet in red_bullets:
        pygame.draw.rect(WIN, BLUE, bullet)
    
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, ORANGE, bullet)
    pygame.display.update()
        
def handle_movement(keys_pressed, red, yellow, red_bullets, yellow_bullets):
    if keys_pressed[pygame.K_a] and red.x - VEL > 0:
        red.x -= VEL
    if keys_pressed[pygame.K_d] and red.x + WIDTH < BORDER.x:
        red.x += VEL
    if keys_pressed[pygame.K_s] and red.y + 1.3*HEIGHT < DISPLAY_HEIGTH:
        red.y += VEL
    if keys_pressed[pygame.K_w] and red.y - VEL > 0:
        red.y -= VEL
    if keys_pressed[pygame.K_UP] and yellow.y - VEL > 0:
        yellow.y -= VEL
    if keys_pressed[pygame.K_DOWN] and yellow.y + 1.3*HEIGHT < DISPLAY_HEIGTH:
        yellow.y += VEL
    if keys_pressed[pygame.K_LEFT] and yellow.x - 1.7*VEL> BORDER.x:
        yellow.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and yellow.x + WIDTH < DISPLAY_WIDTH:
        yellow.x += VEL
    
    for bullet in red_bullets:
        bullet.x += BULLET_VEL
        if yellow.colliderect(bullet):
            HIT_SOUND.play()
            pygame.event.post(pygame.event.Event(RED_HIT))
            red_bullets.remove(bullet)
        elif bullet.x >= DISPLAY_WIDTH:
            red_bullets.remove(bullet)
    for bullet in yellow_bullets:
        bullet.x -= BULLET_VEL
        if red.colliderect(bullet):
            HIT_SOUND.play()
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x <= 0:
            yellow_bullets.remove(bullet)

def draw_winner(text):
    winner_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(winner_text, (DISPLAY_WIDTH/2 - winner_text.get_width()/2, DISPLAY_HEIGTH/2 - winner_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)
    
def main():
    run = True
    clock = pygame.time.Clock()
    red = pygame.Rect(100, 900, WIDTH, HEIGHT)
    yellow = pygame.Rect(1400, 100, WIDTH, HEIGHT)
    red_health = 20
    yellow_health = 20
    
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x + WIDTH, red.y + HEIGHT//2, 10, 5)
                    red_bullets.append(bullet)
                    GUN_SOUND.play()
                    
                if event.key == pygame.K_RETURN and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x, yellow.y + HEIGHT//2, 10, 5)
                    yellow_bullets.append(bullet)
                    GUN_SOUND.play()
                       
        
            if event.type == RED_HIT:
                yellow_health -= 1
            if event.type == YELLOW_HIT:
                red_health -= 1
                    
            if yellow_health <= 0:
                winner_text = "Quân đẹp trai lại thắng!"
                draw_winner(winner_text)
                main() 
            if red_health <= 0:
                winner_text = "RIGHT WINS!"
                draw_winner(winner_text)
                main()
                
        keys_pressed = pygame.key.get_pressed()
        handle_movement(keys_pressed, red, yellow, red_bullets, yellow_bullets)
        draw_display(red, yellow, red_health, yellow_health)
       

if __name__ == "__main__":
    main()