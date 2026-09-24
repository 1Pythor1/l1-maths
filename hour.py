from typing import Tuple, Callable
from enum import IntEnum

class InputCodes(IntEnum):
    ASK = 0
    RETRY = 1

class TimeMetaData():
    nb: int = 0;
    sec_change_rate: int = 0;
        
    def condition(self, x: int) -> bool:
        return x < self.nb;
        
class Seconds(TimeMetaData):
    nb: int = 60;
    sec_change_rate: int = 1;   

class Minute(TimeMetaData):
    nb: int = 60;
    sec_change_rate: int = Seconds.nb;

class Hour(TimeMetaData):
    nb: int = 24;
    sec_change_rate: int = Minute.nb * Seconds.nb;

TIME_META_DATA_STRUCT: TimeMetaData = (Hour(), Minute(), Seconds())
NB_ELT_FORMAT: int = len(TIME_META_DATA_STRUCT);

data_time = int;
#<=== I/O ===>
def get_terminal_input(code: InputCodes) -> str:
    msg: Tuple[str] = ("Entrez une date au format HH:MM:SS: \n", "Assurez vous d'entrez une date au format HH:MM:SS: \n")
    return input(msg[code]);

def show_terminal_data_time(data: data_time) -> None:
    msg: str = "Time: ";
    for i in range(NB_ELT_FORMAT -1):
        change_rate: int = TIME_META_DATA_STRUCT[i].sec_change_rate;
        
        msg += str(data // change_rate);
        data %= change_rate;
        msg += ':';
    
    print(msg[:-1]);

input_func: Callable[[InputCodes], str] = get_terminal_input;
output_func: Callable[[data_time], None] = show_terminal_data_time;
#<===/===>
#<=== Utils ===>
def try_convert_int(value) -> Tuple[bool, int | None]:
    try:
        return (True, int(value));
    
    except (ValueError, TypeError):
        return (False, None);
#<===/===>
#<=== Utils Time Convertion ===>
def try_convert_positiv_integer_with_condition(data_str: str, func_condition: Callable[[int], bool]) -> Tuple[bool, int | None]:
    temp_int: Tuple[bool, int | None] = try_convert_int(data_str);
    
    if not temp_int[0]:
        return (False, None);
    
    if temp_int[1] < 0 or not func_condition(temp_int[1]):
        return (False, None);
        
    return temp_int;

def try_convert_data_time(data_str: str, ids: int) -> Tuple[bool, data_time | None]:
    time_meta_data = TIME_META_DATA_STRUCT[ids];
    
    temp: Tuple[bool, int | None] = try_convert_positiv_integer_with_condition(data_str, time_meta_data.condition);
    if temp[0]:
        temp = (True, temp[1] * time_meta_data.sec_change_rate);
    return temp

def try_convert_data_time_input(user_input: str) -> Tuple[bool, data_time | None]:
    user_input = user_input.split(":");
    user_data_time: data_time = 0;
    
    if(len(user_input) != NB_ELT_FORMAT):
        return (False, None);
    
    data: Tuple[bool, int | None];
    for i in range(NB_ELT_FORMAT):
        data = try_convert_data_time(user_input[i], i);
        if(not data[0]):
            return (False, None);
        
        user_data_time += data[1];
    
    return (True, user_data_time)
#<===/===>
    
def get_data_time_input() -> data_time:
    user_input = input_func(InputCodes.ASK);
    
    temp_result: Tuple[bool, data_time | None];
    
    while not (temp_result := try_convert_data_time_input(user_input))[0]:
        user_input = input_func(InputCodes.RETRY);
    
    return temp_result[1];

def add_sec(data: data_time, nb: int) -> data_time:  
    return data + nb;

def add_minute(data: data_time, nb: int) -> data_time:  
    return data + nb * Minute.sec_change_rate;

def add_hour(data: data_time, nb: int) -> data_time:  
    return data + nb * Hour.sec_change_rate;

t = get_data_time_input();
t = add_minute(t, 1);

output_func(t);
