from pydub import AudioSegment

'''
Max file size that the speech to text model can accept
'''
MAX_FILE_SIZE_MB = 25


'''
Converts a voice message file which is in OGG format to MP3 format

Parameters:
    - file_path: File path of the original voice message

Returns:
    - mp3_file_path: File path of the voice message in MP3 format
'''
def convert_from_ogg_to_mp3(file_path: str):
    try:
        audio = AudioSegment.from_ogg(file_path)
        mp3_path = file_path.replace('.ogg', '.mp3')
        audio.export(mp3_path, format='mp3')
        return mp3_path
    except Exception as e:
        print(f'Error converting audio: {e}')
        return None



'''
Converts a MP3 file to an OGG file

Parameters:
    - file_path: File path of the MP3 file

Returns:
    - ogg_file_path: File path of the OGG file
'''
def convert_from_mp3_to_ogg(file_path: str):
    try:
        audio = AudioSegment.from_mp3(file_path)
        ogg_path = file_path.replace('.mp3', '.ogg')
        audio.export(ogg_path, format='ogg')
        return ogg_path
    except Exception as e:
        print(f'Error converting audio: {e}')
        return None