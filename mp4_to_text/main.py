from yt_dlp import YoutubeDL
import whisper

video_url = "https://www.youtube.com/watch?v=o8TssbmY-GM"  # 例: "https://www.youtube.com/watch?v=VIDEO_ID"

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'audio.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '192',
    }],
}

try:
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    print("音声のダウンロードが完了しました。")
except Exception as e:
    print(f"音声のダウンロード中にエラーが発生しました: {e}")




# whisper
model = whisper.load_model('small')  # 'tiny', 'base', 'small', 'medium', 'large'
result = model.transcribe('audio.wav')
transcript = result['text']
with open('transcript.txt', 'w', encoding='utf-8') as f:
    f.write(transcript)
print("transcript.txt is generated.")

# タイムスタンプのフォーマット関数
def format_timestamp(seconds_float):
    hours = int(seconds_float // 3600)
    minutes = int((seconds_float % 3600) // 60)
    seconds = int(seconds_float % 60)
    milliseconds = int(round((seconds_float - int(seconds_float)) * 1000))
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

# 字幕ファイルの作成
segments = result['segments']

with open('subtitles.srt', 'w', encoding='utf-8') as f:
    for i, segment in enumerate(segments):
        start_time = format_timestamp(segment['start'])
        end_time = format_timestamp(segment['end'])
        text = segment['text'].strip()
        f.write(f"{i + 1}\n")
        f.write(f"{start_time} --> {end_time}\n")
        f.write(f"{text}\n\n")

print("subtitles.srt is generated.")
