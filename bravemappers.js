function escpressed(e) {
    if (e.keyCode == 27) {
        ip = document.getElementById('info')
        ip2 = document.getElementById('maininfo')
        ip.style.display='none';
        ip2.style.display='none';
    }
}

document.addEventListener('keyup', escpressed, false);

function pop(ar) {
    ip = document.getElementById('info')
    ip2 = document.getElementById('maininfo')
    if (!ip) return;
    ip.style.display = (ip.style.display == 'block') ? 'none' : 'block';
    ip2.style.display = 'none';
    stuff = JSON.parse(ar);    
    ip.innerHTML = '<h1><a href=\"http://www.openstreetmap.org/user/' + stuff[1] + '\">' + stuff[1] + '</a> (' + stuff[0] + ')</h1>'; 
    ip.innerHTML += '<h2>' + new Date(stuff[11]).toDateString() + ' - ' + new Date(stuff[12]).toDateString() + '</h2>';
    ip.innerHTML += '<p><strong>Edited</strong> ' + stuff[2] + ' nodes, ' + stuff[5] + ' ways, ' + stuff[8] + ' relations. <strong>Created</strong> ' + stuff[3] + ' nodes, ' + stuff[6] + ' ways, ' + stuff[9] + ' relations. <strong>Still around</strong> ' + stuff[4] + ' nodes, ' + stuff[7] + ' ways, ' + stuff[10] + ' relations.</p>';
    
    ip.innerHTML += '<p id=badge>' + stuff[1] + ' is<br /><big><strong>a ' + stuff[20] + stuff[21] + stuff[22] + stuff[18] + '</strong></big>';
    var snippet = '<br /><div id=\"charts\">';
    for (chartname in stuff[19]) {
        snippet += '<img width=300 height=300 src=' + stuff[19][chartname] + ' />'
    }
    snippet += '</div>';
    ip.innerHTML += snippet;
    ip.innerHTML += '</p><p><a href=\"#\" onClick=\"pop(null)\">close</a>';
}

function popinfo(ar, reg) {
    ip = document.getElementById('maininfo')
    ip2 = document.getElementById('info')
    if (!ip) return;
    ip2.style.display = 'none';
    stuff = JSON.parse(ar);    
    ip.style.display = (ip.style.display == 'block') ? 'none' : 'block';
    ip.innerHTML = '<h1>About the Brave Mappers project</h1>';
    ip.innerHTML += '<p>This web site tells the story of the OpenStreetMap contributors of '+reg+'. It uses the <a href=\"https://wiki.openstreetmap.org/wiki/Planet.osm/full\">full history planet</a> to look back in time to unveil the stories of heroic contributors who are no longer active, nodes and ways that you thought everyone had forgotten about, and of those who have been toiling away creating the awesome free and open map that we have today.</p><h2>What do you see?</h2><p>The page shows the activity of mappers through time. The length of one mapper\'s bar represents the time he has been mapping here. This is also how the mappers are sorted: those who have been involved the longest, appear at the top. The taller the bar, the higher his average number of edits per day. Users with really big names have especially many daily edits. They are superhuman or bots. The more transparent the mapper\'s bar, the more of his edits have been wiped out by more recent mapping. Finally, the bars and names are clickable for mapper stat pr0n.</p>';
    ip.innerHTML += '<h2>Overall Statistics</h2>';
    var tablesnippet = '<table width=400 border=0 cellpadding=2 align=center>';
    tablesnippet += '<tr><td width=200 align=right><strong>First recorded edit</strong><td>' + new Date(stuff[0]).toDateString() + '</tr>';
    tablesnippet += '<tr><td align=right><strong>Last recorded edit</strong><td>' + new Date(stuff[1]).toDateString() + '</tr>';
    tablesnippet += '<tr><td align=right><strong>Total nodes</strong><td>' + stuff[2] + '</tr>';
    tablesnippet += '<tr><td align=right><strong>Total ways</strong><td>' + stuff[3] + '</tr>';
    tablesnippet += '<tr><td align=right><strong>Total relations</strong><td>' + stuff[4] + '</tr>';
    tablesnippet += '<tr><td align=right><strong>Total users</strong><td>' + stuff[5] + '</tr>';
    tablesnippet += '<tr><td align=right><strong>Users not displayed <br />(20 contributions on current map or less)</strong><td>' + stuff[6] + '</tr>';
    tablesnippet += '<tr><td align=right><strong>Users with only 1 edit</strong><td>' + stuff[7] + '</tr>';
    tablesnippet += '</table>';
    ip.innerHTML += tablesnippet;
    ip.innerHTML += '<h2>Stuff used</h2><ul><li>The aforementioned full history planet, more specifically <a href=\"ftp://ftp5.gwdg.de/pub/misc/openstreetmap/osm-full-history-extracts/\">Peter K&ouml;rner\'s extracts</a><li>Jochen Topf and others\' awesome <a href=\"https://wiki.openstreetmap.org/wiki/Osmium\">Osmium</a> framework, by way of <a href=\"https://github.com/joto/osmium/tree/master/osmjs\">OSMJS</a>, for processing the history planet extract.<li>Python for processing the results into HTML and generating the charts, with useful contributions from NumPy, SciPy and PyMatLab</ul><p>most of the code is too much of a mess to share right now, but the OSMJS script is <a href=\"https://github.com/mvexel/OSMQualityMetrics/blob/master/UserStats.js\">on GitHub</a>.';
    ip.innerHTML += '<h2>Contact</h2><p>Do you want to know more about how this was done? Want this for your area? Suggestions for improvements? Bug report? Drop <a href=\"https://oegeo.wordpress.com/martijnvanexel/\">me</a> a line.'
    ip.innerHTML += '<p><small>A <img src=\'veryfurry4_100.png\' width=100 height=55 /> project.';
    
    ip.innerHTML += '<p><a href=\"#\" onClick=\"popinfo(null)\">close</a>';
//    ip.innerHTML += stuff.join(', ')
}
