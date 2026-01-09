# ウイルス対策ソフト誤検知対策 - 実装チェックリスト

このチェックリストを使用して、段階的に誤検知対策を実装してください。

## 📋 準備段階

- [ ] `ANTIVIRUS_FALSE_POSITIVE_SOLUTIONS.md` を読んで、全体像を把握
- [ ] 病院のIT部門に事前相談（配布許可の確認）
- [ ] 現在使用しているウイルス対策ソフトを確認
- [ ] 配布予定のユーザー数を確認（コスト見積もりのため）

---

## 🚀 フェーズ1: 即座に実装可能（無料、1日以内）

### ビルドオプションの最適化

- [ ] `build.py` を最新版に更新（このリポジトリに含まれる）
- [ ] 最適化ビルドを実行:
  ```bash
  python build.py --optimized
  ```
- [ ] ビルド成果物を確認: `dist/PDF_Locker/` フォルダ

### VirusTotalでの検証

- [ ] https://www.virustotal.com にアクセス
- [ ] `dist/PDF_Locker/PDF_Locker.exe` をアップロード
- [ ] 検出結果のURLを保存（IT部門への説明資料として使用）
- [ ] 検出数を記録: _____ / 60

### 誤検知報告

- [ ] **Microsoft Defender（最優先）**
  - [ ] https://www.microsoft.com/en-us/wdsi/filesubmission にアクセス
  - [ ] 「File」を選択
  - [ ] exeファイルをアップロード
  - [ ] 「I believe this file does not contain a threat」を選択
  - [ ] 理由を記載（例: "This is a legitimate PDF password protection tool"）
  - [ ] 送信後、24〜48時間待機

- [ ] **Norton/Symantec**（使用している場合）
  - [ ] https://submit.symantec.com/false_positive/ で報告

- [ ] **McAfee**（使用している場合）
  - [ ] https://www.mcafee.com/enterprise/en-us/threat-center/false-positive.html で報告

- [ ] **その他のベンダー**（病院で使用しているもの）
  - [ ] ベンダー名: _______________
  - [ ] 報告URL: _______________

### IT部門への事前説明

- [ ] 説明資料を準備:
  - [ ] アプリケーション概要
  - [ ] VirusTotalの結果（URLを含む）
  - [ ] ソースコードの提供意思
  - [ ] 使用するライブラリのリスト（pypdf、tkinter、cryptography）

- [ ] IT部門にメールまたは面談で説明
- [ ] フィードバックを記録: _______________

### 結果の確認

- [ ] 最適化前の検出数: _____ / 60
- [ ] 最適化後の検出数: _____ / 60
- [ ] 改善率: _____%

**この段階での目標: 検出数を30〜50%削減**

---

## 📊 フェーズ2: 短期的な改善（$50〜$300、1〜2週間）

### コード署名証明書の取得

- [ ] 予算の確保: $_____ （標準証明書: $50〜$216/年）
- [ ] プロバイダーの選定:
  - [ ] Sectigo（推奨、$215.99/年）
  - [ ] DigiCert
  - [ ] その他: _______________

- [ ] 証明書の申請:
  - [ ] 組織情報の準備（法人登記情報、担当者情報）
  - [ ] 申請フォームの記入
  - [ ] 身元確認書類の提出
  - [ ] 電話/メール確認の対応

- [ ] 証明書の受領:
  - [ ] .pfxファイルをダウンロード
  - [ ] パスワードを安全に保管
  - [ ] バックアップを作成

### Windows SDKのインストール（SignTool用）

- [ ] Windows SDKのダウンロード:
  - [ ] https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/
  - [ ] インストール時に「Windows SDK Signing Tools for Desktop Apps」を選択

- [ ] SignToolの動作確認:
  ```bash
  where signtool
  ```

### exeファイルへの署名

- [ ] 環境変数の設定（推奨）:
  ```bash
  set CODE_SIGN_CERT=証明書のパス.pfx
  set CODE_SIGN_PASSWORD=パスワード
  ```

- [ ] 署名ヘルパースクリプトの使用:
  ```bash
  python sign_executable.py --file dist/PDF_Locker/PDF_Locker.exe
  ```

- [ ] 署名の検証:
  ```bash
  python sign_executable.py --verify dist/PDF_Locker/PDF_Locker.exe
  ```

- [ ] Windowsエクスプローラーで確認:
  - [ ] exeファイルを右クリック → プロパティ → デジタル署名タブ
  - [ ] 署名が表示されることを確認

### インストーラーの作成（Inno Setup）

- [ ] Inno Setupのダウンロードとインストール:
  - [ ] https://jrsoftware.org/isinfo.php

- [ ] `installer_setup.iss` ファイルの編集:
  - [ ] `AppPublisher`を病院名に変更
  - [ ] URLを実際のものに変更（または削除）
  - [ ] コード署名の設定（SignTool行のコメントを外す）

- [ ] インストーラーのビルド:
  - [ ] Inno Setup Compilerで `installer_setup.iss` を開く
  - [ ] Build > Compile を実行
  - [ ] `installer_output/PDF_Locker_Setup.exe` が生成されることを確認

- [ ] インストーラーへの署名:
  ```bash
  python sign_executable.py --file installer_output/PDF_Locker_Setup.exe
  ```

### 再度VirusTotalで検証

- [ ] インストーラーをVirusTotalにアップロード
- [ ] 検出数を記録: _____ / 60
- [ ] 改善率を計算: _____%

### IT部門への正式申請

