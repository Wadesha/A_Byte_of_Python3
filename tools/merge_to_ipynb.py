#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
merge_to_ipynb.py — 将各章目录下的 Python 源码合并为 Jupyter Notebook。

用法:
    python tools/merge_to_ipynb.py [SOURCE_DIR]

说明:
    - 不传参数时，默认扫描本脚本所在目录的上一级（即仓库根）下的 chapters/ 与 examples/ 子目录。
    - 为每个子目录生成一个同名 .ipynb（如 chapters/ch08-functions -> ch08-functions.ipynb）。
    - 自动检测 while True: / input()，并在 Notebook 中插入运行警告，避免误执行。

注意: 原脚本硬编码了本地绝对路径，本仓库版本已改为可移植的相对路径，
       以便在任何克隆本仓库的机器上运行，且不泄露作者本地目录结构。
"""
import os
import json
import glob
import sys


def resolve_source_dir():
    """决定要扫描的源目录（仓库根）。"""
    if len(sys.argv) > 1:
        return os.path.abspath(sys.argv[1])
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(here)  # 仓库根


SOURCE_DIR = resolve_source_dir()
EXCLUDE_DIRS = {"__pycache__", "tmp", ".git"}
INCLUDE_EXTENSIONS = [".py", ".pyw"]


def create_ipynb_from_scripts(folder_path, output_ipynb):
    """将文件夹中的 Python 脚本合并成一个 ipynb 文件。"""
    python_files = []
    for ext in INCLUDE_EXTENSIONS:
        python_files.extend(glob.glob(os.path.join(folder_path, f"*{ext}")))
    python_files.sort()

    if not python_files:
        print(f"文件夹 {folder_path} 中没有 Python 文件，跳过...")
        return

    ipynb_content = {
        "cells": [],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            }
        },
        "nbformat": 4,
        "nbformat_minor": 2,
    }

    for file_path in python_files:
        file_name = os.path.basename(file_path)

        ipynb_content["cells"].append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [f"# {file_name}\n"],
        })

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                file_content = f.read()
        except UnicodeDecodeError:
            with open(file_path, "r", encoding="gbk") as f:
                file_content = f.read()

        has_infinite_loop = "while True:" in file_content
        has_input = "input(" in file_content or "raw_input(" in file_content

        explanation_cell = {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 代码说明\n"],
        }
        if has_input:
            explanation_cell["source"].append("- **输入参数**: 用户输入\n")
        if "print(" in file_content:
            explanation_cell["source"].append("- **输出结果**: 控制台输出\n")
        if has_infinite_loop:
            explanation_cell["source"].append("- **循环结构**: 无限循环，需要用户输入特定值退出\n")
        if "def " in file_content:
            explanation_cell["source"].append("- **函数定义**: 包含函数声明\n")
        if "class " in file_content:
            explanation_cell["source"].append("- **类定义**: 包含类声明\n")
        ipynb_content["cells"].append(explanation_cell)

        if has_infinite_loop:
            ipynb_content["cells"].append({
                "cell_type": "markdown",
                "metadata": {"warning": True},
                "source": [
                    "## ⚠️ 重要警告\n",
                    "- **此代码包含无限循环**\n",
                    "- **不建议在 Jupyter Notebook 中执行**\n",
                    "- 若要查看代码逻辑，请仅阅读，不要运行\n",
                    "- 如果意外运行，请立即停止：点击工具栏停止按钮或使用快捷键 Esc + I + I\n",
                ],
            })
        elif has_input:
            ipynb_content["cells"].append({
                "cell_type": "markdown",
                "metadata": {"warning": True},
                "source": [
                    "## 安全提示\n",
                    "- 此代码包含用户输入\n",
                    "- 在 Jupyter Notebook 中运行时，需要在弹出的输入框中提供输入\n",
                    "- 若要停止运行，请点击工具栏中的停止按钮\n",
                    "- 或使用键盘快捷键: Esc + I + I\n",
                ],
            })

        ipynb_content["cells"].append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 使用提示\n",
                "1. **阅读模式**: 建议以只读方式查看代码逻辑\n",
                "2. **测试模式**: 如果需要测试，建议在本地 Python 环境中运行\n",
                "3. **安全运行**: 如需在 Notebook 中运行，请确保了解代码行为\n",
                "4. **紧急停止**: 如遇问题，使用快捷键 Esc + I + I 强制停止\n",
            ],
        })

        ipynb_content["cells"].append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [file_content],
        })

    with open(output_ipynb, "w", encoding="utf-8") as f:
        json.dump(ipynb_content, f, indent=2, ensure_ascii=False)
    print(f"已创建 {output_ipynb}，包含 {len(python_files)} 个 Python 文件")


def main():
    """主函数：遍历 chapters/ 与 examples/ 下各子目录生成笔记本。"""
    for item in os.listdir(SOURCE_DIR):
        item_path = os.path.join(SOURCE_DIR, item)
        if not os.path.isdir(item_path) or item in EXCLUDE_DIRS:
            continue
        if item in ("chapters", "examples"):
            for sub in os.listdir(item_path):
                sub_path = os.path.join(item_path, sub)
                if os.path.isdir(sub_path):
                    output_ipynb = os.path.join(sub_path, f"{sub}.ipynb")
                    create_ipynb_from_scripts(sub_path, output_ipynb)
        # 其它顶层目录（如 tools）跳过


if __name__ == "__main__":
    main()
