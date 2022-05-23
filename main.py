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
    csvData = pd.read_csv('db/order_list.csv',
                          names=col_names, header=None, delimiter="\t")
    return render_template("order_list.html", data=csvData.to_html())


@app.route('/summary')
def summary():
    # Set The upload HTML template '\templates\order_list.html'
    col_names = ['date', 'chicken', 'egg', 'vegetable', 'pickup_location', 'distribution_center', 'delivery_address', 'order_placed_by',
                 'contact_number', 'comments', 'tusker_name', 'amount']
    data = getOrderListSummary(pd.read_csv(
        'db/order_list.csv', names=col_names, header=None, delimiter="\t"))
    pickUpData = getPickUpSummary(pd.read_csv(
        'db/order_list.csv', names=col_names, header=None, delimiter="\t"))
    return render_template("summary.html", chicken=data[0], egg=data[1], vegetable=data[2], pickUpChickenNewLands=pickUpData[0][0],
                           pickUpChickenChurtonPark=pickUpData[0][1], pickUpChickenLowerHutt=pickUpData[
                               0][2], pickUpEggNewLands=pickUpData[1][0],
                           pickUpEggChurtonPark=pickUpData[1][1], pickUpEggLowerHutt=pickUpData[
                               1][2], pickUpVegeNewLands=pickUpData[2][0],
                           pickUpVegeChurtonPark=pickUpData[2][1], pickUpVegeLowerHutt=pickUpData[2][2])


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


# def getDeliverySummary(csvData):
#     chickenNewlandsOrders = 0
#     chickenChurtonParkOrders = 0
#     chickenLowerHuttOrders = 0
#     chickenCityOrders = 0
#     eggNewlandsOrders = 0
#     eggChurtonParkOrders = 0
#     eggLowerHuttOrders = 0
#     eggCityOrders = 0
#     vegeNewlandsOrders = 0
#     vegeChurtonParkOrders = 0
#     vegeLowerHuttOrders = 0
#     vegeCityOrders = 0

#     # Loop through the Rows
#     for i, row in csvData.iterrows():
#         if i > 0:
#             if int(row['chicken']) > 0 and row['distribution_center'] == 'Newlands':
#                 chickenNewlandsOrders = chickenNewlandsOrders + \
#                     int(row['chicken'])
#     for i, row in csvData.iterrows():
#         if i > 0:
#             if int(row['chicken']) > 0 and row['distribution_center'] == 'Churton Park':
#                 chickenChurtonParkOrders = chickenChurtonParkOrders + \
#                     int(row['chicken'])
#     for i, row in csvData.iterrows():
#         if i > 0:
#             if int(row['chicken']) > 0 and row['distribution_center'] == 'Lower Hutt':
#                 pickUpChickenLowerHuttOrders = pickUpChickenLowerHuttOrders + \
#                     int(row['chicken'])
#     for i, row in csvData.iterrows():
#         if i > 0:
#             if int(row['chicken']) > 0 and row['distribution_center'] == 'City':
#                 pickUpChickenLowerHuttOrders = pickUpChickenLowerHuttOrders + \
#                     int(row['chicken'])

#     for i, row in csvData.iterrows():
#         if i > 0:
#             if int(row['egg']) > 0 and row['distribution_center'] == 'Newlands':
#                 pickUpEggNewlandsOrders = pickUpEggNewlandsOrders + \
#                     int(row['egg'])
#     for i, row in csvData.iterrows():
#         if i > 0:
#             if int(row['egg']) > 0 and row['distribution_center'] == 'Churton Park':
#                 pickUpEggChurtonParkOrders = pickUpEggChurtonParkOrders + \
#                     int(row['egg'])
#     for i, row in csvData.iterrows():
#         if i > 0:
#             if int(row['egg']) > 0 and row['distribution_center'] == 'Lower Hutt':
#                 pickUpEggLowerHuttOrders = pickUpEggLowerHuttOrders + \
#                     int(row['egg'])
#     for i, row in csvData.iterrows():
#         if i > 0:
#             if int(row['egg']) > 0 and row['distribution_center'] == 'City':
#                 pickUpEggLowerHuttOrders = pickUpEggLowerHuttOrders + \
#                     int(row['egg'])

#     for i, row in csvData.iterrows():
#         if i > 0:
#             if int(row['egg']) > 0 and row['distribution_center'] == 'Newlands':
#                 pickUpVegeNewlandsOrders = pickUpVegeNewlandsOrders + \
#                     int(row['vegetable'])
#     for i, row in csvData.iterrows():
#         if i > 0:
#             if int(row['egg']) > 0 and row['distribution_center'] == 'Churton Park':
#                 pickUpVegeChurtonParkOrders = pickUpVegeChurtonParkOrders + \
#                     int(row['vegetable'])
#     for i, row in csvData.iterrows():
#         if i > 0:
#             if int(row['egg']) > 0 and row['distribution_center'] == 'Lower Hutt':
#                 pickUpVegeLowerHuttOrders = pickUpVegeLowerHuttOrders + \
#                     int(row['vegetable'])
#     for i, row in csvData.iterrows():
#         if i > 0:
#             if int(row['egg']) > 0 and row['distribution_center'] == 'City':
#                 pickUpVegeLowerHuttOrders = pickUpVegeLowerHuttOrders + \
#                     int(row['vegetable'])

#     return [[pickUpChickenNewlandsOrders, pickUpChickenChurtonParkOrders, pickUpChickenLowerHuttOrders],
#             [pickUpEggNewlandsOrders, pickUpEggChurtonParkOrders,
#                 pickUpEggLowerHuttOrders],
#             [pickUpVegeNewlandsOrders, pickUpVegeChurtonParkOrders, pickUpVegeLowerHuttOrders]]


if __name__ == "__main__":
    app.run(port=5000)
