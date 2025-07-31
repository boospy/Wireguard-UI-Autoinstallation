Wireguard-UI Autoinstallation
=============================

**You would like to show your appreciation for our help 8-o. Gladly. We thank you for your donation! ;)**

<a href="https://www.paypal.com/donate/?hosted_button_id=JTFYJYVH37MNE">
  <img src="https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif">
</a>

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/L3L813B3CV)

---

The entire project is documented in detail in [my wiki](https://deepdoc.at/dokuwiki/doku.php?id=vpn:ubuntu_lts_wireguard_wireguard-ui_fortigate_ein_sicheres_gespann).

Tested on [Ubuntu-Server 24.04 LTS](https://releases.ubuntu.com/noble/). 

With the installation script “setup-wireguard-zshshell.sh” you install [Wireguard UI](https://github.com/ngoduykhanh/wireguard-ui) including Docker and Nginx with TLS certificate for HTTPS on an Ubuntu server 24.04 LTS.
The certificate, key, and CA must be available on the server before installation. The default paths can be changed during installation:

### Default credentials:
+ Username: admin
+ Password: admin

### SSL Certificates:
 + Certificate: /docker/appdata/certs/wireguard-UI.crt
 + Private Key: /docker/appdata/certs/wireguard-UI.key
 + CA Certificate: /docker/appdata/certs/wireguard-UI-ca.crt

To start the installation process on your Ubuntu, simply download the installation script and run it:

~~~
wget https://git.osit.cc/public-projects/wireguard-ui-autoinstallation/-/raw/main/wireguard_UI_installer.py
chmod +x wireguard_UI_installer.py
./wireguard_UI_installer.py
~~~

### ZSH-Shell

<img src="https://deepdoc.at/dokuwiki/lib/exe/fetch.php?w=1000&tok=a6b145&media=vpn:wg-prompt.png" width="" height="256">

The [zsh-config](https://github.com/mh-firouzjah/zsh-config) project was used for this special ZSH shell. For easy installation Use my automatic installer:

~~~
wget https://git.osit.cc/public-projects/wireguard-ui-autoinstallation/-/raw/main/setup-wireguard-zshshell.sh
chmod +x setup-wireguard-zshshell.sh
./setup-wireguard-zshshell.sh
~~~