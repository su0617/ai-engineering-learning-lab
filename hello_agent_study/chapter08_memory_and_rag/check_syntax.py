"""对第八章示例做轻量语法检查。

这个检查只使用 Python 标准库，不导入 HelloAgents、数据库驱动或模型依赖。
因此可以在没有完整运行环境时，先确认课程代码本身没有语法错误。
"""

from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent


def main() -> int:
    """编译当前目录下的 Python 文件，并返回进程状态码。"""
    files = sorted(PROJECT_DIR.glob("*.py"))
    failed = []

    for file_path in files:
        try:
            source = file_path.read_text(encoding="utf-8")
            compile(source, str(file_path), "exec")
            print(f"[OK] {file_path.name}")
        except (OSError, SyntaxError) as error:
            failed.append((file_path.name, error))
            print(f"[FAIL] {file_path.name}: {error}")

    print(f"\n检查完成：{len(files) - len(failed)}/{len(files)} 个文件通过。")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
