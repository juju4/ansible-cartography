# Security - cartography

## Architecture

* Base setup is single-tier, single host via public Internet
```
┌───────────────┐
│ User          │
└──────┬────────┘
       │
┌──────▼────────┐
│     VM        │
└───────────────┘
```

* Setup on Azure via Express Route
```
┌───────────────┐
│ User          │
└──────┬────────┘
       │
┌──────▼────────┐
│ Express Route │
└──────┬────────┘
       │
┌──────▼────────┐
│     VM        │
└───────────────┘
```
(https://asciiflow.com/#/)

## Infrastructure setup

* Fully automated with ansible
* Upstream ansible role with continuous integration and weekly test.

## Data

* Purpose: Ensure Security of environment with coverage assessment, ensure no gaps and easier state audit.

* Data is collected from configured sources downstream. Downstream data is normally collected as part of IT and Security processing, usually falling under company job contract, acceptable use policy and right to monitor.

* It should mostly be technical infrastructure data but some fields may contain PII like emails, for example as contacts. It should normally contain no Sensitive Personal Information, Financial or Health related.

* Retention is up to 7 days as per cleanup jobs configuration.
  * Multi-instances collections require retention of at least one day, else latest run removes data from other instances.
  * Cleanup is executed after each collection. If collection is stopped, no cleanup is performed.

## Risks

* Confidentiality
Uploaded data contain sensitive data as cartography of an infrastructure and its tool coverage and gaps.
Proper access control and regular remediation of gaps should limit impact.

* Integrity
Limited risk of tampering as data is updated regularly from tools source with read-only credentials normally.
A threat actor compromising system could add or remove asset(s) or modify data that could influence user to think that a system is in a state not reflecting reality and taking wrong decisions based on it. If change done only at cartography server level and not upstream source, it will normally be limited to the timeperiod between data refresh.

* Availability
Limited risk as will only impede the service itself with no dependency.
Service can also be rebuilt in less than few hours as fully automated with either a database restore, either a new data synchronisation.
SLA at 90% should usually be enough (https://sre.google/sre-book/availability-table/)

* Attack on underlying infrastructure (Azure or else)

## Mitigating factors

### Identity

* Tool should only used read-only accesses to fetch upstream data.

* Neo4j backend access
  * If opensource free version, simple model and only users management without roles - https://neo4j.com/docs/cypher-manual/current/access-control/manage-users/
    `CREATE USER jake IF NOT EXISTS SET PLAINTEXT PASSWORD 'xyz'`
  * If Enterprise version, full RBAC available - https://neo4j.com/docs/operations-manual/current/authentication-authorization/

Possible option to use with a reverse proxy for web access

Backend identity limitations can be reduced through network segmentation and if only identified automation is used to access.
In this case, the identity management is handled downstream.

### System

* Systemd hardening with seccomp, capabilities.
* Split services under multiple systemd units and timers - [The systemd house of horror](https://jdebp.uk/FGA/systemd-house-of-horror/)
  * different level of privilege, system hardening
  * eventually separating between different hosts or containers aka multi-tiers architecture
* hardening roles: juju4.harden, juju4.osquery, juju4.falco
* Azure
  * Microsoft.GuestConfiguration VM extension
  * Azure Backup policy set daily
  * Optional Azure Bastion
  * Optional use of existing virtual network/subnet with private IP mapped on an Express Route to avoid having public IP
  * Issue: LinuxDiagnostic v3 does not support Ubuntu 22.04 at August 2022

### Network

|From|To|protocol/port|
|----|--|-------------|
|Authorized EndUser/Jumphost|Website|tcp/443|
|Cartography|Ingestion Source|tcp/443, other ports as required|
|System|DNS server|tcp+udp/53|
|System|SMTP server|tcp/587|

* Firewall at host level and nsg for azure for both incoming and outgoing traffic
  For azure playbook:
  * DNS hosts restricted to Azure as default
  * SMTP hosts restricted to O365 as default

* Neo4j web access can be over public Internet which should be avoided. If using Azure Express Route, this is limited to internal network.
* Optional reverse proxy

* Web proxy for outgoing traffic (local). If larger environment, use separate host.
A allow-only web proxy is setup with less than 40 domains approved, related to system and pandora operations
```
# test
ifconfig.me
# install
github.com
objects.githubusercontent.com
pypi.org
files.pythonhosted.org
debian.neo4j.org
debian.neo4j.com
# system - tinyproxy takes a single filters file
archive.ubuntu.com
ca.archive.ubuntu.com
security.ubuntu.com
azure.archive.ubuntu.com
ddebs.ubuntu.com
archive.canonical.com
changelogs.ubuntu.com
nova.clouds.archive.ubuntu.com
keyserver.ubuntu.com
livepatch.canonical.com
ppa.launchpad.net
# optional tools
pkg.osquery.io
osquery-packages.s3.us-east-1.amazonaws.com
download.falco.org
packages.microsoft.com
# juju4.harden
raw.githubusercontent.com
# crowdstrike
ts01-b.cloudsink.net
# Azure collection
login.microsoftonline.com
management.azure.com
graph.windows.net
api.securitycenter.microsoft.com
169.254.169.254
nvd.nist.gov
api.crowdstrike.com
# www.googleapis.com
# api.pagerduty.com
# subdomain.pagerduty.com
# github.com
# api.github.com
```

### Encryption

* Neo4j: requires certificate configuration, applicable to access with https and bolt protocols.
* Backup: as per tool configuration
  * [Azure Backup](Encryption in Azure Backup): "By default, all your data is encrypted using platform-managed keys.", option for customer-managed keys.

### Logging

* System level

* Cloud level
Use of Azure Diagnostics.

* Neo4j if Enterprise version

* Downstream frontends if applicable (web reverse proxy, automation bot...)

### Security monitoring

* Neo4j access if Enterprise version

* Network access at cloud level, system level (osquery, falco...)

* Frontends (automation, web...)

### Application Code scanning - TBD

Upstream project workflows include:
* test_suite via pre-commit: flake8, autopep8, pyupgrade, mypy
https://github.com/lyft/cartography/tree/master/.github/workflows


## Improvements - TBD

* Setup: use web proxy with TLS inspection if web mode.

* [Add more controls in pre-commit, partly security #1036](https://github.com/lyft/cartography/pull/1036) including detect-secrets, semgrep, bandit.
* [Add ossf scorecard #1037](https://github.com/lyft/cartography/pull/1037)
* codeql analysis = no
