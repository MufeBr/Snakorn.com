import pygame, sys, random, json
from pygame.math import Vector2
from pathlib import Path

# ---------------- PATHS ----------------
BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "Graphics"
SOUND_DIR = BASE_DIR / "Sound"
FONT_DIR = BASE_DIR / "Font"

# ---------- IMAGENS ----------
apple_path = ASSETS_DIR / "apple.png"
head_up_path = ASSETS_DIR / "head_up.png"
head_down_path = ASSETS_DIR / "head_down.png"
head_right_path = ASSETS_DIR / "head_right.png"
head_left_path = ASSETS_DIR / "head_left.png"
tail_up_path = ASSETS_DIR / "tail_up.png"
tail_down_path = ASSETS_DIR / "tail_down.png"
tail_right_path = ASSETS_DIR / "tail_right.png"
tail_left_path = ASSETS_DIR / "tail_left.png"
body_vertical_path = ASSETS_DIR / "body_vertical.png"
body_horizontal_path = ASSETS_DIR / "body_horizontal.png"
body_tr_path = ASSETS_DIR / "body_tr.png"
body_tl_path = ASSETS_DIR / "body_tl.png"
body_br_path = ASSETS_DIR / "body_br.png"
body_bl_path = ASSETS_DIR / "body_bl.png"

# ---------- SONS ----------
crunch_sound_path = SOUND_DIR / "crunch.wav"

# ---------- FONTE ----------
font_path = FONT_DIR / "PoetsenOne-Regular.ttf"

# ---------------- CONFIG TELA ----------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 40
CELL_NUMBER_X = SCREEN_WIDTH // CELL_SIZE
CELL_NUMBER_Y = SCREEN_HEIGHT // CELL_SIZE

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snakorn")
clock = pygame.time.Clock()

# ---------------- CORES ----------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)
ACCENT = (50, 150, 255)
BG = (30, 30, 40)
LIGHT_GRASS = (175, 215, 70)
GRASS = (167, 209, 61)
BUTTON_HOVER = (70, 70, 120)

# ---------------- INICIALIZAÇÃO ----------------
pygame.init()
apple = pygame.image.load(apple_path).convert_alpha()
crunch_sound = pygame.mixer.Sound(str(crunch_sound_path))
game_font = pygame.font.Font(str(font_path), 25)

# ---------------- HIGH SCORE ----------------
HS_FILE = "highscore.json"
try:
  with open(HS_FILE, "r") as f:
    HS = json.load(f)
except:
  HS = {"highscore": 0}


def save_highscores():
  with open(HS_FILE, "w") as f:
    json.dump(HS, f)


difficulty_speed = 9  # padrão Normal


# ---------------- FUNÇÃO TEXTOS ----------------
def draw_text(surface, text, pos, size, color, center=True, bold=False):
  font = pygame.font.Font(str(font_path), size)
  text_surf = font.render(text, bold, color)
  text_rect = text_surf.get_rect()
  if center:
    text_rect.center = pos
  else:
    text_rect.topleft = pos
  surface.blit(text_surf, text_rect)


