import requests

api_key = 'AIzaSyBGxY5ZI7yGMh0_vBNaeatSV19ZTJK59Sg'
# video_id = 'VIDEO_ID'
# Define your API key and video ID
def fetchYoutubeData(video_id, key=api_key):
    url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={key}'

    try:
        # Send the GET request with a timeout
        response = requests.get(url, timeout=5)
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            
            # Check if 'items' exists in the data and is not empty
            if 'items' in data and data['items']:
                print('data is present')
                return data
            else:
                print("No data found for this video ID.")
        else:
            print('Failed to fetch data:', response.status_code)
            
    except requests.ConnectionError:
        print("Connection error. Please check your network.")
    except requests.Timeout:
        print("The request timed out.")
    except Exception as e:
        print(f"An error occurred: {e}")
