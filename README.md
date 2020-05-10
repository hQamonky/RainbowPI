# RainbowPI
A web API to control an LED strip on a Raspberry PI.
# Introduction
This guide will go over on how to install and configure RainbowPi on a Raspberry PI.  
It will not go over on how to connect the LED strip to the Raspberry, but you can follow [this](https://dordnung.de/raspberrypi-ledstrip/) very well written guide to do so.  
I've also made a resume of this guide [here](https://github.com/hQamonky/RainbowPI/blob/master/docs/Hardware%20Installation.md).    
# Installation
*The following has been tested on a Raspberry Pi 2 model B v1.1 with Raspbian buster (Release 10).*  
Everything in this guide is done either on the terminal of the Raspberry Pi or by ssh to the Raspberry.  
## Requirements
RainbowPI is wrapped in a docker container.  
To make it work, you will have to install Docker.  
Run the command:  
`curl -sSL https://get.docker.com | sh`  
To be able to use docker without sudo, run:
`sudo usermod -aG docker pi` *(note that 'pi' is the username of the Raspberry)*  
Then reboot: `sudo reboot`  
After restart, test that it works:  
`docker run hello-world`  
Install dependencies:  
`sudo apt-get install -y libffi-dev libssl-dev`  
`sudo apt-get install -y python3 python3-pip`  
`sudo apt-get remove python-configparser`  
Install docker-compose  
`sudo pip3 install docker-compose`  
And we're done.  
## 1. Clone git project
Create and go to a new folder:  
`mkdir ~/qmk && cd ~/qmk`  
Clone the RainbowPI project:  
`git clone https://github.com/hQamonky/RainbowPI.git`  
## 2. Build the docker container
Run the commands:  
`docker build --no-cache -t qmk_rainbowpi ~/qmk/RainbowPI`  
`docker run -p 8093:8080 -v ~/qmk/RainbowPI:/usr/src/app -d --name qmk_rainbowpi --device /dev/gpiomem qmk_rainbowpi`  
The container should now be up and running.  
You can test it by running `curl 127.0.0.1:8093/`. This should display the content of the 'API User Guide.md' file in a html format.  
## 3. Make the container run at startup
### Using cron
Edit the cron file: `sudo crontab -e`  
Add the following line at the end of the file:  
`@reboot docker start qmk_rainbowpi &`  
# Usage
## Start the container
`docker start qmk_rainbowpi`  
## Stop the container
`docker stop qmk_rainbowpi`  
## Restart the container
`docker restart qmk_rainbowpi`  
## Using the API
The API is documented [here](https://github.com/hQamonky/RainbowPI/blob/master/docs/API%20User%20Guide.md).  
You can access it from the / endpoint of the API server.  
You can also access the file directly in your folder at ~/qmk/RainbowPI/docs/API\ User\ Guide.md.  
## use different GPIO pn numbers
If you want to use different GPIO pin numbers thant the ones that I used, you will have to edit my source code.  
For Reference, I used:  
> GPIO17 for red  
> GPIO22 for green  
> GPIO24 for blue  

The file that you will have to edit is ~/qmk/RainbowPI/src/endpoints/__init__.py.  
Change the values of the constants `RED`, `GREEN` and `BLUE` to match your pin numbers.   
