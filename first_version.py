import random, pygame, math, time

graphs = [] #hello, World of the
found = {}
cell = [15, 10]

max_lengh = 15

chance = [4, 1]
size_cell = 50
size_top_bar = 0
size_left_bar = 0
size_right_bar = 0
size_bottom_bar = 0
size_main_bar = [cell[0] * size_cell, cell[1] * size_cell]
size_screen = [
    size_left_bar + size_right_bar + size_main_bar[0],
    size_top_bar + size_bottom_bar + size_main_bar[1],
]

x_wall = []
y_wall = []
width_wall = 3
color_wall = (150, 150, 150)

color_screen = (250, 250, 250)

player_coord = [0, 0]
player_color = (150, 150, 150)
player_size = [size_cell - 10, size_cell - 10]
player_move = ""
player_step_move = 0.2

clock = pygame.time.Clock()
FPS = 50

pygame.init()
screen = pygame.display.set_mode(size_screen)
pygame.display.set_caption("jast maze")


def print_maze(x_wall, y_wall):
    for i in range(cell[1] + 1):
        line = ""
        for j in range(cell[0] + 1):
            if y_wall[i][j]:
                line += "|"
            else:
                line += " "
            if x_wall[i][j]:
                line += "__"
            else:
                line += "  "
        print(line)


