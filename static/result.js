const canvas = document.querySelector("#bar-chart")
const barCard = document.querySelector(".diagram")
const tabelPenjualan = document.querySelector(".statistika-deskriptif")
const topSection = document.querySelector(".top-section")
const sideBarItem = []
let myChart;
let activeMenuID = "paling-banyak-dibeli"

function getSubMenuItem() {
	const list = document.querySelector(".item-list-sidebar").querySelector("ul")

	const items = Array.from(list.children)

	for (let i = 0; i < items.length; ++i) {
		const btn = items[i].querySelector("button")
		sideBarItem.push([btn.id, btn.value])
		btn.addEventListener('click', () => {
			list.querySelectorAll("button").forEach(el => {
				if(el.id !== btn.id) el.classList.remove("active")
			});
			btn.classList.add("active")

			if(btn.id === "histogram") {
				tabelPenjualan.style.display = 'none',
				topSection.style.display = 'none'
			} else {
				tabelPenjualan.style.display = 'flex',
				topSection.style.display = 'flex'
			}
		})
	}
}

function statistikaDeskriptifFunction(dataLabel, dataQuantity, statisika, table_title, table_header = []) {
	const tableTitle = document.querySelector('.table-title')
	const thead = document.querySelector('table').querySelector('thead')
	const tbody = document.querySelector('table').querySelector('tbody')

	thead.innerHTML = ''
	tbody.innerHTML = ''

	tableTitle.textContent = table_title
	const tr = document.createElement('tr')
	for (let item in table_header) {
		tr.innerHTML += `<th>${table_header[item]}</th>`
	}
	thead.append(tr)

	if(tbody.innerHTML.trim() === '') {
		let count = 1
		for (let item in dataQuantity) {
			const tr = document.createElement('tr')
			tr.innerHTML = `
				<td>${count}</td>
				<td>${dataLabel[item]}</td>
				<td>${dataQuantity[item]}</td>
			`
			tbody.append(tr)
			count++
		}
		
		const dataTerurut = document.querySelector(".data-terurut")
		dataTerurut.textContent = "[" + statisika["sorted"].join(", ") + "]"

		const minimum = document.querySelector(".minimum")
		const minimumName = minimum.querySelector(".item-name")
		const minimumQuantity = minimum.querySelector(".quantity")
		minimumName.textContent = statisika["minimum"]["name"]
		minimumQuantity.textContent = statisika["minimum"]["number"]
		
		const maximum = document.querySelector(".maximum")
		const maximumName = maximum.querySelector(".item-name")
		const maximumQuantity = maximum.querySelector(".quantity")
		maximumName.textContent = statisika["maximum"]["name"]
		maximumQuantity.textContent = statisika["maximum"]["number"]

		const mean = document.querySelector(".mean").querySelector('.quantity')
		mean.textContent = statisika["mean"]
		const median = document.querySelector(".median").querySelector('.quantity')
		median.textContent = statisika["median"]
		const modus = document.querySelector(".modus").querySelector('.quantity')
		modus.textContent = statisika["modus"]
	}	
}

/////////////////////////////////////////////////////////////////////////

function pizzaBar(pizzaTotal, statisika) {
	const pizzaName = []
	const pizzaCount = []

	for (let item in pizzaTotal) {
		pizzaName.push(pizzaTotal[item][0].replace("The ", "").replace(" Pizza", ""));
		pizzaCount.push(pizzaTotal[item][1])
	}

	chart("Penjualan Pizza", pizzaName, pizzaCount, {})
	statistikaDeskriptifFunction(pizzaName, pizzaCount, statisika,"Data Penjualan Jenis Pizza", ["No", "Jenis Pizza", "Quantity"])
}

function categoryBar(categoryData, statisika) {
	const pizzaCategory = Object.keys(categoryData)
	const categoryTotal = []

	for (let item in pizzaCategory) {
		categoryTotal.push(categoryData[pizzaCategory[item]])
	}

	chart("Pendapatan per Kategori", pizzaCategory, categoryTotal, {})
	statistikaDeskriptifFunction(pizzaCategory, categoryTotal, statisika, "Data Pendapatan Per Kategori", ["No", "Kategori Pizza", "Total"])
}

function monthlyBar(monthlyData, statisika) {
	const month = Object.keys(monthlyData)
	const monthlyAvg = []

	for (let item in month) {
		monthlyAvg.push(monthlyData[month[item]])
	}

	chart("Penjualan Perbulan", month, monthlyAvg, {tipe: 'line'})
	statistikaDeskriptifFunction(month, monthlyAvg, statisika, "Data Penjualan Perbulan", ["No", "Bulan", "Total"])
}

