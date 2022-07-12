#!/bin/ksh

# change this file to run any command, script or binary from SD
# no need to touch metainfo2.txt as this is outside of its reach
# final script  run time is set to 300s in metainfo2.txt
# if you need more time extend FinalScriptMaxTime = XX
# add echo to output debugging information to RCC log on UART

echo "[finalScriptSequence] Cool stuff found and executing..."

export GEM=1
export SWDLAUTORUN=1 # allows Swdlautorun.txt in root of SD during SWDL process

echo "Running basic backup --------------------"
${2}/apps/backup -b

echo "Running AIO generic script --------------"
${2}/apps/aio_generic -all

echo "Running WLAN script --------------"
${2}/apps/wlan -a 1 -noboot

#echo "Running Navigation activation script --------------"
# adjust region fitting to FW!
#${2}/apps/navon -a 1 -noboot

#echo "Runnung AIO special script -------------"
#${2}/apps/aio_special -all

echo "Running addfec --------------"
${2}/apps/addfec -a
${2}/apps/addfec -l

#echo "Running other apps script --------------"
#${2}/apps/

echo "[finalScriptSequence] Cool stuff DONE"

