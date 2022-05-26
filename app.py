from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd
from os.path import join, dirname, realpath

app = Flask(__name__)

# enable debugging mode
app.config["DEBUG"] = True

# Upload folder
UPLOAD_FOLDER = 'uploads/files'
DB = 'db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DB'] = DB


# Root URL
@app.route('/')
def index():
    # Set The upload HTML template '\templates\index.html'
    return render_template('index.html')


@app.route('/order_list')
def order_list():
    # Set The upload HTML template '\templates\order_list.html'
    col_names = ['date', 'chicken', 'egg', 'vegetable', 'pickup_location', 'delivery_address', 'distribution_center', 'order_placed_by',
                 'contact_number', 'comments', 'tusker_name', 'amount']
    csvData = pd.read_csv('db/order_list.csv',names=col_names, header=None, delimiter="\t")

    return render_template("order_list.html", data=csvData.to_html())

@app.route('/pickup')
def pickup_order_list():
    # Set The upload HTML template '\templates\order_list.html'
    col_names = ['date', 'chicken', 'egg', 'vegetable', 'pickup_location', 'delivery_address', 'distribution_center', 'order_placed_by',
                 'contact_number', 'comments', 'tusker_name', 'amount']

    generateNewlandsPickUpOrderList(pd.read_csv('db/order_list.csv', names=col_names, header=None, delimiter="\t"))
    generateChurtonParkPickUpOrderList(pd.read_csv('db/order_list.csv', names=col_names, header=None, delimiter="\t"))
    generateLowerHuttPickUpOrderList(pd.read_csv('db/order_list.csv', names=col_names, header=None, delimiter="\t"))

    newlandsPickUpData = pd.read_csv('db/newlands_pickup_order_list.csv', names=col_names, header=None, delimiter="\t")
    churtonParkPickUpData = pd.read_csv('db/churtonpark_pickup_order_list.csv', names=col_names, header=None, delimiter="\t")
    lowerHuttPickUpData = pd.read_csv('db/lowerhutt_pickup_order_list.csv', names=col_names, header=None, delimiter="\t")

    return render_template("pickup_order_list.html", newlandsData=newlandsPickUpData.to_html(), churtonParkData=churtonParkPickUpData.to_html(),
     lowerHuttData=lowerHuttPickUpData.to_html())

@app.route('/delivery')
def delivery_order_list():
    # Set The upload HTML template '\templates\order_list.html'
    col_names = ['date', 'chicken', 'egg', 'vegetable', 'pickup_location', 'delivery_address', 'distribution_center', 'order_placed_by',
                 'contact_number', 'comments', 'tusker_name', 'amount']

    generateNewlandsDeliveryOrderList(pd.read_csv('db/order_list.csv', names=col_names, header=None, delimiter="\t"))
    generateChurtonParkDeliveryOrderList(pd.read_csv('db/order_list.csv', names=col_names, header=None, delimiter="\t"))
    generateLowerHuttDeliveryOrderList(pd.read_csv('db/order_list.csv', names=col_names, header=None, delimiter="\t"))
    generateCityDeliveryOrderList(pd.read_csv('db/order_list.csv', names=col_names, header=None, delimiter="\t"))
    
    newlandsDeliveryData = pd.read_csv('db/newlands_delivery_order_list.csv', names=col_names, header=None, delimiter="\t")
    churtonParkDeliveryData = pd.read_csv('db/churtonpark_delivery_order_list.csv', names=col_names, header=None, delimiter="\t")
    lowerHuttDeliveryData = pd.read_csv('db/lowerhutt_delivery_order_list.csv', names=col_names, header=None, delimiter="\t")
    cityDeliveryData = pd.read_csv('db/city_delivery_order_list.csv', names=col_names, header=None, delimiter="\t")

    return render_template("delivery_order_list.html", newlandsData=newlandsDeliveryData.to_html(), churtonParkData=churtonParkDeliveryData.to_html(),
     lowerHuttData=lowerHuttDeliveryData.to_html(), cityData=cityDeliveryData.to_html())


