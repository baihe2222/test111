#!/usr/bin/env python3
"""
俄罗斯方块游戏测试文件
"""

import unittest
from tetris import TetrisPiece, TetrisGame, TETRIS_SHAPES


class TestTetrisPiece(unittest.TestCase):
    """测试TetrisPiece类"""
    
    def test_piece_creation(self):
        """测试方块创建"""
        piece = TetrisPiece(5, 0, 0)  # I方块
        self.assertEqual(piece.x, 5)
        self.assertEqual(piece.y, 0)
        self.assertEqual(piece.shape_index, 0)
        self.assertEqual(piece.rotation, 0)
    
    def test_invalid_shape_index(self):
        """测试无效的方块索引"""
        with self.assertRaises(ValueError):
            TetrisPiece(0, 0, 10)  # 超出范围
        
        with self.assertRaises(ValueError):
            TetrisPiece(0, 0, -1)  # 负数
    
    def test_piece_rotation(self):
        """测试方块旋转"""
        piece = TetrisPiece(5, 0, 0)  # I方块
        rotated = piece.rotate()
        
        self.assertEqual(rotated.x, 5)
        self.assertEqual(rotated.y, 0)
        self.assertEqual(rotated.shape_index, 0)
        self.assertEqual(rotated.rotation, 1)
    
    def test_piece_movement(self):
        """测试方块移动"""
        piece = TetrisPiece(5, 0, 0)
        moved = piece.move(1, 2)
        
        self.assertEqual(moved.x, 6)
        self.assertEqual(moved.y, 2)
        self.assertEqual(moved.shape_index, 0)
        self.assertEqual(moved.rotation, 0)
    
    def test_get_cells(self):
        """测试获取方块占用的格子"""
        piece = TetrisPiece(0, 0, 1)  # O方块
        cells = piece.get_cells()
        
        # O方块应该占用4个格子
        self.assertEqual(len(cells), 4)
        # 检查具体位置
        expected_cells = [(1, 2), (2, 2), (1, 3), (2, 3)]
        self.assertEqual(sorted(cells), sorted(expected_cells))


class TestTetrisGame(unittest.TestCase):
    """测试TetrisGame类"""
    
    def setUp(self):
        """测试前准备"""
        # 避免实际初始化pygame窗口
        import pygame
        pygame.display.set_mode = lambda x: None
        self.game = TetrisGame()
    
    def test_game_initialization(self):
        """测试游戏初始化"""
        self.assertEqual(len(self.game.grid), 20)
        self.assertEqual(len(self.game.grid[0]), 10)
        self.assertEqual(self.game.score, 0)
        self.assertEqual(self.game.level, 1)
        self.assertFalse(self.game.game_over)
        self.assertFalse(self.game.paused)
    
    def test_valid_position(self):
        """测试位置有效性检查"""
        # 创建一个在有效位置的方块
        piece = TetrisPiece(0, 0, 1)  # O方块在左上角
        self.assertTrue(self.game.is_valid_position(piece))
        
        # 创建一个超出边界的方块
        piece_out_of_bounds = TetrisPiece(-1, 0, 1)
        self.assertFalse(self.game.is_valid_position(piece_out_of_bounds))
    
    def test_line_clearing(self):
        """测试行消除功能"""
        # 填满底部一行
        for x in range(10):
            self.game.grid[19][x] = 1
        
        lines_cleared = self.game.clear_lines()
        self.assertEqual(lines_cleared, 1)
        
        # 检查行是否被清除
        self.assertTrue(all(cell == 0 for cell in self.game.grid[19]))


if __name__ == "__main__":
    unittest.main()