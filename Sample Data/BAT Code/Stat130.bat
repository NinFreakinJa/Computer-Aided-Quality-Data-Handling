@echo off
:: This cycles through all the indivdual bat files that convert the .dat to a .dfq
:: 2019.08.01 Author Capt. Chaos - The Disruptor
setlocal
set conf=D:\EV14_SL03\DataProcessing\DAT2DFQ\Station_XMLs
set conv=c:\windows\SysWOW64\cscript.exe /nologo D:\EV14_SL03\DataProcessing\DAT2DFQ\dfqconverter.vbs
set deletesource= false


rem convert all the file types (creates a long term set of files under year\month folders, an akt_st.dfq file with current run data and a set of files for uploading to qdas)
Call %conv% D:\EV14_SL03\DataProcessing\DAT2DFQ\Station_XMLs\SL03_DFQ_Stat130_Fu1.xml D:\EV14_SL03\ALR\ResultData\Stat130\FU1 %deletesource%
Call %conv% D:\EV14_SL03\DataProcessing\DAT2DFQ\Station_XMLs\SL03_DFQ_Stat130_Fu2.xml D:\EV14_SL03\ALR\ResultData\Stat130\FU2 %deletesource%

