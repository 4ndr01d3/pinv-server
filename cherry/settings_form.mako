<html>
<body>

<form name="comment_form" controller="comment" action="save_settings">
<table>
    <tr>
        <th colspan="2">Submit your JSON</th>
    </tr>
    <tr>
	<td>
	<textarea rows="20" cols="120" name="json_settings">
{
"employees": [
		{ "firstName":"John" , "lastName":"Doe" }, 
		{ "firstName":"Anna" , "lastName":"Smith" }, 
		{ "firstName":"Peter" , "lastName":"Jones" }
	]
} 
	</textarea>
</td>
    </tr>

<tr>
<td>
<input type="submit" value="Submit">
</td>
</tr>
</table>
</form>

</body>
</html>
