import os
import json
import ipaddress
import argparse
import sys
# import requests
# from bs4 import BeautifulSoup


class NameClass:
    def __init__(self, name):
        self.name = name

# Read IP addresses from a file
def read_ip_addresses_from_file(file_path):
    ip_addresses = []
    with open(file_path, 'r') as file:
        for line in file:
            ip_addresses.append(line.strip())
    return ip_addresses

# Read the JSON file
def open_json():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "ServiceTags_Public.json")
    with open(file_path, "r") as file:
        data = json.load(file)
    return data

def read_ip_addresses_from_stdin():
    ip_addresses = []
    for line in sys.stdin:
        ip_addresses.append(line.strip())
    return ip_addresses

def update_json():
    url = "https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519"
    print("Visit the following URL to download the JSON file: " + url)
    print("After downloading the file, rename it to ServiceTags_Public.json and place it in the same directory as this script.")


    # Not functioning yet due to BeautifulSoup not being able to parse the page

    # response = requests.get(url)
    # if response.status_code == 200:
    #     soup = BeautifulSoup(response.content, 'html.parser')
    #     download_link = soup.find('span', class_='file-link-view1').find('a')['href']
    #     print(download_link)
    #     response = requests.get(download_link)
    #     if response.status_code == 200:
    #         with open("ServiceTags_Public.json", "wb") as file:
    #             file.write(response.content)
    #     else:
    #         print("Failed to download the file")
            
    #         exit(1)
    # else:
    #     print("Failed to download the file")
    #     exit(1)
    # with open("ServiceTags_Public_20240506.json", "wb") as file:
    #     file.write(response.content)
    # print("Successfully updated the JSON file")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process IP addresses from a file.')
    parser.add_argument('--update-json', action='store_true', help='Update the JSON file with the latest version from Microsoft.')
    parser.add_argument('--file', type=str, help='Path to the file containing IP addresses.  - for stdin.', required='--update-json' not in sys.argv)
    args = parser.parse_args()
    
    if args.update_json:
        update_json()
        exit(0)

    # Read IP addresses from standard input or file
    if args.file == '-':
        ips_in = read_ip_addresses_from_stdin()
    elif args.file:
        if not os.path.exists(args.file):
            print("File does not exist")
            exit(1)
        ips_in = read_ip_addresses_from_file(args.file)

    data = open_json()
    # Get the json name tag from data
    name_tags = [item['name'] for item in data['values']]

    name_instances = [NameClass(name) for name in name_tags]

    for i in name_instances:
        cidr_list = data['values'][name_tags.index(i.name)]['properties']['addressPrefixes']
        for cidr in cidr_list:
            for ip in ips_in:
                if ipaddress.ip_address(ip) in ipaddress.ip_network(cidr):
                    result = {
                        "ip": ip,
                        "addressPrefixes": cidr,
                        "platform": i.name,
                        "region": data['values'][name_tags.index(i.name)]['properties']['region'],
                        "networkFeatures": data['values'][name_tags.index(i.name)]['properties']['networkFeatures']

                    }
                    json_result = json.dumps(result)
                    print(json_result)