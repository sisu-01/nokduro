from pytube import YouTube
import yt_dlp

def normal():
  # 다운로드할 유튜브 URL
  url = "https://www.youtube.com/live/6lbtHKBK80M?si=8IAzD6HUviZR6zi6"

  # YouTube 객체 생성
  yt = YouTube(url)

  # 360p 해상도, 소리 없는 영상 필터링
  stream = yt.streams.filter(res="360p", file_extension="mp4", only_video=True).first()

  # 영상이 존재하는지 확인하고 다운로드
  if stream:
    stream.download(output_path="다운로드할 경로를 여기에 적으세요")
    print("다운로드 완료!")
  else:
    print("360p 해상도의 소리 없는 영상을 찾을 수 없습니다.")

def live():

  # 다운로드할 유튜브 라이브 URL
  url = "https://www.youtube.com/live/6lbtHKBK80M?si=8IAzD6HUviZR6zi6"

  # yt-dlp 옵션 설정
  ydl_opts = {
      'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',  # 360p 해상도
      'outtmpl': 'video/video.%(ext)s',                       # 저장 경로와 파일명
  }

  # 다운로드 실행
  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

  print("다운로드 완료!")

live()

"""
yt-dlp가 비디오와 오디오 스트림을 병합하려면 ffmpeg가 필요합니다. 이 오류는 ffmpeg가 시스템에 설치되지 않아서 발생하는 것입니다.

1. ffmpeg 설치
Windows: ffmpeg 공식 웹사이트에서 Windows용 ffmpeg를 다운로드한 후, 설치 경로를 환경 변수에 추가하세요.

다운로드 후 압축을 해제하고, bin 폴더 경로를 PATH 환경 변수에 추가합니다.
macOS: 터미널에서 다음 명령어로 설치할 수 있습니다.

bash
코드 복사
brew install ffmpeg
Linux: 패키지 관리자에서 설치할 수 있습니다. 예:

bash
코드 복사
sudo apt update
sudo apt install ffmpeg
"""