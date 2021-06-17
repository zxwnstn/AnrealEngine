echo "hello Build.bat"
cd Extras\ThirdParty\Python
set PYTHONHOME=%cd%
set PYTHONPATH=%cd%\Lib
python.exe ../../../Scripts/Build.py