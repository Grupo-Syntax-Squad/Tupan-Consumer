from subs import getData
from connRedis import setData, getRedisData

while True:
    response = getData()
    print(response)
    setData(response)
    print(getRedisData(response))
