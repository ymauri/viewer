from django.shortcuts import render
from django.http import *
from django.core import serializers
from django.db import connection
import json
# Modelos
from panel.models import Summary as sm
from panel.models import Result as rs
from panel.models import Labels as lb

def  index(request):
	return render(request, 'panel/index.html')

def main(request):
	return render(request, 'panel/main.html')
    #return HttpResponse("bienvenido a mi pagina en %s" % request.path) 

def configure(request):
	return render(request, 'panel/graph.html', {'parametro':request.POST['parametro'], 'algoritmo': request.POST['algoritmo']})	  

def load_summary(request):
	if (request.GET['parametro'] and request.GET['algoritmo']):
		despegue = sm.objects.filter(parametro=request.GET['parametro'], algoritmo=request.GET['algoritmo'], fase='despegue').values('row0', 'row1', 'row2', 'row3', 'row4', 'row5', 'row6', 'row7', 'row8', 'row9', 'row10', 'row11', 'row12', 'row13', 'row14', 'row15', 'row16', 'row17', 'row18', 'row19', 'row20', 'row21', 'row22', 'row23', 'row24', 'grupo', 'parametro')	
		aterrizaje = sm.objects.filter(parametro=request.GET['parametro'], algoritmo=request.GET['algoritmo'], fase='aterrizaje').values('row0', 'row1', 'row2', 'row3', 'row4', 'row5', 'row6', 'row7', 'row8', 'row9', 'row10', 'row11', 'row12', 'row13', 'row14', 'row15', 'row16', 'row17', 'row18', 'row19', 'row20', 'row21', 'row22', 'row23', 'row24', 'grupo', 'parametro')	
		return JsonResponse({'despegue': parse_data_summary(list(despegue)), 'aterrizaje':parse_data_summary(list(aterrizaje))})
	else:
		return JsonResponse({'despegue': [], 'aterrizaje':[]})	

def load_result(request):
	despegue = sm.objects.filter(parametro=request.GET['parametro'], algoritmo=request.GET['algoritmo'])	
	return JsonResponse(list(despegue), safe=False)

def parse_data_summary(data):
	order_index = ['row0', 'row1', 'row2', 'row3', 'row4', 'row5', 'row6', 'row7', 'row8', 'row9', 'row10', 'row11', 'row12', 'row13', 'row14', 'row15', 'row16', 'row17', 'row18', 'row19', 'row20', 'row21', 'row22', 'row23', 'row24', 'grupo']	
	list_result = []	
	
	for item in data:
		order_row = []
		grupo = ''
		i = 1
		for current in order_index:
			if current == 'grupo':
				grupo = item[current]
			else:
				order_row.append([i,item[current]])
				i = i + 1
		list_result.append({grupo:order_row})

	return list_result
 	
def asign_label(request):
	grupos = rs.objects.filter(parametro=request.GET['parametro'], algoritmo=request.GET['algoritmo'], fase= request.GET['fase']).values('cluster').distinct()

	for current in grupos:		
		current_clusters = rs.objects.filter(parametro=request.GET['parametro'], algoritmo=request.GET['algoritmo'], fase= request.GET['fase'], cluster=current['cluster'])
		for flight in current_clusters:		
			flight.etiqueta = request.GET[current['cluster']]
			flight.save()
	return JsonResponse({}, safe=False)

def cantidad_grupo(request):
	grupos = rs.objects.filter(parametro=request.GET['parametro'], algoritmo=request.GET['algoritmo'], fase= request.GET['fase']).values('cluster').distinct()
	listado = {}
	for current in grupos:
		valores = rs.objects.filter(parametro=request.GET['parametro'], algoritmo=request.GET['algoritmo'], fase= request.GET['fase'], cluster=current['cluster'])
		listado[current['cluster']] = len(valores)
	return JsonResponse(listado, safe=False)

def load_resumen(request):
	pass

def resumen(request):
	"""FILTRAR POR EL ALGORITMO"""
	#if request.GET['algoritmo']:
	#	algoritmo = request.GET['algoritmo']
	#else:
	algoritmo = 'K-means'
	parametros = ['VRTG', 'AOAC', 'FLAP', 'PTCH', 'ROLL']
	vuelos = rs.objects.filter(algoritmo=algoritmo, fase='despegue').values('flight','id').distinct()
	etiquetas_despegue = []
	for vuelo in vuelos:
		listado = {'flight':vuelo['flight'],'VRTG':'-', 'AOAC':'-', 'FLAP':'-', 'PTCH':'-', 'ROLL':'-'}
		
		"""for parametro in parametros:			
			try:
				etiqueta = rs.objects.get(algoritmo=algoritmo, fase='despegue', flight=vuelo['flight'], parametro=parametro)
			except etiqueta.DoesNotExist, e:
				print str(vuelo['id']) +'  ---  '+ str(e)
			else:
				listado[parametro] =  etiqueta.etiqueta
			finally:
				pass"""
			
			#if hasattr(etiqueta, 'etiqueta'):
			#	print str(vuelo['id'])+' -- '+ etiqueta.etiqueta
				
		etiquetas_despegue.append(listado)
	return render(request, 'panel/resumen.html', {'despegue':list(etiquetas_despegue)})	  

def detalle_vuelo(request, flight):
	return render(request, 'panel/detalle_vuelo.html', {'vuelo':flight, 'algoritmo':''})

def load_detalle_vuelo(request):
	parametros = ['VRTG', 'AOAC', 'FLAP', 'PTCH', 'ROLL']
	listado = {'despegue':{'VRTG':[], 'AOAC':[], 'FLAP':[], 'PTCH':[], 'ROLL':[]}, 'aterrizaje':{'VRTG':[], 'AOAC':[], 'FLAP':[], 'PTCH':[], 'ROLL':[]}}
	for parametro in parametros:
		query_objetc = rs.objects.filter(flight=request.GET['vuelo'], parametro=parametro, fase='despegue').values('row0', 'row1', 'row2', 'row3', 'row4', 'row5', 'row6', 'row7', 'row8', 'row9', 'row10', 'row11', 'row12', 'row13', 'row14', 'row15', 'row16', 'row17', 'row18', 'row19', 'row20', 'row21', 'row22', 'row23', 'row24', 'parametro').distinct()
		listado['despegue'][parametro] = parse_data_detalle(list(query_objetc), request.GET['vuelo'])
		query_objetc = rs.objects.filter(flight=request.GET['vuelo'], parametro=parametro, fase='aterrizaje').values('row0', 'row1', 'row2', 'row3', 'row4', 'row5', 'row6', 'row7', 'row8', 'row9', 'row10', 'row11', 'row12', 'row13', 'row14', 'row15', 'row16', 'row17', 'row18', 'row19', 'row20', 'row21', 'row22', 'row23', 'row24', 'parametro').distinct()
		listado['aterrizaje'][parametro] = parse_data_detalle(list(query_objetc), request.GET['vuelo'])
	return JsonResponse({'listado': listado})

def parse_data_detalle(data, vuelo):
	order_index = ['row0', 'row1', 'row2', 'row3', 'row4', 'row5', 'row6', 'row7', 'row8', 'row9', 'row10', 'row11', 'row12', 'row13', 'row14', 'row15', 'row16', 'row17', 'row18', 'row19', 'row20', 'row21', 'row22', 'row23', 'row24', 'parametro']	
	list_result = []	
	
	for item in data:
		order_row = []
		parametro = ''
		i = 1
		for current in order_index:
			if current == 'parametro':
				parametro = item[current]
			else:
				order_row.append([i,item[current]])
				i = i + 1
		list_result.append({vuelo:order_row})

	return list_result
 	