- [ ] 申請書類を準備:
  - [ ] 署名付きインストーラー
  - [ ] VirusTotalの結果（更新版）
  - [ ] 証明書情報（発行元、有効期限）
  - [ ] インストール手順書
  - [ ] アンインストール手順書

- [ ] 申請を提出
- [ ] 承認結果: _______________
- [ ] 承認日: _______________

**この段階での目標: 検出数を70〜85%削減、IT部門の承認取得**

---

## 🏆 フェーズ3: 中期的な最適化（$280〜$400、1ヶ月）

### EV証明書の検討

- [ ] 以下のいずれかに該当する場合、EV証明書を検討:
  - [ ] 100ユーザー以上に配布予定
  - [ ] SmartScreenの警告を完全に排除したい
  - [ ] 標準証明書でも誤検知が多い
  - [ ] 病院の複数部署で使用予定

- [ ] EV証明書の申請:
  - [ ] 予算の確保: $280〜$400/年
  - [ ] より厳格な組織検証の準備
  - [ ] ハードウェアトークン（USBキー）の購入

- [ ] EV証明書での署名:
  - [ ] ハードウェアトークンを使用して署名
  - [ ] SmartScreenテスト（警告が出ないことを確認）

### Nuitkaへの移行（必要に応じて）

- [ ] PyInstallerで誤検知が残る場合のみ検討
- [ ] Nuitkaのインストール:
  ```bash
  pip install nuitka
  ```

- [ ] ビルドテスト:
  ```bash
  python -m nuitka --standalone --onefile --windows-disable-console \
      --enable-plugin=tk-inter \
      --company-name="病院名" \
      --product-name="PDF Locker" \
      --file-version=1.0.0.0 \
      pdf_locker.py
  ```

- [ ] VirusTotalで比較:
  - [ ] PyInstaller版: _____ / 60
  - [ ] Nuitka版: _____ / 60
  - [ ] どちらを採用: _______________

### MSIインストーラーの作成（大規模展開の場合）

- [ ] WiX Toolsetのインストール:
  - [ ] https://wixtoolset.org/

- [ ] MSIインストーラーのビルド
- [ ] Active Directory GPOでの配布テスト

**この段階での目標: 検出数を95〜100%削減、完全なIT承認**

---

## 🔧 フェーズ4: 高度な最適化（必要に応じて）

### カスタムブートローダーのビルド

- [ ] 他の対策で不十分な場合のみ実施
- [ ] Visual Studio 2019以降のインストール（C++ワークロード）
- [ ] PyInstallerソースのクローン:
  ```bash
  git clone https://github.com/pyinstaller/pyinstaller.git
  cd pyinstaller/bootloader
  python ./waf all --target-arch=64bit
  cd ..
  pip install .
  ```

- [ ] カスタムブートローダーでのビルド
- [ ] VirusTotalで検証

---

## 📝 配布準備

### ドキュメントの作成

- [ ] エンドユーザー向け使い方ガイド（`使い方ガイド.md`を更新）
- [ ] IT管理者向けインストール手順書
- [ ] トラブルシューティングガイド

### テスト環境での検証

- [ ] IT部門の検証用PCでテスト
- [ ] ウイルス対策ソフトのリアルタイム保護を有効化してテスト
- [ ] 実際の業務フローでの動作確認

### 配布方法の決定

- [ ] **小規模（〜20ユーザー）**: USBメモリ + 署名付きインストーラー
- [ ] **中規模（20〜100ユーザー）**: ネットワーク共有 + Inno Setupインストーラー
- [ ] **大規模（100ユーザー以上）**: Active Directory GPO + MSIインストーラー

### 最終確認

- [ ] すべての署名が有効か確認
- [ ] VirusTotalで最終検証: _____ / 60
- [ ] IT部門の最終承認: _______________
- [ ] 配布開始日: _______________

---

## 📊 成果の記録

### Before & After

| 項目 | 最適化前 | 最適化後 | 改善率 |
|------|---------|---------|--------|
| VirusTotal検出数 | ___/60 | ___/60 | ___% |
| Windows Defender | 検出される/されない | 検出される/されない | - |
| IT部門の承認 | 未承認/承認済み | 未承認/承認済み | - |
| SmartScreen警告 | あり/なし | あり/なし | - |

### コスト

| 項目 | 金額 |
|------|------|
| コード署名証明書（年間） | $_____ |
| その他のツール | $_____ |
| 作業時間 | ___時間 |
| **合計** | **$_____** |

### ROI（投資対効果）

- [ ] 配布ユーザー数: _____ 人
- [ ] IT承認にかかった時間: _____ 日（最適化前） → _____ 日（最適化後）
- [ ] ユーザーサポート問い合わせ: _____ 件（最適化前） → _____ 件（最適化後）

---

## 🎓 学んだこと・備考

### うまくいったこと

1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

### 課題・改善点

1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

### 次回への引き継ぎ事項

- 証明書の有効期限: _______________（更新忘れに注意）
- IT部門の担当者: _______________
- 配布用ネットワークパス: _______________
- その他: _______________________________________________

---

## ✅ 完了！

すべてのチェックリストを完了したら、このファイルを保存して、次回のアップデート時に参照してください。

**おめでとうございます！ウイルス対策ソフトの誤検知対策が完了しました。**

---

**参考資料:**
- [ANTIVIRUS_FALSE_POSITIVE_SOLUTIONS.md](./ANTIVIRUS_FALSE_POSITIVE_SOLUTIONS.md) - 詳細な技術解説
- [README.md](./README.md) - プロジェクト全体の説明
- [使い方ガイド.md](./使い方ガイド.md) - エンドユーザー向けガイド

**最終更新:** 2026年1月
