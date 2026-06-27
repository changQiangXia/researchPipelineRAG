# DomainRAG Human Calibration Packet

Questions for review: 4

## fresh_hard::flashrag_bm25_live_deepseek::ns_ht_q009

- Priority: normal
- Reasons: none
- Method: flashrag_bm25_live_deepseek
- Question type: single_choice

Question:

During 850 C creep, which factor can control gamma-prime rafting in a directionally solidified nickel-based superalloy?
A. Aluminum mobility
B. Markdown heading depth
C. PDF filename length
D. API retry counter

Gold answers: ['A']
Prediction: A

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The model prediction matches the gold answer and is directly supported by the retrieved context, making it fully correct and faithful.

Retrieved context:

### ns_ht_creep_rafting_al_mobility_001

During 850 C creep of a directionally solidified nickel-based superalloy, aluminum mobility can control gamma-prime rafting. Larger plastic strain flow promotes P-type rafting, while restricted deformation can leave the gamma-prime structure less rafted.

### ns_ht_creep_orientation_850c_001

At 850 C, a directionally solidified nickel-based superalloy can show stronger creep resistance in the longitudinal orientation than in the transverse orientation. The longitudinal condition activates more slip systems and APB shearing, while the transverse condition is dominated by fewer slip bands and SISF-related deformation.

### ns_ht_rejuvenation_heat_treatment_001

Rejuvenation heat treatment can recover creep-degraded directionally solidified superalloys by modifying gamma-prime morphology. In one optimized regime, solution treatment near 1283 C and primary aging near 1095 C restored most standard heat-treatment creep life and increased total creep life.

### ns_ht_pf_ml_creep_features_001

Phase-field-informed machine learning can predict creep strain from simulated microstructure and composition descriptors. Useful descriptors include gamma-prime rafting degree, gamma-prime volume fraction, interparticle spacing, and elemental partitioning coefficients.

### ns_ht_am_abd900_carbide_damage_001

Under high-temperature creep in additively manufactured ABD-900AM, MC carbides can grow near grain boundaries while consuming gamma-prime. This process can create precipitate-free zones and grain-boundary damage, with cavitation morphology depending on stress.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_live_deepseek::ns_ht_q010

- Priority: normal
- Reasons: none
- Method: flashrag_bm25_live_deepseek
- Question type: multiple_choice

Question:

Which statements compare two oxidation-mitigation mechanisms in the pilot corpus?
A. A cerium coating can improve chromia scale adherence in AM IN625
B. LPBF GH3536 cellular microstructure can accelerate protective-film formation
C. Both mechanisms are described as deleting source chunks
D. The LPBF GH3536 mechanism involves rapid diffusion paths
E. The cerium coating mechanism is described as slowing inward oxide growth

Gold answers: ['A', 'B', 'D', 'E']
Prediction: A,B,D,E

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The answer matches the gold answer perfectly and each selected option is supported by the context.

Retrieved context:

### ns_ht_oxidation_lpbf_gh3536_001

For LPBF GH3536 oxidized at 950 C, the cellular microstructure can provide rapid diffusion paths that accelerate protective-film formation during early exposure. After long exposure, the LPBF material can show better oxidation resistance than a wrought counterpart.

### ns_ht_oxidation_ce_coating_001

In additively manufactured IN625 exposed to 900 C air, intergranular oxidation can begin when scale buckling opens grain-boundary voids. A very thin cerium coating can improve chromia scale adherence and slow inward oxide growth.

### ns_ht_oxidation_gb_energy_001

Initial oxidation in Inconel 718 can depend on grain-boundary character. Boundaries with different energy states can change oxygen adsorption, diffusion, and oxide nucleation, so intergranular oxidation does not begin uniformly across all boundaries.

### ns_ht_am_abd900_carbide_damage_001

Under high-temperature creep in additively manufactured ABD-900AM, MC carbides can grow near grain boundaries while consuming gamma-prime. This process can create precipitate-free zones and grain-boundary damage, with cavitation morphology depending on stress.

### ns_ht_creep_rafting_al_mobility_001

