"""
TODO:

1. [V] Bar chart = Pizza yang paling banyak dibeli sepanjang tahun
2. [V] Bar chart = Pendapatan untuk per kategori pizza
3. [V] Line chart = Penjualan perbulan (order_date, total_price/quantity)
4. [V] Line chart = jam paling dikunjungi
5. [V] Pie Chart = distribusi ukuran pizza
6. [V] Histogram = persebaran histogram (x: harga, y: quantity)
7. [_] total penjualan (bisa pendapatan tahunan atau jumlah pizza yang terjual)
 
"""

from flask import Flask, jsonify, redirect, render_template, request, url_for
import pandas as pd
import math
import json

app = Flask(__name__)
app.json.sort_keys = False
bulan = ["januari", "februari", "maret", "april", "mei", "juni", "juli", "agustus", "september", "oktober", "november", "desember"]
global_file_result = {
    "file_name": "",
    "data": None,
    "paling-banyak-dibeli": {
        "data": {},
    },
    "pendapatan-per-kategori": {
        "data": {},
    },
    "pendapatan-perbulan": {
        "data": {},
        "statistika-deskriptif": {
            "mean": None,
            "median": None,
            "modus": None,
            "sorted": []
        } 
    },
    "jam-paling-dikunjungi": {
        "data": {},
        "statistika-deskriptif": {
            "mean": None,
            "median": None,
            "modus": None,
            "sorted": []
        } 
    },
    "distribusi-ukuran": {
        "data": {},
        "statistika-deskriptif": {
            "mean": None,
            "median": None,
            "modus": None,
            "sorted": []
        } 
    },
    "histogram": {
        "range": [],
        "data": {},
        "histo_data": {
            "kategori": 'classic',
            "ukuran": 'L',
            "bulan": 12
        }
    }
}

menu = [
    # format nya biar gak lupa
    # [value, label, title label, icon, is default active?]
    ["paling-banyak-dibeli", "Paling Banyak Dibeli", "Pizza yang paling banyak dibeli sepanjang tahun", "fa-cart-shopping", True],
    ["pendapatan-per-kategori", "Pendapatan Per Kategori", "Pendapatan untuk per kategori pizza", "fa-money-bill-trend-up", False],
    ["pendapatan-perbulan", "Pendapatan Perbulan", "Pendapatan perbulan ($)", "fa-calendar-days", False],
    ["jam-paling-dikunjungi", "Jam Paling Dikunjungi", "Jam paling sering dikunjungi", "fa-clock", False],
    ["distribusi-ukuran", "Distribusi Ukuran", "Distribusi ukuran pizza", "fa-chart-simple", False],
    ["histogram", "Persebaran Histrogram", "Histogram Persebaran Harga Pizza L Classic di bulan Desember", "fa-square-poll-horizontal", False],
]

def manual_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def mean(arr):
    total = 0
    count = 0
    for num in arr:
        total += num
        count += 1
    return total / count if count != 0 else 0

def median(arr):
    sorted_arr = manual_sort(arr[:])
    n = len(sorted_arr)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_arr[mid - 1] + sorted_arr[mid]) / 2
    else:
        return sorted_arr[mid]


def modus(arr):
    if len(arr) == 0:
        return None

    frequencyMap = {};
    maxFrequency = 0;
    mostFrequentElement = 0;

    for element in arr:
        element_key = str(element)
        if element_key not in frequencyMap:
            frequencyMap[element_key] = 0
        else: 
            frequencyMap[element_key] += frequencyMap[element_key]
        if element > maxFrequency:
            maxFrequency = frequencyMap[element_key]
            mostFrequentElement = element
    return mostFrequentElement


def to_json(file_result):
    return json.loads(file_result.to_json(orient="records"))

def paling_banyak_dibeli():
    if global_file_result["data"] is not None:
        data= global_file_result["data"][["pizza_name", "quantity"]].values.tolist()
        for item in data:
            key = "_".join(item[0].split(" ")).lower()
            if key in global_file_result["paling-banyak-dibeli"]["data"]:
                global_file_result["paling-banyak-dibeli"]["data"][key][1] += item[1]
            else:
                global_file_result["paling-banyak-dibeli"]["data"][key] = [item[0], item[1]]
       
        minimum = {
            "number": 0,
            "name": ""
        }
        maximum = {
            "number": 0,
            "name": ""
        }

        for key in global_file_result["paling-banyak-dibeli"]["data"]:
            item = global_file_result["paling-banyak-dibeli"]["data"][key]
            if minimum["number"] == 0:
                minimum["number"] = item[1]
                minimum["name"] = item[0]
            elif item[1] < minimum["number"]:
                minimum["number"] = item[1]
                minimum["name"] = item[0]
            elif item[1] > maximum["number"]:
                maximum["number"] = item[1]
                maximum["name"] = item[0]


        array_data_value = []
        for item in global_file_result["paling-banyak-dibeli"]["data"]:
            array_data_value.append(global_file_result["paling-banyak-dibeli"]["data"][item][1])

        global_file_result["paling-banyak-dibeli"]["statistika-deskriptif"] = {
            "sorted": manual_sort(array_data_value),
            "mean": round(mean(array_data_value), 2),
            "median": round(median(array_data_value), 2),
            "modus": round(modus(array_data_value), 2), 
            "minimum": minimum,
            "maximum": maximum
        }

