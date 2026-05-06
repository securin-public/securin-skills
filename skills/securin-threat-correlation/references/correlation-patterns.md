# Correlation Patterns

Reference templates for common threat-correlation questions. Each pattern assumes Step 0 preflight has already resolved the account-id and composite-vs-source model.

## Pattern 1 — "Am I affected by CVE-X?"

```text
1. searchVulnerabilityData
   filters: vulnerabilityId = 'CVE-X'
   → fetch KEV status, severity, exploits

2. searchExposureData
   filters: exposure.mappedAttributes.vulnerabilityIds = 'CVE-X'
            AND exposure.status = 'Open'
   → itemize each exposure (capped, e.g., top 25 by severity)

3. aggregateExposureData
   filters: <same as step 2>
   aggs: [{ name: "by_severity", function: "TERMS", field: "exposure.scores.scoreLevel" }]
   → count + severity breakdown

4. searchAssetData (or searchCompositeAssetData)
   filters: asset.assetId in (<ids from step 2>)
   → asset context

5. createDeepLink per affected asset + top-level filter link
```

## Pattern 2 — "Am I affected by [ransomware family]?"

```text
1. **Web search** for the ransomware family (e.g., "LockBit CVE list", "Clop ransomware CVE")
   → collect CVE IDs from published threat-intel reports (Unit42, Mandiant, CISA advisories)
   → confirm the CVE list with the user before correlating

2. searchExposureData + aggregateExposureData (two calls, same filter)
   filters: exposure.mappedAttributes.vulnerabilityIds in (<cve-list>)
            AND exposure.status = 'Open'
   aggregate aggs: [{ name: "by_severity", function: "TERMS", field: "exposure.scores.scoreLevel" }]

3-5. As Pattern 1 steps 3-5
```

## Pattern 3 — "Am I affected by [threat actor]?"

```text
1. searchThreatActorData
   filters: name like '<actor>'          # bare path — no `threatActor.` prefix
   # Do NOT pass fields: ['threatActor'] — actor records are flat (name,
   # description, associatedGroups, vulnerabilities, software, techniques, …),
   # not nested under a `threatActor` prefix, so that filter returns empty rows.
   # Omit `fields` to get the full record, or list specific top-level keys.
   → gather actor record (associatedGroups, vulnerabilities, software, techniques)
   → ALSO gather TTPs if present

2-5. As Pattern 2 steps 2-5

6. Web search for ATT&CK mapping — Use web search for MITRE ATT&CK data.
```

## Pattern 4 — "Show me exposures to CISA KEV in my prod env"

Run search + aggregate with the same filter:

```text
# 1) Row list
searchExposureData
filters: exposure.status = 'Open'
         AND vulnerabilities.isCisaKEV = true
         AND exposure.workspaces.id in (<prod-ws-id-1>, <prod-ws-id-2>)
         # workspace ids are numeric — do NOT single-quote them

# 2) Bucket counts (same filter)
aggregateExposureData
filters: <same as above>
aggs: [{ name: "by_severity", function: "TERMS", field: "exposure.scores.scoreLevel" }]
```

## Pattern 5 — "What hunts my environment" (outbound)

```text
1. aggregateExposureData
   filters: exposure.status = 'Open' AND <scope>
   aggs: [{ name: "by_cve", function: "TERMS",
            field: "exposure.mappedAttributes.vulnerabilityIds" }]
   → list of CVEs with exposure counts in your env

2. For top N CVEs by exposure count, in parallel:
   - searchVulnerabilityData (CVE record)
   - searchThreatActorData (actors exploiting it)   # do NOT pass fields:['threatActor'] (see Pattern 3)
   - **Web search** (ransomware/malware → CVE list)

3. Aggregate by threat actor / ransomware family:
   Which actors/families map to the most CVEs in your env?
   Rank by # affected assets (join back via exposures → assets).
```

## Pattern 6 — "Am I vulnerable to the latest news-worthy CVE?"

User says "the Fortinet thing from last week" — no CVE ID.

```text
1. Web search to resolve the event to a CVE list.
   Ask user to confirm before proceeding.

2. For each confirmed CVE, run Pattern 1.

3. Consolidated report covering all CVEs from the event.
```

## Pattern 7 — "Net open exposures to exploited vulns, over time"

Time-series correlation for trending:

```text
searchVulnerabilityTimelineData
filters: title like 'CVE-2024-3400'
fields: ["author", "title", "publishedDate", "source.name", "type"]
   # `fields` matters: without a valid timeline prefix in the projection,
   # the call returns totalRecords > 0 with an empty results array. Valid
   # paths come from getApiFields(entityType=['VULNERABILITY_TIMELINE']):
   # author · title · content · publishedDate · language · type · source.name
   # · translatedPost.{title,content,language}
```
`fields` and `filters` are mandatory in the above tool call. 

## Anti-patterns to avoid

- **Starting a correlation without a resolved account-id** — CC-1 preflight first, always.
- **Passing `fields: ["threatActor"]` to `searchThreatActorData`** — returns empty rows silently because actor records are flat, not nested under that prefix. Omit `fields` (or pass top-level keys like `name`, `vulnerabilities`) to get the record. The same trap may apply to `searchThreatData` — verify with the live schema before adding a `fields` array.
- **Hand-constructing URLs** instead of `createDeepLink`.
- **Mixing `asset.*` and `compositeAsset.*`** in one query — pick one per account.
- **Blindly iterating all CVEs for a prolific threat actor** — batch, or prioritize by CISA KEV / isExploitedInTheWild first.