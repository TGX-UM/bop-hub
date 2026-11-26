---
id: "BOP:1"
title: "Energy deficit from fasting leading to resolution of metabolic dysfunction-associated steatotic liver disease"
short_title: "Fasting → resolution of MASLD"
description: >-
  An acute energy deficit produced by fasting activates AMP-activated protein kinase and
  inhibits mTORC1 signalling, inducing autophagy and lipophagy, withdrawing the drive on
  hepatic de novo lipogenesis, raising fatty acid beta-oxidation and ketogenesis, lowering
  hepatic inflammation and oxidative stress, and restoring hepatic and systemic insulin
  sensitivity, with resolution of hepatic steatosis as the beneficial outcome.

status: draft
overall_confidence: moderate

# --- nodes ----------------------------------------------------------------
# `role` is the part each event plays in THIS BOP and is never stored on the
# event page: an event is an outcome in one BOP and intermediate in another.
events:
  - {event: "BOPE:0001", role: initiating}   # Energy deficit, hepatocyte
  - {event: "BOPE:0002", role: key}          # Activation, AMPK
  - {event: "BOPE:0003", role: key}          # Inhibition, mTORC1 signalling
  - {event: "BOPE:0004", role: key}          # Decrease, hepatic de novo lipogenesis
  - {event: "BOPE:0005", role: key}          # Increase, autophagy
  - {event: "BOPE:0006", role: key}          # Increase, lipophagy
  - {event: "BOPE:0007", role: key}          # Increase, hepatic fatty acid beta-oxidation
  - {event: "BOPE:0008", role: key}          # Increase, ketogenesis
  - {event: "BOPE:0009", role: key}          # Increase, plasma urate
  - {event: "BOPE:0010", role: key}          # Decrease, hepatic oxidative stress
  - {event: "BOPE:0011", role: key}          # Decrease, hepatic inflammation
  - {event: "BOPE:0012", role: key}          # Restoration, insulin sensitivity
  - {event: "BOPE:0013", role: outcome}      # Resolution, MASLD

# --- edges ----------------------------------------------------------------
# Each entry points at a relationship page, which carries the intrinsic
# evidence, and rates it in the context of this BOP.
relationships:
  - {ker: "BOPR:0001", essentiality: strong,   confidence: high}
  - {ker: "BOPR:0002", essentiality: strong,   confidence: high}
  - {ker: "BOPR:0003", essentiality: strong,   confidence: moderate}
  - {ker: "BOPR:0004", essentiality: moderate, confidence: moderate}
  - {ker: "BOPR:0005", essentiality: moderate, confidence: high}
  - {ker: "BOPR:0006", essentiality: strong,   confidence: high}
  - {ker: "BOPR:0007", essentiality: moderate, confidence: moderate}
  - {ker: "BOPR:0008", essentiality: moderate, confidence: high}
  - {ker: "BOPR:0009", essentiality: weak,     confidence: moderate}
  - {ker: "BOPR:0010", essentiality: moderate, confidence: moderate}
  - {ker: "BOPR:0011", essentiality: weak,     confidence: moderate}
  - {ker: "BOPR:0012", essentiality: weak,     confidence: low,
     comment: "Weakest link in the pathway: the urate-antioxidant route rests on indirect allopurinol evidence."}
  - {ker: "BOPR:0013", essentiality: strong,   confidence: moderate}
  - {ker: "BOPR:0014", essentiality: weak,     confidence: moderate}
  - {ker: "BOPR:0015", essentiality: strong,   confidence: high}
  - {ker: "BOPR:0016", essentiality: moderate, confidence: moderate}
  - {ker: "BOPR:0017", essentiality: strong,   confidence: high}
  - {ker: "BOPR:0018", essentiality: moderate, confidence: moderate}
  - {ker: "BOPR:0019", essentiality: strong,   confidence: high,
     comment: "Non-adjacent: carries the clinical weight of the BOP (meta-analysis, 21 studies, 1226 participants)."}

# --- applicability domain -------------------------------------------------
interventions: ["MESH:D005215"]
taxa:          ["NCBITaxon:9606", "NCBITaxon:10090"]
sex:           ["PATO:0000383", "PATO:0000384"]
life_stage:    ["HsapDv:0000087"]
diseases:      ["MONDO:0013209", "MONDO:0007027"]
phenotypes:    ["HP:0001397"]

