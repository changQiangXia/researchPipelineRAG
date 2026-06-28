# DomainRAG Human Calibration Packet

Questions for review: 40

## fresh_hard::no_rag::ns_ht_q009

- Priority: high
- Reasons: unsupported_claims, context_support_below_5, faithfulness_below_5, hallucination_risk_above_0
- Method: no_rag
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

correctness=5.0, context_support=0.0, faithfulness=0.0, unsupported_claims=Aluminum mobility controls gamma-prime rafting in a directionally solidified nickel-based superalloy, reason=Prediction matches gold answer but no context retrieved, so context_support is 0 and the factual claim is unsupported.

Retrieved context:

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::no_rag::ns_ht_q010

- Priority: high
- Reasons: unsupported_claims, correctness_below_5, context_support_below_5, faithfulness_below_5, hallucination_risk_above_0
- Method: no_rag
- Question type: multiple_choice

Question:

Which statements compare two oxidation-mitigation mechanisms in the pilot corpus?
A. A cerium coating can improve chromia scale adherence in AM IN625
B. LPBF GH3536 cellular microstructure can accelerate protective-film formation
C. Both mechanisms are described as deleting source chunks
D. The LPBF GH3536 mechanism involves rapid diffusion paths
E. The cerium coating mechanism is described as slowing inward oxide growth

Gold answers: ['A', 'B', 'D', 'E']
Prediction: C

Judge:

correctness=0.0, context_support=0.0, faithfulness=0.0, unsupported_claims=Both mechanisms are described as deleting source chunks., reason=The model selected option C, which is not among the gold answers A, B, D, E, and the claim about deleting source chunks is unsupported.

Retrieved context:

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::no_rag::ns_ht_q011

- Priority: high
- Reasons: unsupported_claims, correctness_below_5, context_support_below_5, faithfulness_below_5, hallucination_risk_above_0
- Method: no_rag
- Question type: fill_blank

Question:

In AM IN625 exposed to 900 C air, scale buckling can open grain-boundary voids and initiate ____ oxidation.

Gold answers: ['intergranular']
Prediction: internal

Judge:

correctness=0.0, context_support=0.0, faithfulness=0.0, unsupported_claims=The prediction 'internal' is not supported by any retrieved context., reason=The prediction 'internal' is incorrect because the gold answer is 'intergranular', and without retrieved context, it is unsupported and unfaithful.

Retrieved context:

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::no_rag::ns_ht_q012

- Priority: high
- Reasons: unsupported_claims, correctness_below_5, context_support_below_5, faithfulness_below_5, hallucination_risk_above_0
- Method: no_rag
- Question type: short_answer

Question:

Why can longitudinal orientation and plastic strain flow favor stronger creep resistance and P-type rafting at 850 C?

Gold answers: ['The longitudinal condition activates more slip systems and APB shearing, and larger plastic strain flow promotes P-type gamma-prime rafting.']
Prediction: Longitudinal orientation aligns grain boundaries parallel to the stress axis, minimizing transverse boundaries that weaken creep resistance. Plastic strain introduces dislocations that accelerate diffusion and promote directional coarsening of gamma-prime precipitates. The resulting dislocation arrangements can induce local compressive stresses in the matrix, favoring P-type rafting where precipitates raft parallel to the applied load.

Judge:

correctness=1.0, context_support=0.0, faithfulness=1.0, unsupported_claims=Longitudinal orientation minimizes transverse grain boundaries to improve creep resistance, not via slip systems or APB shearing.; Plastic strain introduces dislocations that accelerate diffusion.; Dislocation arrangements induce local compressive stresses that cause P-type rafting., reason=The prediction misses the key mechanisms (more slip systems and APB shearing) and focuses on grain boundary effects not in the gold answer, though it loosely connects plastic strain to rafting.

Retrieved context:

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::no_rag::ns_ht_q021

- Priority: high
- Reasons: context_support_below_5
- Method: no_rag
- Question type: single_choice

Question:

At 1200 C and 80 MPa, what kind of result supports a transfer-learning-designed single-crystal superalloy candidate?
A. Rupture life above 170 h in creep validation
B. A shorter prompt context
C. A missing qrels file
D. A room-temperature hardness label only

Gold answers: ['A']
Prediction: A

Judge:

correctness=5.0, context_support=0.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction correctly selects option A, which is the gold answer, but no context was provided to support it.

Retrieved context:

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::no_rag::ns_ht_q022

- Priority: high
- Reasons: unsupported_claims, correctness_below_5, context_support_below_5, faithfulness_below_5, hallucination_risk_above_0
- Method: no_rag
- Question type: fill_blank

Question:

A drilled single-crystal superalloy can alter scale adhesion and corrosion-product evolution around the ____ region.

Gold answers: ['machined']
Prediction: recrystallized

Judge:

correctness=0.0, context_support=0.0, faithfulness=0.0, unsupported_claims=The claim that the region is 'recrystallized' is unsupported., reason=The prediction 'recrystallized' does not match the gold answer 'machined' and is unsupported by any context.

Retrieved context:

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::no_rag::ns_ht_q023

- Priority: high
- Reasons: unsupported_claims, correctness_below_5, context_support_below_5, faithfulness_below_5, hallucination_risk_above_0
- Method: no_rag
- Question type: multiple_choice

Question:

Which statements compare hot-corrosion mitigation or modification mechanisms in the expanded corpus?
A. Pre-oxidation in SLM Inconel 625 can form a protective barrier
B. Molten-salt hot corrosion can involve scale cracking and spallation
C. Drilling can change local diffusion paths near a hole surface
D. All mechanisms are described as unrelated to oxide layers
E. TiC additions may affect oxide-scale continuity

Gold answers: ['A', 'B', 'C', 'E']
Prediction: D

Judge:

correctness=0.0, context_support=0.0, faithfulness=0.0, unsupported_claims=All mechanisms are described as unrelated to oxide layers, reason=Prediction selects D, which is incorrect and unsupported by any context, as the correct answers include mechanisms related to oxide layers.

Retrieved context:

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::no_rag::ns_ht_q024

- Priority: high
- Reasons: unsupported_claims, correctness_below_5, context_support_below_5, faithfulness_below_5, hallucination_risk_above_0
- Method: no_rag
- Question type: short_answer

Question:

How do entropy-based fatigue prediction and PM-HIP fatigue review knowledge differ in the expanded corpus?

Gold answers: ['The entropy method treats entropy generation from cyclic plasticity as a damage-related predictor, while PM-HIP review knowledge emphasizes processing factors such as powder quality, residual defects, grain structure, and heat treatment.']
Prediction: Entropy-based fatigue prediction uses thermodynamic entropy generation to model fatigue damage accumulation, while PM-HIP fatigue review focuses on empirical observations of fatigue properties in powder metallurgy-hot isostatic pressing materials. The former is a theoretical, physics-based approach, and the latter is an applied review of processing-structure-property relationships.

Judge:

correctness=4.0, context_support=0.0, faithfulness=0.0, unsupported_claims=Entropy-based fatigue prediction uses thermodynamic entropy generation to model fatigue damage accumulation.; PM-HIP fatigue review focuses on empirical observations of fatigue properties in powder metallurgy-hot isostatic pressing materials., reason=The prediction generally captures the contrast but lacks specific details from the gold answer; without retrieved context, the factual claims remain unsupported.

Retrieved context:

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::oracle_context::ns_ht_q009

- Priority: normal
- Reasons: none
- Method: oracle_context
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

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction correctly selects aluminum mobility which is supported by the context.

Retrieved context:

### ns_ht_creep_rafting_al_mobility_001

