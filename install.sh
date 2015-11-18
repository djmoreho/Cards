pip install virtualenv
virtualenv cards
source cards/bin/activate

pip install -r reqs.txt
cd Server/
python server.py
deactivate
