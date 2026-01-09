; PDF Locker - Inno Setup インストーラー設定ファイル
;
; このファイルを使用して、PDF Lockerのインストーラーを作成できます。
; Inno Setupをダウンロード: https://jrsoftware.org/isinfo.php
;
; 使い方:
;   1. Inno Setupをインストール
;   2. このファイルを開く（Inno Setup Compilerで）
;   3. Build > Compile を実行
;   4. Output フォルダに PDF_Locker_Setup.exe が生成される
;
; コード署名を使用する場合:
;   1. 下記の [Setup] セクションの SignTool の行のコメントを外す
;   2. 証明書のパスとパスワードを設定
;   3. コンパイル時に自動的に署名される

[Setup]
; アプリケーション情報
AppName=PDF Locker
AppVersion=1.0.0
AppPublisher=病院名（変更してください）
AppPublisherURL=https://your-hospital.example.com
AppSupportURL=https://your-hospital.example.com/support
AppUpdatesURL=https://your-hospital.example.com/updates

; インストール設定
DefaultDirName={autopf}\PDF_Locker
DefaultGroupName=PDF Locker
AllowNoIcons=yes
LicenseFile=LICENSE
InfoBeforeFile=README.md
OutputDir=installer_output
OutputBaseFilename=PDF_Locker_Setup
SetupIconFile=icon.ico
Compression=lzma2
SolidCompression=yes
WizardStyle=modern

; 特権設定
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

; アーキテクチャ
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

; アンインストール設定
UninstallDisplayIcon={app}\PDF_Locker.exe

; コード署名（証明書がある場合にコメントを外す）
; SignTool=signtool sign /f "証明書のパス.pfx" /p "パスワード" /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 $f
; SignedUninstaller=yes

[Languages]
Name: "japanese"; MessagesFile: "compiler:Languages\Japanese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
; --onedir モードでビルドした場合
Source: "dist\PDF_Locker\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; --onefile モードでビルドした場合は以下を使用（上記をコメントアウト）
; Source: "dist\PDF_Locker.exe"; DestDir: "{app}"; Flags: ignoreversion

; 追加のリソースファイル（必要に応じて）
; Source: "使い方ガイド.md"; DestDir: "{app}"; Flags: ignoreversion
; Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion isreadme

[Icons]
Name: "{group}\PDF Locker"; Filename: "{app}\PDF_Locker.exe"
Name: "{group}\{cm:UninstallProgram,PDF Locker}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\PDF Locker"; Filename: "{app}\PDF_Locker.exe"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\PDF Locker"; Filename: "{app}\PDF_Locker.exe"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\PDF_Locker.exe"; Description: "{cm:LaunchProgram,PDF Locker}"; Flags: nowait postinstall skipifsilent

[Code]
// カスタム初期化コード
function InitializeSetup(): Boolean;
begin
  Result := True;
  // ここに初期化コードを追加可能
end;

// 既存のバージョンチェック（必要に応じて）
function InitializeUninstall(): Boolean;
begin
  Result := True;
  MsgBox('PDF Lockerをアンインストールします。', mbInformation, MB_OK);
end;

[Messages]
; カスタムメッセージ（日本語）
WelcomeLabel1=PDF Locker セットアップウィザードへようこそ
WelcomeLabel2=このウィザードは、PDF Lockerをこのコンピューターにインストールします。%n%nセットアップを続ける前に、他のアプリケーションをすべて終了することをお勧めします。%n%n続行するには [次へ] をクリックしてください。
