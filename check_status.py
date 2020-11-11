import sys
from google.api_core import operation as operation_core
from google.cloud import speech_v1p1beta1 as speech


def check_transcription_status(operation_name: str):
    speech_client = speech.SpeechClient()
    operation_instance = speech_client._transport.operations_client.get_operation(
        operation_name
    )
    operation_response = operation_core.from_gapic(
        operation_instance,
        speech_client._transport.operations_client,
        speech.LongRunningRecognizeResponse,
        metadata_type=speech.LongRunningRecognizeMetadata,
    )
    if operation_response.done():
        operation = operation_response.operation
        if operation.HasField("error"):
            raise RuntimeError(
                f"Transcription error: {operation.error.code} {operation.error.message} {operation.error.details}"
            )
        # operation.response.value contains the protobuff with the transcription result
        # The question is how to decode it. 
        print(operation.response.value)
        # decoded_response = decode_response(operation.response.value)
        # results = decoded_response.results
        # print(results)
    else:
        print("Transcription still in progress...")

if __name__ == '__main__':
    operation_name = sys.argv[1]
    check_transcription_status(operation_name)
