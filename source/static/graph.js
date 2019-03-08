// Quelle: https://github.com/networkx/networkx/tree/master/examples/javascript
// Nur leicht adaptiert
// TODO: Eigenen, passenden D3-Code schreiben


// This is adapted from https://bl.ocks.org/mbostock/2675ff61ea5e063ede2b5d63c08020c7

var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height");

var simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(function (d) {
        console.log("d.id 1: ", d.id) // TODO: Aus irgendeinem Grund werden durch diese Funktion die letzten drei Stellen der Tweet_IDs gerundet 
        return d.id;
    }))
    .force("charge", d3.forceManyBody())
    .force("center", d3.forceCenter(width / 2, height / 2));


//d3.json("../temp_files/json/graph/graph.json", function (error, graph) {
d3.json("/static/graph.json", function (error, graph) {
    if (error) throw error;

    var link = svg.append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(graph.links)
        .enter().append("line");
    
    var node = svg.append("g")
        .attr("class", "nodes")
        .selectAll("circle")
        .data(graph.nodes)
        .enter().append("circle")
        .attr("r", 10)
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));
	
	var label = svg.selectAll(null)
		.data(graph.nodes)
		.enter()
		.append("text")
		.text(function (d) { return d.label; })
		.style("text-anchor", "middle")
		.style("fill", "#555")
		.style("font-family", "Arial")
		.style("font-size", 8);
		
	
	
    	// TODO: image is still not working
	node.append("image")
		.attr("xlink:href", "https://github.com/favicon.ico")
		.attr("x", -8)
		.attr("y", -8)
		.attr("width", 16)
		.attr("height", 16);
		
    simulation
        .nodes(graph.nodes)
        .on("tick", ticked);

    simulation
   		.force("link")
        .links(graph.links);

    function ticked() {
        link
            .attr("x1", function (d) {
                return d.source.x;
            })
            .attr("y1", function (d) {
                return d.source.y;
            })
            .attr("x2", function (d) {
                return d.target.x;
            })
            .attr("y2", function (d) {
                return d.target.y;
            });

        node
            .attr("cx", function (d) {
                return d.x;
            })
            .attr("cy", function (d) {
                return d.y;
            });
    }
});


// Ein Test for onClick
svg.on("click", function() {
	var coords = d3.mouse(this);
    console.log("coords: ", coords)     
})


function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
}

function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
}

function dragended(d) {
    if (!d3.event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
}


