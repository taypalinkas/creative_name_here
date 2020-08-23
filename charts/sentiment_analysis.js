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
    top: 80,
    right: 120,
    bottom: 100,
    left: 120
  };

  var chartwidth = svgWidth - margin.left - margin.right;
  var chartheight = svgHeight - margin.top - margin.bottom;

  // SVG wrapper 
  var svg = d3
    .select("body")
    .append("svg")
    .attr("width", svgWidth)
    .attr("height", svgHeight);

  var chartGroup = svg.append("g")
    .attr("transform", `translate(${margin.left}, ${margin.top})`);

// csv import & format data 
// ("%Y-%m-%d %H:%M:%S")
  d3.csv("condensed_dow_and_sentiment.csv").then(function(sentimentData) {
  
  var parseTime = d3.timeParse("%Y-%m-%d %H:%M:%S");
    sentimentData.forEach(function(data) {
      data.Time = parseTime(data.Time);
      data.Volatility = +data.Volatility;
      data.Close = +data.Close;
    });

    // Create  scales
    var xTimeScale = d3.scaleTime()
      .domain(d3.extent(sentimentData, d => d.Time))
      .range([0, chartwidth]);

    var yLinearScale1 = d3.scaleLinear()
      .domain([0, d3.max(sentimentData, d => d.Close)])
      .range([chartheight, 0]);

    var yLinearScale2 = d3.scaleLinear()
      .domain([0, d3.max(sentimentData, d => d.Volatility)])
      .range([chartheight, 0]);

    //  Create the axes 
    var bottomAxis = d3.axisBottom(xTimeScale).tickFormat(d3.timeFormat("%b-%y"));
    var leftAxis = d3.axisLeft(yLinearScale1);
    var rightAxis = d3.axisRight(yLinearScale2);
    
    // Append the axes to the chartGroup

    // Add x-axis
    chartGroup.append("g")
      .attr("transform", `translate(0, ${chartheight})`)
      .call(bottomAxis);

    // Add y-axis (Left)
    chartGroup.append("g").call(leftAxis);

    // Add y-axis (Right)
  chartGroup.append("g")
  .attr("transform", `translate(${chartwidth}, 0)`)
  .call(rightAxis);

    // Set up generators and append SVG paths

    // Line generator for Volatility
    var line1 = d3.line()
      .x(d => xTimeScale(d.Time))
      .y(d => yLinearScale2(d.Volatility));

    // Line generator for Close
    var line2 = d3.line()
      .x(d => xTimeScale(d.Time))
      .y(d => yLinearScale1(d.Close));

    // Append a path for line1
    chartGroup
      .data([sentimentData])
      .append("path")
      .attr("d", line1)
      .classed("green", true)
      .style("opacity", .7)
      .on("mouseover", function() {
        d3.select(this)
          .style("stroke-width", "7");
      })
      .on("mouseout", function() {
        d3.select(this)
          .style("stroke-width", "3");
      });

    // Append a path for line2
    chartGroup
      .data([sentimentData])
      .append("path")
      .attr("d", line2)
      .classed("blue", true)
      .style("opacity", .7)
      .on("mouseover", function() {
        d3.select(this)
          .style("stroke-width", "7");
      })
      .on("mouseout", function() {
        d3.select(this)
          .style("stroke-width", "3");
      });

      var lis =  sentimentData["columns"].slice(1)

    var circlesGroup = chartGroup.selectAll("circle")
      .data(sentimentData)
      .enter()
      .append("circle")
      .attr("cx", d => xTimeScale(d.Time))
      .attr("cy", d => yLinearScale1(d.Close))
      .attr("r", "1")
      .attr("fill", "blue")
      .attr("stroke-width", "0")
      .attr("stroke","white")

    // Initialize Tooltip
    var toolTip = d3.tip()
      .attr("class", "tooltip")
      .offset([65, 0])
      .html(function(d,k) {
        return (`Time: ${d.Time} <br> 
          Open: ${d.Open} <br> 
          Close: ${d.Close}`);
      });

      // Create the tooltip in chartGroup.
    chartGroup.call(toolTip);

    // Create "mouseover" event listener to display tooltip
    circlesGroup.on("mouseover", function(d) {
      toolTip.show(d, this);
    })
    // Create "mouseout" event listener to hide tooltip
    .on("mouseout", function(d) {
      toolTip.hide(d);
    });

    // Create axes labels
    chartGroup.append("text")
      .attr("transform", `translate(${chartwidth / 2}, ${(chartheight/chartheight)-20})`)
      .attr("class", "title")
      .text("Dow & Volatility")

    // Create axes labels
    chartGroup.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - margin.left + 35)
      .attr("x", 0 - (chartheight / 2))
      .attr("dy", "1em")
      .attr("class", "axisText")
      .text("Dow Jones Industrial Average");


    // Create axes labels
    chartGroup.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", chartwidth + 55)
      .attr("x", 0 - (chartheight / 2))
      .attr("dy", "1em")
      .attr("class", "axisText")
      .text("Volatility");


    var j = 1;
    
    var color_list = ["darkblue","green"]

    chartGroup.append("text")
      .attr("transform", `translate(${chartwidth / 2}, ${chartheight + margin.top})`)
      .attr("class", "axisText")
      .text("Year");

    console.log(sentimentData["columns"].slice(4,6));
    var sentimentDataSlice = ["Close", "Volatility"];

    var legends = svg.append("g")
          .attr("transform", `translate(${chartwidth}, ${(chartheight/chartheight)+ 10})`)
          .selectAll(".legends")
          .data(sentimentDataSlice);

    var legend = legends
          .enter()
          .append("g")
          .classed("legends",true)
          .attr("transform",function(d,i){return "translate(0," + (i + 1 )* 15 + ")";});
    legend.append("rect")
          .attr("width", 15)
          .attr("height",3)
          .attr("fill",function (d,j){return color_list[j];})
          .style("opacity", .7)

    legend.append("text")
          .text(function(d,j){return d;})
          .attr("fill","black")
          .attr("font-size","10")
          .attr("font-weight", "bold")
          .attr("x",30)
          .attr("y", 4);
          j = j + 1;
  }).catch(function(error) {
    console.log(error);
  });
  }

makeResponsive();

// Event listener for window resize
d3.select(window).on("resize", makeResponsive);
