# MD5 Counter

A simple [Chalice](http://chalice.readthedocs.io/) application that has four API endpoints:

1. `/` - report the number of successful and unsuccessful MD5 calculations
2. `/success` - increment the successful count by 1
3. `/error` - increment the unsuccessful count by 1
4. `/reset` - reset the `success` and `error` counters to `0`

The counter is stored as a DynamoDB table, which is created by the [`createtable.py`](./createtable.py) script.
