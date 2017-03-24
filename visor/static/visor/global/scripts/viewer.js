

$('#main-viewer').ready(function(){
	if ($('input#parametro').val() != '' && $('input#algoritmo').val()){
		$.ajax({
		  url : '/panel/load_summary/',
		  type: "GET",
		  data : {parametro: $('input#parametro').val(), algoritmo: $('input#algoritmo').val()}
		}).done(function(data) {
		  	$('#slc-parametro').val($('input#parametro').val())  
		  	$('#slc-algoritmo').val($('input#algoritmo').val()) 
		  	
		  	graficar_summary(data.despegue, $('input#parametro').val(), 'graph_despegue')
		  	graficar_summary(data.aterrizaje, $('input#parametro').val(), 'graph_aterrizaje')
		    
		    Charts.init();
		    cantidad_grupo('despegue')
		    cantidad_grupo('aterrizaje')
		  })
		  .fail(function(data) {
		    //alert( "error" );
		  })
		  .always(function(data) {
		    //alert( "complete" );

		  });
	}	
})

function graficar_summary (datos, parametro, container){
	var result = []
	var i = 0;
	for (var current in datos) {		
		for (var index in datos[current]) {
			result[i] = {
		    	data: datos[current][index],
		        label: index,
		        lines: {
		            lineWidth: 1,
		        },
		        shadowSize: 0
		    }
		    break
		}
		i++
	}	

	var plot = $.plot($("#"+container), 
		result,
		{
        series: {
            lines: {
                show: true,
                lineWidth: 2,
                fill: true,
                fillColor: {
                    colors: [{
                            opacity: 0.05
                        }, {
                            opacity: 0.01
                        }
                    ]
                }
            },
            points: {
                show: true,
                radius: 3,
                lineWidth: 1
            },
            shadowSize: 2
        },
        grid: {
            hoverable: true,
            clickable: true,
            tickColor: "#eee",
            borderColor: "#eee",
            borderWidth: 1
        },
        colors: ["#d12610", "#37b7f3", "#52e136", "#DC9720", "#aab7f3", "#5ee136"],
        xaxis: {
            ticks: 25,
            tickDecimals: 0,
            tickColor: "#eee",
        },
        yaxis: {
            ticks: 30,
            tickDecimals: 2,
            tickColor: "#eee",
        }
	});
	function showTooltip(x, y, contents) {
        $('<div id="tooltip">' + contents + '</div>').css({
            position: 'absolute',
            display: 'none',
            top: y + 5,
            left: x + 15,
            border: '1px solid #333',
            padding: '4px',
            color: '#fff',
            'border-radius': '3px',
            'background-color': '#333',
            opacity: 0.80
        }).appendTo("body").fadeIn(200);
    }

    var previousPoint = null;
    $("#"+container).bind("plothover", function (event, pos, item) {
        $("#x").text(pos.x.toFixed(2));
        $("#y").text(pos.y.toFixed(2));

        if (item) {
            if (previousPoint != item.dataIndex) {
                previousPoint = item.dataIndex;

                $("#tooltip").remove();
                var x = item.datapoint[0].toFixed(2),
                    y = item.datapoint[1].toFixed(2);

                showTooltip(item.pageX, item.pageY, item.series.label + " of " + x + " = " + y);
            }
        } else {
            $("#tooltip").remove();
            previousPoint = null;
        }
    });
	
}
$('#link_label_despegue').click(function(){
	$('#fase').val('despegue')	
	$('#cant_0').text($('#cant_0_despegue').text())
	$('#cant_1').text($('#cant_1_despegue').text())
	$('#cant_2').text($('#cant_2_despegue').text())
})

$('#link_label_aterrizaje').click(function(){
	$('#fase').val('aterrizaje')
	$('#cant_0').text($('#cant_0_aterrizaje').text())
	$('#cant_1').text($('#cant_1_aterrizaje').text())
	$('#cant_2').text($('#cant_2_aterrizaje').text())
	
})

