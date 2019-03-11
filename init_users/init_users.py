from faker import Faker
import random
import string
import pandas as pd


def make_users():
    fake = Faker()

    chars = string.ascii_letters + string.digits
    length = 8
    tags = ['Dogs Ok', 'Cats OK', 'No Pets', 'No Smoking',
            'Furnished', 'Wheelchair Access', 'Quiet', 'Public Traffic',
            'Parking', 'Laundry']

    name = fake.name()
    email = fake.email()
    pwd = ''.join([random.choice(chars) for _ in range(length)])
    mobile = fake.phone_number()
    gender = random.choice(['Male', 'Female'])
    tag = random.choices(tags, k=random.randint(1, 6))

    return {
        "name": name,
        "email": email,
        "password": pwd,
        "gender": gender,
        "mobile": mobile,
        "tag": tag
    }


def main():
    df = pd.DataFrame(columns=['name', 'email', 'password', 'gender', 'mobile', 'tag'])

    for i in range(100):
        dic = make_users()
        series = pd.Series(dic)
        df = df.append(series, ignore_index=True)

    df.to_csv('init_users.csv', index=False)


if __name__ == '__main__':
    main()
