import requests

class DictionaryAPI:
    def __init__(self, api_key):
        self.base_url = "https://google.serper.dev/search"
        self.api_key = api_key

    def get_word(self, word: str):
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "q": f"translate {word} to Uzbek"
        }

        try:
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            # natijadan tarjima olish (snippet ichidan)
            if "organic" in data and len(data["organic"]) > 0:
                return data["organic"][0]["snippet"]
            else:
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching word: {e}")
            return None
