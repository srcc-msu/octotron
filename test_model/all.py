# include all system wrappers
from octopy import *

# include all standard library files
from octopy_lib import *

NODES = 2

rack = GenID(CreateObject({"const" : {"type" : "rack"}}))

chassis = GenID(CreateObject(lib_network.GroupPingModule("chassis_nodes", NODES)
	, {"const" : {"type" : "chassis"}}))
OneToOne(rack, chassis, lib_links.link_contain)

nodes = GenID(CreateObjects(NODES
	, lib_collectd.NodeModule()
	, lib_collectd.ExperimentalNodeModule()
	, lib_network.PingModule()
	, lib_network.SshModule()
	, {"const" : {"type" : "node"}}))
OneToEvery(chassis, nodes, lib_links.link_contain)

disks = GenID(CreateObjects(NODES
	, lib_collectd.DiskModule()
	, lib_collectd.DiskProphecy()
	, {"const" : {"type" : "disk"}}))
EveryToEvery(nodes, disks, lib_links.link_contain, lib_links.link_cooling)

mountpoints = GenID(CreateObjects(NODES
	, lib_collectd.MountPointModule()
	, {"const" : {"type" : "mountpoint"}}))
EveryToEvery(nodes, mountpoints, lib_links.link_include)

cpus = GenID(CreateObjects(NODES
	, lib_collectd.CpuModule()
	, {"const" : {"type" : "cpu"}}))
EveryToEvery(nodes, cpus, lib_links.link_contain, lib_links.link_cooling)

memories = GenID(CreateObjects(NODES
	, lib_collectd.MemoryModule()
	, {"const" : {"type" : "memory", "req_mem" : 100}}))
EveryToEvery(nodes, memories, lib_links.link_contain, lib_links.link_cooling)

ib_cards = GenID(CreateObjects(NODES
	, lib_collectd.IBModule()
	, lib_collectd.IBProphecy()
	, {"const" : {"type" : "ib_card"}}))
EveryToEvery(nodes, ib_cards, lib_links.link_contain, lib_links.link_cooling)

eth_cards = GenID(CreateObjects(NODES
	, lib_collectd.EthModule()
	, lib_collectd.EthProphecy()
	, lib_eth.PortModule()
	, lib_eth.PortSpeedModule()
	, {"const" : {"type" : "eth_card", "speed_req" : 100}}))
EveryToEvery(nodes, eth_cards, lib_links.link_contain, lib_links.link_cooling)

queue = GenID(CreateObject(lib_drms.DrmsModule()
	, lib_network.GroupPingModule("queue_nodes", NODES)
	, {"const" : 
		{
			"tasks_running_min" : 1,
			"tasks_queued_min" : 1,
			"cpus_total" : 2,
			"cpus_free_max_pct" : 10,
			"cpus_blocked_max_pct": 10,
			"type" : "queue"
		}}))
OneToEvery(queue, nodes, lib_links.link_include)

eth_switch = GenID(CreateObject(lib_network.SnmpModule()
	, {"const" : {"type" : "eth_switch"}}))
OneToOne(rack, eth_switch, lib_links.link_contain)

eth_switch_ports = GenID(CreateObjects(NODES
	, lib_eth.PortModule()
	, lib_eth.PortDuplexModule()
	, lib_eth.PortSpeedModule()
	, lib_snmp_eth.EthPortSnmpModule()
	, {"const" : {"type" : "eth_switch_port", "speed_req" : 100}}))
OneToEvery(eth_switch, eth_switch_ports, lib_links.link_contain)

ib_switch = GenID(CreateObject(lib_network.SnmpModule()
	, {"const" : {"type" : "ib_switch"}}))
OneToOne(rack, ib_switch, lib_links.link_contain)

ib_switch_ports = GenID(CreateObjects(NODES
	, {"const" : {"type" : "ib_switch_port"}}))
OneToEvery(ib_switch, ib_switch_ports, lib_links.link_contain)

eth_links = EveryToEvery(eth_cards, eth_switch_ports, lib_links.link_eth
		, lib_eth.LinkModule())

panasas_system = GenID(CreateObject(lib_panasas.PanasasSystemModule()))

panasas_shelf = GenID(CreateObject(lib_panasas.PanasasShelfModule()))
OneToOne(rack, panasas_shelf, lib_links.link_contain)

panasas_blade = GenID(CreateObject(lib_panasas.PanasasBladeModule()))
OneToOne(panasas_shelf, panasas_blade, lib_links.link_contain)

panasas_volume = GenID(CreateObject(lib_panasas.PanasasVolumeModule()))

OneToOne(panasas_system, panasas_volume, lib_links.link_include)

ems_sensor = GenID(CreateObject(lib_snmp_ems.EmsSensorModule()
	, {"const" : {"type" : "ems_sensor"}}))
OneToOne(rack, ems_sensor, lib_links.link_contain)

ems_contact = GenID(CreateObject(lib_snmp_ems.EmsContactModule()
	, {"const" : {"type" : "ems_contact"}}))
OneToOne(rack, ems_contact, lib_links.link_contain)

fan = GenID(CreateObject(lib_snmp_fan.FanSnmpModule()
	, {"const" : {"type" : "fan"}}))
OneToOne(rack, fan, lib_links.link_contain)
