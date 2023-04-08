import pymunk, \
    pymunk.pygame_util, \
    pygame, \
    random, \
    math, time

shapes = {
    "o": lambda size: [[(-size, -size), (-size, size), (size, size), (size, -size)]],
    "i": lambda size: [[(-size/2, size*1.5), (size/2, size*1.5), (size/2, -size*1.5), (-size/2, -size*1.5)]],
    "l": lambda size: [[(0, size*1.5), (-size, size*1.5), (-size, -size*1.5), (0, -size*1.5)], [(0, -size/2), (0, -size*1.5), (size, -size*1.5), (size, -size/2)]],
    "lr": lambda size: [[(0, size*1.5), (size, size*1.5), (size, -size*1.5), (0, -size*1.5)], [(0, -size/2), (0, -size*1.5), (-size, -size*1.5), (-size, -size/2)]],
    "z": lambda size: [[(-size/2, 0), (-size/2, size), (size*1.5, size), (size*1.5, 0)], [(-size*1.5, 0), (size/2, 0), (size/2, -size), (-size*1.5, -size)]],
    "zr": lambda size: [[(-size*1.5, 0), (-size*1.5, size), (size/2, size), (size/2, 0)], [(-size/2, 0), (-size/2, -size), (size*1.5, -size), (size*1.5, 0)]],
    "t": lambda size: [[(-size/2, -size), (size/2, -size), (size/2, 0), (-size/2, 0)], [(-size*1.5, 0), (size*1.5, 0), (size*1.5, size), (-size*1.5, size)]]
}


def rotateVector(vector, angle):
    X = vector[0] * math.cos(-angle) - vector[1] * math.sin(-angle)
    Y = vector[0] * math.sin(-angle) + vector[1] * math.cos(-angle)
    return X, Y
def replaceBlock(space, body:pymunk.Body):
    momentum = body.moment
    b = pymunk.Body(body.mass, momentum, body.STATIC)
    shapes = []
    for x in body.points:
        shape = pymunk.Poly(body, x)
        shape.friction = 9999
        shape.elasticity = 0
        shapes.append(shape)
    b._set_angle(body.angle)
    b._set_center_of_gravity(body.center_of_gravity)

    body._set_position((-10000, 1000))
    space.add(b, *shapes)


class Screen:
    def __init__(self) -> None:

        self.clock = pygame.time.Clock()

        self.win = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("TetrisAlt")
        self.physics = None
        self.activeTile = 0
    
    def update(self):
        self.clock.tick(100)
        pygame.display.update()
        self.win.fill((255, 255, 255))

    def events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    # replaceBlock(self.physics.space, self.physics.space.bodies[self.activeTile])
                    size = random.randint(20, 50)
                    makeBlock(physics.space, shapes[random.choice(["o", "i", "l", "lr", "z", "zr", "t"])](size), size*2, (300, 600))
                    self.activeTile = len(self.physics.space.bodies) - 1
        pressed = pygame.key.get_pressed()

        if self.physics.space.bodies[self.activeTile].angular_velocity > 0:
            self.physics.space.bodies[self.activeTile].angular_velocity -= .05
        elif self.physics.space.bodies[self.activeTile].angular_velocity < 0:
            self.physics.space.bodies[self.activeTile].angular_velocity += .05
        
        angle = self.physics.space.bodies[self.activeTile].angle
    
        if pressed[pygame.K_LEFT]:
            self.physics.space.bodies[self.activeTile].apply_impulse_at_local_point(rotateVector((-500, 0), angle), (0, 0))
        if pressed[pygame.K_RIGHT]:
            self.physics.space.bodies[self.activeTile].apply_impulse_at_local_point(rotateVector((500, 0), angle), (0, 0))
        if pressed[pygame.K_UP]:
            self.physics.space.bodies[self.activeTile].angular_velocity = 5
        if pressed[pygame.K_DOWN]:
            self.physics.space.bodies[self.activeTile].angular_velocity = -5



class Physics:
    def __init__(self, screen):
        self.space = pymunk.Space()
        self.space.gravity = 0, -1000
        self.space.sleep_time_threshold = 0.05

        self.screen = screen

        pymunk.pygame_util.positive_y_is_up = True
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen.win)

        shape = pymunk.Segment(self.space.static_body, (200, 10), (400, 10), 1.0)
        shape.friction = 9999
        self.space.add(shape)

    def update(self):
        self.space.step(0.01)
    
    def draw(self):
        self.space.debug_draw(self.draw_options)

def makeBlock(space, points, mass, pos):
    momentum = pymunk.moment_for_poly(mass, points[0])

    body = pymunk.Body(mass, momentum)
    body.position = pos
    body.points = points

    shapes = []

    for x in points:
        shape = pymunk.Poly(body, x)
        shape.friction = 9999
        shape.elasticity = 0
        shapes.append(shape)

    space.add(body, *shapes)

screen = Screen()
physics = Physics(screen)
screen.physics = physics
size = random.randint(20, 50)
makeBlock(physics.space, shapes[random.choice(["o", "i", "l", "lr", "z", "zr", "t"])](size), size*2, (300, 600))


while True:
    screen.events()
    physics.update()
    physics.draw()
    screen.update()
