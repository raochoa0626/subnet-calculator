
import subnet_calc as sc

def test_calc_ipv4():
    data = sc.calc_network_info("192.168.1.0/24")
    assert data["version"] == 4
    assert data["network"] == "192.168.1.0"
    assert data["broadcast"] == "192.168.1.255"
    assert data["num_addresses"] == 256

def test_calc_ipv6():
    data = sc.calc_network_info("2001:db8::/64")
    assert data["version"] == 6
    assert data["network"].startswith("2001:db8::")
    assert data["num_addresses"] == 2**64