def pendapatan_perkategori():
    if global_file_result["data"] is not None:
        data = global_file_result["data"][["total_price", "pizza_category"]].values.tolist()
        for item in data:
            key = item[1].lower()
            if key in global_file_result["pendapatan-per-kategori"]["data"]:
                global_file_result["pendapatan-per-kategori"]["data"][key] += item[0]
                global_file_result["pendapatan-per-kategori"]["data"][key] = round(global_file_result["pendapatan-per-kategori"]["data"][key], 2) 
            else:
                global_file_result["pendapatan-per-kategori"]["data"][key] = item[0]

        minimum = {
            "number": 0,
            "name": ""
        }
        maximum = {
            "number": 0,
            "name": ""
        }

        for key in global_file_result["pendapatan-per-kategori"]["data"]:
            item = global_file_result["pendapatan-per-kategori"]["data"][key]

            if minimum["number"] == 0:
                minimum["number"] = item
                minimum["name"] = key
            elif item < minimum["number"]:
                minimum["number"] = item
                minimum["name"] = key
            elif item > maximum["number"]:
                maximum["number"] = item
                maximum["name"] = key


        array_data_value = []
        for item in global_file_result["pendapatan-per-kategori"]["data"]:
            array_data_value.append(global_file_result["pendapatan-per-kategori"]["data"][item])

        global_file_result["pendapatan-per-kategori"]["statistika-deskriptif"] = {
            "sorted": manual_sort(array_data_value),
            "mean": round(mean(array_data_value), 2),
            "median": round(median(array_data_value), 2),
            "modus": round(modus(array_data_value), 2),
            "minimum": minimum,
            "maximum": maximum
        }

def pendapatan_perbulan():
    if global_file_result['data'] is not None:
        data = global_file_result["data"][["order_date", "total_price", "quantity"]].values.tolist()

        array_data_value = []
        total_pendapatan_bulan_ini = 0
        jumlah_penjualan = 0
        bulan_saat_ini = bulan[0]

        for item in data:
            idx_key = item[0].month
            key = bulan[int(idx_key) - 1]

            if key != bulan_saat_ini:
                global_file_result["pendapatan-perbulan"]["data"][bulan_saat_ini] = round(total_pendapatan_bulan_ini, 2)
                array_data_value.append(round(total_pendapatan_bulan_ini, 2))
                bulan_saat_ini = key
                total_pendapatan_bulan_ini = 0
            else:
                total_pendapatan_bulan_ini = total_pendapatan_bulan_ini + item[1]
                jumlah_penjualan = jumlah_penjualan + item[2]
        
        if bulan_saat_ini == "desember":
            global_file_result["pendapatan-perbulan"]["data"][bulan_saat_ini] = round(total_pendapatan_bulan_ini, 2)
            array_data_value.append(round(total_pendapatan_bulan_ini, 2))

        minimum = {
            "number": 0,
            "name": ""
        }
        maximum = {
            "number": 0,
            "name": ""
        }

        for key in global_file_result["pendapatan-perbulan"]["data"]:
            item = global_file_result["pendapatan-perbulan"]["data"][key]

            if minimum["number"] == 0:
                minimum["number"] = item
                minimum["name"] = key
            elif item < minimum["number"]:
                minimum["number"] = item
                minimum["name"] = key
            elif item > maximum["number"]:
                maximum["number"] = item
                maximum["name"] = key

        
        global_file_result["pendapatan-perbulan"]["statistika-deskriptif"] = {
            "sorted": manual_sort(array_data_value),
            "mean": round(mean(array_data_value), 2),
            "median": round(median(array_data_value), 2),
            "modus": round(modus(array_data_value), 2), 
            "minimum": minimum,
            "maximum": maximum
        }
        
