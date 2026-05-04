import json
from datetime import date, datetime, timedelta
from django.views.generic import TemplateView, View
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from apps.staff.models import Master
from apps.services.models import Service
from apps.clients.models import Client
from apps.appointments.models import Appointment, AppointmentStatus


class BookingPageView(TemplateView):
    template_name = 'booking/book.html'


class MastersAPIView(View):
    def get(self, request):
        masters = (
            Master.objects.filter(is_active=True)
            .prefetch_related('specializations', 'services')
            .order_by('calendar_order', 'display_name')
        )
        data = []
        for m in masters:
            specs = [s.name for s in m.specializations.all()]
            photo_url = m.photo.url if m.photo else None
            data.append({
                'id':    m.pk,
                'name':  m.display_name,
                'bio':   m.bio,
                'photo': photo_url,
                'color': m.color,
                'rating': float(m.rating),
                'specs': specs,
            })
        return JsonResponse({'masters': data})


class ServicesAPIView(View):
    def get(self, request, master_id):
        try:
            master = Master.objects.get(pk=master_id, is_active=True)
        except Master.DoesNotExist:
            return JsonResponse({'error': 'Мастер не найден'}, status=404)

        services = master.services.filter(is_active=True).select_related('category').order_by(
            'category__order', 'order', 'name'
        )
        data = []
        for s in services:
            data.append({
                'id':          s.pk,
                'name':        s.name,
                'description': s.description,
                'duration':    s.duration,
                'duration_display': s.duration_display,
                'price':       float(s.price),
                'category':    s.category.name,
            })
        return JsonResponse({'services': data})


class SlotsAPIView(View):
    def get(self, request, master_id):
        date_str = request.GET.get('date', '')
        service_id = request.GET.get('service_id', '')

        try:
            slot_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Неверный формат даты'}, status=400)

        if slot_date < date.today():
            return JsonResponse({'slots': []})

        try:
            master = Master.objects.get(pk=master_id, is_active=True)
        except Master.DoesNotExist:
            return JsonResponse({'error': 'Мастер не найден'}, status=404)

        try:
            service = Service.objects.get(pk=service_id, is_active=True)
        except Service.DoesNotExist:
            return JsonResponse({'error': 'Услуга не найдена'}, status=404)

        # Check work schedule for this weekday
        weekday = slot_date.weekday()  # 0=Mon … 6=Sun
        schedule = master.schedules.filter(weekday=weekday, is_day_off=False).first()
        if not schedule:
            return JsonResponse({'slots': []})

        # Check day off
        if master.days_off.filter(date=slot_date).exists():
            return JsonResponse({'slots': []})

        # Generate slots
        duration = timedelta(minutes=service.duration)
        step     = timedelta(minutes=30)  # slots every 30 min
        current  = datetime.combine(slot_date, schedule.start_time)
        end_work = datetime.combine(slot_date, schedule.end_time)

        # Fetch existing appointments for that day
        existing = list(
            Appointment.objects.filter(
                master=master,
                start_time__date=slot_date,
            ).exclude(status__in=[AppointmentStatus.CANCELLED, AppointmentStatus.NO_SHOW])
            .values_list('start_time', 'end_time')
        )

        now = datetime.now()
        slots = []
        while current + duration <= end_work:
            slot_end = current + duration
            # Skip slots in the past (today only)
            if slot_date == date.today() and current <= now:
                current += step
                continue
            # Check for overlap with existing appointments
            overlap = False
            for appt_start, appt_end in existing:
                # Strip timezone awareness for comparison
                a_start = appt_start.replace(tzinfo=None) if appt_start.tzinfo else appt_start
                a_end   = appt_end.replace(tzinfo=None) if appt_end and appt_end.tzinfo else appt_end
                if a_end is None:
                    a_end = a_start + timedelta(minutes=30)
                if current < a_end and slot_end > a_start:
                    overlap = True
                    break
            if not overlap:
                slots.append(current.strftime('%H:%M'))
            current += step

        return JsonResponse({'slots': slots})


@method_decorator(csrf_exempt, name='dispatch')
class BookingSubmitView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, ValueError):
            return JsonResponse({'error': 'Неверный формат данных'}, status=400)

        # Validate required fields
        required = ['master_id', 'service_id', 'date', 'time', 'first_name', 'last_name', 'phone']
        for field in required:
            if not data.get(field):
                return JsonResponse({'error': f'Поле {field} обязательно'}, status=400)

        try:
            master = Master.objects.get(pk=data['master_id'], is_active=True)
        except Master.DoesNotExist:
            return JsonResponse({'error': 'Мастер не найден'}, status=404)

        try:
            service = Service.objects.get(pk=data['service_id'], is_active=True)
        except Service.DoesNotExist:
            return JsonResponse({'error': 'Услуга не найдена'}, status=404)

        try:
            slot_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            slot_time = datetime.strptime(data['time'], '%H:%M').time()
        except ValueError:
            return JsonResponse({'error': 'Неверный формат даты или времени'}, status=400)

        if slot_date < date.today():
            return JsonResponse({'error': 'Дата не может быть в прошлом'}, status=400)

        start_dt = datetime.combine(slot_date, slot_time)

        # Find or create client by phone
        phone = data['phone'].strip()
        client, _ = Client.objects.get_or_create(
            phone=phone,
            defaults={
                'first_name': data['first_name'].strip(),
                'last_name':  data['last_name'].strip(),
            }
        )

        # Create appointment
        appt = Appointment.objects.create(
            client=client,
            master=master,
            service=service,
            start_time=start_dt,
            status=AppointmentStatus.PENDING,
            notes=data.get('notes', ''),
        )

        return JsonResponse({
            'success': True,
            'appointment_id': appt.pk,
            'master':  master.display_name,
            'service': service.name,
            'date':    slot_date.strftime('%d.%m.%Y'),
            'time':    slot_time.strftime('%H:%M'),
            'price':   float(service.price),
            'client':  f"{data['last_name']} {data['first_name']}",
        })
