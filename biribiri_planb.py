import RPi.GPIO as GPIO
import time

# ==========================
# リレー接続GPIO設定
# ==========================
RELAY_UP = 17     # リレー1（電源ON／レベルUP用）
RELAY_DOWN = 27   # リレー2（レベルDOWN／電源OFF用）

# ==========================
# パラメータ設定
# ==========================
PRESS_TIME = 1.0  # 押下時間（秒）
WAIT_BETWEEN = 1  # 押下間の待機（秒）

# ==========================
# GPIO初期化（Active High対応）
# ==========================
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Active Highリレーなので、起動時はLOWでOFF
GPIO.setup(RELAY_UP, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(RELAY_DOWN, GPIO.OUT, initial=GPIO.LOW)

print("🔧 GPIO初期化完了（Active Highリレー：初期LOW＝OFF）")

# ==========================
# リレー制御関数
# ==========================
def press_relay(pin, name):
    """リレーを短時間ONしてスイッチ押下を模倣"""
    print(f"➡ {name}：リレーON（スイッチ押下）")
    GPIO.output(pin, GPIO.HIGH)   # リレーON（Active High）
    time.sleep(PRESS_TIME)        # 押下時間
    GPIO.output(pin, GPIO.LOW)    # リレーOFF
    time.sleep(WAIT_BETWEEN)      # 押下間インターバル


# ==========================
# メイン処理
# ==========================
try:
    print("\n============================")
    print("💡 EMSコントローラ動作テスト開始")
    print("============================\n")

    # ① 電源ON（スイッチ1押下）
    press_relay(RELAY_UP, "スイッチ1（電源ON）")
    print("🟢 電源ON 完了\n")

    # ② レベル1（スイッチ1もう一度押す）
    press_relay(RELAY_UP, "スイッチ1（レベル1）")
    print("⚙️ レベル1 駆動開始\n")

    # ③ レベル2（スイッチ2押下）
    press_relay(RELAY_UP, "スイッチ2（レベル2）")
    print("⚙️ レベル2 駆動中...\n")
    time.sleep(5)  # ④ 10秒間駆動

    # ⑤ レベルDOWN → 1
    press_relay(RELAY_DOWN, "スイッチ2（レベルDOWN → 1）")
    print("🔽 レベル1 に戻しました\n")

    # ⑥ レベルDOWN → 0
    press_relay(RELAY_DOWN, "スイッチ2（レベルDOWN → 0）")
    print("🕓 レベル0（待機）\n")

    # ⑦ レベルDOWN → 電源OFF
    press_relay(RELAY_DOWN, "スイッチ2（電源OFF）")
    print("🔴 電源OFF 完了\n")

    print("============================")
    print("✅ テスト完了（GPIO解放します）")
    print("============================")

# ==========================
# 終了処理
# ==========================
finally:
    GPIO.output(RELAY_UP, GPIO.LOW)
    GPIO.output(RELAY_DOWN, GPIO.LOW)
    GPIO.cleanup()
    print("GPIOピンを安全に解放しました。")