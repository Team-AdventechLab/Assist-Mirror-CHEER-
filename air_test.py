import RPi.GPIO as GPIO
import time

RELAY_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)

def press_switch(seconds=5):
    GPIO.output(RELAY_PIN, GPIO.HIGH)
    print(f"送風機ON ({seconds}秒間)")
    time.sleep(seconds)
    GPIO.output(RELAY_PIN, GPIO.LOW)
    print("送風機OFF")

def cleanup():
    GPIO.cleanup()

# ★単体テスト用 テスト後以下削除
if __name__ == "__main__":
    try:
        press_switch(5)  # 5秒だけ送風してみる
    finally:
        cleanup()