During 850 C creep of a directionally solidified nickel-based superalloy, aluminum mobility can control gamma-prime rafting. Larger plastic strain flow promotes P-type rafting, while restricted deformation can leave the gamma-prime structure less rafted.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::oracle_context::ns_ht_q010

- Priority: normal
- Reasons: none
- Method: oracle_context
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

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=All selected statements are correct and fully supported by the provided contexts.

Retrieved context:

### ns_ht_oxidation_ce_coating_001

In additively manufactured IN625 exposed to 900 C air, intergranular oxidation can begin when scale buckling opens grain-boundary voids. A very thin cerium coating can improve chromia scale adherence and slow inward oxide growth.

### ns_ht_oxidation_lpbf_gh3536_001

For LPBF GH3536 oxidized at 950 C, the cellular microstructure can provide rapid diffusion paths that accelerate protective-film formation during early exposure. After long exposure, the LPBF material can show better oxidation resistance than a wrought counterpart.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::oracle_context::ns_ht_q011

- Priority: normal
- Reasons: none
- Method: oracle_context
- Question type: fill_blank

Question:

In AM IN625 exposed to 900 C air, scale buckling can open grain-boundary voids and initiate ____ oxidation.

Gold answers: ['intergranular']
Prediction: intergranular

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction exactly matches the gold answer and is directly supported by the retrieved context.

Retrieved context:

### ns_ht_oxidation_ce_coating_001

In additively manufactured IN625 exposed to 900 C air, intergranular oxidation can begin when scale buckling opens grain-boundary voids. A very thin cerium coating can improve chromia scale adherence and slow inward oxide growth.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::oracle_context::ns_ht_q012

- Priority: normal
- Reasons: none
- Method: oracle_context
- Question type: short_answer

Question:

Why can longitudinal orientation and plastic strain flow favor stronger creep resistance and P-type rafting at 850 C?

Gold answers: ['The longitudinal condition activates more slip systems and APB shearing, and larger plastic strain flow promotes P-type gamma-prime rafting.']
Prediction: Longitudinal orientation favors stronger creep resistance because it activates more slip systems and APB shearing. Larger plastic strain flow promotes P-type rafting, as it influences aluminum mobility during gamma-prime rafting.

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction correctly captures the required points about slip systems, APB shearing, and P-type rafting, and all claims are context-supported.

Retrieved context:

### ns_ht_creep_orientation_850c_001

At 850 C, a directionally solidified nickel-based superalloy can show stronger creep resistance in the longitudinal orientation than in the transverse orientation. The longitudinal condition activates more slip systems and APB shearing, while the transverse condition is dominated by fewer slip bands and SISF-related deformation.

### ns_ht_creep_rafting_al_mobility_001

During 850 C creep of a directionally solidified nickel-based superalloy, aluminum mobility can control gamma-prime rafting. Larger plastic strain flow promotes P-type rafting, while restricted deformation can leave the gamma-prime structure less rafted.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::oracle_context::ns_ht_q021

- Priority: normal
- Reasons: none
- Method: oracle_context
- Question type: single_choice

Question:

At 1200 C and 80 MPa, what kind of result supports a transfer-learning-designed single-crystal superalloy candidate?
A. Rupture life above 170 h in creep validation
B. A shorter prompt context
C. A missing qrels file
D. A room-temperature hardness label only

Gold answers: ['A']
Prediction: A

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction exactly matches the gold answer and the context supports rupture life >170 h as validation.

Retrieved context:

### ns_ht_transfer_learning_creep_design_001

Transfer learning can guide single-crystal superalloy composition design for ultrahigh-temperature creep resistance. A designed alloy can be validated under 1200 C and 80 MPa creep, where rupture life above 170 h indicates that data-driven screening can still require experimental confirmation.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::oracle_context::ns_ht_q022

- Priority: normal
- Reasons: none
- Method: oracle_context
- Question type: fill_blank

Question:

A drilled single-crystal superalloy can alter scale adhesion and corrosion-product evolution around the ____ region.

Gold answers: ['machined']
Prediction: machined

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction exactly matches the gold answer and is directly supported by the context.

Retrieved context:

### ns_ht_drilled_sx_hot_corrosion_001

A drilled nickel-based single-crystal superalloy can show abnormal hot-corrosion behavior because the hole surface changes diffusion paths and oxide-layer development. Local drilling can therefore alter scale adhesion and corrosion-product evolution around the machined region.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::oracle_context::ns_ht_q023

- Priority: normal
- Reasons: none
- Method: oracle_context
- Question type: multiple_choice

Question:

Which statements compare hot-corrosion mitigation or modification mechanisms in the expanded corpus?
A. Pre-oxidation in SLM Inconel 625 can form a protective barrier
B. Molten-salt hot corrosion can involve scale cracking and spallation
C. Drilling can change local diffusion paths near a hole surface
D. All mechanisms are described as unrelated to oxide layers
E. TiC additions may affect oxide-scale continuity

Gold answers: ['A', 'B', 'C', 'E']
Prediction: A,B,C,E

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction correctly selects options A, B, C, and E, which match the gold answer and are all supported by the context.

Retrieved context:

### ns_ht_slm_in625_preoxidation_001

For SLM Inconel 625, heat treatment combined with pre-oxidation can form a more protective oxide barrier before hot-corrosion exposure. The preformed barrier can improve corrosion resistance by slowing aggressive species from penetrating the additively manufactured microstructure.

### ns_ht_hot_corrosion_alloying_001

In molten-salt hot corrosion of nickel-based superalloys, alloying elements can change oxide-scale stability, internal sulfidation, and diffusion of protective elements. Damage can combine surface oxidation, internal sulfidation, scale cracking, and spallation rather than a single degradation mode.

### ns_ht_drilled_sx_hot_corrosion_001

A drilled nickel-based single-crystal superalloy can show abnormal hot-corrosion behavior because the hole surface changes diffusion paths and oxide-layer development. Local drilling can therefore alter scale adhesion and corrosion-product evolution around the machined region.

### ns_ht_tic_in625_oxidation_001

TiC-containing Inconel 625 can change microstructural features that affect high-temperature oxidation behavior. Ceramic-particle additions may influence oxide-scale continuity, local element distribution, and oxidation resistance rather than acting only as inert reinforcement.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::oracle_context::ns_ht_q024

- Priority: high
- Reasons: correctness_below_5
- Method: oracle_context
- Question type: short_answer

Question:

How do entropy-based fatigue prediction and PM-HIP fatigue review knowledge differ in the expanded corpus?

Gold answers: ['The entropy method treats entropy generation from cyclic plasticity as a damage-related predictor, while PM-HIP review knowledge emphasizes processing factors such as powder quality, residual defects, grain structure, and heat treatment.']
Prediction: Entropy-based fatigue prediction uses thermodynamic entropy as a damage quantity for life prediction in GH4169 low-cycle fatigue. PM-HIP fatigue review assesses how powder quality, residual defects, grain structure, and heat treatment affect fatigue behavior, aiming to distinguish processing-driven limits from intrinsic strengthening.

Judge:

correctness=4.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction captures the core distinction but omits the explicit link to cyclic plasticity modeling; it is fully supported by the context.

Retrieved context:

### ns_ht_gh4169_entropy_fatigue_001

For GH4169 low-cycle fatigue at elevated temperature, a thermodynamic entropy method can connect cyclic plasticity modeling with fatigue-life prediction. Entropy generation in the gauge section can serve as a damage-related quantity rather than using stress amplitude alone.

### ns_ht_pm_hip_fatigue_review_001

Powder metallurgy hot-isostatic-pressed superalloys can show fatigue behavior controlled by powder quality, residual defects, grain structure, and heat treatment. Reviewing these factors helps separate processing-driven fatigue limits from intrinsic alloy strengthening effects.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::lexical_rag::ns_ht_q009