function hourlyBar(hourlyData, statisika) {
	const hour = []
	const hourAvg = []

	for (let item in hourlyData) {
		hour.push(hourlyData[item.toString()][0])
		hourAvg.push(hourlyData[item.toString()][1])
	}

	chart("jam", hour, hourAvg, {tipe: 'line', interpolation: 'monotone', pointStyle: false})
	statistikaDeskriptifFunction(hour, hourAvg, statisika, "Data Jam Paling Sering Dikunjungi", ["No", "Waktu", "Quantity"])
}

function pizzaSize(pizzaData, statisika) {
	const size = Object.keys(pizzaData)
	const sizeAvg = []
	
	for (let item in size) {
		sizeAvg.push(pizzaData[size[item]][1])
	}

	chart("ukuran", size, sizeAvg, {tipe: 'pie', interpolation: 'monotone', borderColor: 'transparent'})
	statistikaDeskriptifFunction(size, sizeAvg, statisika, "Data Ukuran Pizza", ["No", "Ukuran", "Quantity"])
}

function histogramBar(histogramData) {
	const range = histogramData["range"]
	const newRange = []
	for (let i = 0; i < range.length - 1; ++i) {
		newRange.push(`${range[i]} ----- ${range[i+1]}`)
	}

	let data = histogramData["data"]
	
	const backgroundColor = Array(range.length).fill('rgba(255, 99, 132, 0.2)');
	const borderColor = Array(range.length).fill('rgba(255, 99, 132, 1)');

	backgroundColor[parseInt(range.length / 2)] = 'rgba(54, 162, 235, 0.2)';
	borderColor[parseInt(range.length / 2)] = 'rgba(54, 162, 235, 1)';

	myChart.destroy()
	myChart = new Chart(canvas.getContext('2d'), {
    type: 'bar',
    data: {
		labels: newRange,
        datasets: [{
            label: '# quantity',
            data: data,
            backgroundColor: backgroundColor,
            borderColor: borderColor,
            borderWidth: 1,
            barPercentage: 1,
            categoryPercentage: 1,
            borderRadius: 5,
        }]
    },
    options: {
        scales: {
            x: {
                ticks: {
					align: 'center',
                    stepSize: 10
                },
                title: {
                  display: true,
                  text: 'price ($)',
                  font: {
                      size: 14
                  }
                }
            }, 
            y: {
                title: {
                  display: true,
                  text: 'quantity',
                  font: {
                      size: 14
                  }
                }
            }
        },
        plugins: {
          legend: {
              display: false,
            },
          tooltip: {
            callbacks: {
              title: (items) => {
                if (!items.length) {
                  return '';
                }
                const item = items[0];
                const x = item.parsed.x;
                const min = x - 0.5;
                const max = x + 0.5;
                return `Price: $${min} - $${max}`;
              }
            }
          }
        }
    }
	});
}



function chart(title, labels, data, { tipe = 'bar', interpolation = 'default', borderColor = '#7340d7', pointStyle = 'circle', scales = {} }) {
	let delayed;

	if(myChart !== undefined) myChart.destroy()
	const chartColors1 = [
		"#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF",
		"#FF9F40", "#C9CBCF", "#FF6B6B", "#6BCB77", "#FFD93D",
		"#845EC2", "#D65DB1", "#FF6F91", "#FF9671", "#FFC75F",
		"#F9F871", "#00C9A7", "#0081CF", "#4D8076", "#B0A8B9",
		"#B39CD0", "#FF8066", "#FF5E78", "#FFD365", "#9AE66E",
		"#2C73D2", "#0089BA", "#F5C7B8", "#A2D2FF", "#F77F00",
		"#F45B69", "#3A86FF", "#8338EC", "#FF006E", "#FB5607"
   	];

	const chartColors2 = [
		'rgba(255, 99, 132, 1)',
      	'rgba(255, 159, 64, 1)',
      	'rgba(255, 205, 86, 1)',
      	'rgba(75, 192, 192, 1)',
      	'rgba(54, 162, 235, 1)',
      	'rgba(153, 102, 255, 1)',
      	'rgba(201, 203, 207, 1)',
	]

	myChart = new Chart(canvas, {
    	type: tipe,
    	data: {
      	labels: labels,
      		datasets: [{
        		label: '# ' + title,
       			data: data,
				borderColor: borderColor,
				pointStyle: pointStyle,
				cubicInterpolationMode: interpolation,
				pointRadius: 6,
				pointHoverRadius: 10,
				backgroundColor: tipe === 'line' ? [borderColor] : chartColors1 
      		}]
    	},
    	options: {
			plugins: { 
				title: {
					display: true,
        			text: title
				}
			},
			animation: {
      			
				onComplete: () => {
        			delayed = true;
				},
      			delay: (context) => {
        			let delay = 0;
        			if (context.type === 'data' && context.mode === 'default' && !delayed) {
          				delay = context.dataIndex * 100 + context.datasetIndex * 100;
        			}
        			return delay;
      			},
				
    		},
     		scales: scales
    	}
  });
}


