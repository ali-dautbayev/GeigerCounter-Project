import pyfirmata2
import time
import csv


board = pyfirmata2.Arduino("COM5")  # selects usb port

it = pyfirmata2.util.Iterator(board) # to continuously read data
it.start()

analogPin = board.get_pin("a:4:i")  # input pin to detect voltage
signalPin = board.get_pin("d:9:p")  # PWM for piezo

THRESHOLD = 0.5 / 5       # analog trigger voltage (normalised to 0-1)
BEEP_DURATION = 0.01       # seconds
FREQUENCY = 4000        # Hz

last_trigger = False   # prevents repeated beeps

def beep(): # generates 'beep' for piezo buzzer
    half_period = 1 / (2 * FREQUENCY)
    end_time = time.time() + BEEP_DURATION
    while time.time() < end_time:
        signalPin.write(1)
        time.sleep(half_period)
        signalPin.write(0)
        time.sleep(half_period)


dt = 0.01

fieldnames = ['time','voltage']

with open('data.csv','w') as csv_file: # writes to csv
    csv_writer =  csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()
  
times = 0
voltage = 0    

count_over_thresh = 0
interval_start_time = time.time()
interval_number = 1

try:
    while True:
        with open('data.csv', 'a') as csv_file:                
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            
            info = {
                "time": times,
                "voltage": voltage
            }
        
            csv_writer.writerow(info)
        
            times += dt
            val = analogPin.value
            
            if val is not None:
                if val > THRESHOLD and not last_trigger:
                    beep()
                    last_trigger = True
                    count_over_thresh += 1
                elif val <= THRESHOLD:
                    last_trigger = False
            
            if val != None:
                voltage = val * 5
            else:
                voltage = 0
            
            print(voltage, times)
                
            if time.time() - interval_start_time >= 60:
            # write count to a text file
                with open("counts.txt", "a") as txt_file:
                    txt_file.write(f"Interval {interval_number}: {count_over_thresh}\n")
                
                # reset counter and timer for next interval
                count_over_thresh = 0
                interval_start_time = time.time()
                interval_number += 1
            
        time.sleep(dt) # slight delay after detecting
        
except KeyboardInterrupt:
    print("Exiting...")
finally:
    board.exit()    
        