@app.route('/summary')
def summary():
    # Set The upload HTML template '\templates\order_list.html'
    col_names = ['date', 'chicken', 'egg', 'vegetable', 'pickup_location', 'delivery_address', 'distribution_center', 'order_placed_by',
                 'contact_number', 'comments', 'tusker_name', 'amount']
    data = getOrderListSummary(pd.read_csv(
        'db/order_list.csv', names=col_names, header=None, delimiter="\t"))
    pickUpData = getPickUpSummary(pd.read_csv(
        'db/order_list.csv', names=col_names, header=None, delimiter="\t"))
    deliveryData = getDeliverySummary(pd.read_csv(
        'db/order_list.csv', names=col_names, header=None, delimiter="\t"))

    return render_template("summary.html", chicken=data[0], egg=data[1], vegetable=data[2], pickUpChickenNewLands=pickUpData[0][0],
                           pickUpChickenChurtonPark=pickUpData[0][1], pickUpChickenLowerHutt=pickUpData[0][2], 
                           pickUpEggNewLands=pickUpData[1][0],pickUpEggChurtonPark=pickUpData[1][1], 
                           pickUpEggLowerHutt=pickUpData[1][2], pickUpVegeNewLands=pickUpData[2][0],
                           pickUpVegeChurtonPark=pickUpData[2][1], pickUpVegeLowerHutt=pickUpData[2][2], 
                           chickenNewLands=deliveryData[0][0],chickenChurtonPark=deliveryData[0][1], 
                           chickenLowerHutt=deliveryData[0][2], chickenCity=deliveryData[0][3], 
                           eggNewLands=deliveryData[1][0], eggChurtonPark=deliveryData[1][1], 
                           eggLowerHutt=deliveryData[1][2], eggCity=deliveryData[1][3], 
                           vegeNewLands=deliveryData[2][0], vegeChurtonPark=deliveryData[2][1], 
                           vegeLowerHutt=deliveryData[2][2], vegeCity=deliveryData[2][3])


