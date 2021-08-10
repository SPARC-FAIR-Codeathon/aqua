# AQUA - docker
## About
Docker module for AQUA SPARC

# Docker deployment:
## Initial setup:
  - git clone the project
  - go to the containing directory (the one that having docker-compose.yml):
    - `cd aqua_docker`
  - create `.env` file, set the value:

        SANIC_LOGO="OVERRIDE LOGO USING CONFIG"
        ES_API_KEY = "api-key to acces SciCrunch"
        NM_EMAIL_USR = "email address for notifyme"
        NM_EMAIL_PWD = "email password for notifyme"
        DB_NAME = "sqlite3 file path"


## Deployment using docker-machine
  - Preparation
    - Clone the project and go to the containing directory (the one that having docker-compose.yml):
      - `cd aqua_docker`
    - Make sure docker-machine is installed:
      - `docker-machine version`
    - If not, refer to [here](https://docs.docker.com/machine/install-machine/) to install docker-machine.
    - Install a virtual machine application to create a docker machine. We use [VirtualBox](https://www.virtualbox.org/wiki/Downloads) to deploy locally.
  - Create a new docker machine:
      - `docker-machine create --driver virtualbox --virtualbox-memory 2048 aqua;`
        - creating a docker machine on VirtualBox
        - the minimum VirtualBox allocation is 2048 MB
  - Point docker client to `aqua`:
    - Mac OSX & Linux:
      - `eval "$(docker-machine env aqua)"`
    - Windows:
      - Show the environment of `aqua`
        - `docker-machine env --shell cmd aqua`
      - Set the environment by running a command under
        - `Run this command to configure your shell: `
          - If you use CMD, the command can be:
            - `@FOR /f "tokens=*" %i IN ('docker-machine env --shell cmd aqua') DO @%i`
          - If you use Powershell:
            - `docker-machine env --shell powershell aqua | Invoke-Expression`
  - Build and start the containers:
    - `docker-compose up -d --build`
  - Get the machine IP
    - `docker-machine ip aqua`
  - Now you can access AQUA via web browser with given docker api
    - http://DOCKER-MACHINE-IP/
  - Rerun after computer restart:
    - `docker-machine start aqua`

## Cloud deployment using docker context
  - Create a virtual machine instance in the cloud with minimum RAM 2048 MB
    (for our purpose we create a Ubuntu 18.04 LTS (Bionic) amd64 VM in [Nectar](https://ardc.edu.au/services/nectar-research-cloud/) cloud services)
    - before creating the VM, make sure you have created RSA key pair,
      - setup the public key in the cloud and the VM
      - here are links how to create RSA key pair in different OS:
        - Windows 10: https://phoenixnap.com/kb/generate-ssh-key-windows-10
        - Mac OSX: https://www.siteground.com/kb/how_to_generate_an_ssh_key_pair_in_mac_os/
        - Ubuntu: https://help.ubuntu.com/community/SSH/OpenSSH/Keys
  - Install Docker to the VM using ssh:
    - Connect to the VM:
      - `ssh ubuntu@VM-PUBLIC-IP` (if you are not use ubuntu, change the username)
    - Install Docker:
      - `sudo apt-get remove docker docker-engine docker.io containerd runc`
      - `sudo apt-get update`
      - `sudo apt-get install docker-ce docker-ce-cli containerd.io`
      - `sudo systemctl start docker`
    - Make sure you can run docker
      - `docker run hello-world`
    - If cannot run docker
      - `sudo groupadd docker`
      - `sudo usermod -aG docker $USER`
      - `newgrp docker`
    - Logout from the VM:
      - `exit`

  - Create context
    - `docker context create --docker host=ssh://ubuntu@VM-PUBLIC-IP remote_aqua`
  - Set remote_aqua as default context
    - `docker context use remote_aqua`
  - Build and run the containers in the VM:
    - `docker-compose --context remote_aqua up -d --build`
  - Now you can access AQUA via web browser with your VM public IP
    - http://VM-PUBLIC-IP/

MIT - **Free Software, Enjoy!**

[//]: #URLs
   [sanic]: <https://github.com/channelcat/sanic>
   [nginx]: <https://www.nginx.com/resources/wiki/>
