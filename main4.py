import configparser
import subprocess
import pyautogui
import sys
import time
from datetime import datetime
from datetime import timedelta
from time import mktime
import python_imagesearch.imagesearch as imgsearch
from pyclick import HumanClicker
from pynput.keyboard import Key
from pynput.keyboard import Controller
import pynput.keyboard
import random
#new - добавил я 26 числа. Не тестил 2 добавления.
'''
Буду стараться по максимуму фиксить баги, чтобы быстрее закончить разработку.
'''
'''
Код красивый. Хочу так же научиться)
'''
path = 'img\\'
print('Starting TLM_digger...')
exec_stop = False
mode = 'autoclicker'
hc = HumanClicker()
keyboard = Controller()
#mode = "pos_logger":
debug = True

btn = {'mine': (),
       'close_d': (),
        }



def see(image):
    position = imgsearch.imagesearch(path + image + '.png')
    if position[0] != -1:
        if debug:
            print(f'SEE:    {image} {str(position)}')
        return True
    else:
        return False


def click(*btn):
    x1, x2, y1, y2 = btn

    if bool(random.getrandbits(1)):
        hc.move((random.randint(0,800),random.randint(0,600)),1)
    if bool(random.getrandbits(1)):
        time.sleep(random.randint(2,4))
    coord = (random.randint(x1, x2) , random.randint(y1, y2))
    hc.move(coord, 1)
    hc.click()
    if debug:
        print('CLICK: ' + str(coord))


def run_browser():
    config = configparser.ConfigParser()
    try:
        config.read('conf.ini')
        exe = config['browser']['exe']
    except Exception as e:
        exe = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
    if debug:
        print(f'Opening  browser {exe}')
    subprocess.Popen(exe + " http://play.alienworlds.io")
    time.sleep(2)
    subprocess.Popen(exe + " https://wallet.wax.io/dashboard")
    time.sleep(5)
    #БАГ! На расширении 800х600 нужен костыль для скролла сайта вниз. Допилил ниже
    #Не тестил. Может уйти в вечный  цикл. Надеюсь, что нет. Завтра будем тестить весь код
    # + на ночь 5 серверов поставил
    subprocess.Popen(exe + " https://wax.alcor.exchange/swap?output=WAX-eosio.token&input=TLM-alien.worlds-eosio.token")
    time.sleep(5)
    while True:
        if see("tlm"):
            click(785,793,543,556)
            break
    # Простой способ переключить вкладку
    with keyboard.pressed(Key.ctrl):
        keyboard.press('1')


def close_browser():
    if debug:
        print('Trying to close browser')
    click(753,796,0,16)


