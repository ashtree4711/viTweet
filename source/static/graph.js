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



        // Append a "defs" element to SVG
        var defs = svg.append("defs").attr("id", "imgdefs")

        // Store an element called "clipPath#clip-circle" in defs, which can be used at a later time
        var clipPath = defs.append('clipPath').attr('id', 'clip-circle')
                .append("circle")
                .attr("r", 24)
                .attr("cx", 14)
                .attr("cy", 14);

        // Use images (profile pictures) to display the nodes
        node.append("image")
        		    .attr("xlink:href", function (d) { return d.profile_picture; })
              	.attr("x", -10)
              	.attr("y", -10)
              	.attr("width", 48)
              	.attr("height", 48)
                // Clip images to a circle shape using the previously defined #clip-circle
                .attr("clip-path", "url(#clip-circle)");

    // Add label texts to nodes
    node.append("text")
        .attr("dx", 38)
        .attr("dy", ".35em")
        // Text is hidden
        .style("visibility","hidden")
        .text(function(d) { return d.tweet_content;});


	var setEvents = node
          .on( 'click', function (d) {
              d3.select("h2").html(d.label);
           })


		.on("mouseover", function(d)
		 {
          // Mouseover enlarges image
          d3.select(this).select("image")
            	.transition()
              	.duration(200)
              	.attr("x", -10*2)
             	  .attr("y", -10*2)
              	.attr("height", 48*1.5)
              	.attr("width", 48*1.5);
          d3.select(this).select("#clip-circle") // Does not work
            .transition()
              .duration(200)
              .attr("r", 24*1.5)
              .attr("cx", 14*2)
              .attr("cy", 14*2);

          // Mouseover shows the hidden text
    		  d3.select(this).select("text").style("visibility","visible")
		 })

		.on("mouseout", function(d)
 		{
        // On mouseout the image becomes smaller again
        d3.select(this).select("image")
          .transition()
            .duration(200)
            .attr("x", -10)
            .attr("y", -10)
            .attr("height", 48)
            .attr("width", 48);
        d3.select(this).select("#clip-circle")
        .transition()
          .duration(200)
          .attr("r", 24)
          .attr("cx", 14)
          .attr("cy", 14);

        // On mouseout the text is again hidden
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
