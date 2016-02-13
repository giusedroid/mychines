<script type="text/javascript">
	var ws = new WebSocket("ws://localhost:{{port}}/{{url}}");

	ws.onopen = function (event){
		console.log("WebSocket connection enstabilished");
	};

	ws.onmessage = function (event){
		console.log(event.data);
	};

	window.onbeforeunload = function() {
    	ws.onclose = function () {}; 
    	ws.close();
	};


</script>