$('#btn_asign_labels_despegue').click(function(){
	$.ajax({
	  url : '/panel/asign_label/',
	  type: "GET",
	  data : $('#form-labels_despegue').serialize()
	})
	  .done(function(data) {
	  	//$('#main-viewer').html(data.despegue[0]['Cluster0'].toSource())	  	
	  	alert('Etiquetas actualizadas correctamente');
	  })
	  .fail(function(data) {
	    //alert( "error" );
	  })
	  .always(function(data) {
	    //alert( "complete" );

	  });
})

$('#btn_asign_labels_aterrizaje').click(function(){
	$.ajax({
	  url : '/panel/asign_label/',
	  type: "GET",
	  data : $('#form-labels_aterrizaje').serialize()
	})
	  .done(function(data) {
	  	//$('#main-viewer').html(data.despegue[0]['Cluster0'].toSource())	  	
	  	alert('Etiquetas actualizadas correctamente');
	  })
	  .fail(function(data) {
	    //alert( "error" );
	  })
	  .always(function(data) {
	    //alert( "complete" );

	  });
})

function cantidad_grupo (current_fase){
	$.ajax({
	  url : '/panel/cantidad_grupo/',
	  type: "GET",
	  data : {parametro: $('input#parametro').val(), algoritmo: $('input#algoritmo').val(), fase: current_fase}
	})
	  .done(function(data) {	
	  	var fase = ''
	  	var etiquetar = ''
	  	$('#form-labels .form-group').remove(); 

	  	for(var current in data){
	  		fase += '<div class="col-md-2"> <span class="help-block">'+current+': <b>'+data[current]+'</b> vuelos. </span> </div>'
	  		etiquetar += '<div class="form-group"><label class="col-md-2">'+current+'</label><select id="'+current+'" name="'+current+'" class="form-control input-small col-md-4"><option value="">...</option><option value="Anómalo">Anómalo</option><option value="Eventual">Eventual</option><option value="Normal">Normal</option></select><span class="help-block col-md-5"> Contiene <b>'+data[current]+'</b> vuelos. </span></div>'
	  	}
	  	$('#legend-'+current_fase).html(fase) 	
	  	$('#form-labels_'+current_fase).append(etiquetar)

	  	
	  })
	  .fail(function(data) {
	    //alert( "error" );
	  })
	  .always(function(data) {
	    //alert( "complete" );

	  });
}

/*$('#slc-algoritmo').on('change', function(){
	$('.link_flight').each(function(){
		var current = $(this).attr('href') + $('#slc-algoritmo').val()
		$(this).attr('href', current + '/')
	})
	
})*/

$('#detalle_vuelo').ready(function(){
	if ($('input#vuelo').val() != ''){
		$.ajax({
			  url : '/panel/load_detalle_vuelo/',
			  type: "GET",
			  data : {vuelo: $('input#vuelo').val()}
			}).done(function(data) {
			  	graficar_summary(data.listado.despegue.VRTG, '', 'graph_VRTG_despegue')
			  	graficar_summary(data.listado.despegue.AOAC, '', 'graph_AOAC_despegue')
			  	graficar_summary(data.listado.despegue.PTCH, '', 'graph_PTCH_despegue')
			  	graficar_summary(data.listado.despegue.FLAP, '', 'graph_FLAP_despegue')
			  	graficar_summary(data.listado.despegue.ROLL, '', 'graph_ROLL_despegue')

			  	graficar_summary(data.listado.aterrizaje.VRTG, '', 'graph_VRTG_aterrizaje')
			  	graficar_summary(data.listado.aterrizaje.AOAC, '', 'graph_AOAC_aterrizaje')
			  	graficar_summary(data.listado.aterrizaje.PTCH, '', 'graph_PTCH_aterrizaje')
			  	graficar_summary(data.listado.aterrizaje.FLAP, '', 'graph_FLAP_aterrizaje')
			  	graficar_summary(data.listado.aterrizaje.ROLL, '', 'graph_ROLL_aterrizaje')
			  	//graficar_summary(data.despegue, $('input#parametro').val(), 'graph_despegue')
			  	//graficar_summary(data.aterrizaje, $('input#parametro').val(), 'graph_aterrizaje')
			    
			    Charts.init();
			    //cantidad_grupo('despegue')
			    //cantidad_grupo('aterrizaje')
			  })
			  .fail(function(data) {
			    //alert( "error" );
			  })
			  .always(function(data) {
			    //alert( "complete" );

		  });
		}
	
})