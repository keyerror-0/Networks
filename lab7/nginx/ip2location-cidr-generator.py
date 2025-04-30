import csv
import ipaddress
import sys
from pathlib import Path

def main():
    csv_path = "/tmp/IP2LOCATION-LITE-DB1.CSV"
    output_path = "/etc/nginx/geoip/ru-cidr.txt"
    
    # Создаем директорию, если не существует
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    cidr_entries = []
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            
            for row in reader:
                try:
                    start = int(row[0].strip('"'))
                    end = int(row[1].strip('"'))
                    country = row[2].strip('"').upper()
                    
                    if country != 'RU':
                        continue
                        
                    start_ip = ipaddress.IPv4Address(start)
                    end_ip = ipaddress.IPv4Address(end)
                    
                    if start_ip > end_ip:
                        continue
                        
                    for network in ipaddress.summarize_address_range(start_ip, end_ip):
                            cidr_entries.append(f"{network} 1;")

                except Exception as e:
                    print(f"Error processing row: {e}", file=sys.stderr)
                    continue

        if not cidr_entries:
            raise ValueError("No valid RU CIDR blocks found!")

        if "37.195.0.0/16" not in cidr_entries:
            cidr_entries.append("37.195.0.0/16 1;")

        # Сохраняем результат с правильным форматом
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(cidr_entries))
            f.write("\ndefault 0;")

        print(f"Successfully generated {len(cidr_entries)} CIDR entries")

    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()