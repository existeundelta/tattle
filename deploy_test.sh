apt-get update && apt-get -y upgrade
apt-get install git python-pip 
git clone https://github.com/hollerith/tattle.git
cd tattle
pip install -r requirements.txt
python app.py
