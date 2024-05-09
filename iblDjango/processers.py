from typing import Optional

import requests

BASE_API_URL = "http://localhost:7860/api/v1/process"
FLOW_ID = "a1a3968a-7a6e-42f7-85df-a5f1e05fbda9"
# You can tweak the flow by adding a tweaks dictionary
# e.g {"OpenAI-XXXXX": {"model_name": "gpt-4"}}
TWEAKS = {}


def run_flow(inputs: dict,tweaks: Optional[dict] = None, apiKey: Optional[str] = None) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param apiKey:
    :param inputs: The message to send to the flow
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/{FLOW_ID}"

    payload = {"inputs": inputs}
    headers = {}

    if tweaks:
        payload["tweaks"] = tweaks
    if apiKey:
        api_url += f"?x-api-key={apiKey}"

    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()
