TopDAS
======

Top long exercise 2014, CMSDAS at LPC

Description:
============
1. The useful macros are in directory /bin and the location of edm Ntuples in form of .txt files is in directory /test.


2. Following are examples to run on edm Ntuples.

# For signal and background
python plotWJetsQuick.py --txtfiles=../test/ttbar_skim_files_8TeV.txt --outputFile=ttbar_skim_plots.root --doMC
python plotWJetsQuick.py --txtfiles=../test/t_skim_files_8TeV.txt --outputFile=t_skim_plots.root --doMC
python plotWJetsQuick.py --txtfiles=../test/tbar_skim_files_8TeV.txt --outputFile=tbar_skim_plots.root --doMC
python plotWJetsQuick.py --txtfiles=../test/wjets_skim_files_8TeV.txt --outputFile=wjets_skim_plots.root --doMC
python plotWJetsQuick.py --txtfiles=../test/mu_skim_files_8TeV.txt --outputFile=mu_skim_plots.root

# for the ABCD method the isolation of the muon has to be inverted, syntax is as follows:
python plotWJetsQuick.py --txtfiles=../test/mu_skim_files_8TeV.txt --outputFile=qcd_skim_plots.root --invertPFIso