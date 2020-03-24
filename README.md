# A docker-compose setup for evaluating cs848w20 project.
# Semi-supervised learning for Entity Matching.

# Setup & Installation
NOTE: This guide is intended for linux based systems such as Ubuntu 16.04 and 18.04, however any system that can run docker & docker-compose will work.

1. Install stable docker-ce (if docker is not already installed on your system)
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
NOTE: You must restart your shell or your computer for the docker permission changes to take effect.

2. Install docker-compose, allow execution permissions, and create a symbolic link for command-line execution.
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.25.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```

3. Clone this repository, & navigate inside the project directory.
```
git clone git@github.com:JRWu/cs848w20.git

cd cs848w20/
```

4. TODO: Add instructions on how to run our software, and then the comparable other software(s).

5. 