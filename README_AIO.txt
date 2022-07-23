This is a generic AIO FW update package

Automated FW install function.
Just plug prepared SD card into unit.

PLEASE NOTE: Start of automatic FW update can take up to 1-2 minutes after plugging SD card in.

Manual:


All-In-One features:
- Automatic starting FW update after plugging in SD
- Patched IFS-Root (FEC & CP patch) will be used during the installation.
- FecContainer will be adjusted with missing FECs during the installation including code for latest maps (073000EE).
  - addFecs.txt in /common/tools/ can be adjusted as needed. Change add FECS with e.g. notepad.
- CarPlay and AndroidAuto will be enabled during the installation.
- Developer Mode with GEM (hidden Green Engineering Menu) will be enabled during the installation. No need for OBDeleven, VCDS, VCP.
- WLAN will be enabled - required for e.g.  Porsche Track Precision App
- Navigation will be enabled
- Basic backup will be run during installation before any chnages to units coding is applied
- M.I.B. - More Incredible Bash will be enabled to run from SD
- M.I.B. AIO version - with reduced functions - will be available directly from FW SD card
  - SVM fix, Backup functions, some basic cosing checks

Version: 202YMMDD