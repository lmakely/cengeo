__author__ = 'makel004'

ccd_list = ('01',
            '02',
            '04',
            '06',
            '08',
            '10',
            '12',
            '13',
            '15',
            '16',
            '21',
            '30',
            '32',
            '35',
            '40',
            '41',
            '45',
            '48',
            '49',
            '53',
            '56')

change_types = {'incplace': '_changes_incplace.shp',
                'cousub': '_changes_cousub.shp',
                'concity': '_changes_concity.shp',
                'aiannh': '_changes_aiannh.shp',
                'ln': '_ln_changes.shp',
                'hydroa': '_hydroa_changes.shp',
                'plndk': '_plndk_changes.shp',
                'alndk': '_alndk_changes.shp',
                'county': '_changes_county.shp'}

change_fields_id = {'incplace': 'PLACEFP',
                    'cousub': 'COUSUBFP',
                    'concity': 'CONCITYFP',
                    'county': 'COUNTYFP',
                    'aiannh': 'AIANNHCE',
                    'ln': 'TLID',
                    'hydroa': 'HYDROID',
                    'plndk': 'POINTID',
                    'alndk': 'AREAID'}

change_fields_req = {'incplace': ['STATEFP',
                                  'PLACEFP',
                                  'NAME',
                                  'NAMELSAD',
                                  'CHNG_TYPE',
                                  'EFF_DATE',
                                  'DOCU',
                                  'AREA',
                                  'RELATE'],
                     'county': ['STATEFP',
                                'COUNTYFP',
                                'NAME',
                                'NAMELSAD',
                                'CHNG_TYPE',
                                'EFF_DATE',
                                'DOCU',
                                'AREA',
                                'RELATE'],
                     'cousub': ['STATEFP',
                                'COUNTYFP',
                                'COUSUBFP',
                                'NAME',
                                'NAMELSAD',
                                'CHNG_TYPE',
                                'EFF_DATE',
                                'DOCU',
                                'AREA',
                                'RELATE'],
                     'concity': ['STATEFP',
                                 'CONCITYFP',
                                 'NAME',
                                 'NAMELSAD',
                                 'CHNG_TYPE',
                                 'EFF_DATE',
                                 'DOCU',
                                 'AREA',
                                 'RELATE'],
                     'aiannh': ['AIANNHCE',
                                'NAME',
                                'NAMELSAD',
                                'CHNG_TYPE',
                                'EFF_DATE',
                                'DOCU',
                                'AREA',
                                'RELATE'],
                     'ln': ['TLID',
                            'FULLNAME',
                            'CHNG_TYPE',
                            'MTFCC'],
                     'hydroa': ['HYDROID',
                                'FULLNAME',
                                'CHNG_TYPE',
                                'MTFCC',
                                'RELATE'],
                     'plndk': ['POINTID',
                               'FULLNAME',
                               'CHNG_TYPE',
                               'MTFCC'],
                     'alndk': ['AREAID',
                               'FULLNAME',
                               'CHNG_TYPE',
                               'MTFCC',
                               'RELATE']}

table_criteria = {'STATEFP': ["TEXT", '2'],
                  'COUNTYFP': ["TEXT", '3'],
                  'COUNTYNS': ["TEXT", '8'],
                  'NAMELSAD': ["TEXT", '100'],
                  'LSAD': ["TEXT", '2'],
                  'FUNCSTAT': ["TEXT", '1'],
                  'CLASSFP': ["TEXT", '2'],
                  'CHNG_TYPE': ["TEXT", '2'],
                  'EFF_DATE': ["DATE", '8'],
                  'AUTHTYPE': ["TEXT", '1'],
                  'DOCU': ["TEXT", '120'],
                  'FORM_ID': ["TEXT", '4'],
                  'AREA': ["DOUBLE", '10'],
                  'RELATE': ["TEXT", '120'],
                  'JUSTIFY': ["TEXT", '150'],
                  'NAME': ["TEXT", '100'],
                  'VINTAGE': ["TEXT", '2'],
                  'PLACEFP': ["TEXT", '5'],
                  'COUSUBFP': ["TEXT", '5'],
                  'CONCITYFP': ["TEXT", '5'],
                  'AIANNHCE': ["TEXT", '4']}