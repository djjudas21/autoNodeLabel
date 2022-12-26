def mapVendor(vendor):
    if vendor == 'GenuineIntel':
        returnval = 'Intel'
    elif vendor == 'AuthenticAMD':
        returnval = 'AMD'
    else:
        returnval = vendor
    return returnval

def cleanBrand(brand):
    # Strip annoying chars
    brand = brand.replace('(R)', '')
    brand = brand.replace('(TM)', '')
    brand = brand.replace('CPU', '')

    # Drop the '@ 2.40GHz' suffix
    brand = brand.split('@')[0]

    # Drop the 'with Radeon Graphics' suffix
    brand = brand.split('with')[0]
    brand = brand.strip()

    return brand

if __name__ == '__main__':
    from cpuinfo import get_cpu_info

    #for key, value in get_cpu_info().items():
    #    print("{0}: {1}".format(key, value))

    cpuinfo = get_cpu_info()

    annotations = {}
    annotations['vendor'] = mapVendor(cpuinfo['vendor_id_raw'])
    annotations['brand'] = cleanBrand(cpuinfo['brand_raw'])
    annotations['speed'] = cpuinfo['hz_advertised_friendly']

    print(annotations)
