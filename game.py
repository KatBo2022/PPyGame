class Board:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_cell(self, mouse_pos):
        x = mouse_pos[0] - self.left
        y = mouse_pos[1] - self.top
        if x < 0 or y < 0:
            return None
        x //= self.cell_size
        y //= self.cell_size
        if x < self.width and y < self.height:
            return x, y
        return None

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def on_click(self, cell_coords):
        if cell_coords is None:
            return
        x, y = cell_coords
        self.board[y][x] += 1
        self.board[y][x] %= 3

    def render(self, screen):
        clr = ((0, 0, 0), (255, 0, 0), (0, 0, 255))
        screen.fill((255, 255, 255), (self.left, self.top, self.width *
                                      self.cell_size, self.height * self.cell_size))
        i = 0
        for y in range(self.top + 1, self.height * self.cell_size, self.cell_size):
            j = 0
            for x in range(self.left + 1, self.width * self.cell_size,
                           self.cell_size):
                screen.fill(clr[self.board[i][j]], (x, y, self.cell_size - 2,
                                                    self.cell_size - 2))
                j += 1
            i += 1


if __name__ == '__main__':

    import pygame

    pygame.init()
    pygame.display.set_caption('Реакция на события от мыши')
    size = width, height = 300, 400
    screen = pygame.display.set_mode(size)

    running = True
    fps = 30
    clock = pygame.time.Clock()
    board = Board(5, 7)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        screen.fill((0, 0, 0))
        board.render(screen)
        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()