def jam_paling_dikunjungi():
    if global_file_result["data"] is not None:
        data = global_file_result["data"]["order_time"].tolist()
        for item in data:
            key = item.hour
            if key in global_file_result["jam-paling-dikunjungi"]["data"]:
                global_file_result["jam-paling-dikunjungi"]["data"][key][1] += 1 
            else:
                global_file_result["jam-paling-dikunjungi"]["data"][key] = [f"{item.hour}.00", 1]

        minimum = {
            "number": 0,
            "name": ""
        }
        maximum = {
            "number": 0,
            "name": ""
        }

        for key in global_file_result["jam-paling-dikunjungi"]["data"]:
            item = global_file_result["jam-paling-dikunjungi"]["data"][key]

            if minimum["number"] == 0:
                minimum["number"] = item[1]
                minimum["name"] = item[0]
            elif item[1] < minimum["number"]:
                minimum["number"] = item[1]
                minimum["name"] = item[0]
            elif item[1] > maximum["number"]:
                maximum["number"] = item[1]
                maximum["name"] = item[0]

        array_data_value = []
        for item in global_file_result["jam-paling-dikunjungi"]["data"]:
            array_data_value.append(global_file_result["jam-paling-dikunjungi"]["data"][item][1])

        global_file_result["jam-paling-dikunjungi"]["statistika-deskriptif"] = {
            "sorted": manual_sort(array_data_value),
            # "mean": round(mean(array_data_value), 2),
            # "median": round(median(array_data_value), 2),
            # "modus": round(modus(array_data_value), 2),
            "minimum": minimum,
            "maximum": maximum
        }
        

def distribusi_ukuran():
    if global_file_result["data"] is not None:
        data= global_file_result["data"]["pizza_size"].tolist()
        for item in data:
            key = item
            if key in global_file_result["distribusi-ukuran"]["data"]:
                global_file_result["distribusi-ukuran"]["data"][key][1] += 1
            else:
                global_file_result["distribusi-ukuran"]["data"][key] = [item, 1]
       
        minimum = {
            "number": 0,
            "name": ""
        }
        maximum = {
            "number": 0,
            "name": ""
        }

        for key in global_file_result["distribusi-ukuran"]["data"]:
            item = global_file_result["distribusi-ukuran"]["data"][key]

            if minimum["number"] == 0:
                minimum["number"] = item[1]
                minimum["name"] = item[0]
            elif item[1] < minimum["number"]:
                minimum["number"] = item[1]
                minimum["name"] = item[0]
            elif item[1] > maximum["number"]:
                maximum["number"] = item[1]
                maximum["name"] = item[0]

        array_data_value = []
        for item in global_file_result["distribusi-ukuran"]["data"]:
            array_data_value.append(global_file_result["distribusi-ukuran"]["data"][item][1])

        global_file_result["distribusi-ukuran"]["statistika-deskriptif"] = {
            "sorted": manual_sort(array_data_value),
            # "mean": round(mean(array_data_value), 2),
            # "median": round(median(array_data_value), 2),
            # "modus": round(modus(array_data_value), 2),
            "minimum": minimum,
            "maximum": maximum
        }


def histogram(kategori, ukuran, bulan):
    if global_file_result["data"] is not None:
        global_file_result["histogram"]["range"] = []
        global_file_result["histogram"]["data"] = {}

        data = global_file_result["data"][["unit_price", "pizza_name", "order_date", "pizza_size", "pizza_category"]].values.tolist()
        minimum = 0
        maximum = 0
        length = 0

        all_prices = []
        for item in data:
            if item[2].month == int(bulan) and item[3] == ukuran.upper() and item[4].lower() == kategori:
                all_prices.append(item[0])
                length += 1
                if minimum == 0:
                    minimum = item[0]
                elif item[0] < minimum:
                    minimum = item[0]
                elif item[0] > maximum:
                    maximum = item[0]

        print(maximum, minimum)

        k = 1 + 3.3 * math.log10(length)
        divide = round(k)
        # range_margin = 0.01
        ranged = maximum - minimum
        ranged_per_item = round(ranged/k)

        ondoted = 0;
        while ranged_per_item == 0:
            ondoted += 1
            ranged_per_item = round(ranged/k, ondoted)

        print(ranged_per_item, divide, k, length)
        print(kategori, ukuran, bulan)

        price = minimum
        for i in range(0, divide+1):
            global_file_result["histogram"]["range"].append(price)
            global_file_result["histogram"]["data"][str(price)] = []
            price += ranged_per_item

        for item in data:
            if item[2].month == int(bulan) and item[3] == ukuran.upper() and item[4].lower() == kategori:
                for i in range(0, divide):
                    data_item = global_file_result["histogram"]["range"]
                    key = str(data_item[i])
                    if i == 0 and item[0] >= (data_item[i]) and item[0] <= data_item[i+1]:
                        if key not in global_file_result["histogram"]["data"]:
                            global_file_result["histogram"]["data"][key] = []

                        # if item[1] not in global_file_result["histogram"]["data"][key]:
                        global_file_result["histogram"]["data"][key].append(item[1])


                    elif item[0] >= (data_item[i]) and item[0] <= data_item[i+1]:
                        if key not in global_file_result["histogram"]["data"]:
                            global_file_result["histogram"]["data"][key] = []

                        # if item[1] not in global_file_result["histogram"]["data"][key]:
                        global_file_result["histogram"]["data"][key].append(item[1])


