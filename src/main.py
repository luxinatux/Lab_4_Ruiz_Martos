"""!
    @file           main.py
    @brief          Task implementation for Interrupt Service Routine RC circuit step Response
    @details        Creates an Interrupt Service Routine to be run with a timer. The timer calls the
                    ISR every millisecond. Data is passed out of our ISR via queues to be printed in our
                    __main__ FSM. Our __main__ FSM allows us to turn the ISR off after 1500s to not overload the queue
                    as the ISR gets called much faster than the processor is able to print
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
    @brief    Creates the Interrupt Service Routine
    @details  When called, reads the ADC object (the pin set up to read ADC) and stores in a queue.
              Then computes the current time and stores that in a queue
    @param    bad Necessary input for ISR. not used in routine
    """
    C0_queue.put(adc_obj.read(),in_ISR = True)
    #T1_queue.put(time.ticks_diff(time.ticks_ms(),time_start))
    T1_queue.put(time.ticks_diff(time.ticks_ms(),time_start),in_ISR = True)
    
  

    
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
    print_count = 0
    while(True):
        if state == 0:
            time_now = time.ticks_diff(time.ticks_ms(),time_start)
            ## current position from Encoder task
            print_count += 1
            try:
                print('{:},{:}'.format(T1_queue.get(), C0_queue.get()))
                
            except:
                pass
            
            else:
                if print_count >= 1500:
                   timer1.callback(None)
                   state = 1
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
