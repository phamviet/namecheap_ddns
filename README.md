### Cli Usage
    namecheap_ddns.py --domain=domain_name --password=domain_password --host=host_name --debug=1

### Application Usage
    from namecheap_ddns import NamecheapDDNS
    n = NamecheapDDNS(domain, password)
    n.update(host, ip)
    
### Raspberry auto update scripts
    curl -o /home/pi/autoupdate_example.sh https://raw.githubusercontent.com/phamviet/namecheap_ddns/master/namecheap_ddns.py
    chmod +x /home/pi/autoupdate_example.sh
    
Create a dhcp client hook script at /etc/dhcp/dhclient-exit-hooks.d/namecheap_ddns
 
    #! /bin/sh
    /home/pi/namecheap_ddns_updater.sh >/dev/null 2>&1 || true

Make it executable

    chmod +x /etc/dhcp/dhclient-exit-hooks.d/namecheap_ddns