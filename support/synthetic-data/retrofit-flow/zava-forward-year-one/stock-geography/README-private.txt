PRIVATE REPOSITORY DATA - DO NOT PUBLISH OR MAKE THE REPOSITORY PUBLIC

This dataset contains real OpenStreetMap address details combined with
fictional property, tenure and condition attributes. Keep it only in the
private repository; do not publish or expose it externally.

Purpose
This folder extends the Zava Forward synthetic example with a 60,000-row full-stock scenario and a map-ready address overlay. The existing one-year operational CSVs in the repository were not changed and are intentionally not joined to real addresses in this file.

Geographic framing
The case study gives only a North of England operating region, not a company boundary. This scenario uses a fictional composite of 12 North East England local-authority areas: Newcastle upon Tyne, Gateshead, North Tyneside, South Tyneside, Sunderland, County Durham, Northumberland, Hartlepool, Middlesbrough, Redcar and Cleveland, Stockton-on-Tees and Darlington. The urban-core, former industrial/coalfield town, and rural/coastal themes are illustrative; they are not Zava North Homes service areas.

Sources
* Census 2021 TS054, ONS/Nomis, local-authority household tenure (Census day 21 March 2021). Council and other social rented categories are summed, as the ONS recommends. URL: https://www.nomisweb.co.uk/datasets/c2021ts054
* English Indices of Deprivation 2025, MHCLG, LSOA ranks/scores/deciles (published 30 October 2025; corrected files used). URL: https://www.gov.uk/government/statistics/english-indices-of-deprivation-2025
* ONS LSOA 2021 BGC V5 and LAD December 2021 BFC boundaries. URLs: https://geoportal.statistics.gov.uk/ and https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Lower_layer_Super_Output_Areas_December_2021_Boundaries_EW_BGC_V5/FeatureServer
* OpenStreetMap address-bearing building/map objects retrieved 30 September 2026 using the Overpass API. OSM data is ODbL 1.0. Attribution: Contains OpenStreetMap data © OpenStreetMap contributors. License: https://www.openstreetmap.org/copyright
* Modelled portfolio-category mix from the project’s Company Profile Research. These are owner-modelled estimates, not company facts. The 74% EPC C-or-above / 26% below-C split is an English social-rented planning benchmark, not a Zava North Homes asset-register result.

Placement method
Local-authority allocations start from Census 2021 social-rented household counts and are capacity-adjusted to the address-bearing OSM points available in the area. Within each authority, point selection is weighted toward LSOAs in lower IMD 2025 deciles, but no decile is treated as proof of tenure and higher-decile areas are not automatically excluded. This is a synthetic allocation rule, not an inferred Zava North Homes distribution. Address coverage and tagging in OSM vary by authority; the local-authority summary records the resulting capacity adjustment.

Synthetic attributes and limits
Every tenure, portfolio category, EPC need group and neighbourhood pattern in the register is synthetic. No public source identifies which individual UPRNs/buildings are social housing or belong to a specific landlord. The real address/coordinate is only a map anchor; it does not mean the real building has the simulated tenure, EPC status, occupancy or work history. OSM includes imperfect/incomplete tags and some address nodes have no verified residential-use tag; review the location-quality field. Synthetic clusters are statistical groupings inside LSOAs, not mapped real estates. IMD 2025 is a current deprivation snapshot; no 2019-to-2025 trend is claimed.

The operational 12-month work dataset remains separate and unchanged. No case, resident, safety, complaint or contractor event has been attached to a real address.
