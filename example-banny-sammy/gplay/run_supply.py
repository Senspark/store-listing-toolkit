#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os, os.path

cmd = 'supply -j ../../Google\ Play\ Android\ Developer-394f15d83386.json -p com.senspark.bannysammy --skip_upload_apk true --skip_upload_images true --skip_upload_screenshots true'
print cmd
os.system(cmd)