#!/usr/bin/with-contenv bashio
# ==============================================================================
# Home Assistant Add-on: Raw WireGuard
# Creates the interface configuration
# ==============================================================================

declare interface
declare config
declare rp_filter1
declare src_valid_mark

if [[ $(</proc/sys/net/ipv4/ip_forward) -eq 0 ]]; then
    bashio::log.warning
    bashio::log.warning "IP forwarding is disabled on the host system!"
    bashio::log.warning "You can still use WireGuard, however, it will not"
    bashio::log.warning "forwrd any IP package, so it will not act as a"
    bashio::log.warning "gateway."
    bashio::log.warning
fi

# Comment out the code which will crash
sed -i 's/^[^#].*sysctl -q net.ipv4.conf.all.src_valid_mark=1*/#&/g' /usr/bin/wg-quick

set +o errexit
rp_filter1=$(sysctl net.ipv4.conf | grep "\.rp_filter = 1")
src_valid_mark=$(sysctl -n net.ipv4.conf.all.src_valid_mark)
if [[ -n "${rp_filter1}" && ${src_valid_mark} = "0" ]] ; then
    bashio::log.warning
    bashio::log.warning "${rp_filter1}"
    bashio::log.warning
    bashio::log.warning "\`rp_filter\` is set to 1 on the host system!"
    bashio::log.warning "You can still use WireGuard, however, if you set"
    bashio::log.warning "\`0.0.0.0/0\` in any peer's \`EndPoint\`, it"
    bashio::log.warning "may lead to traffic block."
    bashio::log.warning
fi
set -o errexit

# Get interface and config file location
interface="wg0"
if bashio::config.has_value "interface_name"; then
    interface=$(bashio::config "interface_name")
fi

config="/etc/wireguard/${interface}.conf"
if ! bashio::fs.directory_exists '/etc/wireguard'; then
    mkdir -p /etc/wireguard ||
        bashio::exit.nok "Could not create /etc/wireguard/ !"
fi

# Finish up the [Interface] configuration
{
    echo "[Interface]"

    echo "PrivateKey = $(bashio::config "interface.PrivateKey")"

    bashio::config.has_value "interface.ListenPort" && echo "ListenPort = $(bashio::config "interface.ListenPort")"

    bashio::config.has_value "interface.FwMark" && echo "FwMark = $(bashio::config "interface.FwMark")"

    bashio::config.has_value "interface.Address" && echo "Address = $(bashio::config "interface.Address")"

    bashio::config.has_value "interface.DNS" && echo "DNS = $(bashio::config "interface.DNS")"

    bashio::config.has_value "interface.MTU" && echo "MTU = $(bashio::config "interface.MTU")"

    bashio::config.has_value "interface.Table" && echo "Table = $(bashio::config "interface.Table")"

    bashio::config.has_value "interface.PreUp" && echo "PreUp = $(bashio::config "interface.PreUp")"

    bashio::config.has_value "interface.PostUp" && echo "PostUp = $(bashio::config "interface.PostUp")"

    bashio::config.has_value "interface.PreDown" && echo "PreDown = $(bashio::config "interface.PreDown")"

    bashio::config.has_value "interface.PostDown" && echo "PostDown = $(bashio::config "interface.PostDown")"

    bashio::config.has_value "interface.SaveConfig" && bashio::config.true "interface.SaveConfig" && echo "SaveConfig = true"

    # End configuration file with an empty line
    echo ""
} > "${config}"

# Fetch all the peers
for peer in $(bashio::config 'peers|keys'); do

    # Start writing peer information in server config
    {
        echo "[Peer]"

        echo "PublicKey = $(bashio::config "peers[${peer}].PublicKey")"

        bashio::config.has_value "peers[${peer}].PreSharedKey" \
            && echo "PreSharedKey = $(bashio::config "peers[${peer}].PreSharedKey")"

        bashio::config.has_value "peers[${peer}].AllowedIPs" \
            && echo "AllowedIPs = $(bashio::config "peers[${peer}].AllowedIPs")"

        bashio::config.has_value "peers[${peer}].EndPoint" \
            && echo "EndPoint = $(bashio::config "peers[${peer}].EndPoint")"

        bashio::config.has_value "peers[${peer}].PersistentKeepalive" \
            && echo "PersistentKeepalive = $(bashio::config "peers[${peer}].PersistentKeepalive")"

        echo ""
    } >> "${config}"

done