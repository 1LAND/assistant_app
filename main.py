import pyautogui as pg
import time
import threading 

need_wait = True

def thread(fn):
    def execute(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs).start()
    return execute


@thread
def wait_game():
    x = 0
    while True:
        if not need_wait:
            break
        if x%5==0:
            pg.click(950,788)
        _time = f'Прошло {x//60} минут'
        print(_time)
        time.sleep(1)
        x +=1 
@thread        
def game_start():
    pg.moveTo(1265,180,2.5)
    pg.click(1265,180)
    pg.moveTo(300,120,2.5)
    pg.click(300,120)
    pg.moveTo(400,780,2.5)
    pg.click(400,780)
    pg.moveTo(890,920,2.5)
    pg.click(890,920,10,1)
    wait_game()
defList = {
    'Ждем катку': wait_game,
    'Запускаем катку + ждем катку':game_start
}

def main():
    defList.get(pg.confirm('Что делаем?','Что делаем?',('Запускаем катку + ждем катку','Ждем катку')), 'err')()

if __name__ == '__main__':
    wait_game()