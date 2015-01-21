/**
url params:
a_auth - authentication for control/snapshot in web format 'usr:pass'
s_auth - authentication for view/suppressed ^
host = host and port of octotoron, without protocol 'ip:port' or 'hostname:port'
*/

var urlParams; // http://stackoverflow.com/a/2880929
var rawParams;

(window.onpopstate = function () {
	var match,
		pl     = /\+/g,  // Regex for replacing addition symbol with a space
		search = /([^&=]+)=?([^&]*)/g,
		decode = function (s) { return decodeURIComponent(s.replace(pl, " ")); },
		query  = window.location.search.substring(1);

	urlParams = {};
	while (match = search.exec(query))
	   urlParams[decode(match[1])] = decode(match[2]);
	
	rawParams = query;
})();

$(document).ready(function() {
	if(!("host" in urlParams))
		$("#msg").html("<p>Error: host is not specified</p>");

	document.getElementById('link_active').href += "?" + rawParams;
	document.getElementById('link_suppressed').href += "?" + rawParams;

	if(document.getElementById('result_active') !== null)
	{
		Update(urlParams["host"] + "/control/snapshot?format=jsonp&callback=octotron_state&v"
			, urlParams["a_auth"], "result_active", ProcessSnapshot);
	}

	if(document.getElementById('result_suppressed') !== null)
	{
		Update(urlParams["host"] + "/view/suppressed?callback=octotron_state"
			, urlParams["s_auth"], "result_suppressed", ProcessSuppressed);
	}
});


function Update(data_url, auth, target, processor)
{
	if(!("host" in urlParams))
		return;

	var data = {};

	$.ajax({
		type: "GET",
		url: "http://" + auth + "@" + data_url,
		contentType: "application/json",
		dataType: "jsonp",
		crossDomain: true,
		async: false,
		cache: true,
		success: function(json) { processor(json, target); },
		error: function(json) { $("#msg").html("<p>Error: could not get data</p>"); }
	});
}

function ProcessSnapshot(json, target)
{
	var table = $('<table></table>').attr("cellspacing", "1").addClass("tablesorter");

	var head = $('<thead></thead>');
	var fields = $('<tr></tr>');

	fields.append($('<th></th>').text("status"))
	fields.append($('<th></th>').text("time"))
	fields.append($('<th></th>').text("tag"))
	fields.append($('<th></th>').text("loc"))
	fields.append($('<th></th>').text("msg"))

	fields.append($('<th></th>').text("attr.name"))
	fields.append($('<th></th>').text("attr.value"))
	fields.append($('<th></th>').text("suppressed"))

	head.append(fields)

	var body = $('<tbody></tbody>');

	for(var i = 0; i < json.data.length; i++)
	{
		var column = $('<tr></tr>');


		var date = new Date(json.data[i].info.time*1000);
		var time = date.getDate() + "-" + date.getMonth() + " " + date.getHours() + ":" + date.getMinutes();

		column.append($('<td></td>').text(json.data[i].info.status))
		column.append($('<td></td>').text(time))
		column.append($('<td></td>').text(json.data[i].usr.tag))
		column.append($('<td></td>').text(json.data[i].usr.loc))
		column.append($('<td></td>').text(json.data[i].usr.msg))

		var attribute_aid = json.data[i].reaction.attribute;
		var name = null;
		var value = null;

		var attributes = json.data[i].model.entity.sensor.concat(json.data[i].model.entity.var);

		for(var j = 0; j < attributes.length; j++)
		{
			var item = attributes[j];

			if(item["AID"] == attribute_aid)
			{
				name = item["name"]
				value = item["value"]
			}

		}

		column.append($('<td></td>').text(name))
		column.append($('<td></td>').text(value))
		column.append($('<td></td>').text(json.data[i].reaction.suppressed))

		body.append(column);
	}

	table.append(head);
	table.append(body);

	$('#' + target).append(table.tablesorter());
}

function ProcessSuppressed(json, target, host)
{
	var table = $('<table></table>').attr("cellspacing", "1").addClass("tablesorter");

	var head = $('<thead></thead>');
	var fields = $('<tr></tr>');

	fields.append($('<th></th>').text("reason"))
	fields.append($('<th></th>').text("attr.name"))
	fields.append($('<th></th>').text("tag"))
	fields.append($('<th></th>').text("descr"))
	fields.append($('<th></th>').text("entity AID"))
	fields.append($('<th></th>').text("unsuppress"))

	head.append(fields)

	var body = $('<tbody></tbody>');

	for(var i = 0; i < json.data.length; i++)
	{
		var column = $('<tr></tr>');

		column.append($('<td></td>').text(json.data[i].info.descr))
		column.append($('<td></td>').text(json.data[i].model.attribute.name))
		column.append($('<td></td>').text(json.data[i].usr.tag))
		column.append($('<td></td>').text(json.data[i].usr.descr))

		column.append($('<td></td>').text(json.data[i].model.entity.AID))
		var url = host + "/modify/unsuppress?path=obj(AID=="+json.data[i].model.entity.AID+")&template_id="+json.data[i].template.AID;

		var link = $("<a></a>").attr("href", url).text("unsuppress");
		column.append($('<td></td>').html(link));

		body.append(column);
	}

	table.append(head);
	table.append(body);

	$('#' + target).append(table.tablesorter());
}
