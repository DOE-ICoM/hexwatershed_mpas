
import os, sys, stat
from pathlib import Path
from os.path import realpath
import cartopy.crs as ccrs
from pyhexwatershed.pyhexwatershed_read_model_configuration_file import pyhexwatershed_read_model_configuration_file

#===========================
#setup workspace path
#===========================
sPath_parent = str(Path(__file__).parents[2]) # data is located two dir's up
sPath_data = realpath( sPath_parent +  '/data/susquehanna' )
sWorkspace_input =  str(Path(sPath_data)  /  'input')
sWorkspace_output = '/compyfs/liao313/04model/pyhexwatershed/susquehanna'

#===================================
#you need to update this file based on your own case study
#===================================
sFilename_configuration_in = realpath( sPath_parent +  '/examples/susquehanna/pyhexwatershed_susquehanna_square.json' )
if os.path.isfile(sFilename_configuration_in):
    pass
else:
    print('This configuration does not exist: ', sFilename_configuration_in )


#===========================
#setup case information
#===========================
iFlag_create_job=0
iFlag_visualization =1
iCase_index = 5
aResolution_meter = [5000, 40000]
nResolution = len(aResolution_meter)
sMesh_type = 'square'
sDate='20220901'

#===================================
#setup output and HPC job 
#===================================
if iFlag_create_job ==1:
    sSlurm = 'short'
    sFilename = sWorkspace_output + '/' + sMesh_type + '.bash'
    ofs = open(sFilename, 'w')
    sLine  = '#!/bin/bash' + '\n'
    ofs.write(sLine)

#===================================
#visualization spatial extent
#===================================
dLongitude_outlet_degree=-76.0093 
dLatitude_outlet_degree=39.4620
pProjection_map = ccrs.Orthographic(central_longitude=  dLongitude_outlet_degree, \
        central_latitude= dLatitude_outlet_degree, globe=None)
aExtent_full = [-79,-74.6, 39.3,43.0]
aExtent_meander = [-76.5,-76.2, 41.6,41.9] #meander
aExtent_braided = [-77.3,-76.5, 40.2,41.0] #braided
aExtent_confluence = [-77.3,-76.5, 40.2,41.0] #confluence
aExtent_outlet = [-76.0,-76.5, 39.5,40.0] #outlet
aExtent_dam = [-75.75,-76.15, 42.1,42.5] #dam  

