#!/usr/bin/python

import sys

try:
    import json
except:
    import simplejson as json

def add_host(vm_name, group, inventory, flavor=None):

  if not group in inventory:
    inventory[group] = {
      'hosts' : [],
    }

  if not vm_name in inventory[group]:
    inventory[group]['hosts'].append(vm_name)

  if not vm_name in inventory['_meta']:
    inventory['_meta']['hostvars'][vm_name] = {}
    if flavor:
      inventory['_meta']['hostvars'][vm_name]['flavor_id'] = flavor

def main(args):

  f = open('hosts')

  # initialize the inventory
  inventory = {}
  inventory['_meta'] = {}
  inventory['_meta']['hostvars'] = {}

  for line in f.readlines():
    flavor = None
    if line == "[openstack_instances]\n":
      group = line.replace("[", "")
      group = group.replace("]", "")
      group = group.replace("\n", "")
    # FIXME: test cases
    elif line.startswith("[") or line == "\n":
      break
    else:
      server = line.split()
      name = server[0]
      # FIXME
      # flavor_id=1
      flavor = server[1].split("=")[1]
      # group=somegroup
      group = server[2].split("=")[1]

      add_host(vm_name=name, group=group, inventory=inventory )
      add_host(vm_name=name, group='openstack_instances', inventory=inventory)
      # add flavor last
      add_host(vm_name=name, group='undefined', inventory=inventory, flavor=flavor)

  print json.dumps(inventory, sort_keys=True, indent=4)

if __name__ == "__main__":
    main(sys.argv)
