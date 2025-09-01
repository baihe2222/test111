import pygame
import random
import sys

# 初始化pygame
pygame.init()

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

# 游戏配置
GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30
GRID_X_OFFSET = 50
GRID_Y_OFFSET = 50

# 窗口尺寸
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE + 2 * GRID_X_OFFSET + 200
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE + 2 * GRID_Y_OFFSET

# 方块形状定义 (I, O, T, S, Z, J, L)
SHAPES = [
    # I形
    [['.....',
      '..#..',
      '..#..',
      '..#..',
      '..#..'],
     ['.....',
      '.....',
      '####.',
      '.....',
      '.....']],
    
    # O形
    [['.....',
      '.....',
      '.##..',
      '.##..',
      '.....']],
    
    # T形
    [['.....',
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
      '.#...']],
    
    # S形
    [['.....',
      '.....',
      '.##..',
      '##...',
      '.....'],
     ['.....',
      '.#...',
      '.##..',
      '..#..',
      '.....']],
    
    # Z形
    [['.....',
      '.....',
      '##...',
      '.##..',
      '.....'],
     ['.....',
      '..#..',
      '.##..',
      '.#...',
      '.....']],
    
    # J形
    [['.....',
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
      '.....']],
    
    # L形
    [['.....',
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
      '.....']]
]

SHAPE_COLORS = [CYAN, YELLOW, PURPLE, GREEN, RED, BLUE, ORANGE]

class Piece:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shape_index = random.randint(0, len(SHAPES) - 1)
        self.rotation = 0
        self.color = SHAPE_COLORS[self.shape_index]
    
    def get_shape(self):
        return SHAPES[self.shape_index][self.rotation]
    
    def get_cells(self):
        """获取方块占用的所有单元格坐标"""
        cells = []
        shape = self.get_shape()
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell == '#':
                    cells.append((self.x + j, self.y + i))
        return cells
    
    def rotate(self):
        """旋转方块"""
        self.rotation = (self.rotation + 1) % len(SHAPES[self.shape_index])

