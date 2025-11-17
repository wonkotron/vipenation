@ECHO off
set NAME=AirGoons KTO
set VER=0.01
python ../../build_theater.py -n "%NAME%" -v "%VER%" -c "build_ag_kto.json" -b "../../build" -a "../../artifacts" -m "AirGoons KTO" -s "Data\"
