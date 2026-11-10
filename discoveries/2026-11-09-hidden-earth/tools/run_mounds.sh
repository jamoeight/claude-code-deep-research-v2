#!/bin/bash
cd "$(dirname "$0")/.."
O=data/private/mounds
run(){ [ -f $O/$1.json ] || NTH=3 python3 tools/scan_mounds.py $2 $3 $4 $5 $O/$1.json > $O/$1.log 2>&1; echo "$1 done"; }
run iraq_akkad_diyala 33 35 43 46
run ekallatum 35 36 43 44
run ghana_ghaba 15 16 -9 -7
run kanem_njimi 13 15 14 17
run mali_capital 11 13 -9 -6
run niger_inland_delta 13 16 -6 -3
run sistan 30 32 61 63
run cholistan 28 30 70 73