# Upload the order list csv
@app.route("/", methods=['POST'])
def uploadFiles():
    # get the uploaded file
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        # set the file path
        file_path = os.path.join(
            app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        # save the file
        uploaded_file.save(file_path)
        # Initiate parseCSV function to read the data
        parseCSV(file_path)
        return redirect("summary")


def parseCSV(filePath):
    # CVS Column Names
    col_names = ['date', 'chicken', 'egg', 'vegetable', 'pickup_location', 'delivery_address', 'distribution_center', 'order_placed_by',
                 'contact_number', 'comments', 'tusker_name', 'amount']
    # Use Pandas to parse the CSV file
    csvData = pd.read_csv(filePath, names=col_names, header=None)
    # Send csvData to print the order list
    generateOrderList(csvData)


def generateOrderList(csvData):
    # Loop through the Rows
    with open(os.path.join(app.config['DB'], "order_list.csv"), "w") as fo:
        for i, row in csvData.iterrows():
            if i > 0:

                fo.writelines(str(row['date']) + "\t" + str(row['chicken']) + "\t" + str(row['egg']) + "\t" +
                              str(row['vegetable']) + "\t" + str(row['pickup_location']) + "\t" +
                              str(row['delivery_address']) + "\t" + str(row['distribution_center']) + "\t" +
                              str(row['order_placed_by']) + "\t" + str(row['contact_number']) + "\t" +
                              str(row['comments']) + "\t" + str(row['tusker_name']) + "\t" + str(row['amount']) + "\n")


def generateNewlandsPickUpOrderList(csvData):
    # Loop through the Rows
    with open(os.path.join(app.config['DB'], "newlands_pickup_order_list.csv"), "w") as fo:
        for i, row in csvData.iterrows():
            if i > 0:
                if row['pickup_location'] == 'Newlands':
                    fo.writelines(str(row['date']) + "\t" + str(row['chicken']) + "\t" + str(row['egg']) + "\t" +
                                str(row['vegetable']) + "\t" + str(row['pickup_location']) + "\t" +
                                str(row['delivery_address']) + "\t" + str(row['distribution_center']) + "\t" +
                                str(row['order_placed_by']) + "\t" + str(row['contact_number']) + "\t" +
                                str(row['comments']) + "\t" + str(row['tusker_name']) + "\t" + str(row['amount']) + "\n")

def generateChurtonParkPickUpOrderList(csvData):
    # Loop through the Rows
    with open(os.path.join(app.config['DB'], "churtonpark_pickup_order_list.csv"), "w") as fo:
        for i, row in csvData.iterrows():
            if i > 0:
                if row['pickup_location'] == 'Churton Park':
                    fo.writelines(str(row['date']) + "\t" + str(row['chicken']) + "\t" + str(row['egg']) + "\t" +
                                str(row['vegetable']) + "\t" + str(row['pickup_location']) + "\t" +
                                str(row['delivery_address']) + "\t" + str(row['distribution_center']) + "\t" +
                                str(row['order_placed_by']) + "\t" + str(row['contact_number']) + "\t" +
                                str(row['comments']) + "\t" + str(row['tusker_name']) + "\t" + str(row['amount']) + "\n")

def generateLowerHuttPickUpOrderList(csvData):
    # Loop through the Rows
    with open(os.path.join(app.config['DB'], "lowerhutt_pickup_order_list.csv"), "w") as fo:
        for i, row in csvData.iterrows():
            if i > 0:
                if row['pickup_location'] == 'Lower Hutt':
                    fo.writelines(str(row['date']) + "\t" + str(row['chicken']) + "\t" + str(row['egg']) + "\t" +
                                str(row['vegetable']) + "\t" + str(row['pickup_location']) + "\t" +
                                str(row['delivery_address']) + "\t" + str(row['distribution_center']) + "\t" +
                                str(row['order_placed_by']) + "\t" + str(row['contact_number']) + "\t" +
                                str(row['comments']) + "\t" + str(row['tusker_name']) + "\t" + str(row['amount']) + "\n")

def generateNewlandsDeliveryOrderList(csvData):
    # Loop through the Rows
    with open(os.path.join(app.config['DB'], "newlands_delivery_order_list.csv"), "w") as fo:
        for i, row in csvData.iterrows():
            if i > 0:
                if row['distribution_center'] == 'Newlands':
                    fo.writelines(str(row['date']) + "\t" + str(row['chicken']) + "\t" + str(row['egg']) + "\t" +
                                str(row['vegetable']) + "\t" + str(row['pickup_location']) + "\t" +
                                str(row['delivery_address']) + "\t" + str(row['distribution_center']) + "\t" +
                                str(row['order_placed_by']) + "\t" + str(row['contact_number']) + "\t" +
                                str(row['comments']) + "\t" + str(row['tusker_name']) + "\t" + str(row['amount']) + "\n")

def generateChurtonParkDeliveryOrderList(csvData):
    # Loop through the Rows
    with open(os.path.join(app.config['DB'], "churtonpark_delivery_order_list.csv"), "w") as fo:
        for i, row in csvData.iterrows():
            if i > 0:
                if row['distribution_center'] == 'Churton Park':
                    fo.writelines(str(row['date']) + "\t" + str(row['chicken']) + "\t" + str(row['egg']) + "\t" +
                                str(row['vegetable']) + "\t" + str(row['pickup_location']) + "\t" +
                                str(row['delivery_address']) + "\t" + str(row['distribution_center']) + "\t" +
                                str(row['order_placed_by']) + "\t" + str(row['contact_number']) + "\t" +
                                str(row['comments']) + "\t" + str(row['tusker_name']) + "\t" + str(row['amount']) + "\n")

def generateLowerHuttDeliveryOrderList(csvData):
    # Loop through the Rows
    with open(os.path.join(app.config['DB'], "lowerhutt_delivery_order_list.csv"), "w") as fo:
        for i, row in csvData.iterrows():
            if i > 0:
                if row['distribution_center'] == 'Lower Hutt':
                    fo.writelines(str(row['date']) + "\t" + str(row['chicken']) + "\t" + str(row['egg']) + "\t" +
                                str(row['vegetable']) + "\t" + str(row['pickup_location']) + "\t" +
                                str(row['delivery_address']) + "\t" + str(row['distribution_center']) + "\t" +
                                str(row['order_placed_by']) + "\t" + str(row['contact_number']) + "\t" +
                                str(row['comments']) + "\t" + str(row['tusker_name']) + "\t" + str(row['amount']) + "\n")

def generateCityDeliveryOrderList(csvData):
    # Loop through the Rows
    with open(os.path.join(app.config['DB'], "city_delivery_order_list.csv"), "w") as fo:
        for i, row in csvData.iterrows():
            if i > 0:
                if row['distribution_center'] == 'City':
                    fo.writelines(str(row['date']) + "\t" + str(row['chicken']) + "\t" + str(row['egg']) + "\t" +
                                str(row['vegetable']) + "\t" + str(row['pickup_location']) + "\t" +
                                str(row['delivery_address']) + "\t" + str(row['distribution_center']) + "\t" +
                                str(row['order_placed_by']) + "\t" + str(row['contact_number']) + "\t" +
                                str(row['comments']) + "\t" + str(row['tusker_name']) + "\t" + str(row['amount']) + "\n")

def getOrderListSummary(csvData):
    chickenOrders = 0
    eggOrders = 0
    vegeOrders = 0

    # Loop through the Rows
    for i, row in csvData.iterrows():
        if i > 0:
            if int(row['chicken']) > 0:
                chickenOrders = chickenOrders + int(row['chicken'])

    for i, row in csvData.iterrows():
        if i > 0:
            if int(row['egg']) > 0:
                eggOrders = eggOrders + int(row['egg'])

    for i, row in csvData.iterrows():
        if i > 0:
            if int(row['vegetable']) > 0:
                vegeOrders = vegeOrders + int(row['vegetable'])

    return [chickenOrders, eggOrders, vegeOrders]


def getPickUpSummary(csvData):
    pickUpChickenNewlandsOrders = 0
    pickUpChickenChurtonParkOrders = 0
    pickUpChickenLowerHuttOrders = 0
    pickUpEggNewlandsOrders = 0
    pickUpEggChurtonParkOrders = 0
    pickUpEggLowerHuttOrders = 0
    pickUpVegeNewlandsOrders = 0
    pickUpVegeChurtonParkOrders = 0
    pickUpVegeLowerHuttOrders = 0

    # Loop through the Rows
    for i, row in csvData.iterrows():
        if i > 0:
            if int(row['chicken']) > 0 and row['pickup_location'] == 'Newlands':
                pickUpChickenNewlandsOrders = pickUpChickenNewlandsOrders + \
                    int(row['chicken'])
    for i, row in csvData.iterrows():
        if i > 0:
            if int(row['chicken']) > 0 and row['pickup_location'] == 'Churton Park':
                pickUpChickenChurtonParkOrders = pickUpChickenChurtonParkOrders + \
                    int(row['chicken'])
    for i, row in csvData.iterrows():
        if i > 0:
            if int(row['chicken']) > 0 and row['pickup_location'] == 'Lower Hutt':
                pickUpChickenLowerHuttOrders = pickUpChickenLowerHuttOrders + \
                    int(row['chicken'])

    for i, row in csvData.iterrows():
        if i > 0:
            if int(row['egg']) > 0 and row['pickup_location'] == 'Newlands':
                pickUpEggNewlandsOrders = pickUpEggNewlandsOrders + \
                    int(row['egg'])
    for i, row in csvData.iterrows():
        if i > 0:
            if int(row['egg']) > 0 and row['pickup_location'] == 'Churton Park':
                pickUpEggChurtonParkOrders = pickUpEggChurtonParkOrders + \
                    int(row['egg'])
    for i, row in csvData.iterrows():
        if i > 0:
            if int(row['egg']) > 0 and row['pickup_location'] == 'Lower Hutt':
                pickUpEggLowerHuttOrders = pickUpEggLowerHuttOrders + \
                    int(row['egg'])

    for i, row in csvData.iterrows():
        if i > 0:
            if int(row['egg']) > 0 and row['pickup_location'] == 'Newlands':
                pickUpVegeNewlandsOrders = pickUpVegeNewlandsOrders + \
                    int(row['vegetable'])
    for i, row in csvData.iterrows():
        if i > 0:
            if int(row['egg']) > 0 and row['pickup_location'] == 'Churton Park':
                pickUpVegeChurtonParkOrders = pickUpVegeChurtonParkOrders + \
                    int(row['vegetable'])
    for i, row in csvData.iterrows():
        if i > 0:
            if int(row['egg']) > 0 and row['pickup_location'] == 'Lower Hutt':
                pickUpVegeLowerHuttOrders = pickUpVegeLowerHuttOrders + \
                    int(row['vegetable'])

    return [[pickUpChickenNewlandsOrders, pickUpChickenChurtonParkOrders, pickUpChickenLowerHuttOrders],
            [pickUpEggNewlandsOrders, pickUpEggChurtonParkOrders,
                pickUpEggLowerHuttOrders],
            [pickUpVegeNewlandsOrders, pickUpVegeChurtonParkOrders, pickUpVegeLowerHuttOrders]]


def getDeliverySummary(csvData):
    chickenNewlandsOrders = 0
    chickenChurtonParkOrders = 0
    chickenLowerHuttOrders = 0
    chickenCityOrders = 0
    eggNewlandsOrders = 0
    eggChurtonParkOrders = 0
    eggLowerHuttOrders = 0
    eggCityOrders = 0
    vegeNewlandsOrders = 0
    vegeChurtonParkOrders = 0
    vegeLowerHuttOrders = 0
    vegeCityOrders = 0

    # Loop through the Rows
    for i, row in csvData.iterrows():
        if i > 0:
            if int(row['chicken']) > 0 and row['distribution_center'] == 'Newlands':
                chickenNewlandsOrders = chickenNewlandsOrders + \
                    int(row['chicken'])
    for i, row in csvData.iterrows():
        if i > 0:
            if int(row['chicken']) > 0 and row['distribution_center'] == 'Churton Park':
                chickenChurtonParkOrders = chickenChurtonParkOrders + \
                    int(row['chicken'])
    for i, row in csvData.iterrows():
        if i > 0:
            if int(row['chicken']) > 0 and row['distribution_center'] == 'Lower Hutt':
                chickenLowerHuttOrders = chickenLowerHuttOrders + \
                    int(row['chicken'])
    for i, row in csvData.iterrows():
        if i > 0:
            if int(row['chicken']) > 0 and row['distribution_center'] == 'City':
                chickenCityOrders = chickenCityOrders + \
                    int(row['chicken'])

    for i, row in csvData.iterrows():
        if i > 0:
            if int(row['egg']) > 0 and row['distribution_center'] == 'Newlands':
                eggNewlandsOrders = eggNewlandsOrders + \
                    int(row['egg'])
    for i, row in csvData.iterrows():
        if i > 0:
            if int(row['egg']) > 0 and row['distribution_center'] == 'Churton Park':
                eggChurtonParkOrders = eggChurtonParkOrders + \
                    int(row['egg'])
    for i, row in csvData.iterrows():
        if i > 0:
            if int(row['egg']) > 0 and row['distribution_center'] == 'Lower Hutt':
                eggLowerHuttOrders = eggLowerHuttOrders + \
                    int(row['egg'])
    for i, row in csvData.iterrows():
        if i > 0:
            if int(row['egg']) > 0 and row['distribution_center'] == 'City':
                eggCityOrders = eggCityOrders + \
                    int(row['egg'])

    for i, row in csvData.iterrows():
        if i > 0:
            if int(row['egg']) > 0 and row['distribution_center'] == 'Newlands':
                vegeNewlandsOrders = vegeNewlandsOrders + \
                    int(row['vegetable'])
    for i, row in csvData.iterrows():
        if i > 0:
            if int(row['egg']) > 0 and row['distribution_center'] == 'Churton Park':
                vegeChurtonParkOrders = vegeChurtonParkOrders + \
                    int(row['vegetable'])
    for i, row in csvData.iterrows():
        if i > 0:
            if int(row['egg']) > 0 and row['distribution_center'] == 'Lower Hutt':
                vegeLowerHuttOrders = vegeLowerHuttOrders + \
                    int(row['vegetable'])
    for i, row in csvData.iterrows():
        if i > 0:
            if int(row['egg']) > 0 and row['distribution_center'] == 'City':
                vegeCityOrders = vegeCityOrders + \
                    int(row['vegetable'])

    return [[chickenNewlandsOrders, chickenChurtonParkOrders, chickenLowerHuttOrders, chickenCityOrders],
            [eggNewlandsOrders, eggChurtonParkOrders,
                eggLowerHuttOrders, eggCityOrders],
            [vegeNewlandsOrders, vegeChurtonParkOrders, vegeLowerHuttOrders, vegeCityOrders]]


if __name__ == "__main__":
    app.run(port=5000)
