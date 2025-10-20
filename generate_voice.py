import requests
import json
import os

# VoiceVoxのAPIサーバー
VOICEVOX_URL = "http://127.0.0.1:50021"

# 出力フォルダ
OUTPUT_DIR = "sounds"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 変換したい文章リスト
# テキストの内容は要相談。短めがいい？？
texts = [
    "今日の笑顔も素敵です",
    "とってもいい笑顔",
    "その調子！！",
    "ナイススマイル",
    "笑顔がまぶしいぞ～",
    "その笑顔最高です",
]

# 使用するキャラクターID
#speaker_id = 0  # 四国メタン　あまあま
#speaker_id = 2  # 四国メタン　のーまる
speaker_id = 3 #ずんだもん　のーまる
#speaker_id = 1 #ずんだもん　あまあま
#speaker_id = 76 #ずんだもん　なみだめ
#speaker_id = 42 #ちび式じい

for i, text in enumerate(texts, start=1):
    # Step1: 音声合成用のクエリ作成
    query = requests.post(
        f"{VOICEVOX_URL}/audio_query",
        params={"text": text, "speaker": speaker_id}
    )
    query_json = query.json()

    # --- 🎛 パラメータ調整 ---
    query_json["speedScale"] = 1.1       # 話速（1.0 が標準、2.0で2倍速）
    query_json["intonationScale"] = 1.3  # 抑揚（1.0 が標準、数値を上げると強調）
    query_json["pitchScale"] = 0.0       # 音高（±で上下、0.0 が標準）
    query_json["volumeScale"] = 1.0      # 音量（1.0 が標準）
    query_json["prePhonemeLength"] = 0.1 # 発話前の無音秒数
    query_json["postPhonemeLength"] = 0.1 # 発話後の無音秒数

    # Step2: 音声合成してwav生成
    synthesis = requests.post(
        f"{VOICEVOX_URL}/synthesis",
        headers={"Content-Type": "application/json"},
        params={"speaker": speaker_id},
        data=json.dumps(query_json)
    )

    # ファイル保存
    file_path = os.path.join(OUTPUT_DIR, f"voice_{i}四国めたん.wav")
    with open(file_path, "wb") as f:
        f.write(synthesis.content)

    print(f"保存完了: {file_path}")