class TetrisGame:
    def __init__(self):
        self.grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.fall_time = 0
        self.fall_speed = 500  # 毫秒
        
    def new_piece(self):
        """创建新方块"""
        return Piece(GRID_WIDTH // 2 - 2, 0)
    
    def is_valid_position(self, piece, dx=0, dy=0, rotation=None):
        """检查方块位置是否有效"""
        if rotation is None:
            rotation = piece.rotation
        
        # 临时创建一个方块来检查位置
        temp_piece = Piece(piece.x + dx, piece.y + dy)
        temp_piece.shape_index = piece.shape_index
        temp_piece.rotation = rotation
        
        cells = temp_piece.get_cells()
        for x, y in cells:
            # 检查边界
            if x < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT:
                return False
            # 检查是否与已存在的方块重叠
            if y >= 0 and self.grid[y][x] != BLACK:
                return False
        return True
    
    def place_piece(self):
        """放置当前方块到网格中"""
        cells = self.current_piece.get_cells()
        for x, y in cells:
            if y >= 0:
                self.grid[y][x] = self.current_piece.color
        
        # 检查并清除完整的行
        self.clear_lines()
        
        # 生成新方块
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        
        # 检查游戏结束
        if not self.is_valid_position(self.current_piece):
            return False
        return True
    
    def clear_lines(self):
        """清除完整的行"""
        lines_to_clear = []
        for y in range(GRID_HEIGHT):
            if all(self.grid[y][x] != BLACK for x in range(GRID_WIDTH)):
                lines_to_clear.append(y)
        
        # 移除完整的行
        for y in lines_to_clear:
            del self.grid[y]
            self.grid.insert(0, [BLACK for _ in range(GRID_WIDTH)])
        
        # 更新得分
        if lines_to_clear:
            self.lines_cleared += len(lines_to_clear)
            # 得分计算：单行100分，双行300分，三行500分，四行800分
            line_scores = {1: 100, 2: 300, 3: 500, 4: 800}
            self.score += line_scores.get(len(lines_to_clear), 0) * self.level
            
            # 每清除10行提升一个等级
            self.level = self.lines_cleared // 10 + 1
            # 等级越高下落越快
            self.fall_speed = max(50, 500 - (self.level - 1) * 50)
    
    def move_piece(self, dx, dy):
        """移动方块"""
        if self.is_valid_position(self.current_piece, dx, dy):
            self.current_piece.x += dx
            self.current_piece.y += dy
            return True
        return False
    
    def rotate_piece(self):
        """旋转方块"""
        new_rotation = (self.current_piece.rotation + 1) % len(SHAPES[self.current_piece.shape_index])
        if self.is_valid_position(self.current_piece, rotation=new_rotation):
            self.current_piece.rotation = new_rotation
            return True
        return False
    
    def hard_drop(self):
        """硬降（快速下降到底部）"""
        while self.move_piece(0, 1):
            self.score += 2  # 硬降奖励分数
        return self.place_piece()
    
    def update(self, dt):
        """更新游戏状态"""
        self.fall_time += dt
        if self.fall_time >= self.fall_speed:
            if not self.move_piece(0, 1):
                return self.place_piece()
            self.fall_time = 0
        return True

class TetrisRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
    
    def draw_grid(self):
        """绘制游戏网格"""
        for x in range(GRID_WIDTH + 1):
            pygame.draw.line(self.screen, GRAY, 
                           (GRID_X_OFFSET + x * CELL_SIZE, GRID_Y_OFFSET),
                           (GRID_X_OFFSET + x * CELL_SIZE, GRID_Y_OFFSET + GRID_HEIGHT * CELL_SIZE))
        
        for y in range(GRID_HEIGHT + 1):
            pygame.draw.line(self.screen, GRAY,
                           (GRID_X_OFFSET, GRID_Y_OFFSET + y * CELL_SIZE),
                           (GRID_X_OFFSET + GRID_WIDTH * CELL_SIZE, GRID_Y_OFFSET + y * CELL_SIZE))
    
    def draw_cell(self, x, y, color):
        """绘制单个单元格"""
        rect = pygame.Rect(
            GRID_X_OFFSET + x * CELL_SIZE + 1,
            GRID_Y_OFFSET + y * CELL_SIZE + 1,
            CELL_SIZE - 2,
            CELL_SIZE - 2
        )
        pygame.draw.rect(self.screen, color, rect)
    
    def draw_piece(self, piece):
        """绘制方块"""
        cells = piece.get_cells()
        for x, y in cells:
            if 0 <= x < GRID_WIDTH and y >= 0:
                self.draw_cell(x, y, piece.color)
    
    def draw_ghost_piece(self, game):
        """绘制虚影方块（显示方块将要落下的位置）"""
        ghost_piece = Piece(game.current_piece.x, game.current_piece.y)
        ghost_piece.shape_index = game.current_piece.shape_index
        ghost_piece.rotation = game.current_piece.rotation
        
        # 找到最低可能的位置
        while game.is_valid_position(ghost_piece, 0, 1):
            ghost_piece.y += 1
        
        # 绘制虚影（使用较淡的颜色）
        cells = ghost_piece.get_cells()
        for x, y in cells:
            if 0 <= x < GRID_WIDTH and y >= 0:
                color = tuple(c // 3 for c in game.current_piece.color)
                self.draw_cell(x, y, color)
    
    def draw_next_piece(self, piece):
        """绘制下一个方块预览"""
        next_x = GRID_X_OFFSET + GRID_WIDTH * CELL_SIZE + 20
        next_y = GRID_Y_OFFSET + 50
        
        # 绘制标题
        text = self.small_font.render("Next:", True, WHITE)
        self.screen.blit(text, (next_x, next_y - 30))
        
        # 绘制下一个方块
        shape = piece.get_shape()
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell == '#':
                    rect = pygame.Rect(
                        next_x + j * (CELL_SIZE // 2),
                        next_y + i * (CELL_SIZE // 2),
                        CELL_SIZE // 2 - 1,
                        CELL_SIZE // 2 - 1
                    )
                    pygame.draw.rect(self.screen, piece.color, rect)
    
    def draw_info(self, game):
        """绘制游戏信息"""
        info_x = GRID_X_OFFSET + GRID_WIDTH * CELL_SIZE + 20
        info_y = GRID_Y_OFFSET + 150
        
        # 得分
        score_text = self.small_font.render(f"Score: {game.score}", True, WHITE)
        self.screen.blit(score_text, (info_x, info_y))
        
        # 行数
        lines_text = self.small_font.render(f"Lines: {game.lines_cleared}", True, WHITE)
        self.screen.blit(lines_text, (info_x, info_y + 30))
        
        # 等级
        level_text = self.small_font.render(f"Level: {game.level}", True, WHITE)
        self.screen.blit(level_text, (info_x, info_y + 60))
        
        # 控制说明
        controls_y = info_y + 120
        controls = [
            "Controls:",
            "← → : Move",
            "↓ : Soft Drop",
            "↑ : Rotate",
            "Space: Hard Drop",
            "P: Pause",
            "R: Restart"
        ]
        
        for i, control in enumerate(controls):
            color = WHITE if i == 0 else GRAY
            font = self.small_font if i == 0 else pygame.font.Font(None, 20)
            text = font.render(control, True, color)
            self.screen.blit(text, (info_x, controls_y + i * 20))
    
    def draw_game_over(self):
        """绘制游戏结束画面"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font.render("GAME OVER", True, RED)
        restart_text = self.small_font.render("Press R to restart", True, WHITE)
        
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(restart_text, restart_rect)
    
    def draw_pause(self):
        """绘制暂停画面"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        pause_text = self.font.render("PAUSED", True, YELLOW)
        continue_text = self.small_font.render("Press P to continue", True, WHITE)
        
        pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        continue_rect = continue_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        
        self.screen.blit(pause_text, pause_rect)
        self.screen.blit(continue_text, continue_rect)
    
    def render(self, game, game_state):
        """渲染整个游戏"""
        self.screen.fill(BLACK)
        
        # 绘制游戏区域
        self.draw_grid()
        
        # 绘制已放置的方块
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if game.grid[y][x] != BLACK:
                    self.draw_cell(x, y, game.grid[y][x])
        
        if game_state == "playing":
            # 绘制虚影方块
            self.draw_ghost_piece(game)
            # 绘制当前方块
            self.draw_piece(game.current_piece)
        
        # 绘制下一个方块和游戏信息
        self.draw_next_piece(game.next_piece)
        self.draw_info(game)
        
        # 绘制状态覆盖层
        if game_state == "game_over":
            self.draw_game_over()
        elif game_state == "paused":
            self.draw_pause()

def main():
    try:
        # 尝试初始化显示
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("俄罗斯方块")
        clock = pygame.time.Clock()
    except pygame.error as e:
        print(f"无法初始化游戏窗口: {e}")
        print("这通常是因为没有可用的图形显示设备。")
        print("请在有图形界面的环境中运行此游戏。")
        return
    
    game = TetrisGame()
    renderer = TetrisRenderer(screen)
    game_state = "playing"  # "playing", "paused", "game_over"
    
    # 按键重复设置
    pygame.key.set_repeat(250, 50)
    
    running = True
    while running:
        dt = clock.tick(60)  # 60 FPS
        
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # 重新开始游戏
                    game = TetrisGame()
                    game_state = "playing"
                
                elif event.key == pygame.K_p:
                    # 暂停/继续
                    if game_state == "playing":
                        game_state = "paused"
                    elif game_state == "paused":
                        game_state = "playing"
                
                elif game_state == "playing":
                    if event.key == pygame.K_LEFT:
                        game.move_piece(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        game.move_piece(1, 0)
                    elif event.key == pygame.K_DOWN:
                        if game.move_piece(0, 1):
                            game.score += 1  # 软降奖励分数
                    elif event.key == pygame.K_UP:
                        game.rotate_piece()
                    elif event.key == pygame.K_SPACE:
                        if not game.hard_drop():
                            game_state = "game_over"
        
        # 更新游戏状态
        if game_state == "playing":
            if not game.update(dt):
                game_state = "game_over"
        
        # 渲染
        renderer.render(game, game_state)
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()