- Priority: normal
- Reasons: none
- Method: lexical_rag
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

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction matches the gold answer and is directly supported by the context stating that aluminum mobility controls gamma-prime rafting.

Retrieved context:

### ns_ht_creep_rafting_al_mobility_001

During 850 C creep of a directionally solidified nickel-based superalloy, aluminum mobility can control gamma-prime rafting. Larger plastic strain flow promotes P-type rafting, while restricted deformation can leave the gamma-prime structure less rafted.

### ns_ht_rejuvenation_heat_treatment_001

Rejuvenation heat treatment can recover creep-degraded directionally solidified superalloys by modifying gamma-prime morphology. In one optimized regime, solution treatment near 1283 C and primary aging near 1095 C restored most standard heat-treatment creep life and increased total creep life.

### ns_ht_creep_orientation_850c_001

At 850 C, a directionally solidified nickel-based superalloy can show stronger creep resistance in the longitudinal orientation than in the transverse orientation. The longitudinal condition activates more slip systems and APB shearing, while the transverse condition is dominated by fewer slip bands and SISF-related deformation.

### ns_ht_pf_ml_creep_features_001

Phase-field-informed machine learning can predict creep strain from simulated microstructure and composition descriptors. Useful descriptors include gamma-prime rafting degree, gamma-prime volume fraction, interparticle spacing, and elemental partitioning coefficients.

### ns_ht_transfer_learning_creep_design_001

Transfer learning can guide single-crystal superalloy composition design for ultrahigh-temperature creep resistance. A designed alloy can be validated under 1200 C and 80 MPa creep, where rupture life above 170 h indicates that data-driven screening can still require experimental confirmation.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::lexical_rag::ns_ht_q010

- Priority: normal
- Reasons: none
- Method: lexical_rag
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

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The model accurately selected all and only the statements that describe the two oxidation-mitigation mechanisms with full support from the retrieved context.

Retrieved context:

### ns_ht_oxidation_lpbf_gh3536_001

For LPBF GH3536 oxidized at 950 C, the cellular microstructure can provide rapid diffusion paths that accelerate protective-film formation during early exposure. After long exposure, the LPBF material can show better oxidation resistance than a wrought counterpart.

### ns_ht_oxidation_ce_coating_001

In additively manufactured IN625 exposed to 900 C air, intergranular oxidation can begin when scale buckling opens grain-boundary voids. A very thin cerium coating can improve chromia scale adherence and slow inward oxide growth.

### ns_ht_slm_in625_preoxidation_001

For SLM Inconel 625, heat treatment combined with pre-oxidation can form a more protective oxide barrier before hot-corrosion exposure. The preformed barrier can improve corrosion resistance by slowing aggressive species from penetrating the additively manufactured microstructure.

### ns_ht_creep_orientation_850c_001

At 850 C, a directionally solidified nickel-based superalloy can show stronger creep resistance in the longitudinal orientation than in the transverse orientation. The longitudinal condition activates more slip systems and APB shearing, while the transverse condition is dominated by fewer slip bands and SISF-related deformation.

### ns_ht_drilled_sx_hot_corrosion_001

A drilled nickel-based single-crystal superalloy can show abnormal hot-corrosion behavior because the hole surface changes diffusion paths and oxide-layer development. Local drilling can therefore alter scale adhesion and corrosion-product evolution around the machined region.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::lexical_rag::ns_ht_q011

- Priority: normal
- Reasons: none
- Method: lexical_rag
- Question type: fill_blank

Question:

In AM IN625 exposed to 900 C air, scale buckling can open grain-boundary voids and initiate ____ oxidation.

Gold answers: ['intergranular']
Prediction: intergranular

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction exactly matches the gold answer and is directly supported by the retrieved context.

Retrieved context:

### ns_ht_oxidation_ce_coating_001

In additively manufactured IN625 exposed to 900 C air, intergranular oxidation can begin when scale buckling opens grain-boundary voids. A very thin cerium coating can improve chromia scale adherence and slow inward oxide growth.

### ns_ht_oxidation_gb_energy_001

Initial oxidation in Inconel 718 can depend on grain-boundary character. Boundaries with different energy states can change oxygen adsorption, diffusion, and oxide nucleation, so intergranular oxidation does not begin uniformly across all boundaries.

### ns_ht_hot_corrosion_alloying_001

In molten-salt hot corrosion of nickel-based superalloys, alloying elements can change oxide-scale stability, internal sulfidation, and diffusion of protective elements. Damage can combine surface oxidation, internal sulfidation, scale cracking, and spallation rather than a single degradation mode.

### ns_ht_am_abd900_carbide_damage_001

Under high-temperature creep in additively manufactured ABD-900AM, MC carbides can grow near grain boundaries while consuming gamma-prime. This process can create precipitate-free zones and grain-boundary damage, with cavitation morphology depending on stress.

### ns_ht_tic_in625_oxidation_001

TiC-containing Inconel 625 can change microstructural features that affect high-temperature oxidation behavior. Ceramic-particle additions may influence oxide-scale continuity, local element distribution, and oxidation resistance rather than acting only as inert reinforcement.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::lexical_rag::ns_ht_q012

- Priority: normal
- Reasons: none
- Method: lexical_rag
- Question type: short_answer

Question:

Why can longitudinal orientation and plastic strain flow favor stronger creep resistance and P-type rafting at 850 C?

Gold answers: ['The longitudinal condition activates more slip systems and APB shearing, and larger plastic strain flow promotes P-type gamma-prime rafting.']
Prediction: Longitudinal orientation activates more slip systems and APB shearing, leading to stronger creep resistance. Larger plastic strain flow promotes P-type rafting, as aluminum mobility controls gamma-prime rafting at 850 °C.

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=Prediction includes all required points from gold answer and adds context-supported detail.

Retrieved context:

### ns_ht_creep_rafting_al_mobility_001

During 850 C creep of a directionally solidified nickel-based superalloy, aluminum mobility can control gamma-prime rafting. Larger plastic strain flow promotes P-type rafting, while restricted deformation can leave the gamma-prime structure less rafted.

### ns_ht_creep_orientation_850c_001

At 850 C, a directionally solidified nickel-based superalloy can show stronger creep resistance in the longitudinal orientation than in the transverse orientation. The longitudinal condition activates more slip systems and APB shearing, while the transverse condition is dominated by fewer slip bands and SISF-related deformation.

### ns_ht_am_abd900_heat_treatment_001

In additively manufactured ABD-900AM, grain size, heat treatment, and build orientation influence creep behavior. Super-solvus heat treatment can recrystallize and coarsen grains, improving creep resistance compared with a near-solvus condition.

### ns_ht_pf_ml_creep_features_001

Phase-field-informed machine learning can predict creep strain from simulated microstructure and composition descriptors. Useful descriptors include gamma-prime rafting degree, gamma-prime volume fraction, interparticle spacing, and elemental partitioning coefficients.

### ns_ht_rejuvenation_heat_treatment_001

Rejuvenation heat treatment can recover creep-degraded directionally solidified superalloys by modifying gamma-prime morphology. In one optimized regime, solution treatment near 1283 C and primary aging near 1095 C restored most standard heat-treatment creep life and increased total creep life.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::lexical_rag::ns_ht_q021

- Priority: normal
- Reasons: none
- Method: lexical_rag
- Question type: single_choice

Question:

At 1200 C and 80 MPa, what kind of result supports a transfer-learning-designed single-crystal superalloy candidate?
A. Rupture life above 170 h in creep validation
B. A shorter prompt context
C. A missing qrels file
D. A room-temperature hardness label only

