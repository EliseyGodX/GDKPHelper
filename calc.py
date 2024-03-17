import pprint
from sympy import symbols, solve
CHEQUE = {
    'error': 'Не было получено данных с таблицы'
}

def calculator(data: dict) -> None:
    global CHEQUE

    x = symbols('x')
    equation = (data['bonus']['005']*(x+data['wholeBank']*0.005) + 
                data['bonus']['010']*(x+data['wholeBank']*0.010) +
                data['bonus']['015']*(x+data['wholeBank']*0.015) + 
                data['bonus']['100']*(x+data['wholeBank']*0.100) +
                data['raiders_norOrdinary']*x +
                data['fine']['10']*(x*0.9) + 
                data['fine']['25']*(x*0.75) + 
                data['fine']['50']*(x*0.5) + 
                data['fine']['75']*(x*0.25) - 
                data['wholeBank'])
    try:
        x = int(solve(equation, x)[0])
    except Exception as exc:
        CHEQUE['error'] = exc
        return
    CHEQUE = data
    CHEQUE['x'] = x
    


def pcheque():
    if len(CHEQUE.keys()) <= 1: return 'Ошибка, перезапустите приложение'
    return pprint.pformat(CHEQUE)