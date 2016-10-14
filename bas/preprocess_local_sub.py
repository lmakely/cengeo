__author__ = 'Lauren Makely'

# import all needed modules
import notify
import lisrds
import bas
import os
import arcpy
import shutil
import datetime
import sqlite3

# set ArcGIS environments
arcpy.env.outputMFlag = "Disabled"
arcpy.env.outputZFlag = "Disabled"

# set directories on local drive
geo_area = r'\\batch4.ditd.census.gov\mtdata003_geoarea\BAS'
geoShape = r'\\batch4.ditd.census.gov\mtdata003_geo_shpgen\mtps_mtdb'
bas_year = '17'

swim_dir = os.path.join(geo_area, 'Digital_BAS_20{XX}\Local_Submission'.format(bas_year))
bas_dir = os.path.join(geo_area, 'Digital_BAS_20{XX}\processing'.format(bas_year))
blisrds = os.path.join(geo_area, 'BLISRDS_STAGE')
log_db = os.path.join(bas_dir, 'basSetup.db')
mxd_template = os.path.join(geo_area, 'Digital_BAS_20{XX}\Templates\preprocess_template3.mxd'.format(bas_year))
bas_yy_county_merge = os.path.join(geo_area, 'ABEUS\bas{XX}countymerge.shp'.format(bas_year))

