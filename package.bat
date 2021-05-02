REM SET CANDLE="C:\Program Files (x86)\WiX Toolset v3.11\bin\candle.exe"
REM SET LIGHT="C:\Program Files (x86)\WiX Toolset v3.11\bin\light.exe"

Del Setup\*.wixpdb
Del Setup\*.wixobj
Del Setup\*.msi

%CANDLE% ".\AViewer.wxs" -out .\Setup\
IF %ERRORLEVEL% NEQ 0 goto :ERROR
%LIGHT% -out ".\Setup\AViewer-%1.msi" ".\Setup\AViewer.wixobj" -ext WixUIExtension -ext WixUtilExtension
IF %ERRORLEVEL% NEQ 0 goto :ERROR

:EOF
ECHO process completed 
exit

:ERROR
exit 1