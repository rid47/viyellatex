from datetime import datetime, timedelta
import pymysql

debug = False

db = pymysql.connect("localhost", "root", "Ds@iot123", "viyellatex")
time_now = datetime.now()
threshold_time = time_now - timedelta(minutes=30)
if debug:
    print(f"Time Now:{time_now}")
    print(f"Threshold Time {threshold_time}")


# Defining blueprint for devices
class Device:

    def __init__(self, device_id):
        self.device_id = device_id

    # Get timestamp of last data received from device
    def get_latest_timestamp(self):
        with db.cursor() as cursor1:
            query_latest_timestamp = "SELECT MAX(last_date) FROM device_data WHERE device_num = %s"
            try:
                cursor1.execute(query_latest_timestamp, self.device_id)
                latest_timestamp = cursor1.fetchone()

                return latest_timestamp
            except Exception as error:
                print(f"Error:{error}")

    # Update iot_device_status column based on threshold
    def update_device_status(self, status):
        with db.cursor() as cursor2:
            query_update_status = "UPDATE device_info SET iot_device_status = %s WHERE device_num = %s" % \
                                  (status, self.device_id)
            if debug:
                print(f"update query: {query_update_status}")
            try:
                cursor2.execute(query_update_status)
                db.commit()
            except Exception as error:
                db.rollback()
                if debug:
                    print(f"Error:{error}")

    def __str__(self):
        return str(self.device_id)


# Fetching total registered device count from DB
with db.cursor() as cursor:
    query = "SELECT device_num FROM device_info"
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        if debug:
            print(f"Query Result: {result}")
    except Exception as e:
        if debug:
            print(f"Error: {e}")


device_list = []  # list to keep device object
for device in result:
    if debug:
        print(device[0])
    device_list.append(Device(device[0]))


for obj in device_list:
    last_data_received = obj.get_latest_timestamp()
    if debug:
        print(f"Last Data for device {obj.device_id} arrived @: {last_data_received}")
    if last_data_received[0] is None:
        if debug:
            print("Update iot_device_status as 0")
        obj.update_device_status(0)
    else:
        if debug:
            print("compare last_data_received with threshold and update")
            print(f"Type of last_data_received is {type(last_data_received[0])}")
        if threshold_time > last_data_received[0]:
            if debug:
                print("IoT Device Offline")
            obj.update_device_status(0)
        else:
            if debug:
                print("IoT Device Online")
            obj.update_device_status(1)