class Sleeper:
    """ """

    def __init__(self):
        """ """
        self.hanguptime = (13,0)
        self.sleepmin = 420
        timeformat = "%H:%M"
        dhu = datetime.strptime("13:00",timeformat)
        self.schedule = {'sleep': ( dhu,dhu + timedelta(minutes=420)), }
        # wt = ht + timedelta(minutes=self.sleepmin)
        config = configparser.ConfigParser()
        try:
            config.read('conf.ini')
            print('Config found in conf.ini')
            self.hanguptime = config['sleep']['hanguptime'].split(':')
            self.hanguptime[0] = int(self.hanguptime[0])
            self.hanguptime[1] = int(self.hanguptime[1])
            self.sleepmin = int(config['sleep']['sleep'])
            msg = f'Go to sleep at {self.hanguptime[0]}:{self.hanguptime[1]} for '
            print(f'{msg} {self.sleepmin} minutes')
            hu = datetime.strptime(config['sleep']['hanguptime'],timeformat)
            self.schedule['sleep'] = (hu , hu + timedelta(minutes=self.sleepmin))
            print('Naping at:')
            for block in config:
                if block.startswith('nap'):
                    msg = f'"{block}" at {config[block]["start"]} for '
                    print(f'{msg} {config[block]["napsec"]} sec')
                    d = config[block]["napsec"].split('-')
                    d = timedelta(seconds=random.randint(int(d[0]),int(d[1])))
                    hu = config[block]['start'].split('-')
                    t1 = datetime.strptime(hu[0],"%H:%M")
                    t2 = datetime.strptime(hu[1],"%H:%M")
                    # print(t1)
                    ds = timedelta(seconds=random.randint(0,((t2-t1).total_seconds())))
                    hu = t1 + ds
                    wu = hu + d
                    print(f'      from {hu.time()} till {wu.time()}')
                    self.schedule[str(block)] = (hu , wu)
                    # print(time.mktime(t2)-time.mktime(t1))
            # print(self.schedule)
            # wakeuptime = time.strftime('%H:%m',config['sleep']['hanguptime'])
        except Exception as e:
            print(e)
            print('Config not found in conf.ini use defaults: sleep from 13:00 till 20:00')
            print(f'Go to sleep at {self.hanguptime} for {self.sleepmin} minutes')


    def timetosleep(self):
        dt = datetime.now()
        for item in self.schedule:
            hu = self.schedule[item][0].replace(year=dt.year,
                                                month=dt.month,
                                                day=dt.day)
            wu = self.schedule[item][1].replace(year=dt.year,
                                                month=dt.month,
                                                day=dt.day)
            if hu < dt < wu:
                ss = (wu-dt).total_seconds()
                print(f'Now is time to sleep untill {wu} ({item})')
                if debug:
                    print(f'Sleep: {ss}sec')
                close_browser()
                time.sleep(ss)
                run_browser()
        return False



def reload(tab=0):
    '''
    идея по коду - добавить условие на наличие капчи. При наличии будет закрывать
    в этой функции вместо закрытия капчи перед вызовом функции
    '''
    click(83, 95, 54, 64)
    time.sleep(15)
    if changeTab != 0:
        changeTab(tab=tab)


def captcha():
    #Таймер на капчу. Если больше минуты - закрывает капчу, перезапускает вкладку, return
    # добавлено сегодня вместо кода на 191 строке. Не тестил.
    timer = 0
    '''
    Функция решает любую всплывающую капчу. Не возвращает ничего.
    '''
    tr_load = 0
    while True:
        # Ищет изображение появления капчи
        if see("transaction_request"):
            click(605, 607, 373, 533)
        time.sleep(1)
        # Ищет кнопку прохождения капчи(условие выполняется даже до решения капчи ботом(не знаю почему))
        if see("captcha_solved"):
            click(169, 436, 336, 372)

        #new. Нашёл картинку, которая появляется только в капче и постоянно её видно.
        if not see("wax_cloud_2"):
            return


        #Поиск по вечной загрузке транзакции(баги серверов)
        '''
        Идея по коду: вместо поиска бесконечных загрузок сделать отдельный таймер, который будет
        перезагружать страницу после 3 минут какого-то процесса, который так и не закончился
        (например, бесконечный логин в аккаунт после трёх минут будет перезагружать страницу
        , а если бесконечная загрузка капчи - то и закрыть капчу)
        '''
        #new
        timer += 1
        if timer == 40:
            # Поиск ошибки на всякий случай, чтобы закрыть её в случае чего перед перезагрузкой
            if see("error"):
                click(587, 624, 200, 205)
            # Закрытие капчи
            click(580, 600, 7, 23)
            # Сброс таймера
            timer = 0
            # Перезагрузка страницы(необходимо добавить)
            reload()
            # Выход из функции капчи для повтора заново функции
            return

        # Поиск по просрочености решения капчи. Перезагружает страницу
        if (see("solve_again")) or \
                (see("solve_again_2")) or \
                    (see("solve_again_3")):
            # Закрывает капчу
            click(580, 600, 5, 10)
            reload()
            return

        time.sleep(1)


