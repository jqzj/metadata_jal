# ICPSR Metadata API Documentation

## Under Development: A New API to Export Metadata!

ICPSR is developing a new application programming interface (API) so that community members can perform bulk exports of metadata records. This new API will:
 - Simplify and standardize the process of accessing metadata records.
 - Allow ICPSR to provide metadata in a broader range of standards and formats.
 - Support more complex queries so that users can find the metadata records that best meet their needs.

## ICPSR Metadata API Mappings

Upon its release, the ICPSR Metadata API will produce records that conform to the following standards (with more to come in the future): 
 - [DCAT-US](https://resources.data.gov/resources/dcat-us/)
 - [MARCXML](https://www.loc.gov/standards/marcxml/)
 - [Dublin Core](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/). 

This [Metadata API Mappings](https://docs.google.com/spreadsheets/d/1Avw212FfzxRjsUFvlJOLtsJclKeL8VJc0pbhLQevXg8/edit?usp=sharing) spreadsheet provides more information about how ICPSR metadata elements align with the above-mentioned standards. 

## Additional Mapping Details

### Geographic Coverage Area

The current version of DCAT-US only permits a single value for the [spatial](https://resources.data.gov/resources/dcat-us/#spatial) metadata element. In cases where a study has multiple Geographic Coverage Area entries, ICPSR will use the term "Multiple" in the 'spatial' property and then add all the terms to an array in the 'spatialExt' property, an ICPSR-specific extension of the the base DCAT-US schema.

### Time Period: Dates

#### Dublin Core and MARCXML Modifications

While ICPSR's [Time Period](https://icpsr.github.io/metadata/icpsr_study_schema/#18-time-period) element is repeatable, not all metadata standards permit multiple date elements or allow structured descriptive text to contextualize multiple dates. To better align with the Dublin Core and MARCXML standards and simplify the presentation of time period information, ICPSR will collapse multiple time periods into a single date range representing the earliest and latest dates to which the data refer.

#### DCAT-US Modifications

The current version of DCAT-US only permits a single value for the [temporal](https://resources.data.gov/resources/dcat-us/#temporal) metadata element. In cases where a study has multiple Time Period entries, ICPSR will collapse them into a single date range (representing the earliest and latest dates to which the data refer) and use that value for the 'temporal' property. Each individual Time Period entry will then be added to an array in the 'temporalExt' property, an ICPSR-specific extension of the the base DCAT-US schema.

#### Restrictions

ICPSRWe make a valiant effort by incorporating information about (a) member vs. public and (b) restricted access vs. direct download in the DDI <restrctn> field, but it would require some custom coding to parse out the info. Here's a breakdown of how we handle this field:

(a) If ICPSR membership is required, <restrctn> will start with the string "Available to ICPSR member institutions."; if not, it will start with "Available to the general public."

b) If there are no additional access restrictions (i.e., the 'restricted' flag in the API's source metadata is 'false') then there will be no additional text.  If there are access restrictions (i.e., the 'restricted' flag is 'true') there will be additional text (the content of our 'Restrictions' metadata field, along with boiler text to 'Visit [study DOI] to apply for access to restricted data.'

Here are examples of how these would actually look (using dummy data/fake DOIs):
No membership and direct download:  <restrctn>"Available to the general public."</restrctn>
Membership and direct download  :  <restrctn>" Available to ICPSR member institutions."</restrctn>
No membership and access restriction:  <restrctn>"Available to the general public. These data may not be used for any purpose other than statistical reporting and analysis. Use of these data to learn the identity of any person or establishment is strictly prohibited. To protect respondent privacy, certain files within this data collection are restricted from general dissemination. To obtain these files, researchers must agree to the terms and conditions of a Restricted Data Use Agreement in accordance with existing ICPSR servicing policies. Visit https;//actual-study-doi to apply for access to restricted data." </restrctn>
Membership and access restriction:  <restrctn>" Available to ICPSR member institutions.  These data may not be used for any purpose other than statistical reporting and analysis. Use of these data to learn the identity of any person or establishment is strictly prohibited. To protect respondent privacy, certain files within this data collection are restricted from general dissemination. To obtain these files, researchers must agree to the terms and conditions of a Restricted Data Use Agreement in accordance with existing ICPSR servicing policies. Visit https;//actual-study-doi to apply for access to restricted data."</restrctn>