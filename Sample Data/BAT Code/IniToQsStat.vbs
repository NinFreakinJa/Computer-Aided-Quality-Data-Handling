'/* ------------------------------------------------------------------ */
'/*      I n i T o Q s S t a t . v b s                                 */
'/* ------------------------------------------------------------------ */
'/*                                                                    */
'/*      Project       :    OpCon IniToQsCom Converter                 */
'/*      Filename      :    IniToQsStat.vbs                            */
'/*      Moduleversion :    01                                         */
'/*      Date          :    01.02.2000 - 20:25:31                      */
'/*      Author(s)     :    F.-J. Kaiser (Informatikbüro Mellein)      */
'/*                                                                    */
'/*      Short description                                             */
'/*      * Simple interface to the converter object                    */
'/*                                                                    */
'/*                                                                    */
'/* ------------------------------------------------------------------ */
'/*                                                                    */
'/*  Moduleversions                                                    */
'/*  - V01  01.02.2000 F.-J. Kaiser (Informatikbüro Mellein)           */
'/*         Baseversion                                                */
'   - V02.00 04.02.00 BaW/TEF3.42 Schoberth
'                +   Dim res (sonst abbruch bei Fehler ohne errorcode !!!
'                +   OpenDatafile
'                    (3 Versuche das Resultfile zu oeffnen)
'/*                                                                    */
'/* ------------------------------------------------------------------ */
Option Explicit
Dim bNewFile
Dim sNewFileName
Dim aDataFile, sDataFile, sDataType
Dim aModule, aConvApp
Dim res, i

' Do not stop on error
On Error Resume Next

' ---------------------------------------------------------
' Function:     OpenDataFile
'
' Description:  Open the input data file and return it
' ---------------------------------------------------------
Function OpenDataFile (sDataFile)
  Dim aDataFile, nResult, Message
  
  'On Error Resume Next
  Set aDataFile = CreateObject("OpConFile.DataObjectFile")
  nResult = aDataFile.FileLoad(sDataFile)
  If nResult <> 0 then 
    nResult = aDataFile.FileLoad(sDataFile)
  End If
  If nResult <> 0 then 
    nResult = aDataFile.FileLoad(sDataFile)
  End If

  If nResult <> 0 then 
    Message = "Laden des Datenfiles fehlgeschlagen. Filename: " & sDataFile
    WScript.Echo (Message)
  	WScript.quit 98
  End If
  Set OpenDataFile = aDataFile
End Function


If WScript.Arguments.Count < 2 then
    WScript.Echo "Usage: cscript " & WScript.ScriptName & " <file> /CFG=<type> [/NewDfq] [/DfqFile=<name>]"
    WScript.Quit 1
ElseIf lcase(left(WScript.Arguments(1), 5)) <> "/cfg=" then
    WScript.Echo "Usage: cscript " & WScript.ScriptName & " <file> /CFG=<type> [/NewDfq] [/DfqFile=<name>]"
    WScript.Quit 2
End if

bNewFile = false
sNewFileName = ""
sDataFile = WScript.Arguments(0)
sDataType = mid(WScript.Arguments(1), 6)
For i = 1 to WScript.Arguments.Count - 1
    if lcase(WScript.Arguments(i)) = "/newdfq" then bNewFile = true
    if lcase(left(WScript.Arguments(i), 9)) = "/dfqfile=" then sNewFileName = mid(WScript.Arguments(i), 10)
Next

' Load the data file
'set aDataFile = CreateObject( "OpConFile.DataObjectFile2")
'res = aDataFile.FileLoad( sDataFile)
'if res <> 0 then PrintError "Error loading source file " & sDataFile, 3
set aDataFile = OpenDataFile(sDataFile)

set aConvApp = CreateObject( "IniToQsCom.Application")
If aConvApp Is Nothing Then PrintError "CreateObject( IniToQsCom.Application) failed", 6
    
set aModule = aConvApp.Modules.Item(sDataType)
if aModule is nothing then PrintError "Module " & sDataType & " not defined!", 7

res = aModule.Convert(aDataFile)
if res <> 0 then PrintError "Error " & hex(res) & " converting data file " & sDataFile, 8

'WScript.Echo "Successfully converted " & sDataFile

set aModule = nothing
set aConvApp = nothing

WScript.Quit Err.Number

'// -----------------------------------------
'// Error output
'// -----------------------------------------
Sub PrintError( sText, errorcode)
    WScript.Echo sText
    WScript.Quit errorcode
end sub


