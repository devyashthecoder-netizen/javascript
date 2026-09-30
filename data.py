import requests
import re
import json
import csv

url = "https://www.youtube.com/results?search_query=?"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers, timeout=10)
response.raise_for_status()

text = response.text

match = re.search(r'var ytInitialData = ({.*?});', text)

if not match:
    print("ytInitialData not found")
    exit()

data = json.loads(match.group(1))


def find_objects(obj, key):
    found = []

    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == key:
                found.append(v)

            found.extend(find_objects(v, key))

    elif isinstance(obj, list):
        for item in obj:
            found.extend(find_objects(item, key))

    return found


videos = find_objects(data, "videoRenderer")

print("Videos found:", len(videos))

with open("youtube_data.csv", "w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)

    writer.writerow([
        "Title",
        "Video ID",
        "URL"
    ])

    for video in videos:

        video_id = video.get("videoId")

        title_runs = video.get("title", {}).get("runs", [])

        title = "".join(
            run.get("text", "")
            for run in title_runs
        )

        video_url = f"https://www.youtube.com/watch?v={video_id}"

        writer.writerow([
            title,
            video_id,
            video_url
        ])

        print(title)

print("\nData saved to youtube_data.csv")