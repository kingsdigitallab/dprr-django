# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "puphpet/debian75-x64"

  config.vm.provision :shell, :path => ".vagrant_provisioning/vagrant.sh"

  config.vm.network :forwarded_port, guest: 8080, host: 8081
  config.vm.network :forwarded_port, guest: 8000, host: 8001
  config.vm.network :forwarded_port, guest: 5432, host: 15432
  config.vm.network :forwarded_port, guest: 80, host: 8002

  config.vm.provider "virtualbox" do |provider|
    provider.customize ["modifyvm", :id, "--memory", "512"]
  end

  config.vm.provider "vmware" do |provider|
    provider.customize ["modifyvm", :id, "--memory", "512"]
  end

  config.vm.define "dprr" do |machine|
    machine.vm.box = "puphpet/debian75-x64"
    machine.vm.hostname = "dprr.vagrant"
    machine.vm.network "private_network", ip: "192.168.101.20"
  end
end
