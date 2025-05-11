import argparse
import shutil
import subprocess
import sys

def is_command_available(cmd):
    return shutil.which(cmd) is not None

def is_uv_installed():
    return is_command_available("uv")

def install_uv(force=False, use_git=False):
    if not is_command_available("cargo"):
        print("❌ 未找到 cargo，请先安装 Rust：https://www.rust-lang.org/tools/install")
        sys.exit(1)

    if is_uv_installed() and not force:
        print("✅ uv 已安装。")
        return

    cmd = ["cargo", "install"]
    if use_git:
        cmd.extend(["--git", "https://github.com/astral-sh/uv"])
    else:
        cmd.append("uv")

    if force:
        cmd.append("--force")

    try:
        print(f"📦 {'从 Git 安装' if use_git else '使用 cargo 安装'} uv...")
        subprocess.run(cmd, check=True)
        print("✅ uv 安装完成，你可以运行 `uv` 使用它。")
    except subprocess.CalledProcessError:
        print("❌ 安装 uv 失败，请检查错误信息。")
        sys.exit(1)

def uninstall_uv():
    if not is_command_available("cargo"):
        print("❌ 未找到 cargo，请先安装 Rust。")
        sys.exit(1)

    try:
        subprocess.run(["cargo", "uninstall", "uv"], check=True)
        print("🗑️ uv 已卸载。")
    except subprocess.CalledProcessError:
        print("⚠️ 卸载失败，可能未安装 uv 或 cargo 出现问题。")

def check_uv_version():
    if not is_command_available("uv"):
        print("⚠️ 未检测到 uv。")
        return

    try:
        result = subprocess.run(["uv", "--version"], capture_output=True, text=True)
        print("📦 uv 当前版本：", result.stdout.strip())
    except Exception:
        print("⚠️ 无法获取 uv 版本。")

def main():
    parser = argparse.ArgumentParser(description="uv 安装/卸载/查询脚本")
    parser.add_argument(
        "--install", action="store_true", help="安装或更新 uv（默认行为）"
    )
    parser.add_argument("--uninstall", action="store_true", help="卸载 uv")
    parser.add_argument("--version", action="store_true", help="显示已安装的 uv 版本")
    parser.add_argument("--git", action="store_true", help="使用 Git 安装最新开发版")
    parser.add_argument("--force", action="store_true", help="强制重新安装 uv")

    args = parser.parse_args()

    if not (args.install or args.uninstall or args.version):
        args.install = True  # 默认行为是安装

    if args.uninstall:
        uninstall_uv()
    elif args.version:
        check_uv_version()
    elif args.install:
        install_uv(force=args.force, use_git=args.git)

if __name__ == "__main__":
    main()
