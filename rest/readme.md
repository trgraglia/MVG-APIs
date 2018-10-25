# MVG REST API FLASK WEB APP

## Installation
Update the PI
```
sudo apt-get update
sudo apt-get upgrade -y
sudo rpi-update
sudo reboot
```
Install Python PIP
```
sudo apt-get install python-pip
```
Install Flask
```
sudo pip install Flask
```
Clone this folder

## Start script on boot
```
pm2 startup
```
You need to copy the command given and paste back into your terminal.
```
cd ~
nano flask-start.sh
```
Add the command for the python script to the .sh file:
```
sudo python ~/rest/app.py
```
Exit and Save
Make the script executable
```
chmod +x flask-start.sh
```
Start the flask web app and force it to start on boot
```
pm2 start flask-start.sh
pm2 save
sudo reboot
```
