documentation_ru = """

Проект Heating представляет собой автоматизированный инструмент для Telegram, разработанный для симуляции активности пользователя в различных каналах и чатах. Основная цель проекта - создать естественную модель поведения пользователя, включая присоединение к каналам, взаимодействие с контентом и управление профилем.

> **Обязательно прочтите перед использованием!**
> Ваши аккаунты могу быть заблокированы, для того чтобы снизить шансы, покупайте только зарегистрированные вручную аккаунты.
> ВАЖНО использовать прокси той страны в которой аккаунт был зарегистрирован.
> На один аккаунт используем один прокси.
> Софт лишь помогает выполнять те действия, которые вы выполняли бы вручную.
> Используйте на свой страх и риск!

**Основные возможности:**

1. **Автоматическое присоединение к каналам**:
   - Скрипт может присоединяться к заданному списку каналов. Ссылки на каналы добавляете в файл channels.py
   - После присоединения автоматически отключаются уведомления для каждого канала.

2. **Симуляция активности пользователя**:
   - Имитация набора текста
   - Симуляция чтения сообщений
   - Имитация онлайн-статуса
   - Реакции на сообщения
   - Просмотр медиаконтента
   - Прокрутка ленты

3. **Управление профилем**:
   - Автоматическая установка аватара (Предварительно загрузите аватары в папку img)
   - Генерация и установка био. Автоматически генерирует уникальное био для каждого аккаунта.
   - Добавление эмодзи к имени пользователя

4. **Работа через прокси**:
   - Поддержка работы через прокси-серверы для каждой сессии

5. **Парсинг чатов**:
   - Возможность парсинга всех доступных чатов (опционально)

**Создание сессий либо использование готовых**
  - Для использования готовых сессий pyrogram добавьте их в папку sessions
  - Для создания новых сессий выполните команду `python main.py`
  - Выберите опцию 2 в главное меню программы и следуйте инструкциям на экране. 

**Работа с прокси**

Проект поддерживает работу через прокси-серверы. Для настройки прокси:

1. Заполните файл `session_proxy.json`, связав каждый аккаунт с отдельным прокси.
2. Для автоматического заполнения используйте скрипт `session_proxy_matcher.py`:
   - Добавьте прокси в файл `proxies.txt`
   - Назовите сессии в формате "1-Имя", "2-Имя" и т.д.
   - Запустите скрипт командой `python bot/config/proxies/session_proxy_matcher.py`

**Конфигурация**

Настройка проекта осуществляется в `config.py`. Рассмотрим основные параметры:

**Основные настройки**

- `API_ID` и `API_HASH`: 
  - Описание: Ключи API для работы с Telegram.
  - Как получить: Зарегистрируйте приложение на [my.telegram.org](https://my.telegram.org) и получите ключи.

**Настройки запуска**

- `USE_RANDOM_DELAY_IN_RUN`: 
  - Описание: Включает случайную задержку перед началом работы скрипта для каждой сессии.
  - Доступные значения: `True` или `False`

- `RANDOM_DELAY_IN_RUN`: 
  - Описание: Диапазон задержки в секундах `[мин, макс]`.
  - Доступные значения: пример, `[0, 3600]`. В данному случае для каждой сессии будет выбрана случайная задержка для старта в диапазоне от 0 до 3600 секунд.

**Настройки прокси**

- `USE_PROXY`: 
  - Описание: Включает или выключает использование прокси.
  - Доступные значения: `True` или `False`

**Настройки профиля**

- `SET_AVATAR`: 
  - Описание: Включает автоматическую установку аватара в профиль сессии.
  - Доступные значения: `True` или `False`

- `SET_BIO`: 
  - Описание: Включает автоматическую установку био в профиль сесии.
  - Доступные значения: `True` или `False`

- `SET_EMOJI`: 
  - Описание: Включает добавление эмодзи к имени пользователя.
  - Доступные значения: `True` или `False`

- `EMOJI_TO_SET`: 
  - Описание: добавляет модзи для добавления к имени.
  - Значение по умолчанию: Здесь вставляете нужный вам эмодзи, пример `"🌟"`

- `DELETE_ALL_EMOJI`: 
  - Описание: удаляет все эмодзи из имени и фамилии.
  - Доступные значения: `True` или `False`

- `AVATAR_DELAY_RANGE`: 
  - Описание: Диапазон задержки в часах перед установкой аватара `[мин, макс]`.
  - Значение по умолчанию: пример, `[48, 96]`. В данному случае для каждой сессии будет выбрана случайная задержка перед установкой аватара между 48 и 96 часами.

- `BIO_DELAY_RANGE`: 
  - Описание: Диапазон задержки в часах перед установкой био `[мин, макс]`.
  - Значение по умолчанию: пример, `[48, 96]`. В данному случае для каждой сессии будет выбрана случайная задержка перед установкой био между 48 и 96 часами. 

**Настройки парсинга**

- `PARSE_ALL_CHATS`: 
  - Описание: Включает режим парсинга всех доступных чатов для конкретной сессии.
  - Доступные значения: `True` или `False`

- `PARSE_ALL_CHATS_SESSION`: 
  - Описание: Имя сессии для парсинга всех чатов.
  - Доступные значения: Вставляте имя нужной сессии из папки sessions, пример `"Andrey"`

**Парсинг чатов**

Для парсинга всех доступных чатов:

1. Установите `PARSE_ALL_CHATS = True` в конфигурации.
2. Укажите имя сессии для парсинга в `PARSE_ALL_CHATS_SESSION`.

> **Важно**: Функция парсинга чатов должна использоваться с осторожностью и в соответствии с правилами Telegram.

---

**Отказ от ответственности:** _Используйте скрипт на свой страх и риск. Автор этого скрипта не несет ответственности за любые действия пользователей и их последствия, включая блокировку аккаунтов и другие ограничения. Мы рекомендуем вам быть осторожными и избегать передачи конфиденциальной информации, так как это может привести к компрометации ваших данных. Перед использованием обязательно ознакомьтесь с условиями обслуживания приложений, с которыми вы работаете, чтобы избежать нарушения их правил. Учитывайте, что автоматизация может вызвать нежелательные последствия, такие как временная или полная блокировка вашего аккаунта. Всегда действуйте осознанно и учитывайте возможные риски._
"""

