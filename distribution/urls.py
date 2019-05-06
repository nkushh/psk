from django.urls import path

from . import views

app_name = 'distribution'

urlpatterns = [
	path('nets-distribution', views.distribution_index, name='nets_distribution'),
	path('monthly-distribution/<int:mwezi>/', views.monthly_net_delivery, name='monthly_distribution'),
	path('nets-issuance', views.record_nets_issued, name='issue_nets' ),
	path('monthly-issuance/<int:mwezi>/', views.monthly_issuance_index, name='monthly_issuance'),
	path('distribution-download-all', views.download_all_distribution_excel, name='all_distribution_download'),
	path('yearly-distribution-download/<int:mwaka>/', views.download_distribution_by_year, name='yearly_distribution_download'),
	path('distribution-download/<int:mwezi>/<int:mwaka>/', views.download_distribution_excel, name='distribution_download'),
	path('excel-nets-issuance', views.record_nets_issued_excel, name='issue_nets_excel' ),
	path('issuance-download/<int:mwezi>/<str:mwaka>/', views.download_issuance_excel, name='issuance_download'),
	path('excel-nets-donation', views.record_nets_donated_excel, name='donate_nets_excel' ),
	path('excel-nets-distribution', views.record_nets_distributed_excel, name='distribute_nets_excel' ),
	path('counties-nets-issuance', views.nets_distributed_by_county, name='counties_issued_nets' ),
	path('nets-to-facilities', views.nets_issued_to_facilities, name='nets_to_facilities' ),
	path('nets-donated', views.nets_donated, name='nets_donated' ),
	path('delivery-by-county/<str:county>/', views.delivery_by_county, name='delivery_by_county'),
	path('delivery-by-region/<str:region>/', views.delivery_by_region, name='delivery_by_region'),
	path('record-distribution', views.record_distribution, name="record_distribution"),
	path('nets-distributed', views.nets_distributed, name='nets_distributed'),
	path('warehouses', views.all_warehouses, name='warehouses'),
	path('new-warehouse', views.new_warehouse, name='new_warehouse'),
	path('stock-warehouse', views.stock_warehouse, name='stock_warehouse'),
	path('stocking-history', views.stockin_history, name='stocking_history'),
	path('delete-delivery/<int:delivery_pk>/', views.delete_delivery, name="delete_delivery"),
	path('delete-deliveries', views.delete_all_deliveries, name="delete_deliveries"),
	path('reset-balances', views.reset_nets_balance, name="reset_nets_balance"),
	path('quarter-report-download', views.download_qdistribution_excel, name="quarter_report_download"),
	path('issuance-index', views.issuance_index, name="issuance_index"),
	# Targets
	path('set-distribution-targets', views.create_target, name="create_target"),
	path('fetch-targets', views.fetch_targets, name="fetch_targets"),
]