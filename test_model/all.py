# include all system wrappers
from octopy import *

# include all standard library files
from octopy_lib import *

NODES = 2

nodes = GenID(CreateObjects(NODES
	, lib_collectd.NodeModule()
	, lib_collectd.ExperimentalNodeModule()
	, lib_network.PingModule()
	, lib_network.SshModule()
	, { "const" : {"type" : "node"}}))

disks = GenID(CreateObjects(NODES
	, lib_collectd.DiskModule()
	, lib_collectd.DiskProphecy()
	, { "const" : {"type" : "disk"}}))

mountpoints = GenID(CreateObjects(NODES
	, lib_collectd.MountPointModule()
	, { "const" : {"type" : "mountpoint"}}))

cpus = GenID(CreateObjects(NODES
	, lib_collectd.CpuModule()
	, { "const" : {"type" : "cpu"}}))

memorys = GenID(CreateObjects(NODES
	, lib_collectd.MemoryModule()
	, { "const" : {"type" : "memory", "req_mem" : 100}}))

ib_cards = GenID(CreateObjects(NODES
	, lib_collectd.IBModule()
	, lib_collectd.IBProphecy()
	, { "const" : {"type" : "ib_card"}}))

eth_cards = GenID(CreateObjects(NODES
	, lib_collectd.EthModule()
	, lib_collectd.EthProphecy()
	, lib_eth.PortModule()
	, lib_eth.PortSpeedModule()
	, { "const" : {"type" : "eth_card", "speed_req" : 100}}))

queue = GenID(CreateObject(lib_drms.DrmsModule()
	, { "const" : 
		{
			"tasks_running_min" : 1,
			"tasks_queued_min" : 1,
			"cpus_total" : 2,
			"cpus_free_max_pct" : 10,
			"cpus_blocked_max_pct": 10,
			"type" : "queue"
		}}))

eth_switch = GenID(CreateObject(lib_network.SnmpModule()
	, { "const" : {"type" : "eth_switch"}}))
eth_switch_ports = GenID(CreateObjects(NODES
	, lib_eth.PortModule()
	, lib_eth.PortDuplexModule()
	, lib_eth.PortSpeedModule()
	, lib_snmp_eth.EthPortSnmpModule()
	, { "const" : {"type" : "eth_switch_port", "speed_req" : 100}}))

ib_switch = GenID(CreateObject(lib_network.SnmpModule()
	, { "const" : {"type" : "ib_switch"}}))
ib_switch_ports = GenID(CreateObjects(NODES
	, { "const" : {"type" : "ib_switch_port"}}))

eth_links = EveryToEvery(eth_cards, eth_switch_ports, lib_links.link_eth
		, lib_eth.LinkModule())

panasas_system = GenID(CreateObject(lib_panasas.PanasasSystemModule()))
panasas_shelf = GenID(CreateObject(lib_panasas.PanasasShelfModule()))
panasas_blade = GenID(CreateObject(lib_panasas.PanasasBladeModule()))
panasas_volume = GenID(CreateObject(lib_panasas.PanasasVolumeModule()))

ems_sensor = GenID(CreateObject(lib_snmp_ems.EmsSensorModule()
	, { "const" : {"type" : "ems_sensor"}}))
ems_contact = GenID(CreateObject(lib_snmp_ems.EmsContactModule()
	, { "const" : {"type" : "ems_contact"}}))

fan = GenID(CreateObject(lib_snmp_fan.FanSnmpModule()
	, { "const" : {"type" : "fan"}}))
