# install python-dlt
mkdir -p libs && cd libs
git clone -b v2.18.9 https://github.com/bmwcarit/python-dlt.git

# install libdlt, a dependency of python-dlt
sudp apt-get update
sudo apt-get install -y cmake zlib1g-dev libdbus-glib-1-dev build-essential
git clone -b v2.18.8 https://github.com/COVESA/dlt-daemon.git
cd dlt-daemon
mkdir build
cd build
cmake ..
make
sudo make install
sudo ldconfig
## If the installation didn't work, check symbolic links are setup properly.
## Run: ls -la /usr/local/lib | grep "\->"
## python-dlt only works on libdlt.so.2 version 2.18.5 and 2.18.8