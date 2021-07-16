# AQUA - docker
# About
Docker module for AQUA SPARK

Docker deployment:
# Initial setup:
  - git clone the project
  - go to the containing directory:
    `cd aqua_docker`
  - Start a new docker-machine:
    `docker-machine create -d virtualbox --virtualbox-memory 8192 aqua;`
    unfortunately, we need a large memory for CoreNLP and Stanza
  - Attach to the machine:
    `eval "$(docker-machine env aqua)"`

## Local deployment
  - Build the containers (This will take a while for the first time!):
    `docker-compose build`
  - Create and start containers:
    `docker-compose up -d`
  - Use `docker-machine ip aqua` to get the machine IP
  - Now you can access AQUA via web browser with given docker api
    http://DOCKER-MACHINE-IP/

  - Rerun after computer restart:
    `docker-machine start aqua`

## Local rebuild
  - Make sure the machine is started:
    `eval "$(docker-machine env aqua)"`
  - Make sure the available container is down
    `docker-compose down`
  - Rebuild, create, and start container
    `docker-compose up --build`
  - Make sure the docker machine is running
    `docker-machine start aqua`

## Cloud deployment
  - Create a virtual machine instance in the cloud
    (* for our purpose we create a Ubuntu 18.04 LTS (Bionic) amd64 VM in Nectar cloud services)
    - before creating the VM, make sure you have created RSA key pair,
      - setup the public key in the cloud and the VM
      - here are links how to create RSA key pair in different OS:
        - Windows 10: https://phoenixnap.com/kb/generate-ssh-key-windows-10
        - Mac OSX: https://www.siteground.com/kb/how_to_generate_an_ssh_key_pair_in_mac_os/
        - Ubuntu: https://help.ubuntu.com/community/SSH/OpenSSH/Keys
  - Install Docker to the VM using ssh:
    - Connect to the VM:
      `ssh ubuntu@VM-PUBLIC-IP` (if you are not use ubuntu, change the username)
    - Install Docker:
      `sudo apt-get remove docker docker-engine docker.io containerd runc`
      `sudo apt-get update`
      `sudo apt-get install docker-ce docker-ce-cli containerd.io`
      `sudo systemctl start docker`
    - Logout from the VM:
      `exit`

  - Create context
    `docker context create --docker host=ssh://ubuntu@VM-PUBLIC-IP remote_aqua`
  - Set remote_aqua as default context
    `docker context use remote_aqua`
  - Build the containers in the VM (you do not need to run it if you already build locally):
    `docker-compose --context remote_aqua build`
  - Run the containers in the VM:
    `docker-compose --context remote_aqua up -d`
  - Now you can access AQUA via web browser with your VM public IP
    http://VM-PUBLIC-IP/

## Cloud rebuild
  - Set remote_aqua as default context
    `docker context use remote_aqua`
  - Make sure the available container is down
    `docker-compose --context remote_aqua down`
  - Rebuild, create, and start container
    `docker-compose --context remote_aqua up --build`

MIT - **Free Software, Enjoy!**

[//]: #URLs
   [sanic]: <https://github.com/channelcat/sanic>
   [nginx]: <https://www.nginx.com/resources/wiki/>
