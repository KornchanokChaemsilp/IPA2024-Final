from ncclient import manager
import xmltodict

m = manager.connect(
    host="10.0.15.61",
    port=830,
    username="admin",
    password="cisco",
    hostkey_verify=False
    )

def create():
    current_status = status()
    if current_status == "up" or current_status == "down":
        print("Cannot create: Interface loopback 66070001 (already exists)")
        return "Cannot create: Interface loopback 66070001"
    
    netconf_config = f"""
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <Loopback xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0" xc:operation="create">
            <name>66070001</name>
            <description>Loopback 66070001</description>
            <ip>
              <address>
                <primary>
                  <address>172.0.1.1</address>
                  <mask>255.255.255.0</mask>
                </primary>
              </address>
            </ip>
          </Loopback>
        </interface>
      </native>
    </config>
    """

    try:
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            print("Interface loopback 66070001 is created successfully")
            return "Interface loopback 66070001 is created successfully"
    except:
        print("Cannot create: Interface loopback 66070001")


def delete():
    current_status = status()
    if current_status == "no-return":
        print("Cannot delete: Interface loopback 66070001 (does not exist)")
        return "Cannot delete: Interface loopback 66070001"
    
    netconf_config = f"""
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <Loopback xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0" xc:operation="delete">
            <name>66070001</name>
          </Loopback>
        </interface>
      </native>
    </config>
    """

    try:
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            print("Interface loopback 66070123 is deleted successfully")
            return "Interface loopback 66070123 is deleted successfully"
    except:
        print("Error!")


def enable():

    current_status = status()
    if current_status == "no-return":
        print("Cannot enable: Interface loopback 66070001 (does not exist)")
        return "Cannot enable: Interface loopback 66070001"
    
    netconf_config = f"""
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <Loopback>
            <name>66070001</name>
            <shutdown xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="delete"/>
          </Loopback>
        </interface>
      </native>
    </config>
    """

    try:
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            print("Interface loopback 66070001 is enabled successfully")
            return "Interface loopback 66070001 is enabled successfully"
    except:
        print("Error!")


def disable():

    current_status = status()
    if current_status == "no-return":
        print("Cannot shutdown: Interface loopback 66070001 (does not exist)")
        return "Cannot shutdown: Interface loopback 66070001"
    
    netconf_config = f"""
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <Loopback>
            <name>66070001</name>
            <shutdown/>
          </Loopback>
        </interface>
      </native>
    </config>
    """

    try:
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            print("Interface loopback 66070123 is shutdowned successfully")
            return "Interface loopback 66070123 is shutdowned successfully"
    except:
        print("Error!")

def netconf_edit_config(netconf_config):
    return m.edit_config(target="running", config=netconf_config)


def status():
    netconf_filter = f"""
    <filter>
      <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <name>Loopback66070001</name>
        </interface>
      </interfaces-state>
    </filter>
    """

    try:
        # Use Netconf operational operation to get interfaces-state information
        netconf_reply = m.get(filter=netconf_filter)
        # print(netconf_reply)
        netconf_reply_dict = xmltodict.parse(netconf_reply.xml)

        # if there data return from netconf_reply_dict is not null, the operation-state of interface loopback is returned
        data = netconf_reply_dict.get('rpc-reply', {}).get('data')
        if data and data.get('interfaces-state') and data['interfaces-state'].get('interface'):
            interface_state = data['interfaces-state']['interface']
            # extract admin_status and oper_status from netconf_reply_dict
            admin_status = interface_state.get('admin-status')
            oper_status = interface_state.get('oper-status')
            if admin_status == 'up' and oper_status == 'up':
                return "up"
            elif admin_status == 'down' and oper_status == 'down':
                return "down"
        else: # no operation-state data
            return "no-return"
    except:
       print("Error!")

# ทดสอบ
# if __name__ == "__main__":
    
#     print("\n--- [STEP 1: Attempt to create (should work or fail if exists)] ---")
#     create()
    
#     print("\n--- [STEP 2: Attempt to create again (should fail)] ---")
#     create()
    
#     print("\n--- [STEP 3: Check Status] ---")
#     print(f"Current Status: {status()}")

#     print("\n--- [STEP 4: Disable interface] ---")
#     disable()

#     print("\n--- [STEP 5: Check Status] ---")
#     print(f"Current Status: {status()}")

#     print("\n--- [STEP 6: Enable interface] ---")
#     enable()

#     print("\n--- [STEP 7: Check Status] ---")
#     print(f"Current Status: {status()}")

#     print("\n--- [STEP 8: Delete interface] ---")
#     delete()

#     print("\n--- [STEP 9: Delete interface again (should fail)] ---")
#     delete()

#     print("\n--- [STEP 10: Check Status] ---")
#     print(f"Current Status: {status()}")

#     # Close the connection
#     m.close_session()
#     print("\n--- Connection Closed ---")