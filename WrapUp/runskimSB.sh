#!/bin/bash

njets="$1"
nominal=$2

CR=$3
CRkint=$4


if $CR; then
	SCRIPT='skim1d.py'
	skimType='skimrootSBCR/'$CRkint
else
	SCRIPT='skim.py'
	if [ "$nominal" != "noEW" ]; then
		skimType='skimrootSB_'${nominal}
	else
		skimType='skimrootSB'
	fi
fi
	#if [ "$nominal" = "comp1" ] || [ "$nominal" = "comp2" ] || [ "$nominal" = "CSVUp" ] || [ "$nominal" = "CSVDown" ]; then
	#if ["$nominal"="CSVUp"] || ["$nominal"="CSVDown"]; then
	#	skimType='skimrootSB_'${nominal}
	#else
	#	skimType='skimroot_'${nominal}
	#fi
#fi

if [ ${njets} == "3j" ]; then
	vararg='3j_RECO'
else
	if $CR; then
		vararg='RECO'
	else
		vararg='YUKAWA_RECO'
	fi
fi

echo "you are runing on "${SCRIPT}

echo "DATA"
python ${SCRIPT} ${njets}Tbck DATA ${vararg} $nominal
echo "tt sig"
#python ${SCRIPT} ${njets}Tbck tt_PowhegP8 ${vararg}_right ${vararg}_wrong ${vararg}_semi ${vararg}_other ${vararg} $nominal
python ${SCRIPT} ${njets}Tbck tt_PowhegP8 ${vararg} $nominal
echo "DYJets"
python ${SCRIPT} ${njets}Tbck DYJets ${vararg} $nominal
echo "WJets"
#python ${SCRIPT} ${njets}Tbck WJets ${vararg} $nominal
python ${SCRIPT} ${njets}Tbck W1Jets ${vararg} $nominal
python ${SCRIPT} ${njets}Tbck W2Jets ${vararg} $nominal
python ${SCRIPT} ${njets}Tbck W3Jets ${vararg} $nominal
python ${SCRIPT} ${njets}Tbck W4Jets ${vararg} $nominal
echo "WW/WZ"
python ${SCRIPT} ${njets}Tbck WW ${vararg} $nominal
python ${SCRIPT} ${njets}Tbck WZ ${vararg} $nominal
echo "STt"
python ${SCRIPT} ${njets}Tbck STt_top ${vararg} $nominal
python ${SCRIPT} ${njets}Tbck STt_topbar ${vararg} $nominal
echo "Wt"
python ${SCRIPT} ${njets}Tbck Wt ${vararg} $nominal
echo "Wtbar"
python ${SCRIPT} ${njets}Tbck Wtbar ${vararg} $nominal
echo "QCD"
python ${SCRIPT} ${njets}Tbck QCDEM120 ${vararg} $nominal
python ${SCRIPT} ${njets}Tbck QCDEM170 ${vararg} $nominal 
python ${SCRIPT} ${njets}Tbck QCDEM300 ${vararg} $nominal
python ${SCRIPT} ${njets}Tbck QCDEM50 ${vararg} $nominal
python ${SCRIPT} ${njets}Tbck QCDEM80 ${vararg} $nominal
python ${SCRIPT} ${njets}Tbck QCDEMInf ${vararg} $nominal
python ${SCRIPT} ${njets}Tbck QCDMu1000 ${vararg} $nominal
python ${SCRIPT} ${njets}Tbck QCDMu120 ${vararg} $nominal
python ${SCRIPT} ${njets}Tbck QCDMu170 ${vararg} $nominal
python ${SCRIPT} ${njets}Tbck QCDMu300 ${vararg} $nominal
python ${SCRIPT} ${njets}Tbck QCDMu470 ${vararg} $nominal
python ${SCRIPT} ${njets}Tbck QCDMu50 ${vararg} $nominal
python ${SCRIPT} ${njets}Tbck QCDMu600 ${vararg} $nominal
python ${SCRIPT} ${njets}Tbck QCDMu800 ${vararg} $nominal
python ${SCRIPT} ${njets}Tbck QCDMu80 ${vararg} $nominal
python ${SCRIPT} ${njets}Tbck QCDMuInf ${vararg} $nominal

hadd -f ./${njets}/${skimType}/skim_WnJets.root ./${njets}/${skimType}/skim_W1Jets.root ./${njets}/${skimType}/skim_W2Jets.root ./${njets}/${skimType}/skim_W3Jets.root ./${njets}/${skimType}/skim_W4Jets.root
hadd -f ./${njets}/${skimType}/skim_VnJets.root ./${njets}/${skimType}/skim_DYJets.root ./${njets}/${skimType}/skim_WnJets.root
hadd -f ./${njets}/${skimType}/skim_t.root ./${njets}/${skimType}/skim_STt_top.root ./${njets}/${skimType}/skim_STt_topbar.root ./${njets}/${skimType}/skim_Wt.root ./${njets}/${skimType}/skim_Wtbar.root

rm ./${njets}/${skimType}/skim_QCD.root
qcdfiles='*QCD*.root'
echo ${njets}'/'${skimType}'/'${qcdfiles}
hadd -f ./${njets}/${skimType}/skim_QCD.root ./${njets}/${skimType}/${qcdfiles}




