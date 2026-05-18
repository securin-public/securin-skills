<!-- Mirrored from skills/_shared/groupby-allowlist.md. Do not edit here — edit the source and run scripts/sync-shared.sh. -->

## GroupBy Aggregation Columns

This file is the **allowlist of aggregate column ids** for deeplinks
generated from aggregation tool calls. It is referenced from
`deep-links.md` whenever a group-by deeplink is being composed — see
the **Group-By Deeplinks** section there for the surrounding rules.

These are the ONLY valid aggregate column ids you may place in
`view.view.columns[].id` when the deeplink's `view.view.groupBy` field
is set. Exactly one column in the deeplink — the one that displays the
grouped dimension — uses a regular apiField path (the same path you
set on `view.view.groupBy`) as its `id`; every OTHER column's `id`
MUST come from this list.

Pick the composite-mode list when the upstream call was
`Securin__assetQuery` / `Securin__exposureQuery`; pick the source-mode
list when it was any `Securin__aggregate*Data` tool. Never mix the two
within a single deeplink payload.

The `aggregate:` line under each entry is metadata only — it describes
what the platform computes for that column (function, the field it
operates over, and any built-in filters). **Do NOT copy it into the
deeplink tool call.** The columns object structure stays the same as
documented in `deep-links.md` (`id`, `name`, `order`, `isHidden`,
`width: 180`, optional `sort`); only the `id` is drawn from here.

### Composite mode 

