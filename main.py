import base64
import os
import requests

engine_id = "stable-diffusion-v1-6"
api_host = os.getenv('API_HOST', 'https://api.stability.ai')
api_key = os.getenv("STABILITY_API_KEY")
api_key = "sk-hV2ZXdHgwyHa9zOkkBSrvpFiRttZMqGKOzBWFpGmnn456Rlr"
if api_key is None:
    raise Exception("Missing Stability API key.")

print("program running")
val = input("Enter the prompt")
response = requests.post(
    f"{api_host}/v1/generation/{engine_id}/text-to-image",
    headers={
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    },
    json={
        "text_prompts": [
            {
                "text": val
            }
        ],
        "cfg_scale": 7,
        "height": 1024,
        "width": 1024,
        "samples": 1,
        "steps": 30,
    },
)

if response.status_code != 200:
    raise Exception("Non-200 response: " + str(response.text))

data = response.json()

for i, image in enumerate(data["artifacts"]):
    with open(f"./v1_txt2img_{i}.jpg", "wb") as f:
        f.write(base64.b64decode(image["base64"]))
os.system("python index.py")
