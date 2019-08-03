#!/bin/bash

# data file: a1_final_data
test_data=a2_final_data
echo "Test data file: ${test_data}"

cat ${test_data}

./ur_bguanabara.py -h

./ur_bguanabara.py -l user ${test_data}
./ur_bguanabara.py -l host ${test_data}
./ur_bguanabara.py -u rchan -t daily ${test_data}
./ur_bguanabara.py -u rchan -t weekly ${test_data}
./ur_bguanabara.py -u rchan -t monthly ${test_data}
./ur_bguanabara.py -r 10.40.105.99 -t daily ${test_data}
./ur_bguanabara.py -r 10.40.105.99 -t weekly ${test_data}
./ur_bguanabara.py -r 10.40.105.99 -t monthly ${test_data}

./ur_bguanabara.py -l user ${test_data} -v
./ur_bguanabara.py -l host ${test_data} -v
./ur_bguanabara.py -u asmith -t daily ${test_data} -v
./ur_bguanabara.py -u asmith -t weekly ${test_data} -v
./ur_bguanabara.py -u asmith -t monthly ${test_data} -v
./ur_bguanabara.py -r 10.40.105.130 -t daily ${test_data} -v
./ur_bguanabara.py -r 10.40.105.130 -t weekly ${test_data} -v
./ur_bguanabara.py -r 10.40.105.130 -t monthly ${test_data} -v
