coverage run --source=jspec -m unittest test/test.py
coverage report -m > test/coverage/coverage.txt
coverage json -o test/coverage/coverage.json
python3 ./test/coverage/coverage.py
