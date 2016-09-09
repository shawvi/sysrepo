#!/usr/bin/env python

__author__ = "Mislav Novakovic <mislav.novakovic@sartura.hr>"
__copyright__ = "Copyright 2016, Deutsche Telekom AG"
__license__ = "Apache 2.0"

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import libsysrepoPython2 as sr
import sys

def print_value(value):
    print value.xpath() + " ",

    if (value.type() == sr.SR_CONTAINER_T):
        print "(container)"
    elif (value.type() == sr.SR_CONTAINER_PRESENCE_T):
        print "(container)"
    elif (value.type() == sr.SR_LIST_T):
        print "(list instance)"
    elif (value.type() == sr.SR_STRING_T):
        print "= " + value.data().get_string()
    elif (value.type() == sr.SR_BOOL_T):
        if (value.data().get_bool()):
            print "= true"
        else:
            print "= false"
    elif (value.type() == sr.SR_ENUM_T):
        print "= " + value.data().get_enum()
    elif (value.type() == sr.SR_UINT8_T):
        print "= " + repr(value.data().get_uint8())
    elif (value.type() == sr.SR_UINT16_T):
        print "= " + repr(value.data().get_uint16())
    elif (value.type() == sr.SR_UINT32_T):
        print "= " + repr(value.data().get_uint32())
    elif (value.type() == sr.SR_UINT64_T):
        print "= " + repr(value.data().get_uint64())
    elif (value.type() == sr.SR_INT8_T):
        print "= " + repr(value.data().get_int8())
    elif (value.type() == sr.SR_INT16_T):
        print "= " + repr(value.data().get_int16())
    elif (value.type() == sr.SR_INT32_T):
        print "= " + repr(value.data().get_int32())
    elif (value.type() == sr.SR_INT64_T):
        print "= " + repr(value.data().get_int64())
    elif (value.type() == sr.SR_IDENTITYREF_T):
        print "= " + repr(value.data().get_identityref())
    elif (value.type() == sr.SR_BITS_T):
        print "= " + repr(value.data().get_bits())
    elif (value.type() == sr.SR_BINARY_T):
        print "= " + repr(value.data().get_binary())
    else:
        print "(unprintable)"

def test_rpc_cb(xpath, in_vals, out_vals, private_ctx):
#    try:
        print "\n\n ========== RPC CALLED =========="
        out_vals.allocate(3)

        if (in_vals == None or out_vals == None):
            return

        for n in range(in_vals.val_cnt()):
            print_value(in_vals.val(n))

        out_vals.val(0).set("/test-module:activate-software-image/status", "The image acmefw-2.3 is being installed.", sr.SR_STRING_T)
        out_vals.val(1).set("/test-module:activate-software-image/version", "2.3", sr.SR_STRING_T)
        out_vals.val(2).set("/test-module:activate-software-image/location", "/", sr.SR_STRING_T)

#    except Exception as e:
#        print e

try:
    module_name = "test-module"

    # connect to sysrepo
    conn = sr.Connection("example_application")

    # start session
    sess = sr.Session(conn)

    # subscribe for changes in running config */
    subscribe = sr.Subscribe(sess)


    print "\n\n ========== SUBSCRIBE TO RPC CALL =========="
    subscribe.rpc_subscribe("/test-module:activate-software-image", test_rpc_cb);

    in_vals = sr.Vals(2);

    in_vals.val(0).set("/test-module:activate-software-image/image-name", "acmefw-2.3", sr.SR_STRING_T)
    in_vals.val(1).set("/test-module:activate-software-image/location", "/", sr.SR_STRING_T)


    print "\n\n ========== START RPC CALL =========="
    out_vals = subscribe.rpc_send("/test-module:activate-software-image", in_vals);

    print "\n\n ========== PRINT RETURN VALUE =========="
    for n in range (out_vals.val_cnt()):
        print_value(out_vals.val(n))

    print "\n\n ========== END PROGRAM =========="

except Exception as e:
    print e


