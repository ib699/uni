import requests

try:
    print("Hello, World!")
    pic_url = "https://example.com/pic.jpg"
    response = requests.get(pic_url)
    if response.status_code == 200:
        with open("pic.jpg", "wb") as f:
            f.write(response.content)
        print("Picture downloaded successfully.")
    else:
        print("Failed to download the picture.")
except Exception as e:
    print(f"An error occurred: {e}")


