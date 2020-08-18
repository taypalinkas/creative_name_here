Plotly.d3.csv('candlestick/DJI.csv', function(rows){

function unpack(rows, key) {
  return rows.map(function(row) {
    return row[key];
  });
}

var trace = {
  x: unpack(rows, 'Date'),
  close: unpack(rows, 'Close'),
  open: unpack(rows, 'Open'),  
  high: unpack(rows, 'High'),
  low: unpack(rows, 'Low'),

  increasing: {line: {color: 'green'}},
  decreasing: {line: {color: 'red'}},

  type: 'candlestick',
  xaxis: 'x',
  yaxis: 'y'
};

var data = [trace];

var layout = {
  title: 'Dow Jones Industrial Average',
  dragmode: 'zoom',
  showlegend: false,
  xaxis: {
    autorange: true,
    title: 'Date Range',
    rangeselector: {
      x: 0,
      y: 1.2,
      xanchor: 'left',
      font: {size:12},
      buttons: [{
        step: 'month',
        stepmode: 'backward',
        count: 1,
        label: '1 month'
      }, {
        step: 'month',
        stepmode: 'backward',
        count: 3,
        label: '3 months'
      }, {
        step: 'month',
        stepmode: 'backward',
        count: 6,
        label: '6 months'
      }, {
        step: 'month',
        stepmode: 'backward',
        count: 12,
        label: '1 Year'
      }, {
        step: 'all',
        label: 'All dates'
      }]
    }
  },
  yaxis: {
    autorange: true,
  }
};

Plotly.newPlot('stockChart', data, layout);
});