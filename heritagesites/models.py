# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models
from django.urls import reverse #chnote added 11/8/2018 hw8
from django.urls import reverse_lazy #chnote added 11/8/2018 hw8 debugging


class CountryArea(models.Model):
    country_area_id = models.AutoField(primary_key=True)
    country_area_name = models.CharField(unique=True, max_length=100)
    # region = models.ForeignKey('Region', models.DO_NOTHING, blank=True, null=True)
    # sub_region = models.ForeignKey('SubRegion', models.DO_NOTHING, blank=True, null=True)
    # intermediate_region = models.ForeignKey('IntermediateRegion', models.DO_NOTHING, blank=True, null=True)
    m49_code = models.SmallIntegerField()
    iso_alpha3_code = models.CharField(max_length=3)
    dev_status = models.ForeignKey('DevStatus', models.DO_NOTHING, blank=True, null=True)
    location = models.ForeignKey('Location', models.DO_NOTHING, default=1) #chnote: added 10/2/18
    
    class Meta:
        managed = False
        db_table = 'country_area'
        ordering = ['country_area_name']
        verbose_name = 'UNSD M49 Country or Area'
        verbose_name_plural = 'UNSD M49 Countries or Areas'

    def __str__(self):
        return self.country_area_name

class Location(models.Model): #CHnote added 10/2/108
    """
    New model based on Mtg 5 refactoring of the database.
    """
    location_id = models.AutoField(primary_key=True)
   #location_name = models.CharField(unique=True, max_length=100)
    planet = models.ForeignKey('Planet', models.DO_NOTHING)
    region = models.ForeignKey('Region', models.DO_NOTHING, blank=True, null=True)
    sub_region = models.ForeignKey('SubRegion', models.DO_NOTHING, blank=True, null=True)
    intermediate_region = models.ForeignKey('IntermediateRegion', models.DO_NOTHING, blank=True, null=True)
    # define additional properties as needed    

    class Meta:
        managed = False   #<-- #YOU MUST SET managed TO FALSE
        db_table = 'location'
        ordering = ['location_id']
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

    def __str__(self):
        return str(self.location_id) #<-- MUST RETURN A STRING

'''   
class CountryArea(models.Model):
    country_area_id = models.AutoField(primary_key=True)
    country_area_name = models.CharField(unique=True, max_length=100)
    region = models.ForeignKey('Region', models.DO_NOTHING, blank=True, null=True)
    sub_region = models.ForeignKey('SubRegion', models.DO_NOTHING, blank=True, null=True)
    intermediate_region = models.ForeignKey('IntermediateRegion', models.DO_NOTHING, blank=True, null=True)
    m49_code = models.SmallIntegerField()
    iso_alpha3_code = models.CharField(max_length=3)
    dev_status = models.ForeignKey('DevStatus', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'country_area'
'''


class DevStatus(models.Model):
    dev_status_id = models.AutoField(primary_key=True)
    dev_status_name = models.CharField(unique=True, max_length=25)

    class Meta:
        managed = False
        db_table = 'dev_status'
        ordering = ['dev_status_name']
        verbose_name = 'UNSD M49 Country or Area Development Status'
        verbose_name_plural = 'UNSD M49 Country or Area Development Statuses'

    def __str__(self):
        return self.dev_status_name


'''
class DevStatus(models.Model):
    dev_status_id = models.AutoField(primary_key=True)
    dev_status_name = models.CharField(unique=True, max_length=25)

    class Meta:
        managed = False
        db_table = 'dev_status'
'''


