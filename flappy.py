import pygame
import sys
import random

# Inisialisasi pygame
pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
pygame.init()

# Layar permainan
screen = pygame.display.set_mode((864, 860))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF', 40)

# Variabel permainan
gravity = 0.25
bird_movement = 0
game_active = False  # Ganti jadi False agar jeda muncul di awal
score = 0
high_score = 0

# Load gambar dan inisialisasi objek
background_surface = pygame.image.load('bg6.jpg').convert()
floor_surface = pygame.image.load('ground5.jpg').convert()
floor_x_position = 0
bird_upflap = pygame.image.load('bird2.png').convert_alpha()
bird_upflap = pygame.transform.scale(bird_upflap, (int(bird_upflap.get_width() * 1.5), int(bird_upflap.get_height() * 1.5)))
bird_frames = [bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rectangle = bird_surface.get_rect(center=(100, 512))

pipe_surface = pygame.image.load('pipe-red.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)  # event triggered every 1.5 seconds
pipe_height = [400, 600, 800]

game_over_surface = pygame.image.load('message.png').convert_alpha()
game_over_surface = pygame.transform.scale2x(game_over_surface)
game_over_rectangle = game_over_surface.get_rect(center=(420, 512))

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound_countdown = 260

# Fungsi untuk menggambar lantai
def draw_floor():
    screen.blit(floor_surface, (floor_x_position, 760))
    screen.blit(floor_surface, (floor_x_position + 900, 800))

def draw_floor():
	screen.blit(floor_surface,(floor_x_position,760))
	screen.blit(floor_surface,(floor_x_position + 900,800))

# Membuat pasangan pipa 
def create_pipe():
	random_pipe_position = random.choice(pipe_height)
	bottom_pipe = pipe_surface.get_rect(midtop = (700,random_pipe_position))
	top_pipe = pipe_surface.get_rect(midbottom = (700,random_pipe_position-250))
	return bottom_pipe, top_pipe

# Menggerakkan pipa ke kiri
def move_pipes(pipes):
	for pipe in pipes:
		pipe.centerx -= 5
	return pipes

# Menggambar pipa-pipa pada layar
def draw_pipes(pipes):
	for pipe in pipes:
		if pipe.bottom >= 1024:
			screen.blit(pipe_surface, pipe)
		else:
			flip_pipe = pygame.transform.flip(pipe_surface, False, True)
			screen.blit(flip_pipe, pipe)

# Memeriksa tabrakan antara burung dan pipa atau lantai
def check_collision(pipes):
	for pipe in pipes:
		if bird_rectangle.colliderect(pipe):
			death_sound.play()
			return False
		
	if bird_rectangle.top <= -100 or bird_rectangle.bottom >= 900:
		return False
	return True
#  Memutar gambar burung sesuai dengan pergerakannya
def rotate_bird(bird):
	new_bird = pygame.transform.rotozoom(bird, -bird_movement*3, 1)
	return new_bird

# Menampilkan skor di layar.
def score_display(game_state):
	if game_state == 'main_game':
		score_surface = game_font.render(str(int(score)), True, (255,255,255))
		score_rectangle = score_surface.get_rect(center = (screen.get_width() // 2, 100))
		screen.blit(score_surface, score_rectangle)

	if game_state == 'game_over':
		score_surface = game_font.render(f'Score: {int(score)}', True, (255,255,255))
		score_rectangle = score_surface.get_rect(center = (screen.get_width() // 2, 100))
		screen.blit(score_surface, score_rectangle)

		high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255,255,255))
		high_score_rectangle = high_score_surface.get_rect(center = (screen.get_width() // 2, 185))
		screen.blit(high_score_surface, high_score_rectangle)

# Memperbarui skor tertinggi jika skor saat ini lebih tinggi
def update_score(score, high_score):
	if score > high_score:
		high_score = score
	return high_score
# Tampilkan jeda selama 5 detik
countdown = 5
while countdown > 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(background_surface, (0, 0))
    draw_floor()  # Menambahkan tampilan lantai selama countdown

    count_surface = game_font.render(f"Game starts in: {countdown}", True, (255, 255, 255))
    count_rectangle = count_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(count_surface, count_rectangle)

    pygame.display.update()
    clock.tick(1)
    countdown -= 1
countdown = 5
game_active = True  # Setelah jeda selesai, ubah ke True untuk memulai permainan

# Mulai loop utama permainan
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 8
                flap_sound.play()

            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rectangle.center = (100, 512)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    screen.blit(background_surface, (0, 0))

    if game_active:
        # bird movement
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rectangle.centery += bird_movement
        screen.blit(rotated_bird, bird_rectangle)
        game_active = check_collision(pipe_list)

        # pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        score += 0.01
        score_display('main_game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound_countdown = 100

    else:
        screen.blit(game_over_surface, game_over_rectangle)
        high_score = update_score(score, high_score)
        score_display('game_over')

    # Floor
    floor_x_position -= 1
    draw_floor()
    if floor_x_position <= -0:
        floor_x_position = 0

    pygame.display.update()
    clock.tick(120)