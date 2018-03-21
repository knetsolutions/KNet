#!/bin/bash


export LC_ALL="en_US.UTF-8"

function check_ubuntu_version(){

    if [[ -x $(command -v apt-get 2>/dev/null) ]]; then
        sudo apt-get install -y lsb-release
        os_RELEASE=$(lsb_release -r -s)
        os_CODENAME=$(lsb_release -c -s)
        os_VENDOR=$(lsb_release -i -s)
        if [[ $os_RELEASE =~ 16.04 ]]; then
            echo "*************************"
            echo "Your OS is UBUNTU 16.04. "
            echo "******* Installation starts ........"
        else
            echo "*************************"            
            echo $os_VENDOR
            echo $os_CODENAME
            echo $os_RELEASE
            echo "Installation failed... Install supports only Ubuntu 16.04 version."
            exit 1
        fi
    else
       echo "Installation failed... Instal script supports only Ubuntu 16.04 version."
       exit 1
    fi
}



function u16_install_docker(){
        # install Docker
        sudo apt-get -y install apt-transport-https ca-certificates curl software-properties-common

        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
        sudo apt-key fingerprint 0EBFCD88
        sudo add-apt-repository \
                "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
                $(lsb_release -cs) \
                stable"
        sudo apt-get update
        sudo apt-get install -y docker-ce
}


function u16_install_ovs_docker(){
        # Download the ovs-docker script
        wget https://raw.githubusercontent.com/openvswitch/ovs/master/utilities/ovs-docker
        chmod a+rwx ovs-docker
        sudo cp ovs-docker /usr/bin/.

}


function u16_install_deps() {

	sudo apt-get update
	sudo apt-get install -y openvswitch-switch python python-dev python-pip build-essential
}


function u16_pull_imgs() {
	# Pull the Ubuntu dockeer images
	sudo docker pull knet/host
        sudo docker pull knet/web
        sudo docker pull knet/router
}


function verify_installation(){
        echo "------------Verifying openvswitch tool------------- "
        sudo ovs-vsctl show
        echo "------------Verifying ovs-docker tool------------- "
        sudo ovs-docker -h
        echo "------------Verifying docker ------------- "
        sudo docker  --version 
        echo "------------Verifying docker images------------- "
        sudo docker images
}

function install_u1604(){
    echo "*********** 1. Install OVS and other Dependencies ***************"
    u16_install_deps
    echo "*********** 2. Install Docker ***************"
    u16_install_docker
    echo "*********** 3. Install ovs_docker ***************"
    u16_install_ovs_docker
    echo "*********** 4. Download docker images ***************"
    pull_imgs
    echo "*********** Installation Completed ***************"

}


function install(){
    echo "*********** 0. Checking your OS compatibility  ****************"
    check_ubuntu_version
    install_u1604
}


install
verify_installation