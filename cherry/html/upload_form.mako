<html>
<head />
<body>
<h2>Upload a file</h2>
<form action="upload" method="post" enctype="multipart/form-data">
    <div>Network name: <input type="text" name="network_name" value="testDeleteme"></input></div>
    <div>Network file: <input type="file" name="network_file" /></div>
    <div>Annotations file: <input type="file" name="annotations_file" /></div>
    <div><input type="radio" name="type" value="public" checked="checked">Public</div>
    <div><input type="radio" name="type" value="private">Private</div>
    <div>email: <input type="text" name="email" value="aytonm@gmail.com"></input></div>
	<div><input type="submit" /></div>
</form>
<table>
</table>
</body>
</html>
