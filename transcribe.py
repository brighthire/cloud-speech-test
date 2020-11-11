import argparse
import io
from google.api_core import operation as operation_core
from google.cloud import speech_v1p1beta1 as speech


def start_transcription(audio_file, multichannel, speaker_count):
    client = speech.SpeechClient()

    #  Note that transcription is limited to 60 seconds audio.
    #  Use a GCS file for audio longer than 1 minute.
    with io.open(audio_file, "rb") as file:
        content = file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        language_code="en-US",
        use_enhanced=True,
        model="phone_call",
        enable_word_time_offsets=True,
        enable_automatic_punctuation=True,
    )

    if multichannel:
        config.audio_channel_count = speaker_count
        config.enable_separate_recognition_per_channel = True
    else:
        config.enable_speaker_diarization = True
        config.diarization_speaker_count = speaker_count

    operation = client.long_running_recognize(
        request={"config": config, "audio": audio}
    )
    return operation._operation.name

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--multichannel', type=bool, default=True)
    parser.add_argument('-s', '--speakers', type=int, default=2)
    parser.add_argument('file')
    args = parser.parse_args()
    op_name = start_transcription(args.file, args.multichannel, args.speakers)
    print(f"Transciption started. Operation name: {op_name}")