class HeritageSite(models.Model):
    heritage_site_id = models.AutoField(primary_key=True)
    site_name = models.CharField(unique=True, max_length=255)
    description = models.TextField()
    justification = models.TextField(blank=True, null=True)
    date_inscribed = models.IntegerField(blank=True, null=True)  #chnote changed 11/8/2018 hw8
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    area_hectares = models.FloatField(blank=True, null=True)
    heritage_site_category = models.ForeignKey('HeritageSiteCategory', models.DO_NOTHING)
    transboundary = models.IntegerField()

    # Intermediate model (country_area -> heritage_site_jurisdiction <- heritage_site)
    country_area = models.ManyToManyField(CountryArea, through='HeritageSiteJurisdiction')

    location = models.ManyToManyField(Location, through='HeritageSiteJurisdiction')

    class Meta:
        managed = False
        db_table = 'heritage_site'
        ordering = ['site_name']
        verbose_name = 'UNESCO Heritage Site'
        verbose_name_plural = 'UNESCO Heritage Sites'

    def __str__(self):
        return self.site_name

    def country_area_display(self):
        """Create a string for country_area. This is required to display in the Admin view."""
        return ', '.join(
            country_area.country_area_name for country_area in self.country_area.all()[:25])

    country_area_display.short_description = 'Country or Area'

    def get_absolute_url(self):
    # return reverse('site_detail', args=[str(self.id)])
        return reverse('site_detail', kwargs={'pk': self.pk}) #chnote added 11/8/2018 hw8 - is this the correct spot?

    
    #chnote country_area_names added 11/13/2018 hw9
    @property
    def country_area_names(self):
        """
        Returns a list of UNSD countries/areas (names only) associated with a Heritage Site.
        Note that not all Heritage Sites are associated with a country/area (e.g., Old City
        Walls of Jerusalem). In such cases the Queryset will return as <QuerySet [None]> and the
        list will need to be checked for None or a TypeError (sequence item 0: expected str
        instance, NoneType found) runtime error will be thrown.
        :return: string
        """
        countries = self.country_area.select_related('location').order_by('country_area_name')

        names = []
        for country in countries:
            name = country.country_area_name
            if name is None:
                continue
            iso_code = country.iso_alpha3_code

            name_and_code = ''.join([name, ' (', iso_code, ')'])
            if name_and_code not in names:
                names.append(name_and_code)
        return ', '.join(names)

    @property
    def region_names(self):
        regions = self.country_area.select_related('location__region').order_by('location__region__region_name')
        names = []
        for region in regions:
            # try: 
            name = region.region_name # relationship between tables is dots, relationship between variable and a table is also dots
            #name = region.region_name
            if name is None:
                continue
            if name not in names:
                names.append(name)
            # except: 
            #     continue 
        return ', '.join(names)
    

    @property
    def intermediate_region_names(self):
        #irs = self.country_area.select_related('location__intermediate_region').order_by('location__intermediate_region__intermediate_region_name')
        intermediate_regions = self.country_area.select_related('intermediate_region').order_by('intermediate_region_name')
            ## returning ORM queryset iterator 
        names = []
        for intermediate_region in intermediate_regions: # object
            try: # larger try/except look is necessary to deal with none ntypes
                name = intermediate_region.location.intermediate_region.intermediate_region_name
                #name = Pancakes
                # have to explain how to traverse through full dataset (dynamic change)
                if name is None:
                    continue
                if name not in names:
                    names.append(name)
            except: 
                continue

        return ', '.join(names)

        #chnote added intermediate_names function during hw9



    @property
    def sub_region_names(self):
        sub_regions = self.country_area.select_related('location__sub_region').order_by('location__sub_region__sub_region_name')
        names = []
        for sub_region in sub_regions:
            try: 
                name = sub_region.location.sub_region.sub_region_name
                if name is None:
                    continue
                if name not in names:
                    names.append(name)
            except: 
                continue

        return ', '.join(names)


'''
class HeritageSite(models.Model):
    heritage_site_id = models.AutoField(primary_key=True)
    site_name = models.CharField(unique=True, max_length=255)
    description = models.TextField()
    justification = models.TextField(blank=True, null=True)
    date_inscribed = models.TextField(blank=True, null=True)  # This field type is a guess.
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    area_hectares = models.FloatField(blank=True, null=Trpkue)
    heritage_site_category = models.ForeignKey('HeritageSiteCategory', models.DO_NOTHING)
    transboundary = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'heritage_site'
'''


class HeritageSiteCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(unique=True, max_length=25)

    class Meta:
        managed = False
        db_table = 'heritage_site_category'
        ordering = ['category_name']
        verbose_name = 'UNESCO Heritage Site Category'
        verbose_name_plural = 'UNESCO Heritage Site Categories'

    def __str__(self):
        return self.category_name


