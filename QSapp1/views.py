from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.db.models import F
from .models import Service, Ticket, Counter, SystemSettings, DisplayAd

# --- 1. واجهة الكشك (Kiosk): للعملاء لقطع التذاكر ---

def kiosk_view(request):
    services = Service.objects.all()
    counters = Counter.objects.all()
    settings = SystemSettings.objects.first()
    total_waiting = Ticket.objects.filter(status='waiting').count()
    total_served = Ticket.objects.filter(status='completed').count()
    
    return render(request, 'kiosk.html', {
        'services': services,
        'settings': settings,
        'total_waiting': total_waiting,
        'total_served': total_served,
        'counters': counters
    })

def issue_ticket(request, service_id, counter_id):
    # 1. جلب الخدمة واليوم الحالي
    service = get_object_or_404(Service, id=service_id)
    counter = get_object_or_404(Counter, id=counter_id)
    today = timezone.now().date()
    settings = SystemSettings.objects.first()
    
    
    # 2. حساب الرقم التالي (تصفير يومي تلقائي)
    last_ticket = Ticket.objects.filter(
        service=service, 
        created_at__date=today
    ).order_by('-number').first()
    
    new_number = (last_ticket.number + 1) if last_ticket else 1
    
    # 3. إنشاء التذكرة وحفظها
    ticket = Ticket.objects.create(
        service=service,
        number=new_number,
        status='waiting',
        counter=counter,
    )
    
    # 4. عرض صفحة التذكرة للطباعة
    return render(request, 'ticket.html', {
        'ticket': ticket, 
        'settings': settings,
        'counter_id': counter_id
    })


# --- 2. واجهة الشاشة الكبيرة (Main Display): لعرض الأرقام الحالية ---

def main_display(request):
    # جلب آخر 5 تذاكر تم النداء عليها حالياً
    calling_tickets = Ticket.objects.filter(status='calling').order_by('-called_at')[:5]
    # جلب الإعلانات النشطة
    ads = DisplayAd.objects.filter(is_active=True).order_by('order')
    settings = SystemSettings.objects.first()
    
    return render(request, 'display.html', {
        'calling_tickets': calling_tickets,
        'ads': ads,
        'settings': settings
    })


# --- 3. واجهة الموظف (Staff Dashboard): للتحكم بالدور ---

def staff_dashboard(request, counter_id):
    counter = get_object_or_404(Counter, id=counter_id)
    
    # 1. التذكرة الحالية التي يخدمها هذا الشباك (التي يتم النداء عليها أو خدمتها الآن)
    current_ticket = Ticket.objects.filter(counter=counter, status__in=['calling', 'serving']).first()
    
    # 2. قائمة الانتظار المفلترة:
    # يجب أن تكون الخدمة ضمن خدمات الشباك المسموحة (service__in)
    # ويجب أن يكون الشباك المرتبط بالتذكرة هو هذا الشباك (counter=counter)
    waiting_tickets = Ticket.objects.filter(
        service__in=counter.services.all(), # من نفس الخدمة
        counter=counter,                    # ومن نفس الشباك
        status='waiting'
    ).order_by('created_at')

    settings = SystemSettings.objects.first()

    return render(request, 'counter.html', {
        'counter': counter,
        'current_ticket': current_ticket,
        'waiting_tickets': waiting_tickets,
        'waiting_count': waiting_tickets.count(),
        'settings': settings,
    })

def call_next(request, counter_id):
    counter = get_object_or_404(Counter, id=counter_id)
    
    # 1. إنهاء التذكرة السابقة إن وجدت لهذا الشباك
    Ticket.objects.filter(counter=counter, status__in=['calling', 'serving']).update(
        status='completed', 
        finished_at=timezone.now()
    )
    
    # 2. البحث عن التذكرة التالية
    next_ticket = Ticket.objects.filter(
        service__in=counter.services.all(),
        status='waiting'
    ).order_by('created_at').first()
    
    if next_ticket:
        next_ticket.status = 'calling'
        next_ticket.counter = counter
        next_ticket.called_at = timezone.now()
        next_ticket.save()
        messages.success(request, f"تم النداء على التذكرة {next_ticket.ticket_code}")
    else:
        messages.warning(request, "لا يوجد عملاء في الانتظار حالياً")
        
    return redirect('staff_dashboard', counter_id=counter.id)

def skip_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    counter_id = ticket.counter.id if ticket.counter else request.GET.get('counter_id')
    
    ticket.status = 'skipped'
    ticket.finished_at = timezone.now()
    ticket.save()
    
    return redirect('staff_dashboard', counter_id=counter_id)

def recall_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    ticket.called_at = timezone.now()  # تحديث الوقت ليظهر كأحدث نداء
    ticket.save()
    messages.info(request, f"تم إعادة النداء على {ticket.ticket_code}")
    return redirect('staff_dashboard', counter_id=ticket.counter.id)

def start_serving(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    ticket.status = 'serving'
    ticket.started_at = timezone.now()
    ticket.save()
    return redirect('staff_dashboard', counter_id=ticket.counter.id)

def complete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    ticket.status = 'completed'
    ticket.finished_at = timezone.now()
    ticket.save()
    return redirect('staff_dashboard', counter_id=ticket.counter.id)

def hold_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    # جلب رقم الشباك من التذكرة أو من الرابط
    counter_id = ticket.counter.id if ticket.counter else request.GET.get('counter_id')
    
    ticket.status = 'waiting'
    ticket.counter = None
    ticket.save()
    return redirect('staff_dashboard', counter_id=counter_id)

def call_specific_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    counter_id = request.GET.get('counter_id')
    counter = get_object_or_404(Counter, id=counter_id)
    
    # إنهاء أي تذكرة نشطة لهذا الشباك أولاً
    Ticket.objects.filter(counter=counter, status__in=['calling', 'serving']).update(
        status='completed', finished_at=timezone.now()
    )
    
    ticket.status = 'calling'
    ticket.counter = counter
    ticket.called_at = timezone.now()
    ticket.save()
    return redirect('staff_dashboard', counter_id=counter.id)

def remove_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    # نحدد الشباك قبل الحذف لإعادة التوجيه
    counter_id = ticket.counter.id if ticket.counter else request.GET.get('counter_id')
    ticket.delete()
    return redirect('staff_dashboard', counter_id=counter_id)

def return_to_queue(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    counter_id = ticket.counter.id if ticket.counter else request.GET.get('counter_id')
    
    ticket.status = 'waiting'
    ticket.counter = None
    ticket.called_at = None 
    ticket.save()
    
    return redirect('staff_dashboard', counter_id=counter_id)

