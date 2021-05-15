# Home Assistant Add-on: Raw WireGuard

## Configuration

If you are familiar with WireGuard's configuration, everything will be very easy.

The add-on's configuration looks like this:

```yaml
# add-on Raw WireGuard configuration example
interface:
  PrivateKey: yAnz5TF+lXXJte14tji3zlMNq+hd2rYUIgJBgB3fBmk=
  Address: 172.27.66.8/24
peers:
  - PublicKey: rJ0ZpE/paYS1StWstO78kpGQV4G3WmjmWY93lA7bK1I=
    EndPoint: my_vpn_server:51820
    AllowedIPs: 172.27.66.3/32
  - PublicKey: QNLXV8lrsPnKOd011DO8g5DWyad6iHJDSVOD6yOqjiE=
    EndPoint: my_vpn_server2:51820
    AllowedIPs: 172.27.66.5/32
```
**Note**: *This is just an example, don't copy and paste it! Create your own!*

- **Option**: `interface_name` (optional)

  The interface name of WireGuard network. If not set, `wg0` will be used.

- **Option**: `interface`

  The `[Interface]` section in WireGuard configuration file.

  It includes:

  + `PrivateKey`
  + `ListenPort` (optional)
  + `FwMark` (optional)
  + `Address` (optional)
  + `DNS` (optional)
  + `MTU` (optional)
  + `Table` (optional)
  + `PreUp` (optional)
  + `PostUp` (optional)
  + `PreDown` (optional)
  + `PostDown` (optional)
  + `SaveConfig` (optional)

- **Option**: `peers`

  The `[Peer]` sections in WireGuard configuration file.

  It includes:

  + `PublicKey`
  + `PreSharedKey` (optional)
  + `AllowedIPs` (optional)
  + `EndPoint` (optional)
  + `PersistentKeepalive` (optional)

**All items inclueded in `interface` and `peers` are the same as what is included in the WireGuard configuration file.**

