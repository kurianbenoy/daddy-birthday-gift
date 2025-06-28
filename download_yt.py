import os
import logging
import shutil
from typing import Optional
from yt_dlp import YoutubeDL


def save_locally(save_dir: str, video_id: str, output_path: str) -> None:
    """Save downloaded files to the specified output path."""
    for file in os.listdir(os.path.join(save_dir, video_id)):
        local_file_path = os.path.join(save_dir, video_id, file)
        dest_path = os.path.join(output_path, video_id, file)

        # Create destination directory if it doesn't exist
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

        # Copy file to destination
        shutil.copy2(local_file_path, dest_path)


def is_video_downloaded(save_dir: str, video_id: str) -> bool:
    """Check if video files exist in the specified directory."""
    final_dir = os.path.join(save_dir, video_id)
    if not os.path.exists(final_dir):
        return False

    files = os.listdir(final_dir)
    video_extensions = (
        '.webm', '.mp3', '.m4a', '.flac', '.wav', '.mp4', '.mkv', '.avi'
    )

    return any(
        file.endswith(ext) for file in files for ext in video_extensions
    )


def get_media_file_name(save_dir: str, video_id: str) -> Optional[str]:
    """Get the name of the audio or video file if it exists."""
    final_dir = os.path.join(save_dir, video_id)
    if not os.path.exists(final_dir):
        return None

    for file in os.listdir(final_dir):
        if file.endswith((
            '.webm', '.mp3', '.m4a', '.flac', '.wav', '.mp4', '.mkv', '.avi'
        )):
            return file
    return None


def process_video(video_id: str, output_path: str) -> bool:
    """Process and download a YouTube video with subtitles."""
    try:
        video_url = f'https://youtu.be/{video_id}'
        save_dir = os.path.join(os.path.dirname(__file__), 'video_output')
        os.makedirs(save_dir, exist_ok=True)

        ydl_opts = {
            'format': '232+233/231+233/230+233/best',
            'continue_dl': True,
            'ignoreerrors': False,
            'concurrent_fragment_downloads': 20,
            'outtmpl': {
                'default': os.path.join(
                    save_dir,
                    '%(id)s',
                    '%(id)s.%(ext)s'
                ),
                'infojson': os.path.join(
                    save_dir,
                    '%(id)s',
                    'metadata.%(ext)s'
                ),
            },
            'restrictfilenames': True,
            'cachedir': '/tmp',
            'writesubtitles': True,
            'writeautomaticsub': True,
            'writeinfojson': True,
            'subtitlesformat': 'vtt',
            'noplaylist': True,
            'quiet': True,
            'socket_timeout': 60,
            'verbose': False,
            'force_ipv4': True,
            'fragment_retries': 100000000,
            'skip_unavailable_fragments': True,
            'no_part': True,
            'retries': 100000000
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(video_url, download=True)

            if is_video_downloaded(save_dir, video_id):
                logging.info(f'Successfully downloaded video {video_id}')
                media_file_name = get_media_file_name(save_dir, video_id)
                if media_file_name:
                    save_locally(save_dir, video_id, output_path)
                    return True
                else:
                    logging.error(f'No media file found for {video_id}')
                    return False
            else:
                logging.error(
                    f'Could not download the media file for {video_id}. '
                    'Maybe only metadata is present.'
                )
                return False

    except Exception as e:
        logging.error(
            f'Exception occurred while processing video {video_id}: {str(e)}'
        )
        return False


def process_audio(video_id: str, output_path: str) -> bool:
    try:
        video_url = f'https://youtu.be/{video_id}'
        save_dir = os.path.join(os.path.dirname(__file__), 'video_output')
        os.makedirs(save_dir, exist_ok=True)

        ydl_opts = {
            'format': '233/234/bestaudio/best',
            # 'postprocessor_args': {'ffmpeg': ['-ac', '1', '-ar', '16000']},
            # 'postprocessors': [
            #     {
            #         'key': 'FFmpegExtractAudio',
            #         'preferredcodec': 'mp3',
            #         'preferredquality': '0',
            #     }
            # ],
            'continue_dl': True,
            'ignoreerrors': False,
            'concurrent_fragment_downloads': 20,
            'outtmpl': {
                'default': os.path.join(
                    save_dir,
                    '%(id)s',
                    '%(id)s.%(ext)s'
                ),
                'infojson': os.path.join(
                    save_dir,
                    '%(id)s',
                    'metadata.%(ext)s'
                ),
            },
            'restrictfilenames': True,
            'cachedir': '/tmp',
            # 'writethumbnail': True,
            'writesubtitles': True,
            'writeautomaticsub': True,
            'writeinfojson': True,
            'subtitleslangs': [
                'en.*', 'hi-orig.*', 'bn-orig.*', 'gu-orig.*', 'kn-orig.*',
                'ml-orig.*', 'mr-orig.*', 'or-orig.*', 'ta-orig.*',
                'te-orig.*', 'pa.*'
            ],
            'subtitlesformat': 'vtt',
            'noplaylist': True,
            'quiet': True,
            'socket_timeout': 60,
            'verbose': False,
            'force_ipv4': True,
            'fragment_retries': 100000000,
            'skip_unavailable_fragments': True,
            'no_part': True,
            'retries': 100000000
            # 'download_archive': archive_file,
            # 'break_on_existing': True,
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(video_url, download=True)

            if is_video_downloaded(save_dir, video_id):
                logging.info(f'Successfully downloaded video {video_id}')
                media_file_name = get_media_file_name(save_dir, video_id)
                if media_file_name:
                    save_locally(save_dir, video_id, output_path)
                    return True
                else:
                    logging.error(f'No media file found for {video_id}')
                    return False
            else:
                logging.error(
                    f'Could not download the media file for {video_id}. '
                    'Maybe only metadata is present.'
                )
                return False

    except Exception as e:
        logging.error(
            f'Exception occurred while processing video {video_id}: {str(e)}'
        )
        return False


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    output_path = os.path.join(
        os.path.dirname(__file__),
        'audio_input'
    )
    process_audio("5TBgsf5chxQ", output_path)
    # https://www.youtube.com/watch?v=hY-sBLhEpbw
    # 9p75x0UZUCg
