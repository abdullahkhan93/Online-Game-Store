$(document).ready(() => {
    console.log('gameid', GAME_ID)

    // npm package for generating colors
    const getColor = () => randomColor({
        luminosity: 'light',
        format: 'rgb'
    });

    // bind chart
    let ctx = document.getElementById("myChart").getContext('2d');
    let myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: []
        },
        options: {
            legend: {
                position: 'top',
            }
        }
    });

    // dto 
    const buildDataset = (label, data) => {
        const datasetColor = getColor();
        return {
            label: label,
            data: data,
            backgroundColor: datasetColor,
            fill: false,
            borderColor: datasetColor,
            borderWidth: 2
        }
    };

    // updates the chart
    updateData = (data) => {
        const dataParsed = JSON.parse(data);
        console.log('dataParsed: ', dataParsed)

        const units = []
        const unitsCumulative = []
        const revenue = []
        const revenueCumulative = []
        const labels = []

        // build cumulative data from response
        let unitSum = 0, revenueSum = 0;
        dataParsed.data.sales.reverse().forEach(sale => {
            unitSum = unitSum + sale.sales;
            revenueSum = revenueSum + sale.revenue;
            labels.push(sale.date)
            revenueCumulative.push(revenueSum)
            unitsCumulative.push(unitSum)
            revenue.push(sale.revenue)
            units.push(sale.sales)
        });

        // build and insert datasets for charts js
        myChart.data.labels = labels;
        myChart.data.datasets = [
            buildDataset('units', units),
            buildDataset('units cumulative', unitsCumulative),
            buildDataset('revenue', revenue),
            buildDataset('revenue cumulative', revenueCumulative)
        ]

        $('#sales-totals-revenue').text(dataParsed.data.totals.totalRevenue + ' €');
        $('#sales-totals-units').text(dataParsed.data.totals.totalSales);
        myChart.update();
    };

    // load data async
    const loadData =  () => gamestoreAJAX
        .get('../../gamestatistics/' + GAME_ID)
        .done(data => {
            updateData(data);
        });

    loadData();

    $('#get-gamestats').click(function() {
        loadData();
    });
});
