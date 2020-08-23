function makeResponsive() {

  // resize chart according to window size
var svgArea = d3.select("body").select("svg");

if (!svgArea.empty()) {
  svgArea.remove();
}

  // svg params
var svgHeight = window.innerHeight;
var svgWidth = window.innerWidth;

var margin = {
  top: 50,
  right: 100,
  bottom: 80,
  left: 20
};

var chartwidth = svgWidth - margin.left - margin.right;
var chartheight = svgHeight - margin.top - margin.bottom;

var svg = d3
.select("body")
.append("svg")
.attr("width", svgWidth)
.attr("height", svgHeight);

var chartGroup = svg.append("g")
.attr("transform", `translate(${margin.left - 20 } , ${margin.top })`);

//Read the data
d3.csv("condensed_dow_and_sentiment.csv", function(data) {

  // Add X axis
  var x = d3.scaleLinear()
    .domain([0, 120])
    .range([ 100, (chartwidth) ]);
  svg.append("g")
  .attr("transform", `translate(${chartwidth / chartwidth}, ${(chartheight)+ 50})`)
    .call(d3.axisBottom(x));

  // Add Y axis
  var y = d3.scaleLinear()
    .domain([15, 2000])
    .range([ chartheight, 0]);
  svg.append("g")
  .attr("transform", `translate(${(chartwidth/chartwidth) + 100}, ${(chartheight/chartheight)+ 50})`)
    .call(d3.axisLeft(y));

  // Add a scale for bubble size
  var z = d3.scaleLinear()
    .domain([-1, 1])
    .range([ 2, 2]);

  // Add dots
  chartGroup.append('g')
    .selectAll("dot")
    .data(data)
    .enter()
    .append("circle")
      .attr("cx", function (d) { return x(d.Tweet_count); } )
      .attr("cy", function (d) { return y(d.Volatility); } )
      .attr("r", function (d) { return z(d.Close); } )
      .style("fill", "#69b3a2")
      .style("opacity", "0.7")
      .attr("stroke", "black")

  chartGroup.append("text")
      .attr("x", ((chartwidth + 100)/ 2))             
      .attr("y", 0 - ((margin.top - 10 )/ 2))
      .attr("text-anchor", "middle")  
      .style("font-size", "16px") 
      .attr("class", "axisText")
      .text("Daily Volatility & Tweet Count");
  
  chartGroup.append("text")
      .attr("transform", `translate(${(chartwidth/2) + 50}, ${(chartheight) + 40})`)
      .attr("class", "axisText")
      .text("Tweet Count");

  chartGroup.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", margin.left)
      .attr("x", 0 - (chartheight / 2))
      .attr("dy", "1em")
      .attr("class", "axisText")
      .text("Daily Volatility");
})
}
makeResponsive();

// Event listener for window resize
d3.select(window).on("resize", makeResponsive);

