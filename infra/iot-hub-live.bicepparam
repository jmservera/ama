using './iot-hub-live.bicep'

// Existing development exercise only, not a production or main deployment profile.
// B1 USD10/month; <=USD1 attributed hub cost through 2026-10-31, within USD5 additional.
// No service SAS, additional namespace, private endpoint, role assignment or app change.
param name = 'iot-cutover-test-rzsrg'
param location = 'uksouth'
param skuName = 'B1'
param unitCount = 1
