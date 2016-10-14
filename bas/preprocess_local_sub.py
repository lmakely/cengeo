__author__ = 'makel004'

# import all needed modules
import cengeo
from cengeo import bas
import os
import arcpy
import zipfile
import shutil
import datetime
import sqlite3
import winsound

# set ArcGIS environments
arcpy.env.outputMFlag = "Disabled"
arcpy.env.outputZFlag = "Disabled"

# set directories on local drive
geo_area = r'\\batch4.ditd.census.gov\mtdata003_geoarea\BAS'
geoShape = r'\\batch4.ditd.census.gov\mtdata003_geo_shpgen\mtps_mtdb'

# some of these are for sure old and not needed anymore. ask Nick which can just get deleted?
swim_dir = os.path.join(geo_area, 'Digital_BAS_2016\Local_Submission')
bas_dir = os.path.join(geo_area, 'Digital_BAS_2016\processing')
blisrds = os.path.join(geo_area, 'BLISRDS_STAGE')
bench_dir = os.path.join(geoShape, 'bas16_2015')
bench_base = 'bas16_2015_'
bas_yy_county_merge = os.path.join(geo_area, 'ABEUS\bas16countymerge.shp')  # change before production
log_db = os.path.join(bas_dir, 'basSetup.db')
mxd_template = os.path.join(geo_area, 'Digital_BAS_2016\Templates\preprocess_template3.mxd')


