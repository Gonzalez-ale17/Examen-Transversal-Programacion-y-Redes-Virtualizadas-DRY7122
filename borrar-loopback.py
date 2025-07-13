from ncclient import manager
import xmltodict
import json

router = {
    "host": "192.168.56.104",
    "port": 830,
    "username": "cisco",
    "password": "cisco123!",
    "hostkey_verify": False
}

with manager.connect(**router) as m:
    print("Conexion NETCONF establecida con el router")

    borrar_loopback = """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <Loopback operation="delete">
            <name>11</name>
          </Loopback>
        </interface>
      </native>
    </config>
    """

    m.edit_config(target="running", config=borrar_loopback)
    print("Loopback11 eliminada")

    crear_loopback22 = """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <Loopback>
            <name>22</name>
            <ip>
              <address>
                <primary>
                  <address>22.22.22.22</address>
                  <mask>255.255.255.255</mask>
                </primary>
              </address>
            </ip>
            <shutdown/>
          </Loopback>
        </interface>
      </native>
    </config>
    """

    m.edit_config(target="running", config=crear_loopback22)
    print("Loopback22 con IP 22.22.22.22/32 apagada")

    filtro_interfaces = """
    <filter>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface/>
      </native>
    </filter>
    """

    respuesta = m.get_config(source="running", filter=filtro_interfaces)
    datos_xml = xmltodict.parse(respuesta.xml)
    print("Interfaces en formato JSON:")
    print(json.dumps(datos_xml, indent=2))
