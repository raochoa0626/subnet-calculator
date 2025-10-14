# subnet_calc/__init__.py
from __future__ import annotations
import ipaddress
from typing import Dict, Optional, Union

__all__ = ["calc_network_info"]

def _wildcard(mask_ddn: str) -> str:
    # Inverse of dotted-decimal IPv4 mask
    return ".".join(str(255 - int(o)) for o in mask_ddn.split("."))

def calc_network_info(cidr: str) -> Dict[str, Union[str, int, None]]:
    """
    Return a dict describing the IPv4/IPv6 network for the given CIDR.
    Keys (superset; some are IPv4-only):
      version, cidr, prefix, network, total,
      broadcast (None for IPv6),
      mask_ddn, wildcard (IPv4 only),
      first, last, usable
    """
    net = ipaddress.ip_network(cidr, strict=False)

    info: Dict[str, Union[str, int, None]] = {
        "version": net.version,
        "cidr": str(net.with_prefixlen),
        "prefix": net.prefixlen,
        "network": str(net.network_address),
        "total": net.num_addresses,
        "num_addresses": net.num_addresses,
    }

    if net.version == 4:
        mask_ddn = str(net.netmask)
        info["mask_ddn"] = mask_ddn
        info["wildcard"] = _wildcard(mask_ddn)
        info["broadcast"] = str(net.broadcast_address)

        if net.prefixlen == 32:
            # Single host
            info.update(first=str(net.network_address), last=str(net.network_address), usable=1)
        elif net.prefixlen == 31:
            # RFC 3021 point-to-point: both usable
            first = net.network_address
            last = net.broadcast_address
            info.update(first=str(first), last=str(last), usable=2)
        else:
            first_int = int(net.network_address) + 1
            last_int = int(net.broadcast_address) - 1
            usable = max(net.num_addresses - 2, 0)
            info.update(
                first=str(ipaddress.IPv4Address(first_int)) if usable > 0 else "N/A",
                last=str(ipaddress.IPv4Address(last_int)) if usable > 0 else "N/A",
                usable=usable,
            )
    else:
        # IPv6: no broadcast; compute first/last arithmetically
        info["broadcast"] = None
        n = int(net.network_address)
        total = net.num_addresses
        if total == 1:
            info.update(first=str(net.network_address), last=str(net.network_address), usable=1)
        else:
            first = ipaddress.IPv6Address(n + 1)
            last = ipaddress.IPv6Address(n + total - 1)
            # "usable" is not the same concept in IPv6; keep simple for tool/tests
            info.update(first=str(first), last=str(last), usable=total)

    return info
