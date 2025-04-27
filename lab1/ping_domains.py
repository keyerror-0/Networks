import csv
from pythonping import ping

def ping_domains(hosts):
    with open('ping_stats.csv', 'w', newline = '') as csvfile:
        fieldnames = ['domain_name', 'packets_sent', 'packets_returned', 'packets_lost', 'rtt min/avg/max']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for host in hosts:
            response = ping(host)
            writer.writerow({'domain_name': host, 'packets_sent': response.stats_packets_sent, 'packets_returned': response.stats_packets_returned, 
                            'packets_lost': response.stats_packets_lost, 'rtt min/avg/max': f"{response.rtt_min_ms}/{response.rtt_avg_ms}/{response.rtt_max_ms}"})


hosts = ['google.com', 'vk.com', 'playvalorant.com', 'www.gismeteo.ru', 'culture.ru', 'gdz.ru', 'animego.org', 'ria.ru', 'youtube.com', 'gmail.com']
ping_domains(hosts=hosts)