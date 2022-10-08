[![Actions Status - Master](https://github.com/juju4/ansible-cartography/workflows/AnsibleCI/badge.svg)](https://github.com/juju4/ansible-cartography/actions?query=branch%3Amaster)
[![Actions Status - Devel](https://github.com/juju4/ansible-cartography/workflows/AnsibleCI/badge.svg?branch=devel)](https://github.com/juju4/ansible-cartography/actions?query=branch%3Adevel)

# cartography ansible role

Setup cartography server, a Python tool that consolidates infrastructure assets and the relationships between them in an intuitive graph view powered by a Neo4j database.
* https://github.com/lyft/cartography
* https://lyft.github.io/cartography/

## Requirements & Dependencies

### Ansible
It was tested on the following versions:
 * 2.12

### Operating systems

Tested on Ubuntu 20.04, 22.04.

## Example Playbook

Just include this role in your list.
For example

```
- host: myhost
  roles:
    - juju4.cartography
```

See also docs folder for example playbooks for Azure and Digital Ocean

## Variables

TBD

## Continuous integration

```
$ pip install molecule docker
$ molecule test
$ MOLECULE_DISTRO=ubuntu:20.04 molecule test --destroy=never
```

## Troubleshooting & Known issues

* cartography is executed through systemd timer (can be cron too). To do manual execution through systemd:
```
systemd-run --on-calendar=2022-02-02T23:00 systemctl start cartography.service
```
or manually, exporting first variables from /etc/default/cartography (if you call file directly, cartography won't read variable and will return empty value)
```
$ export VAR1= VAR2=
$ cartography $CARTOGRAPHY_ARGS
```

## License

BSD 2-clause