Gold answers: ['A']
Prediction: A

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction correctly selects option A, which is directly supported by the retrieved context stating that rupture life above 170 h under 1200 °C and 80 MPa validates the designed alloy.

Retrieved context:

### ns_ht_transfer_learning_creep_design_001

Transfer learning can guide single-crystal superalloy composition design for ultrahigh-temperature creep resistance. A designed alloy can be validated under 1200 C and 80 MPa creep, where rupture life above 170 h indicates that data-driven screening can still require experimental confirmation.

### ns_ht_gh4169_entropy_fatigue_001

For GH4169 low-cycle fatigue at elevated temperature, a thermodynamic entropy method can connect cyclic plasticity modeling with fatigue-life prediction. Entropy generation in the gauge section can serve as a damage-related quantity rather than using stress amplitude alone.

### ns_ht_rejuvenation_heat_treatment_001

Rejuvenation heat treatment can recover creep-degraded directionally solidified superalloys by modifying gamma-prime morphology. In one optimized regime, solution treatment near 1283 C and primary aging near 1095 C restored most standard heat-treatment creep life and increased total creep life.

### ns_ht_creep_orientation_850c_001

At 850 C, a directionally solidified nickel-based superalloy can show stronger creep resistance in the longitudinal orientation than in the transverse orientation. The longitudinal condition activates more slip systems and APB shearing, while the transverse condition is dominated by fewer slip bands and SISF-related deformation.

### ns_ht_hot_corrosion_alloying_001

In molten-salt hot corrosion of nickel-based superalloys, alloying elements can change oxide-scale stability, internal sulfidation, and diffusion of protective elements. Damage can combine surface oxidation, internal sulfidation, scale cracking, and spallation rather than a single degradation mode.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::lexical_rag::ns_ht_q022

- Priority: normal
- Reasons: none
- Method: lexical_rag
- Question type: fill_blank

Question:

A drilled single-crystal superalloy can alter scale adhesion and corrosion-product evolution around the ____ region.

Gold answers: ['machined']
Prediction: machined

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=Prediction matches the gold answer and is directly supported by the context.

Retrieved context:

### ns_ht_drilled_sx_hot_corrosion_001

A drilled nickel-based single-crystal superalloy can show abnormal hot-corrosion behavior because the hole surface changes diffusion paths and oxide-layer development. Local drilling can therefore alter scale adhesion and corrosion-product evolution around the machined region.

### ns_ht_hot_corrosion_alloying_001

In molten-salt hot corrosion of nickel-based superalloys, alloying elements can change oxide-scale stability, internal sulfidation, and diffusion of protective elements. Damage can combine surface oxidation, internal sulfidation, scale cracking, and spallation rather than a single degradation mode.

### ns_ht_slm_in625_preoxidation_001

For SLM Inconel 625, heat treatment combined with pre-oxidation can form a more protective oxide barrier before hot-corrosion exposure. The preformed barrier can improve corrosion resistance by slowing aggressive species from penetrating the additively manufactured microstructure.

### ns_ht_creep_orientation_850c_001

At 850 C, a directionally solidified nickel-based superalloy can show stronger creep resistance in the longitudinal orientation than in the transverse orientation. The longitudinal condition activates more slip systems and APB shearing, while the transverse condition is dominated by fewer slip bands and SISF-related deformation.

### ns_ht_transfer_learning_creep_design_001

Transfer learning can guide single-crystal superalloy composition design for ultrahigh-temperature creep resistance. A designed alloy can be validated under 1200 C and 80 MPa creep, where rupture life above 170 h indicates that data-driven screening can still require experimental confirmation.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::lexical_rag::ns_ht_q023

- Priority: normal
- Reasons: none
- Method: lexical_rag
- Question type: multiple_choice

Question:

Which statements compare hot-corrosion mitigation or modification mechanisms in the expanded corpus?
A. Pre-oxidation in SLM Inconel 625 can form a protective barrier
B. Molten-salt hot corrosion can involve scale cracking and spallation
C. Drilling can change local diffusion paths near a hole surface
D. All mechanisms are described as unrelated to oxide layers
E. TiC additions may affect oxide-scale continuity

Gold answers: ['A', 'B', 'C', 'E']
Prediction: A,B,C,E

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction matches the gold answer exactly and each selected statement is directly supported by the provided context.

Retrieved context:

### ns_ht_hot_corrosion_alloying_001

In molten-salt hot corrosion of nickel-based superalloys, alloying elements can change oxide-scale stability, internal sulfidation, and diffusion of protective elements. Damage can combine surface oxidation, internal sulfidation, scale cracking, and spallation rather than a single degradation mode.

### ns_ht_slm_in625_preoxidation_001

For SLM Inconel 625, heat treatment combined with pre-oxidation can form a more protective oxide barrier before hot-corrosion exposure. The preformed barrier can improve corrosion resistance by slowing aggressive species from penetrating the additively manufactured microstructure.

### ns_ht_drilled_sx_hot_corrosion_001

A drilled nickel-based single-crystal superalloy can show abnormal hot-corrosion behavior because the hole surface changes diffusion paths and oxide-layer development. Local drilling can therefore alter scale adhesion and corrosion-product evolution around the machined region.

### ns_ht_tic_in625_oxidation_001

TiC-containing Inconel 625 can change microstructural features that affect high-temperature oxidation behavior. Ceramic-particle additions may influence oxide-scale continuity, local element distribution, and oxidation resistance rather than acting only as inert reinforcement.

### ns_ht_oxidation_ce_coating_001

In additively manufactured IN625 exposed to 900 C air, intergranular oxidation can begin when scale buckling opens grain-boundary voids. A very thin cerium coating can improve chromia scale adherence and slow inward oxide growth.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::lexical_rag::ns_ht_q024

- Priority: normal
- Reasons: none
- Method: lexical_rag
- Question type: short_answer

Question:

How do entropy-based fatigue prediction and PM-HIP fatigue review knowledge differ in the expanded corpus?

Gold answers: ['The entropy method treats entropy generation from cyclic plasticity as a damage-related predictor, while PM-HIP review knowledge emphasizes processing factors such as powder quality, residual defects, grain structure, and heat treatment.']
Prediction: Entropy-based fatigue prediction uses thermodynamic entropy generation as a damage quantity to connect cyclic plasticity with fatigue-life prediction. PM-HIP fatigue review examines how powder quality, residual defects, grain structure, and heat treatment influence fatigue behavior to separate processing-driven limits from intrinsic alloy strengthening.

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction accurately captures and contrasts both approaches with full context support, no unfaithful claims, and direct relevance.

Retrieved context:

### ns_ht_gh4169_entropy_fatigue_001

For GH4169 low-cycle fatigue at elevated temperature, a thermodynamic entropy method can connect cyclic plasticity modeling with fatigue-life prediction. Entropy generation in the gauge section can serve as a damage-related quantity rather than using stress amplitude alone.

### ns_ht_pm_hip_fatigue_review_001

Powder metallurgy hot-isostatic-pressed superalloys can show fatigue behavior controlled by powder quality, residual defects, grain structure, and heat treatment. Reviewing these factors helps separate processing-driven fatigue limits from intrinsic alloy strengthening effects.

### ns_ht_creep_orientation_850c_001

At 850 C, a directionally solidified nickel-based superalloy can show stronger creep resistance in the longitudinal orientation than in the transverse orientation. The longitudinal condition activates more slip systems and APB shearing, while the transverse condition is dominated by fewer slip bands and SISF-related deformation.

### ns_ht_drilled_sx_hot_corrosion_001

