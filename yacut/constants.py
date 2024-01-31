from string import ascii_lowercase, ascii_uppercase, digits

# Values
VALID_VALUE = ascii_uppercase + ascii_lowercase + digits

# Errors
EMPTY_REQUEST = 'Отсутствует тело запроса'
EMPTY_URL = '\"url\" является обязательным полем!'
SHORT_LINK_EXIST = 'Предложенный вариант короткой ссылки уже существует.'
TOO_LONG_LINK = 'Предложенный вариант короткой ссылки больше 16 знаков.'
NOT_VALID_LINK = 'Указано недопустимое имя для короткой ссылки.'
LINK_NOT_EXIST = 'Указанный id не найден'
