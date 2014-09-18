<html>
<head />
<body>
<h2>Upload a file</h2>

<form action="upload" method="post" enctype="multipart/form-data">
    <div>Network name: <input type="text" name="network_name" value="mynetwork"></input></div>
    <div>Annotations file: <input type="file" name="annotations_file" /></div>
    <div>Network file: <input type="file" name="network_file" /></div>
	<div><input type="submit" /></div>
</form>

${message}

<table>
</table>
</body>
</html>