@app.route('/', methods=["GET", "POST"])
def main():
    return render_template('index.html')
    
@app.route('/result', methods=["GET"])
def result():
    if global_file_result["data"] is None:
        return redirect("/")
    return render_template('result.html', menu_sidebar=menu, file_name=global_file_result["file_name"])

@app.route('/api/result', methods=["GET", "POST"])
def home():
    if request.method == "GET":
        if global_file_result["data"] is None:
            return {}
        return jsonify(
            pizza_total=global_file_result["paling-banyak-dibeli"]
        )
    else:
        if global_file_result["data"] is not None:
            return jsonify(
                pizza_total=global_file_result["pizza_total"],
            )
        global_file_result["data"] = None
        file = request.files['csv-file']
        global_file_result["file_name"] = file.filename
        byte = file.read()
        file_result = pd.read_excel(byte)
        global_file_result["data"] = file_result

        paling_banyak_dibeli()
        return redirect('/api/result')

@app.route('/api/result/perkategori', methods=['GET'])
def perkategori_page():
    if global_file_result['data'] is None:
        return redirect('/api/result')
    
    if not global_file_result['pendapatan-per-kategori']['data']:
        pendapatan_perkategori();
        return jsonify(pendapatan_perkategori=global_file_result['pendapatan-per-kategori'])
    return jsonify(pendapatan_perkategori=global_file_result['pendapatan-per-kategori'])

@app.route('/api/result/pendapatan-perbulan', methods=['GET'])
def pendapatan_perbulan_page():
    if global_file_result['data'] is None:
        return redirect('/api/result')
    
    if not global_file_result['pendapatan-perbulan']['data']:
        pendapatan_perbulan();
        return jsonify(pendapatan_perbulan=global_file_result['pendapatan-perbulan'])
    return jsonify(pendapatan_perbulan=global_file_result['pendapatan-perbulan'])

@app.route('/api/result/jam-paling-dikunjungi', methods=['GET'])
def jam_paling_dikunjungi_page():
    if global_file_result['data'] is None:
        return redirect('/api/result')
    
    if not global_file_result['jam-paling-dikunjungi']['data']:
        jam_paling_dikunjungi();
        return jsonify(jam_paling_dikunjungi=global_file_result['jam-paling-dikunjungi'])
    return jsonify(jam_paling_dikunjungi=global_file_result['jam-paling-dikunjungi'])

@app.route('/api/result/distribusi-ukuran', methods=['GET'])
def distribusi_ukuran_page():
    if global_file_result['data'] is None:
        return redirect('/api/result')
    
    if not global_file_result['distribusi-ukuran']['data']:
        distribusi_ukuran();
        return jsonify(distribusi_ukuran=global_file_result['distribusi-ukuran'])
    return jsonify(distribusi_ukuran=global_file_result['distribusi-ukuran'])

@app.route('/api/result/histogram', methods=['GET', 'POST'])
def histogram_page():
    if global_file_result['data'] is None:
        return redirect('/api/result')
   
    histo_data = global_file_result['histogram']['histo_data']
    if request.method == 'GET':
        histogram(histo_data['kategori'], histo_data['ukuran'], histo_data['bulan'])
        global_file_result['histogram']['histo_data'] = histo_data
        
    else:
        histo_data['ukuran'] = request.form['ukuran']
        histo_data['kategori'] = request.form['kategori']
        histo_data['bulan'] = request.form['bulan']
        histogram(histo_data['kategori'], histo_data['ukuran'], histo_data['bulan'])

        global_file_result['histogram']['histo_data'] = histo_data
    
    return jsonify(histogram=global_file_result['histogram'], title=f"Histogram Persebaran Harga Pizza {histo_data['ukuran']} {histo_data['kategori']} di bulan {bulan[int(histo_data['bulan']) - 1]}")

    # if len(global_file_result['histogram']['range']) == 0:
        # return jsonify(histogram=global_file_result['histogram'])



if __name__ == '__main__':
    app.run(debug=True)