def changeTab(tab=1, stack=0):
    '''
    Перекликивает между рабочими вкладками(всего их 3
    первая - вкладка алиен ворлдс(номер указывает её положение в браузере. По другому не работает))
    Вторая - вкладка кошелька вакс - https://wallet.wax.io/dashboard
    Третья - вкладка биржи алкор, где будет меняться 3 тлм на вакс для покупки ресурсов для работы игры)
    Вызывает под каждую вкладку её функцию
    '''
    '''
    new - идея по коду - сделать переключение вкладки также по контрл. Сам не сделал - 
    боюсь багов
    '''
    # tab alien
    if tab == 1:
        # Перекликивает на вкладку alien worlds (игра)
        click(7, 149, 7, 26)
        # Ищет ошибку любую(в игре проводится поиск на любую ошибку, кроме ошибку покупки ресурсов), а тут - любую ошибку
        if see("error"):
            click(587, 624, 200, 205)
        #Вызывает основную функцию
        run(0)
    # Вкладка кошелька вакс
    if tab == 2:
        '''Перекликивает на вкладку кошелька и запускает функцию
        с pereklik = True, вызывается в функции alkor_swap после её полной отработки
        для покупки ресурсов. Если параметр pereklik = False, то функция buy_resourses
        вызовет функцию alkor_swap'''
        click(204, 358, 6, 21)
        buy_resourses(stack, pereklik=True)
    # Перекликивает на функцию alkor_swap. Вызывается функцией buy_resourses
    if tab == 3:
        click(395, 538, 5, 17)
        alkor_swap(stack)


def alkor_swap(stack):
    """
    Функция автоматически меняет 3 тлм на вакс для покупки ресурсов.
    """
    '''
    Идея по коду( добавить сюда так же проверку по изображениям, как и везде в коде)
    Для перестраховки на случай долгой загрузки
    '''
    time.sleep(1)
    #Клик по области ввода количества токенов
    time.sleep(1)
    #нужны чёткие координаты. Поэтому, не подойдёт функция. Случай единичный.
    hc.move((67,258), 1)
    hc.click()
    #Ввод цифры 3 в область ввода
    time.sleep(0.5)
    keyboard.press('1')
    keyboard.release('1')
    time.sleep(2)
    # Клик на кнопку swap tlm
    click(40, 745, 455, 490)
    #Вызов функции решения капчи
    captcha()
    #Вызов функции buy_resourses
    changeTab(tab=2, stack = stack)


def buy_resourses(stack, pereklik = False):
    '''
    Покупает в кошельке вакс два вида ресурсов в зависимости от переменной stack
    stack = 1 , то будет куплен ресурс cpu
    stack = 2 , то будет куплен ресурс ram
    Картинки с ошибкой ram нету, т.к. ошибка редкая , но всё равно рано или поздно выскочит
    Как только будет картинка - скину
    '''
    while True:
        time.sleep(1)
        # Если pereklik = False - вызов функции alcor_swap
        '''
        Идея по коду - убрать этот велосипед вызыванием функции alcor_swap сразу же, а не
        через функцию buy_resources
        '''
        if not pereklik:
            changeTab(tab=3, stack= stack)
        # Кликает на картинку вакса, для вызова меню, где можно купить ресурсы
        if see("wax_ava_v_nft"):
            click(758, 776, 90, 104)
        # Кликает на кнопку ресурсов. Поиск проводится по скриншоту немного выше сделанному,
        # т.к. слетает винда, но не на всех акках, из-за этого не находит скрин
        if see("resources"):
            click(588, 747, 448, 477)
            #Кликает по пустому месту в новом окне, чтобы сделать его активным
            click(46, 536, 275, 505)
            time.sleep(1)
        # Нажимает page_down для скролла сайта вниз
        if see("network_resources"):
            keyboard.press(Key.page_down)
            time.sleep(1)
        if stack == 2:
            # Если нужно купить ресурс рам - выбирает его.
            click(132, 199, 446, 475)
            click(123, 211, 538, 551)
        # покупает ресурс
        if see("stake") or see("buy"):
            click(239, 409, 449, 475)
            time.sleep(0.5)
            keyboard.press('1')
            keyboard.release('1')
            click(439, 503, 441, 477)
            captcha()
            # Перезагружает вкладку с перекликом в основную фукцию игры.
            reload(tab=1)
        time.sleep(1)


