#
# utility classes
#

#
# utlity class to read nested json field from Python Dictionary row
# e.g. item is Python Dictionary row, there's collection named "fields"
# each field contains "xml_data"
#
# usage:
#
# from utility import DictQuery
#
# DictQuery(item).get('fields/xml_data')
#
class DictQuery(dict):
    def get(self, path, default = None):
        keys = path.split("/")
        val = None

        for key in keys:
            if val:
                if isinstance(val, list):
                    val = [ v.get(key, default) if v else None for v in val]
                else:
                    val = val.get(key, default)
            else:
                val = dict.get(self, key, default)

            if not val:
                break;

        return val
