mes_server/
├── app.py                  # Flask API + MQTT broker interface
├── dashboard.py            # Streamlit app (runs separately)
├── requirements.txt
└── data/
    ├── work_orders.json
    └── machine_status.json



ERP/Manual Order → Flask API (app.py)
                        ↓
              Sends Order via MQTT → ESP32
                        ↑                        ↓
         Receives status via MQTT     Executes Order
                        ↓
                Saves in machine_status.json
                        ↓
          📊 Streamlit dashboard.py reads JSONs and shows:
              ✅ Orders
              📈 Machine Status
              📋 History Logs






steps:

mkdir -p mes_server/data
cd mes_server


nano requirements.txt

and paste -->Flask==2.3.2


# Create machine_status.json

nano data/machine_status.json

and paste-->[]

nano data/work_orders.json

and paste -->

[
  {
    "order_id": "WO123",
    "product": "WidgetA",
    "quantity": 100,
    "machine_id": "M001",
    "status": "PENDING"
  }
]


.......................................

create app.py
nano app.py
...................................
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

run the server:   python app.py
and observe--> http://192.168.182.131:5000
............................................................
work oreder--pushing and testing-->  curl http://192.168.137.14:5000/api/work-orders
.........................................................
#Setup venv and Install paho-mqtt
# 1. Navigate to your MES app folder
cd ~/mes_server

# 2. Create a virtual environment
python3 -m venv venv

# 3. Activate the virtual environment
source venv/bin/activate

# 4. Now install paho-mqtt inside venv
pip install paho-mqtt flask
...............................................................
 Confirm Installation

pip list
..............................


if mqtt not functioning:at cmd @raspi and add(if req)

Check /etc/mosquitto/mosquitto.conf:

listener 1883
allow_anonymous true

..................
sudo systemctl restart mosquitto
............................................

To Run streamlit: Inside vnc

streamlit run dashboard.py

check:
http://192.168.182.131:8501

...............................
Special case: For  immutable file writing
1. ls -l app.py
2.sudo chown pi:pi app.py
sudo chmod +w app.py


/////****** production-grade WSGI server********/////
When deploying a Python web application (like Flask, Django, FastAPI, etc.) 
in a production environment, you should not use the built-in development server. 
Instead, you should use a production-grade WSGI server

ACTION--->

1. pip install gunicorn
2.app.py Modified
3.Create ---->gunicorn_config.py
4.gunicorn -b 0.0.0.0:5000 app:app -c gunicorn_config.py( ACHEIVED)

5. ***Auto start

/etc/supervisor/conf.d/mes.conf

Paste--->


[program:mes]
directory=/home/pi/MES_server
command=/home/pi/MES_server/venv/bin/gunicorn -b 0.0.0.0:5000 app:app -c gunicorn_config.py
autostart=true
autorestart=true
stderr_logfile=/var/log/mes.err.log
stdout_logfile=/var/log/mes.out.log
user=pi

......................................

Relaod and Start:

sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start mes


............................................
copy any folder to laptop from Raspi--->
scp -r pi@192.168.1.100:/home/pi/MES_server C:\Users\YourUsername\Documents\

...............................
Git/ GitHub integration: https://github.com/arefin7/MES_server

How to:

1. find /home/pi -type d -name ".git"


Note:  GitHub recommends keeping files < 50 MB.

venv/ is platform dependent → does not need to be in git.

Must Do:
nano .gitignore

paste-->

# Python
__pycache__/
*.pyc

# Virtualenv
venv/

# Logs
*.log

# Data
data/*.json


Then,

git rm -r --cached venv
git add .gitignore
git commit -m "Add .gitignore and remove venv from repo"
git push


//
Final result:
✅ Your GitHub repo will only contain:

app.py

dashboard.py

requirements.txt

data/ (if you want)

README.md (you can add)

///













2.
cd ~/MES_server
git init
git add .
git commit -m "Initial commit - MES server baseline"

#Then your repo will be ready

Create empty GitHub repo
👉 Go to https://github.com → login → + → New Repository
👉 Name it: MES_server (or any name you like)
👉 Set Public or Private → your choice
👉 Don't initialize with README (keep it empty) → Create repository

3.
 git branch

#  It will say master

4. add remote
git remote add origin https://github.com/arefin7/MES_server.git

5. Push code to GitHub

 Generate PAT:
👉 Go to → https://github.com/settings/tokens → Tokens (classic)
👉 Click → Generate new token (classic)
👉 Give it name: Raspi MES push
👉 Expiration → 90 days or 1 year
👉 Select scopes:

✅ repo

✅ workflow (optional)

✅ read:org (optional)

👉 Generate → copy the token




git push -u origin master


Username: arefin7
Password: <<< paste your PAT here >>>

..............................................Achieved!

✅ You can now see it here → https://github.com/arefin7/MES_server
 






















