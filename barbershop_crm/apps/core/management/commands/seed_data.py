import random
from datetime import timedelta, time
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from faker import Faker

fake = Faker("ru_RU")

CATEGORY_DATA = [
    ("Haircuts", "bi-scissors", [("Classic cut",30,800),("Machine cut",20,600),("Kids cut",25,500),("Cut+style",45,1200)]),
    ("Beard", "bi-brush", [("Beard trim",20,600),("Straight razor",30,900),("Mustache trim",15,400)]),
    ("Combos", "bi-stars", [("Cut+Beard",50,1400),("Royal shave",60,1800)]),
]
MASTER_DATA = [
    ("Aleksej", "Gromov", "#c9a84c"),("Dmitrij","Sokolov","#5b9bd5"),
    ("Ivan","Petrov","#70ad47"),("Sergej","Volkov","#e07b54"),
]

class Command(BaseCommand):
    help = "Seed database"
    def add_arguments(self, parser):
        parser.add_argument("--appointments", type=int, default=150)
        parser.add_argument("--clear", action="store_true")
    def handle(self, *args, **options):
        if options["clear"]: self.clear_data()
        services = self.create_services()
        masters = self.create_masters(services)
        clients = self.create_clients(masters)
        self.create_appointments(clients, masters, services, options["appointments"])
        self.stdout.write(self.style.SUCCESS("Seed done!"))
    def clear_data(self):
        from apps.billing.models import Payment
        from apps.appointments.models import Appointment
        from apps.clients.models import Client
        from apps.services.models import Service, ServiceCategory
        from apps.staff.models import Master, WorkSchedule
        Payment.objects.all().delete(); Appointment.objects.all().delete()
        Client.objects.all().delete(); Master.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        Service.objects.all().delete(); ServiceCategory.objects.all().delete()
    def create_services(self):
        from apps.services.models import ServiceCategory, Service
        svcs = []
        for cat_name, icon, items in CATEGORY_DATA:
            cat, _ = ServiceCategory.objects.get_or_create(name=cat_name, defaults={"icon": icon})
            for name, dur, price in items:
                s, _ = Service.objects.get_or_create(name=name, defaults={"category": cat, "duration": dur, "price": price})
                svcs.append(s)
        return svcs
    def create_masters(self, services):
        from apps.staff.models import Master, WorkSchedule
        masters = []
        for i, (first, last, color) in enumerate(MASTER_DATA):
            uname = f"master_{i+1}"
            user, _ = User.objects.get_or_create(username=uname, defaults={"first_name": first, "last_name": last})
            user.set_password("master123"); user.save()
            m, _ = Master.objects.get_or_create(user=user, defaults={"display_name": f"{first} {last}","phone": fake.phone_number()[:20],"color": color,"rating": Decimal(str(round(random.uniform(4.2,5.0),2))),"calendar_order": i})
            m.services.set(services)
            for wd in range(6): WorkSchedule.objects.get_or_create(master=m, weekday=wd, defaults={"start_time": time(9,0), "end_time": time(21,0)})
            masters.append(m)
        return masters
    def create_clients(self, masters):
        from apps.clients.models import Client
        clients = []; used = set()
        for _ in range(50):
            p = fake.numerify("+7-9##-###-##-##")
            while p in used: p = fake.numerify("+7-9##-###-##-##")
            used.add(p)
            c, _ = Client.objects.get_or_create(phone=p, defaults={"first_name": fake.first_name_male(),"last_name": fake.last_name_male(),"email": fake.email(),"preferred_master": random.choice(masters) if random.random()>0.5 else None})
            clients.append(c)
        return clients
    def create_appointments(self, clients, masters, services, count):
        from apps.appointments.models import Appointment, AppointmentStatus
        from apps.billing.models import Payment, PaymentMethod
        from django.db.models import Sum, Count
        now = timezone.now()
        for _ in range(count):
            c=random.choice(clients); m=random.choice(masters); s=random.choice(services)
            d=random.randint(-30,7); h=random.randint(9,19); mn=random.choice([0,30])
            start=now.replace(hour=h,minute=mn,second=0,microsecond=0)+timedelta(days=d)
            end=start+timedelta(minutes=s.duration)
            if d<0: st=random.choice([AppointmentStatus.DONE]*3+[AppointmentStatus.CANCELLED,AppointmentStatus.NO_SHOW])
            elif d==0: st=random.choice([AppointmentStatus.CONFIRMED,AppointmentStatus.IN_PROGRESS,AppointmentStatus.DONE])
            else: st=random.choice([AppointmentStatus.PENDING,AppointmentStatus.CONFIRMED])
            appt=Appointment.objects.create(client=c,master=m,service=s,start_time=start,end_time=end,status=st,price_paid=s.price if st==AppointmentStatus.DONE else None)
            if st==AppointmentStatus.DONE:
                disc=random.choice([0,0,0,10,15])
                Payment.objects.create(appointment=appt,amount=s.price,method=random.choice(list(PaymentMethod.values)),discount=disc)
        from apps.billing.models import Payment as P
        for cl in clients:
            agg=P.objects.filter(appointment__client=cl).aggregate(total=Sum("amount"),visits=Count("id"))
            cl.total_spent=agg["total"] or 0; cl.visit_count=agg["visits"] or 0
            cl.save(update_fields=["total_spent","visit_count"]); cl.recalculate_tier()