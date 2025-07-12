from ncclient import manager

router = {
    "host": "192.168.56.104",
    "port": 830,
    "username": "cisco",
    "password": "cisco123!",
    "hostkey_verify": False
}

with manager.connect(**router) as m:
    print("Conexion NETCONF-Router exitosa")
    print("Capacidades del servidor:")
    for cap in m.server_capabilities:
        print(cap)

    config_hostname = """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <hostname>gonzalez-munoz</hostname>
      </native>
    </config>
    """

    m.edit_config(target="running", config=config_hostname)
    print("Hostname cambiado a gonzalez-munoz")

    config_loopback = """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <Loopback>
            <name>11</name>
            <ip>
              <address>
                <primary>
                  <address>11.11.11.11</address>
                  <mask>255.255.255.255</mask>
                </primary>
              </address>
            </ip>
          </Loopback>
        </interface>
      </native>
    </config>
    """

    m.edit_config(target="running", config=config_loopback)
    print("Loopback11 configurada con IP 11.11.11.11/32")
