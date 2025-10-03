import pigpio
import time

PIN = 18  # PWM可能なGPIOピンを選択

pi = pigpio.pi()
if not pi.connected:
    raise SystemExit("pigpioデーモンに接続できません")

# パラメータ
pulse_high = 200      # パルス幅 [µs] = 0.2ms
period = 30000        # 周期 [µs] = 30ms
count = int(5 / (period / 1_000_000))  # 5秒分の繰り返し回数

# 波形を定義
wave = []
wave.append(pigpio.pulse(1<<PIN, 0, pulse_high))          # GPIOをHighに200µs
wave.append(pigpio.pulse(0, 1<<PIN, period - pulse_high)) # 残りをLow

pi.set_mode(PIN, pigpio.OUTPUT)
pi.wave_clear()
pi.wave_add_generic(wave)
wid = pi.wave_create()

# 5秒間繰り返し送信
if wid >= 0:
    pi.wave_send_repeat(wid)
    time.sleep(5)  # 5秒待つ
    pi.wave_tx_stop()
    pi.wave_clear()

pi.stop()
