from netmiko import ConnectHandler

router = {
    "device_type": "cisco_ios",
    "host": "192.168.56.104",
    "username": "cisco",
    "password": "cisco123!",
}

net_connect = ConnectHandler(**router)
print("conexion al router establecida.")

config_commands = [
    "router eigrp grupo1",
    "address-family ipv4 autonomous-system 100",
    "network 192.168.56.0 0.0.0.255",
    "network 11.11.11.11 0.0.0.0",
    "network 22.22.22.22 0.0.0.0",
    "passive-interface default",
    "no passive-interface Loopback0",
    "no passive-interface Loopback22",
    "exit-address-family",
    "address-family ipv6 autonomous-system 100",
    "af-interface Loopback0",
    "no shutdown",
    "exit-af-interface",
    "af-interface Loopback22",
    "no shutdown",
    "exit-af-interface",
    "passive-interface default",
    "no passive-interface Loopback0",
    "no passive-interface Loopback22",
    "exit-address-family"
]

print("configurando EIGRP")
output = net_connect.send_config_set(config_commands)
print(output)

show_commands = [
    ("EIGRP config", "show running-config | section eigrp"),
    ("interfaces IPv4", "show ip interface brief"),
    ("interfaces IPv6", "show ipv6 interface brief"),
    ("running config", "show running-config"),
    ("versión del sistema", "show version"),
]

print("resultados de comandos show")
for descripcion, comando in show_commands:
    print(f"\n--- {descripcion} ---")
    output = net_connect.send_command(comando)
    print(output)

net_connect.disconnect()
