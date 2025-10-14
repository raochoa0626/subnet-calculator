# subnet_calc/__main__.py
import argparse
from . import calc_network_info  # import from __init__

def main():
    p = argparse.ArgumentParser(description="IPv4/IPv6 subnet calculator")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--cidr", help="CIDR like 192.168.1.130/26 or 2001:db8::/64")
    g.add_argument("--file", help="Path to a file with one CIDR per line")
    p.add_argument("--summary", action="store_true", help="Print one-line summary per CIDR")
    args = p.parse_args()

    def print_one(c):
        info = calc_network_info(c.strip())
        if args.summary:
            # Compact line; adjust columns if you like
            fields = [
                info["cidr"],
                f"mask={info.get('mask_ddn','-')}",
                f"net={info['network']}",
                f"bcast={info['broadcast'] if info['broadcast'] is not None else '-'}",
                f"usable={info['usable']}",
            ]
            print(" | ".join(map(str, fields)))
        else:
            print(f"Input:     {info['cidr']}")
            if "mask_ddn" in info:
                print(f"Mask:      {info['mask_ddn']} (/{info['prefix']})")
                print(f"Wildcard:  {info['wildcard']}")
            else:
                print(f"Prefix:    /{info['prefix']}")
            print(f"Network:   {info['network']}")
            print(f"Broadcast: {info['broadcast']}")
            print(f"Usable:    {info['first']} - {info['last']} ({info['usable']})")
            print()

    if args.cidr:
        print_one(args.cidr)
    else:
        with open(args.file) as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                print_one(line)

if __name__ == "__main__":
    main()