# this affects later bits of code but need to make sure i can't make it a function
try:  # fix this up later?
    conn = sqlite3.connect(log_db, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.execute("CREATE TABLE IF NOT EXISTS ENTITIES (BASID TEXT, FILENAME TEXT, FOLDER TEXT, STATE TEXT,"
                 "SUBTYPE TEXT,COUNTIES TEXT,ERRORS TEXT,TIMESTAMP NUMERIC)")
    conn.execute("CREATE TABLE IF NOT EXISTS SHAPEFILES (BASID TEXT, FILENAME TEXT, SHP TEXT, CHANGETYPE TEXT,"
                 "GDBFC TEXT, FLDERRORS TEXT, VALUEERRORS TEXT, PRJ TEXT)")
except:  # fix this up later?
    raise Exception
    #pass


def run_it(bas_id, supervised=True):
    print '*'*34 + '\n*   Running BASID: ' + bas_id + '   *' + '\n'+'*'*34
    state = bas_id[1:3]
    st_folder = os.path.join(bas_dir, state)
    if not os.path.exists(st_folder):
        os.mkdir(st_folder)
    folder = os.path.join(st_folder, bas_id)
    zp = zipPath(bas_id)
    filename = bas.which_zip(zp, bas_id)
    if not filename:
        print "No zip file encountered for " + bas_id
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
        bas.log_it(conn, bas_id, filename, folder, state, subType, counties, errors, datetime.datetime.now(), shp_dict)
    try:
        subType = submissionType(folder)
        shplist = getSHPs(folder)
        if not shplist:
            errors.append('No shapefiles found') #log_it
            bas.log_it(conn, bas_id, filename, folder, state, subType, counties, errors, datetime.datetime.now(), shp_dict)
            return
        for path, fn in shplist:
            shp_dict[path+'\\'+fn] = {'changetype':None, 'GDBFC':None, 'fldErrors':None, 'valueErrors':None, 'prj':None}
        changeFiles = chngSHPs(shplist)
        if not changeFiles:  #ask the user
            changeFiles = cantFindChanges(shplist)
        if not changeFiles:  #still no changes shapefile, time to give up.
            errors.append('No changes identified') #log_it
            bas.log_it(conn, bas_id, filename, folder, state, subType, counties, errors, datetime.datetime.now(), shp_dict)
            return

        for cf in changeFiles:
            ct = chngType(cf)
            if ct[:7] in ['mismatc', 'nomatch']:
                print ct
                ct = cantFindChangeType(cf)
                if ct:
                    ct = ct
            shp_dict[cf]['changetype'] = ct
        if subType == 'MTPS':
            formid = getFormDBF(folder)
            for cf in changeFiles:
                if shp_dict[cf]['changetype'] in ['incplace', 'cousub', 'concity', 'aiannh']:
                    formIDupdate(formid, cf)

        arcpy.CreateFileGDB_management(folder, "DB"+bas_id)
        GDB = folder + '\\' + "DB" + bas_id + '.gdb'
        if state == '02':  # Alaska
            arcpy.CreateFeatureDataset_management(
                GDB,
                "submission",
                "PROJCS['NAD_1983_Alaska_Albers', GEOGCS['GCS_North_American_1983',"
                "DATUM['D_North_American_1983', SPHEROID['GRS_1980',6378137.0,298.257222101]],"
                "PRIMEM['Greenwich',0.0], UNIT['Degree',0.0174532925199433]],"
                "PROJECTION['Albers'], PARAMETER['False_Easting',0.0],"
                "PARAMETER['False_Northing',0.0], PARAMETER['Central_Meridian',-154.0],"
                "PARAMETER['Standard_Parallel_1', 55.0], PARAMETER['Standard_Parallel_2',65.0],"
                "PARAMETER['Latitude_Of_Origin', 50.0], UNIT['Meter',1.0]];"
                "-13752200 -8948200 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision")
        elif state == '15':  # Hawaii
            arcpy.CreateFeatureDataset_management(
                GDB,
                "submission",
                "PROJCS['Hawaii_Albers_Equal_Area_Conic', GEOGCS['GCS_North_American_1983',"
                "DATUM['D_North_American_1983', SPHEROID['GRS_1980',6378137.0,298.257222101]],"
                "PRIMEM['Greenwich',0.0], UNIT['Degree',0.0174532925199433]], PROJECTION['Albers'],"
                "PARAMETER['False_Easting',0.0], PARAMETER['False_Northing',0.0], "
                "PARAMETER['Central_Meridian',-157.0], PARAMETER['Standard_Parallel_1',8.0],"
                "PARAMETER['Standard_Parallel_2',18.0], PARAMETER['Latitude_Of_Origin',13.0],"
                "UNIT['Meter',1.0]];-22487400 -7108900 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision")
        else:    # contiguous USA 48
            arcpy.CreateFeatureDataset_management(
                GDB,
                "submission",
                "PROJCS['USA_Contiguous_Albers_Equal_Area_Conic_USGS_version',"
                "GEOGCS['GCS_North_American_1983', DATUM['D_North_American_1983',"
                "SPHEROID['GRS_1980',6378137.0,298.257222101]], PRIMEM['Greenwich',0.0],"
                "UNIT['Degree',0.0174532925199433]], PROJECTION['Albers'], "
                "PARAMETER['False_Easting',0.0], PARAMETER['False_Northing',0.0],"
                "PARAMETER['Central_Meridian',-96.0], PARAMETER['Standard_Parallel_1',29.5],"
                "PARAMETER['Standard_Parallel_2',45.5], PARAMETER['Latitude_Of_Origin',23.0],"
                "UNIT['Meter',1.0]];-16901100 -6972200 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision")
        fd = GDB + '\\submission'
        for cf in changeFiles:
            ct = shp_dict[cf]['changetype']
            if ct in bas.dicts.change_types.keys():
                shp_dict[cf]['fldErrors'] = fldErrors = fldChk(cf, ct)

                arcpy.AddField_management(cf, "PROCESS", "TEXT", field_length=1)
                arcpy.AddField_management(cf, "P_COMMENTS", "TEXT", field_length=200)
                arcpy.AddField_management(cf, "VERIFY", "TEXT", field_length=1)
                arcpy.AddField_management(cf, "V_COMMENTS", "TEXT", field_length=200)
                arcpy.AddField_management(cf, "DIGITIZE", "TEXT", field_length=1)
                arcpy.AddField_management(cf, "D_COMMENTS", "TEXT", field_length=200)
                arcpy.AddField_management(cf, "QC", "TEXT", field_length=1)
                arcpy.AddField_management(cf, "Q_COMMENTS", "TEXT", field_length=200)

                try:
                    if ct in ['ln', 'hydroa', 'plndk', 'alndk']:
                        shp_dict[cf]['valueErrors'] = valueErrors = valChk2(cf, ct)
                    else:
                        shp_dict[cf]['valueErrors'] = valueErrors = valChk(cf, georgia)
                except:
                    shp_dict[cf]['valueErrors'] = valueErrors = ['values could not be checked; perhaps a key field is missing.']
                shp_dict[cf]['prj'] = prj = prjChk(cf)
                if not prj:
                    errors.append('shapefile "' + cf + '" is not projected, and could not be imported to the GDB')  # log_it
                else:
                    shp_dict[cf]['GDBFC'] = outputFC = 'bas' + bas_year + '_' + bas_id + '_changes_' + ct
                    if arcpy.Exists(fd+'\\'+outputFC):
                        try:
                            arcpy.Append_management(cf, fd+ '\\' +outputFC, 'TEST')
                        except:
                            errors.append("Feature Class " + outputFC + " might be missing data from Shapefile "
                                          + cf + " because their attributes did not line up exactly.")
                            arcpy.Append_management(cf, fd + '\\' +outputFC, 'NO_TEST')
                    else:
                        arcpy.FeatureClassToFeatureClass_conversion(cf, fd, outputFC)
        #counties = bas.get_counties(list(x+'\\'+y for x,y in changeFiles), BAS14countyMerge)
        counties = bas.get_counties(changeFiles, bas_yy_county_merge)
        bas.import_support(GDB, counties, folder, state)
        lisrds(counties)
        mxd = GDB.replace('.gdb', '.mxd')
        shutil.copy(mxd_template, mxd)
        mxd = arcpy.mapping.MapDocument(mxd)
        layers = arcpy.mapping.ListLayers(mxd)
        for layer in layers:
            new_fc = layer.datasetName.replace('template', bas_id)
            new_path = os.path.join(GDB, new_fc)
            if layer.isFeatureLayer and arcpy.Exists(new_path):
                layer.replaceDataSource(GDB, "FILEGDB_WORKSPACE", new_fc)
            layer.name = layer.name.replace('template', bas_id)
        df = arcpy.mapping.ListDataFrames(mxd)[0]
        layers = arcpy.mapping.ListLayers(mxd)
        for layer in layers:
            if layer.isBroken:
                arcpy.mapping.RemoveLayer(df, layer)
        county_lyr = arcpy.mapping.ListLayers(mxd, 'bas_county', df)[0]
        df.extent = county_lyr.getExtent()
        mxd.save()
        del mxd, df
        bas.log_it(conn, bas_id, filename, folder, state, subType, counties, errors, datetime.datetime.now(), shp_dict)
    except Exception, e:
        errors.append(e)
        bas.log_it(conn, bas_id, filename, folder, state, subType, counties, errors, datetime.datetime.now(), shp_dict)


if __name__ == "__main__":  # script is being executed on its own, outside of idle.
    notify()
    inText = raw_input("Enter a BAS ID, or comma separated list of BAS IDs (with no spaces):\n")
    while 1:
        if inText:
            inList = inText.split(',')
            for entity in inList:
                run_it(entity)
        else:
            break
        notify()
        repeat = raw_input("Done with list. Do you want to run more (y,n)?: ")
        if repeat.lower() in ['y', 'yes', '1']:
            notify()
            inText = raw_input("Enter a BAS ID, or comma separated list of BAS IDs (with no spaces):\n")
        else:
            break
