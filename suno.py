import time
import requests

# replace with your suno-api URL
base_url = 'http://localhost:3000'


def custom_generate_audio(payload):
    url = f"{base_url}/api/custom_generate"
    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    return response.json()


def extend_audio(payload):
    url = f"{base_url}/api/extend_audio"
    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    return response.json()

def generate_audio_by_prompt(payload):
    url = f"{base_url}/api/generate"
    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    return response.json()


def get_audio_information(audio_ids):
    url = f"{base_url}/api/get?ids={audio_ids}"
    response = requests.get(url)
    return response.json()


def get_quota_information():
    url = f"{base_url}/api/get_limit"
    response = requests.get(url)
    return response.json()

def get_clip(clip_id):
    url = f"{base_url}/api/clip?id={clip_id}"
    response = requests.get(url)
    return response.json()

def generate_whole_song(clip_id):
    payload = {"clip_id": clip_id}
    url = f"{base_url}/api/concat"
    response = requests.post(url, json=payload)
    return response.json()


if __name__ == '__main__':
    data = generate_audio_by_prompt({
        "prompt": "A popular heavy metal song about war, sung by a deep-voiced male singer, slowly and melodiously. The lyrics depict the sorrow of people after the war.",
        "make_instrumental": False,
        "model": "chirp-v4",
        "wait_audio": False
    })

    ids = f"{data[0]['id']},{data[1]['id']}"
    print(f"Generated IDs: {ids}")
    print("\nPolling for results...")

    for i in range(60):
        data = get_audio_information(ids)
        print(f"\nCheck {i+1}/60:")
        for idx, item in enumerate(data):
            print(f"Track {idx+1}:")
            print(f"  Status: {item['status']}")
            print(f"  ID: {item['id']}")
            if item['audio_url']:
                print(f"  Audio URL: {item['audio_url']}")
            else:
                print("  Audio URL: Not yet available")
        
        if all(item['status'] == 'streaming' for item in data):
            print("\nAll tracks are ready!")
            break
        
        print("\nWaiting 5 seconds...")
        time.sleep(5)
