import RPi.GPIO as GPIO
import time
import sqlite3


# Define GPIO pin number.
GPIO0_PIN = 11
GPIO1_PIN = 12
GPIO2_PIN = 13
GPIO3_PIN = 15
GPIO4_PIN = 16
GPIO5_PIN = 18
GPIO6_PIN = 22
GPIO7_PIN = 7


def setup_gpio():
    GPIO.setmode(GPIO.BOARD)
    # Set GPIO as input.
    GPIO.setup(GPIO0_PIN, GPIO.IN)
    GPIO.setup(GPIO1_PIN, GPIO.IN)
    GPIO.setup(GPIO2_PIN, GPIO.IN)
    GPIO.setup(GPIO3_PIN, GPIO.IN)
    GPIO.setup(GPIO4_PIN, GPIO.IN)
    GPIO.setup(GPIO5_PIN, GPIO.IN)
    GPIO.setup(GPIO6_PIN, GPIO.IN)
    GPIO.setup(GPIO7_PIN, GPIO.IN)

def get_temp():
    d0 = GPIO.input(GPIO0_PIN)
    d1 = GPIO.input(GPIO1_PIN)
    d2 = GPIO.input(GPIO2_PIN)
    d3 = GPIO.input(GPIO3_PIN)
    d4 = GPIO.input(GPIO4_PIN)
    d5 = GPIO.input(GPIO5_PIN)
    d6 = GPIO.input(GPIO6_PIN)
    d7 = GPIO.input(GPIO7_PIN)
    value = (d7 << 7) + (d6 << 6) + (d5 << 5) + (d4 << 4) + (d3 << 3) + (d2 << 2) + (d1 << 1) + d0
    voltage = (value * 2.5 * 2) / 256
    temp = voltage * 1000 / 10
    print "0b%d%d%d%d%d%d%d%d, %d, %f, %f" % \
        (d7, d6, d5, d4, d3, d2, d1, d0, value, voltage, temp)
    return temp

def insert_to_db(temp):
    # Connect to db.
    conn = sqlite3.connect('./db/test.db')
    c = conn.cursor()

    # Create table if not exist.
    c.execute('''CREATE TABLE IF NOT EXISTS `stats`(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            temperature REAL
        )''')

    # Insert the temp to db.
    c.execute('INSERT INTO `stats`(`temperature`) VALUES(?)', (temp,))
    # Save.
    conn.commit()
    # Disconnect with db.
    conn.close()

#
# Program entry point.
#
if __name__ == "__main__":
    setup_gpio()
    while True:
        temp = get_temp()
        insert_to_db(temp)
        time.sleep(5)
