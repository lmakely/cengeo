
#This script creates a bunch of folders on the NPC side ("XX001", "XX003", etc) to house the data.  and copies
# local places and census places shapefile from the geoarea BQARP folder to the NPC BQARP folder


# Import system modules
import arcpy
from arcpy import env

# Set workspace
env.workspace = "\\\\batch4.ditd.census.gov\\mtdata003_geoarea\\BAS\CARP\\BQARP\\20\\"
print "Start"
xList = [ "201", "203", "205", "207", "209"]
for x in xList:
# Set local variables
    out_folder_path = "\\\\batch4.ditd.census.gov\\mtdata003_geoarea\\BAS\CARP\\BQARP\\20\\" 
    out_name = "20"+x
    print "folder for  20"+x+" created"

# Execute CreateFolder
    arcpy.CreateFolder_management(out_folder_path, out_name)

    inCopy = "\\\\batch4.ditd.census.gov\\mtdata003_geoarea\\BAS\CARP\\BQARP\\20\\Local_Places\\local_places_20"+x+".shp"
    outCopy = out_folder_path + out_name + "\\local_places_20"+x+".shp"

# Process: Copy
    if arcpy.Exists(inCopy):
        arcpy.Copy_management(inCopy, outCopy, "ShapeFile")
        print  "local places copied for  20"+x

    inCopy1 = "\\\\batch4.ditd.census.gov\\mtdata003_geoarea\\BAS\CARP\\BQARP\\20\\Census\\census_places_20"+x+".shp"
    outCopy1 = out_folder_path + out_name + "\\census_places_20"+x+".shp"

# Process: Copy
    if arcpy.Exists(inCopy1):
        arcpy.Copy_management(inCopy1, outCopy1, "ShapeFile")
        print  "census places copied for  20"+x
print "Complete"