A drilled nickel-based single-crystal superalloy can show abnormal hot-corrosion behavior because the hole surface changes diffusion paths and oxide-layer development. Local drilling can therefore alter scale adhesion and corrosion-product evolution around the machined region.

### ns_ht_hot_corrosion_alloying_001

In molten-salt hot corrosion of nickel-based superalloys, alloying elements can change oxide-scale stability, internal sulfidation, and diffusion of protective elements. Damage can combine surface oxidation, internal sulfidation, scale cracking, and spallation rather than a single degradation mode.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_oracle_reader::ns_ht_q009

- Priority: normal
- Reasons: none
- Method: flashrag_bm25_oracle_reader
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

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The model correctly selects A, which is directly supported by the retrieved context.

Retrieved context:

### ns_ht_creep_rafting_al_mobility_001

During 850 C creep of a directionally solidified nickel-based superalloy, aluminum mobility can control gamma-prime rafting. Larger plastic strain flow promotes P-type rafting, while restricted deformation can leave the gamma-prime structure less rafted.

### ns_ht_pm_hip_fatigue_review_001

Powder metallurgy hot-isostatic-pressed superalloys can show fatigue behavior controlled by powder quality, residual defects, grain structure, and heat treatment. Reviewing these factors helps separate processing-driven fatigue limits from intrinsic alloy strengthening effects.

### ns_ht_pf_ml_creep_features_001

Phase-field-informed machine learning can predict creep strain from simulated microstructure and composition descriptors. Useful descriptors include gamma-prime rafting degree, gamma-prime volume fraction, interparticle spacing, and elemental partitioning coefficients.

### ns_ht_rejuvenation_heat_treatment_001

Rejuvenation heat treatment can recover creep-degraded directionally solidified superalloys by modifying gamma-prime morphology. In one optimized regime, solution treatment near 1283 C and primary aging near 1095 C restored most standard heat-treatment creep life and increased total creep life.

### ns_ht_creep_orientation_850c_001

At 850 C, a directionally solidified nickel-based superalloy can show stronger creep resistance in the longitudinal orientation than in the transverse orientation. The longitudinal condition activates more slip systems and APB shearing, while the transverse condition is dominated by fewer slip bands and SISF-related deformation.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_oracle_reader::ns_ht_q010

- Priority: normal
- Reasons: none
- Method: flashrag_bm25_oracle_reader
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

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The model prediction exactly matches the gold answer and is fully supported by the context.

Retrieved context:

### ns_ht_oxidation_lpbf_gh3536_001

For LPBF GH3536 oxidized at 950 C, the cellular microstructure can provide rapid diffusion paths that accelerate protective-film formation during early exposure. After long exposure, the LPBF material can show better oxidation resistance than a wrought counterpart.

### ns_ht_oxidation_ce_coating_001

In additively manufactured IN625 exposed to 900 C air, intergranular oxidation can begin when scale buckling opens grain-boundary voids. A very thin cerium coating can improve chromia scale adherence and slow inward oxide growth.

### ns_ht_hot_corrosion_alloying_001

In molten-salt hot corrosion of nickel-based superalloys, alloying elements can change oxide-scale stability, internal sulfidation, and diffusion of protective elements. Damage can combine surface oxidation, internal sulfidation, scale cracking, and spallation rather than a single degradation mode.

### ns_ht_tic_in625_oxidation_001

TiC-containing Inconel 625 can change microstructural features that affect high-temperature oxidation behavior. Ceramic-particle additions may influence oxide-scale continuity, local element distribution, and oxidation resistance rather than acting only as inert reinforcement.

### ns_ht_drilled_sx_hot_corrosion_001

A drilled nickel-based single-crystal superalloy can show abnormal hot-corrosion behavior because the hole surface changes diffusion paths and oxide-layer development. Local drilling can therefore alter scale adhesion and corrosion-product evolution around the machined region.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_oracle_reader::ns_ht_q011

- Priority: normal
- Reasons: none
- Method: flashrag_bm25_oracle_reader
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

### ns_ht_hot_corrosion_alloying_001

In molten-salt hot corrosion of nickel-based superalloys, alloying elements can change oxide-scale stability, internal sulfidation, and diffusion of protective elements. Damage can combine surface oxidation, internal sulfidation, scale cracking, and spallation rather than a single degradation mode.

### ns_ht_am_abd900_heat_treatment_001

In additively manufactured ABD-900AM, grain size, heat treatment, and build orientation influence creep behavior. Super-solvus heat treatment can recrystallize and coarsen grains, improving creep resistance compared with a near-solvus condition.

### ns_ht_am_abd900_carbide_damage_001

Under high-temperature creep in additively manufactured ABD-900AM, MC carbides can grow near grain boundaries while consuming gamma-prime. This process can create precipitate-free zones and grain-boundary damage, with cavitation morphology depending on stress.

### ns_ht_tic_in625_oxidation_001

TiC-containing Inconel 625 can change microstructural features that affect high-temperature oxidation behavior. Ceramic-particle additions may influence oxide-scale continuity, local element distribution, and oxidation resistance rather than acting only as inert reinforcement.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_oracle_reader::ns_ht_q012

- Priority: normal
- Reasons: none
- Method: flashrag_bm25_oracle_reader
- Question type: short_answer

Question:

Why can longitudinal orientation and plastic strain flow favor stronger creep resistance and P-type rafting at 850 C?

Gold answers: ['The longitudinal condition activates more slip systems and APB shearing, and larger plastic strain flow promotes P-type gamma-prime rafting.']
Prediction: The longitudinal condition activates more slip systems and APB shearing, and larger plastic strain flow promotes P-type gamma-prime rafting.

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction exactly matches the gold answer and is fully supported by the retrieved context.

Retrieved context:

### ns_ht_creep_rafting_al_mobility_001

During 850 C creep of a directionally solidified nickel-based superalloy, aluminum mobility can control gamma-prime rafting. Larger plastic strain flow promotes P-type rafting, while restricted deformation can leave the gamma-prime structure less rafted.

### ns_ht_creep_orientation_850c_001

At 850 C, a directionally solidified nickel-based superalloy can show stronger creep resistance in the longitudinal orientation than in the transverse orientation. The longitudinal condition activates more slip systems and APB shearing, while the transverse condition is dominated by fewer slip bands and SISF-related deformation.

### ns_ht_pf_ml_creep_features_001

Phase-field-informed machine learning can predict creep strain from simulated microstructure and composition descriptors. Useful descriptors include gamma-prime rafting degree, gamma-prime volume fraction, interparticle spacing, and elemental partitioning coefficients.

### ns_ht_gh4169_entropy_fatigue_001

For GH4169 low-cycle fatigue at elevated temperature, a thermodynamic entropy method can connect cyclic plasticity modeling with fatigue-life prediction. Entropy generation in the gauge section can serve as a damage-related quantity rather than using stress amplitude alone.

### ns_ht_rejuvenation_heat_treatment_001

Rejuvenation heat treatment can recover creep-degraded directionally solidified superalloys by modifying gamma-prime morphology. In one optimized regime, solution treatment near 1283 C and primary aging near 1095 C restored most standard heat-treatment creep life and increased total creep life.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_oracle_reader::ns_ht_q021

- Priority: normal
- Reasons: none
- Method: flashrag_bm25_oracle_reader
- Question type: single_choice

Question:

At 1200 C and 80 MPa, what kind of result supports a transfer-learning-designed single-crystal superalloy candidate?
A. Rupture life above 170 h in creep validation
B. A shorter prompt context
C. A missing qrels file
D. A room-temperature hardness label only

Gold answers: ['A']
Prediction: A

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The model correctly identifies the creep validation result from the context.

Retrieved context:

### ns_ht_transfer_learning_creep_design_001

