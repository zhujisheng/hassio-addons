# Home Assistant Add-on: Raw WireGuard

WireGuard: fast, modern, secure VPN tunnel.

## What's the difference

What's the difference between this add-on and [Home Assistant Community Add-on: WireGuard](https://github.com/hassio-addons/addon-wireguard) ?

1. This add-on run in host-network mode, so, it's simpler and more powerful, but you should config it more carefully.
2. This add-on use the raw WireGuard configuration format, support all configuration file fields that [wg](https://man7.org/linux/man-pages/man8/wg.8.html) and [wg-quick](https://man7.org/linux/man-pages/man8/wg-quick.8.html) supports.

## About WireGuard

[WireGuard®](https://www.wireguard.com/) is an extremely simple yet fast and modern VPN that
utilizes state-of-the-art cryptography. It aims to be faster, simpler, leaner,
and more useful than IPsec, while avoiding the massive headache.

It intends to be considerably more performant than OpenVPN. WireGuard is
designed as a general-purpose VPN for running on embedded interfaces and
supercomputers alike, fit for many different circumstances.

Initially released for the Linux kernel, it is now cross-platform (Windows,
macOS, BSD, iOS, Android) and widely deployable,
including via an Hass.io add-on!

WireGuard is currently under heavy development, but already it might be
regarded as the most secure, easiest to use, and the simplest VPN solution
in the industry.
