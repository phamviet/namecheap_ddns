### Cli Usage
    namecheap_ddns.py --domain=domain_name --password=domain_password --host=host_name

### Application Usage
    import namecheap_ddns
    n = NamecheapDDNS(domain, password)
    n.update(host, ip)
    