modulating_factors:
  - factor: "Baseline insulin resistance and hepatic glycogen status"
    direction: enhances
    comment: "A chronically hyperinsulinaemic, high-carbohydrate state shows a steeper fall in insulin and a more pronounced switch to lipolysis once fasting begins."
  - factor: "Fasting protocol: duration, depth of caloric withdrawal and macronutrient profile"
    direction: modulates
    comment: "Dose is depth of deficit and repetition over time, not duration alone. Time-restricted eating without caloric reduction may not trigger the initiating event at all."
  - factor: "Physical activity during the fast"
    direction: enhances
    comment: "Light aerobic activity accelerates glycogen depletion and advances the timing of AMPK activation and ketone appearance."
  - factor: "Age"
    direction: attenuates
    comment: "Older adults show slower AMPK activation, reduced mitochondrial adaptability and more proteolysis relative to lipid oxidation."
  - factor: "Advanced fibrosis or cirrhosis"
    direction: attenuates
    comment: "Mitochondrial dysfunction in cirrhosis blunts ketogenesis despite lipolysis. Also a contraindication, not only an attenuator: see the safety section."
  - factor: "Medication: sulfonylureas, SGLT2 inhibitors, glucocorticoids, beta-blockers, statins"
    direction: modulates
    comment: "All affect lipolysis, gluconeogenesis or ketogenesis even in the fed state, and can dominate the metabolic switch."
  - factor: "Dietary quality after refeeding"
    direction: modulates
    comment: "Benefits depend on what follows the fast. Reintroducing ultra-processed or high-sugar food can reverse the improvement."

# --- crosswalk to AOP-Wiki ------------------------------------------------
# Verified against AOP-Wiki RDF release 2026.11.21. These nine AOPs all
# terminate in hepatic steatosis, which is what this BOP resolves.
related_aops:
  - {aop: "aop:34",  relation: counteracts, note: "LXR activation leading to hepatic steatosis"}
  - {aop: "aop:57",  relation: counteracts, note: "AhR activation leading to hepatic steatosis"}
  - {aop: "aop:58",  relation: counteracts, note: "NR1I3 (CAR) suppression leading to hepatic steatosis"}
  - {aop: "aop:59",  relation: counteracts, note: "HNF4alpha suppression leading to hepatic steatosis"}
  - {aop: "aop:60",  relation: counteracts, note: "NR1I2 (PXR) activation leading to hepatic steatosis"}
  - {aop: "aop:61",  relation: counteracts, note: "NFE2L2/FXR activation leading to hepatic steatosis"}
  - {aop: "aop:62",  relation: counteracts, note: "AKT2 activation leading to hepatic steatosis"}
  - {aop: "aop:318", relation: counteracts, note: "Glucocorticoid receptor activation leading to hepatic steatosis"}
  - {aop: "aop:650", relation: counteracts, note: "Polystyrene nanoplastic-induced PPAR signaling dysregulation leading to hepatic steatosis"}

references:
  - {doi: "10.1155/jnme/3190642", pmid: "41970466", pmcid: "PMC13063385", citation: "Mesnage R, Buchinger V. Beneficial Outcome Pathways: A New Mechanistic Framework to Map the Health Effects of Fasting in Metabolic Dysfunction-Associated Steatotic Liver Disease. J Nutr Metab. 2026;2026:3190642."}
curators:
  - {name: "Marvin Martens", orcid: "0000-0003-2230-0840", github: marvinm2}
created:  2026-11-26
modified: 2026-11-26
license: "CC0-1.0"
---

## Overall weight of evidence

The spine of this pathway — energy deficit, AMPK activation, mTORC1 inhibition, autophagy and
lipophagy, beta-oxidation and ketogenesis, insulin sensitivity, resolution of steatosis — is
well supported, and the clinical endpoint is carried by a meta-analysis of 21 studies and 1226
participants in which fasting decreased liver fat and steatosis independently of participant age,
health status, weight status or intervention duration.

Confidence is nevertheless rated **moderate** overall, for three reasons.

