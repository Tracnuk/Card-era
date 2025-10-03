from colorama import init, Fore, Style
init(autoreset=True)


# -------------------------------
# Меню регистрации
# -------------------------------
Register_menu = f'''{Fore.YELLOW}______________________________________________________________{Style.RESET_ALL}


             {Fore.LIGHTMAGENTA_EX} М Е Н Ю   Р Е Г И С Т Р А Ц И И {Style.RESET_ALL}
{Fore.YELLOW}______________________________________________________________{Style.RESET_ALL}


                    {Fore.CYAN}1 - регистрация{Style.RESET_ALL}
                    {Fore.GREEN}2 - вход{Style.RESET_ALL}
                    {Fore.RED}3 - удаление аккаунта{Style.RESET_ALL}
                    {Fore.MAGENTA}0 - выход{Style.RESET_ALL}

                  Выберите пункт меню:

{Fore.YELLOW}______________________________________________________________{Style.RESET_ALL}'''
# -------------------------------
# Поле боя
# -------------------------------
Game_field = ' ' + '__________________________________________________________________________________________' + ' ' + '\n'
Game_field +=  '|' + Fore.RED + '■' * 40 + Style.RESET_ALL + ' ' * 10 +  Fore.BLUE + '■' * 40 + Style.RESET_ALL + '|'

count = 0
for _ in range(62):
    count += 1
    if count == 54:
        Game_field += '\n'
        Game_field +=  '|' + Fore.RED + '■' * 40 + Style.RESET_ALL + ' ' * 10 +  Fore.BLUE + '■' * 40 + Style.RESET_ALL + '|' + '\n'
        Game_field += '|__________________________________________________________________________________________|'
    else:
        Game_field += '\n|                                                                                          |'
Game_field += '\n'
Game_field += ' ' + '-' * 90 + ' ' 

# -------------------------------
# Главное меню игры
# -------------------------------
Game_menu = f'''{Fore.YELLOW}____________________________________________________________________________________________{Style.RESET_ALL}
|                                                                                          |
|                                   {Fore.CYAN}М Е Н Ю   И Г Р Ы{Style.RESET_ALL}                                      |
|                                                                                          |
|                                  {Fore.LIGHTRED_EX}1 - Начать бой ⚔️{Style.RESET_ALL}                                       |
|                                  {Fore.GREEN}2 - Войти в инвентарь 🧰{Style.RESET_ALL}                                |
|                                  {Fore.YELLOW}3 - Настройки аккаунта ⚙️{Style.RESET_ALL}                               |
|                                  {Fore.MAGENTA}4 - Открыть магазин 🛒{Style.RESET_ALL}                                  |
|                                  {Fore.CYAN}0 - Выход из игры ❌{Style.RESET_ALL}                                    |
|                                                                                          |
|                                  {Fore.WHITE}Выберите пункт меню:{Style.RESET_ALL}                                    |
|                                                                                          |
{Fore.YELLOW}____________________________________________________________________________________________{Style.RESET_ALL}'''


bear = '''_/□\\_
ʕ•ᴥ•ʔ'''

cat = '''/\\_/\\
(•·•)'''

bunny = '''(\\_/)
(•×•)'''

print(Game_field)
print(len('____________________________________________________________________________________________'))