# this affects later bits of code but need to make sure i can make it a function
try:  # fix this up later?
    conn = sqlite3.connect(log_db, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.execute("CREATE TABLE IF NOT EXISTS ENTITIES (BASID TEXT, FILENAME TEXT, FOLDER TEXT, STATE TEXT,"
                 "SUBTYPE TEXT,COUNTIES TEXT,ERRORS TEXT,TIMESTAMP NUMERIC)")
    conn.execute("CREATE TABLE IF NOT EXISTS SHAPEFILES (BASID TEXT, FILENAME TEXT, SHP TEXT, CHANGETYPE TEXT,"
                 "GDBFC TEXT, FLDERRORS TEXT, VALUEERRORS TEXT, PRJ TEXT)")
except:  # fix this up later?
    pass


def runit(basid, supervised=True):
    print '*'*34 + '\n*   Running BASID: ' + basid + '   *' + '\n'+'*'*34
    state = basid[1:3]
    stfolder = bas_dir+'\\'+state
    if not os.path.exists(stfolder):
        os.mkdir(stfolder)
    folder = stfolder+'\\'+basid
    zp = zipPath(basid)
    filename = whichZip(zp,basid)
    if not filename:
        print "No zip file encountered for " + basid
        return
    fullzipsrc = zp + '\\' + filename
    errors = []
    shp_dict = {}
    subType = None
    counties = None
    if state == '13':
        georgia = True
    else:
        georgia = False
    try:
        os.mkdir(folder)
    except Exception, e:
        print 'Could not make project directory.'
        print e
    try:
        extractZip(fullzipsrc, folder)
    except Exception, e:
        errors.append('Could not extract ZIP file.')
        bas.log_it(conn, basid, filename, folder, state, subType, counties, errors, datetime.datetime.now(), shp_dict)
    try:
        subType = submissionType(folder)
        shplist = getSHPs(folder)
        if not shplist:
            errors.append('No shapefiles found') #log_it
            bas.log_it(conn, basid, filename, folder, state, subType, counties, errors, datetime.datetime.now(), shp_dict)
            return
        for path, fn in shplist:
            shp_dict[path+'\\'+fn] = {'changetype':None, 'GDBFC':None, 'fldErrors':None, 'valueErrors':None, 'prj':None}
        changeFiles = chngSHPs(shplist)
        if not changeFiles:  #ask the user
            changeFiles = cantFindChanges(shplist)
        if not changeFiles:  #still no changes shapefile, time to give up.
            errors.append('No changes identified') #log_it
            bas.log_it(conn, basid, filename, folder, state, subType, counties, errors, datetime.datetime.now(), shp_dict)
            return

        for CF in changeFiles:
            CT = chngType(CF)
            if CT[:7] in ['mismatc', 'nomatch']:
                print CT
                ct = cantFindChangeType(CF)
                if ct:
                    CT = ct
            shp_dict[CF]['changetype'] = CT
        if subType == 'MTPS':
            formid = getFormDBF(folder)
            for CF in changeFiles:
                if shp_dict[CF]['changetype'] in ['incplace', 'cousub', 'concity', 'aiannh']:
                    formIDupdate(formid, CF)

        arcpy.CreateFileGDB_management(folder, "DB"+basid)
        GDB = folder + '\\' + "DB" + basid + '.gdb'
        if state == '02':  # Alaska
            arcpy.CreateFeatureDataset_management(
                GDB, "submission", "PROJCS['NAD_1983_Alaska_Albers', GEOGCS['GCS_North_American_1983',"
                                   "DATUM['D_North_American_1983', SPHEROID['GRS_1980',6378137.0,298.257222101]],"
                                   "PRIMEM['Greenwich',0.0], UNIT['Degree',0.0174532925199433]],"
                                   "PROJECTION['Albers'], PARAMETER['False_Easting',0.0],"
                                   "PARAMETER['False_Northing',0.0], PARAMETER['Central_Meridian',-154.0],"
                                   "PARAMETER['Standard_Parallel_1', 55.0], PARAMETER['Standard_Parallel_2',65.0],"
                                   "PARAMETER['Latitude_Of_Origin', 50.0], UNIT['Meter',1.0]];"
                                   "-13752200 -8948200 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision")
        elif state == '15':  # Hawaii
            arcpy.CreateFeatureDataset_management(
                GDB, "submission", "PROJCS['Hawaii_Albers_Equal_Area_Conic', GEOGCS['GCS_North_American_1983',"
                                   "DATUM['D_North_American_1983', SPHEROID['GRS_1980',6378137.0,298.257222101]],"
                                   "PRIMEM['Greenwich',0.0], UNIT['Degree',0.0174532925199433]], PROJECTION['Albers'],"
                                   "PARAMETER['False_Easting',0.0], PARAMETER['False_Northing',0.0], "
                                   "PARAMETER['Central_Meridian',-157.0], PARAMETER['Standard_Parallel_1',8.0],"
                                   "PARAMETER['Standard_Parallel_2',18.0], PARAMETER['Latitude_Of_Origin',13.0],"
                                   "UNIT['Meter',1.0]];-22487400 -7108900 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision")
        else:    # contiguous USA 48
            arcpy.CreateFeatureDataset_management(
                GDB, "submission", "PROJCS['USA_Contiguous_Albers_Equal_Area_Conic_USGS_version',"
                                   "GEOGCS['GCS_North_American_1983', DATUM['D_North_American_1983',"
                                   "SPHEROID['GRS_1980',6378137.0,298.257222101]], PRIMEM['Greenwich',0.0],"
                                   "UNIT['Degree',0.0174532925199433]], PROJECTION['Albers'], "
                                   "PARAMETER['False_Easting',0.0], PARAMETER['False_Northing',0.0],"
                                   "PARAMETER['Central_Meridian',-96.0], PARAMETER['Standard_Parallel_1',29.5],"
                                   "PARAMETER['Standard_Parallel_2',45.5], PARAMETER['Latitude_Of_Origin',23.0],"
                                   "UNIT['Meter',1.0]];-16901100 -6972200 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision")
        FD = GDB + '\\submission'
        for CF in changeFiles:
            CT = shp_dict[CF]['changetype']
            if CT in change_types.keys():
                shp_dict[CF]['fldErrors'] = fldErrors = fldChk(CF,CT)

                arcpy.AddField_management(CF, "PROCESS", "TEXT", field_length=1)
                arcpy.AddField_management(CF, "P_COMMENTS", "TEXT", field_length=200)
                arcpy.AddField_management(CF, "VERIFY", "TEXT", field_length=1)
                arcpy.AddField_management(CF, "V_COMMENTS", "TEXT", field_length=200)
                arcpy.AddField_management(CF, "DIGITIZE", "TEXT", field_length=1)
                arcpy.AddField_management(CF, "D_COMMENTS", "TEXT", field_length=200)
                arcpy.AddField_management(CF, "QC", "TEXT", field_length=1)
                arcpy.AddField_management(CF, "Q_COMMENTS", "TEXT", field_length=200)

                try:
                    if CT in ['ln', 'hydroa', 'plndk', 'alndk']:
                        shp_dict[CF]['valueErrors'] = valueErrors = valChk2(CF, CT)
                    else:
                        shp_dict[CF]['valueErrors'] = valueErrors = valChk(CF, georgia)
                except:
                    shp_dict[CF]['valueErrors'] = valueErrors = ['values could not be checked; perhaps a key field is missing.']
                shp_dict[CF]['prj'] = prj = prjChk(CF)
                if not prj:
                    errors.append('shapefile "' + CF + '" is not projected, and could not be imported to the GDB')  # log_it
                else:
                    shp_dict[CF]['GDBFC'] = outputFC = 'bas16_' + basid + '_changes_' + CT
                    if arcpy.Exists(FD+'\\'+outputFC):
                        try:
                            arcpy.Append_management(CF, FD+ '\\' +outputFC, 'TEST')
                        except:
                            errors.append("Feature Class " + outputFC + " might be missing data from Shapefile "
                                          + CF + " because their attributes did not line up exactly.")
                            arcpy.Append_management(CF, FD + '\\' +outputFC, 'NO_TEST')
                    else:
                        arcpy.FeatureClassToFeatureClass_conversion(CF, FD, outputFC)
        #counties = get_counties(list(x+'\\'+y for x,y in changeFiles), BAS14countyMerge)
        counties = get_counties(changeFiles, bas_yy_county_merge)
        import_support(GDB, counties, folder, state)
        lisrds(counties)
        mxd = GDB.replace('.gdb', '.mxd')
        shutil.copy(mxd_template, mxd)
        MXD = arcpy.mapping.MapDocument(mxd)
        layers = arcpy.mapping.ListLayers(MXD)
        for layer in layers:
            newfc = layer.datasetName.replace('template', basid)
            newpath = GDB+'\\'+newfc
            if layer.isFeatureLayer and arcpy.Exists(newpath):
                layer.replaceDataSource(GDB, "FILEGDB_WORKSPACE", newfc)
            layer.name = layer.name.replace('template', basid)
        df = arcpy.mapping.ListDataFrames(MXD)[0]
        layers = arcpy.mapping.ListLayers(MXD)
        for layer in layers:
            if layer.isBroken:
                arcpy.mapping.RemoveLayer(df, layer)
        county_lyr = arcpy.mapping.ListLayers(MXD, 'bas_county', df)[0]
        df.extent = county_lyr.getExtent()
        MXD.save()
        del MXD, df
        bas.log_it(conn, basid, filename, folder, state, subType, counties, errors, datetime.datetime.now(), shp_dict)
    except Exception, e:
        errors.append(e)
        bas.log_it(conn, basid, filename, folder, state, subType, counties, errors, datetime.datetime.now(), shp_dict)


if __name__ == "__main__":  # script is being executed on its own, outside of idle.
    cengeo.notify()
    inText = raw_input("Enter a BAS ID, or comma separated list of BAS IDs (with no spaces):\n")
    while 1:
        if inText:
            inList = inText.split(',')
            for entity in inList:
                runit(entity)
        else:
            break
        cengeo.notify()
        repeat = raw_input("Done with list. Do you want to run more (y,n)?: ")
        if repeat.lower() in ['y', 'yes', '1']:
            cengeo.notify()
            inText = raw_input("Enter a BAS ID, or comma separated list of BAS IDs (with no spaces):\n")
        else:
            break
