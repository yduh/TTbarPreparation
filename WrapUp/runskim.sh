#!/bin/bash

nominal='noEW'
#nominal='noEW_removetrigger'
GT='noEW' #'0.0y 1.0y 2.0y 3.0y 4.0y 5.0y noEW'
skimType='skimroot'
njets="$1"

CR=false

RunSig=false
RunBcks=false
RunSB=false

RunUnc_EXP=false
RunUnc_EXPBCK=false
RunUnc_TH=true
RunUnc_THBCK=false
RunUnc_JES=false
RunUnc_pT=false

RunMultiSBs=false
RunUnc_QCD=false


if $CR; then
	SCRIPT='skim1d.py'
	TbckSCRIPT='Tbck1d.py'
	CRfolder="$2" #'thadpt' #this should be the same like in vararg: folder_savename
	#skimType='skimrootCR/'$CRfolder
else
	SCRIPT='skim.py'
	TbckSCRIPT='Tqcd.py'
	#skimType='skimrootSB'
fi

if [ ${njets} == "3j" ]; then
	vararg='3j'
else
	vararg='YUKAWA'
fi

echo "you are runing on "${njets}

if $RunUnc_pT; then
	python ${SCRIPT} ${njets} tt_PowhegP8 ${vararg}_RECO 'nnlopT'
fi

if $RunSig; then
	if $CR; then
		python ${SCRIPT} ${njets} tt_PowhegP8 ${vararg}_RECO ${nominal}
	else
		for gt in $GT
		do
			echo "tt_PowehgP8 ${gt}"
			python ${SCRIPT} ${njets} tt_PowhegP8 ${vararg}_RECO_right ${vararg}_RECO_wrong ${vararg}_RECO_semi ${vararg}_RECO_other ${vararg}_RECO ${gt}
		done
	fi
fi

if $RunBcks; then
	runbckList='DATA DYJets W1Jets W2Jets W3Jets W4Jets WW WZ STt_top STt_topbar Wt Wtbar WJets QCDEM120 QCDEM170 QCDEM300 QCDEM50 QCDEM80 QCDEMInf QCDMu1000 QCDMu120 QCDMu170 QCDMu300 QCDMu470 QCDMu50 QCDMu600 QCDMu800 QCDMu80 QCDMuInf'
	##runList=$(ls ~/work/lpcresults/${njets}/noEW/*.root )
	##runList=$(ls /afs/cern.ch/user/y/yduh/work/lpcresults/${njets}/${nominal}/*.root | cut -f 1 -d '.' | grep -v tt_*)
	for unc in $runbckList; 
	do
		##python ${SCRIPT} ${njets} $(basename $i | cut -f 1 -d '.' | egrep -v '(tt_powhegP8|DATAEL|DATAMU)') ${vararg}_RECO $nominal
		echo $unc
		python ${SCRIPT} ${njets} ${unc} ${vararg}_RECO $nominal
	done

	hadd -f ./${njets}/${skimType}/skim_WnJets.root ./${njets}/${skimType}/skim_W1Jets.root ./${njets}/${skimType}/skim_W2Jets.root ./${njets}/${skimType}/skim_W3Jets.root ./${njets}/${skimType}/skim_W4Jets.root
	hadd -f ./${njets}/${skimType}/skim_VnJets.root ./${njets}/${skimType}/skim_DYJets.root ./${njets}/${skimType}/skim_WnJets.root
	hadd -f ./${njets}/${skimType}/skim_t.root ./${njets}/${skimType}/skim_STt_top.root ./${njets}/${skimType}/skim_STt_topbar.root ./${njets}/${skimType}/skim_Wtbar.root ./${njets}/${skimType}/skim_Wt.root

	rm ./${njets}/${skimType}/skim_QCD.root
	qcdfiles='skim_QCD*.root'
	echo ${njets}'/'${skimType}'/'${qcdfiles}
	hadd -f ./${njets}/${skimType}/skim_QCD.root ./${njets}/${skimType}/${qcdfiles}
fi


if $RunSB; then
	echo "preparing the sideband templates"
	if $CR; then
		./runskimSB.sh ${njets} $nominal $CR $CRfolder
	else
		./runskimSB.sh ${njets} $nominal $CR 
	fi
	python ${TbckSCRIPT} ${njets} $nominal
fi

if $RunUnc_QCD; then
	./runskimSB.sh ${njets} "comp1" false
	python ${TbckSCRIPT} ${njets} "comp1"
	
	./runskimSB.sh ${njets} "comp2" false
	python ${TbckSCRIPT} ${njets} "comp2"

	./runskimSB.sh ${njets} "CSVUp" false
	python ${TbckSCRIPT} ${njets} "CSVUp"
	
	./runskimSB.sh ${njets} "CSVDown" false
	python ${TbckSCRIPT} ${njets} "CSVDown"
