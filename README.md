# A pyang plugin to extract OpenConfig module catalog data from YANG modules

This pyang plugin extracts module metadata from YANG files according to [draft-openconfig-netmod-model-catalog](https://tools.ietf.org/html/draft-openconfig-netmod-model-catalog-01). The output (in JSON or XML) can be fed right back into a NETCONF or RESTCONF server that have the module catalog YANG module (openconfig-module-catalog.yang) loaded.

```
$ pyang -f module-catalog ietf-interfaces\@2014-05-08.yang
{
    "module": {
        "prefix": "if",
        "dependencies": {
            "required-module": [
                {
                    "module-revision": "unknown",
                    "module-name": "ietf-yang-types"
                }
            ]
        },
        "namespace": "urn:ietf:params:xml:ns:yang:ietf-interfaces",
        "name": "ietf-interfaces",
        "revision": "2014-05-08"
    }
}
```
