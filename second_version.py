import random, pygame, math, time


class Maze:
    def __init__(
        self,
        min_solution_length,
        wall_possibility,
        maze_size,
        start,
        player_start_coord,
    ):
        self.size = maze_size
        self.wall_possibility = wall_possibility
        self.walls = []
        self.test_walls = []
        self.num_vertex = 1
        self.vertex_coord = []
        self.edge_list = []
        self.graphs = []
        self.start = start
        self.finish = 0
        self.min_solution_length = min_solution_length
        self.test_solution_length = 0
        self.test_solution_path = []
        self.solution_length = 0
        self.solution_path = []
        self.create_flag = False
        self.player_coord = player_start_coord
        self.player_cell = (
            1 + self.player_coord[1] * self.size[0] + self.player_coord[0]
        )
        self.steps = 0
        self.weights = []
        self.amt_points = 0

    def get_random_walls(self):
        self.test_walls = []
        c = []
        for i in range(self.wall_possibility[0] * self.size[0] + 1):
            c.append(0)
        for i in range(self.wall_possibility[1] * self.size[1] + 1):
            c.append(1)
        self.test_walls.append(
            list(random.sample(c, self.size[0] + 1) for _ in range(self.size[1] + 1))
        )
        self.test_walls.append(
            list(random.sample(c, self.size[0] + 1) for _ in range(self.size[1] + 1))
        )
        for i in range(self.size[0] + 1):
            self.test_walls[0][0][self.size[0] - i] = 1
            self.test_walls[0][self.size[1]][self.size[0] - i] = 1
        for i in range(self.size[1] + 1):
            self.test_walls[0][i][self.size[0]] = 0
        for i in range(self.size[1] + 1):
            self.test_walls[1][i][0] = 1
            self.test_walls[1][i][self.size[0]] = 1
        for i in range(self.size[0] + 1):
            self.test_walls[1][0][i] = 0

    def print(self):
        for i in range(self.size[1] + 1):
            line = ""
            for j in range(self.size[0] + 1):
                if self.test_walls[1][i][j]:
                    line += "|"
                else:
                    line += " "
                if self.test_walls[0][i][j]:
                    line += "__"
                else:
                    line += "  "
            print(line)

    def cell2coord(self, num_vertex):
        vertex_coord = []
        vertex_coord.append((num_vertex - 1) // self.size[0])
        vertex_coord.append((num_vertex - 1) % self.size[0])
        return vertex_coord

    def coord2cell(self, coord):
        cell = 1 + coord[1] * self.size[0] + coord[0]
        return cell

    def get_edge_list(self):
        self.vertex_coord = self.cell2coord(self.num_vertex)
        self.edge_list = []

        for i in range(self.vertex_coord[1], self.size[0]):
            if self.test_walls[1][self.vertex_coord[0] + 1][i + 1]:
                num = self.size[0] * self.vertex_coord[0] + i + 1
                if num != self.num_vertex:
                    self.edge_list.append(num)
                break
        for i in range(self.vertex_coord[1], -1, -1):
            if self.test_walls[1][self.vertex_coord[0] + 1][i]:
                num = self.size[0] * self.vertex_coord[0] + i + 1
                if num != self.num_vertex:
                    self.edge_list.append(num)
                break
        for i in range(self.vertex_coord[0], self.size[1]):
            if self.test_walls[0][i + 1][self.vertex_coord[1]]:
                num = self.size[0] * i + self.vertex_coord[1] + 1
                if num != self.num_vertex:
                    self.edge_list.append(num)
                break
        for i in range(self.vertex_coord[0], -1, -1):
            if self.test_walls[0][i][self.vertex_coord[1]]:
                num = self.size[0] * i + self.vertex_coord[1] + 1
                if num != self.num_vertex:
                    self.edge_list.append(num)
                break

        self.edge_list.sort()

    def get_path(self):
        n = self.size[0] * self.size[1]
        D = [None] * (n + 1)
        D[self.start] = 0
        Q = [self.start]
        Qstart = 0
        Prev = [None] * (n + 1)

        while Qstart < len(Q):
            u = Q[Qstart]
            Qstart += 1
            for v in self.graphs[u - 1]:
                if D[v] is None:
                    D[v] = D[u] + 1
                    Q.append(v)
                    Prev[v] = u

        self.amt_points = 0
        self.test_solution_length = 0
        self.test_solution_path = []

        for i in range(n + 1):
            Ans = []
            curr = i
            while curr is not None:
                Ans.append(curr)
                curr = Prev[curr]

            if D[i]:
                self.amt_points += 1
                if self.test_solution_length < D[i]:
                    self.test_solution_length = D[i]
                    self.test_solution_path = Ans[::-1]
                    self.finish = i

    def try_to_create(self):
        self.create_flag = False
        self.graphs = []
        self.get_random_walls()
        for i in range(self.size[0] * self.size[1]):
            self.num_vertex = i + 1
            self.get_edge_list()
            self.graphs.append(self.edge_list)
        self.get_path()
        if self.test_solution_length > 15 and self.amt_points > 20:
            self.walls = self.test_walls.copy()
            self.solution_length = self.test_solution_length
            self.solution_path = self.test_solution_path.copy()
            self.create_flag = True
            print(self.cell2coord(self.finish))

    def draw(self, color, coord, size, width_wall):
        size_x = size[0] / self.size[0]
        size_y = size[1] / self.size[1]
        for i in range(self.size[1] + 1):
            for j in range(self.size[0] + 1):
                if j + 1 < len(self.walls[0][i]):
                    if self.walls[0][i][j]:
                        pygame.draw.line(
                            screen,
                            color,
                            (int(j * size_x + coord[0]), int(i * size_y + coord[1])),
                            (
                                int((j + 1) * size_x + coord[0]),
                                int(i * size_y + coord[1]),
                            ),
                            width_wall,
                        )
                if i + 1 < len(self.walls[1]):
                    if self.walls[1][i + 1][j]:
                        pygame.draw.line(
                            screen,
                            color,
                            (int(j * size_x + coord[0]), int(i * size_y + coord[1])),
                            (
                                int(j * size_x + coord[0]),
                                int((i + 1) * size_y + coord[1]),
                            ),
                            width_wall,
                        )

        crd = self.cell2coord(self.start)
        crd[0], crd[1] = crd[1], crd[0]
        crd[0] *= size_x
        crd[1] *= size_y
        pygame.draw.rect(
            screen, (0, 230, 0), (crd[0] + 10, crd[1] + 10, size_x - 15, size_y - 15)
        )
        pygame.draw.rect(
            screen, (0, 0, 0), (crd[0] + 10, crd[1] + 10, size_x - 15, size_y - 15), 5
        )

        crd = self.cell2coord(self.finish)
        crd[0], crd[1] = crd[1], crd[0]
        crd[0] *= size_x
        crd[1] *= size_y
        pygame.draw.rect(
            screen, (230, 0, 0), (crd[0] + 10, crd[1] + 10, size_x - 15, size_y - 15)
        )
        pygame.draw.rect(
            screen, (0, 0, 0), (crd[0] + 10, crd[1] + 10, size_x - 15, size_y - 15), 5
        )


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    size_screen = [325, 645]
    color_screen = (230, 230, 230)
    screen = pygame.display.set_mode(size_screen)

    clock = pygame.time.Clock()
    FPS = 50

    keydown = []

    maze = Maze(20, [10, 1], [8, 16], 1, [2, 2])

    step = 1
    TMP_i = 0
    while step:
        if step == 1:
            maze.try_to_create()
            if maze.create_flag:
                maze.print()
                print(TMP_i, maze.solution_length)
                TMP_i = 0
                step = 2
            else:
                TMP_i += 1

        if step == 2:
            screen.fill(color_screen)
            maze.draw((0, 0, 0), [2, 2], [320, 640], 5)
            if pygame.K_BACKSPACE in keydown:
                flag = True
                while flag:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYUP:
                            keydown.remove(event.key)
                            if event.key == pygame.K_BACKSPACE:
                                flag = False
                                break
                maze.start = maze.finish
                step = 1
            pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                step = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    step = 0
                keydown.append(event.key)
            if event.type == pygame.KEYUP:
                keydown.remove(event.key)

        clock.tick()

    pygame.quit()
