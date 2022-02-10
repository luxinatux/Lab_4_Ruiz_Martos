"""!
    @file           main.py
    @brief          Task implementation for step responses for two motors.
    @details        Implements co-task implementation using the cotask file.   
                    Produces and prints out step response results for both motors. 
                    Tasks are implemented as generators.
    @author         Dylan Ruiz
    @author         Lucas Martos-Repath
    @date           February 9, 2022
"""

import gc
import pyb
import time
import task_share
from micropython import const

## Safety Feature
import micropython
micropython.alloc_emergency_exception_buf(1000)


def isr_adc(bad):
    """!
    @brief    Task which initializes and updates encoder 1. 
    @details  Continuously writes the encoder position to the shared variable position1_share.
    """
    C0_queue.put(adc_obj.read(),in_ISR = True)
    T1_queue.put(time.ticks_diff(time.ticks_ms(),time_start))
    
  

    
if __name__ == "__main__":
    
    global time_start
    #prints the start flag used to notify when to start reading the data lines.
    print("111")
    C0_queue = task_share.Queue('H', 4000, thread_protect = False, overwrite = False,
                           name = "C0 Queue")
    T1_queue = task_share.Queue('H', 4000, thread_protect = False, overwrite = False,
                           name = "Time Queue")
    
    pinC1 = pyb.Pin(pyb.Pin.cpu.C1, pyb.Pin.OUT_PP)
    
    pinC0 = pyb.Pin(pyb.Pin.cpu.C0)
    
    pinC1.low()
    time.sleep_ms(2000)
    
    adc_obj = pyb.ADC(pinC0)
    
    state = 0

    time_now = 0
    
    timer1 = pyb.Timer(1, freq = 1000) # frequency
    #timer_ch1 = timer1.channel(1, pyb.Timer., pin= pinIN1)
    timer1.callback(isr_adc)
    
    #pinC1.high()
    time_start = time.ticks_ms()
    

    

    time_start = time.ticks_ms()
    pinC1.high()
    while(True):
        if state == 0:
            time_now = time.ticks_diff(time.ticks_ms(),time_start)
            ## current position from Encoder task
            try:
                print('{:},{:}'.format(T1_queue.get(), C0_queue.get()))
            except:
                print('done')
                break
            
            else:
                if time_now >= 1000:
                   timer1.callback(None)
                   pass
               
#             if time_now >= 4000:
#                 state = 1
            
        elif state == 1:
            print('done')
            state = 2
            pass
        elif state == 2:
            break
    
    
    pinC1.low()
    '''
    time.sleep_ms(100)
    pinC1.low()
    time.sleep_ms(1000)
    pinC1.high()
    time.sleep_ms(3000)
    #pinC1.low()
    time.sleep_ms(3000)
    #pinC1.high()
    time.sleep_ms(1000)
    pinC1.low()
    '''
    

    # Creates shares objects used to share the position between tasks.
    
    
    #position2_share = task_share.Share('i', thread_protect = False, name = "Position 2")