document.addEventListener('DOMContentLoaded', async (ev) => {
	const mainTitle = document.querySelector(".main-title")

	getSubMenuItem()
	const data = await fetch('/api/result')
	const json = await data.json()
	const pizzaTotal = json["pizza_total"]
	pizzaBar(pizzaTotal["data"], pizzaTotal["statistika-deskriptif"])
	

	const btnPalingBanyakDibeli = document.querySelector('#paling-banyak-dibeli')
	btnPalingBanyakDibeli.addEventListener('click', async (ev) => {
		if(activeMenuID !== ev.currentTarget.id) {
			pizzaBar(pizzaTotal["data"], pizzaTotal["statistika-deskriptif"])

			activeMenuID = btnPalingBanyakDibeli.id
			mainTitle.textContent = btnPalingBanyakDibeli.value
		}
	})

	const btnPendapatanPerKategori = document.querySelector('#pendapatan-per-kategori')
	btnPendapatanPerKategori.addEventListener('click', async (ev) => {
		if(activeMenuID !== ev.currentTarget.id) {
			const data = await fetch('/api/result/perkategori')
			const json = await data.json()
	
			const categoryData = json["pendapatan_perkategori"]
			categoryBar(categoryData["data"], categoryData["statistika-deskriptif"])
			
			activeMenuID = btnPendapatanPerKategori.id
			mainTitle.textContent = btnPendapatanPerKategori.value
		}
	})

	const btnPenjualanPerbulan = document.querySelector('#pendapatan-perbulan')
	btnPenjualanPerbulan.addEventListener('click', async (ev) => {
		if(activeMenuID !== ev.currentTarget.id) {
			const data = await fetch('/api/result/pendapatan-perbulan')
			const json = await data.json()
	
			const monthlyData = json["pendapatan_perbulan"]
			monthlyBar(monthlyData["data"], monthlyData["statistika-deskriptif"])
			
			activeMenuID = btnPenjualanPerbulan.id
			mainTitle.textContent = btnPenjualanPerbulan.value
		}
	})

	const btnJamPalingDikunjungi = document.querySelector('#jam-paling-dikunjungi')
	btnJamPalingDikunjungi.addEventListener('click', async (ev) => {
		if(activeMenuID !== ev.currentTarget.id) {
			const data = await fetch('/api/result/jam-paling-dikunjungi')
			const json = await data.json()
	
			const hourlyData = json["jam_paling_dikunjungi"]
			hourlyBar(hourlyData["data"], hourlyData["statistika-deskriptif"])
			
			activeMenuID = btnJamPalingDikunjungi.id
			mainTitle.textContent = btnJamPalingDikunjungi.value
		}
	})

	const btnDistribusiUkuran = document.querySelector('#distribusi-ukuran')
	btnDistribusiUkuran.addEventListener('click', async (ev) => {
		if(activeMenuID !== ev.currentTarget.id) {
			const data = await fetch('/api/result/distribusi-ukuran')
			const json = await data.json()
	
			const sizeData = json["distribusi_ukuran"]
			pizzaSize(sizeData["data"], sizeData["statistika-deskriptif"])
			
			activeMenuID = btnDistribusiUkuran.id
			mainTitle.textContent = btnDistribusiUkuran.value
		}
	})

	const btnHistogram = document.querySelector('#histogram')
	btnHistogram.addEventListener('click', async (ev) => {
		if(activeMenuID !== ev.currentTarget.id) {
			const data = await fetch('/api/result/histogram')
			const json = await data.json()
	
			const histogramData = json["histogram"]
			histogramBar(histogramData)
			
			activeMenuID = btnHistogram.id
			mainTitle.textContent = btnHistogram.value
		}
	})
})
