Highcharts.chart('container', {
    chart: {
        type: 'pie'
    },
    title:{
        text: 'Número de donaciones por tipo'
    },
    series: [{
        name: 'Donaciones',
        data: []

    }]
});
Highcharts.chart('container2', {
    chart: {
        type: 'pie'
    },
    title:{
        text: 'Número de pedidos por tipo'
    },
    series: [{
        name: 'Donaciones',
        data: []
    }]
});

fetch('http://localhost:5000/get-graphs-data')
    .then(response => response.json())
        .then(data => {
            console.log(data)
            const d_chart = Highcharts.charts.find(
                (chart) => chart && chart.renderTo.id ==='container')
            const p_chart = Highcharts.charts.find(
                (chart) => chart && chart.renderTo.id ==='container2')
            d_chart.update({
                series: [{
                    name: 'Donaciones',
                    data: data['donaciones']
                }
                ]
            })
            p_chart.update({
                series: [{
                    name: 'Pedidos',
                    data: data['pedidos']
                }]
            }
        )
        })
