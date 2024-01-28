import random, pygame, time
from game_windows.end_window import start_final_window


def start_the_game():
    class Maze:
        def __init__(
            self,
            min_solution_length,
            wall_possibility,  # дробь отношения (например 10 к 1): 1 - что стенка есть, 10 - что нет.
            maze_size,  # размер окна в клетках
            start,  # первая координата в списке
            player_start_coord,  # где начинает игрок
        ):
            self.size = maze_size
            self.wall_possibility = wall_possibility
            self.walls = []  # 100% правильные уже отрисованные стенки лабиринта
            self.test_walls = (
                []
            )  # не факт что правильные стенки. Используется при генерации self.walls
            self.num_vertex = 1  # номер вершины
            self.vertex_coord = []  # не номер, а координата
            self.edge_list = []  # список смежностей (куда мы можем попасть из клетки)
            self.graphs = []
            self.start = start
            self.finish = 0
            self.min_solution_length = min_solution_length
            self.test_solution_length = 0
            self.test_solution_path = []
            self.solution_length = 0
            self.solution_path = []
            self.create_flag = False
            self.player_coord = (
                player_start_coord  # player не отрисовывается, поэтому ничего нет
            )
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
                list(
                    random.sample(c, self.size[0] + 1) for _ in range(self.size[1] + 1)
                )
            )
            self.test_walls.append(
                list(
                    random.sample(c, self.size[0] + 1) for _ in range(self.size[1] + 1)
                )
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
            # вычисляем количество вершин в графе
            n = self.size[0] * self.size[1]
            # инициализируем список расстояний до вершин
            D = [None] * (n + 1)  # n + 1 потому что индексация с 0
            D[self.start] = 0  # расстояние до начальной вершины равно 0
            # список вершин для обхода
            Q = [self.start]
            Qstart = 0  # индекс начала списка Q
            # список для хранения предыдущих вершин
            Prev = [None] * (n + 1)

            # обходим вершины графа, пока список вершин для обхода не пуст
            while Qstart < len(Q):
                u = Q[Qstart]  # извлекаем вершину
                Qstart += 1  # увеличиваем индекс для извлечения следующей вершины
                # обходим смежные вершины
                for v in self.graphs[u - 1]:
                    # если расстояние до вершины v не определено
                    if D[v] is None:
                        # устанавливаем расстояние и добавляем вершину в список для обхода
                        D[v] = D[u] + 1
                        Q.append(v)
                        # сохраняем предыдущую вершину для восстановления пути
                        Prev[v] = u

            # инициализируем переменные для хранения информации о пути
            self.amt_points = 0  # количество точек, в которые можно попасть
            self.test_solution_length = 0
            self.test_solution_path = []

            # вычисляем информацию о доступных точках
            for i in range(n + 1):
                Ans = []  # список для хранения пути до вершины i
                curr = i
                # восстанавливаем путь до вершины i, используя информацию из Prev
                while curr is not None:
                    Ans.append(curr)  # добавляем текущую вершину в путь
                    curr = Prev[curr]  # переходим к предыдущей вершине

                # если длина расстояния до вершины i не равна 0
                if D[i]:
                    self.amt_points += 1  # увеличиваем количество доступных точек
                    # если длина пути до вершины i больше, чем сохраненная длина тестового решения
                    if self.test_solution_length < D[i]:
                        # обновляем информацию о решении
                        self.test_solution_length = D[i]
                        self.test_solution_path = Ans[
                            ::-1
                        ]  # сохраняем путь в обратном порядке
                        self.finish = i  # сохраняем финишную вершину

        def try_to_create(self):
            self.create_flag = False
            self.graphs = (
                []
            )  # граф еще не создан. В итоге тут будут все клетки куда можно отсюда попасть
            self.get_random_walls()
            for i in range(
                self.size[0] * self.size[1]
            ):  # для каждой клетки создается список смежных клеток.
                self.num_vertex = i + 1
                self.get_edge_list()
                self.graphs.append(self.edge_list)  # добавляем все связи в граф
            self.get_path()  # исчет путь
            if (
                self.test_solution_length
                > self.min_solution_length  # and self.amt_points > 20
            ):  # проверка на правильность лабиринта
                self.walls = self.test_walls.copy()
                self.solution_length = self.test_solution_length
                self.solution_path = self.test_solution_path.copy()
                self.create_flag = True

        def draw(
            self, color, coord, size, width_wall
        ):  # coord - отступ от левого верх угла
            size_x = size[0] / self.size[0]  # размер клетки по X
            size_y = size[1] / self.size[1]  # размер клетки по Y
            for i in range(self.size[1] + 1):
                for j in range(self.size[0] + 1):
                    if j + 1 < len(self.walls[0][i]):
                        # проверка на стенки и рисование стенок
                        if self.walls[0][i][j]:
                            pygame.draw.line(
                                screen,
                                color,
                                (
                                    int(j * size_x + coord[0]),
                                    int(i * size_y + coord[1]),
                                ),
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
                                (
                                    int(j * size_x + coord[0]),
                                    int(i * size_y + coord[1]),
                                ),
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
                screen,
                (0, 230, 0),
                (crd[0] + 10, crd[1] + 10, size_x - 15, size_y - 15),
            )
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (crd[0] + 10, crd[1] + 10, size_x - 15, size_y - 15),
                5,
            )

            crd = self.cell2coord(self.finish)
            crd[0], crd[1] = crd[1], crd[0]
            crd[0] *= size_x
            crd[1] *= size_y
            pygame.draw.rect(
                screen,
                (230, 0, 0),
                (crd[0] + 10, crd[1] + 10, size_x - 15, size_y - 15),
            )
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (crd[0] + 10, crd[1] + 10, size_x - 15, size_y - 15),
                5,
            )

        def if_wall_at_right(self):
            current_coords = self.player_coord
            vert_walls = self.walls[1][current_coords[1]]
            if vert_walls[current_coords[0]]:
                return True
            return False

        def if_wall_at_left(self):
            current_coords = self.player_coord
            vert_walls = self.walls[1][current_coords[1]]
            if vert_walls[current_coords[0] - 1]:
                return True
            return False

        def if_wall_at_up(self):
            current_coords = self.player_coord
            goriz_walls = self.walls[0][current_coords[1] - 1]
            if goriz_walls[current_coords[0] - 1]:
                return True
            return False

        def if_wall_at_down(self):
            current_coords = self.player_coord
            vert_walls = self.walls[0][current_coords[1]]
            if vert_walls[current_coords[0] - 1]:
                return True
            return False

        def draw_player(self, size):
            self.player_cell = self.coord2cell(self.player_coord) - 9

            size_x = size[0] / self.size[0]
            size_y = size[1] / self.size[1]

            crd = self.cell2coord(self.player_cell)
            crd[0], crd[1] = crd[1], crd[0]
            crd[0] *= size_x
            crd[1] *= size_y

            pygame.draw.rect(
                screen,
                (255, 165, 0),
                (
                    crd[0] + 10,
                    crd[1] + 10,
                    size_x - 15,
                    size_y - 15,
                ),
            )
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (
                    crd[0] + 10,
                    crd[1] + 10,
                    size_x - 15,
                    size_y - 15,
                ),
                5,
            )

    pygame.init()
    pygame.font.init()
    size_screen = [325, 645]
    color_screen = (230, 230, 230)
    screen = pygame.display.set_mode(size_screen)

    clock = pygame.time.Clock()
    FPS = 50

    keydown = []

    maze = Maze(20, [10, 1], [8, 16], 1, [1, 1])  #

    step = 1
    TMP_i = 0
    games_count = 0
    steps_player_count = 0

    default_time_per_step = 1.5
    time_elapsed = 0

    final_points = 0

    while step and games_count <= 5:
        keydown = pygame.key.get_pressed()
        if step == 1:
            maze.try_to_create()
            if maze.create_flag:
                maze.print()
                print(TMP_i, maze.solution_length)
                TMP_i = 0
                step = 2
                print("steps:", steps_player_count)
                print("time:", round(time_elapsed))

                prev_points = final_points
                if steps_player_count != 0:
                    final_points += (
                        (maze.min_solution_length * default_time_per_step)
                        / max(
                            time_elapsed,
                            (maze.min_solution_length * default_time_per_step),
                        )
                        + maze.min_solution_length / steps_player_count
                    ) * 50

                print("points for that game:", final_points - prev_points)

                games_count += 1
                steps_player_count = 0
                start_time = time.time()
            else:
                TMP_i += 1

        if step == 2:
            screen.fill(color_screen)
            maze.draw((0, 0, 0), [2, 2], [320, 640], 5)
            maze.draw_player([320, 640])

            if keydown[pygame.K_r]:
                maze.player_coord = list(
                    map(lambda x: x + 1, maze.cell2coord(maze.start))
                )[::-1]

            if keydown[pygame.K_d]:
                moving = False
                while not maze.if_wall_at_right():
                    moving = True
                    maze.player_coord[0] += 1
                    screen.fill(color_screen)
                    maze.draw((0, 0, 0), [2, 2], [320, 640], 5)
                    maze.draw_player([320, 640])
                    pygame.display.flip()
                    time.sleep(FPS * 0.001)
                if moving:
                    steps_player_count += 1
                if (
                    maze.player_coord
                    == list(map(lambda x: x + 1, maze.cell2coord(maze.finish)))[::-1]
                ):
                    maze.start = maze.finish
                    step = 1
                    end_time = time.time()
                    time_elapsed = end_time - start_time

            if keydown[pygame.K_a]:
                moving = False
                while not maze.if_wall_at_left():
                    moving = True
                    maze.player_coord[0] -= 1
                    screen.fill(color_screen)
                    maze.draw((0, 0, 0), [2, 2], [320, 640], 5)
                    maze.draw_player([320, 640])
                    pygame.display.flip()
                    time.sleep(FPS * 0.001)
                if moving:
                    steps_player_count += 1
                if (
                    maze.player_coord
                    == list(map(lambda x: x + 1, maze.cell2coord(maze.finish)))[::-1]
                ):
                    maze.start = maze.finish
                    step = 1
                    end_time = time.time()
                    time_elapsed = end_time - start_time

            if keydown[pygame.K_w]:
                moving = False
                while not maze.if_wall_at_up():
                    moving = True
                    maze.player_coord[1] -= 1
                    screen.fill(color_screen)
                    maze.draw((0, 0, 0), [2, 2], [320, 640], 5)
                    maze.draw_player([320, 640])
                    pygame.display.flip()
                    time.sleep(FPS * 0.001)
                if moving:
                    steps_player_count += 1
                if (
                    maze.player_coord
                    == list(map(lambda x: x + 1, maze.cell2coord(maze.finish)))[::-1]
                ):
                    maze.start = maze.finish
                    step = 1
                    end_time = time.time()
                    time_elapsed = end_time - start_time

            if keydown[pygame.K_s]:
                moving = False
                while not maze.if_wall_at_down():
                    moving = True
                    maze.player_coord[1] += 1
                    screen.fill(color_screen)
                    maze.draw((0, 0, 0), [2, 2], [320, 640], 5)
                    maze.draw_player([320, 640])
                    pygame.display.flip()
                    time.sleep(FPS * 0.001)
                if moving:
                    steps_player_count += 1
                if (
                    maze.player_coord
                    == list(map(lambda x: x + 1, maze.cell2coord(maze.finish)))[::-1]
                ):
                    maze.start = maze.finish
                    step = 1
                    end_time = time.time()
                    time_elapsed = end_time - start_time

            pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                step = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    step = 0

        clock.tick()

    print(round(final_points), "/ 500")

    with open("data/game_data/record.txt", "r") as f:
        record_score = int(f.readlines()[0].strip())

    if round(final_points) > record_score:
        with open("data/game_data/record.txt", "w") as f:
            f.write(str(round(final_points)))

    return start_final_window(round(final_points))
