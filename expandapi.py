import requests

def check_authenticated_url(url, api_key):
    headers = {
        'x-api-key': api_key
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json()
    except requests.RequestException:
        return False, {'message': 'Error reaching the URL'}

# Example usage
url = "https://api.expand.network/chain/getbalance/?address=0x731FDBd6871aD5cD905eE560A84615229eD8197a"
api_key = "4TxuJj4YvI3D3lIoTpWCF152D1r61IG78TLVPNB0"
is_successful, response_data = check_authenticated_url(url, api_key)

if is_successful:
    print("Request successful:")
    print(response_data)
else:
    print("Request failed:")
    print(response_data)
