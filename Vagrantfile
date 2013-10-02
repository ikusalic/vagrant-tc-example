# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure('2') do |config|
  config.vm.box = 'precise64cloudimagesubuntu'
  config.vm.box_url = 'http://cloud-images.ubuntu.com/precise/current/precise-server-cloudimg-vagrant-amd64-disk1.box'

  config.vm.provision :shell, :inline => <<-HERE
    apt-get install cgroup-lite
    modprobe cls_cgroup
    echo 'cls_cgroup' >> /etc/modules
    cgroups-umount
    cgroups-mount

    apt-get install iproute
    tc qdisc add dev eth0 root handle 1:0 htb default 1
    tc class add dev eth0 parent 1:0 classid 1:1 htb rate 80kbit burst 2k
    tc qdisc add dev eth0 parent 1:1 handle 2:0 drr
    tc class add dev eth0 parent 2:0 classid 2:1 drr
    tc filter add dev eth0 parent 2:0 prio 20 handle 1 basic flowid 2:1
    tc class add dev eth0 parent 2:0 classid 2:2 drr
    tc filter add dev eth0 parent 2:0 prio 10 handle 2 cgroup
    echo '0x00020001' > /sys/fs/cgroup/net_cls/net_cls.classid
    mkdir /sys/fs/cgroup/net_cls/test_group
    echo '0x00020002' > /sys/fs/cgroup/net_cls/test_group/net_cls.classid

    nohup python /vagrant/attack.py > /dev/null 2>&1 &
    echo $! > /sys/fs/cgroup/net_cls/test_group/tasks
  HERE
end