fi

if $RunMultiSBs; then
	runbckList='DATA DYJets W1Jets W2Jets W3Jets W4Jets WW WZ STt_top STt_topbar Wt Wtbar tt_PowhegP8'
	for unc in $runbckList;
	do
		python ${SCRIPT} ${njets} ${unc} ${vararg}_RECO Aless0.3
		#python ${SCRIPT} ${njets} ${unc} ${vararg}_RECO B0.3to0.6
		#python ${SCRIPT} ${njets} ${unc} ${vararg}_RECO Clarger0.6
		#python ${SCRIPT} ${njets} ${unc} ${vararg}_RECO C0.6to0.8
	done
	hadd -f ./${njets}/${skimType}/skim_WnJets.root ./${njets}/${skimType}/skim_W1Jets.root ./${njets}/${skimType}/skim_W2Jets.root ./${njets}/${skimType}/skim_W3Jets.root ./${njets}/${skimType}/skim_W4Jets.root
	hadd -f ./${njets}/${skimType}/skim_VnJets.root ./${njets}/${skimType}/skim_DYJets.root ./${njets}/${skimType}/skim_WnJets.root 
	hadd -f ./${njets}/${skimType}/skim_t.root ./${njets}/${skimType}/skim_STt_top.root ./${njets}/${skimType}/skim_STt_topbar.root ./${njets}/${skimType}/skim_Wtbar.root ./${njets}/${skimType}/skim_Wt.root
fi


if $RunUnc_EXP; then
	echo "Experimental uncertainties:"
	runsysexpList='btagUp btagDown ltagUp ltagDown JESUp JESDown JERUp JERDown pileupUp pileupDown METUp METDown lepUp lepDown'
	for unc in $runsysexpList; 
	do
		echo $unc
		python ${SCRIPT} ${njets}unc ${unc}/tt_PowhegP8 ${vararg}_RECO $nominal
	done
fi


if $RunUnc_TH; then
	echo "Theoretical uncertainties:"
	runsysthList1='fsUp fsDown rsUp rsDown rsfsSSUp rsfsSSDown bdecayUp bdecayDown bfragUp bfragDown'
	#runsysthList2='MCs/tt_mtop1755_PowhegP8 MCs/tt_mtop1695_PowhegP8 MCs/tt_hdup_PowhegP8 MCs/tt_hddown_PowhegP8 MCs/tt_isrup_PowhegP8 MCs/tt_isrdown_PowhegP8 MCs/tt_fsrup_PowhegP8 MCs/tt_fsrdown_PowhegP8 MCs/tt_tuneup_PowhegP8 MCs/tt_tunedown_PowhegP8 MCs/tt_erdon_PowhegP8'
	runsysthList2='MCs/tt_mtop1735new_PowhegP8 MCs/tt_mtop1715new_PowhegP8 MCs/tt_mtop1735old_PowhegP8 MCs/tt_mtop1715old_PowhegP8 MCs/tt_mtop1735_PowhegP8 MCs/tt_mtop1713_PowhegP8'

	#for unc in $runsysthList1; 
	#do
	#	echo $unc
	#	python ${SCRIPT} ${njets}unc ${unc}/tt_PowhegP8 ${vararg}_RECO $nominal
	#done
	for unc in $runsysthList2; 
	do
		echo $unc
		python ${SCRIPT} ${njets}unc ${unc} ${vararg}_RECO $nominal
	done
fi