documentation_en = """

The Heating project is an automated tool for Telegram designed to simulate user activity in various channels and chats. The main goal of the project is to create a natural model of user behavior, including joining channels, interacting with content, and managing the profile.

> **Be sure to read before use!**
> Your accounts may be blocked; to reduce the risk, purchase only manually registered accounts.
> It is IMPORTANT to use a proxy from the country where the account is registered.
> Use one proxy per account.
> The software only assists in performing actions you would otherwise do manually.
> Use at your own risk!

**Key Features:**

1. **Automatic Channel Joining**:
   - The script can join a specified list of channels. You can add channel links in the `channels.py` file.
   - Notifications are automatically disabled for each channel after joining.

2. **User Activity Simulation**:
   - Simulating typing
   - Simulating message reading
   - Simulating online status
   - Reacting to messages
   - Viewing media content
   - Scrolling the feed

3. **Profile Management**:
   - Automatic avatar setting (Preload avatars into the `img` folder)
   - Bio generation and setting. Automatically generates a unique bio for each account.
   - Adding emojis to the username.

4. **Proxy Support**:
   - Supports working through proxy servers for each session

5. **Chat Parsing**:
   - Optional feature to parse all available chats

**Create Sessions or Use Existing Ones**
  - To use existing pyrogram sessions, add them to the `sessions` folder.
  - To create new sessions, run in terminal: `python main.py`
  - Select option "2" in the main menu of the program and follow the prompts 

**Working with Proxies**

The project supports working through proxy servers. To configure proxies:

1. Fill in the `session_proxy.json` file by linking each account to a specific proxy.
2. Use the `session_proxy_matcher.py` script for automatic filling:
   - Add proxies to the `proxies.txt` file.
   - Name the sessions in the format "1-Name", "2-Name", etc.
   - Run the script with the command `python bot/config/proxies/session_proxy_matcher.py`

**Configuration**

Project configuration is done in `config.py`. Let’s review the key parameters:

**General Settings**

- `API_ID` and `API_HASH`: 
  - Description: API keys to interact with Telegram.
  - How to get them: Register your application at [my.telegram.org](https://my.telegram.org) and obtain the keys.

**Launch Settings**

- `USE_RANDOM_DELAY_IN_RUN`: 
  - Description: Enables a random delay before the script starts for each session.
  - Available values: `True` or `False`

- `RANDOM_DELAY_IN_RUN`: 
  - Description: Delay range in seconds `[min, max]`.
  - Available values: for example, `[0, 3600]`. In this case, each session will start with a random delay between 0 and 3600 seconds.

**Proxy Settings**

- `USE_PROXY`: 
  - Description: Enables or disables the use of proxies.
  - Available values: `True` or `False`

**Profile Settings**

- `SET_AVATAR`: 
  - Description: Enables automatic avatar setting in the session profile.
  - Available values: `True` or `False`

- `SET_BIO`: 
  - Description: Enables automatic bio setting in the session profile.
  - Available values: `True` or `False`

- `SET_EMOJI`: 
  - Description: Enables adding emojis to the username.
  - Available values: `True` or `False`

- `EMOJI_TO_SET`: 
  - Description: Specifies the emoji to be added to the username.
  - Default value: Insert the desired emoji here, for example, `"🌟"`

- `DELETE_ALL_EMOJI`: 
  - Description: removes all emoji from first and last name.
  - Available values: `True` or `False`.  

- `AVATAR_DELAY_RANGE`: 
  - Description: Delay range in hours before setting the avatar `[min, max]`.
  - Default value: for example, `[48, 96]`. In this case, each session will have a random delay before setting the avatar between 48 and 96 hours.

- `BIO_DELAY_RANGE`: 
  - Description: Delay range in hours before setting the bio `[min, max]`.
  - Default value: for example, `[48, 96]`. In this case, each session will have a random delay before setting the bio between 48 and 96 hours.

**Parsing Settings**

- `PARSE_ALL_CHATS`: 
  - Description: Enables the mode to parse all available chats for a specific session.
  - Available values: `True` or `False`

- `PARSE_ALL_CHATS_SESSION`: 
  - Description: The session name for parsing all chats.
  - Available values: Insert the name of the desired session from the `sessions` folder, for example, `"Andrey"`

**Chat Parsing**

To parse all available chats:

1. Set `PARSE_ALL_CHATS = True` in the configuration.
2. Specify the session name for parsing in `PARSE_ALL_CHATS_SESSION`.

> **Important**: The chat parsing feature should be used with caution and in accordance with Telegram’s rules.

---

**Disclaimer:** _Use the script at your own risk. The author of this script is not responsible for any user actions and their consequences, including account blocks or other restrictions. We recommend being cautious and avoiding sharing sensitive information as it may lead to data compromise. Before use, make sure to familiarize yourself with the terms of service of the applications you are working with to avoid violating their rules. Keep in mind that automation may lead to unwanted consequences, such as temporary or permanent account bans. Always act responsibly and be aware of potential risks._
"""

def get_documentation(language='ru'):
    return documentation_ru if language == 'ru' else documentation_en
