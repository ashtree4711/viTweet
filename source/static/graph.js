// Based on https://github.com/networkx/networkx/tree/master/examples/javascript / https://bl.ocks.org/mbostock/2675ff61ea5e063ede2b5d63c08020c7
// and https://bl.ocks.org/mbostock/950642
    
var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height");

var simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(function (d) {
        console.log("d.id 1: ", d.id) // TODO: Aus irgendeinem Grund werden durch diese Funktion die letzten drei Stellen der Tweet_IDs gerundet
        return d.id;
    }).distance(100).strength(1))
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

    var node = svg.selectAll(".node")
          .data(graph.nodes)
        .enter().append("g")
        .attr("class", "node")
        .call(d3.drag()
              .on("start", dragstarted)
              .on("drag", dragged)
              .on("end", dragended));
			
   
    node.append("image") // Use images for nodes instead of circles
		.attr("xlink:href", function (d) { return d.profile_picture; })
      	.attr("x", -8)
      	.attr("y", -8)
      	.attr("width", 20)
      	.attr("height", 20);
      		
	//Text is hidden
    node.append("text")
        .attr("dx", 12)
        .attr("dy", ".35em") 
        .style("visibility","hidden")   
        .text(function(d) { return d.tweet_content;
        });
	
        	
	var setEvents = node
          .on( 'click', function (d) {
              d3.select("h2").html(d.label);   
           })
	
		//mouseover shows the hidden text
		.on("mouseover", function(d)
		 {
    		 d3.select(this).select("text").style("visibility","visible")
		 })
		 
		//with mouseout the text is again hidden
		.on("mouseout", function(d)
 		{
   			  d3.select(this).select("text").style("visibility","hidden")
 		})
		
	
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
            .attr("transform", function(d) {
                return "translate(" + d.x + "," + d.y + ")";
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