Transfer learning can guide single-crystal superalloy composition design for ultrahigh-temperature creep resistance. A designed alloy can be validated under 1200 C and 80 MPa creep, where rupture life above 170 h indicates that data-driven screening can still require experimental confirmation.

### ns_ht_rejuvenation_heat_treatment_001

Rejuvenation heat treatment can recover creep-degraded directionally solidified superalloys by modifying gamma-prime morphology. In one optimized regime, solution treatment near 1283 C and primary aging near 1095 C restored most standard heat-treatment creep life and increased total creep life.

### ns_ht_drilled_sx_hot_corrosion_001

A drilled nickel-based single-crystal superalloy can show abnormal hot-corrosion behavior because the hole surface changes diffusion paths and oxide-layer development. Local drilling can therefore alter scale adhesion and corrosion-product evolution around the machined region.

### ns_ht_gh4169_entropy_fatigue_001

For GH4169 low-cycle fatigue at elevated temperature, a thermodynamic entropy method can connect cyclic plasticity modeling with fatigue-life prediction. Entropy generation in the gauge section can serve as a damage-related quantity rather than using stress amplitude alone.

### ns_ht_creep_rafting_al_mobility_001

During 850 C creep of a directionally solidified nickel-based superalloy, aluminum mobility can control gamma-prime rafting. Larger plastic strain flow promotes P-type rafting, while restricted deformation can leave the gamma-prime structure less rafted.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_oracle_reader::ns_ht_q022

- Priority: normal
- Reasons: none
- Method: flashrag_bm25_oracle_reader
- Question type: fill_blank

Question:

A drilled single-crystal superalloy can alter scale adhesion and corrosion-product evolution around the ____ region.

Gold answers: ['machined']
Prediction: machined

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction matches the gold answer exactly and is directly supported by the retrieved context.

Retrieved context:

### ns_ht_drilled_sx_hot_corrosion_001

A drilled nickel-based single-crystal superalloy can show abnormal hot-corrosion behavior because the hole surface changes diffusion paths and oxide-layer development. Local drilling can therefore alter scale adhesion and corrosion-product evolution around the machined region.

### ns_ht_hot_corrosion_alloying_001

In molten-salt hot corrosion of nickel-based superalloys, alloying elements can change oxide-scale stability, internal sulfidation, and diffusion of protective elements. Damage can combine surface oxidation, internal sulfidation, scale cracking, and spallation rather than a single degradation mode.

### ns_ht_transfer_learning_creep_design_001

Transfer learning can guide single-crystal superalloy composition design for ultrahigh-temperature creep resistance. A designed alloy can be validated under 1200 C and 80 MPa creep, where rupture life above 170 h indicates that data-driven screening can still require experimental confirmation.

### ns_ht_oxidation_ce_coating_001

In additively manufactured IN625 exposed to 900 C air, intergranular oxidation can begin when scale buckling opens grain-boundary voids. A very thin cerium coating can improve chromia scale adherence and slow inward oxide growth.

### ns_ht_tic_in625_oxidation_001

TiC-containing Inconel 625 can change microstructural features that affect high-temperature oxidation behavior. Ceramic-particle additions may influence oxide-scale continuity, local element distribution, and oxidation resistance rather than acting only as inert reinforcement.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_oracle_reader::ns_ht_q023

- Priority: normal
- Reasons: none
- Method: flashrag_bm25_oracle_reader
- Question type: multiple_choice

Question:

Which statements compare hot-corrosion mitigation or modification mechanisms in the expanded corpus?
A. Pre-oxidation in SLM Inconel 625 can form a protective barrier
B. Molten-salt hot corrosion can involve scale cracking and spallation
C. Drilling can change local diffusion paths near a hole surface
D. All mechanisms are described as unrelated to oxide layers
E. TiC additions may affect oxide-scale continuity

Gold answers: ['A', 'B', 'C', 'E']
Prediction: A,B,C,E

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction matches the gold answer perfectly and each selected statement is explicitly supported by the retrieved context.

Retrieved context:

### ns_ht_slm_in625_preoxidation_001

For SLM Inconel 625, heat treatment combined with pre-oxidation can form a more protective oxide barrier before hot-corrosion exposure. The preformed barrier can improve corrosion resistance by slowing aggressive species from penetrating the additively manufactured microstructure.

### ns_ht_tic_in625_oxidation_001

TiC-containing Inconel 625 can change microstructural features that affect high-temperature oxidation behavior. Ceramic-particle additions may influence oxide-scale continuity, local element distribution, and oxidation resistance rather than acting only as inert reinforcement.

### ns_ht_hot_corrosion_alloying_001

In molten-salt hot corrosion of nickel-based superalloys, alloying elements can change oxide-scale stability, internal sulfidation, and diffusion of protective elements. Damage can combine surface oxidation, internal sulfidation, scale cracking, and spallation rather than a single degradation mode.

### ns_ht_drilled_sx_hot_corrosion_001

A drilled nickel-based single-crystal superalloy can show abnormal hot-corrosion behavior because the hole surface changes diffusion paths and oxide-layer development. Local drilling can therefore alter scale adhesion and corrosion-product evolution around the machined region.

### ns_ht_oxidation_gb_energy_001

Initial oxidation in Inconel 718 can depend on grain-boundary character. Boundaries with different energy states can change oxygen adsorption, diffusion, and oxide nucleation, so intergranular oxidation does not begin uniformly across all boundaries.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_oracle_reader::ns_ht_q024

- Priority: high
- Reasons: unsupported_claims, context_support_below_5, faithfulness_below_5, hallucination_risk_above_0
- Method: flashrag_bm25_oracle_reader
- Question type: short_answer

Question:

How do entropy-based fatigue prediction and PM-HIP fatigue review knowledge differ in the expanded corpus?

Gold answers: ['The entropy method treats entropy generation from cyclic plasticity as a damage-related predictor, while PM-HIP review knowledge emphasizes processing factors such as powder quality, residual defects, grain structure, and heat treatment.']
Prediction: The entropy method treats entropy generation from cyclic plasticity as a damage-related predictor, while PM-HIP review knowledge emphasizes processing factors such as powder quality, residual defects, grain structure, and heat treatment.

Judge:

correctness=5.0, context_support=0.0, faithfulness=0.0, unsupported_claims=entropy method treats entropy generation from cyclic plasticity as a damage-related predictor, reason=The prediction exactly matches the gold answer, yielding high correctness and relevance, but the entropy-based fatigue claim has no support in the retrieved context, leading to low context support and faithfulness.

Retrieved context:

### ns_ht_oxidation_gb_energy_001

Initial oxidation in Inconel 718 can depend on grain-boundary character. Boundaries with different energy states can change oxygen adsorption, diffusion, and oxide nucleation, so intergranular oxidation does not begin uniformly across all boundaries.

### ns_ht_pm_hip_fatigue_review_001

Powder metallurgy hot-isostatic-pressed superalloys can show fatigue behavior controlled by powder quality, residual defects, grain structure, and heat treatment. Reviewing these factors helps separate processing-driven fatigue limits from intrinsic alloy strengthening effects.

### ns_ht_oxidation_lpbf_gh3536_001

For LPBF GH3536 oxidized at 950 C, the cellular microstructure can provide rapid diffusion paths that accelerate protective-film formation during early exposure. After long exposure, the LPBF material can show better oxidation resistance than a wrought counterpart.

### ns_ht_creep_rafting_al_mobility_001

During 850 C creep of a directionally solidified nickel-based superalloy, aluminum mobility can control gamma-prime rafting. Larger plastic strain flow promotes P-type rafting, while restricted deformation can leave the gamma-prime structure less rafted.

