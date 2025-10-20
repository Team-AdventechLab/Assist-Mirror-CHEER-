import pigpio
import os
import time

PIN = 18  # PWM可能なGPIOピン

# ---------------- デーモン起動 ----------------
print("pigpiodを起動中...")
os.system("sudo systemctl start pigpiod")
time.sleep(1)  # 起動安定のため少し待機

pi = pigpio.pi()
if not pi.connected:
    raise SystemExit("pigpioデーモンに接続できません")

print("✅ pigpiod に接続成功")

# ---------------- 波形設定 ----------------
pulse_high = 200      # パルス幅 [µs]
period = 30000        # 周期 [µs]

wave = [
    pigpio.pulse(1 << PIN, 0, pulse_high),
    pigpio.pulse(0, 1 << PIN, period - pulse_high)
]

pi.set_mode(PIN, pigpio.OUTPUT)
pi.wave_clear()
pi.wave_add_generic(wave)
wid = pi.wave_create()

# ---------------- 波形送信 ----------------
if wid >= 0:
    pi.wave_send_repeat(wid)
    print("✅ 波形送信開始 (Ctrl+Cで停止)")
    try:
        while True:
            busy = pi.wave_tx_busy()
            print(f"送信中: {busy}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 停止します")

# ---------------- 終了処理 ----------------
pi.wave_tx_stop()
time.sleep(0.05)
pi.wave_delete(wid)
pi.wave_clear()
pi.write(PIN, 0)
pi.set_mode(PIN, pigpio.INPUT)
pi.stop()

print("GPIO解放完了")

# ---------------- デーモン停止 ----------------
print("pigpiodを停止中...")
os.system("sudo systemctl stop pigpiod")
print("✅ デーモン停止完了")
