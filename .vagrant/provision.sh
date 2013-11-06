#!/bin/bash

export DEBIAN_FRONTEND noninteractive
echo "APT::Get::Install-Recommends \"0\";" >> /etc/apt/apt.conf.d/99local
echo "APT::Get::Install-Suggests \"0\";" >> /etc/apt/apt.conf.d/99local
echo 'DPkg::Post-Invoke {"/bin/rm -f /var/cache/apt/archives/*.deb || true";};' | tee /etc/apt/apt.conf.d/no-cache
apt-get -qq update
apt-get install -y python-software-properties
add-apt-repository ppa:mumble/release
apt-get -qq update
apt-get install -y mumble-server python-zeroc-ice zeroc-ice
sed -i 's/^icesecretwrite=$/icesecretwrite=test/g' /etc/mumble-server.ini
/etc/init.d/mumble-server restart