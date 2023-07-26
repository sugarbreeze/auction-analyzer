; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "24au helper"
#define MyAppVersion "1.10"
#define MyAppPublisher "Labirynth apps"
#define MyAppURL "http://labirynthapps.github.io/products/"
#define MyAppExeName "24au helper.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{036355D8-A46E-4C6D-A678-A97CC01D06E5}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={pf}\{#MyAppName}
DefaultGroupName={#MyAppName}
LicenseFile=C:\24au\Licension.txt
InfoBeforeFile=C:\24au\dist.txt
OutputDir=C:\Users\admin\Desktop
OutputBaseFilename=24au helper setup
SetupIconFile=C:\24au\icon.ico
Compression=lzma
SolidCompression=yes

[Languages]
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: startupicon; Description: "��������� ��� ������ Windows"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\24au\dist\24au helper.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\24au\dist\_ctypes.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\24au\dist\_hashlib.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\24au\dist\_socket.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\24au\dist\_ssl.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\24au\dist\_tkinter.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\24au\dist\api-ms-win-core-delayload-l1-1-1.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\24au\dist\api-ms-win-core-errorhandling-l1-1-1.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\24au\dist\api-ms-win-core-handle-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\24au\dist\api-ms-win-core-heap-l1-2-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\24au\dist\api-ms-win-core-heap-obsolete-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\24au\dist\api-ms-win-core-libraryloader-l1-2-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\24au\dist\api-ms-win-core-localization-obsolete-l1-2-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\24au\dist\api-ms-win-core-processthreads-l1-1-2.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\24au\dist\api-ms-win-core-profile-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\24au\dist\api-ms-win-core-registry-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\24au\dist\api-ms-win-core-string-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\24au\dist\api-ms-win-core-string-obsolete-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\24au\dist\api-ms-win-core-synch-l1-2-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\24au\dist\api-ms-win-core-sysinfo-l1-2-1.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\24au\dist\api-ms-win-security-base-l1-2-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\24au\dist\bz2.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\24au\dist\CRYPT32.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\24au\dist\favicon.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\24au\dist\libcurl.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\24au\dist\library.zip"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\24au\dist\lxml.etree.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\24au\dist\pycurl.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\24au\dist\python27.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\24au\dist\select.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\24au\dist\tcl85.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\24au\dist\tk85.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\24au\dist\unicodedata.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\24au\dist\w9xpopen.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\24au\dist\WLDAP32.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\24au\dist\1\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,24au helper}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userstartup}\24au helper"; Filename: "{app}\24au.exe"; Tasks: startupicon

[Run]