**You can get details from [wg](https://man7.org/linux/man-pages/man8/wg.8.html) and [wg-quick](https://man7.org/linux/man-pages/man8/wg-quick.8.html)'s man page.**

## Generate Key Pairs

- WireGuard installed Linux

  `wg genkey | tee privatekey | wg pubkey > publickey`

  Run the command, then the keys will be in file `privatekey` and `publickey`.

- GUI WireGuard installed Windows/Android/IOS

  You can generate the key pair on the GUI. Copy them, then, paste where it's needed.

- Online

  [https://www.wireguardconfig.com/](https://www.wireguardconfig.com/)

  Generate Config, then copy private and public key in the configuration generated, paste where it's needed.

## Some Typical Configurations

#### (1) Add-on As a VPN Client

<img src="https://github.com/zhujisheng/Home-Assistant-DIY/raw/master/04.%E5%85%AC%E7%BD%91%E8%AE%BF%E9%97%AE%E7%AF%87/images/wg_asclient.png" width="60%">

- Add-on Configuration

  ```yaml
  interface:
    PrivateKey: my_add-on_private_key
    Address: 172.27.66.1/24
  peers:
    - PublicKey: the_vpn_server_public_key
      EndPoint: "x.x.x.x:51820"
      PersistentKeepalive: 25
      AllowedIPs: "172.27.66.2/32"
  ```

  *`x.x.x.x` is the IP of VPN Server*

- VPN Server WireGuard Configuration

  ```conf
  [Interface]
  PrivateKey = the_vpn_server_private_key
  Address = 172.27.66.2/24
  ListenPort = 51820

  [Peer]
  PublicKey = my_add-on_public_key
  AllowedIPs = 172.27.66.1/32

  [Peer]
  ......
  ```

After the add-on started, you can ping `172.27.66.1` from the VPN server, and ping `172.27.66.2` from the HomeAssistant host.

#### (2) HomeAssistant host visit Internet via VPN

<img src="https://github.com/zhujisheng/Home-Assistant-DIY/raw/master/04.%E5%85%AC%E7%BD%91%E8%AE%BF%E9%97%AE%E7%AF%87/images/wg_haoutviavpntunnel.png" width="80%">

- Add-on Configuration

  Add `AllowedIPs: "0.0.0.0/0"` in `peer` section.

  ```yaml
  interface:
    ......
  peers:
    - PublicKey: the_vpn_server_public_key
      ......
      AllowedIPs: "0.0.0.0/0"
      ......
  ```

  *If you set `AllowedIPs: "0.0.0.0/0"`, it's suggested to run `sysctl net.ipv4.conf.all.src_valid_mark=1` on the host. Or in some very rare cases, when `rp_filter` is set to `1` in the host network, network may block.*

  *This is because `sysctl -q net.ipv4.conf.all.src_valid_mark=1` has been commented out in `wg-quick` script in this add-on, which should run when `AllowedIPs: "*/0"` configged. `--privileged` parameter is not provided by HomeAssistant Supervisor add-on's configuration, and without which, setting system parameter by `sysctl` leads to error in docker containers.*

  *Another way to avoid `AllowedIPs: "0.0.0.0/0"` is `AllowdIPs: "0.0.0.0/1, 128.0.0.0/1"`, which means the whole IP addresses also. However, in such configuration, you will have to add route manually to prevent endless loop of the VPN package wrapping. The configuration example shows below:*

  ```yaml
  interface:
    ....
    PostUp: "ip -4 route add x.x.x.x/32 via 192.168.3.1 dev wlan0"
    PostDown: "ip -4 route del x.x.x.x/32 via 192.168.3.1 dev wlan0"
  peers:
    - ......
      AllowedIPs: "0.0.0.0/1, 128.0.0.0/1"
  ```
  *`x.x.x.x` is IP of the VPN Server, `192.168.3.1` is the local gateway of HomeAssistant host.*

- VPN Server Configuration

  The VPN Server must have `ip_forward` and NAT configured.

  + `ip_forward`

    ```sh
    sudo sysctl -w net.ipv4.ip_forward=1
    echo "net.ipv4.ip_forward = 1" | sudo tee -a /etc/sysctl.conf
    sudo sysctl -p /etc/sysctl.conf
    ```
  + NAT

    You can open NAT in the wireguard's `PostUp` script, or run it by any other means on the server.

    ```
    [Interface]
    ....
    PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -A FORWARD -o %i -j ACCEPT; iptables -t nat -I POSTROUTING -s 172.27.66.0/24 -j MASQUERADE
    PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -D FORWARD -o %i -j ACCEPT; iptables -t nat -D POSTROUTING -s 172.27.66.0/24 -j MASQUERADE
    ```


#### (3) HomeAssistant As local gateway

<img src="https://github.com/zhujisheng/Home-Assistant-DIY/raw/master/04.%E5%85%AC%E7%BD%91%E8%AE%BF%E9%97%AE%E7%AF%87/images/wg_asgateway.png">

- Add-on Configuration

  ```yaml
  interface:
    ......
    PostUp: "iptables -A FORWARD -i %i -j ACCEPT; iptables -A FORWARD -o %i -j ACCEPT; iptables -t nat -A POSTROUTING -o %i -j MASQUERADE"
    PostDown: "iptables -D FORWARD -i %i -j ACCEPT; iptables -D FORWARD -o %i -j ACCEPT; iptables -t nat -D POSTROUTING -o %i -j MASQUERADE"
  peers:
    - ......
  ```

  *Combine this configuration with `HomeAssistant host visit Internet via VPN` above, you can now let devices in local network visit Internet via VPN tunnel, by setting their network gateway to HomeAssistant host IP.*

#### (4) Access HomeAssistant's 8123 from Internet

<img src="https://github.com/zhujisheng/Home-Assistant-DIY/raw/master/04.%E5%85%AC%E7%BD%91%E8%AE%BF%E9%97%AE%E7%AF%87/images/wg_openha2internet.png" width="80%">

You can do by nginx on the VPN server, config as below:

```
server {
    listen 443;
    server_name your_domain_name;

    ssl on;
    ssl_certificate path_to_fullchain.pem;
    ssl_certificate_key path_to_privkey.pem;
    ssl_prefer_server_ciphers on;

    location / {
        proxy_pass http://172.27.66.1:8123;
        proxy_set_header Host $host;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

 *`your_domain_name` is the domain name of your homeassistant, which should resolved to IP of the VPN Server. `path_to_fullchain.pem` and `path_to_privkey.pem` is the certification and private key file of the website.*

#### (5) Visit Local Network Via VPN

<img src="https://github.com/zhujisheng/Home-Assistant-DIY/raw/master/04.%E5%85%AC%E7%BD%91%E8%AE%BF%E9%97%AE%E7%AF%87/images/wg_openlocal2vpn.png" width="80%">

- Add-on Configuration

  ```yaml
  interface:
    ......
    PostUp: "iptables -A FORWARD -i %i -j ACCEPT; iptables -A FORWARD -o %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE"
    PostDown: "iptables -D FORWARD -i %i -j ACCEPT; iptables -D FORWARD -o %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE"
  peers:
    - ......
  ```
  *`eth0` is the HomeAssistant host interface to local network*

- VPN peers

  ```
  [Interface]
  ......

  [Peer]
  PublicKey = my_add-on_public_key
  ......
  AllowedIPs: "172.27.66.1/32; 192.168.3.0/24"
  ```

  *`192.168.3.0/24 is the local network where HomeAssistant host located.`*

#### (6) Add-on As a VPN Server

<img src="https://github.com/zhujisheng/Home-Assistant-DIY/raw/master/04.%E5%85%AC%E7%BD%91%E8%AE%BF%E9%97%AE%E7%AF%87/images/wg_asserver.png" width="70%">

- Add-on Configuration

  ```yaml
  interface:
    PrivateKey: my_add-on_private_key
    Address: 172.27.66.1/24
    ListenPort: 51820
  peers:
    - PublicKey: vpn_client_1_public_key
      AllowedIPs: 172.27.66.n1/32
    - PublicKey: vpn_client_2_public_key
      AllowedIPs: 172.27.66.n2/32
    - PublicKey: vpn_client_3_public_key
      AllowedIPs: 172.27.66.n3/32
    - ......
  ```
  *`172.27.66.n?` is the IP of each VPN client*

- VPN Client WireGuard Configuration

  ```conf
  [Interface]
  PrivateKey = vpn_client_n_private_key
  Address = 172.27.66.n/24

  [Peer]
  PublicKey = my_add-on_public_key
  EndPoint = y.y.y.y:51820
  PersistentKeepalive = 25
  ```

  *HomeAssistant opens UDP port 51820, which should be accessible from internet by connecting to `y.y.y.y:51820`(You may need a pulic IP, and do some port mapping on your local router)*
