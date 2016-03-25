var areaChartData = [
{label:'RequestJobs', values:[]},
{label:'DoneJobs', values:[]},
{label:'FailedJobs', values:[]},
{label:'RefusedJobs', values:[]}
];

$(document).ready(function(){

	var $time = $('#time');
	var chart = $('#areaChart').epoch({
    type: 'time.area',
    data: areaChartData
  	});

	function ajaxCall(){
		$.ajax({
	    	url: 'http://localhost:8088/data',
	    	dataType:'json',
		    success: function( response ) {
		        		$time.html('time: ' + response.time);
		        		chart.push([
		        			{x:response.time, y:response.jobRequests},
		        			{x:response.time, y:response.doneJobs},
		        			{x:response.time, y:response.failedJobs},
		        			{x:response.time, y:response.refusedJobs}
		        			 ]);
			    		}
			});
	}

	var to = setInterval(ajaxCall, 1000);

});




