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

        // Store an element called "clipPath#clip-circle-small" in defs, which can be used at a later time
        var clipPath = defs.append('clipPath').attr('id', 'clip-circle-small')
                .append("circle")
                .attr("r", 12)
                .attr("cx", 0)
                .attr("cy", 0);

        // "clipPath#clip-circle-large" is needed when images are enlarged on mouseover
        clipPath = defs.append('clipPath').attr('id', 'clip-circle-large')
                .append("circle")
                .attr("r", 12*1.5)
                .attr("cx", 0)
                .attr("cy", 0);

        // Use images (profile pictures) to display the nodes
        node.append("image")
        		.attr("xlink:href", function (d) {
        		return d.profile_picture; })
              	.attr("x", -12)
              	.attr("y", -12)
              	.attr("width", 24)
              	.attr("height", 24)

                // Clip images to a circle shape using #clip-circle-small
                .attr("clip-path", "url(#clip-circle-small)");

    // Add label texts to nodes
    node.append("text")
        .attr("dx", 12*1.5+2)
        .attr("dy", ".35em")
        // Text is hidden
        .style("visibility","hidden")
        .text(function(d) { return d.tweet_content;})
		.call(wrap, 30);
	
	function wrap(text, width) {
    text.each(function () {
        var text = d3.select(this),	
            words = text.text().split(/\s+/).reverse(),
            word,
            line = [],
            lineNumber = 0,
            lineHeight = 1.2, 
            x = text.attr("x"),
            y = text.attr("y"),
            dy = parseFloat(text.attr("dy")),
            tspan = text.text(null)
                        .append("tspan")
                        .attr("x", 0)
                        .attr("y", y)
                        .attr("dy", dy + "em");
        while (word = words.pop()) {
            line.push(word);
            tspan.text(line.join(" "));
            if (tspan.node().getComputedTextLength() > width) {
                line.pop();
                tspan.text(line.join(" "));
                line = [word];
                tspan = text.append("tspan")
                            .attr("x", 0)
                            .attr("y", y)
                            .attr("dy", lineHeight + "em")
                            .text(word);
            }
        }
    });
}

	var setEvents = node
    .on( 'click', function (d) {
          d3.select("h3").html(d.label);
    })

		.on("mouseover", function(d) {
          // Mouseover enlarges image
          d3.select(this).select("image")
            	.transition()
              	.duration(200)
                .attr("x", -12*1.5)
              	.attr("y", -12*1.5)
              	.attr("width", 24*1.5)
              	.attr("height", 24*1.5)
                // Clip images to the larger circle shape using #clip-circle-large
                .attr("clip-path", "url(#clip-circle-large)");

          // Mouseover shows the hidden text
    		  d3.select(this).select("text").style("visibility","visible")
		 })

		.on("mouseout", function(d)	{
        // On mouseout the image becomes smaller again
        d3.select(this).select("image")
          .transition()
            .duration(200)
            .attr("x", -12)
            .attr("y", -12)
            .attr("width", 24)
            .attr("height", 24)
            .attr("clip-path", "url(#clip-circle-small)");

        // On mouseout the text is hidden again
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
