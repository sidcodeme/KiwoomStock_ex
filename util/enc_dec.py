import cryptocode

enc_key = "asdlfasldkfal;kjq348t98p0ugaekl;jhqea54xvnxdfsgsxdf"
def my_encrypt(str):
    encryptStr = cryptocode.encrypt(str, enc_key)
    print(encryptStr)

def my_decrypt():
    return cryptocode.decrypt("change_your_enc_key", enc_key)

def db_user():
    return cryptocode.decrypt("change_your_enc_key", enc_key)

def db_pass():
    return cryptocode.decrypt("change_your_enc_key", enc_key)

