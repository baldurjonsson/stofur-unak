from datetime import datetime
from tabulate import tabulate
import stofur

stofa = 'L102'
stofa_input = input(f'Hvaða stofa? [default: {stofa}]: ')
if stofa_input != '':
    stofa = stofa_input

date = datetime.now().replace(second=0, microsecond=0)

date_input = input(f'Hvaða dag? [default: {date.strftime("%d.%m.%Y")}]: ')
if date_input != '':
    date_input_split = date_input.split('.')
    date = date.replace(day=int(date_input_split[0]), month=int(date_input_split[1]), year=int(date_input_split[2]))

time_input = input(f'Klukkan hvað? [default: {date.strftime("%H:%M")}]: ')
if time_input != '':
    time_input_split = time_input.split(':')
    date = date.replace(hour=int(time_input_split[0]), minute=int(time_input_split[1]))

table = stofur.get_data(date, stofa)

if len(table) == 0:
    print('Stofan er ekkert bókuð þennan dag!')
else:
    occupied = False
    for slot in table:
        from_split = slot['from'].split(':')
        from_hour = int(from_split[0])
        from_minute = int(from_split[1])
        to_split = slot['to'].split(':')
        to_hour = int(to_split[0])
        to_minute = int(to_split[1])
        if from_hour <= date.hour <= to_hour:
            if from_minute <= date.minute <= to_minute:
                occupied = True
                break

    print('Eftirfarandi tíma er stofan bókuð:')
    print(tabulate(table, headers={'from': 'Frá', 'to': 'Til', 'comment': 'Athugasemd', 'group': 'Hópur'}))
    if occupied:
        print('\nStofan er upptekin á skilgreindum tíma.')
    else:
        print('\nStofan virðist vera laus. Sjá nánar í töflu')