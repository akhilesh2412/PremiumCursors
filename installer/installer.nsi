; Pro Premium Cursors — Professional Installer (NSIS)
; Installs the full 17-cursor scheme to C:\Windows\Cursors\ProPremium,
; registers it under Control Panel schemes AND applies it immediately.
Unicode True
SetCompressor /SOLID lzma

!include "MUI2.nsh"

Name "Pro Premium Cursors"
OutFile "PremiumCursors-Setup.exe"
InstallDir "$WINDIR\Cursors\ProPremium"
RequestExecutionLevel admin

VIProductVersion "1.0.0.0"
VIAddVersionKey "ProductName" "Pro Premium Cursors"
VIAddVersionKey "FileDescription" "Premium Windows cursor scheme - dark glass arrows with cyan glow, animated spinners"
VIAddVersionKey "FileVersion" "1.0.0.0"
VIAddVersionKey "ProductVersion" "1.0"

!define MUI_ICON "app.ico"
!define MUI_UNICON "app.ico"
!define MUI_ABORTWARNING
!define MUI_WELCOMEPAGE_TITLE "Pro Premium Cursors"
!define MUI_WELCOMEPAGE_TEXT "This will install the Pro Premium cursor scheme (17 cursors: sleek macOS style, glossy black pointers, white glove hand, spinning beach-ball Busy) and apply it to your PC right away.$\r$\n$\r$\nYou can switch back any time from Mouse settings -> Pointers."
!define MUI_FINISHPAGE_TEXT "Done! Your new premium cursors are live.$\r$\nMove your mouse - the new pointer is already active."

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "English"

Section "Pro Premium Cursors (required)"
  SectionIn RO
  SetOutPath "$INSTDIR"
  File "..\cursors\Arrow.cur"
  File "..\cursors\Help.cur"
  File "..\cursors\AppStarting.ani"
  File "..\cursors\Wait.ani"
  File "..\cursors\Crosshair.cur"
  File "..\cursors\IBeam.cur"
  File "..\cursors\NWPen.cur"
  File "..\cursors\No.cur"
  File "..\cursors\SizeNS.cur"
  File "..\cursors\SizeWE.cur"
  File "..\cursors\SizeNWSE.cur"
  File "..\cursors\SizeNESW.cur"
  File "..\cursors\SizeAll.cur"
  File "..\cursors\UpArrow.cur"
  File "..\cursors\Hand.cur"
  File "..\cursors\Pin.cur"
  File "..\cursors\Person.cur"

  ; Register the scheme (Mouse Properties -> Pointers dropdown)
  WriteRegStr HKCU "Control Panel\Cursors\Schemes" "macOS Style" "$INSTDIR\Arrow.cur,$INSTDIR\Help.cur,$INSTDIR\AppStarting.ani,$INSTDIR\Wait.ani,$INSTDIR\Crosshair.cur,$INSTDIR\IBeam.cur,$INSTDIR\NWPen.cur,$INSTDIR\No.cur,$INSTDIR\SizeNS.cur,$INSTDIR\SizeWE.cur,$INSTDIR\SizeNWSE.cur,$INSTDIR\SizeNESW.cur,$INSTDIR\SizeAll.cur,$INSTDIR\UpArrow.cur,$INSTDIR\Hand.cur,$INSTDIR\Pin.cur,$INSTDIR\Person.cur"

  ; Apply it NOW as the current scheme
  WriteRegStr HKCU "Control Panel\Cursors" "(default)" "macOS Style"
  WriteRegStr HKCU "Control Panel\Cursors" "Arrow" "$INSTDIR\Arrow.cur"
  WriteRegStr HKCU "Control Panel\Cursors" "Help" "$INSTDIR\Help.cur"
  WriteRegStr HKCU "Control Panel\Cursors" "AppStarting" "$INSTDIR\AppStarting.ani"
  WriteRegStr HKCU "Control Panel\Cursors" "Wait" "$INSTDIR\Wait.ani"
  WriteRegStr HKCU "Control Panel\Cursors" "Crosshair" "$INSTDIR\Crosshair.cur"
  WriteRegStr HKCU "Control Panel\Cursors" "IBeam" "$INSTDIR\IBeam.cur"
  WriteRegStr HKCU "Control Panel\Cursors" "NWPen" "$INSTDIR\NWPen.cur"
  WriteRegStr HKCU "Control Panel\Cursors" "No" "$INSTDIR\No.cur"
  WriteRegStr HKCU "Control Panel\Cursors" "SizeNS" "$INSTDIR\SizeNS.cur"
  WriteRegStr HKCU "Control Panel\Cursors" "SizeWE" "$INSTDIR\SizeWE.cur"
  WriteRegStr HKCU "Control Panel\Cursors" "SizeNWSE" "$INSTDIR\SizeNWSE.cur"
  WriteRegStr HKCU "Control Panel\Cursors" "SizeNESW" "$INSTDIR\SizeNESW.cur"
  WriteRegStr HKCU "Control Panel\Cursors" "SizeAll" "$INSTDIR\SizeAll.cur"
  WriteRegStr HKCU "Control Panel\Cursors" "UpArrow" "$INSTDIR\UpArrow.cur"
  WriteRegStr HKCU "Control Panel\Cursors" "Hand" "$INSTDIR\Hand.cur"
  WriteRegStr HKCU "Control Panel\Cursors" "Pin" "$INSTDIR\Pin.cur"
  WriteRegStr HKCU "Control Panel\Cursors" "Person" "$INSTDIR\Person.cur"
  ; Tell Windows to reload cursors immediately (SPI_SETCURSORS = 0x0057)
  System::Call 'user32::SystemParametersInfo(i 87, i 0, i 0, i 0)'

  WriteUninstaller "$INSTDIR\Uninstall-PremiumCursors.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ProPremiumCursors" "DisplayName" "Pro Premium Cursors"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ProPremiumCursors" "DisplayVersion" "1.0"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ProPremiumCursors" "Publisher" "akhilesh2412"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ProPremiumCursors" "UninstallString" '"$INSTDIR\Uninstall-PremiumCursors.exe"'
SectionEnd

Section "Uninstall"
  ; Restore Windows default scheme marker (values fall back to Aero defaults)
  DeleteRegValue HKCU "Control Panel\Cursors\Schemes" "macOS Style"
  WriteRegStr HKCU "Control Panel\Cursors" "(default)" "Windows Aero"
  System::Call 'user32::SystemParametersInfo(i 87, i 0, i 0, i 0)'
  Delete "$INSTDIR\*.cur"
  Delete "$INSTDIR\*.ani"
  Delete "$INSTDIR\Uninstall-PremiumCursors.exe"
  RMDir "$INSTDIR"
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ProPremiumCursors"
SectionEnd
