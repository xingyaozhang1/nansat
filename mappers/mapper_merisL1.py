#-------------------------------------------------------------------------------
# Name:        nansat_mapper_merisL1
# Purpose:     Mapping for Meris-L1 data
#
# Author:      antonk
#
# Created:     29.11.2011
# Copyright:   (c) asumak 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from vrt import VRT, Geolocation
from envisat import Envisat

class Mapper(VRT, Envisat):
    ''' VRT with mapping of WKV for MERIS Level 1 (FR or RR) '''

    def __init__(self, fileName, gdalDataset, gdalMetadata):
        ''' Create MER1 VRT '''
        product = gdalMetadata.get("MPH_PRODUCT", "Not_MERIS")

        if product[0:9] != "MER_FRS_1" and product[0:9] != "MER_RR__1":
            raise AttributeError("MERIS_L1 BAD MAPPER")

        # Create VRTdataset with small VRTRawRasterbands
        #geoDataset = self.create_VRT_with_rawbands(fileName, product[0:4], ["DME roughness", "viewing zenith angles"])
        #
        # Enlarge the band to the underlying data band size
        #self.geoDataset = geoDataset.resized(gdalDataset.RasterXSize, gdalDataset.RasterYSize)

        metaDict = [
        {'src': {'SourceFilename': fileName, 'SourceBand':  1}, 'dst': {'wkv': 'surface_upwelling_spectral_radiance_in_air_emerging_from_sea_water', 'wavelength': '412'}},
        {'src': {'SourceFilename': fileName, 'SourceBand':  2}, 'dst': {'wkv': 'surface_upwelling_spectral_radiance_in_air_emerging_from_sea_water', 'wavelength': '443'}},
        {'src': {'SourceFilename': fileName, 'SourceBand':  3}, 'dst': {'wkv': 'surface_upwelling_spectral_radiance_in_air_emerging_from_sea_water', 'wavelength': '490'}},
        {'src': {'SourceFilename': fileName, 'SourceBand':  4}, 'dst': {'wkv': 'surface_upwelling_spectral_radiance_in_air_emerging_from_sea_water', 'wavelength': '510'}},
        {'src': {'SourceFilename': fileName, 'SourceBand':  5}, 'dst': {'wkv': 'surface_upwelling_spectral_radiance_in_air_emerging_from_sea_water', 'wavelength': '560'}},
        {'src': {'SourceFilename': fileName, 'SourceBand':  6}, 'dst': {'wkv': 'surface_upwelling_spectral_radiance_in_air_emerging_from_sea_water', 'wavelength': '620'}},
        {'src': {'SourceFilename': fileName, 'SourceBand':  7}, 'dst': {'wkv': 'surface_upwelling_spectral_radiance_in_air_emerging_from_sea_water', 'wavelength': '665'}},
        {'src': {'SourceFilename': fileName, 'SourceBand':  8}, 'dst': {'wkv': 'surface_upwelling_spectral_radiance_in_air_emerging_from_sea_water', 'wavelength': '680'}},
        {'src': {'SourceFilename': fileName, 'SourceBand':  9}, 'dst': {'wkv': 'surface_upwelling_spectral_radiance_in_air_emerging_from_sea_water', 'wavelength': '708'}},
        {'src': {'SourceFilename': fileName, 'SourceBand': 10}, 'dst': {'wkv': 'surface_upwelling_spectral_radiance_in_air_emerging_from_sea_water', 'wavelength': '753'}},
        {'src': {'SourceFilename': fileName, 'SourceBand': 11}, 'dst': {'wkv': 'surface_upwelling_spectral_radiance_in_air_emerging_from_sea_water', 'wavelength': '761'}},
        {'src': {'SourceFilename': fileName, 'SourceBand': 12}, 'dst': {'wkv': 'surface_upwelling_spectral_radiance_in_air_emerging_from_sea_water', 'wavelength': '778'}},
        {'src': {'SourceFilename': fileName, 'SourceBand': 13}, 'dst': {'wkv': 'surface_upwelling_spectral_radiance_in_air_emerging_from_sea_water', 'wavelength': '864'}},
        {'src': {'SourceFilename': fileName, 'SourceBand': 14}, 'dst': {'wkv': 'surface_upwelling_spectral_radiance_in_air_emerging_from_sea_water', 'wavelength': '849'}},
        {'src': {'SourceFilename': fileName, 'SourceBand': 15}, 'dst': {'wkv': 'surface_upwelling_spectral_radiance_in_air_emerging_from_sea_water', 'wavelength': '900'}},
        {'src': {'SourceFilename': fileName, 'SourceBand': 16}, 'dst': {'wkv': 'quality_flags', 'BandName': 'l1_flags'}}
        ]

        # add 'band_name' to 'parameters'
        for bandDict in metaDict:
            if bandDict['dst'].has_key('wavelength'):
                bandDict['dst']['BandName'] = 'radiance_' + bandDict['dst']['wavelength']

        # get GADS from header
        scales = self.read_scaling_gads(fileName, range(7, 22));
        # set scale factor to the band metadata (only radiances)
        for i, bandDict in enumerate(metaDict[:-1]):
            bandDict['src']['ScaleRatio'] = str(scales[i])

        #add geolocation dictionary into metaDict
        #for iBand in range(self.geoDataset.dataset.RasterCount):
        #    bandMetadata = self.geoDataset.dataset.GetRasterBand(iBand+1).GetMetadata()
        #    metaDict.append({'src': {'SourceFilename': self.geoDataset.fileName, 'SourceBand': iBand+1}, 'dst': {'wkv': '', 'parameters':bandMetadata})

        # create empty VRT dataset with geolocation only
        VRT.__init__(self, gdalDataset)

        # add bands with metadata and corresponding values to the empty VRT
        self._create_bands(metaDict)

        # set time
        self._set_envisat_time(gdalMetadata)

        ''' Set GeolocationArray '''
        #latlonName = {"latitude":"latitude","longitude":"longitude"}
        #self.add_geoarray_dataset(fileName, product[0:4], gdalDataset.RasterXSize, gdalDataset.RasterYSize, latlonName, gdalDataset.GetGCPProjection())
