# cs848w20: Semi-supervised learning for Entity Matching.
NOTE: This guide assumes you have docker & docker-compose installed. If you do not, see Setup & Installation for instructions on installing docker & docker-compose.



## Quickstart
1. Clone this repository, & navigate inside the project directory.
```
git clone git@github.com:JRWu/cs848w20.git

cd cs848w20/
```

2. Initialize the submodules
```
git submodule init

git submodule update
```

3. Run & Evaluate Magellan on RESTAURANTS and ABT_BUY
```
# Shell into the magellan container & set the paths
make magellan
bash /magellan/entrypoint.sh

# This step evaluates baseline magellan on RESTAURANTS
python /src/running_magellan.py

# This step evaluates EMSS magellan on RESTAURANTS
python /src/active_magellan.py

# This step evaluates baseline & EMSS magellan on ABT_BUY
python /src/active_magellan_buy_dataset.py

```

4. Run & Evaluate Dedupe.io on ABT_BUY
```
make dedupe
python /src/link_example/record_linkage_example.py
```




## Setup & Installation
NOTE: This guide is intended for linux based systems such as Ubuntu 16.04 and 18.04, however any system that can run docker & docker-compose will work.

1. Install stable docker-ce
```
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - 
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt-get update
sudo apt-get install docker-ce
```

(Optional) Perform post-install docker instructions in order to run docker as root.
```
sudo groupadd docker
sudo usermod -aG docker $USER
```
NOTE: You must restart your shell for the docker permission changes to take effect.

2. Install docker-compose, allow execution permissions, and create a symbolic link for command-line execution.
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.25.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```
