d3.csv("../charts/condensed_dow_and_sentiment.csv").then(function(sentimentData) {

//count
var sum = 0;

// Arrays for Vader_compound
var positive_sentiment = [];
var neutral_sentiment = [];
var negative_sentiment = [];

sentimentData.forEach(function(score) {

  // If x, add it to the list of positive_sentiment
  if (score.Vader_compound >= 0.05) {
    positive_sentiment.push(score.Vader_compound);
  }
  // If between x and y, add it to neutral_sentiment
  else if (score.Vader_compound > -0.05 && score.Vader_compound < 0.05) {
    neutral_sentiment.push(score.Vader_compound);
  }
  // Otherwise, add it to negative_sentiment
  else {
    negative_sentiment.push(score.Vader_compound);
  }
});

// Store the length
var num_positive_sentiment = positive_sentiment.length;
var num_neutral_sentiment = neutral_sentiment.length;
var num_negative_sentiment = negative_sentiment.length;

var data = [
  {
    x: ['<b>Positive</b>', '<b>Neutral</b>', '<b>Negative</b>'],
    y: [num_positive_sentiment, num_neutral_sentiment, num_negative_sentiment],
    marker:{
      color: ['rgba(222,45,38,0.8)', 'rgba(0,0,0,0.8)','rgba(222,45,38,0.8)']
    },
    type: 'bar'
  }
];

var layout = {
  title: '<b>Trump Tweet Count</b>',
  font:{
    family: 'Raleway, sans-serif'
  },
  yaxis: {
    zeroline: false,
    gridwidth: 2
  },
  bargap :0.2
};

console.log(data)
Plotly.newPlot('myDiv', data, layout);
});