- `COMPOSITE_ACTIVE_ASSETS` — "Active Assets"
    - aggregate: function=`COUNT`, over=`compositeAsset.id`, filters=`compositeAsset.status = "Active"`
  - `COMPOSITE_ASSETS` — "Assets"
    - aggregate: function=`COUNT`, over=`compositeAsset.id`
  - `COMPOSITE_ASSET_FIRST_DISCOVERED` — "Asset First Discovered On"
    - aggregate: function=`MIN`, over=`compositeAsset.firstDiscoveredOn`
  - `COMPOSITE_ASSET_FIRST_INGESTED` — "Asset First Ingested On"
    - aggregate: function=`MIN`, over=`compositeAsset.firstIngestedOn`
  - `COMPOSITE_ASSET_LAST_DISCOVERED` — "Asset Last Discovered On"
    - aggregate: function=`MAX`, over=`compositeAsset.lastDiscoveredOn`
  - `COMPOSITE_ASSET_LAST_INGESTED` — "Asset Last Ingested On"
    - aggregate: function=`MAX`, over=`compositeAsset.lastIngestedOn`
  - `COMPOSITE_CISA_KEV_EXPOSURES` — "Exposures with CISA KEVs"
    - aggregate: function=`COUNT`, over=`compositeExposure.id`, filters=`vulnerabilities.isCisaKEV = "true" AND compositeExposure.status = "Open"`
  - `COMPOSITE_CLOSED_EXPOSURES` — "Closed Exposures"
    - aggregate: function=`COUNT`, over=`compositeExposure.id`, filters=`compositeExposure.status = "Closed"`
  - `COMPOSITE_CRITICAL_SCORE_EXPOSURES` — "Critical"
    - aggregate: function=`COUNT`, over=`compositeExposure.id`, filters=`compositeExposure.scores.scoreLevel = "Critical" AND compositeExposure.status = "Open"`
  - `COMPOSITE_DECOMMISSIONED_ASSETS` — "Decommissioned Assets"
    - aggregate: function=`COUNT`, over=`compositeAsset.id`, filters=`compositeAsset.lifeCycleState = "Decommissioned"`
  - `COMPOSITE_DECOMMISSIONED_EXPOSURES` — "Decommissioned Exposures"
    - aggregate: function=`COUNT`, over=`compositeExposure.id`, filters=`compositeExposure.lifeCycleState = "Decommissioned"`
  - `COMPOSITE_DISCOVERY_ON_TRACK` — "On Track (Discovery)"
    - aggregate: function=`COUNT`, over=`compositeAsset.id`, filters=`compositeAsset.status = "Active" AND compositeAsset.discoveryTarget.status = "On Track"`
  - `COMPOSITE_DISCOVERY_OVERDUE` — "Overdue (Discovery)"
    - aggregate: function=`COUNT`, over=`compositeAsset.id`, filters=`compositeAsset.status = "Active" AND compositeAsset.discoveryTarget.status = "Overdue"`
  - `COMPOSITE_DORMANT_ASSETS` — "Dormant Assets"
    - aggregate: function=`COUNT`, over=`compositeAsset.id`, filters=`compositeAsset.lifeCycleState = "Dormant"`
  - `COMPOSITE_EXPLOITABLE_ASSETS` — "Assets with Exploitable Exposures"
    - aggregate: function=`COUNT`, over=`compositeAsset.id`, filters=`compositeAsset.status = "Active" AND vulnerabilities.hasExploit = "true"`
  - `COMPOSITE_EXPLOITABLE_EXPOSURES` — "Exploitable Exposures"
    - aggregate: function=`COUNT`, over=`compositeExposure.id`, filters=`vulnerabilities.hasExploit = "true"  AND compositeExposure.status = "Open"`
  - `COMPOSITE_EXPLOITS` — "Exploits"
    - aggregate: function=`CARDINALITY`, over=`vulnerabilities.exploits.title`, filters=`compositeExposure.status = "Open"`
  - `COMPOSITE_FIRST_DISCOVERED` — "Exposure First Discovered On"
    - aggregate: function=`MIN`, over=`compositeExposure.firstDiscoveredOn`
  - `COMPOSITE_FIRST_INGESTED` — "Exposure First Ingested On"
    - aggregate: function=`MIN`, over=`compositeExposure.firstIngestedOn`
  - `COMPOSITE_FIXES` — "Fixes"
    - aggregate: function=`CARDINALITY`, over=`compositeExposure.sources.mappedAttributes.vendorRemediation`, filters=`compositeExposure.status = "Open"`
  - `COMPOSITE_HIGH_SCORE_EXPOSURES` — "High"
    - aggregate: function=`COUNT`, over=`compositeExposure.id`, filters=`compositeExposure.scores.scoreLevel = "High" AND compositeExposure.status = "Open"`
  - `COMPOSITE_INACTIVE_ASSETS` — "Inactive Assets"
    - aggregate: function=`COUNT`, over=`compositeAsset.id`, filters=`compositeAsset.status = "Inactive"`
  - `COMPOSITE_INFO_SCORE_EXPOSURES` — "Info"
    - aggregate: function=`COUNT`, over=`compositeExposure.id`, filters=`compositeExposure.scores.scoreLevel = "Info" AND compositeExposure.status = "Open"`
  - `COMPOSITE_LAST_DISCOVERED` — "Exposure Last Discovered On"
    - aggregate: function=`MAX`, over=`compositeExposure.lastDiscoveredOn`
  - `COMPOSITE_LAST_INGESTED` — "Exposure Last Ingested On"
    - aggregate: function=`MAX`, over=`compositeExposure.lastIngestedOn`
  - `COMPOSITE_LOW_SCORE_EXPOSURES` — "Low"
    - aggregate: function=`COUNT`, over=`compositeExposure.id`, filters=`compositeExposure.scores.scoreLevel = "Low" AND compositeExposure.status = "Open"`
  - `COMPOSITE_MALWARE` — "Malware"
    - aggregate: function=`CARDINALITY`, over=`vulnerabilities.malwares.title`, filters=`compositeExposure.status = "Open"`
  - `COMPOSITE_MALWARE_ASSETS` — "Assets with Malware"
    - aggregate: function=`COUNT`, over=`compositeAsset.id`, filters=`compositeAsset.status = "Active" AND vulnerabilities.hasMalware= "true"`
  - `COMPOSITE_MALWARE_EXPOSURES` — "Malware Exposures"
    - aggregate: function=`COUNT`, over=`compositeExposure.id`, filters=`vulnerabilities.hasMalware = "true" AND compositeExposure.status = "Open"`
  - `COMPOSITE_MAX_EXPOSURE_SCORE` — "Max Score"
    - aggregate: function=`MAX`, over=`compositeExposure.scores.score`
  - `COMPOSITE_MEAN_TIME_TO_ROUTE` — "Mean Time to Route"
    - aggregate: function=`AVG`, over=`compositeExposure.sources.assignments.timeToAssign`
  - `COMPOSITE_MEDIUM_SCORE_EXPOSURES` — "Medium"
    - aggregate: function=`COUNT`, over=`compositeExposure.id`, filters=`compositeExposure.scores.scoreLevel = "Medium" AND compositeExposure.status = "Open"`
  - `COMPOSITE_MIXED_ASSETS` — "Mixed Assets"
    - aggregate: function=`COUNT`, over=`compositeAsset.id`, filters=`compositeAsset.lifeCycleState = "Mixed"`
  - `COMPOSITE_MIXED_EXPOSURES` — "Mixed Exposures"
    - aggregate: function=`COUNT`, over=`compositeExposure.id`, filters=`compositeExposure.lifeCycleState = "Mixed"`
  - `COMPOSITE_MONITORED_ASSETS` — "Monitored Assets"
    - aggregate: function=`COUNT`, over=`compositeAsset.id`, filters=`compositeAsset.lifeCycleState = "Monitored"`
  - `COMPOSITE_NEW_EXPOSURES` — "New Exposures"
    - aggregate: function=`COUNT`, over=`compositeExposure.id`, filters=`compositeExposure.lifeCycleState = "New"`
  - `COMPOSITE_OPEN_EXPOSURES` — "Exposures"
    - aggregate: function=`COUNT`, over=`compositeExposure.id`, filters=`compositeExposure.status = "Open"`
  - `COMPOSITE_PERSISTENT_EXPOSURES` — "Persistent Exposures"
    - aggregate: function=`COUNT`, over=`compositeExposure.id`, filters=`compositeExposure.lifeCycleState = "Persistent"`
  - `COMPOSITE_RANSOMWARE_ASSETS` — "Assets with Ransomware"
    - aggregate: function=`COUNT`, over=`compositeAsset.id`, filters=`compositeAsset.status = "Active" AND vulnerabilities.hasRansomware= "true"`
  - `COMPOSITE_RANSOMWARE_EXPOSURES` — "Ransomware Exposures"
    - aggregate: function=`COUNT`, over=`compositeExposure.id`, filters=`vulnerabilities.hasRansomware= "true" AND compositeExposure.status = "Open"`
  - `COMPOSITE_RCE_PE_ASSETS` — "Assets with RCE/PE"
    - aggregate: function=`COUNT`, over=`compositeAsset.id`, filters=`compositeAsset.status = "Active" AND vulnerabilities.threats.attackClassifications in ("RCE", "PE")`
  - `COMPOSITE_RCE_PE_EXPOSURES` — "Exposures with RCE/PE"
    - aggregate: function=`COUNT`, over=`compositeExposure.id`, filters=`vulnerabilities.threats.attackClassifications in ("RCE", "PE")  AND compositeExposure.status = "Open"`
  - `COMPOSITE_REMEDIATION_MET` — "Met (Remediation)"
    - aggregate: function=`COUNT`, over=`compositeExposure.id`, filters=`compositeExposure.remediationTarget.status = "Met"`
  - `COMPOSITE_REMEDIATION_MISSED` — "Missed (Remediation)"
    - aggregate: function=`COUNT`, over=`compositeExposure.id`, filters=`compositeExposure.remediationTarget.status = "Missed"`
  - `COMPOSITE_REMEDIATION_ON_TRACK` — "On Track (Remediation)"
    - aggregate: function=`COUNT`, over=`compositeExposure.id`, filters=`compositeExposure.remediationTarget.status = "On Track"`
  - `COMPOSITE_REMEDIATION_OVERDUE` — "Overdue ( Remediation)"
    - aggregate: function=`COUNT`, over=`compositeExposure.id`, filters=`compositeExposure.remediationTarget.status = "Overdue"`
  - `COMPOSITE_REMEDIATION_P1_OPEN` — "P1 Exposures (Remediation)"
    - aggregate: function=`COUNT`, over=`compositeExposure.id`, filters=`compositeExposure.remediationTarget.priority = "P1" AND compositeExposure.status = "Open"`
  - `COMPOSITE_REOPEN_EXPOSURES` — "Reopened Exposures"
    - aggregate: function=`COUNT`, over=`compositeExposure.id`, filters=`compositeExposure.lifeCycleState = "Reopened"`
  - `COMPOSITE_RESOLVED_EXPOSURES` — "Resolved Exposures"
    - aggregate: function=`COUNT`, over=`compositeExposure.id`, filters=`compositeExposure.lifeCycleState = "Resolved"`
  - `COMPOSITE_ROUTING_MET` — "Met (Routing)"
    - aggregate: function=`COUNT`, over=`compositeExposure.id`, filters=`compositeExposure.routingTarget.status = "Met"`
  - `COMPOSITE_ROUTING_MISSED` — "Missed (Routing)"
    - aggregate: function=`COUNT`, over=`compositeExposure.id`, filters=`compositeExposure.routingTarget.status = "Missed"`
  - `COMPOSITE_ROUTING_NOT_ROUTED` — "Not Routed"
    - aggregate: function=`COUNT`, over=`compositeExposure.id`, filters=`compositeExposure.routingTarget.status = "Not Routed"`
  - `COMPOSITE_ROUTING_ON_TRACK` — "On Track (Routing)"
    - aggregate: function=`COUNT`, over=`compositeExposure.id`, filters=`compositeExposure.routingTarget.status = "On Track"`
  - `COMPOSITE_ROUTING_OVERDUE` — "Overdue (Routing)"
    - aggregate: function=`COUNT`, over=`compositeExposure.id`, filters=`compositeExposure.routingTarget.status = "Overdue"`
  - `COMPOSITE_SECURIN_KEV_EXPOSURES` — "Exposures with Securin KEVs"
    - aggregate: function=`COUNT`, over=`compositeExposure.id`, filters=`vulnerabilities.isExploitedInTheWild = "true"  AND compositeExposure.status = "Open"`
  - `COMPOSITE_SUPPRESSED_EXPOSURES` — "Suppressed Exposures"
    - aggregate: function=`COUNT`, over=`compositeExposure.id`, filters=`compositeExposure.lifeCycleState = "Suppressed"`
  - `COMPOSITE_THREATS` — "Threats"
    - aggregate: function=`CARDINALITY`, over=`vulnerabilities.threats.title`, filters=`compositeExposure.status = "Open"`
  - `COMPOSITE_THREAT_ASSETS` — "Assets with Threats"
    - aggregate: function=`COUNT`, over=`compositeAsset.id`, filters=`compositeAsset.status = "Active" AND vulnerabilities.hasThreat= "true"`
  - `COMPOSITE_TOTAL_EXPOSURES` — "Total Exposures"
    - aggregate: function=`COUNT`, over=`compositeExposure.id`
  - `COMPOSITE_TRENDING_ASSETS` — "Assets with Trending CVEs"
    - aggregate: function=`COUNT`, over=`compositeAsset.id`, filters=`compositeAsset.status = "Active" AND vulnerabilities.threats.lastTrendingDate > today() - 7`
  - `COMPOSITE_TRENDING_CVE_EXPOSURES` — "Exposures with Trending CVEs"
    - aggregate: function=`COUNT`, over=`compositeExposure.id`, filters=`compositeExposure.status = "Open" AND vulnerabilities.threats.lastTrendingDate > today() - 7`
  - `COMPOSITE_USER_RESOLVED_EXPOSURES` — "User Resolved Exposures"
    - aggregate: function=`COUNT`, over=`compositeExposure.id`, filters=`compositeExposure.lifeCycleState = "User Resolved"`
  - `COMPOSITE_VULNERABILITY_COUNT` — "Unique CVEs"
    - aggregate: function=`CARDINALITY`, over=`vulnerabilities.id`, filters=`compositeExposure.status = "Open"`
  - `COMPOSITE_WEAKNESS_COUNT` — "Unique CWEs"
    - aggregate: function=`CARDINALITY`, over=`weaknesses.id`, filters=`compositeExposure.status = "Open"`
  - `COMPOSITE_WORKSPACES` — "Workspaces"
    - aggregate: function=`TERMS`, over=`compositeAsset.workspaces.name`


