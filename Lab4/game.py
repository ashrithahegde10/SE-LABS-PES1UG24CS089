import pygame
import random
import math
import time

WIDTH, HEIGHT = 800, 560
FPS = 60
BG = (30,35,25)


class Zombie:
    """Standard zombie. Subclasses only override the stat constants below."""
    SPEED = 1.5
    HP = 3
    SIZE = 30
    COLOR = (60,140,60)

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, self.SIZE, self.SIZE)
        self.pos = [float(x), float(y)]   # float position so speeds below 1 px/frame still move
        self.color = self.COLOR
        self.hp = self.HP
        self.wobble = random.uniform(0, 6.28)
        self.frame = 0

    def update(self, player_pos):
        px, py = player_pos
        cx, cy = self.rect.center
        dx, dy = px-cx, py-cy
        dist = (dx**2+dy**2)**0.5
        if dist:
            self.pos[0] += dx/dist*self.SPEED
            self.pos[1] += dy/dist*self.SPEED
            self.rect.x = round(self.pos[0])
            self.rect.y = round(self.pos[1])
        self.frame += 1

    def hit(self):
        self.hp -= 1
        return self.hp <= 0

    def draw(self, screen):
        wobble_y = int(math.sin(self.frame*0.2)*3)
        draw_rect = self.rect.move(0, wobble_y)
        pygame.draw.rect(screen, self.color, draw_rect, border_radius=5)
        eye_r = max(2, self.SIZE // 8)
        for ex in [draw_rect.x + self.SIZE//5, draw_rect.x + self.SIZE*3//5]:
            pygame.draw.circle(screen, (200,40,40), (ex, draw_rect.y + self.SIZE//3), eye_r)
        if self.hp < self.HP:   # health bar once damaged
            bar = pygame.Rect(draw_rect.x, draw_rect.y-7, self.SIZE, 4)
            pygame.draw.rect(screen, (90,20,20), bar)
            pygame.draw.rect(screen, (220,60,60),
                             (bar.x, bar.y, int(bar.width*self.hp/self.HP), bar.height))


class FastZombie(Zombie):      # Task 4: fast, fragile, small
    SPEED = 2.8
    HP = 1
    SIZE = 20
    COLOR = (200,200,60)


class TankZombie(Zombie):      # Task 4: slow, durable, large
    SPEED = 0.8
    HP = 6
    SIZE = 44
    COLOR = (40,90,70)


# Task 4: spawn mix (standard, fast, tank)
ZOMBIE_TYPES = [Zombie, FastZombie, TankZombie]
ZOMBIE_WEIGHTS = [0.5, 0.3, 0.2]

# Wave top-up spawning: keeps zombies coming so a wave's kill target is reachable
SPAWN_INTERVAL = 90      # frames between top-up spawns
MAX_ALIVE_BASE = 4       # alive cap = MAX_ALIVE_BASE + wave

# Task 3: barrels
BARREL_COUNT = 4
EXPLOSION_RADIUS = 110


def spawn_zombie(width, height, player_rect, margin=120, cls=None):
    if cls is None:
        cls = random.choices(ZOMBIE_TYPES, ZOMBIE_WEIGHTS)[0]
    while True:
        x = random.randint(0, width-cls.SIZE)
        y = random.randint(0, height-cls.SIZE)
        rect = pygame.Rect(x, y, cls.SIZE, cls.SIZE)
        if not rect.colliderect(player_rect.inflate(margin, margin)):
            return cls(x, y)


SPEED = 4

# Task 1: health
MAX_HP = 3
INVINCIBLE_MS = 1500   # invincibility window after each hit

# Task 2: ammo
CLIP_SIZE = 12
RELOAD_MS = 2000       # reload duration


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.color = (60,160,220)
        self.bullets = []
        self.shoot_cooldown = 0
        # Task 1: health
        self.hp = MAX_HP
        self.invincible_until = 0   # time (ms) when invincibility ends
        # Task 2: ammo
        self.ammo = CLIP_SIZE
        self.reloading = False
        self.reload_until = 0       # time (ms) when reload finishes

    def move(self, keys, width, height):
        dx = dy = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]: dy = -SPEED
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: dy = SPEED
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: dx = -SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: dx = SPEED
        self.rect.x = max(0, min(width-self.rect.width, self.rect.x+dx))
        self.rect.y = max(0, min(height-self.rect.height, self.rect.y+dy))
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def shoot(self, target_pos):
        if self.shoot_cooldown > 0: return
        if self.reloading: return
        if self.ammo <= 0:
            self.start_reload()
            return
        cx, cy = self.rect.center
        tx, ty = target_pos
        dx, dy = tx-cx, ty-cy
        dist = (dx**2+dy**2)**0.5
        if dist == 0: return
        vx, vy = dx/dist*10, dy/dist*10
        self.bullets.append(pygame.Rect(cx-4, cy-4, 8, 8))
        self.bullets.append([cx-4, cy-4, vx, vy])
        self.bullets.pop(-2)
        self.shoot_cooldown = 15
        self.ammo -= 1
        if self.ammo == 0:
            self.start_reload()

    def update_bullets(self, width, height):
        live = []
        for b in self.bullets:
            b[0] += b[2]; b[1] += b[3]
            if 0 <= b[0] <= width and 0 <= b[1] <= height:
                live.append(b)
        self.bullets = live

    # ---- Task 1: health ----
    def is_invincible(self):
        return pygame.time.get_ticks() < self.invincible_until

    def take_hit(self):
        """Lose 1 HP unless invincible. Returns True if damage was applied."""
        if self.is_invincible():
            return False
        self.hp -= 1
        self.invincible_until = pygame.time.get_ticks() + INVINCIBLE_MS
        return True

    # ---- Task 2: ammo / reload ----
    def start_reload(self):
        if self.reloading:
            return
        self.reloading = True
        self.reload_until = pygame.time.get_ticks() + RELOAD_MS

    def update_reload(self):
        if self.reloading and pygame.time.get_ticks() >= self.reload_until:
            self.ammo = CLIP_SIZE
            self.reloading = False

    def reload_remaining(self):
        return max(0, self.reload_until - pygame.time.get_ticks()) / 1000

    def draw(self, screen):
        # flash white every 100 ms while invincible so the window is visible
        flash = self.is_invincible() and (pygame.time.get_ticks() // 100) % 2 == 0
        pygame.draw.rect(screen, (255,255,255) if flash else self.color,
                         self.rect, border_radius=6)
        for b in self.bullets:
            pygame.draw.circle(screen, (255,220,60), (int(b[0]), int(b[1])), 5)


class Barrel:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 28, 36)

    def draw(self, screen):
        pygame.draw.rect(screen, (190,60,30), self.rect, border_radius=5)
        for yy in (self.rect.y+9, self.rect.y+26):
            pygame.draw.line(screen, (110,30,15), (self.rect.x, yy), (self.rect.right-1, yy), 3)
        pygame.draw.rect(screen, (240,200,40), (self.rect.centerx-3, self.rect.y+14, 6, 8))


def place_barrels(count, width, height, avoid_rect):
    barrels = []
    while len(barrels) < count:
        b = Barrel(random.randint(20, width-60), random.randint(80, height-60))
        if b.rect.colliderect(avoid_rect.inflate(160, 160)): continue
        if any(b.rect.colliderect(o.rect.inflate(60, 60)) for o in barrels): continue
        barrels.append(b)
    return barrels


class Explosion:
    DURATION = 400   # ms

    def __init__(self, pos, radius):
        self.pos, self.radius = pos, radius
        self.start = pygame.time.get_ticks()

    def alive(self):
        return pygame.time.get_ticks() - self.start < self.DURATION

    def draw(self, screen):
        t = (pygame.time.get_ticks() - self.start) / self.DURATION
        if t >= 1: return
        r = max(1, int(self.radius * (0.3 + 0.7*t)))   # grows out to the real blast radius
        alpha = int(200 * (1 - t))
        surf = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (255,140,30,alpha), (self.radius, self.radius), r)
        pygame.draw.circle(surf, (255,230,120,alpha), (self.radius, self.radius), int(r*0.6))
        screen.blit(surf, (self.pos[0]-self.radius, self.pos[1]-self.radius))


class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Zombie Escape")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 24)
        self.big_font = pygame.font.SysFont("monospace", 44, bold=True)
        self.hud_font = pygame.font.SysFont("monospace", 20)
        self.hint_font = pygame.font.SysFont("monospace", 16)
        pygame.mouse.set_visible(False)   # we draw our own crosshair
        self.reset()

    def reset(self):
        self.player = Player(WIDTH//2, HEIGHT//2)
        # first four are fixed (one of each type shows up immediately); later spawns are random
        self.zombies = [spawn_zombie(WIDTH, HEIGHT, self.player.rect, cls=c)
                        for c in (Zombie, FastZombie, TankZombie, Zombie)]
        self.barrels = place_barrels(BARREL_COUNT, WIDTH, HEIGHT, self.player.rect)
        self.explosions = []
        self.spawn_timer = 0
        self.score = 0
        self.bonus = 0   # points from kills, kept separate so the timer doesn't overwrite it
        self.wave = 1
        self.kills = 0
        self.kills_to_next = 8
        self.game_over = False
        self.start_time = time.time()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r: self.reset()
            if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                self.player.shoot(event.pos)
        return True

    def update(self):
        if self.game_over: return
        keys = pygame.key.get_pressed()
        self.player.move(keys, WIDTH, HEIGHT)
        self.player.update_bullets(WIDTH, HEIGHT)
        self.player.update_reload()
        self.score = int(time.time() - self.start_time) + self.bonus

        for z in self.zombies:
            z.update(self.player.rect.center)
            if z.rect.colliderect(self.player.rect):
                if self.player.take_hit() and self.player.hp <= 0:
                    self.game_over = True

        dead = []
        for z in self.zombies:
            for b in self.player.bullets[:]:
                bx, by = int(b[0]), int(b[1])
                if z.rect.collidepoint(bx, by):
                    if z.hit():
                        dead.append(z)
                    if b in self.player.bullets:
                        self.player.bullets.remove(b)
        # Task 3: bullet hits barrel -> explosion kills zombies within radius
        for barrel in self.barrels[:]:
            for b in self.player.bullets[:]:
                if barrel.rect.collidepoint(int(b[0]), int(b[1])):
                    self.player.bullets.remove(b)
                    center = barrel.rect.center
                    self.explosions.append(Explosion(center, EXPLOSION_RADIUS))
                    for z in self.zombies:
                        zx, zy = z.rect.center
                        if (zx-center[0])**2 + (zy-center[1])**2 <= EXPLOSION_RADIUS**2:
                            dead.append(z)   # goes through the normal kill/score handling below
                    self.barrels.remove(barrel)
                    break

        for z in dead:
            if z in self.zombies:
                self.zombies.remove(z)
                self.kills += 1
                self.bonus += 10

        if self.kills >= self.kills_to_next:
            self.kills = 0
            self.wave += 1
            self.kills_to_next = 8 + self.wave * 2
            for _ in range(self.wave + 3):
                self.zombies.append(spawn_zombie(WIDTH, HEIGHT, self.player.rect))

        # top-up spawning: without this only the initial zombies ever exist
        self.explosions = [e for e in self.explosions if e.alive()]
        self.spawn_timer += 1
        if self.spawn_timer >= SPAWN_INTERVAL and len(self.zombies) < MAX_ALIVE_BASE + self.wave:
            self.zombies.append(spawn_zombie(WIDTH, HEIGHT, self.player.rect))
            self.spawn_timer = 0

    def draw_crosshair(self):
        mx, my = pygame.mouse.get_pos()
        col = (150,150,150) if self.player.reloading else (255,220,60)
        pygame.draw.circle(self.screen, col, (mx, my), 9, 2)
        pygame.draw.line(self.screen, col, (mx-14, my), (mx+14, my), 2)
        pygame.draw.line(self.screen, col, (mx, my-14), (mx, my+14), 2)

    def draw(self):
        self.screen.fill(BG)
        for x in range(0, WIDTH, 60):
            pygame.draw.line(self.screen, (40,45,35), (x,0), (x,HEIGHT), 1)
        for y in range(0, HEIGHT, 60):
            pygame.draw.line(self.screen, (40,45,35), (0,y), (WIDTH,y), 1)
        for barrel in self.barrels: barrel.draw(self.screen)
        for z in self.zombies: z.draw(self.screen)
        for e in self.explosions: e.draw(self.screen)
        self.player.draw(self.screen)
        self.draw_crosshair()
        hud_bg = pygame.Rect(0, 0, WIDTH, 50)
        pygame.draw.rect(self.screen, (15,20,15), hud_bg)
        p = self.player
        ammo_txt = f"RELOAD {p.reload_remaining():.1f}s" if p.reloading else f"{p.ammo}/{CLIP_SIZE}"
        hud = self.hud_font.render(
            f"Wave: {self.wave}  Score: {self.score}  Kills: {self.kills}/{self.kills_to_next}  HP: {p.hp}/{MAX_HP}  Ammo: {ammo_txt}",
            True, (220,90,90) if p.hp == 1 else (160,220,120))
        self.screen.blit(hud, (8, 6))
        hint = self.hint_font.render("WASD Move, Click Shoot, R Restart", True, (110,150,90))
        self.screen.blit(hint, (8, 30))
        if self.game_over:
            ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            ov.fill((0,0,0,160))
            self.screen.blit(ov, (0,0))
            m = self.big_font.render("DEVOURED!", True, (180,40,40))
            s = self.font.render(f"Wave {self.wave} | Score {self.score} | Press R", True, (200,200,200))
            self.screen.blit(m, (WIDTH//2-m.get_width()//2, HEIGHT//2-40))
            self.screen.blit(s, (WIDTH//2-s.get_width()//2, HEIGHT//2+20))
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()


if __name__ == "__main__":
    engine = GameEngine()
    engine.run()