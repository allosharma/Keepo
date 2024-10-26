import re

def extract_video_id(url):

  # Check for "youtu.be" in the URL
  match_be = re.search(r"https://youtu\.be/([^/?]+)", url)

  # Check for "youtube.com/watch" in the URL
  match_watch = re.search(r"https://www\.youtube\.com/watch\?v=([^&]+)", url)

  # Extract the video ID based on the matched pattern
  if match_be:
    return match_be.group(1)
  elif match_watch:
    return match_watch.group(1)
  else:
    return None  # No match found