def graph_vertex_coord(num):
    coord = []
    coord.append((num - 1) // cell[0])
    coord.append((num - 1) % cell[0])
    return coord


def graph_edge_list(num, x_wall, y_wall):
    coord = graph_vertex_coord(num)
    vertex = []

    for i in range(coord[1], cell[0]):
        if y_wall[coord[0] + 1][i + 1]:
            if cell[0] * coord[0] + i + 1 != num:
                vertex.append(cell[0] * coord[0] + i + 1)
            break

    for i in range(coord[1], -1, -1):
        if y_wall[coord[0] + 1][i]:
            if cell[0] * coord[0] + i + 1 != num:
                vertex.append(cell[0] * coord[0] + i + 1)
            break

    for i in range(coord[0], cell[1]):
        if x_wall[i + 1][coord[1]]:
            if cell[0] * i + coord[1] + 1 != num:
                vertex.append(cell[0] * i + coord[1] + 1)
            break

    for i in range(coord[0], -1, -1):
        if x_wall[i][coord[1]]:
            if cell[0] * i + coord[1] + 1 != num:
                vertex.append(cell[0] * i + coord[1] + 1)
            break

    vertex.sort()
    return vertex


def graph_pathfinder(start, finish, graphs):
    n = cell[0] * cell[1]
    D = [None] * (n + 1)
    D[start] = 0
    Q = [start]
    Qstart = 0
    Prev = [None] * (n + 1)

    while Qstart < len(Q):
        u = Q[Qstart]
        Qstart += 1
        for v in graphs[u - 1]:
            if D[v] is None:
                D[v] = D[u] + 1
                Q.append(v)
                Prev[v] = u

    Ans = []
    curr = finish
    while curr is not None:
        Ans.append(curr)
        curr = Prev[curr]

    return D[finish], Ans[::-1]


def maze_x_y_wall():
    x_wall = []
    y_wall = []
    c = []

    for i in range(chance[0] * cell[0]):
        c.append(0)
    for i in range(chance[1] * cell[0]):
        c.append(1)

    x_wall = list(random.sample(c, cell[0] + 1) for i in range(cell[1] + 1))
    y_wall = list(random.sample(c, cell[0] + 1) for i in range(cell[1] + 1))

    for i in range(cell[0] + 1):
        x_wall[0][cell[0] - i] = 1
        x_wall[cell[1]][cell[0] - i] = 1
    for i in range(cell[1] + 1):
        y_wall[i][cell[0]] = 1
        y_wall[i][0] = 1
    for i in range(cell[1] + 1):
        x_wall[i][cell[0]] = 0
    for i in range(cell[0] + 1):
        y_wall[0][i] = 0

    return x_wall, y_wall


def draw_maze(x_wall, y_wall):
    for i in range(len(x_wall)):
        for j in range(len(x_wall[i]) - 1):
            if x_wall[i][j]:
                pygame.draw.line(
                    screen,
                    color_wall,
                    (j * size_cell + size_left_bar, i * size_cell + size_top_bar),
                    ((j + 1) * size_cell + size_left_bar, i * size_cell + size_top_bar),
                    width_wall,
                )

    for i in range(len(y_wall) - 1):
        for j in range(len(y_wall[i])):
            if y_wall[i + 1][j]:
                pygame.draw.line(
                    screen,
                    color_wall,
                    (j * size_cell + size_left_bar, i * size_cell + size_top_bar),
                    (j * size_cell + size_left_bar, (i + 1) * size_cell + size_top_bar),
                    width_wall,
                )


def maze_attempt():
    graphs = []

    x_wall, y_wall = maze_x_y_wall()

    for i in range(cell[0] * cell[1]):
        graphs.append(graph_edge_list(i + 1, x_wall, y_wall))

    solution_length, solution_path = graph_pathfinder(1, cell[0] * cell[1], graphs)

    if solution_length:
        if solution_length >= max_lengh:
            print_maze(x_wall, y_wall)
            print(solution_length, solution_path)
            return x_wall, y_wall, graphs

    return False


def maze_ganeration():
    a = 1
    while True:
        print(a)
        a += 1

        attempt_result = maze_attempt()

        if attempt_result:
            return attempt_result[0], attempt_result[1]


def draw_player():
    pygame.draw.rect(
        screen,
        player_color,
        (
            player_coord[0] * size_cell + 5 + size_left_bar,
            player_coord[1] * size_cell + 5 + size_top_bar,
            player_size[0],
            player_size[1],
        ),
    )


def move_player(move):
    global player_move, player_coord
    if move == "up":
        if x_wall[math.ceil(player_coord[1])][player_coord[0]]:
            player_coord[1] = math.ceil(player_coord[1])
            player_move = ""
        else:
            player_coord[1] -= player_step_move
    if move == "down":
        if x_wall[math.floor(player_coord[1]) + 1][player_coord[0]]:
            player_coord[1] = math.floor(player_coord[1])
            player_move = ""
        else:
            player_coord[1] += player_step_move
    if move == "left":
        if y_wall[player_coord[1] + 1][math.ceil(player_coord[0])]:
            player_coord[0] = math.ceil(player_coord[0])
            player_move = ""
        else:
            player_coord[0] -= player_step_move
    if move == "right":
        if y_wall[player_coord[1] + 1][math.floor(player_coord[0]) + 1]:
            player_coord[0] = math.floor(player_coord[0])
            player_move = ""
        else:
            player_coord[0] += player_step_move


program_running = True
step_running = 1

while program_running:
    x_wall, y_wall = maze_ganeration()
    player_coord = [0, 0]
    player_move = ""

    while step_running == 1:
        clock.tick(FPS)

        screen.fill(color_screen)
        draw_player()
        draw_maze(x_wall, y_wall)
        pygame.display.flip()

        move_player(player_move)

        if player_coord[0] == cell[0] - 1 and player_coord[1] == cell[1] - 1:
            time.sleep(0.5)
            step_running = 2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                step_running = 0
                program_running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    step_running = 2
                if player_move == "":
                    if event.key == pygame.K_UP:
                        player_move = "up"
                    if event.key == pygame.K_LEFT:
                        player_move = "left"
                    if event.key == pygame.K_RIGHT:
                        player_move = "right"
                    if event.key == pygame.K_DOWN:
                        player_move = "down"

    while step_running == 2:
        screen.fill(color_screen)
        draw_player()
        draw_maze(x_wall, y_wall)
        pygame.display.flip()

        if math.ceil(player_coord[0]) > 0:
            player_coord[0] -= 0.05
        elif math.ceil(player_coord[1]) > 0:
            player_coord[1] -= 0.05
        else:
            step_running = 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                step_running = 0
                program_running = False

pygame.quit()
