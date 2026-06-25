[Setup]
AppId={{A9E82C23-E78A-4B6A-91FF-D9EEB3A123FE}
AppName=Amethyst Engine
AppVersion=1.4.0
AppPublisher=JackTheDemon355 Dev Group
DefaultDirName={autopf}\Amethyst Engine
DefaultGroupName=Amethyst Engine
AllowNoIcons=yes
OutputDir=.
OutputBaseFilename=AmethystEngine_CoreSetup
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: ".\dist\amethyst_engine.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: ".\Minecraftia-Regular.ttf"; DestDir: "{autofonts}"; FontInstall: "Minecraftia"; Flags: onlyifdoesntexist uninsneveruninstall

[Icons]
Name: "{group}\Amethyst Engine"; Filename: "{app}\amethyst_engine.exe"
Name: "{autodesktop}\Amethyst Engine"; Filename: "{app}\amethyst_engine.exe"; Tasks: desktopicon

[Run]
Description: "{cm:LaunchProgram,Amethyst Engine}"; Filename: "{app}\amethyst_engine.exe"; Flags: nowait postinstall skipifsilent
