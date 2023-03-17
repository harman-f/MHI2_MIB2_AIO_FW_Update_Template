# MHI2_MIB2_AIO_FW_Update_Template 

This repository contains the building blocks for custom **A**ll **I**n **O**ne FW updates.

**⚠️ Content of this repository is NOT a FW update**

ℹ️ Read full article before using this update.<br />

# Check WIKI about how to use AIO FWs

[WIKI](https://github.com/harman-f/MHI2_MIB2_AIO_FW_Update_Template/wiki) contains instruction on how to use [AIO FWs](https://mibsolution.one/#/1/9/MHI2%20-%20HARMAN/Firmware) based on this building blocks.

# AIO FWs know to exist

## VW

* MHI2_ER_VWG11_K3342_1_AIO_MU1427
* MHI2_ER_VWG13_K4525_1_AIO_MU1367 - [can also convert from G11 to G13](https://github.com/harman-f/MHI2_MIB2_AIO_FW_Update_Template/wiki/G11-to-G13-conversion)

## Skoda

* MHI2_ER_SKG11_K3343_1_AIO_MU1433
* MHI2_ER_SKG13_P4526_1_AIO_MU1440 - [can also convert from G11 to G13](https://github.com/harman-f/MHI2_MIB2_AIO_FW_Update_Template/wiki/G11-to-G13-conversion)

## SEAT

* MHI2_ER_SEG11_P4709_1_AIO_MU1447

## Porsche

* MHI2_ER_POG11_K5126_1_AIO_MU1394
* MHI2_ER_POG24_K5137_1_AIO_MU1417
* MHI2_US_POG11_K5186_1_AIO_MU1476
* MHI2_US_POG24_K5136_1_AIO_MU1416

## Audi

* MHI2_ER_AU57x_K3663_1_MU1425_AIO
not based on this repo, but working similar

# Features

* Automatic starting FW update after plugging in SD<br />
* Patched IFS-Root (FEC, VCRN & Component Protection patch) will be used during the installation.<br />
* FecContainer.fec will be extended with missing FECs:<br />
    * `00030000`,`00040100`, `00050000`,`00070100`, `00070200`, `00030000`, `map FEC`,`00060100`,`00060500`,`00060700`,`00060800`, `00060900`, `00060A00`<br />
    * addFecs.txt in /common/tools/ can be adjusted as needed. Change add FECS with e.g. notepad.<br />
* CarPlay and AndroidAuto will be enabled during the installation<br />
* Developer Mode with GEM (hidden Green Engineering Menu) will be enabled during the installation<br />
    *No need for OBD tools like PIWIS to enable it.<br />
* WLAN will be enabled
* M.I.B. - More Incredible Bash will be enabled to run from SD<br />
* [M.I.B. AIO version](https://github.com/Mr-MIBonk/M.I.B._More-Incredible-Bash) - with AIO tailored functions - will be available directly from AIO SD card
    * SVM fix, backup/restore functions, some basic coding checks and more<br />
* Gracenote can be udated to latest version
* RadioStation DB can be updated to latest version
* Basic system backup will be run during installation process, before any changes to unit are applied<br />
* Full LOG of installation process is stored on SD card folder /backup/logs/<br />