### Source mode

- `ACTIVE_ASSETS` — "Active Assets"
    - aggregate: function=`COUNT`, over=`asset.assetId`, filters=`asset.status = "Active"`
  - `ACTIVE_EXPOSURES` — "Active Exposures"
    - aggregate: function=`COUNT`, over=`exposure.exposureId`, filters=`exposure.lifeCycleState = "Active"`
  - `ASSETS` — "Assets"
    - aggregate: function=`COUNT`, over=`asset.assetId`
  - `ASSET_FIRST_DISCOVERED` — "Asset First Discovered On"
    - aggregate: function=`MIN`, over=`asset.firstDiscoveredOn`
  - `ASSET_FIRST_INGESTED` — "Asset First Ingested On"
    - aggregate: function=`MIN`, over=`asset.firstIngestedOn`
  - `ASSET_LAST_DISCOVERED` — "Asset Last Discovered On"
    - aggregate: function=`MAX`, over=`asset.lastDiscoveredOn`
  - `ASSET_LAST_INGESTED` — "Asset Last Ingested On"
    - aggregate: function=`MAX`, over=`asset.lastIngestedOn`
  - `ASSET_SOURCES` — "Sources"
    - aggregate: function=`TERMS`, over=`asset.integration.definitionID`
  - `ASSET_TAGS_COUNT` — "Tags"
    - aggregate: function=`CARDINALITY`
  - `CISA_KEV_EXPOSURES` — "CISA KEV"
    - aggregate: function=`COUNT`, over=`exposure.exposureId`, filters=`vulnerabilities.isCisaKEV = "true"`
  - `CLOSED_EXPOSURES` — "Closed Exposures"
    - aggregate: function=`COUNT`, over=`exposure.exposureId`, filters=`exposure.status = "Closed"`
  - `CRITICAL_SCORE_EXPOSURES` — "Critical"
    - aggregate: function=`COUNT`, over=`exposure.exposureId`, filters=`exposure.scores.scoreLevel = "Critical"`
  - `DECOMMISSIONED_ASSETS` — "Decommissioned Assets"
    - aggregate: function=`COUNT`, over=`asset.assetId`, filters=`asset.lifeCycleState = "Decommissioned"`
  - `DECOMMISSIONED_EXPOSURES` — "Decommissioned Exposures"
    - aggregate: function=`COUNT`, over=`exposure.exposureId`, filters=`exposure.lifeCycleState = "Decommissioned"`
  - `DISCOVERY_ON_TRACK` — "On Track (Discovery)"
    - aggregate: function=`COUNT`, over=`asset.assetId`, filters=`asset.discoveryTarget.status = "On Track"`
  - `DISCOVERY_OVERDUE` — "Overdue (Discovery)"
    - aggregate: function=`COUNT`, over=`asset.assetId`, filters=`asset.discoveryTarget.status = "Overdue"`
  - `DORMANT_ASSETS` — "Dormant Assets"
    - aggregate: function=`COUNT`, over=`asset.assetId`, filters=`asset.lifeCycleState = "Dormant"`
  - `EXPLOITABLE_ASSETS` — "Exploitable Assets"
    - aggregate: function=`COUNT`, over=`asset.assetId`, filters=`vulnerabilities.threats.type = "exploit"`
  - `EXPLOITABLE_EXPOSURES` — "Exploitable Exposures"
    - aggregate: function=`COUNT`, over=`exposure.exposureId`, filters=`vulnerabilities.threats.type = "exploit"`
  - `EXPOSURES` — "Total Exposures"
    - aggregate: function=`COUNT`, over=`exposure.exposureId`
  - `FIRST_DISCOVERED` — "Exposure First Discovered On"
    - aggregate: function=`MIN`, over=`exposure.firstDiscoveredOn`
  - `FIRST_INGESTED` — "Exposure First Ingested On"
    - aggregate: function=`MIN`, over=`exposure.firstIngestedOn`
  - `HIGH_SCORE_EXPOSURES` — "High"
    - aggregate: function=`COUNT`, over=`exposure.exposureId`, filters=`exposure.scores.scoreLevel = "High"`
  - `INFO_SCORE_EXPOSURES` — "Info"
    - aggregate: function=`COUNT`, over=`exposure.exposureId`, filters=`exposure.scores.scoreLevel = "Info"`
  - `LAST_DISCOVERED` — "Exposure Last Discovered On"
    - aggregate: function=`MAX`, over=`exposure.lastDiscoveredOn`
  - `LAST_INGESTED` — "Exposure Last Ingested On"
    - aggregate: function=`MAX`, over=`exposure.lastIngestedOn`
  - `LOW_SCORE_EXPOSURES` — "Low"
    - aggregate: function=`COUNT`, over=`exposure.exposureId`, filters=`exposure.scores.scoreLevel = "Low"`
  - `MALWARE_EXPOSURES` — "Malware Exposures"
    - aggregate: function=`COUNT`, over=`exposure.exposureId`, filters=`vulnerabilities.threats.type = "malware"`
  - `MAX_EXPOSURE_SCORE` — "Max Score"
    - aggregate: function=`MAX`, over=`exposure.scores.score`
  - `MEAN_TIME_TO_REMEDIATE` — "Mean Time to Remediate"
    - aggregate: function=`AVG`, over=`exposure.timeToRemediate`, filters=`exposure.status = "Closed"`
  - `MEAN_TIME_TO_ROUTE` — "Mean Time to Route"
    - aggregate: function=`AVG`, over=`exposure.timeToAssign`
  - `MEAN_TIME_TO_SCAN` — "Mean Time to Discover"
    - aggregate: function=`AVG`, over=`asset.timeToScan`
  - `MEDIUM_SCORE_EXPOSURES` — "Medium"
    - aggregate: function=`COUNT`, over=`exposure.exposureId`, filters=`exposure.scores.scoreLevel = "Medium"`
  - `MONITORED_ASSETS` — "Monitored Assets"
    - aggregate: function=`COUNT`, over=`asset.assetId`, filters=`asset.lifeCycleState = "Monitored"`
  - `NEW_EXPOSURES` — "New Exposures"
    - aggregate: function=`COUNT`, over=`exposure.exposureId`, filters=`exposure.lifeCycleState = "New"`
  - `OPEN_CISA_KEV_EXPOSURES` — "Open CISA KEV Exposures"
    - aggregate: function=`COUNT`, over=`exposure.exposureId`, filters=`vulnerabilities.isCisaKEV = "true" and exposure.status = "Open"`
  - `OPEN_EXPOSURES` — "Open Exposures"
    - aggregate: function=`COUNT`, over=`exposure.exposureId`, filters=`exposure.status = "Open"`
  - `OPEN_RANSOMWARE_EXPOSURES` — "Open Ransomware Exposures"
    - aggregate: function=`COUNT`, over=`exposure.exposureId`, filters=`vulnerabilities.threats.subType = "ransomware" and exposure.status = "Open"`
  - `OPEN_SECURIN_KEV_EXPOSURES` — "Open Securin KEV Exposures"
    - aggregate: function=`COUNT`, over=`exposure.exposureId`, filters=`vulnerabilities.isExploitedInTheWild = "true" and exposure.status = "Open"`
  - `PERSISTENT_EXPOSURES` — "Persistent Exposures"
    - aggregate: function=`COUNT`, over=`exposure.exposureId`, filters=`exposure.lifeCycleState = "Persistent"`
  - `RANSOMWARE_ASSETS` — "Ransomware Assets"
    - aggregate: function=`COUNT`, over=`asset.assetId`, filters=`exposure.status = "Open" AND  vulnerabilities.threats.subType = "ransomware"`
  - `RANSOMWARE_EXPOSURES` — "Ransomware Exposures"
    - aggregate: function=`COUNT`, over=`exposure.exposureId`, filters=`vulnerabilities.threats.subType = "ransomware"`
  - `RCE_PE_EXPOSURES` — "RCE/PE Exposures"
    - aggregate: function=`COUNT`, over=`exposure.exposureId`, filters=`vulnerabilities.threats.attackClassifications in ("RCE", "PE")`
  - `REMEDIATION_MET` — "Met (Remediation)"
    - aggregate: function=`COUNT`, over=`exposure.exposureId`, filters=`exposure.remediationTarget.status = "Met"`
  - `REMEDIATION_MISSED` — "Missed (Remediation)"
    - aggregate: function=`COUNT`, over=`exposure.exposureId`, filters=`exposure.remediationTarget.status = "Missed"`
  - `REMEDIATION_ON_TRACK` — "On Track (Remediation)"
    - aggregate: function=`COUNT`, over=`exposure.exposureId`, filters=`exposure.remediationTarget.status = "On Track"`
  - `REMEDIATION_OVERDUE` — "Overdue ( Remediation)"
    - aggregate: function=`COUNT`, over=`exposure.exposureId`, filters=`exposure.remediationTarget.status = "Overdue"`
  - `REMEDIATION_P1_OPEN` — "P1 Exposures (Remediation)"
    - aggregate: function=`COUNT`, over=`exposure.exposureId`, filters=`exposure.remediationTarget.priority = "P1" AND exposure.status = "Open"`
  - `REOPEN_EXPOSURES` — "Reopened Exposures"
    - aggregate: function=`COUNT`, over=`exposure.exposureId`, filters=`exposure.lifeCycleState = "Reopened"`
  - `RESOLVED_EXPOSURES` — "Resolved Exposures"
    - aggregate: function=`COUNT`, over=`exposure.exposureId`, filters=`exposure.lifeCycleState = "Resolved"`
  - `ROUTING_MET` — "Met (Routing)"
    - aggregate: function=`COUNT`, over=`exposure.exposureId`, filters=`exposure.routingTarget.status = "Met"`
  - `ROUTING_MISSED` — "Missed (Routing)"
    - aggregate: function=`COUNT`, over=`exposure.exposureId`, filters=`exposure.routingTarget.status = "Missed"`
  - `ROUTING_NOT_ROUTED` — "Not Routed"
    - aggregate: function=`COUNT`, over=`exposure.exposureId`, filters=`exposure.routingTarget.status = "Not Routed"`
  - `ROUTING_ON_TRACK` — "On Track (Routing)"
    - aggregate: function=`COUNT`, over=`exposure.exposureId`, filters=`exposure.routingTarget.status = "On Track"`
  - `ROUTING_OVERDUE` — "Overdue (Routing)"
    - aggregate: function=`COUNT`, over=`exposure.exposureId`, filters=`exposure.routingTarget.status = "Overdue"`
  - `SECURIN_KEV_EXPOSURES` — "Securin KEV"
    - aggregate: function=`COUNT`, over=`exposure.exposureId`, filters=`vulnerabilities.isExploitedInTheWild = "true"`
  - `SUPPRESSED_EXPOSURES` — "Suppressed Exposures"
    - aggregate: function=`COUNT`, over=`exposure.exposureId`, filters=`exposure.lifeCycleState = "Suppressed"`
  - `TRENDING_CVE_EXPOSURES` — "Trending Exposures"
    - aggregate: function=`COUNT`, over=`exposure.exposureId`, filters=`vulnerabilities.threats.lastTrendingDate > today() - 7`
  - `USER_RESOLVED_EXPOSURES` — "User Resolved Exposures"
    - aggregate: function=`COUNT`, over=`exposure.exposureId`, filters=`exposure.lifeCycleState = "User Resolved"`
  - `WEAKNESS_COUNT` — "Unique CWEs"
    - aggregate: function=`CARDINALITY`, over=`weaknesses.id`, filters=`exposure.status = "Open"`
  - `WORKSPACES` — "Workspaces"
    - aggregate: function=`TERMS`, over=`asset.workspaces.name`