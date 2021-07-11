#!/usr/bin/env python3

import re
import sys
import ipaddress
import json
from collections import Counter

"""Define subnets to check if distinct IP address is belonged to."""
bucket = ["108.162.0.0/16", "212.129.32.223/32", "173.245.56.0/23"]
source_ip_count = []
source_ip_list = []
bucket_network_list = []

def process_log(log_file):
    """Take source nginx log file and process to output distinct IP addresses.

    :param log_file:
    :return: distinct IP addresses
    """
    for line in log_file:
        ip_pattern = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
        if ip_pattern is not None:
            source_ip_count.append(ip_pattern.group())
            if ip_pattern.group() not in source_ip_list:
                source_ip_list.append(ip_pattern.group())
    
    return source_ip_list

def count_ip(source_ip_list):
    """Take distinct IP addresses and output IP lists that are in subnets.
    Use python ipaddress module to check if each IP is belonged to subnet in bucket
    :param source_ip_list:
    """
    for ip in source_ip_list:
        ip_address = ipaddress.ip_address(ip)
        for netowrk in bucket:
            if ip_address in ipaddress.ip_network(netowrk):
                bucket_network_list.append(netowrk)

def output_result():
    """Print result in a nice format
    Counter module to track of the number of times each IP are encountered
    Counter module to track of the number of times each unique IP is belonged to subnet in bucket 
    """
    for i, j in Counter(source_ip_count).items():
        print(f'Address {i} was encountered {j} time(s)')
    for i,j in Counter(bucket_network_list).items():
        print(f'The bucket {i} contains {j} addresses')
    
    return bucket_network_list

def print_result():
    """Output result to html file for web server to display
    Construct output to JSON format
    """
    result = open("web/index.html", "w")
    public_result = {"buckets": [], "address": []}
    for i, j in Counter(source_ip_count).items():
        public_result["address"].append({i: j})
    for i, j in Counter(bucket_network_list).items():
        public_result["buckets"].append({i: j})
    json.dump(public_result, result, indent = 4)
    result.close()

if __name__ == '__main__': 
    
    try:
        # open and load source log file
        log_file = open('logs/nginx.log', 'r')
        process_log(log_file)
        count_ip(source_ip_list)
        output_result()
        print_result()
    except Exception as e:
        print(f'Error opening file:', str(e))
        sys.exit(1)
