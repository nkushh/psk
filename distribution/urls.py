from django.urls import path

from . import views

app_name = 'distribution'

urlpatterns = [
	path('nets-distribution', views.distribution_index, name='nets_distribution'),
	path('nets-issuance', views.record_nets_issued, name='issue_nets' ),
	path('excel-nets-issuance', views.record_nets_issued_excel, name='issue_nets_excel' ),
	path('excel-nets-distribution', views.record_nets_distributed_excel, name='distribute_nets_excel' ),
	path('counties-nets-issuance', views.nets_distributed_by_county, name='counties_issued_nets' ),
	path('nets-to-facilities', views.nets_issued_to_facilities, name='nets_to_facilities' ),
	path('record-distribution', views.record_distribution, name="record_distribution"),
	path('nets-distributed', views.nets_distributed, name='nets_distributed'),
	path('warehouses', views.all_warehouses, name='warehouses'),
	path('new-warehouse', views.new_warehouse, name='new_warehouse'),
	path('stock-warehouse', views.stock_warehouse, name='stock_warehouse'),
	path('stocking-history', views.stockin_history, name='stocking_history'),
	path('delete-delivery/<int:delivery_pk>/', views.delete_delivery, name="delete_delivery"),
	path('delete-deliveries', views.delete_all_deliveries, name="delete_deliveries"),
	path('reset-balances', views.reset_nets_balance, name="reset_nets_balance"),
]