'''
class HeritageSiteCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(unique=True, max_length=25)

    class Meta:
        managed = False
        db_table = 'heritage_site_category'
'''


class HeritageSiteJurisdiction(models.Model):
    heritage_site_jurisdiction_id = models.AutoField(primary_key=True)
    heritage_site = models.ForeignKey(HeritageSite, models.DO_NOTHING)
    country_area = models.ForeignKey(CountryArea, models.DO_NOTHING)
    location = models.ForeignKey(Location, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'heritage_site_jurisdiction'
        ordering = ['heritage_site', 'country_area']
        verbose_name = 'UNESCO Heritage Site Jurisdiction'
        verbose_name_plural = 'UNESCO Heritage Site Jurisdictions'


'''
class HeritageSiteJurisdiction(models.Model):
    heritage_site_jurisdiction_id = models.AutoField(primary_key=True)
    heritage_site = models.ForeignKey(HeritageSite, models.DO_NOTHING)
    country_area = models.ForeignKey(CountryArea, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'heritage_site_jurisdiction'
'''

class IntermediateRegion(models.Model):
    intermediate_region_id = models.AutoField(primary_key=True)
    intermediate_region_name = models.CharField(unique=True, max_length=100)
    sub_region = models.ForeignKey('SubRegion', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'intermediate_region'
        ordering = ['intermediate_region_name']
        verbose_name = 'UNSD M49 Intermediate Region'
        verbose_name_plural = 'UNSD M49 Intermediate Regions'

    def __str__(self):
        return self.intermediate_region_name


'''
class IntermediateRegion(models.Model):
    intermediate_region_id = models.AutoField(primary_key=True)
    intermediate_region_name = models.CharField(unique=True, max_length=100)
    sub_region = models.ForeignKey('SubRegion', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'intermediate_region'
'''


class Region(models.Model):
    region_id = models.AutoField(primary_key=True)
    region_name = models.CharField(unique=True, max_length=100)
    planet = models.ForeignKey('Planet', models.DO_NOTHING, default=1) #chnote: added 10/2/18

    class Meta:
        managed = False
        db_table = 'region'
        ordering = ['region_name']
        verbose_name = 'UNSD M49 Region'
        verbose_name_plural = 'UNSD M49 Regions'

    def __str__(self):
        return self.region_name
        
    # """
    #     Returns a list of UNSD regions (names only) associated with a Heritage Site.
    #     Note that not all Heritage Sites are associated with a region. In such cases the
    #     Queryset will return as <QuerySet [None]> and the list will need to be checked for
    #     None or a TypeError (sequence item 0: expected str instance, NoneType found) runtime
    #     error will be thrown.
    #     :return: string
    # """




'''
class Region(models.Model):
    region_id = models.AutoField(primary_key=True)
    region_name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'region'
'''


class SubRegion(models.Model):
    sub_region_id = models.AutoField(primary_key=True)
    sub_region_name = models.CharField(unique=True, max_length=100)
    region = models.ForeignKey(Region, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sub_region'
        ordering = ['sub_region_name']
        verbose_name = 'UNSD M49 Subregion'
        verbose_name_plural = 'UNSD M49 Subregions'

    def __str__(self):
        return self.sub_region_name



'''
class SubRegion(models.Model):
    sub_region_id = models.AutoField(primary_key=True)
    sub_region_name = models.CharField(unique=True, max_length=100)
    region = models.ForeignKey(Region, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sub_region'
'''

class Planet(models.Model): #CHnote added 10/2/108
    """
    New model based on Mtg 5 refactoring of the database.
    """
    planet_id = models.AutoField(primary_key=True, unique=True, null=False)
    planet_name = models.CharField(unique=True, null=False, max_length=100)
    unsd_name = models.CharField(null=True, max_length=100)

    class Meta:
        managed = False   #<-- #YOU MUST SET managed TO FALSE
        db_table = 'planet'
        ordering = ['planet_name']
        verbose_name = 'Planet we are on'
        verbose_name_plural = 'Planets we are on'

    def __str__(self):
        return self.planet_name #<-- MUST RETURN A STRING