During 850 C creep of a directionally solidified nickel-based superalloy, aluminum mobility can control gamma-prime rafting. Larger plastic strain flow promotes P-type rafting, while restricted deformation can leave the gamma-prime structure less rafted.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_live_deepseek::ns_ht_q011

- Priority: normal
- Reasons: none
- Method: flashrag_bm25_live_deepseek
- Question type: fill_blank

Question:

In AM IN625 exposed to 900 C air, scale buckling can open grain-boundary voids and initiate ____ oxidation.

Gold answers: ['intergranular']
Prediction: intergranular

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction matches the gold answer and is directly supported by the context.

Retrieved context:

### ns_ht_oxidation_ce_coating_001

In additively manufactured IN625 exposed to 900 C air, intergranular oxidation can begin when scale buckling opens grain-boundary voids. A very thin cerium coating can improve chromia scale adherence and slow inward oxide growth.

### ns_ht_am_abd900_heat_treatment_001

In additively manufactured ABD-900AM, grain size, heat treatment, and build orientation influence creep behavior. Super-solvus heat treatment can recrystallize and coarsen grains, improving creep resistance compared with a near-solvus condition.

### ns_ht_am_abd900_carbide_damage_001

Under high-temperature creep in additively manufactured ABD-900AM, MC carbides can grow near grain boundaries while consuming gamma-prime. This process can create precipitate-free zones and grain-boundary damage, with cavitation morphology depending on stress.

### ns_ht_oxidation_gb_energy_001

Initial oxidation in Inconel 718 can depend on grain-boundary character. Boundaries with different energy states can change oxygen adsorption, diffusion, and oxide nucleation, so intergranular oxidation does not begin uniformly across all boundaries.

### ns_ht_oxidation_lpbf_gh3536_001

For LPBF GH3536 oxidized at 950 C, the cellular microstructure can provide rapid diffusion paths that accelerate protective-film formation during early exposure. After long exposure, the LPBF material can show better oxidation resistance than a wrought counterpart.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_live_deepseek::ns_ht_q012

- Priority: normal
- Reasons: none
- Method: flashrag_bm25_live_deepseek
- Question type: short_answer

Question:

Why can longitudinal orientation and plastic strain flow favor stronger creep resistance and P-type rafting at 850 C?

Gold answers: ['The longitudinal condition activates more slip systems and APB shearing, and larger plastic strain flow promotes P-type gamma-prime rafting.']
Prediction: Longitudinal orientation activates more slip systems and APB shearing, showing stronger creep resistance. Larger plastic strain flow promotes P-type rafting.

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction accurately captures the required points and is fully supported by the retrieved context.

Retrieved context:

### ns_ht_creep_rafting_al_mobility_001

During 850 C creep of a directionally solidified nickel-based superalloy, aluminum mobility can control gamma-prime rafting. Larger plastic strain flow promotes P-type rafting, while restricted deformation can leave the gamma-prime structure less rafted.

### ns_ht_creep_orientation_850c_001

At 850 C, a directionally solidified nickel-based superalloy can show stronger creep resistance in the longitudinal orientation than in the transverse orientation. The longitudinal condition activates more slip systems and APB shearing, while the transverse condition is dominated by fewer slip bands and SISF-related deformation.

### ns_ht_pf_ml_creep_features_001

Phase-field-informed machine learning can predict creep strain from simulated microstructure and composition descriptors. Useful descriptors include gamma-prime rafting degree, gamma-prime volume fraction, interparticle spacing, and elemental partitioning coefficients.

### ns_ht_rejuvenation_heat_treatment_001

Rejuvenation heat treatment can recover creep-degraded directionally solidified superalloys by modifying gamma-prime morphology. In one optimized regime, solution treatment near 1283 C and primary aging near 1095 C restored most standard heat-treatment creep life and increased total creep life.

### ns_ht_am_abd900_heat_treatment_001

In additively manufactured ABD-900AM, grain size, heat treatment, and build orientation influence creep behavior. Super-solvus heat treatment can recrystallize and coarsen grains, improving creep resistance compared with a near-solvus condition.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:
