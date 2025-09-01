#!/usr/bin/env python3
"""
俄罗斯方块游戏逻辑测试脚本
测试游戏的核心逻辑而不需要图形界面
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_piece_creation():
    """测试方块创建"""
    from tetris import Piece, SHAPES
    
    print("测试方块创建...")
    piece = Piece(5, 0)
    assert 0 <= piece.shape_index < len(SHAPES), "方块索引超出范围"
    assert piece.x == 5 and piece.y == 0, "方块位置不正确"
    assert piece.rotation == 0, "初始旋转状态不正确"
    print("✓ 方块创建测试通过")

def test_piece_rotation():
    """测试方块旋转"""
    from tetris import Piece, SHAPES
    
    print("测试方块旋转...")
    piece = Piece(5, 0)
    initial_rotation = piece.rotation
    piece.rotate()
    expected_rotation = (initial_rotation + 1) % len(SHAPES[piece.shape_index])
    assert piece.rotation == expected_rotation, "方块旋转不正确"
    print("✓ 方块旋转测试通过")

def test_game_initialization():
    """测试游戏初始化"""
    from tetris import TetrisGame, GRID_WIDTH, GRID_HEIGHT, BLACK
    
    print("测试游戏初始化...")
    game = TetrisGame()
    
    # 检查网格尺寸
    assert len(game.grid) == GRID_HEIGHT, "网格高度不正确"
    assert len(game.grid[0]) == GRID_WIDTH, "网格宽度不正确"
    
    # 检查网格初始状态
    for row in game.grid:
        for cell in row:
            assert cell == BLACK, "网格初始状态不是空的"
    
    # 检查初始游戏状态
    assert game.score == 0, "初始得分不为0"
    assert game.lines_cleared == 0, "初始消除行数不为0"
    assert game.level == 1, "初始等级不为1"
    assert game.current_piece is not None, "当前方块未创建"
    assert game.next_piece is not None, "下一个方块未创建"
    
    print("✓ 游戏初始化测试通过")

def test_collision_detection():
    """测试碰撞检测"""
    from tetris import TetrisGame, BLACK
    
    print("测试碰撞检测...")
    game = TetrisGame()
    
    # 测试边界碰撞
    piece = game.current_piece
    
    # 测试左边界
    piece.x = -1
    assert not game.is_valid_position(piece), "左边界碰撞检测失败"
    
    # 测试右边界
    piece.x = 15  # 超出右边界
    assert not game.is_valid_position(piece), "右边界碰撞检测失败"
    
    # 测试底边界
    piece.x = 5
    piece.y = 25  # 超出底边界
    assert not game.is_valid_position(piece), "底边界碰撞检测失败"
    
    # 测试有效位置
    piece.x = 5
    piece.y = 0
    assert game.is_valid_position(piece), "有效位置检测失败"
    
    print("✓ 碰撞检测测试通过")

def test_line_clearing():
    """测试行消除逻辑"""
    from tetris import TetrisGame, GRID_WIDTH, RED
    
    print("测试行消除...")
    game = TetrisGame()
    
    # 手动创建一个完整的行
    test_row = GRID_WIDTH - 1  # 最后一行
    for x in range(GRID_WIDTH):
        game.grid[test_row][x] = RED
    
    initial_score = game.score
    initial_lines = game.lines_cleared
    
    # 调用行消除
    game.clear_lines()
    
    # 检查结果
    assert game.lines_cleared == initial_lines + 1, "消除行数未正确更新"
    assert game.score > initial_score, "得分未正确更新"
    
    # 检查行是否被正确移除
    for x in range(GRID_WIDTH):
        assert game.grid[test_row][x] == game.grid[0][x], "行未正确移除"
    
    print("✓ 行消除测试通过")

def test_movement():
    """测试方块移动"""
    from tetris import TetrisGame
    
    print("测试方块移动...")
    game = TetrisGame()
    
    piece = game.current_piece
    initial_x = piece.x
    initial_y = piece.y
    
    # 测试水平移动
    if game.move_piece(1, 0):  # 向右移动
        assert piece.x == initial_x + 1, "水平移动失败"
    
    if game.move_piece(-1, 0):  # 向左移动
        assert piece.x == initial_x, "水平移动失败"
    
    # 测试垂直移动
    if game.move_piece(0, 1):  # 向下移动
        assert piece.y == initial_y + 1, "垂直移动失败"
    
    print("✓ 方块移动测试通过")

def main():
    """运行所有测试"""
    print("开始测试俄罗斯方块游戏逻辑...\n")
    
    try:
        test_piece_creation()
        test_piece_rotation()
        test_game_initialization()
        test_collision_detection()
        test_line_clearing()
        test_movement()
        
        print("\n🎉 所有测试都通过了！")
        print("俄罗斯方块游戏逻辑工作正常。")
        print("\n要在有图形界面的环境中运行完整游戏，请使用:")
        print("  python3 tetris.py")
        print("或者:")
        print("  python3 run_tetris.py")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)