import pyautogui as pg
import time

def err():
    print('[err]')
    pg.alert('Что-то сломалось','Ошибка')
def start_lol():
    pg.hotkey("winleft")
    pg.typewrite("lol")
    pg.typewrite(["enter"])

need_wait = True
def wait_game():
    for i in range(120):
        if not need_wait:
            break
        pg.click(950,788)
        if i%12==0:
            print(f'прошло {i//12} минут ')
        time.sleep(5)
        
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
    None:lambda : print,
    'err':err,
    'Запускаем лол':start_lol,
    'Ждем катку': wait_game,
}

def main():
    defList.get(pg.confirm('Что делаем?','Что делаем?',('Запускаем лол','Ждем катку')), 'err')()

if __name__ == '__main__':
    wait_game()