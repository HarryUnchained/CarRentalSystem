import time
import requests
import math
import random

from Admin import Admin


class Login:
    def __init__(self, cursor):
        self.cursor = cursor

    def authenticate(self, username, password):
        query = "SELECT * FROM Admin WHERE Username = ? AND Password = ?"
        self.cursor.execute(query, username, password)
        user = self.cursor.fetchone()
        user_name = user[1]
        user_pass = user[2]
        user_is_master = user[3]
        user_no = user[4]

        if user_name == username and user_pass == password:
            print("You have received an OTP at the Whatsapp number: ", user_no)

            for i in range(1, 6):
                otp = self.generate_otp()
                self.send_otp_message(phone_number=user_no, otp=otp)
                user_otp = input("Enter OTP received via Whatsapp: ")
                if user_otp == otp:
                    print(f"{username} Admin logged in successfully!")
                    time.sleep(1)
                    admin = Admin(cursor=self.cursor, is_master=user_is_master)
                    admin.main_menu()
                else:
                    print(f"Invalid OTP. Please try again. You have {5 - i} attempts remaining.")
        else:
            print("Username or Password doesn't match")

    @staticmethod
    def generate_otp():
        digits = "0123456789"
        otp = ""
        for i in range(4):
            otp += digits[math.floor(random.random() * 10)]
        return otp

    @staticmethod
    def send_otp_message(phone_number, otp):
        url = "https://api.ultramsg.com/instance50555/messages/chat"

        payload = f"token=96j3u1ceym5d9r92&to={phone_number}&body=OTP = {otp}"
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        try:
            response = requests.post(url, data=payload, headers=headers)
            print(response.text)
            if response.status_code == 200:
                print('WhatsApp OTP message sent successfully!')
            else:
                print('Failed to send WhatsApp OTP message.')
        except requests.RequestException as e:
            print('An error occurred:', str(e))