### ns_ht_creep_orientation_850c_001

At 850 C, a directionally solidified nickel-based superalloy can show stronger creep resistance in the longitudinal orientation than in the transverse orientation. The longitudinal condition activates more slip systems and APB shearing, while the transverse condition is dominated by fewer slip bands and SISF-related deformation.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

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

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction matches the gold answer and is fully supported by the provided context.

Retrieved context:

### ns_ht_creep_rafting_al_mobility_001

During 850 C creep of a directionally solidified nickel-based superalloy, aluminum mobility can control gamma-prime rafting. Larger plastic strain flow promotes P-type rafting, while restricted deformation can leave the gamma-prime structure less rafted.

### ns_ht_pm_hip_fatigue_review_001

Powder metallurgy hot-isostatic-pressed superalloys can show fatigue behavior controlled by powder quality, residual defects, grain structure, and heat treatment. Reviewing these factors helps separate processing-driven fatigue limits from intrinsic alloy strengthening effects.

### ns_ht_pf_ml_creep_features_001

Phase-field-informed machine learning can predict creep strain from simulated microstructure and composition descriptors. Useful descriptors include gamma-prime rafting degree, gamma-prime volume fraction, interparticle spacing, and elemental partitioning coefficients.

### ns_ht_rejuvenation_heat_treatment_001

Rejuvenation heat treatment can recover creep-degraded directionally solidified superalloys by modifying gamma-prime morphology. In one optimized regime, solution treatment near 1283 C and primary aging near 1095 C restored most standard heat-treatment creep life and increased total creep life.

### ns_ht_creep_orientation_850c_001

At 850 C, a directionally solidified nickel-based superalloy can show stronger creep resistance in the longitudinal orientation than in the transverse orientation. The longitudinal condition activates more slip systems and APB shearing, while the transverse condition is dominated by fewer slip bands and SISF-related deformation.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_live_deepseek::ns_ht_q010

- Priority: high
- Reasons: answer_error, judge_error, correctness_below_5, context_support_below_5, faithfulness_below_5, hallucination_risk_above_0
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
Prediction:

Judge:

correctness=0.0, context_support=0.0, faithfulness=0.0, unsupported_claims=none, reason=answer row error: deepseek_response: message content must be non-empty

Retrieved context:

### ns_ht_oxidation_lpbf_gh3536_001

For LPBF GH3536 oxidized at 950 C, the cellular microstructure can provide rapid diffusion paths that accelerate protective-film formation during early exposure. After long exposure, the LPBF material can show better oxidation resistance than a wrought counterpart.

### ns_ht_oxidation_ce_coating_001

In additively manufactured IN625 exposed to 900 C air, intergranular oxidation can begin when scale buckling opens grain-boundary voids. A very thin cerium coating can improve chromia scale adherence and slow inward oxide growth.

### ns_ht_hot_corrosion_alloying_001

In molten-salt hot corrosion of nickel-based superalloys, alloying elements can change oxide-scale stability, internal sulfidation, and diffusion of protective elements. Damage can combine surface oxidation, internal sulfidation, scale cracking, and spallation rather than a single degradation mode.

### ns_ht_tic_in625_oxidation_001

TiC-containing Inconel 625 can change microstructural features that affect high-temperature oxidation behavior. Ceramic-particle additions may influence oxide-scale continuity, local element distribution, and oxidation resistance rather than acting only as inert reinforcement.

### ns_ht_drilled_sx_hot_corrosion_001

A drilled nickel-based single-crystal superalloy can show abnormal hot-corrosion behavior because the hole surface changes diffusion paths and oxide-layer development. Local drilling can therefore alter scale adhesion and corrosion-product evolution around the machined region.

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

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The predicted word 'intergranular' exactly matches the gold answer and is fully supported by the retrieved context.

Retrieved context:

### ns_ht_oxidation_ce_coating_001

In additively manufactured IN625 exposed to 900 C air, intergranular oxidation can begin when scale buckling opens grain-boundary voids. A very thin cerium coating can improve chromia scale adherence and slow inward oxide growth.

### ns_ht_hot_corrosion_alloying_001

In molten-salt hot corrosion of nickel-based superalloys, alloying elements can change oxide-scale stability, internal sulfidation, and diffusion of protective elements. Damage can combine surface oxidation, internal sulfidation, scale cracking, and spallation rather than a single degradation mode.

### ns_ht_am_abd900_heat_treatment_001

In additively manufactured ABD-900AM, grain size, heat treatment, and build orientation influence creep behavior. Super-solvus heat treatment can recrystallize and coarsen grains, improving creep resistance compared with a near-solvus condition.

### ns_ht_am_abd900_carbide_damage_001

Under high-temperature creep in additively manufactured ABD-900AM, MC carbides can grow near grain boundaries while consuming gamma-prime. This process can create precipitate-free zones and grain-boundary damage, with cavitation morphology depending on stress.

### ns_ht_tic_in625_oxidation_001

TiC-containing Inconel 625 can change microstructural features that affect high-temperature oxidation behavior. Ceramic-particle additions may influence oxide-scale continuity, local element distribution, and oxidation resistance rather than acting only as inert reinforcement.

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
Prediction: At 850°C, the longitudinal orientation yields stronger creep resistance by activating more slip systems and APB shearing. Larger plastic strain flow promotes P-type rafting, while restricted deformation limits rafting.

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction correctly states that longitudinal orientation activates more slip systems and APB shearing for creep resistance, and larger plastic strain flow promotes P-type rafting, all supported by context and matching the gold answer.

Retrieved context:

### ns_ht_creep_rafting_al_mobility_001

During 850 C creep of a directionally solidified nickel-based superalloy, aluminum mobility can control gamma-prime rafting. Larger plastic strain flow promotes P-type rafting, while restricted deformation can leave the gamma-prime structure less rafted.

### ns_ht_creep_orientation_850c_001

At 850 C, a directionally solidified nickel-based superalloy can show stronger creep resistance in the longitudinal orientation than in the transverse orientation. The longitudinal condition activates more slip systems and APB shearing, while the transverse condition is dominated by fewer slip bands and SISF-related deformation.

### ns_ht_pf_ml_creep_features_001

Phase-field-informed machine learning can predict creep strain from simulated microstructure and composition descriptors. Useful descriptors include gamma-prime rafting degree, gamma-prime volume fraction, interparticle spacing, and elemental partitioning coefficients.

### ns_ht_gh4169_entropy_fatigue_001

For GH4169 low-cycle fatigue at elevated temperature, a thermodynamic entropy method can connect cyclic plasticity modeling with fatigue-life prediction. Entropy generation in the gauge section can serve as a damage-related quantity rather than using stress amplitude alone.

### ns_ht_rejuvenation_heat_treatment_001

Rejuvenation heat treatment can recover creep-degraded directionally solidified superalloys by modifying gamma-prime morphology. In one optimized regime, solution treatment near 1283 C and primary aging near 1095 C restored most standard heat-treatment creep life and increased total creep life.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_live_deepseek::ns_ht_q021

- Priority: normal
- Reasons: none
- Method: flashrag_bm25_live_deepseek
- Question type: single_choice

Question:

At 1200 C and 80 MPa, what kind of result supports a transfer-learning-designed single-crystal superalloy candidate?
A. Rupture life above 170 h in creep validation
B. A shorter prompt context
C. A missing qrels file
D. A room-temperature hardness label only

Gold answers: ['A']
Prediction: A

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction matches the gold answer and is fully supported by the retrieved context describing rupture life above 170 h as validation.

Retrieved context:

### ns_ht_transfer_learning_creep_design_001

