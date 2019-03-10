import React from "react";
import { Line } from 'react-chartjs-2';
var moment = require('moment');

function percentFullChart(data) {

    let labels = [];
    let dataset = [];

    for (let i = 0; i < data.length; i++) {
        let datapoint = data[i];
        labels.push(
            moment.unix(datapoint.timestamp)
        );
        dataset.push(datapoint.percent_full);
    }

    var chartData = {
        labels: labels,
        datasets: [{
            label: 'Percent full',
            fill: true,
            backgroundColor: 'rgba(0,123,255,0.4)',
            borderColor: 'rgba(0,123,255,1)',
            data: dataset
        }]
    };

    var chartOptions = {
        title: {
            text: 'Sailing capacity'
        },
        scales: {
            xAxes: [{
                type: 'time',
                time: {
                    format: 'HH:mm',
                    tooltipFormat: 'll HH:mm'
                },
                scaleLabel: {
                    display: false,
                    labelString: 'Time'
                }
            }],
            yAxes: [{
                scaleLabel: {
                    display: false,
                    labelString: 'Percent'
                },
                ticks: {
                    suggestedMin: 0,
                    suggestedMax: 100
                }
            }]
        },
    };

    return <div className="row mb-4 pt-2 percentFullChart"><Line data={chartData} width={600} height={200} options={chartOptions} /></div>;
}

export { percentFullChart };