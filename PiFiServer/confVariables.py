hostapd_conf_dir = "/etc/hostapd/hostapd.conf"

hostapd_conf     = """
interface=wlan0
driver=nl80211
ssid={}
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase={}
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
"""
wifi_config_dir = "/etc/wpa_supplicant/wpa_supplicant.conf"

wifi_config ="""ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1
    network={{
        ssid="{}"
        psk="{}"
    }}"""


stop_ap_services  = "systemctl stop dnsmasq hostapd"
start_ap_serivces = "systemctl start dnsmasq hostapd"
damean_reload     = "sudo systemctl daemon-reload"
dhcpcd_restart     = "sudo service dhcpcd restart"


with open('dhcpcd.conf.orig','r') as r:
    wifi_dhcpd = r.read()

wifi_dhcpd_data   = """
interface wlan0
    static ip_address=192.168.4.1/24
    nohook wpa_supplicant"""


wifi_dhcpd_dir    = "/etc/dhcpcd.conf"
wifi_dhcpd_config = wifi_dhcpd + "{}"


with open('hostapd.orig','r') as r:
    hostapd_orig = r.read()

hostapd_config_data = 'DAEMON_CONF="/etc/hostapd/hostapd.conf"'
hostapd_dir    = "/etc/default/hostapd"
hostapd_config = hostapd_orig + "{}"
