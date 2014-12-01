var d3utils = {};

(function (global) {
  "use strict";

  // Get options
  var getopt = function(opt, field_name, default_value) {
    return typeof opt[field_name] != 'undefined' ? opt[field_name] : default_value;
  }

  function drawPieChart(d3div, chart_data) {
    // chart_data.data contains the actual data

    d3div.html(""); // clear div
    var title = getopt(chart_data, 'title', '');

    // Desired width and height of chart
    var w = getopt(chart_data, 'width', 500);
    var h = getopt(chart_data, 'height', 500);
    var pad = getopt(chart_data, 'pad', 50);
    var textmargin = getopt(chart_data, 'textmargin', 40);
    var r = Math.min(w,h) / 2 - pad; // Pie chart radius

    var div = d3div.append('div');
    if(title !== '') {
      div.append('p').attr('class', 'pietitle').text(title);
    }

    // var color = d3.scale.category20();

    var arc = d3.svg.arc()
          .outerRadius(r)
          .innerRadius(r/2);
    

    var pie = d3.layout.pie()
          .sort(null)
          .value(function(d) { return d.value; });

    var svg = d3.select("#piechart").append("svg")
          .attr("width", w)
          .attr("height", h)
          .append("g")
          .attr("transform", "translate(" +w/2 + "," + h/2 + ")");
    var g = svg.selectAll(".arc")
          .data(pie(chart_data.data))
          .enter().append("g")
          .attr("class", "arc");

    g.append("path")
      .attr("d", arc)
      .style("fill", function(d, i) { return d.data.color; });

    g.append("text")
      .style("fill", function(d, i) { return d.data.color; })
      .attr("transform", function(d) {
        var c = arc.centroid(d);
        var x = c[0];
        var y = c[1];
        var h = Math.sqrt(x*x + y*y);
        return "translate(" + (x/h * (r + textmargin)) +  ',' + (y/h * (r + textmargin)) +  ")"; 
      })
      .attr("dy", ".35em")
      .attr("text-anchor", function(d) {
        // are we past the center?
        return (d.endAngle + d.startAngle)/2 > Math.PI ? "end" : "start";
      })
      .text(function(d) { return d.data.label; });
  }

  // exports
  global.drawPieChart = drawPieChart;

})(d3utils);
