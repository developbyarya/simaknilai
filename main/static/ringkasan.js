const ctx = document.querySelector("#chart").getContext('2d');
const table = document.getElementById("table-body")
let labels = [];
let datasets = [];
const selected = document.querySelector("option[selected]").value;
fetch(`api/ringkasan?id=${selected}`)
.then(res => res.json())
.then(data => {
    labels = [...Object.keys(data.data)];
    labels.forEach(elem => {
        datasets = [...datasets, data.data[elem].zonasi.avg];
        // Table
        const el = data.data[elem]
        const tableEl = document.createElement('tr')
        tableEl.innerHTML = `
        <th scope="row">${elem}</th>
        <th>${el.zonasi.high}</th>
        <th>${el.zonasi.low}</th>
        <th>${el.zonasi.avg}</th>
        <th>${el.all.high}</th>
        <th>${el.all.low}</th>
        <th>${el.all.avg}</th>
        `;
        table.appendChild(tableEl);
        console.log(tableEl);
    });
    
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Rata-rata Nilai Zonasi',
                data: datasets,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',                
                ],
                
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)'
                ],
                borderWidth: 3
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: false
                }
        }
    }
});
    fetch(`http://127.0.0.1:8000/api/prediksi?id=${selected}`)
    .then(res => res.json())
    .then(res => {
        const tableEl = document.createElement('tr')
        tableEl.classList.add('table-dark')
        tableEl.innerHTML = `
        <th scope="row" colspan="2">Prediksi Rata-rata</th>
        <th colspan="5">${Math.round((res.data.prediksi + Number.EPSILON) * 100) / 100}</th>
        `;
        table.appendChild(tableEl);
    })
})