def run(cpu):
    '''
    Основная функция для alien worlds.
    '''
    #Таймеры для сброса бесконечного выполнения процессов
    #Опять же идея - сделать таймер. Выше уже была озвученя
    c = 0
    m = 0
    al_w = 0
    tr_log = 0
    tr_load = 0
    fet = 0
    message = ''
    sleeper = Sleeper()

    # While there's no 'execution stop' command passed
    while exec_stop is False:
        # If the script is in autoclicker mode
        if mode == "autoclicker":
            try:
                # Проверка на бесконечность одного из процессов. В случае превышения лимита
                # Проверяет экран на ошибку и закрывает в случае нахождения.
                # Перезагружает страницу
                '''
                Идея по коду - вывести постоянно повторяющиеся проверки в отдельную функцию
                Например, проверка на выскакивающую ошибку и любой клик.
                '''
                # Бесконечный процесс захода в аккаунт

                if see("fetching_in_login"):
                    fet += 1
                    if fet == 40:
                        fet = 0
                        if see("error"):
                            click(587, 624, 200, 205)
                        reload()

                # Бесконечный процесс клейминга
                if see("claiming_tlm"):
                    c += 1
                    if c == 40:
                        c = 0
                        if see("error"):
                            click(587, 624, 200, 205)
                        reload()

                # бесконечная загрузка страницы при перезагрузке
                if see("alien_worlds"):
                    al_w += 1
                    if al_w == 40:
                        al_w = 0
                        if see("error"):
                            click(587, 624, 200, 205)
                        reload()

                # Бесконечный процесс майнинга
                if see("mining_in_progress"):
                    m += 1
                    if m == 60:
                        if see("error"):
                            click(587, 624, 200, 205)
                        m = 0
                        reload()

                # Ещё одна ошибка на бесконечную загрузку транзакции
                if see("transaction_in_login"):
                    tr_log += 1
                    if tr_log == 40:
                        if see("error"):
                            click(580, 600, 200, 205)
                        click(572, 596, 7, 23)
                        tr_log = 0
                        reload()

                # Ошибка на бесконечную загрузку транзакции
                if see("loading_transaction"):
                    tr_load += 1
                    if tr_load == 40:
                        if see("error"):
                            click(580, 600, 200, 205)
                        click(572, 596, 7, 23)
                        tr_load = 0
                        reload()
                time.sleep(1)


                #Клейм в хабе(появляется после перезагрузки страницы, если сработал таймер на вечный клейм)
                #проверка на ошибки с двух сторон т.к. может выскочить на одном экране и error и claim
                #и код начнёт жёстко тупить
                #new - после необъявленного обновления в алиен ворлдсе теперь показывает
                #stack_cpu даже когда не израсходовались ресурсы и можно просто закрыть
                #ошибку и всё пройдёт. Поэтому, вот такой вот костыль между клеймами,
                #чтобы не ушло в капчу.
                if see("stack_cpu"):
                    if cpu > 6:
                        print('go swap!')
                        cpu = 0
                        changeTab(tab=3, stack=1)
                    else:
                        print('don`t swap!')
                        cpu += 1
                        click(597, 612, 190, 204)
                if (see("error")) and not see("stack_cpu"):
                    click(587, 624, 200, 205)
                if (see("claim_in_hub")):
                    click(355, 440, 490, 512)
                    captcha()
                if (see("error")) and not see("stack_cpu"):
                    click(587, 624, 200, 205)
                if see("stack_cpu"):
                    if cpu > 6:
                        print('go swap!')
                        cpu = 0
                        changeTab(tab=3, stack=1)
                    else:
                        print('don`t swap!')
                        cpu += 1
                        click(597, 612, 190, 204)
                #кнопка mine в хабе
                #Хаб - окно которое появляется после прохода одного круга успешно и нажатия на кнопку mining_hub кликером
                #Круг - когда, начисляют tlm и нажимается кнопка mining_hub - то один круг пройден
                if see("mine"):
                    m = 0
                    click(354, 441, 490, 510)

                # Claim TLM button
                if see("stack_cpu"):
                    if cpu > 6:
                        print('go swap!')
                        cpu = 0
                        changeTab(tab=3, stack=1)
                    else:
                        print('don`t swap!')
                        cpu += 1
                        click(597, 612, 190, 204)
                if (see("error")) and not see("stack_cpu"):
                    click(587, 624, 200, 205)

                if (see("claim")) and not see("home"):
                    c = 0
                    click(363, 433, 352, 370)
                    captcha()
                if (see("error")) and not see("stack_cpu"):
                    click(587, 624, 200, 205)
                if see("stack_cpu"):
                    if cpu > 6:
                        print('go swap!')
                        cpu = 0
                        changeTab(tab=3, stack=1)
                    else:
                        print('don`t swap!')
                        cpu += 1
                        click(597, 612, 190, 204)

                time.sleep(1)
                #Back to mining hub button
                if see("go_to_hub"):
                    #Сбрасывает все таймеры
                    c = 0
                    m = 0
                    al_w = 0
                    tr_log = 0
                    tr_load = 0
                    fet = 0
                    click(154, 272, 452, 474)
                    '''New. Перенёс сюда проверку т.к. надо, чтобы багов не было.
                    Например, один акк ушёл в сон на капче и забагал. + не будет 
                    одновременно целая куча уходить в сон, то есть меньше шанс на бан'''
                    sleeper.timetosleep()
                #При перезагрузке нажимает на кнопку логин
                if see("login"):
                    click(355, 439, 419, 443)
                #После перезагрузки заходит в хаб нажатием кнопки mine
                if see("mine_not_in_hub"):
                    click(595, 716, 217, 243)
                ##Поиск на ошибку( лишний поиск никогда не бывает лишним)
                #if (see("error")) and not see("stack_cpu"):
                #    click(587, 624, 200, 205)
                #Если просит зайти в аккаунт вакс - автоматически заходит
                if see("login_wax"):
                    click(176, 423, 267, 295)
                #Кликает на gmail при заходе в вакс
                if see("gmail_wax"):
                    click(243, 259, 180, 206)
                time.sleep(1)

                # Нет картинки ошибки, поэтому код не готов(
                # if see("stack_ram"):
                #     changeTab(tab=2, stack=2)

                '''new - есть ошибка fetch in login, которая не фиксится кодом
                это баги серверов. После того, как ошибка проходит выскакивает меню
                выбора планет. Необходимо перезагрузить страницу и всё пройдёт.
                ''' 
                if see("planet"):
                    reload()

                #Ошибка с тем, что выходит из сессии кошелька вакс при долгой игре
                if see("session"):
                    click(186, 427, 291, 320)
            except Exception as e:
                # If an error occurred
                print("An error occurred: ", e)
                sys.exit(0)
        # If the script is in position logger mode
        else:
            #Режим вывода позиции курсора
            try:
                # Print position to console every second
                print(pyautogui.position())
                time.sleep(1)
            except Exception as e:
                # If an error occurred
                print("An error occurred: ", e)


def on_press(key):
    if key == pynput.keyboard.Key.f1:
        changeTab(tab=1)
    if key == pynput.keyboard.Key.f7:
        run_browser()
    if key == pynput.keyboard.Key.f9:
        close_browser()
    if key == pynput.keyboard.Key.f8:
        global debug
        debug = True if debug == False else False
        print(f"Debug:  {str(debug)}")
    # When F10 key is pressed, toggle modes between Autoclicker and Position Logger
    if key == pynput.keyboard.Key.f10:
        global mode
        mode = "pos_logger" if mode == "autoclicker" else "autoclicker"
        print(f"Changing mode to {mode}")
    # When F12 key is pressed, stop executing the script
    elif key == pynput.keyboard.Key.f12:
        global exec_stop
        exec_stop = True
        print("Shutting down...")
        sys.exit(0)


def main():
    # Listen for pressed keys
    listener = pynput.keyboard.Listener(on_press=on_press)
    listener.start()
    run(0)


if __name__ == '__main__':
    main()
