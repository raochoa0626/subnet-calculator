
import argparse
import sys
import ipaddress

def calc_network_info(cidr: str):
    net = ipaddress.ip_network(cidr, strict=False)
    data = {
        "version": net.version,
        "network": str(net.network_address),
        "prefixlen": net.prefixlen,
        "netmask": str(net.netmask) if hasattr(net, "netmask") else None,
        "hostmask": str(net.hostmask) if hasattr(net, "hostmask") else None,
        "num_addresses": net.num_addresses,
    }
    if net.version == 4:
        data.update({
            "broadcast": str(net.broadcast_address),
            "first_usable": str(list(net.hosts())[0]) if net.num_addresses >= 2 else None,
            "last_usable": str(list(net.hosts())[-1]) if net.num_addresses >= 2 else None,
        })
    return data

def main(argv=None):
    p = argparse.ArgumentParser(description="Subnet calculator")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--cidr", help="Single CIDR (e.g., 10.0.0.0/24)")
    g.add_argument("--file", help="File with one CIDR per line")
    p.add_argument("--summary", action="store_true", help="Print only summary lines")
    args = p.parse_args(argv)

    cidrs = []
    if args.cidr:
        cidrs = [args.cidr.strip()]
    else:
        with open(args.file) as fh:
            cidrs = [line.strip() for line in fh if line.strip()]

    for c in cidrs:
        try:
            info = calc_network_info(c)
        except Exception as e:
            print(f"[ERROR] {c}: {e}", file=sys.stderr)
            continue
        if args.summary:
            print(f"{c}: /{info['prefixlen']} • addrs={info['num_addresses']} • net={info['network']}")
        else:
            print(f"CIDR: {c}")
            for k, v in info.items():
                print(f"  {k}: {v}")
            print()

if __name__ == "__main__":
    main()