for iResolution in range(1, nResolution+1):        
    dResolution_meter = aResolution_meter[iResolution-1]

    #===================================
    #topology turn off
    #===================================
    iFlag_stream_burning_topology = 0
    iFlag_use_mesh_dem = 0
    iFlag_elevation_profile = 0
    oPyhexwatershed = pyhexwatershed_read_model_configuration_file(sFilename_configuration_in,\
        iCase_index_in=iCase_index,\
            iFlag_stream_burning_topology_in=iFlag_stream_burning_topology,\
                iFlag_use_mesh_dem_in=iFlag_use_mesh_dem,\
                    iFlag_elevation_profile_in=iFlag_elevation_profile,\
             dResolution_meter_in = dResolution_meter, sDate_in= sDate, sMesh_type_in= sMesh_type)   
    oPyhexwatershed.pPyFlowline.aBasin[0].dLatitude_outlet_degree=dLatitude_outlet_degree
    oPyhexwatershed.pPyFlowline.aBasin[0].dLongitude_outlet_degree=dLongitude_outlet_degree 
    if iFlag_create_job ==1:
        oPyhexwatershed._create_hpc_job()   
        sLine  = 'cd ' + oPyhexwatershed.sWorkspace_output + '\n'
        ofs.write(sLine)
        sLine  = 'sbatch submit.job' + '\n'
        ofs.write(sLine)
    
    if iFlag_visualization == 1:
        sFilename = os.path.join(  oPyhexwatershed.sWorkspace_output_hexwatershed, 'surface_elevation.png' )
        oPyhexwatershed._plot(sFilename, iFlag_type_in =1, sVariable_in = 'elevation', aExtent_in=aExtent_full,pProjection_map_in=pProjection_map)     
        sFilename = os.path.join(  oPyhexwatershed.sWorkspace_output_hexwatershed, 'surface_slope.png' )        
        oPyhexwatershed._plot(sFilename, iFlag_type_in =1, sVariable_in = 'slope', aExtent_in=aExtent_full,pProjection_map_in=pProjection_map) 
        sFilename = os.path.join(  oPyhexwatershed.sWorkspace_output_hexwatershed, 'drainage_area.png' )
        oPyhexwatershed._plot(sFilename, iFlag_type_in =1, sVariable_in = 'drainagearea', aExtent_in=aExtent_full,pProjection_map_in=pProjection_map)   
        sFilename = os.path.join(  oPyhexwatershed.sWorkspace_output_hexwatershed, 'flow_direction.png' )
        oPyhexwatershed._plot(sFilename, iFlag_type_in =2, sVariable_in = 'flow_direction', aExtent_in=aExtent_full,pProjection_map_in=pProjection_map) 
        sFilename = os.path.join(  oPyhexwatershed.sWorkspace_output_hexwatershed, 'flow_direction_w_mesh.png' )
        oPyhexwatershed._plot(sFilename, iFlag_type_in =3, sVariable_in = 'flow_direction', aExtent_in=aExtent_full,pProjection_map_in=pProjection_map)    
        sFilename = os.path.join(  oPyhexwatershed.sWorkspace_output_hexwatershed, 'flow_direction_w_observation.png' )
        oPyhexwatershed._plot(sFilename, iFlag_type_in =4, sVariable_in = 'flow_direction', aExtent_in=aExtent_full,pProjection_map_in=pProjection_map)  
        sFilename = os.path.join(  oPyhexwatershed.sWorkspace_output_hexwatershed, 'travel_distance.png' )
        oPyhexwatershed._plot(sFilename, iFlag_type_in =1, sVariable_in = 'distance_to_outlet', aExtent_in=aExtent_full, pProjection_map_in=pProjection_map)    
     
    
    iCase_index = iCase_index + 1

    #===================================
    #topology turn on
    #===================================
    iFlag_stream_burning_topology = 1
    oPyhexwatershed = pyhexwatershed_read_model_configuration_file(sFilename_configuration_in,\
        iCase_index_in=iCase_index,  iFlag_stream_burning_topology_in=iFlag_stream_burning_topology,\
              iFlag_use_mesh_dem_in=iFlag_use_mesh_dem,\
                    iFlag_elevation_profile_in=iFlag_elevation_profile,\
            dResolution_meter_in = dResolution_meter, sDate_in= sDate, sMesh_type_in= sMesh_type)   
    oPyhexwatershed.pPyFlowline.aBasin[0].dLatitude_outlet_degree=dLatitude_outlet_degree
    oPyhexwatershed.pPyFlowline.aBasin[0].dLongitude_outlet_degree=dLongitude_outlet_degree
    if iFlag_create_job ==1:
        oPyhexwatershed._create_hpc_job()   
        sLine  = 'cd ' + oPyhexwatershed.sWorkspace_output + '\n'
        ofs.write(sLine)
        sLine  = 'sbatch submit.job' + '\n'
        ofs.write(sLine)

    if iFlag_visualization == 1:
        sFilename = os.path.join(  oPyhexwatershed.sWorkspace_output_hexwatershed, 'surface_elevation.png' )
        oPyhexwatershed._plot(sFilename, iFlag_type_in =1, sVariable_in = 'elevation', aExtent_in=aExtent_full,pProjection_map_in=pProjection_map)     
        sFilename = os.path.join(  oPyhexwatershed.sWorkspace_output_hexwatershed, 'surface_slope.png' )        
        oPyhexwatershed._plot(sFilename, iFlag_type_in =1, sVariable_in = 'slope', aExtent_in=aExtent_full,pProjection_map_in=pProjection_map) 
        sFilename = os.path.join(  oPyhexwatershed.sWorkspace_output_hexwatershed, 'drainage_area.png' )
        oPyhexwatershed._plot(sFilename, iFlag_type_in =1, sVariable_in = 'drainagearea', aExtent_in=aExtent_full,pProjection_map_in=pProjection_map)   
        sFilename = os.path.join(  oPyhexwatershed.sWorkspace_output_hexwatershed, 'flow_direction.png' )
        oPyhexwatershed._plot(sFilename, iFlag_type_in =2, sVariable_in = 'flow_direction', aExtent_in=aExtent_full,pProjection_map_in=pProjection_map) 
        sFilename = os.path.join(  oPyhexwatershed.sWorkspace_output_hexwatershed, 'flow_direction_w_mesh.png' )
        oPyhexwatershed._plot(sFilename, iFlag_type_in =3, sVariable_in = 'flow_direction', aExtent_in=aExtent_full,pProjection_map_in=pProjection_map)    
        sFilename = os.path.join(  oPyhexwatershed.sWorkspace_output_hexwatershed, 'flow_direction_w_observation.png' )
        oPyhexwatershed._plot(sFilename, iFlag_type_in =4, sVariable_in = 'flow_direction', aExtent_in=aExtent_full,pProjection_map_in=pProjection_map)  
        sFilename = os.path.join(  oPyhexwatershed.sWorkspace_output_hexwatershed, 'travel_distance.png' )
        oPyhexwatershed._plot(sFilename, iFlag_type_in =1, sVariable_in = 'distance_to_outlet', aExtent_in=aExtent_full, pProjection_map_in=pProjection_map)  
     

    iCase_index = iCase_index + 1
            
if iFlag_create_job ==1:
    ofs.close()
    os.chmod(sFilename, stat.S_IREAD | stat.S_IWRITE | stat.S_IXUSR) 
