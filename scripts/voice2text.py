#!/usr/bin/env python3
"""语音转文字 - 使用 faster-whisper 本地模型"""
import sys
from faster_whisper import WhisperModel

def transcribe(audio_path, model_size="base"):
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, info = model.transcribe(audio_path, beam_size=5)
    text = "".join(seg.text for seg in segments).strip()
    print(f"[{info.language}] {text}")
    return text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: voice2text.py <audio_file> [model_size]")
        sys.exit(1)
    model = sys.argv[2] if len(sys.argv) > 2 else "base"
    transcribe(sys.argv[1], model)
