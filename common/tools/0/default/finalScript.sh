#!/bin/ksh

echo [finalScript] for HW ${1} on medium ${2}...

# load cool stuff...
if [ -f ${2}/common/tools/finalScriptSequence.sh ]; then
	/bin/ksh ${2}/common/tools/finalScriptSequence.sh ${1} ${2}
else
	# Report error because finalScriptSequence.sh is not found
	echo "error no install script found"
fi

echo "[finalScript] finished"

touch /tmp/SWDLScript.Result

