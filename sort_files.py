import os
import shutil
import sys
from pathlib import Path

# 分类规则，键是目标文件夹名，值是后缀列表
RULES = {
    "图片": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".ico"],
    "文档": [".pdf", ".doc", ".docx", ".txt", ".md", ".xls", ".xlsx", ".ppt", ".pptx"],
    "压缩包": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "音视频": [".mp3", ".mp4", ".wav", ".avi", ".mkv", ".flv"],
    "安装包": [".exe", ".msi"],
    "代码": [".py", ".js", ".html", ".css", ".json", ".java", ".c", ".cpp"],
}


def classify(suffix):
    """按后缀判断该扔进哪个文件夹，认不出来就归到其他"""
    suffix = suffix.lower()
    for folder, exts in RULES.items():
        if suffix in exts:
            return folder
    return "其他"


def sort_folder(target, dry_run=True):
    """整理文件夹，dry_run 为 True 时只打印不搬"""
    target = Path(target)
    if not target.is_dir():
        print(f"找不到这个文件夹: {target}")
        return 0

    moved = 0
    for item in sorted(target.iterdir()):
        if item.is_dir():
            continue

        folder = classify(item.suffix)
        dest_dir = target / folder
        if not dry_run:
            dest_dir.mkdir(exist_ok=True)

        dest = dest_dir / item.name
        n = 1
        while dest.exists():
            dest = dest_dir / f"{item.stem}_{n}{item.suffix}"
            n += 1

        print(f"{item.name}  ->  {folder}/{dest.name}")
        if not dry_run:
            shutil.move(str(item), str(dest))
        moved += 1

    return moved


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    target = args[0] if args else str(Path.home() / "Downloads")
    dry_run = "--go" not in sys.argv

    print(f"目标文件夹: {target}")
    print("试运行模式，只列出来不动文件" if dry_run else "正式执行，开始搬文件")
    print("-" * 40)

    count = sort_folder(target, dry_run=dry_run)

    print("-" * 40)
    print(f"一共处理了 {count} 个文件")
    if dry_run and count:
        print("确认没问题就加上 --go 再跑一次，例如")
        print(f'  python sort_files.py "{target}" --go')


if __name__ == "__main__":
    main()
