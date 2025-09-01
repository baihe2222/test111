#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
俄罗斯方块 (Tetris) Game
A complete Tetris implementation in Python using pygame
"""

import pygame
import random
import sys
from typing import List, Tuple, Optional

# 初始化pygame
pygame.init()

# 游戏常量
GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30
GRID_X_OFFSET = 50
GRID_Y_OFFSET = 50

# 窗口尺寸
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE + 2 * GRID_X_OFFSET + 200
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE + 2 * GRID_Y_OFFSET

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

# 方块颜色
PIECE_COLORS = [CYAN, BLUE, ORANGE, YELLOW, GREEN, PURPLE, RED]

# Tetris方块形状定义 (7种标准方块)
TETRIS_SHAPES = [
    # I方块
    [
        ['.....',
         '..#..',
         '..#..',
         '..#..',
         '..#..'],
        ['.....',
         '.....',
         '####.',
         '.....',
         '.....']
    ],
    # O方块
    [
        ['.....',
         '.....',
         '.##..',
         '.##..',
         '.....']
    ],
    # T方块
    [
        ['.....',
         '.....',
         '.#...',
         '###..',
         '.....'],
        ['.....',
         '.....',
         '.#...',
         '.##..',
         '.#...'],
        ['.....',
         '.....',
         '.....',
         '###..',
         '.#...'],
        ['.....',
         '.....',
         '.#...',
         '##...',
         '.#...']
    ],
    # S方块
    [
        ['.....',
         '.....',
         '.##..',
         '##...',
         '.....'],
        ['.....',
         '.#...',
         '.##..',
         '..#..',
         '.....']
    ],
    # Z方块
    [
        ['.....',
         '.....',
         '##...',
         '.##..',
         '.....'],
        ['.....',
         '..#..',
         '.##..',
         '.#...',
         '.....']
    ],
    # J方块
    [
        ['.....',
         '.#...',
         '.#...',
         '##...',
         '.....'],
        ['.....',
         '.....',
         '#....',
         '###..',
         '.....'],
        ['.....',
         '.##..',
         '.#...',
         '.#...',
         '.....'],
        ['.....',
         '.....',
         '###..',
         '..#..',
         '.....']
    ],
    # L方块
    [
        ['.....',
         '..#..',
         '..#..',
         '.##..',
         '.....'],
        ['.....',
         '.....',
         '###..',
         '#....',
         '.....'],
        ['.....',
         '##...',
         '.#...',
         '.#...',
         '.....'],
        ['.....',
         '.....',
         '..#..',
         '###..',
         '.....']
    ]
]


class TetrisPiece:
    """俄罗斯方块单个方块类"""
    
    def __init__(self, x: int, y: int, shape_index: int):
        self.x = x
        self.y = y
        self.shape_index = shape_index
        self.rotation = 0
        self.color = PIECE_COLORS[shape_index]
        
    def get_shape(self) -> List[str]:
        """获取当前旋转状态下的方块形状"""
        return TETRIS_SHAPES[self.shape_index][self.rotation]
    
    def get_cells(self) -> List[Tuple[int, int]]:
        """获取方块占用的所有格子坐标"""
        cells = []
        shape = self.get_shape()
        for row, line in enumerate(shape):
            for col, cell in enumerate(line):
                if cell == '#':
                    cells.append((self.x + col, self.y + row))
        return cells
    
    def rotate(self) -> 'TetrisPiece':
        """返回旋转后的方块副本"""
        new_piece = TetrisPiece(self.x, self.y, self.shape_index)
        new_piece.rotation = (self.rotation + 1) % len(TETRIS_SHAPES[self.shape_index])
        return new_piece
    
    def move(self, dx: int, dy: int) -> 'TetrisPiece':
        """返回移动后的方块副本"""
        new_piece = TetrisPiece(self.x + dx, self.y + dy, self.shape_index)
        new_piece.rotation = self.rotation
        return new_piece


class TetrisGame:
    """俄罗斯方块游戏主类"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("俄罗斯方块 - Tetris")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        # 游戏状态
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = None
        self.next_piece = None
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_time = 0
        self.fall_speed = 500  # 毫秒
        self.game_over = False
        
        # 生成第一个方块
        self.spawn_new_piece()
        
    def spawn_new_piece(self):
        """生成新的方块"""
        if self.next_piece is None:
            self.next_piece = TetrisPiece(3, 0, random.randint(0, 6))
        
        self.current_piece = self.next_piece
        self.next_piece = TetrisPiece(3, 0, random.randint(0, 6))
        
        # 检查游戏是否结束
        if not self.is_valid_position(self.current_piece):
            self.game_over = True
    
    def is_valid_position(self, piece: TetrisPiece) -> bool:
        """检查方块位置是否有效"""
        for x, y in piece.get_cells():
            # 检查边界
            if x < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT:
                return False
            # 检查与已有方块的碰撞
            if y >= 0 and self.grid[y][x] != 0:
                return False
        return True
    
    def place_piece(self, piece: TetrisPiece):
        """将方块放置到游戏板上"""
        for x, y in piece.get_cells():
            if y >= 0:
                self.grid[y][x] = piece.shape_index + 1
    
    def clear_lines(self) -> int:
        """清除完整的行，返回清除的行数"""
        lines_to_clear = []
        for y in range(GRID_HEIGHT):
            if all(self.grid[y][x] != 0 for x in range(GRID_WIDTH)):
                lines_to_clear.append(y)
        
        # 清除行
        for y in reversed(lines_to_clear):
            del self.grid[y]
            self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
        
        lines_cleared = len(lines_to_clear)
        if lines_cleared > 0:
            # 计分：1行=100分，2行=300分，3行=500分，4行=800分
            score_table = {1: 100, 2: 300, 3: 500, 4: 800}
            self.score += score_table.get(lines_cleared, 0) * self.level
            self.lines_cleared += lines_cleared
            
            # 升级：每10行升一级
            self.level = self.lines_cleared // 10 + 1
            self.fall_speed = max(50, 500 - (self.level - 1) * 50)
        
        return lines_cleared
    
    def handle_input(self):
        """处理用户输入"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_r:
                        self.__init__()  # 重新开始游戏
                    continue
                
                if event.key == pygame.K_LEFT:
                    new_piece = self.current_piece.move(-1, 0)
                    if self.is_valid_position(new_piece):
                        self.current_piece = new_piece
                
                elif event.key == pygame.K_RIGHT:
                    new_piece = self.current_piece.move(1, 0)
                    if self.is_valid_position(new_piece):
                        self.current_piece = new_piece
                
                elif event.key == pygame.K_DOWN:
                    new_piece = self.current_piece.move(0, 1)
                    if self.is_valid_position(new_piece):
                        self.current_piece = new_piece
                        self.score += 1
                
                elif event.key == pygame.K_UP:
                    new_piece = self.current_piece.rotate()
                    if self.is_valid_position(new_piece):
                        self.current_piece = new_piece
                
                elif event.key == pygame.K_SPACE:
                    # 硬降（直接落到底部）
                    while True:
                        new_piece = self.current_piece.move(0, 1)
                        if self.is_valid_position(new_piece):
                            self.current_piece = new_piece
                            self.score += 2
                        else:
                            break
        
        return True
    
    def update(self, dt: int):
        """更新游戏状态"""
        if self.game_over:
            return
        
        self.fall_time += dt
        if self.fall_time >= self.fall_speed:
            self.fall_time = 0
            
            # 尝试向下移动
            new_piece = self.current_piece.move(0, 1)
            if self.is_valid_position(new_piece):
                self.current_piece = new_piece
            else:
                # 方块无法继续下降，固定到游戏板上
                self.place_piece(self.current_piece)
                self.clear_lines()
                self.spawn_new_piece()
    
    def draw_grid(self):
        """绘制游戏网格"""
        for y in range(GRID_HEIGHT + 1):
            pygame.draw.line(self.screen, GRAY,
                           (GRID_X_OFFSET, GRID_Y_OFFSET + y * CELL_SIZE),
                           (GRID_X_OFFSET + GRID_WIDTH * CELL_SIZE, GRID_Y_OFFSET + y * CELL_SIZE))
        
        for x in range(GRID_WIDTH + 1):
            pygame.draw.line(self.screen, GRAY,
                           (GRID_X_OFFSET + x * CELL_SIZE, GRID_Y_OFFSET),
                           (GRID_X_OFFSET + x * CELL_SIZE, GRID_Y_OFFSET + GRID_HEIGHT * CELL_SIZE))
    
    def draw_piece(self, piece: TetrisPiece):
        """绘制方块"""
        for x, y in piece.get_cells():
            if 0 <= x < GRID_WIDTH and y >= 0:
                rect = pygame.Rect(
                    GRID_X_OFFSET + x * CELL_SIZE + 1,
                    GRID_Y_OFFSET + y * CELL_SIZE + 1,
                    CELL_SIZE - 2,
                    CELL_SIZE - 2
                )
                pygame.draw.rect(self.screen, piece.color, rect)
    
    def draw_placed_pieces(self):
        """绘制已放置的方块"""
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x] != 0:
                    color = PIECE_COLORS[self.grid[y][x] - 1]
                    rect = pygame.Rect(
                        GRID_X_OFFSET + x * CELL_SIZE + 1,
                        GRID_Y_OFFSET + y * CELL_SIZE + 1,
                        CELL_SIZE - 2,
                        CELL_SIZE - 2
                    )
                    pygame.draw.rect(self.screen, color, rect)
    
    def draw_next_piece(self):
        """绘制下一个方块预览"""
        if self.next_piece:
            # 绘制预览区域标题
            text = self.font.render("下一个:", True, WHITE)
            self.screen.blit(text, (GRID_X_OFFSET + GRID_WIDTH * CELL_SIZE + 20, 50))
            
            # 绘制下一个方块
            shape = self.next_piece.get_shape()
            for row, line in enumerate(shape):
                for col, cell in enumerate(line):
                    if cell == '#':
                        rect = pygame.Rect(
                            GRID_X_OFFSET + GRID_WIDTH * CELL_SIZE + 20 + col * 20,
                            80 + row * 20,
                            18,
                            18
                        )
                        pygame.draw.rect(self.screen, self.next_piece.color, rect)
    
    def draw_info(self):
        """绘制游戏信息"""
        info_x = GRID_X_OFFSET + GRID_WIDTH * CELL_SIZE + 20
        
        # 分数
        score_text = self.font.render(f"分数: {self.score}", True, WHITE)
        self.screen.blit(score_text, (info_x, 180))
        
        # 等级
        level_text = self.font.render(f"等级: {self.level}", True, WHITE)
        self.screen.blit(level_text, (info_x, 220))
        
        # 消除行数
        lines_text = self.font.render(f"行数: {self.lines_cleared}", True, WHITE)
        self.screen.blit(lines_text, (info_x, 260))
        
        # 操作说明
        controls = [
            "操作说明:",
            "←→: 左右移动",
            "↓: 加速下降",
            "↑: 旋转",
            "空格: 硬降"
        ]
        
        for i, text in enumerate(controls):
            color = YELLOW if i == 0 else WHITE
            control_text = pygame.font.Font(None, 24).render(text, True, color)
            self.screen.blit(control_text, (info_x, 320 + i * 25))
    
    def draw_game_over(self):
        """绘制游戏结束画面"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = pygame.font.Font(None, 72).render("游戏结束", True, RED)
        text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, text_rect)
        
        final_score_text = self.font.render(f"最终分数: {self.score}", True, WHITE)
        score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(final_score_text, score_rect)
        
        restart_text = self.font.render("按 R 键重新开始", True, YELLOW)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        self.screen.blit(restart_text, restart_rect)
    
    def draw(self):
        """绘制游戏画面"""
        self.screen.fill(BLACK)
        
        # 绘制游戏区域
        self.draw_grid()
        self.draw_placed_pieces()
        
        if self.current_piece and not self.game_over:
            self.draw_piece(self.current_piece)
        
        # 绘制UI
        self.draw_next_piece()
        self.draw_info()
        
        # 绘制游戏结束画面
        if self.game_over:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def run(self):
        """运行游戏主循环"""
        running = True
        while running:
            dt = self.clock.tick(60)
            
            running = self.handle_input()
            self.update(dt)
            self.draw()
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = TetrisGame()
    game.run()