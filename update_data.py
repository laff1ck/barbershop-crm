"""Update services to Russian + regenerate clients with Russian names in patronymic format."""
import os, sys, random
sys.path.insert(0, r'D:\CRM\barbershop_crm')
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.development'

import django
django.setup()

from apps.services.models import Service, ServiceCategory
from apps.clients.models import Client
from apps.staff.models import Master

# ─── 1. RENAME SERVICE CATEGORIES ───────────────────────────────────────────
CAT_MAP = {
    'Haircuts': ('Стрижки',    'bi-scissors'),
    'Beard':    ('Борода',     'bi-brush'),
    'Combos':   ('Комплексы',  'bi-stars'),
}
for eng, (rus, icon) in CAT_MAP.items():
    updated = ServiceCategory.objects.filter(name=eng).update(name=rus, icon=icon)
    print(f"Category: {eng} -> {rus} ({updated} rows)")

# ─── 2. RENAME SERVICES ──────────────────────────────────────────────────────
SVC_MAP = {
    'Classic cut':    ('Классическая стрижка',     30, 800),
    'Machine cut':    ('Стрижка машинкой',          20, 600),
    'Kids cut':       ('Детская стрижка',            25, 500),
    'Cut+style':      ('Стрижка + укладка',          45, 1200),
    'Beard trim':     ('Оформление бороды',          20, 600),
    'Straight razor': ('Бритьё опасной бритвой',    30, 900),
    'Mustache trim':  ('Коррекция усов',             15, 400),
    'Cut+Beard':      ('Стрижка + борода',           50, 1400),
    'Royal shave':    ('Королевское бритьё',         60, 1800),
}
for eng, (rus, dur, price) in SVC_MAP.items():
    updated = Service.objects.filter(name=eng).update(name=rus, duration=dur, price=price)
    print(f"Service: {eng} -> {rus} ({updated} rows)")

# ─── 3. REGENERATE CLIENTS WITH RUSSIAN NAMES ────────────────────────────────
SURNAMES = [
    'Иванов','Петров','Сидоров','Смирнов','Кузнецов','Попов','Лебедев',
    'Козлов','Новиков','Морозов','Волков','Соловьёв','Васильев','Зайцев',
    'Павлов','Семёнов','Голубев','Виноградов','Богданов','Воробьёв',
    'Фёдоров','Михайлов','Беляев','Тарасов','Белов','Комаров','Орлов',
    'Киселёв','Макаров','Андреев','Ковалёв','Ильин','Гусев','Титов',
    'Кириллов','Марков','Крылов','Громов','Захаров','Матвеев','Осипов',
    'Чернов','Александров','Дмитриев','Егоров','Никитин','Сафонов',
    'Рыбаков','Степанов','Медведев',
]

FIRST_NAMES = [
    'Александр','Алексей','Андрей','Антон','Артём','Борис','Вадим',
    'Василий','Виктор','Виталий','Владимир','Вячеслав','Геннадий',
    'Денис','Дмитрий','Евгений','Иван','Игорь','Илья','Кирилл',
    'Константин','Максим','Михаил','Никита','Николай','Олег','Павел',
    'Роман','Руслан','Сергей','Степан','Тимур','Фёдор','Юрий','Яков',
]

# Patronymics derived from first names
PATRONYMIC_MAP = {
    'Александр': 'Александрович', 'Алексей': 'Алексеевич',
    'Андрей': 'Андреевич', 'Антон': 'Антонович',
    'Артём': 'Артёмович', 'Борис': 'Борисович',
    'Вадим': 'Вадимович', 'Василий': 'Васильевич',
    'Виктор': 'Викторович', 'Виталий': 'Витальевич',
    'Владимир': 'Владимирович', 'Вячеслав': 'Вячеславович',
    'Геннадий': 'Геннадьевич', 'Денис': 'Денисович',
    'Дмитрий': 'Дмитриевич', 'Евгений': 'Евгеньевич',
    'Иван': 'Иванович', 'Игорь': 'Игоревич',
    'Илья': 'Ильич', 'Кирилл': 'Кириллович',
    'Константин': 'Константинович', 'Максим': 'Максимович',
    'Михаил': 'Михайлович', 'Никита': 'Никитич',
    'Николай': 'Николаевич', 'Олег': 'Олегович',
    'Павел': 'Павлович', 'Роман': 'Романович',
    'Руслан': 'Русланович', 'Сергей': 'Сергеевич',
    'Степан': 'Степанович', 'Тимур': 'Тимурович',
    'Фёдор': 'Фёдорович', 'Юрий': 'Юрьевич',
    'Яков': 'Яковлевич',
}

# Transliterate surname for email
def translit(s):
    T = {
        'А':'A','Б':'B','В':'V','Г':'G','Д':'D','Е':'E','Ё':'E','Ж':'Zh',
        'З':'Z','И':'I','Й':'Y','К':'K','Л':'L','М':'M','Н':'N','О':'O',
        'П':'P','Р':'R','С':'S','Т':'T','У':'U','Ф':'F','Х':'Kh','Ц':'Ts',
        'Ч':'Ch','Ш':'Sh','Щ':'Shch','Ъ':'','Ы':'Y','Ь':'','Э':'E',
        'Ю':'Yu','Я':'Ya',
    }
    return ''.join(T.get(c, c) for c in s)

masters = list(Master.objects.filter(is_active=True))
random.seed(42)
used_phones = set()
used_emails = set()

clients = list(Client.objects.all().order_by('pk'))
surname_list = SURNAMES[:len(clients)]
random.shuffle(surname_list)

for i, client in enumerate(clients):
    surname   = surname_list[i % len(SURNAMES)]
    first     = random.choice(FIRST_NAMES)
    patronymic = PATRONYMIC_MAP.get(first, first + 'ович')

    # Unique email
    base_email = translit(surname) + '@example.com'
    email = base_email
    counter = 2
    while email in used_emails:
        email = translit(surname) + str(counter) + '@example.com'
        counter += 1
    used_emails.add(email)

    # Unique phone
    phone = f"+7-9{random.randint(10,99)}-{random.randint(100,999)}-{random.randint(10,99)}-{random.randint(10,99)}"
    while phone in used_phones:
        phone = f"+7-9{random.randint(10,99)}-{random.randint(100,999)}-{random.randint(10,99)}-{random.randint(10,99)}"
    used_phones.add(phone)

    client.last_name  = surname
    client.first_name = f"{first} {patronymic}"  # Store "Имя Отчество" in first_name
    client.email      = email
    client.phone      = phone
    client.save(update_fields=['first_name', 'last_name', 'email', 'phone'])

print(f"\nUpdated {len(clients)} clients.")
print("\nSample clients:")
for c in Client.objects.order_by('pk')[:6]:
    print(f"  {c.last_name} {c.first_name} | {c.email} | {c.phone}")

print("\nDone!")
