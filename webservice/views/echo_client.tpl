<script type="text/javascript">
	var ws = new WebSocket("ws://localhost:8079/echo");

	ws.onopen = function (event){
		// THIS IS THE BEST PROGRAMMING JOKE EVER
		ws.send("Hello from the other side!");
	};

	ws.onmessage = function (event){
		console.log(event.data);
	};


</script>
