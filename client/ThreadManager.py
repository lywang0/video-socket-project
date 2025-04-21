import threading
from Decoder.DecodePlayer import decode_and_play


def start_decoding_thread(bin_path, video_id, segment_id):
    thread = threading.Thread(target=decode_and_play, args=(bin_path, video_id, segment_id))
    thread.start()
    print("[INFO] Starting decoding thread...")
