from youtube_transcript_api import YouTubeTranscriptApi

def get_transcription(id):
  cc = YouTubeTranscriptApi.get_transcript(id)
  subtitle = ' '.join([i['text'] for i in cc])
  return subtitle