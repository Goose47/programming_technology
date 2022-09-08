import requests
import json
import plotly.express as px
import random
import pandas
from collections import Counter

API_TOKEN = 'c7ad5202334a66'
API_ENDPOINT = 'https://ipinfo.io/batch?token=c7ad5202334a66'


def generate_file():
    with open('ips.txt', 'w') as file:
        for _ in range(80):
            ip_address = generate_ip_address() + '\n'
            file.write(ip_address)


def generate_ip_address():
    ip_address = ''

    for _ in range(4):
        ip_address += str(random.randint(0, 255))
        ip_address += '.'

    return ip_address[:-1]


def parse_file():
    with open('ips.txt', 'r') as file:
        contents = file.read()

    ip_addresses = contents.split('\n')
    ip_addresses.pop()  # remove the last '' element

    for id, _ in enumerate(ip_addresses):
        ip_addresses[id] += '/region'  # to access region property

    return ip_addresses


def make_request(ip_addresses):
    response = requests.request('POST', API_ENDPOINT, json=ip_addresses)

    response = json.loads(response.text)
    regions = []

    for item in response:
        if type(response[item]) is str:  # to discard responses for invalid ips
            regions.append(response[item])

    counted_regions = dict(Counter(regions))

    data = {
        'Regions': [],
        'Count': []
    }  # creating a dataset for DataFrame

    for region in counted_regions:
        data['Regions'].append(region)
        data['Count'].append(counted_regions[region])

    return data


def make_diagram(regions):
    df = pandas.DataFrame(regions)  # creating a dataframe for plotly

    fig = px.pie(df, values='Count', names='Regions', title='Ip addresses distribution among different regions')
    fig.show()


def main():
    generate_file()
    ip_addresses = parse_file()
    regions = make_request(ip_addresses)
    make_diagram(regions)


if __name__ == '__main__':
    main()
