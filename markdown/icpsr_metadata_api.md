# ICPSR Metadata API Documentation

## Under Development: A New API to Export Metadata!

ICPSR is developing a new application programming interface (API) so that community members can perform bulk exports of metadata records. This new API will:

  - Simplify and standardize the process of accessing metadata records.
  - Allow ICPSR to provide metadata in a broader range of standards and formats.
  - Support more complex queries so that users can find the metadata records that best meet their needs.

## ICPSR Metadata API Mappings

Upon its release, the ICPSR Metadata API will produce records that conform to the following standards (with more to come in the future): 

  - [DCAT-US](https://resources.data.gov/resources/dcat-us/): a U.S. government extension of the Data Catalog Vocabulary (DCAT), designed to improve the discoverability and interoperability of federal open data. It provides a standardized way to describe datasets, data services, and distributions using RDF-based metadata, ensuring consistency across data catalogs like data.gov. This standard aligns with international best practices while incorporating specific requirements for U.S. government data publishing.
  - [MARCXML](https://www.loc.gov/standards/marcxml/): an XML-based representation of the MARC (Machine-Readable Cataloging) standard, developed by the Library of Congress for bibliographic and authority data. It preserves the structure and semantics of MARC records while enabling interoperability with modern XML-based systems. This format allows libraries and archives to exchange, transform, and integrate catalog data more easily with digital repositories and web technologies.
  - [Dublin Core](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/): a simple yet flexible schema for describing digital and physical resources, widely used for interoperability across different information systems. Designed to enhance resource discovery and metadata sharing, Dublin Core is commonly used in libraries, data repositories, and web-based metadata applications. 

This [Metadata API Mappings](https://docs.google.com/spreadsheets/d/1Avw212FfzxRjsUFvlJOLtsJclKeL8VJc0pbhLQevXg8/edit?usp=sharing) spreadsheet provides more information about how ICPSR metadata elements align with the above-mentioned standards. 

## Element-Specific Mapping Notes  

This section provides additional information about non-standard mappings from ICPSR's local metadata schema to various export schemas available via the API.

### Geographic Coverage Area

The current version of DCAT-US only permits a single value for the [spatial](https://resources.data.gov/resources/dcat-us/#spatial) metadata element. In cases where a study has multiple Geographic Coverage Area entries, ICPSR will use the term "Multiple" in the 'spatial' property and then add all the terms to an array in the 'spatialExt' property, an ICPSR-specific extension of the the base DCAT-US schema.

### Time Period: Dates

*Dublin Core and MARCXML Date Expressions:* While ICPSR's [Time Period](https://icpsr.github.io/metadata/icpsr_study_schema/#18-time-period) element is repeatable, not all metadata standards permit multiple date elements or allow structured descriptive text to contextualize multiple date values. To better align with the Dublin Core and MARCXML standards and simplify the presentation of time period information, ICPSR will collapse multiple time periods into a single date range representing the earliest and latest dates to which the data refer.

*DCAT-US Date Expressions:* The current version of DCAT-US only permits a single value for the [temporal](https://resources.data.gov/resources/dcat-us/#temporal) metadata element. In cases where a study has multiple Time Period entries, ICPSR will collapse them into a single date range (representing the earliest and latest dates to which the data refer) and use that value for the 'temporal' property. Each individual Time Period entry will then be added to an array in the 'temporalExt' property, an ICPSR-specific extension of the the base DCAT-US schema.

### Restrictions

ICPSR's information about _data availability_ (i.e., the availability of data for members-only vs. the general public) and _restriction type_ (i.e., restricted use vs. public use) are maintained in system administrative metadata (as opposed to study-level metadata). These details are combined with Restriction statements in relevant metadata elements for the various export schema, using the following conventions: 

  - If ICPSR membership is required, the property value will start with the string "Available to ICPSR member institutions."; if not, it will start with "Available to the general public."

  - If there are additional use restrictions, the content of the Restrictions metadata field will be appended, along with a hyperlink to the study's home page for more information. 

Here are examples of how these statements appear in metadata exports:

| Conditions | Example Values |
|----------- | -------------- |
| No membership requirement and no use restriction | "Available to the general public." |
| Membership requirement and no use restriction | "Available to ICPSR member institutions." |
| No membership requirement with a use restriction | "Available to the general public. Access to these data is restricted. Users interested in obtaining these data must complete a Restricted Data Use Agreement, specify the reason for the request, and obtain IRB approval or notice of exemption for their research. Visit [https://doi.org/10.3886/ICPSR37328.v1](https://doi.org/10.3886/ICPSR37328.v1) to apply for access to restricted data." |
| Membership requirement with a use restriction | "Available to ICPSR member institutions. This data collection may not be used for any purpose other than statistical reporting and analysis. Use of these data to learn the identity of any person or establishment is prohibited. To protect respondent privacy, all data files in this collection are restricted from general dissemination. To obtain these restricted files, researchers must agree to the terms and conditions of a Restricted Data Use Agreement. Visit [https://doi.org/10.3886/ICPSR37229.v1](https://doi.org/10.3886/ICPSR37229.v1) to apply for access to restricted data."</restrctn>