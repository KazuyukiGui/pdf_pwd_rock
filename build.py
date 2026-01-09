#!/usr/bin/env python3
"""
PDF Locker ビルドスクリプト

PyInstallerを使用してexeファイルを生成します。

Usage:
    python build.py            # specファイルを使用してビルド
    python build.py --simple   # シンプルなコマンドでビルド（onefile）
    python build.py --optimized # 最適化ビルド（誤検知を減らす・推奨）
    python build.py --clean    # ビルド成果物をクリーンアップ

推奨:
    病院環境や企業環境での配布の場合は --optimized を使用してください。
    ウイルス対策ソフトの誤検知率を大幅に削減します。
    詳細は ANTIVIRUS_FALSE_POSITIVE_SOLUTIONS.md を参照してください。
"""

import subprocess
import sys
import shutil
from pathlib import Path


def clean_build_artifacts():
    """ビルド成果物をクリーンアップ"""
    dirs_to_remove = ['build', 'dist', '__pycache__']
    files_to_remove = ['*.pyc', '*.pyo']

    project_root = Path(__file__).parent

    for dir_name in dirs_to_remove:
        dir_path = project_root / dir_name
        if dir_path.exists():
            print(f"Removing {dir_path}...")
            shutil.rmtree(dir_path)

    # .pycファイルを削除
    for pattern in files_to_remove:
        for file in project_root.rglob(pattern):
            print(f"Removing {file}...")
            file.unlink()

    print("Clean completed!")


def check_dependencies():
    """依存パッケージをチェック"""
    try:
        import pypdf
        print(f"pypdf version: {pypdf.__version__}")
    except ImportError:
        print("Error: pypdf is not installed.")
        print("Run: pip install pypdf[crypto]")
        return False

    try:
        import tkinterdnd2
        print(f"tkinterdnd2 version: {tkinterdnd2.__version__}")
    except ImportError:
        print("Warning: tkinterdnd2 is not installed.")
        print("Drag & drop will be disabled.")
        print("To enable, run: pip install tkinterdnd2")

    try:
        import PyInstaller
        print(f"PyInstaller version: {PyInstaller.__version__}")
    except ImportError:
        print("Error: PyInstaller is not installed.")
        print("Run: pip install pyinstaller")
        return False

    return True


def build_with_spec():
    """specファイルを使用してビルド"""
    print("Building with spec file...")
    result = subprocess.run(
        [sys.executable, "-m", "PyInstaller", "pdf_locker.spec", "--clean"],
        check=True
    )
    return result.returncode == 0


def build_simple():
    """シンプルなコマンドでビルド"""
    print("Building with simple command...")
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "PDF_Locker",
        "--clean",
        # 不要なモジュールを除外
        "--exclude-module", "matplotlib",
        "--exclude-module", "numpy",
        "--exclude-module", "pandas",
        "--exclude-module", "scipy",
        "--exclude-module", "PIL",
        # tkinterdnd2を含める（データとバイナリ両方）
        "--collect-all", "tkinterdnd2",
        "--collect-data", "tkinterdnd2",
        # 隠しインポート
        "--hidden-import", "tkinterdnd2",
        "--hidden-import", "tkinterdnd2.TkinterDnD",
        "pdf_locker.py"
    ]
    result = subprocess.run(cmd, check=True)
    return result.returncode == 0


def build_optimized():
    """
    ウイルス対策ソフトの誤検知を最小限にする最適化ビルド

    以下の最適化を実施:
    - --onedirモード（--onefileより誤検知率が低い）
    - --noupx（UPX圧縮を無効化、誤検知の主要因を排除）
    - 不要なモジュールの徹底的な除外

    詳細: ANTIVIRUS_FALSE_POSITIVE_SOLUTIONS.md を参照
    """
    print("Building with optimized settings (reduced false-positive rate)...")
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onedir",  # onefile より誤検知率が低い
        "--windowed",
        "--name", "PDF_Locker",
        "--noupx",  # UPXを無効化（重要：誤検知の主要因）
        "--clean",
        "--noconfirm",

        # 不要なモジュールを除外（ファイルサイズ削減と誤検知低減）
        "--exclude-module", "matplotlib",
        "--exclude-module", "numpy",
        "--exclude-module", "pandas",
        "--exclude-module", "scipy",
        "--exclude-module", "PIL",
        "--exclude-module", "IPython",
        "--exclude-module", "notebook",
        "--exclude-module", "jupyter",
        "--exclude-module", "pytest",
        "--exclude-module", "unittest",
        "--exclude-module", "test",

        # 必要なモジュールのみ含める
        "--collect-all", "tkinterdnd2",
        "--collect-data", "tkinterdnd2",
        "--hidden-import", "tkinterdnd2",
        "--hidden-import", "tkinterdnd2.TkinterDnD",
        "--hidden-import", "pypdf",
        "--hidden-import", "cryptography",

        "pdf_locker.py"
    ]
    result = subprocess.run(cmd, check=True)
    return result.returncode == 0


def main():
    """メイン処理"""
    if "--clean" in sys.argv:
        clean_build_artifacts()
        return

    print("=" * 50)
    print("PDF Locker Build Script")
    print("=" * 50)

    # 依存パッケージをチェック
    if not check_dependencies():
        sys.exit(1)

    print()

    # ビルド
    try:
        if "--simple" in sys.argv:
            success = build_simple()
        elif "--optimized" in sys.argv:
            success = build_optimized()
        else:
            success = build_with_spec()

        if success:
            print()
            print("=" * 50)
            print("Build completed successfully!")
            print("=" * 50)
            print()
            if "--optimized" in sys.argv:
                print("Output location: dist/PDF_Locker/ (folder)")
                print()
                print("NOTE: This is a folder-based build (--onedir)")
                print("      to reduce antivirus false-positive rate.")
                print()
                print("To distribute:")
                print("  1. Copy the entire 'dist/PDF_Locker' folder")
                print("  2. Run PDF_Locker.exe inside the folder")
                print()
                print("For easier distribution, consider:")
                print("  - Creating an installer (Inno Setup, NSIS)")
                print("  - Code signing the executable")
                print()
                print("See ANTIVIRUS_FALSE_POSITIVE_SOLUTIONS.md for details.")
            else:
                print("Output location: dist/PDF_Locker.exe (Windows)")
                print("                 dist/PDF_Locker.app (macOS)")
                print("                 dist/PDF_Locker (Linux)")
                print()
                print("You can copy this file to any PC and run it.")

    except subprocess.CalledProcessError as e:
        print(f"Build failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
