from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Count, Case, When, F, FloatField
from django.db import transaction
from .models import Production, Shipment, Inventory
from .forms import ProductionForm, ShipmentForm

def index(request):
    """
    ダッシュボード画面を表示
    """
    # 在庫状況
    inventory = Inventory.objects.select_related('production').all()
    
    # 生産サマリー
    production_summary = Production.objects.values('tea_type').annotate(
        total_productions=Count('id'),
        total_quantity=Sum('quantity'),
        a_grade_count=Sum(Case(
            When(quality_check='A級', then=1),
            default=0,
            output_field=FloatField(),
        )),
    ).annotate(
        quality_a_percentage=F('a_grade_count') * 100.0 / F('total_productions')
    )
    
    context = {
        'inventory': inventory,
        'production_summary': production_summary,
    }
    return render(request, 'tea_production/index.html', context)

@transaction.atomic
def production_create(request):
    """
    生産データの登録
    """
    if request.method == 'POST':
        form = ProductionForm(request.POST)
        if form.is_valid():
            production = form.save()
            
            # 在庫データも同時に作成
            Inventory.objects.create(
                production=production,
                quantity=production.quantity
            )
            
            messages.success(request, '生産データを登録しました。')
            return redirect('production_list')
    else:
        form = ProductionForm()
    
    return render(request, 'tea_production/production_form.html', {'form': form})

def production_list(request):
    """
    生産データ一覧の表示
    """
    productions = Production.objects.all()
    return render(request, 'tea_production/production_list.html', {
        'productions': productions
    })

@transaction.atomic
def shipment_create(request):
    """
    出荷データの登録
    """
    if request.method == 'POST':
        form = ShipmentForm(request.POST)
        if form.is_valid():
            shipment = form.save(commit=False)
            inventory = get_object_or_404(
                Inventory,
                production=shipment.production
            )
            
            # 在庫チェック
            if inventory.quantity < shipment.quantity:
                messages.error(request, '在庫が不足しています。')
                return render(request, 'tea_production/shipment_form.html', {'form': form})
            
            # 在庫を更新
            inventory.quantity -= shipment.quantity
            inventory.save()
            
            shipment.save()
            messages.success(request, '出荷データを登録しました。')
            return redirect('shipment_list')
    else:
        form = ShipmentForm()
    
    return render(request, 'tea_production/shipment_form.html', {'form': form})

def shipment_list(request):
    """
    出荷データ一覧の表示
    """
    shipments = Shipment.objects.select_related('production').all()
    return render(request, 'tea_production/shipment_list.html', {
        'shipments': shipments
    })

def inventory_list(request):
    """
    在庫一覧の表示
    """
    inventory = Inventory.objects.select_related('production').all()
    return render(request, 'tea_production/inventory_list.html', {
        'inventory': inventory
    }) 