apt-get -y update
apt-get -y install nginx
service nginx start 

python3 -m pip install --user virtualenv 
python3 -m venv venv
