# PDF Locker

PDFファイルにパスワード保護を追加するローカルツールです。

## 🎯 70代の方でも使える、シンプル版にアップデート！

このツールは**シニア世代の方でも安心して使える**ように設計されています。

### 🆕 NEW! Office文書も直接対応

**Word、Excel、PowerPointファイルも直接投げ込めます！**

- 📝 Word文書 (.docx)
- 📊 Excel表 (.xlsx)
- 📽️ PowerPoint資料 (.pptx)
- 📄 PDFファイル (.pdf)

→ すべて自動的にPDFに変換して鍵をかけます

### 主な改善点

- ✅ **3ステップのウィザード形式**：何をすればいいか迷わない
- ✅ **大きなボタンと文字**：読みやすく、押しやすい（16pt～24pt）
- ✅ **保存先は自動**：デスクトップの「パスワード付きPDF」フォルダに自動保存
- ✅ **パスワード表示機能**：確認入力不要、チェックを入れれば見える
- ✅ **優しい日本語**：専門用語なし、分かりやすい言葉だけ
- ✅ **Office文書対応**：Word/Excel/PowerPointも直接処理可能
- ✅ **詳しい手引き書付き**：「使い方ガイド.md」を参照

## 特徴

- **AES-256暗号化**: 業界標準の強力な暗号化方式
- **完全ローカル**: ファイルを外部サーバーに送信しません
- **シンプルなGUI**: 3ステップで誰でも使える
- **Office文書対応**: Word/Excel/PowerPointを自動でPDF化
- **複数ファイル対応**: 一度に複数のファイルを処理可能
- **exe化対応**: Pythonがないパソコンでも実行可能

## 必要環境

### 開発環境（ビルド用）
- Python 3.8以上
- pypdf[crypto]
- pyinstaller

### 実行環境
- **exe版**: Windows 10/11（Python不要）
- **app版**: macOS 10.14以上（Python不要）

## セットアップ

### 1. 開発環境の準備

```bash
# リポジトリをクローン（または展開）
cd pdf_pwd_rocker

# 仮想環境を作成（推奨）
python -m venv venv

# 仮想環境を有効化
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 依存パッケージをインストール
pip install -r requirements.txt
```

### 2. 動作確認

```bash
# Pythonから直接実行
python pdf_locker.py
```

### 3. exe/appファイルの生成

```bash
# ビルドスクリプトを使用（推奨）
python build.py

# または、シンプルなコマンドで
python build.py --simple

# ビルド成果物のクリーンアップ
python build.py --clean
```

生成されたファイルは `dist/` ディレクトリに作成されます：
- Windows: `dist/PDF_Locker.exe`
- macOS: `dist/PDF_Locker.app`

## 使い方

1. **PDF Lockerを起動**
   - exe版: `PDF_Locker.exe` をダブルクリック
   - Python版: `python pdf_locker.py`

2. **PDFファイルを選択**
   - 「ファイルを選択」ボタンをクリック
   - 複数ファイルの選択も可能

3. **パスワードを設定**
   - 「パスワードを設定」ボタンをクリック
   - パスワードを入力（確認のため2回入力）

4. **保存先を選択**
   - 保存先フォルダを選択（キャンセルで元のフォルダに保存）
   - ファイル名は `locked_元のファイル名.pdf` として保存

## 配布方法

1. `dist/PDF_Locker.exe` をUSBメモリやネットワーク共有でコピー
2. 配布先のPCでダブルクリックして実行

## 注意事項

### ウイルス対策ソフトの誤検知

PyInstallerで作成したexeファイルは、デジタル署名がないため、セキュリティソフトが「不明なファイル」として警告する場合があります。

**🚨 重要: 誤検知対策ガイドを用意しました！**

このプロジェクトには、ウイルス対策ソフトの誤検知を大幅に削減するための包括的なガイドが含まれています：

📘 **[ANTIVIRUS_FALSE_POSITIVE_SOLUTIONS.md](./ANTIVIRUS_FALSE_POSITIVE_SOLUTIONS.md)**
- コード署名の取得方法（EV証明書 vs 標準証明書）
- PyInstallerのビルドオプション最適化
- 代替パッケージング手法（Nuitka、cx_Freeze）
- VirusTotalへの事前提出と誤検知報告
- インストーラー形式の採用（Inno Setup、NSIS、MSI）
- 病院環境での実用性を考慮した優先順位付き推奨事項

📋 **[IMPLEMENTATION_CHECKLIST.md](./IMPLEMENTATION_CHECKLIST.md)**
- 段階的な実装チェックリスト
- コスト・効果の記録
- Before/After の比較

**推奨される対策（効果順）:**
1. **最適化ビルド（無料）**: `python build.py --optimized` で誤検知率を30〜50%削減
2. **コード署名（$50〜$400/年）**: デジタル署名で信頼性向上、誤検知率を70〜85%削減
3. **インストーラー作成（無料）**: Inno Setupで標準的なインストーラー形式に
4. **誤検知報告（無料）**: Microsoft Defenderなどに誤検知を報告

**病院環境での推奨構成:**
- 標準コード署名証明書（$215/年）+ Inno Setupインストーラー
- 大規模展開の場合はEV証明書（$280〜$400/年）を強く推奨

詳細は上記のドキュメントをご覧ください。

### ファイルサイズ

exeファイルには、Pythonランタイムとライブラリが含まれるため、20〜40MB程度のサイズになります。

### 起動時間

初回起動時は内部ファイルの展開のため、数秒〜十数秒かかる場合があります。

## 技術仕様

| 項目 | 内容 |
|------|------|
| 暗号化方式 | AES-256 |
| PDFライブラリ | pypdf |
| GUIフレームワーク | tkinter（Python標準） |
| パッケージング | PyInstaller |

## トラブルシューティング

### 「cryptography」関連のエラー

AES-256暗号化には `cryptography` ライブラリが必要です：

```bash
pip install pypdf[crypto]
```

### exeが起動しない

1. ウイルス対策ソフトの除外設定を確認
2. 管理者として実行を試す
3. 別のフォルダにコピーして実行

### パスワード設定済みPDFを処理できない

既にパスワードが設定されているPDFは処理できません。
先にパスワードを解除してから再度お試しください。

## ライセンス

MIT License

## 更新履歴

- v1.0.0 - 初回リリース
  - 基本的なPDFパスワード設定機能
  - 複数ファイル対応
  - AES-256暗号化