if $RunUnc_THBCK; then
	echo "single top Theoretical uncertainties:"
	runsysthList1_stbcks='bdecayUp bdecayDown bfragUp bfragDown'
	runsysthList2_st='STuncs/STt_topbar_isrfsrdown STuncs/STt_topbar_isrfsrup STuncs/STt_top_isrfsrdown STuncs/STt_top_isrfsrup STuncs/Wtbar_fsrdown STuncs/Wtbar_isrdown STuncs/Wt_fsrdown STuncs/Wt_isrdown'
	for unc in $runsysthList1_stbcks; 
	do
		echo $unc
		python ${SCRIPT} ${njets}unc ${unc}/STt_top ${vararg}_RECO $nominal
		python ${SCRIPT} ${njets}unc ${unc}/STt_topbar ${vararg}_RECO $nominal
		python ${SCRIPT} ${njets}unc ${unc}/Wtbar ${vararg}_RECO $nominal
		python ${SCRIPT} ${njets}unc ${unc}/Wt ${vararg}_RECO $nominal
		hadd -f ./${njets}/${skimType}/skim_${unc}_t.root ./${njets}/${skimType}/skim_${unc}_STt_top.root ./${njets}/${skimType}/skim_${unc}_STt_topbar.root ./${njets}/${skimType}/skim_${unc}_Wtbar.root ./${njets}/${skimType}/skim_${unc}_Wt.root
		rm ./${njets}/${skimType}/skim_${unc}_STt_top.root ./${njets}/${skimType}/skim_${unc}_STt_topbar.root ./${njets}/${skimType}/skim_${unc}_Wtbar.root ./${njets}/${skimType}/skim_${unc}_Wt.root

		bckList='DYJets WJets QCDEM120 QCDEM170 QCDEM300 QCDEM50 QCDEM80 QCDEMInf QCDMu1000 QCDMu120 QCDMu170 QCDMu300 QCDMu470 QCDMu50 QCDMu600 QCDMu800 QCDMu80 QCDMuInf'
		for bck in $bckList;
		do
			python ${SCRIPT} ${njets}unc ${unc}/${bck} ${vararg}_RECO $nominal
		done
		hadd -f ./${njets}/${skimType}/skim_${unc}_Vj.root ./${njets}/${skimType}/skim_${unc}_DYJets.root ./${njets}/${skimType}/skim_${unc}_WJets.root
		rm ./${njets}/${skimType}/skim_${unc}_QCD.root
		qcdfiles='skim_'${unc}'_QCD*.root'
		echo ${njets}'/'${skimType}'/'${qcdfiles}
		hadd -f ./${njets}/${skimType}/skim_${unc}_QCD.root ./${njets}/${skimType}/${qcdfiles}

	done
	for unc in $runsysthList2_st;
	do
		echo $unc
		python ${SCRIPT} ${njets}unc ${unc} ${vararg}_RECO $nominal
	done

	hadd -f ./${njets}/${skimType}/skim_fsrDown_t.root ./${njets}/${skimType}/skim_isrfsrdown_STt_top.root ./${njets}/${skimType}/skim_isrfsrdown_STt_topbar.root ./${njets}/${skimType}/skim_fsrdown_Wt.root ./${njets}/${skimType}/skim_fsrdown_Wtbar.root
	rm ./${njets}/${skimType}/skim_isrfsrdown_STt_top.root ./${njets}/${skimType}/skim_isrfsrdown_STt_topbar.root ./${njets}/${skimType}/skim_fsrdown_Wt.root ./${njets}/${skimType}/skim_fsrdown_Wtbar.root ./${njets}/${skimType}/skim_isrdown_Wtbar.root ./${njets}/${skimType}/skim_isrdown_Wt.root ./${njets}/${skimType}/skim_isrfsrup_STt_topbar.root ./${njets}/${skimType}/skim_isrfsrup_STt_top.root 
fi


if $RunUnc_EXPBCK; then
	echo "BCK Experimential uncertainties"
	sysource='btagUp btagDown ltagUp ltagDown JERUp JERDown pileupUp pileupDown METUp METDown lepUp lepDown'
	#runbckList='DYJets W1Jets W2Jets W3Jets W4Jets' #try with the VnJets in 3j and the sys variations are all within statistics fluctuation  
	runbckList='STt_top STt_topbar Wt Wtbar QCDEM120 QCDEM170 QCDEM300 QCDEM50 QCDEM80 QCDEMInf QCDMu1000 QCDMu120 QCDMu170 QCDMu300 QCDMu470 QCDMu50 QCDMu600 QCDMu800 QCDMu80 QCDMuInf'
	
	for unc in $sysource
	do
		echo $unc
		for comp in $runbckList
		do
			echo $comp
			python ${SCRIPT} ${njets}unc ${unc}/${comp} ${vararg}_RECO $nominal
		done
		
		hadd -f ./${njets}/${skimType}/skim_${unc}_WnJets.root ./${njets}/${skimType}/skim_${unc}_W1Jets.root ./${njets}/${skimType}/skim_${unc}_W2Jets.root ./${njets}/${skimType}/skim_${unc}_W3Jets.root ./${njets}/${skimType}/skim_${unc}_W4Jets.root
		hadd -f ./${njets}/${skimType}/skim_${unc}_VnJets.root ./${njets}/${skimType}/skim_${unc}_DYJets.root ./${njets}/${skimType}/skim_${unc}_WnJets.root
		hadd -f ./${njets}/${skimType}/skim_${unc}_t.root ./${njets}/${skimType}/skim_${unc}_STt_top.root ./${njets}/${skimType}/skim_${unc}_STt_topbar.root ./${njets}/${skimType}/skim_${unc}_Wt.root ./${njets}/${skimType}/skim_${unc}_Wtbar.root

		rm ./${njets}/${skimType}/skim_${unc}_QCD.root
		qcdfiles='skim_'${unc}'_QCD*.root'
		echo ${njets}'/'${skimType}'/'${qcdfiles}
		hadd -f ./${njets}/${skimType}/skim_${unc}_QCD.root ./${njets}/${skimType}/${qcdfiles}
	done
