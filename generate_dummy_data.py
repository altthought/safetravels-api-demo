# Author: Alex Culp
# Description: make data to shove into database for testing
# Last Modified: July 13, 2016
# Notes: not really necessary to mess with after first run
import random
from datetime import datetime
import re
import uuid # uuid.uuid4()

UPPER = 1000

user_t = "INSERT INTO users VALUES('{}',{},{})"
company_t = "INSERT INTO company VALUES({},'{}','{}',{},{},'{}')"
coupon_t = "INSERT INTO coupon VALUES({},{},{},'{}',{})"
redeemed_t = "INSERT INTO redeemed VALUES('{}',{},'{}')"

users = [user_t.format(uuid.uuid4(),random.randint(0,1000),random.randint(0,1000)) for num in range(UPPER)]

companies = [company_t.format(num,"Company #{}".format(num),"address for {}".format(num), random.uniform(100,200),random.uniform(100,200), "bio for {}".format(num), "/img/{}.jpg".format(num)) for num in range(UPPER)]

coupons = [coupon_t.format(num,random.randint(0,UPPER), random.randint(0,50),"summary for {}".format(num), 0) for num in range(UPPER)]

user_pool = []
for user in users:
    patt = re.compile(r"[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}")
    found = re.search(patt, user)
    if found:
        user_pool.append(found.group(0))

redeemed = [redeemed_t.format(random.choice(user_pool), random.randint(0,UPPER),str(datetime.now())) for num in range(UPPER)]



# ugly but works and i'm lazy.
with open('dummydata.sql','wt') as f:
    for u in users:
        f.write(u)
        f.write(';\n')
    for c in companies:
        f.write(c)
        f.write(';\n')
    for c in coupons:
        f.write(c)
        f.write(';\n')
    for r in redeemed:
        f.write(r)
        f.write(';\n')

