d3.csv("condensed_dow_and_sentiment.csv").then(function(sentimentData) {


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

// Add all positive_sentiment
positive_sentiment2 = positive_sentiment.map(Number);
var sum1 = 0
for (var i = 0; i < positive_sentiment2.length; i ++) {
  sum1 += positive_sentiment2[i]
};
console.log(`Sum of all positives: ${sum1}`);

// Find the average positive_sentiment
var avg1 = sum1 / positive_sentiment2.length;
console.log(`Average of positives: ${avg1}`);

// ------------------------------------------------------

// Add all negative_sentiment
negative_sentiment2 = negative_sentiment.map(Number);
var sum2 = 0
for (var i = 0; i < negative_sentiment2.length; i ++) {
  sum2 += negative_sentiment2[i]
};
console.log(`Sum of all negatives: ${sum2}`);

// Find the average negative_sentiment
var avg2 = sum2 / negative_sentiment2.length;
console.log(`Average of negatives: ${avg2}`);

var data = [
  {
    x: ['<b>Positive Average</b>', '<b>Negative Average</b>'],
    y: [avg1, -avg2],
    marker:{
      color: ['rgba(222,45,38,0.8)', 'rgba(0,0,0,0.8)']
    },
    type: 'bar'
  }
];

var layout = {
  title: '<b>Trump Tweet Average Sentiment</b>',
  font:{
    family: 'Raleway, sans-serif'
  },
  yaxis: {
    zeroline: false,
    gridwidth: 2
  },
  bargap :0.2
};


Plotly.newPlot('myDiv', data, layout);
});
