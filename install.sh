apt-get update
apt-get upgrade

apt-get install git dnsmasq hostapd python3-flask python3-passlib python3-rpi.gpio

git clone https://github.com/doct0rr/PiFi.git
sleep 1
cd PiFi
sleep 1
echo "stopping dnsmasq and hostapd"
systemctl stop dnsmasq
systemctl stop hostapd

sleep 1
echo "copying dhcpd and resetting it"
cp /etc/dhcpcd.conf dhcpcd.conf.orig
chmod 777 dhcpcd.conf.orig
cat dhcpcd.conf  >> /etc/dhcpcd.conf
systemctl daemon-reload
service dhcpcd restart

sleep 1
echo "setting up dnsmasq"
mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig  

sleep 1
cp dnsmasq.conf /etc/dnsmasq.conf
chmod 777 /etc/dnsmasq.conf

sleep 1
echo "setting hostapd..conf"
cp hostapd.conf /etc/hostapd/hostapd.conf
chmod 777 /etc/hostapd/hostapd.conf

sleep 1
echo "setting hostapd"
chmod 777 /etc/default/hostapd 
cp /etc/default/hostapd hostapd.orig
cat hostapd >> /etc/default/hostapd

sleep 1
echo "starting everything up"
systemctl start hostapd

sleep 1
systemctl start dnsmasq


cp -R PiFiServer /etc/PiFi

cp pifi_reset.service /etc/systemd/system/pifiReset.service

cp pifi_service.service /etc/systemd/system/pifiWeb.service

systemctl start pifiReset.service
systemctl enable pifiReset.service

systemctl start pifiWeb.service



if pwd | grep -q 'PiFi'; then 
    while true; do
        read -p "Do you wish to delete the install files?" yn
        case $yn in
            [Yy]* )  echo "Deleting Install files";
                     OUTPUT="$(pwd)"; 
                     sudo rm -R "${OUTPUT}";  
                     break;;

            [Nn]* ) echo "Installation Complete"; exit;;
            * ) echo "Please answer yes or no.";;
        esac
    done

else 
    echo "Installation Complete"; 
fi
