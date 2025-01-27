# pip install pycdlib

try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

import pycdlib

iso = pycdlib.PyCdlib()
iso.new(interchange_level=4)

file1 = open("DNS.sh", "rb")
file2 = open("IPTAB.sh", "rb")
filecontent1 = file1.read()
filecontent2 = file2.read()

iso.add_fp(BytesIO(filecontent1), len(filecontent1), '/DNS.SH;1')
iso.add_fp(BytesIO(filecontent2), len(filecontent2), '/IPTAB.SH;1')

iso.write('asd.iso')
iso.close()

file1.close()
file2.close()