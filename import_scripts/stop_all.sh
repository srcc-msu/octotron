#!/bin/bash
set -u

screen -S selftest -X quit

screen -S collectd -X quit

screen -S snmp_eth_switch -X quit
screen -S snmp_check -X quit
screen -S snmp_chiller -X quit
screen -S snmp_emu -X quit
screen -S snmp_fire -X quit
screen -S snmp_rkp -X quit

screen -S ping -X quit
screen -S snmp -X quit