fi

	
if $RunUnc_JES; then
	echo "break down JES uncertainties for each components"
	sysource='AbsoluteStat AbsoluteScale AbsoluteMPFBias Fragmentation SinglePionECAL SinglePionHCAL TimePtEta RelativePtBB RelativePtEC1 RelativePtEC2 RelativeBal RelativeFSR RelativeStatFSR RelativeStatEC PileUpDataMC PileUpPtRef PileUpPtBB PileUpPtEC1 PileUpPtEC2 FlavorQCD'
	#runbckList='DYJets W1Jets W2Jets W3Jets W4Jets' #try with the VnJtes in 3j and the sys variation are all within statistics fluctuation
	runbckList='STt_top STt_topbar Wt Wtbar QCDEM120 QCDEM170 QCDEM300 QCDEM50 QCDEM80 QCDEMInf QCDMu1000 QCDMu120 QCDMu170 QCDMu300 QCDMu470 QCDMu50 QCDMu600 QCDMu800 QCDMu80 QCDMuInf tt_PowhegP8'
	
	for unc in $sysource
	do
		echo $unc
		for comp in $runbckList
		do
			echo $comp
			python ${SCRIPT} ${njets}unc JESUp${unc}/${comp} ${vararg}_RECO $nominal
			python ${SCRIPT} ${njets}unc JESDown${unc}/${comp} ${vararg}_RECO $nominal
		done
	
		hadd -f ./${njets}/${skimType}/skim_JESUp${unc}_WnJets.root ./${njets}/${skimType}/skim_JESUp${unc}_W1Jets.root ./${njets}/${skimType}/skim_JESUp${unc}_W2Jets.root ./${njets}/${skimType}/skim_JESUp${unc}_W3Jets.root ./${njets}/${skimType}/skim_JESUp${unc}_W4Jets.root
		hadd -f ./${njets}/${skimType}/skim_JESDown${unc}_WnJets.root ./${njets}/${skimType}/skim_JESDown${unc}_W1Jets.root ./${njets}/${skimType}/skim_JESDown${unc}_W2Jets.root ./${njets}/${skimType}/skim_JESDown${unc}_W3Jets.root ./${njets}/${skimType}/skim_JESDown${unc}_W4Jets.root
		hadd -f ./${njets}/${skimType}/skim_JESUp${unc}_VnJets.root ./${njets}/${skimType}/skim_JESUp${unc}_DYJets.root ./${njets}/${skimType}/skim_JESUp${unc}_WnJets.root
		hadd -f ./${njets}/${skimType}/skim_JESDown${unc}_VnJets.root ./${njets}/${skimType}/skim_JESDown${unc}_DYJets.root ./${njets}/${skimType}/skim_JESDown${unc}_WnJets.root
		hadd -f ./${njets}/${skimType}/skim_JESUp${unc}_t.root ./${njets}/${skimType}/skim_JESUp${unc}_STt_top.root ./${njets}/${skimType}/skim_JESUp${unc}_STt_topbar.root ./${njets}/${skimType}/skim_JESUp${unc}_Wt.root ./${njets}/${skimType}/skim_JESUp${unc}_Wtbar.root
		hadd -f ./${njets}/${skimType}/skim_JESDown${unc}_t.root ./${njets}/${skimType}/skim_JESDown${unc}_STt_top.root ./${njets}/${skimType}/skim_JESDown${unc}_STt_topbar.root ./${njets}/${skimType}/skim_JESDown${unc}_Wt.root ./${njets}/${skimType}/skim_JESDown${unc}_Wtbar.root

		rm ./${njets}/${skimType}/skim_JESUp${unc}_QCD.root
		rm ./${njets}/${skimType}/skim_JESDown${unc}_QCD.root
		qcdfilesup='skim_JESUp'${unc}'_QCD*.root'
		echo ${njets}'/'${skimType}'/'${qcdfilesup}
		hadd -f ./${njets}/${skimType}/skim_JESUp${unc}_QCD.root ./${njets}/${skimType}/${qcdfilesup}
		qcdfilesdw='skim_JESDown'${unc}'_QCD*.root'
		echo ${njets}'/'${skimType}'/'${qcdfilesdw}
		hadd -f ./${njets}/${skimType}/skim_JESDown${unc}_QCD.root ./${njets}/${skimType}/${qcdfilesdw}
	done
fi