# ---------------- CLASSES DO JOGO ----------------
class SNAKE:
  def __init__(self):
    self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
    self.direction = Vector2(1, 0)
    self.new_block = False
    # cabeças
    self.head_up = pygame.image.load(head_up_path).convert_alpha()
    self.head_down = pygame.image.load(head_down_path).convert_alpha()
    self.head_right = pygame.image.load(head_right_path).convert_alpha()
    self.head_left = pygame.image.load(head_left_path).convert_alpha()
    # caudas
    self.tail_up = pygame.image.load(tail_up_path).convert_alpha()
    self.tail_down = pygame.image.load(tail_down_path).convert_alpha()
    self.tail_right = pygame.image.load(tail_right_path).convert_alpha()
    self.tail_left = pygame.image.load(tail_left_path).convert_alpha()
    # corpo
    self.body_vertical = pygame.image.load(body_vertical_path).convert_alpha()
    self.body_horizontal = pygame.image.load(body_horizontal_path).convert_alpha()
    self.body_tr = pygame.image.load(body_tr_path).convert_alpha()
    self.body_tl = pygame.image.load(body_tl_path).convert_alpha()
    self.body_br = pygame.image.load(body_br_path).convert_alpha()
    self.body_bl = pygame.image.load(body_bl_path).convert_alpha()
    self.crunch_sound = crunch_sound

  def draw(self):
    self.update_head()
    self.update_tail()
    for index, block in enumerate(self.body):
      x_pos = int(block.x * CELL_SIZE)
      y_pos = int(block.y * CELL_SIZE)
      block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)
      if index == 0:
        screen.blit(self.head, block_rect)
      elif index == len(self.body) - 1:
        screen.blit(self.tail, block_rect)
      else:
        prev_block = self.body[index + 1] - block
        next_block = self.body[index - 1] - block
        if prev_block.x == next_block.x:
          screen.blit(self.body_vertical, block_rect)
        elif prev_block.y == next_block.y:
          screen.blit(self.body_horizontal, block_rect)
        else:
          if (prev_block.x == -1 and next_block.y == -1) or (prev_block.y == -1 and next_block.x == -1):
            screen.blit(self.body_tl, block_rect)
          elif (prev_block.x == -1 and next_block.y == 1) or (prev_block.y == 1 and next_block.x == -1):
            screen.blit(self.body_bl, block_rect)
          elif (prev_block.x == 1 and next_block.y == -1) or (prev_block.y == -1 and next_block.x == 1):
            screen.blit(self.body_tr, block_rect)
          elif (prev_block.x == 1 and next_block.y == 1) or (prev_block.y == 1 and next_block.x == 1):
            screen.blit(self.body_br, block_rect)

  def update_head(self):
    head_relation = self.body[1] - self.body[0]
    if head_relation == Vector2(1, 0):
      self.head = self.head_left
    elif head_relation == Vector2(-1, 0):
      self.head = self.head_right
    elif head_relation == Vector2(0, 1):
      self.head = self.head_up
    elif head_relation == Vector2(0, -1):
      self.head = self.head_down

  def update_tail(self):
    tail_relation = self.body[-2] - self.body[-1]
    if tail_relation == Vector2(1, 0):
      self.tail = self.tail_left
    elif tail_relation == Vector2(-1, 0):
      self.tail = self.tail_right
    elif tail_relation == Vector2(0, 1):
      self.tail = self.tail_up
    elif tail_relation == Vector2(0, -1):
      self.tail = self.tail_down

  def move(self):
    body_copy = self.body[:]
    if self.new_block:
      body_copy.insert(0, body_copy[0] + self.direction)
      self.body = body_copy[:]
      self.new_block = False
    else:
      body_copy = self.body[:-1]
      body_copy.insert(0, body_copy[0] + self.direction)
      self.body = body_copy[:]

  def grow(self):
    self.new_block = True

  def play_crunch(self):
    self.crunch_sound.play()


