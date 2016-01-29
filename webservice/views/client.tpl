<script type="text/javascript">
	var ws = new WebSocket("ws://localhost:8079/{{url}}");

	ws.onopen = function (event){
		console.log("WebSocket connection enstabilished");
	};

	ws.onmessage = function (event){
		console.log(event.data);
	};


</script>
