import requests

def get_distance(img1:str,img2:str):
    r = requests.post(
    "https://api.deepai.org/api/image-similarity",
    files={
        'image1': open(img1, 'rb'),
        'image2': open(img2, 'rb'),
    },
    headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
    )

    data = r.json()
    output = data['output']
    distance = output['distance']

    return int(distance)
