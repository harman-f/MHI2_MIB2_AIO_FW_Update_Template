# MHI2_MIB2_AIO_FW_Update_Template 

Custom **A**ll **I**n **O**ne FW update based on latest Porsche firmware available - MHI2_US_POG11_K5186 MU1476.<br />
Usable for all MHI2 US POG11 based MIB2 units

ℹ️ Custom all-in-one FW update based on metainfo2 exploit.<br />
:warning: Read full article before using this update.<br />
<br />
**Last update XX.XX.20XX**<br />

# Features
1. Based on latest `MHI2_XX_XXXXX` firmware<br />
<!-- Check if required for FW: 2. BOSE Sound System update **disabled** and removed from update<br /> -->
3. Automatic starting FW update after plugging in SD<br />
4. Patched IFS-Root (FEC, VCRN & Component Protection patch) will be used during the installation.<br />
5. FecContainer.fec will be extended with missing FECs:<br />
    * `00030000`,`00040100`, `00050000`,`00070100`, `00070200`, `00030000`, `06310099`,`00060100`,`00060500`,`00060700`,`00060800`, `00060900`, `00060A00`<br />
    * addFecs.txt in /common/tools/ can be adjusted as needed. Change add FECS with e.g. notepad.<br />
6. CarPlay and AndroidAuto will be enabled during the installation<br />
7. Developer Mode with GEM (hidden Green Engineering Menu) will be enabled during the installation<br />
    *No need for OBD tools like PIWIS to enable it.<br />
9. WLAN will be enabled - required for e.g. [Porsche Track Precision App](https://github.com/harman-f/MHI2_US_POG11_K5186_1-MU1476-AIO/edit/main/README.md#track-precision-app)<br />
<!-- Check if required for brand/model: 10. Navigation will be enabled on units which do not have it activated from factory<br />
    * All MHI2 based units - like PCM 4 - are capable to run NAvigation!
    * GPS antenna might be missing and has to be retrofitted<br />
    * Check with M.I.B in GEM if antenna is installed<br /> -->
<!-- 11. Add FW/car/model specific features<br /> -->
12. M.I.B. - More Incredible Bash will be enabled to run from SD<br />
13. [M.I.B. AIO version](https://github.com/Mr-MIBonk/M.I.B._More-Incredible-Bash) - with AIO tailored functions - will be available directly from AIO SD card
    * SVM fix, backup/restore functions, some basic coding checks and more<br />
14. Basic system backup will be run during installation process, before any changes to unit are applied<br />
15. Full LOG of installation process is stored on SD card folder /backup/logs/<br />

## Requirements

* Porsche US POG11 with PCM4/MIB2 system (any `MHI2_US_POG11_XXXXX`)
<!-- * Add list of supported FW -->
* Quality SD card, `8GB` capacity or more, **FAT32** formatted

## How to install

ℹ️ Check Youtube videos linked below for a video overview of the installation process.<br />
Videos might be out of date in parts, as the AIO solution is developed further.<br />
Always read the text below carfully!<br />

1. Format SD card with **FAT32** file system.<br />
2. [Download MHI2_XX_XXXXX_XXXXX_1 MUXXXX AIO](https://mibsolution.one/#/1/9/MHI2%20-%20HARMAN/Firmware/)).
   * ℹ️ Use [download manager](https://mibwiki.one/share/99dda9a7-06e2-4673-a5df-2ea7e0eb18cb) to speed up downloading from mibsolution.one
3. Extract the content of the AIO package to the root directory of the FAT32 formatted SD card.<br />
4. Power MIB2 unit system up by pressing power knob<br />
   * Connect external charger to car<br />
   * Power failure during FW update will brick your unit<br />
   * Turn all not required power consumers off<br />
   :warning: In case your car has kessy make sure that the car key will not leave the vehicle during the firmware update procedure.<br />
5. Insert the AIO SD card in `SD 1` port.<br />
6. **Firmware update will start automatically within 60 seconds. Do not do anything.**
   * If nothing happens within 2 minutes, double check SD Card for FAT32 formatting and proper file structure.<br />
7. Wait for the update to be installed - **be patient**.<br />
   * System will reboot a few times during the firmware update procedure. The screen can stay off or stuck on the Porsche logo for several seconds.<br />
   * Depending on the start firmware version the update will take between 10 - 40 minutes (this is why an external charger is required.<br />
8. The installation will finish with a 'Summary of devices' screen of all installed packages and their installation status.<br />
   * Updates packages have to show Y(es)<br />
   * Packages will be different based on original FW version<br />
   * Exit this screen by pressing 'Continue' on screen<br />
<!--    * Add fitting image -->
9. Last screen will be 'Start backup documentation'<br />
   * Exit this screem by pressing 'Cancel backup documentation' on screen<br />
<!--    * Add fitting image<br /> -->
   * This is as it should be<br />
   * Unit will reboot one more time<br />
10. Unit boots up into normal user interface<br />
<!-- 11. Enter GEM and run [SVM fix in M.I.B](update link)<br /> -->
   * This will run for a few minutes and the unit will reboot one last time<br />
12. AIO FW update is completly done<br />
   * Have fun and explore the new functions!<br />

<!-- ## Bose Sound System update

**Standard install has BOSE updates REMOVED.**<br />

By default, the AIO FW will not update the Bose amplifier firmware. `metainfo2.txt` was prepared to skip this component.<br />
Updating will require parameterization of the amplifier, which must be completed with PIWIS or at the dealer.<br />

:warning: Without the parameterization you will have no sound.<br />

If you wish to update Bose you can use different `metainfo2.txt`, which is included into the IO package.

1. Remove `metainfo2.txt`<br />
2. Rename `metainfo2-Bose.txt` to `metainfo2.txt`<br />
3. Run the update<br />
4. Perform parametrization<br /> -->

## SVM fix

Use built-in M.I.B AIO version to run SVM fix.<br />
Enter GEM (CAR+TUNER buttons on home screen) and select function.<br />
![image](https://user-images.githubusercontent.com/98130152/178356676-128374db-d50b-4f4f-981b-377d0ef83e5d.png)<br />

# Map updates to the latest maps:<br />

1. **[Download latest maps here](https://mibsolution.one/#/1/15/MHI2(Q))**<br />
   * ℹ️ Use [download manager](https://mibwiki.one/share/99dda9a7-06e2-4673-a5df-2ea7e0eb18cb) to speed up downloading from mibsolution.one<br />
2. Copy files to the root of a FAT32 32GB SD card<br />
3. Install via Software Update on your unit<br />

<!-- # Retrofit GPS Antenna 

Use M.I.B to check if your car already has a GPS antenan built in.<br />
![image](https://user-images.githubusercontent.com/98130152/178350343-4a692a0c-06b4-4141-9705-950873dc6d68.png)<br />

If NO antenna is installed you have several options to retrofit one.<br />
You can place the antenna directly behind your PCM screen. <br />
 -->
