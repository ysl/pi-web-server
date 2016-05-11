import RPi.GPIO as GPIO
import time
import sqlite3


# GPIO_xx mapping to pin number.
PIN7 = 7
PIN11 = 11
PIN12 = 12
PIN13 = 13
PIN15 = 15
PIN16 = 16
PIN18 = 18
PIN22 = 22


def setup_gpio():
    GPIO.setmode(GPIO.BOARD)
    # Set GPIO as input.
    GPIO.setup(PIN7, GPIO.IN)
    GPIO.setup(PIN11, GPIO.IN)
    GPIO.setup(PIN12, GPIO.IN)
    GPIO.setup(PIN13, GPIO.IN)
    GPIO.setup(PIN15, GPIO.IN)
    GPIO.setup(PIN16, GPIO.IN)
    GPIO.setup(PIN18, GPIO.IN)
    GPIO.setup(PIN22, GPIO.IN)

def get_temp():
    d0 = GPIO.input(PIN7)
    d1 = GPIO.input(PIN11)
    d2 = GPIO.input(PIN12)
    d3 = GPIO.input(PIN13)
    d4 = GPIO.input(PIN15)
    d5 = GPIO.input(PIN16)
    d6 = GPIO.input(PIN18)
    d7 = GPIO.input(PIN22)
    value = (d7 << 7) + (d6 << 6) + (d5 << 5) + (d4 << 4) + (d3 << 3) + (d2 << 2) + (d1 << 1) + d0
    voltage = (value * 2.5 * 2) / 256
    temp = voltage * 1000 / 10
    print "0b%d%d%d%d%d%d%d%d, value=%d, voltage=%f, temp=%f" % \
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