Transfer learning can guide single-crystal superalloy composition design for ultrahigh-temperature creep resistance. A designed alloy can be validated under 1200 C and 80 MPa creep, where rupture life above 170 h indicates that data-driven screening can still require experimental confirmation.

### ns_ht_rejuvenation_heat_treatment_001

Rejuvenation heat treatment can recover creep-degraded directionally solidified superalloys by modifying gamma-prime morphology. In one optimized regime, solution treatment near 1283 C and primary aging near 1095 C restored most standard heat-treatment creep life and increased total creep life.

### ns_ht_drilled_sx_hot_corrosion_001

A drilled nickel-based single-crystal superalloy can show abnormal hot-corrosion behavior because the hole surface changes diffusion paths and oxide-layer development. Local drilling can therefore alter scale adhesion and corrosion-product evolution around the machined region.

### ns_ht_gh4169_entropy_fatigue_001

For GH4169 low-cycle fatigue at elevated temperature, a thermodynamic entropy method can connect cyclic plasticity modeling with fatigue-life prediction. Entropy generation in the gauge section can serve as a damage-related quantity rather than using stress amplitude alone.

### ns_ht_creep_rafting_al_mobility_001

During 850 C creep of a directionally solidified nickel-based superalloy, aluminum mobility can control gamma-prime rafting. Larger plastic strain flow promotes P-type rafting, while restricted deformation can leave the gamma-prime structure less rafted.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_live_deepseek::ns_ht_q022

- Priority: normal
- Reasons: none
- Method: flashrag_bm25_live_deepseek
- Question type: fill_blank

Question:

A drilled single-crystal superalloy can alter scale adhesion and corrosion-product evolution around the ____ region.

Gold answers: ['machined']
Prediction: machined

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction exactly matches the gold answer and is directly supported by the retrieved context.

Retrieved context:

### ns_ht_drilled_sx_hot_corrosion_001

A drilled nickel-based single-crystal superalloy can show abnormal hot-corrosion behavior because the hole surface changes diffusion paths and oxide-layer development. Local drilling can therefore alter scale adhesion and corrosion-product evolution around the machined region.

### ns_ht_hot_corrosion_alloying_001

In molten-salt hot corrosion of nickel-based superalloys, alloying elements can change oxide-scale stability, internal sulfidation, and diffusion of protective elements. Damage can combine surface oxidation, internal sulfidation, scale cracking, and spallation rather than a single degradation mode.

### ns_ht_transfer_learning_creep_design_001

Transfer learning can guide single-crystal superalloy composition design for ultrahigh-temperature creep resistance. A designed alloy can be validated under 1200 C and 80 MPa creep, where rupture life above 170 h indicates that data-driven screening can still require experimental confirmation.

### ns_ht_oxidation_ce_coating_001

In additively manufactured IN625 exposed to 900 C air, intergranular oxidation can begin when scale buckling opens grain-boundary voids. A very thin cerium coating can improve chromia scale adherence and slow inward oxide growth.

### ns_ht_tic_in625_oxidation_001

TiC-containing Inconel 625 can change microstructural features that affect high-temperature oxidation behavior. Ceramic-particle additions may influence oxide-scale continuity, local element distribution, and oxidation resistance rather than acting only as inert reinforcement.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_live_deepseek::ns_ht_q023

- Priority: normal
- Reasons: none
- Method: flashrag_bm25_live_deepseek
- Question type: multiple_choice

Question:

Which statements compare hot-corrosion mitigation or modification mechanisms in the expanded corpus?
A. Pre-oxidation in SLM Inconel 625 can form a protective barrier
B. Molten-salt hot corrosion can involve scale cracking and spallation
C. Drilling can change local diffusion paths near a hole surface
D. All mechanisms are described as unrelated to oxide layers
E. TiC additions may affect oxide-scale continuity

Gold answers: ['A', 'B', 'C', 'E']
Prediction: A,B,C,E

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The model prediction correctly includes all gold answer statements (A, B, C, E) and excludes the incorrect statement D, and each selected statement is directly supported by the retrieved context.

Retrieved context:

### ns_ht_slm_in625_preoxidation_001

For SLM Inconel 625, heat treatment combined with pre-oxidation can form a more protective oxide barrier before hot-corrosion exposure. The preformed barrier can improve corrosion resistance by slowing aggressive species from penetrating the additively manufactured microstructure.

### ns_ht_tic_in625_oxidation_001

TiC-containing Inconel 625 can change microstructural features that affect high-temperature oxidation behavior. Ceramic-particle additions may influence oxide-scale continuity, local element distribution, and oxidation resistance rather than acting only as inert reinforcement.

### ns_ht_hot_corrosion_alloying_001

In molten-salt hot corrosion of nickel-based superalloys, alloying elements can change oxide-scale stability, internal sulfidation, and diffusion of protective elements. Damage can combine surface oxidation, internal sulfidation, scale cracking, and spallation rather than a single degradation mode.

### ns_ht_drilled_sx_hot_corrosion_001

A drilled nickel-based single-crystal superalloy can show abnormal hot-corrosion behavior because the hole surface changes diffusion paths and oxide-layer development. Local drilling can therefore alter scale adhesion and corrosion-product evolution around the machined region.

### ns_ht_oxidation_gb_energy_001

Initial oxidation in Inconel 718 can depend on grain-boundary character. Boundaries with different energy states can change oxygen adsorption, diffusion, and oxide nucleation, so intergranular oxidation does not begin uniformly across all boundaries.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_live_deepseek::ns_ht_q024

- Priority: high
- Reasons: correctness_below_5
- Method: flashrag_bm25_live_deepseek
- Question type: short_answer

Question:

How do entropy-based fatigue prediction and PM-HIP fatigue review knowledge differ in the expanded corpus?

Gold answers: ['The entropy method treats entropy generation from cyclic plasticity as a damage-related predictor, while PM-HIP review knowledge emphasizes processing factors such as powder quality, residual defects, grain structure, and heat treatment.']
Prediction: The supplied context chunks do not include information on entropy-based fatigue prediction, so a comparison with PM-HIP fatigue review knowledge cannot be made from the given corpus.

Judge:

correctness=0.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The model correctly identifies the lack of entropy-based prediction information in the context, but this does not match the gold answer that provides a specific comparison.

Retrieved context:

### ns_ht_oxidation_gb_energy_001

Initial oxidation in Inconel 718 can depend on grain-boundary character. Boundaries with different energy states can change oxygen adsorption, diffusion, and oxide nucleation, so intergranular oxidation does not begin uniformly across all boundaries.

### ns_ht_pm_hip_fatigue_review_001

Powder metallurgy hot-isostatic-pressed superalloys can show fatigue behavior controlled by powder quality, residual defects, grain structure, and heat treatment. Reviewing these factors helps separate processing-driven fatigue limits from intrinsic alloy strengthening effects.

### ns_ht_oxidation_lpbf_gh3536_001

For LPBF GH3536 oxidized at 950 C, the cellular microstructure can provide rapid diffusion paths that accelerate protective-film formation during early exposure. After long exposure, the LPBF material can show better oxidation resistance than a wrought counterpart.

### ns_ht_creep_rafting_al_mobility_001

During 850 C creep of a directionally solidified nickel-based superalloy, aluminum mobility can control gamma-prime rafting. Larger plastic strain flow promotes P-type rafting, while restricted deformation can leave the gamma-prime structure less rafted.

### ns_ht_creep_orientation_850c_001

At 850 C, a directionally solidified nickel-based superalloy can show stronger creep resistance in the longitudinal orientation than in the transverse orientation. The longitudinal condition activates more slip systems and APB shearing, while the transverse condition is dominated by fewer slip bands and SISF-related deformation.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:
