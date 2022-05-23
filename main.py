from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd
from os.path import join, dirname, realpath

app = Flask(__name__)

# enable debugging mode
app.config["DEBUG"] = True

# Upload folder
UPLOAD_FOLDER = 'static/files'
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
    col_names = ['date', 'chicken', 'egg', 'vegetable', 'pickup_location', 'delivery_address', 'order_placed_by',
                 'contact_number', 'comments', 'tusker_name', 'amount']
    csvData = pd.read_csv('db/order_list.csv', names=col_names, header=None, delimiter="\t")
    return render_template("order_list.html", data=csvData.to_html())

@app.route('/chicken')
def order_list():
    # Set The upload HTML template '\templates\order_list.html'
    col_names = ['date', 'chicken', 'egg', 'vegetable', 'pickup_location', 'delivery_address', 'order_placed_by',
                 'contact_number', 'comments', 'tusker_name', 'amount']
    csvData = pd.read_csv('db/order_list.csv', names=col_names, header=None, delimiter="\t")
    return render_template("order_list.html", data=csvData.to_html())

# @app.route('/egg')
# def order_list():
#     # Set The upload HTML template '\templates\order_list.html'
#     col_names = ['date', 'chicken', 'egg', 'vegetable', 'pickup_location', 'delivery_address', 'order_placed_by',
#                  'contact_number', 'comments', 'tusker_name', 'amount']
#     csvData = pd.read_csv('db/order_list.csv', names=col_names, header=None, delimiter="\t")
#     return render_template("order_list.html", data=csvData.to_html())

# @app.route('/vegetable')
# def order_list():
#     # Set The upload HTML template '\templates\order_list.html'
#     col_names = ['date', 'chicken', 'egg', 'vegetable', 'pickup_location', 'delivery_address', 'order_placed_by',
#                  'contact_number', 'comments', 'tusker_name', 'amount']
#     csvData = pd.read_csv('db/order_list.csv', names=col_names, header=None, delimiter="\t")
#     return render_template("order_list.html", data=csvData.to_html())

# @app.route('/newlands')
# def order_list():
#     # Set The upload HTML template '\templates\order_list.html'
#     col_names = ['date', 'chicken', 'egg', 'vegetable', 'pickup_location', 'delivery_address', 'order_placed_by',
#                  'contact_number', 'comments', 'tusker_name', 'amount']
#     csvData = pd.read_csv('db/order_list.csv', names=col_names, header=None, delimiter="\t")
#     return render_template("order_list.html", data=csvData.to_html())

# @app.route('/churtonpark')
# def order_list():
#     # Set The upload HTML template '\templates\order_list.html'
#     col_names = ['date', 'chicken', 'egg', 'vegetable', 'pickup_location', 'delivery_address', 'order_placed_by',
#                  'contact_number', 'comments', 'tusker_name', 'amount']
#     csvData = pd.read_csv('db/order_list.csv', names=col_names, header=None, delimiter="\t")
#     return render_template("order_list.html", data=csvData.to_html())

# @app.route('/lowerhutt')
# def order_list():
#     # Set The upload HTML template '\templates\order_list.html'
#     col_names = ['date', 'chicken', 'egg', 'vegetable', 'pickup_location', 'delivery_address', 'order_placed_by',
#                  'contact_number', 'comments', 'tusker_name', 'amount']
#     csvData = pd.read_csv('db/order_list.csv', names=col_names, header=None, delimiter="\t")
#     return render_template("order_list.html", data=csvData.to_html())

# @app.route('/city')
# def order_list():
#     # Set The upload HTML template '\templates\order_list.html'
#     col_names = ['date', 'chicken', 'egg', 'vegetable', 'pickup_location', 'delivery_address', 'order_placed_by',
#                  'contact_number', 'comments', 'tusker_name', 'amount']
#     csvData = pd.read_csv('db/order_list.csv', names=col_names, header=None, delimiter="\t")
#     return render_template("order_list.html", data=csvData.to_html())

# Get the uploaded files
@app.route("/", methods=['POST'])
def uploadFiles():
    # get the uploaded file
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        # set the file path
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        # save the file
        uploaded_file.save(file_path)
        # Initiate parseCSV function to read the data
        parseCSV(file_path)
        return redirect("order_list")


def parseCSV(filePath):
    # CVS Column Names
    col_names = ['date', 'chicken', 'egg', 'vegetable', 'pickup_location', 'distribution_center', 'delivery_address', 'order_placed_by',
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
                print(i, row['date'], row['chicken'], row['egg'], row['vegetable'], row['pickup_location'],
                      row['delivery_address'], row['order_placed_by'], row['contact_number'], row['comments'],
                      row['tusker_name'], row['amount'], )
                fo.writelines(str(row['date']) + "\t" + str(row['chicken']) + "\t" + str(row['egg']) + ",\t" +
                              str(row['vegetable']) + "\t" + str(row['pickup_location']) + "\t" +
                              str(row['delivery_address']) + str(row['distribution_center']) + "\t" +
                              str(row['order_placed_by']) + "\t" + str(row['contact_number']) + "\t" +
                              str(row['comments']) + "\t" + str(row['tusker_name']) + "\t" + str(row['amount']) + "\n")


def generateChickenOrderList(csvData):
    # Loop through the Rows
    with open(os.path.join(app.config['DB'], "order_list.csv"), "w") as fo:
        for i, row in csvData.iterrows():
            if i > 0:
                if int(row['chicken']) > 0:
                    print(i, row['date'], row['chicken'], row['egg'], row['vegetable'], row['pickup_location'],
                          row['delivery_address'], row['order_placed_by'], row['contact_number'], row['comments'],
                          row['tusker_name'], row['amount'], )
                    fo.writelines(str(row['date']) + "\t" + str(row['chicken']) + "\t" + str(row['egg']) + ",\t" +
                                  str(row['vegetable']) + "\t" + str(row['pickup_location']) + "\t" +
                                  str(row['delivery_address']) + "\t" + str(row['distribution_center']) + "\t" + str(row['order_placed_by']) + "\t" +
                                  str(row['contact_number']) + "\t" + str(row['comments']) + "\t" +
                                  str(row['tusker_name']) + "\t" + str(row['amount']) + "\n")


# def generateEggOrderList(csvData):
# def generateVegetableOrderList(csvData):
# def generateNewlandsList(csvData):
# def generateChurtonParkList(csvData):
# def generateLowerHuttList(csvData):
# def generateCityList(csvData):

if __name__ == "__main__":
    app.run(port=5000)
