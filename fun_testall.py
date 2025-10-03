import RPi.GPIO as GPIO
import time

RELAY_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)

def press_switch(seconds=0.5):
    """スイッチを押す（秒数指定）"""
    GPIO.output(RELAY_PIN, GPIO.HIGH)
    time.sleep(seconds)
    GPIO.output(RELAY_PIN, GPIO.LOW)
    time.sleep(0.5)  # ボタン離し後の待ち時間

def stop_fan():
    """停止のための長押し"""
    press_switch(3)  # 3秒長押しで停止（必要に応じて調整）

def test_level(level):
    """指定レベルの風量を5秒間テストして停止"""
    print(f"\n=== レベル{level}テスト開始 ===")

    # 短押しをレベル回数だけ繰り返す
    for _ in range(level):
        press_switch(0.5)  # 短押し0.5秒

    print(f"→ レベル{level}送風中（5秒間観察）")
    time.sleep(5)

    stop_fan()
    print(f"=== レベル{level}テスト終了 ===\n")
    time.sleep(3)

def test_max():
    """MAX風量を5秒間テスト（長押し）"""
    print("\n=== MAX風量テスト開始 ===")
    press_switch(3)  # 長押しでMAX ON
    print("→ MAX風量送風中（5秒間観察）")
    time.sleep(5)
    # 手を離すと自動停止するので追加操作不要
    print("=== MAX風量テスト終了 ===\n")
    time.sleep(3)

def cleanup():
    GPIO.cleanup()

# ★テスト実行 テストするやつ以外はコメントアウトして！
if __name__ == "__main__":
    try:
        test_level(1)  # レベル1テスト
        #test_level(2)  # レベル2テスト
        #test_level(3)  # レベル3テスト
        #test_max()     # MAX風量テスト
    finally:
        cleanup()
