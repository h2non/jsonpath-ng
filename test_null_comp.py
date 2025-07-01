#!/usr/bin/env python3

print('None == None:', None == None)
try:
    print('None <= None:', None <= None)
except Exception as e:
    print('None <= None error:', e)
try:
    print('None < None:', None < None)
except Exception as e:
    print('None < None error:', e)
try:
    print('None >= None:', None >= None)
except Exception as e:
    print('None >= None error:', e)
try:
    print('None > None:', None > None)
except Exception as e:
    print('None > None error:', e)
print('None != None:', None != None)