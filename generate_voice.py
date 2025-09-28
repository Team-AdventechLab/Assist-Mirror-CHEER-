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
    "おはよう！今日も笑顔が素敵だね！",
    "やったね！とてもいい笑顔だよ！",
    "その調子！とっても楽しそう！",
    "ナイススマイル！最高だよ！",
    "今日の笑顔もめっちゃかわいい！",
    "その笑顔イケメンすぎる！まぶしーー！",
    "起きろ！起きろ！起きろーー！！！",
    "起きてチョーだい",
    "もう寝たんですか？まだ勉強初めたばかりですよ",
    "疲れてるのかな？でも頑張って！",
]

# 使用するキャラクターID
speaker_id = 3  # ずんだもん・なみだめ

for i, text in enumerate(texts, start=1):
    # Step1: 音声合成用のクエリ作成
    query = requests.post(
        f"{VOICEVOX_URL}/audio_query",
        params={"text": text, "speaker": speaker_id}
    )
    query_json = query.json()

    # --- 🎛 パラメータ調整 ---
    query_json["speedScale"] = 1.5       # 話速（1.0 が標準、2.0で2倍速）
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
    file_path = os.path.join(OUTPUT_DIR, f"voice_{i}.wav")
    with open(file_path, "wb") as f:
        f.write(synthesis.content)

    print(f"保存完了: {file_path}")