**Quantitative understanding is low almost everywhere.** Most of the nineteen relationships are
rated low on quantitative understanding. Fasting dose is defined by depth of energy deficit,
macronutrient composition and repetition over time, not duration alone, and the thresholds at
which each step engages in human liver are largely unknown. The one real dose-response signal is
observational: in a study of periodic fasting averaging 8.5 days, the reduction in fatty liver
index tracked both fasting duration and the magnitude of BMI reduction.

**One branch is weakly evidenced.** The urate branch — ketogenesis raising plasma urate, urate
lowering hepatic oxidative stress — rests on the indirect observation that suppressing urate
production with allopurinol worsens oxidative stress. Nothing in the source demonstrates that the
fasting-induced urate rise is what lowers hepatic oxidative stress. It is recorded because the
source argues for it, and rated `empirical_support: low` with `essentiality: weak` so that the
weakness is visible rather than buried.

**The intervention is not unitary.** Fasting is a family of practices, from water-only
abstinence through fasting-mimicking diets to time-restricted eating, that differ in duration,
macronutrient composition and energy load. The TREATY-FLD trial found 8-hour time-restricted
eating gave no liver-fat reduction beyond caloric restriction, which suggests that in that
protocol the benefit was mediated by weight loss rather than by fasting as such. A single
initiating event is a simplification; the canonical form adopted here is substantial acute
caloric withdrawal of about 500 kcal/day or less, or complete abstinence beyond 24 hours.

## A feedback loop the model cannot express

The source describes improved insulin sensitivity as sustaining hepatic fat reduction, "closing a
positive feedback loop that consolidates the beneficial outcome".

That loop is **not** recorded as a relationship. The event-relationship grammar inherited from
AOPs is acyclic, and the content validator rejects a cycle; adding the return edge from the
insulin-sensitivity event back into the lipid-handling events would fail the build. This is a real
expressiveness limit of the inherited model rather than a gap in curation, and it is one of the
things a quantitative BOP would need to represent.

## Safety and non-scope

A BOP maps beneficial outcomes, but fasting is not harmless, and a resource about beneficial
effects has a particular duty to say so.

Fasting can cause hypotension, hypoglycaemia and electrolyte imbalance, and can exacerbate
eating disorders, particularly when unsupervised. It may harm muscle mass in cirrhosis, where
anabolic resistance makes patients prone to catabolic consequences. In a multicentre study of 300
cirrhotic patients fasting during Ramadan, several developed fatigue, variceal bleeding or
encephalopathy, and there were three deaths from hepatorenal syndrome. The consistent reading is
that fasting is not contraindicated in Child class A but that Child class C patients should not
fast. Uncontrolled type 1 diabetes risks unrestrained ketone accumulation and ketoacidosis.

**This page is a mechanistic map, not medical advice, and not a health-claim substantiation.**

## Relationship to AOP-Wiki

Nine AOPs in AOP-Wiki release 2026.11.21 terminate in hepatic steatosis, and all nine are
recorded above as pathways this BOP counteracts. The convergence is the substantive point: one
beneficial pathway can act against a whole family of adverse ones that start from quite different
molecular initiating events.

Two event-level crosswalks are recorded. `BOPE:0007` **is** AOP-Wiki key event 1312, "Increase,
Fatty acid beta-oxidation", reused rather than re-minted, and its adverse mirror is key event 179.
`BOPE:0013` has no identity match, because AOP-Wiki has no event for the resolution of steatosis;
its mirror is key event 459, "Increase, Liver steatosis", which appears in 22 AOPs.

## Curation notes

Content is drawn solely from Mesnage and Buchinger 2026, the first and so far only published BOP.
Two editorial decisions are worth recording.

The source's own key event numbering is internally inconsistent: KE7 is never defined, KE4 is used
both for autophagy and lipophagy and as the target of a fatty acid oxidation relationship, and the
antioxidant events are labelled KE10 and KE11 in ways the surrounding prose does not quite match.
This BOP therefore does **not** reproduce the paper's KE numbers. It assigns its own identifiers
and follows the mechanism as described in the prose of sections 4 and 6.

Compound events in the source have been split into single-concept events, which is standard AOP
practice and a precondition for ontology annotation: autophagy and lipophagy are separate events,
as are fatty acid beta-oxidation and ketogenesis. The Gene Ontology search for the compound forms
returned nothing faithful, which is itself evidence that the split is the right call.
