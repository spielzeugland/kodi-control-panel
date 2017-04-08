echo ">>> run update"
apt-get update -y
echo ">>> run dist-update"
apt-get dist-upgrade -y
echo ">>> install pip"
apt-get install -y python-pip
echo ">>> install RPi.GPIO"
apt-get install -y python-dev gcc
pip install RPi.GPIO
echo ">>> create user group 'gpio'"
python ./create_gpio_user_permission.py
echo ">>> install RPLCD"
pip install RPLCD

# TODO requires restart...
