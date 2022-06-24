from keylogger import KeyLogger
import os


class Test:
    def __init__(self, target_string, column_names, ofile, max_repetitions=100):
        self.keylogger = KeyLogger(max_repetitions, target_string)
        self.column_names = column_names
        self.ofile = ofile
        self.target_string = target_string
    
    def start_test(self):

        self.name = input('Please enter your name > ')
        print("[!] Hooking key events")
        print("[!] Press [esc] to exit and save at any time")
        print("[!] Press [space] to begin test")

        self.keylogger.start()
    
    def process_data(self):

        #TODO: Clean this section up

        down_times = self.keylogger.down_key_events
        up_times = self.keylogger.up_key_events

        data = list(zip(down_times, up_times))
        
        data = [list(zip(*tuple)) for tuple in data]

        
        good_results = list(filter(lambda x : (len(x) == len(self.target_string) + 1), data))

        test_hold_times = []
        test_down_down_times = []
        test_up_down_times = []

        for good_result in good_results:
            hold_times = []
            for result in good_result:
                down_time = result[0]
                up_time   = result[1]
                hold_times.append(round(up_time - down_time, 4))
            test_hold_times.append(hold_times)

        for good_result in good_results:
            dd_times = []
            for i in range(len(good_result)-1):
                first_down = good_result[i][0]
                second_down = good_result[i+1][0]
                dd_times.append(round(second_down - first_down, 4))
            test_down_down_times.append(dd_times)
        

        for good_result in good_results:
            ud_times = []
            for i in range(len(good_result)-1):
                first_up = good_result[i][1]
                second_down = good_result[i+1][0]
                ud_times.append(round(second_down - first_up, 4))
            test_up_down_times.append(ud_times)

        print(f'[!] Trying to write results to {os.getcwd()}/{self.ofile}')

        with open(self.ofile, 'w') as csv:
            csv.write(','.join(self.column_names) + '\n')
            for i in range(len(test_hold_times)):
                row = f'{self.name},0,{i+1}'
                for j in range(len(test_hold_times[0]) - 1):
                    #hold, down_down, up_down
                    row += f",{test_hold_times[i][j]}, \
                    {test_down_down_times[i][j]}, \
                    {test_up_down_times[i][j]}"
                row += f',{test_hold_times[i][len(test_hold_times[i])-1]}'
                csv.write(row + '\n')