class FRUIT:
  def __init__(self):
    self.randomize()

  def draw(self):
    rect = pygame.Rect(int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
    screen.blit(apple, rect)

  def randomize(self):
    self.pos = Vector2(random.randint(0, CELL_NUMBER_X - 1), random.randint(0, CELL_NUMBER_Y - 1))


class MAIN:
  def __init__(self):
    self.snake = SNAKE()
    self.fruit = FRUIT()
    self.level = 1
    self.score = 0
    self.level_up_counter = 0

  def update(self):
    self.snake.move()
    self.check_collision()
    if not (0 <= self.snake.body[0].x < CELL_NUMBER_X and 0 <= self.snake.body[0].y < CELL_NUMBER_Y):
      raise Exception("Game Over")
    for block in self.snake.body[1:]:
      if self.snake.body[0] == block:
        raise Exception("Game Over")

  def check_collision(self):
    if self.fruit.pos == self.snake.body[0]:
      self.fruit.randomize()
      self.snake.grow()
      self.snake.play_crunch()
      self.score += 1
      self.level_up_counter += 1
      if self.level_up_counter >= 5:
        self.level += 1
        self.level_up_counter = 0

  def draw(self):
    screen.fill(LIGHT_GRASS)
    for row in range(CELL_NUMBER_Y):
      for col in range(CELL_NUMBER_X):
        if (row + col) % 2 == 0:
          pygame.draw.rect(screen, GRASS, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    self.fruit.draw()
    self.snake.draw()
    apple_rect = apple.get_rect()
    apple_rect.bottomright = (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 10)
    screen.blit(apple, apple_rect)
    apple_text = game_font.render(str(self.score), True, WHITE)
    screen.blit(apple_text, (apple_rect.right + 10, apple_rect.top - 5))


# ---------------- MENU VISUAL ----------------
def menu_screen():
  options = ["Play", "Options", "Exit"]
  selected = 0
  while True:
    screen.fill(BG)
    mx, my = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]

    # fundo menu estilizado
    pygame.draw.rect(screen, (50, 50, 80), (50, 50, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100), border_radius=30)
    draw_text(screen, "Snakorn", (SCREEN_WIDTH // 2, 120), 90, ACCENT, True, True)

    # botões
    for i, o in enumerate(options):
      rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 250 + i * 100, 300, 70)
      color = BUTTON_HOVER if rect.collidepoint(mx, my) else ACCENT
      pygame.draw.rect(screen, color, rect, border_radius=20)
      draw_text(screen, o, rect.center, 45, WHITE)

      if rect.collidepoint(mx, my) and click:
        if o == "Play": return
        if o == "Options": options_screen()
        if o == "Exit": pygame.quit(); sys.exit()

    draw_text(screen, f"Highscore: {HS.get('highscore', 0)}", (SCREEN_WIDTH - 182, 80), 25, YELLOW)
    for e in pygame.event.get():
      if e.type == pygame.QUIT: pygame.quit(); sys.exit()
    pygame.display.flip()
    clock.tick(60)


# ---------------- OPTIONS ----------------
def options_screen():
  global difficulty_speed
  opts = ["Easy", "Normal", "Hard"]
  speeds = [5, 10, 15]
  selected = 1
  while True:
    screen.fill(BG)
    mx, my = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]
    draw_text(screen, "difficulty", (SCREEN_WIDTH // 2, 80), 70, ACCENT)
    for i, o in enumerate(opts):
      rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 180 + i * 80, 300, 60)
      color = BUTTON_HOVER if rect.collidepoint(mx, my) else ACCENT
      pygame.draw.rect(screen, color, rect, border_radius=15)
      draw_text(screen, o, rect.center, 35, WHITE)
      if rect.collidepoint(mx, my) and click:
        difficulty_speed = speeds[i]
    for e in pygame.event.get():
      if e.type == pygame.QUIT: pygame.quit(); sys.exit()
      if e.type == pygame.KEYDOWN:
        if e.key == pygame.K_ESCAPE: return
    pygame.display.flip()
    clock.tick(30)


# ---------------- SPLASH ----------------
def splash_screen():
  t = 0
  while t <= 100:
    screen.fill(BG)
    draw_text(screen, "Mixbit Studios©", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 50, WHITE)
    pygame.display.flip()
    t += 2
    clock.tick(60)


# ---------------- GAME LOOP ----------------
def run_game():
  game = MAIN()
  speed = difficulty_speed
  while True:
    try:
      for e in pygame.event.get():
        if e.type == pygame.QUIT: pygame.quit(); sys.exit()
        if e.type == pygame.KEYDOWN:
          if e.key in (pygame.K_UP, pygame.K_w) and game.snake.direction.y != 1: game.snake.direction = Vector2(0, -1)
          if e.key in (pygame.K_DOWN, pygame.K_s) and game.snake.direction.y != -1: game.snake.direction = Vector2(0, 1)
          if e.key in (pygame.K_LEFT, pygame.K_a) and game.snake.direction.x != 1: game.snake.direction = Vector2(-1, 0)
          if e.key in (pygame.K_RIGHT, pygame.K_d) and game.snake.direction.x != -1: game.snake.direction = Vector2(1,
                                                                                                                    0)
          if e.key == pygame.K_ESCAPE: pause_screen()
      game.update()
      game.draw()
      pygame.display.flip()
      clock.tick(speed)
    except:
      score = game.score
      again = game_over_screen(score)
      if again:
        return run_game()
      else:
        return


# ---------------- PAUSE ----------------
def pause_screen():
  overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
  overlay.fill((0, 0, 0, 150))
  screen.blit(overlay, (0, 0))
  draw_text(screen, "Game paused", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 60, WHITE)
  draw_text(screen, "Press ESC to continue the game.", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60), 30, WHITE)
  pygame.display.flip()
  waiting = True
  while waiting:
    for e in pygame.event.get():
      if e.type == pygame.QUIT: pygame.quit(); sys.exit()
      if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE: waiting = False
    clock.tick(10)


# ---------------- GAME OVER ----------------
def game_over_screen(score):
  if score > HS.get("highscore", 0):
    HS["highscore"] = score
    save_highscores()
  while True:
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    draw_text(screen, "GAME OVER", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100), 80, RED)
    draw_text(screen, f"Points: {score}", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 50, WHITE)
    draw_text(screen, f"Highscore: {HS.get('highscore', 0)}", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60), 40, YELLOW)
    draw_text(screen, "R to restart / ESC returns to menu", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 140), 30, WHITE)
    pygame.display.flip()
    for e in pygame.event.get():
      if e.type == pygame.QUIT: pygame.quit(); sys.exit()
      if e.type == pygame.KEYDOWN:
        if e.key == pygame.K_r: return True
        if e.key == pygame.K_ESCAPE: return False
    clock.tick(30)


# ---------------- MAIN ----------------
def main():
  splash_screen()
  while True:
    menu_screen()
    run_game()


if __name__ == "__main__":
  main()
