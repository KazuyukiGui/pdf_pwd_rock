#!/usr/bin/env python3
"""
コード署名ヘルパースクリプト

このスクリプトは、ビルドされたexeファイルにデジタル署名を追加します。

前提条件:
- Windows SDKがインストールされている（SignToolが含まれる）
- コード署名証明書（.pfxファイル）を取得済み

使い方:
    python sign_executable.py --cert 証明書.pfx --password パスワード --file dist/PDF_Locker.exe
    python sign_executable.py --cert 証明書.pfx --password パスワード --file installer_output/PDF_Locker_Setup.exe
    python sign_executable.py --verify dist/PDF_Locker.exe  # 署名の検証

環境変数を使用する場合:
    set CODE_SIGN_CERT=証明書.pfx
    set CODE_SIGN_PASSWORD=パスワード
    python sign_executable.py --file dist/PDF_Locker.exe

詳細: ANTIVIRUS_FALSE_POSITIVE_SOLUTIONS.md を参照
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def find_signtool():
    """SignToolの実行ファイルパスを検索"""
    # 一般的なWindows SDKのインストールパス
    sdk_paths = [
        r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.22621.0\x64",
        r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.22000.0\x64",
        r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.19041.0\x64",
        r"C:\Program Files (x86)\Windows Kits\10\App Certification Kit",
    ]

    # パス環境変数から検索
    signtool_in_path = subprocess.run(
        ["where", "signtool"],
        capture_output=True,
        text=True
    )
    if signtool_in_path.returncode == 0:
        return "signtool"

    # 既知のパスから検索
    for sdk_path in sdk_paths:
        signtool_path = Path(sdk_path) / "signtool.exe"
        if signtool_path.exists():
            return str(signtool_path)

    return None


def sign_file(cert_path: str, password: str, file_path: str, timestamp_url: str = "http://timestamp.digicert.com"):
    """
    ファイルにデジタル署名を追加

    Args:
        cert_path: 証明書ファイル（.pfx）のパス
        password: 証明書のパスワード
        file_path: 署名するファイルのパス
        timestamp_url: タイムスタンプサーバーのURL
    """
    signtool = find_signtool()
    if not signtool:
        print("エラー: SignToolが見つかりません。")
        print()
        print("Windows SDKをインストールしてください:")
        print("https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/")
        return False

    # 証明書ファイルの存在確認
    if not Path(cert_path).exists():
        print(f"エラー: 証明書ファイルが見つかりません: {cert_path}")
        return False

    # 署名するファイルの存在確認
    if not Path(file_path).exists():
        print(f"エラー: 署名するファイルが見つかりません: {file_path}")
        return False

    print(f"SignTool: {signtool}")
    print(f"証明書: {cert_path}")
    print(f"ファイル: {file_path}")
    print(f"タイムスタンプサーバー: {timestamp_url}")
    print()
    print("署名中...")

    # 署名コマンド
    cmd = [
        signtool,
        "sign",
        "/f", cert_path,
        "/p", password,
        "/fd", "SHA256",
        "/tr", timestamp_url,
        "/td", "SHA256",
        "/v",  # 詳細出力
        file_path
    ]

    try:
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        print()
        print("✅ 署名が完了しました！")
        return True

    except subprocess.CalledProcessError as e:
        print("❌ 署名に失敗しました:")
        print(e.stderr)
        return False


def verify_signature(file_path: str):
    """
    ファイルの署名を検証

    Args:
        file_path: 検証するファイルのパス
    """
    signtool = find_signtool()
    if not signtool:
        print("エラー: SignToolが見つかりません。")
        return False

    # ファイルの存在確認
    if not Path(file_path).exists():
        print(f"エラー: ファイルが見つかりません: {file_path}")
        return False

    print(f"ファイル: {file_path}")
    print()
    print("署名を検証中...")

    # 検証コマンド
    cmd = [
        signtool,
        "verify",
        "/pa",  # デフォルトの認証ポリシーを使用
        "/v",   # 詳細出力
        file_path
    ]

    try:
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        print()
        print("✅ 署名は有効です！")
        return True

    except subprocess.CalledProcessError as e:
        print("❌ 署名の検証に失敗しました:")
        print(e.stderr)
        print()
        print("注意: ファイルが署名されていないか、署名が無効です。")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="PDF Locker コード署名ヘルパー",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # exeファイルに署名
  python sign_executable.py --cert cert.pfx --password mypass --file dist/PDF_Locker.exe

  # インストーラーに署名
  python sign_executable.py --cert cert.pfx --password mypass --file installer_output/PDF_Locker_Setup.exe

  # 署名の検証
  python sign_executable.py --verify dist/PDF_Locker.exe

  # 環境変数を使用
  set CODE_SIGN_CERT=cert.pfx
  set CODE_SIGN_PASSWORD=mypass
  python sign_executable.py --file dist/PDF_Locker.exe

詳細は ANTIVIRUS_FALSE_POSITIVE_SOLUTIONS.md を参照してください。
        """
    )

    parser.add_argument(
        "--cert",
        help="証明書ファイル（.pfx）のパス（環境変数 CODE_SIGN_CERT でも可）"
    )
    parser.add_argument(
        "--password",
        help="証明書のパスワード（環境変数 CODE_SIGN_PASSWORD でも可）"
    )
    parser.add_argument(
        "--file",
        required=True,
        help="署名または検証するファイルのパス"
    )
    parser.add_argument(
        "--timestamp",
        default="http://timestamp.digicert.com",
        help="タイムスタンプサーバーのURL（デフォルト: DigiCert）"
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="署名の検証のみを行う"
    )

    args = parser.parse_args()

    # プラットフォームチェック
    if sys.platform != "win32":
        print("警告: このスクリプトはWindows専用です。")
        print("macOSの場合は codesign コマンドを使用してください。")
        return

    # 検証モード
    if args.verify:
        success = verify_signature(args.file)
        sys.exit(0 if success else 1)

    # 署名モード
    cert_path = args.cert or os.environ.get("CODE_SIGN_CERT")
    password = args.password or os.environ.get("CODE_SIGN_PASSWORD")

    if not cert_path:
        print("エラー: 証明書ファイルを指定してください。")
        print("  --cert オプション または CODE_SIGN_CERT 環境変数")
        sys.exit(1)

    if not password:
        print("エラー: 証明書のパスワードを指定してください。")
        print("  --password オプション または CODE_SIGN_PASSWORD 環境変数")
        print()
        print("セキュリティ上の理由から、環境変数の使用を推奨します:")
        print("  set CODE_SIGN_PASSWORD=your_password")
        sys.exit(1)

    success = sign_file(cert_path, password, args.file, args.timestamp)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
