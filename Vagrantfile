# -*- mode: ruby -*-
# vi: set ft=ruby :
# vi: set nu :
VAGRANTFILE_API_VERSION = "2"

current_dir = File.dirname(__FILE__)
ubuntu_box_name = 'ubuntu/precise64'

machine_configs = {
  :lxc => {
    :bridge => false,
    :private_ip => "192.168.33.10",
    :ram => 1000,
    :forward_port => [ [5000, 5000] ],
    :fabtask => ['lxc_host'],
    :box_name => ubuntu_box_name,
  }
}

Vagrant.configure(VAGRANTFILE_API_VERSION) do |global_config|
  machine_configs.each_pair do |name, options|
    global_config.vm.define name do |config| 
      config.vm.provision "shell", path: options[:shell_script] if options.has_key?(:shell_script)
      config.vm.box = options[:box_name]
      config.vm.host_name = options[:hostname]
      config.vm.network :private_network, ip: options[:private_ip]
      config.vm.network "forwarded_port", guest: options[:forward_port][0], host: options[:forward_port][1]
      
      config.vm.provider "virtualbox" do |v|
        v.memory = options[:ram]
        v.customize ["modifyvm", :id, "--cpuexecutioncap", "100"]
        v.gui = false
        v.cpus = 4
      end

      if options.has_key?(:fabtask) and not options[:fabtask] == []
        config.vm.provision "fabric" do |fabric|
          fabric.tasks = options[:fabtask]
          fabric.fabfile_path = "./fabfile.py"
        end
      end

    end
  end
end
