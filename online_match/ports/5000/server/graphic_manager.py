import pygame
import sys
import time

black = (0, 0, 0)
white = (255, 255, 255)
menu_main_color = (62, 39, 35)
menu_second_color = (121, 85, 72)


class GraphicManager:
    def __init__(self):
        pygame.init()
        self.display_width = 800
        self.display_height = 600
        self.menu_width = 800
        self.menu_height = 400
        self.menu_surface = None
        self.name = []
        self.board = pygame.image.load("abalone_board_game_2.png")
        self.w_marble = pygame.image.load("white.png")
        self.b_marble = pygame.image.load('black.png')
        self.points_rect = [0, 0]

    def set_output(self, msg):
        self.draw(msg)

    def draw_name(self, name1, name2):
        font = pygame.font.Font("IMMORTAL.ttf", 18)
        text_surface = font.render(name2, 1, white, black)
        text_rect = text_surface.get_rect()
        text_rect.topright = (self.display_width - 1, 0)
        shape_rect = self.b_marble.get_rect()
        shape_rect.topright = text_rect.bottomright
        self.points_rect[1] = shape_rect.bottomright
        self.surface.fill(white, shape_rect)
        self.surface.blit(text_surface, text_rect)
        self.surface.blit(self.b_marble, shape_rect)
        text_surface = font.render(name1, 1, white, black)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (0, 0)
        shape_rect = self.w_marble.get_rect()
        shape_rect.topleft = text_rect.bottomleft
        self.points_rect[0] = shape_rect.bottomleft
        self.surface.blit(self.w_marble, shape_rect)
        self.surface.blit(text_surface, text_rect)

    @staticmethod
    def exit_game():
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    pygame.display.quit()
                    sys.exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                pygame.display.quit()
                sys.exit()

    def draw(self, board):
        rect_board = self.board.get_rect()
        rect_board.center = (self.display_width / 2, self.display_height / 2)
        self.surface.blit(self.board, rect_board)
        self.draw_name(self.name[0], self.name[1])
        self.draw_marbles(board)
        pygame.display.update()
        self.exit_game()

    def draw_marbles(self, board):
        rotate_board = []
        for i in range(len(board)):
            rotate_board.append([j[i] for j in board])
        # print('\n'.join([' '.join([str(j) for j in i]) for i in rotate_board]))
        for i in range(len(rotate_board)):
            for j in range(len(rotate_board[i])):
                j2 = j if i <= 4 else j + 4 - i
                data = rotate_board[i][j]
                x = 102 + abs(4 - i) * 34
                y = 274 + (4 - i) * 57
                color = 0
                if data == 1:
                    color = self.w_marble
                elif data == 2:
                    color = self.b_marble
                else:
                    color = None
                if color is not None:
                    self.surface.blit(color, (x + j2 * 68, y))

    def draw_menu(self):
        self.menu_surface = pygame.display.set_mode((self.menu_width, self.menu_height))
        self.menu_surface.fill(menu_main_color)
        pygame.display.update()
        font = pygame.font.Font("freesansbold.ttf", 30)
        text_surface = font.render("Waiting...", 1, white, menu_second_color)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.menu_width / 2, self.menu_height / 4)
        self.menu_surface.blit(text_surface, text_rect)
        text_rect.center = (self.menu_width / 2, self.menu_height / 4 * 3)
        self.menu_surface.blit(text_surface, text_rect)
        pygame.display.update()

    def draw_menu_name(self, text):
        self.name.append(text)
        font = pygame.font.Font("freesansbold.ttf", 30)
        text_surface = font.render(text + " is connected", 1, white, menu_second_color)
        text_rect = text_surface.get_rect()
        center_temp = self.menu_height / 4 if len(self.name) == 1 else self.menu_height / 4 * 3
        text_rect.center = (self.menu_width / 2, center_temp)
        pygame.draw.rect(self.menu_surface, menu_main_color, (0, center_temp - 50, self.menu_width, center_temp + 50))
        self.menu_surface.blit(text_surface, text_rect)
        pygame.display.flip()
        if len(self.name) == 2:
            text_surface = font.render("Game Is Loading ...", 1, (244, 81, 30), menu_second_color)
            text_rect = text_surface.get_rect()
            text_rect.center = (self.menu_width / 2, self.menu_height / 2)
            self.menu_surface.blit(text_surface, text_rect)
            pygame.display.update()
            # time.sleep(1)
            self.surface = pygame.display.set_mode((self.display_width, self.display_height))
            pygame.display.set_caption('abalone')
            pygame.display.update()

    def draw_points(self, points):
        font = pygame.font.Font("IMMORTAL.ttf", 18)
        text_surface = font.render("{:<5}".format(str(points[0])), 1, (255, 255, 255), (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.topleft = self.points_rect[0]
        self.surface.blit(text_surface, text_rect)
        text_surface = font.render("{:>5}".format(str(points[1])), 1, (255, 255, 255), (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.topright = self.points_rect[1]
        self.surface.blit(text_surface, text_rect)
