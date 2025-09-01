#!/usr/bin/env python3
"""
俄罗斯方块游戏启动脚本
运行此脚本来开始游戏
"""

import os
import sys

def main():
    # 确保我们在正确的目录中
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    try:
        # 导入并运行游戏
        from tetris import main as tetris_main
        print("正在启动俄罗斯方块游戏...")
        print("游戏控制:")
        print("  ← → : 移动方块")
        print("  ↓ : 软降（加速下落）")
        print("  ↑ : 旋转方块")
        print("  空格 : 硬降（直接落到底部）")
        print("  P : 暂停/继续")
        print("  R : 重新开始")
        print("  关闭窗口或按 Ctrl+C 退出游戏")
        print("\n开始游戏！")
        
        tetris_main()
        
    except ImportError as e:
        print(f"导入错误: {e}")
        print("请确保 tetris.py 文件在同一目录中")
        sys.exit(1)
    except Exception as e:
        print(f"游戏运行出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()