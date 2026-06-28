# DomainRAG Human Calibration Packet

Questions for review: 100

## fresh_hard::no_rag::ns_ht_q009

- Priority: high
- Reasons: context_support_below_5
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

correctness=5.0, context_support=0.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction correctly selects the right answer but no retrieved context was supplied to support it.

Retrieved context:

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::no_rag::ns_ht_q010

- Priority: high
- Reasons: correctness_below_5, context_support_below_5
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

correctness=0.0, context_support=0.0, faithfulness=5.0, unsupported_claims=none, reason=The model only selected option C, while the gold answer set consists of A, B, D, and E, resulting in a complete mismatch.

Retrieved context:

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::no_rag::ns_ht_q011

- Priority: high
- Reasons: unsupported_claims, context_support_below_5, faithfulness_below_5, hallucination_risk_above_0
- Method: no_rag
- Question type: fill_blank

Question:

In AM IN625 exposed to 900 C air, scale buckling can open grain-boundary voids and initiate ____ oxidation.

Gold answers: ['intergranular']
Prediction: intergranular

Judge:

correctness=5.0, context_support=0.0, faithfulness=0.0, unsupported_claims=The oxidation initiated is intergranular., reason=The prediction correctly fills the blank as 'intergranular' but there is no retrieved context to support the claim, making it context-unsupported and unfaithful.

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
Prediction: At 850°C, longitudinal orientation aligns the tensile stress with the <001> direction, and plastic strain flow introduces dislocations that relax coherency stresses. These dislocations, combined with positive lattice misfit, drive directional diffusion that favors P-type rafting, aligning γ' precipitates parallel to the stress axis. The resulting rafted structure strongly impedes dislocation motion, enhancing creep resistance.

Judge:

correctness=0.0, context_support=0.0, faithfulness=0.0, unsupported_claims=longitudinal orientation aligns tensile stress with <001> direction; dislocations relax coherency stresses; positive lattice misfit drives directional diffusion, reason=The prediction misses required points (more slip systems, APB shearing) and introduces unsupported claims about stress alignment and coherency stress relaxation.

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

correctness=5.0, context_support=0.0, faithfulness=5.0, unsupported_claims=none, reason=The model prediction matches the gold answer; no context was provided to assess support.

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
Prediction: hole

Judge:

correctness=0.0, context_support=0.0, faithfulness=0.0, unsupported_claims=The region around the drilled area is referred to as the 'hole' region., reason=The prediction 'hole' is not the correct term 'machined' and introduces an unsupported claim without context.

Retrieved context:

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::no_rag::ns_ht_q023

- Priority: high
- Reasons: correctness_below_5, context_support_below_5
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
Prediction: A,C,E

Judge:

correctness=3.0, context_support=0.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction correctly selects A, C, and E but misses B, so it is partially correct; no unsupported claims.

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
Prediction: Entropy-based fatigue prediction focuses on using thermodynamic entropy generation as a physics-based damage metric to predict fatigue life, while PM-HIP fatigue review knowledge compiles experimental and empirical findings on the fatigue behavior of materials processed via powder metallurgy with hot isostatic pressing, emphasizing process-property relationships and defect influences.

Judge:

correctness=3.0, context_support=0.0, faithfulness=0.0, unsupported_claims=Entropy-based fatigue prediction uses thermodynamic entropy generation as a physics-based damage metric.; PM-HIP fatigue review knowledge compiles experimental and empirical findings., reason=The model prediction captures the main distinction but misses explicit mention of cyclic plasticity, grain structure, and heat treatment. Without retrieved context, all claims are unsupported.

Retrieved context:

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::no_rag::ns_ht_q049

- Priority: high
- Reasons: unsupported_claims, context_support_below_5, faithfulness_below_5, hallucination_risk_above_0
- Method: no_rag
- Question type: single_choice

Question:

Which mechanism explains why a correct gold answer can still be poorly supported if BM25 retrieves only part of a multi-source question?
A. A method may hit one relevant chunk while missing another required evidence chunk
B. A hit on any chunk always proves full evidence recall
C. Retrieval recall is unrelated to source_chunk_ids
D. Oracle context removes all need for qrels

Gold answers: ['A']
Prediction: A

Judge:

correctness=5.0, context_support=0.0, faithfulness=0.0, unsupported_claims=The assertion that option A explains the mechanism is not supported by any retrieved context., reason=The prediction correctly identifies the answer but lacks supporting context, leading to low context support and faithfulness.

Retrieved context:

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::no_rag::ns_ht_q050

- Priority: high
- Reasons: context_support_below_5
- Method: no_rag
- Question type: fill_blank

Question:

In AM nickel superalloys, powder oxygen pickup, contamination, recycling history, and flowability are feedstock ____ factors.

Gold answers: ['quality']
Prediction: quality

Judge:

correctness=5.0, context_support=0.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction matches the gold answer exactly, but no context was provided, so context support is 0.

Retrieved context:

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::no_rag::ns_ht_q051

- Priority: high
- Reasons: unsupported_claims, correctness_below_5, context_support_below_5, faithfulness_below_5, hallucination_risk_above_0
- Method: no_rag
- Question type: short_answer

Question:

Compare steam oxidation of Rene 77 with chloride molten-salt corrosion of Inconel 625.

Gold answers: ['Rene 77 steam oxidation can become controlled by a more continuous oxide scale, while chloride molten salt can selectively dissolve chromium and molybdenum and form nonprotective corrosion products.']
Prediction: Steam oxidation of Rene 77 typically results in protective chromia or alumina scales with moderate kinetics governed by solid-state diffusion, whereas chloride molten-salt corrosion of Inconel 625 aggressively attacks the alloy through oxide fluxing and dissolution, causing rapid metal loss and intergranular damage. The steam environment poses a less severe threat compared to the highly corrosive molten chlorides, which induce electrochemical reactions and volatile chloride formation. Rene 77 relies on aluminum and chromium for oxidation resistance, but Inconel 625's molybdenum and niobium offer limited protection against molten salt attack.

Judge:

correctness=3.0, context_support=0.0, faithfulness=0.0, unsupported_claims=Steam oxidation of Rene 77 results in protective chromia or alumina scales with moderate kinetics governed by solid-state diffusion.; Chloride molten-salt corrosion of Inconel 625 aggressively attacks the alloy through oxide fluxing and dissolution, causing rapid metal loss and intergranular damage.; Rene 77 relies on aluminum and chromium for oxidation resistance, but Inconel 625's molybdenum and niobium offer limited protection against molten salt attack., reason=Prediction partially covers continuous oxide scale but misses selective dissolution and depletion; no context support makes all claims unsupported.

Retrieved context:

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::no_rag::ns_ht_q052

- Priority: high
- Reasons: unsupported_claims, correctness_below_5, context_support_below_5, faithfulness_below_5, hallucination_risk_above_0
- Method: no_rag
- Question type: multiple_choice

Question:

Which statements compare molten-salt and SO2 corrosion mechanisms in the medium corpus?
A. FLiNaK stress can accelerate grain-boundary attack in Hastelloy N
B. SO2 exposure can promote sulfur-assisted corrosion in K452
C. Chloride molten salt can deplete chromium and molybdenum in Inconel 625
D. All three mechanisms are independent of grain boundaries or selective chemistry
E. Chromium-rich protective scales can be destabilized or depleted

Gold answers: ['A', 'B', 'C', 'E']
Prediction: D

Judge:

correctness=0.0, context_support=0.0, faithfulness=0.0, unsupported_claims=All three mechanisms are independent of grain boundaries or selective chemistry, reason=The model predicted the single incorrect option D, missing the correct comparisons in A, B, C, and E.

Retrieved context:

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::no_rag::ns_ht_q053

- Priority: high
- Reasons: context_support_below_5
- Method: no_rag
- Question type: single_choice

Question:

What makes DD5 over-temperature damage a creep risk even without obvious TCP phase formation?
A. Gamma-prime coarsening can weaken dislocation-network and Orowan resistance
B. The alloy becomes immune to dislocation motion
C. TCP absence always means rupture life is unchanged
D. Over-temperature exposure removes gamma/gamma-prime morphology

Gold answers: ['A']
Prediction: A

Judge:

correctness=5.0, context_support=0.0, faithfulness=5.0, unsupported_claims=none, reason=Correctly identifies option A, perfectly matching the gold answer without adding unsupported claims.

Retrieved context:

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::no_rag::ns_ht_q054

- Priority: high
- Reasons: context_support_below_5
- Method: no_rag
- Question type: fill_blank

Question:

Feature-importance analysis in PF-informed creep models can rank gamma-prime volume fraction and lattice ____.

Gold answers: ['misfit']
Prediction: misfit

Judge:

correctness=5.0, context_support=0.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction matches the gold answer exactly.

Retrieved context:

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::no_rag::ns_ht_q055

- Priority: high
- Reasons: unsupported_claims, correctness_below_5, context_support_below_5, faithfulness_below_5, hallucination_risk_above_0
- Method: no_rag
- Question type: short_answer

Question:

How do AM Hastelloy X fatigue modelling and AM defect taxonomy connect in the medium corpus?

Gold answers: ['Fatigue models link texture, grains, cyclic plasticity, and damage, while defect taxonomy identifies pores, cracks, residual stress, roughness, and segregation that influence fatigue initiation.']
Prediction: In the medium corpus, AM Hastelloy X fatigue modelling relies on defect taxonomy to classify flaws such as porosity and lack of fusion, which are critical inputs for predicting fatigue behavior and assessing structural integrity.

Judge:

correctness=2.0, context_support=0.0, faithfulness=0.0, unsupported_claims=Fatigue modelling relies on defect taxonomy; Defect taxonomy classifies porosity and lack of fusion; Flaws are critical inputs for predicting fatigue behavior, reason=The prediction partially matches the gold answer but omits key details like microstructure and cyclic plasticity; no context supports any claims.

Retrieved context:

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::no_rag::ns_ht_q056

- Priority: high
- Reasons: correctness_below_5, context_support_below_5
- Method: no_rag
- Question type: multiple_choice

Question:

Which statements synthesize coating, steam, and film-cooling corrosion risks?
A. Coating-substrate interdiffusion can deplete protective elements
B. Inconel 740H-type alloys can depend on chromia continuity
C. Film-cooling holes can change local salt retention and scale growth
D. Water vapor, chlorides, and sulfur can destabilize protective scales
E. All hot-section features always improve scale adherence

Gold answers: ['A', 'B', 'C', 'D']
Prediction: A,C,D

Judge:

correctness=4.0, context_support=0.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction correctly selects A, C, D but misses B, resulting in a mostly correct answer.

Retrieved context:

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::no_rag::ns_ht_q057

- Priority: high
- Reasons: context_support_below_5
- Method: no_rag
- Question type: single_choice

Question:

In high-temperature fatigue, what distinguishes environmental LCF degradation from heat-treatment phase control?
A. Environmental LCF can involve hydrogen or oxidation-assisted crack initiation, while phase control changes precipitates or segregation
B. Both are only dataset split labels
C. Hydrogen and oxidation cannot affect crack initiation
D. Heat treatment never changes precipitates

Gold answers: ['A']
Prediction: A

Judge:

correctness=5.0, context_support=0.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction correctly identifies option A as the answer, matching the gold answer.

Retrieved context:

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::no_rag::ns_ht_q058

- Priority: high
- Reasons: unsupported_claims, context_support_below_5, faithfulness_below_5, hallucination_risk_above_0
- Method: no_rag
- Question type: fill_blank

Question:

A rejuvenation treatment can improve gamma-prime morphology but may not remove prior creep ____.

Gold answers: ['damage']
Prediction: damage

Judge:

correctness=5.0, context_support=0.0, faithfulness=0.0, unsupported_claims=The answer 'damage' is not supported by any retrieved context., reason=The prediction matches the gold answer but lacks context support.

Retrieved context:

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::no_rag::ns_ht_q059

- Priority: high
- Reasons: correctness_below_5, context_support_below_5
- Method: no_rag
- Question type: short_answer

Question:

Compare LPBF CM247LC crack mitigation with Nimonic 263 creep-fatigue dwell damage.

Gold answers: ['LPBF CM247LC mitigation controls thermal gradients, residual stress, and liquid-film cracking, while Nimonic 263 dwell damage involves time-dependent creep-fatigue mechanisms such as grain-boundary oxidation, cavities, and cyclic plastic strain.']
Prediction: LPBF CM247LC crack mitigation strategies aim to prevent solidification cracking and residual stress-induced fractures via process control, whereas Nimonic 263 creep-fatigue dwell damage involves intergranular cavitation and oxidation under sustained high-temperature loads. Mitigation in CM247LC is a manufacturing challenge, while Nimonic 263 damage limits service life in high-temperature cyclic applications.

Judge:

correctness=4.0, context_support=0.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction covers the main comparison points but omits explicit mention of thermal gradients and liquid-film cracking for LPBF CM247LC.

Retrieved context:

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::no_rag::ns_ht_q060

- Priority: high
- Reasons: unsupported_claims, context_support_below_5, faithfulness_below_5, hallucination_risk_above_0
- Method: no_rag
- Question type: multiple_choice

Question:

Which statements synthesize the medium corpus' fatigue and life-prediction evidence?
A. PF-informed models can rank composition and microstructure descriptors
B. Hydrogen-assisted LCF can reduce ductility and promote crack initiation
C. Single-crystal LCF can involve competition between oxidation and pores
D. AM Hastelloy X models connect microstructure heterogeneity to fatigue life
E. Life prediction never uses microstructure or environment

Gold answers: ['A', 'B', 'C', 'D']
Prediction: A,B,C,D

Judge:

correctness=5.0, context_support=0.0, faithfulness=0.0, unsupported_claims=The statements A, B, C, D synthesize the medium corpus' fatigue and life-prediction evidence., reason=Prediction correctly selects all gold answers but lacks retrieved context to support the claims.

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

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction correctly identifies aluminum mobility, which is directly supported by the context.

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

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction exactly matches the gold answers, all supported by the context.

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

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction exactly matches the gold answer and is directly supported by the context.

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
Prediction: Longitudinal orientation activates more slip systems and APB shearing, giving stronger creep resistance. Larger plastic strain flow promotes P-type rafting.

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction accurately captures all required points from the gold answer and is fully supported by the context.

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

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction correctly selects option A, which is supported by the retrieved context indicating rupture life above 170 h validates the alloy.

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

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The model prediction 'machined' exactly matches the gold answer and is directly supported by the retrieved context.

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

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The model correctly identifies all four statements (A, B, C, E) that compare mechanisms, and each is supported by the retrieved context.

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
Prediction: Entropy-based prediction uses entropy generation as a damage-related quantity for fatigue-life prediction. PM-HIP fatigue review knowledge examines powder quality, residual defects, grain structure, and heat treatment to distinguish processing-driven fatigue limits from intrinsic alloy strengthening effects.

Judge:

correctness=4.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction correctly distinguishes the entropy method as using damage-related entropy generation and PM-HIP as focusing on processing factors, but omits explicit mention of cyclic plasticity.

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

## fresh_hard::oracle_context::ns_ht_q049

- Priority: high
- Reasons: context_support_below_5
- Method: oracle_context
- Question type: single_choice

Question:

Which mechanism explains why a correct gold answer can still be poorly supported if BM25 retrieves only part of a multi-source question?
A. A method may hit one relevant chunk while missing another required evidence chunk
B. A hit on any chunk always proves full evidence recall
C. Retrieval recall is unrelated to source_chunk_ids
D. Oracle context removes all need for qrels

Gold answers: ['A']
Prediction: A

Judge:

correctness=5.0, context_support=0.0, faithfulness=5.0, unsupported_claims=none, reason=The predicted answer is correct and faithful, but the retrieved context about DD5 superalloy is entirely unrelated to the BM25 retrieval question, hence no context support.

Retrieved context:

### ns_ht_dd5_creep_rupture_overtemp_001

After over-temperature exposure, DD5 creep rupture life at high temperature can decrease even when no obvious TCP phase forms. The reduction is associated with coarsened gamma-prime, weakened dislocation networks, and less effective Orowan bypass resistance.

### ns_ht_dd5_overtemp_gamma_prime_001

A second-generation DD5 single-crystal superalloy can retain phase stability after short over-temperature exposure, but gamma-prime coarsening and changes in the gamma/gamma-prime morphology reduce the density of obstacles to dislocation motion.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::oracle_context::ns_ht_q050

- Priority: normal
- Reasons: none
- Method: oracle_context
- Question type: fill_blank

Question:

In AM nickel superalloys, powder oxygen pickup, contamination, recycling history, and flowability are feedstock ____ factors.

Gold answers: ['quality']
Prediction: quality

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction correctly fills the blank with 'quality', matching the gold answer and aligning with the context's discussion of feedstock factors.

Retrieved context:

### ns_ht_am_review_feedstock_quality_001

Recent reviews of additively manufactured nickel superalloys emphasize that powder morphology, oxygen pickup, contamination, recycling history, and flowability influence defect formation before any heat treatment is applied.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::oracle_context::ns_ht_q051

- Priority: normal
- Reasons: none
- Method: oracle_context
- Question type: short_answer

Question:

Compare steam oxidation of Rene 77 with chloride molten-salt corrosion of Inconel 625.

Gold answers: ['Rene 77 steam oxidation can become controlled by a more continuous oxide scale, while chloride molten salt can selectively dissolve chromium and molybdenum and form nonprotective corrosion products.']
Prediction: Steam oxidation of Rene 77 can slow mass gain and form a chromium-rich oxide scale whose protectiveness depends on compactness and spallation. In contrast, chloride molten-salt corrosion of Inconel 625 causes selective dissolution, loss of chromium and molybdenum, and formation of nonprotective products; chloride salts are more aggressive than simple dry oxidation.

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction accurately compares the corrosion mechanisms, matching the gold answer and context completely.

Retrieved context:

### ns_ht_rene77_steam_oxidation_001

During long high-temperature steam oxidation of Rene 77, mass gain can slow after an initial transient as a more continuous oxide scale develops. Changes in scale compactness, local spallation, and chromium-rich oxide formation control whether the oxide remains protective.

### ns_ht_in625_molten_salt_chloride_001

Inconel 625 exposed to chloride-containing molten salts can lose chromium and molybdenum from the near-surface region. Selective dissolution and nonprotective corrosion products can make chloride salts more aggressive than simple dry oxidation.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::oracle_context::ns_ht_q052

- Priority: normal
- Reasons: none
- Method: oracle_context
- Question type: multiple_choice

Question:

Which statements compare molten-salt and SO2 corrosion mechanisms in the medium corpus?
A. FLiNaK stress can accelerate grain-boundary attack in Hastelloy N
B. SO2 exposure can promote sulfur-assisted corrosion in K452
C. Chloride molten salt can deplete chromium and molybdenum in Inconel 625
D. All three mechanisms are independent of grain boundaries or selective chemistry
E. Chromium-rich protective scales can be destabilized or depleted

Gold answers: ['A', 'B', 'C', 'E']
Prediction: A,B,C,E

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction matches the gold answer exactly and is fully supported by the retrieved context.

Retrieved context:

### ns_ht_hastelloyn_stress_flinak_001

In FLiNaK molten salt, applied stress can increase Hastelloy N corrosion rate compared with an unloaded condition. Stress-assisted corrosion is linked to accelerated grain-boundary attack and a higher weight-loss rate in the molten-salt environment.

### ns_ht_k452_so2_corrosion_001

For K452 nickel-based cast superalloy in high-temperature SO2-containing atmospheres, long exposure can promote sulfur-assisted corrosion. Damage involves oxide-scale evolution, sulfur penetration, and corrosion products that are less protective than a stable chromia-rich scale.

### ns_ht_in625_molten_salt_chloride_001

Inconel 625 exposed to chloride-containing molten salts can lose chromium and molybdenum from the near-surface region. Selective dissolution and nonprotective corrosion products can make chloride salts more aggressive than simple dry oxidation.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::oracle_context::ns_ht_q053

- Priority: normal
- Reasons: none
- Method: oracle_context
- Question type: single_choice

Question:

What makes DD5 over-temperature damage a creep risk even without obvious TCP phase formation?
A. Gamma-prime coarsening can weaken dislocation-network and Orowan resistance
B. The alloy becomes immune to dislocation motion
C. TCP absence always means rupture life is unchanged
D. Over-temperature exposure removes gamma/gamma-prime morphology

Gold answers: ['A']
Prediction: A

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The model correctly selects option A, which matches the gold answer and is directly supported by the context.

Retrieved context:

### ns_ht_dd5_overtemp_gamma_prime_001

A second-generation DD5 single-crystal superalloy can retain phase stability after short over-temperature exposure, but gamma-prime coarsening and changes in the gamma/gamma-prime morphology reduce the density of obstacles to dislocation motion.

### ns_ht_dd5_creep_rupture_overtemp_001

After over-temperature exposure, DD5 creep rupture life at high temperature can decrease even when no obvious TCP phase forms. The reduction is associated with coarsened gamma-prime, weakened dislocation networks, and less effective Orowan bypass resistance.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::oracle_context::ns_ht_q054

- Priority: normal
- Reasons: none
- Method: oracle_context
- Question type: fill_blank

Question:

Feature-importance analysis in PF-informed creep models can rank gamma-prime volume fraction and lattice ____.

Gold answers: ['misfit']
Prediction: misfit

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction 'misfit' exactly matches the gold answer and is directly supported by the retrieved context listing 'lattice misfit'.

Retrieved context:

### ns_ht_pfml_shap_design_features_001

Feature-importance analysis in phase-field-informed creep models can rank descriptors such as aluminum partitioning, cobalt partitioning, lattice misfit, gamma-prime volume fraction, and rafting state. These descriptors connect composition and microstructure to predicted creep strain.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::oracle_context::ns_ht_q055

- Priority: high
- Reasons: correctness_below_5
- Method: oracle_context
- Question type: short_answer

Question:

How do AM Hastelloy X fatigue modelling and AM defect taxonomy connect in the medium corpus?

Gold answers: ['Fatigue models link texture, grains, cyclic plasticity, and damage, while defect taxonomy identifies pores, cracks, residual stress, roughness, and segregation that influence fatigue initiation.']
Prediction: The defect taxonomy lists defects that influence fatigue, and the fatigue models aim to connect AM microstructure heterogeneity (which can include such defects) to fatigue-life prediction.

Judge:

correctness=3.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction correctly summarizes the connection but lacks specific details from the gold answer, such as cyclic plasticity/damage and how defects influence initiation.

Retrieved context:

### ns_ht_am_hastelloyx_lcf_model_001

For additively manufactured Hastelloy X, microstructure-based low-cycle-fatigue models can combine measured texture or grain information with cyclic plasticity and damage parameters. Such models try to connect AM microstructure heterogeneity to fatigue-life prediction.

### ns_ht_am_review_defect_taxonomy_001

Common AM nickel-superalloy defect classes include lack-of-fusion pores, gas pores, keyhole porosity, microcracks, residual stress, rough surfaces, and microsegregation. These defects influence fatigue, creep, oxidation, and hot-corrosion performance differently.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::oracle_context::ns_ht_q056

- Priority: normal
- Reasons: none
- Method: oracle_context
- Question type: multiple_choice

Question:

Which statements synthesize coating, steam, and film-cooling corrosion risks?
A. Coating-substrate interdiffusion can deplete protective elements
B. Inconel 740H-type alloys can depend on chromia continuity
C. Film-cooling holes can change local salt retention and scale growth
D. Water vapor, chlorides, and sulfur can destabilize protective scales
E. All hot-section features always improve scale adherence

Gold answers: ['A', 'B', 'C', 'D']
Prediction: A,B,C,D

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The model correctly selected all and only the true synthesis statements A, B, C, D, which are directly supported by the retrieved context.

Retrieved context:

### ns_ht_mar_m247_coating_diffusion_001

Protective coatings on MAR-M247-type nickel superalloys rely on aluminum or chromium reservoirs to form adherent oxides. Interdiffusion between coating and substrate can deplete protective elements and change long-term oxidation resistance.

### ns_ht_inconel740h_steam_oxidation_001

Inconel 740H and related nickel alloys in steam or fireside environments can depend on chromia continuity for corrosion resistance. Water vapor, chlorides, and sulfur species can destabilize the oxide scale and accelerate chromium depletion.

### ns_ht_filmcooling_hot_corrosion_001

Film-cooling holes in nickel-based turbine alloys can alter molten-salt hot-corrosion behavior by changing local salt retention, gas access, oxide-scale growth, and stress concentration around the hole surface.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::oracle_context::ns_ht_q057

- Priority: normal
- Reasons: none
- Method: oracle_context
- Question type: single_choice

Question:

In high-temperature fatigue, what distinguishes environmental LCF degradation from heat-treatment phase control?
A. Environmental LCF can involve hydrogen or oxidation-assisted crack initiation, while phase control changes precipitates or segregation
B. Both are only dataset split labels
C. Hydrogen and oxidation cannot affect crack initiation
D. Heat treatment never changes precipitates

Gold answers: ['A']
Prediction: A

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction correctly selects option A, which accurately distinguishes environmental LCF degradation (hydrogen/oxidation-assisted) from heat-treatment phase control (precipitate/segregation changes), and is fully supported by the retrieved context.

Retrieved context:

### ns_ht_in718_hydrogen_lcf_001

Hydrogen-assisted low-cycle fatigue in Inconel 718 can reduce ductility and promote earlier crack initiation. Elevated temperature can interact with hydrogen transport, slip localization, and crack growth, making fatigue life sensitive to environment.

### ns_ht_sx_lcf_oxidation_competition_001

In high-temperature low-cycle fatigue of single-crystal nickel superalloys, surface oxidation and internal casting pores can compete as crack-initiation sites. Load ratio, hold time, and cycling frequency can shift the dominant damage mechanism.

### ns_ht_gh4169_laves_delta_heat_001

In GH4169/Inconel 718, Laves phase formed during solidification can consume niobium and weaken the matrix. Homogenization and aging treatments can reduce segregation, promote delta or gamma-double-prime control, and change creep or fatigue behavior.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::oracle_context::ns_ht_q058

- Priority: normal
- Reasons: none
- Method: oracle_context
- Question type: fill_blank

Question:

A rejuvenation treatment can improve gamma-prime morphology but may not remove prior creep ____.

Gold answers: ['damage']
Prediction: damage

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction matches the gold answer and is supported by the context.

Retrieved context:

### ns_ht_sx_rejuvenation_tcp_001

Rejuvenation or recovery heat treatments for single-crystal superalloys must balance gamma-prime restoration against risks such as TCP phase persistence, recrystallization, and residual creep damage. A treatment that improves precipitate morphology may not fully remove prior damage.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::oracle_context::ns_ht_q059

- Priority: normal
- Reasons: none
- Method: oracle_context
- Question type: short_answer

Question:

Compare LPBF CM247LC crack mitigation with Nimonic 263 creep-fatigue dwell damage.

Gold answers: ['LPBF CM247LC mitigation controls thermal gradients, residual stress, and liquid-film cracking, while Nimonic 263 dwell damage involves time-dependent creep-fatigue mechanisms such as grain-boundary oxidation, cavities, and cyclic plastic strain.']
Prediction: LPBF CM247LC crack mitigation requires control of thermal gradients, residual stress, and grain-boundary liquid films; process optimization and heat treatment reduce but may not eliminate cracking. Nimonic 263 creep-fatigue dwell damage involves grain-boundary oxidation, cavity formation, and cyclic plastic strain, with dwell periods allowing time-dependent damage.

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction accurately compares the two phenomena, covering all required points and using only supported information.

Retrieved context:

### ns_ht_cm247lc_lpbf_crack_mitigation_001

LPBF processing of crack-susceptible CM247LC-class superalloys requires control of thermal gradients, residual stress, and grain-boundary liquid films. Process optimization and heat treatment can reduce cracking but may not remove all solidification-related defects.

### ns_ht_nimonic263_creep_fatigue_interaction_001

Nimonic 263-type nickel superalloys can show creep-fatigue interaction at high temperature when dwell periods allow time-dependent damage. Grain-boundary oxidation, cavity formation, and cyclic plastic strain jointly control life.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::oracle_context::ns_ht_q060

- Priority: normal
- Reasons: none
- Method: oracle_context
- Question type: multiple_choice

Question:

Which statements synthesize the medium corpus' fatigue and life-prediction evidence?
A. PF-informed models can rank composition and microstructure descriptors
B. Hydrogen-assisted LCF can reduce ductility and promote crack initiation
C. Single-crystal LCF can involve competition between oxidation and pores
D. AM Hastelloy X models connect microstructure heterogeneity to fatigue life
E. Life prediction never uses microstructure or environment

Gold answers: ['A', 'B', 'C', 'D']
Prediction: A,B,C,D

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction exactly matches the gold answers and each statement is supported by the retrieved context.

Retrieved context:

### ns_ht_pfml_shap_design_features_001

Feature-importance analysis in phase-field-informed creep models can rank descriptors such as aluminum partitioning, cobalt partitioning, lattice misfit, gamma-prime volume fraction, and rafting state. These descriptors connect composition and microstructure to predicted creep strain.

### ns_ht_in718_hydrogen_lcf_001

Hydrogen-assisted low-cycle fatigue in Inconel 718 can reduce ductility and promote earlier crack initiation. Elevated temperature can interact with hydrogen transport, slip localization, and crack growth, making fatigue life sensitive to environment.

### ns_ht_sx_lcf_oxidation_competition_001

In high-temperature low-cycle fatigue of single-crystal nickel superalloys, surface oxidation and internal casting pores can compete as crack-initiation sites. Load ratio, hold time, and cycling frequency can shift the dominant damage mechanism.

### ns_ht_am_hastelloyx_lcf_model_001

For additively manufactured Hastelloy X, microstructure-based low-cycle-fatigue models can combine measured texture or grain information with cyclic plasticity and damage parameters. Such models try to connect AM microstructure heterogeneity to fatigue-life prediction.

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

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction matches the gold answer and is directly supported by the retrieved context.

Retrieved context:

### ns_ht_creep_rafting_al_mobility_001

During 850 C creep of a directionally solidified nickel-based superalloy, aluminum mobility can control gamma-prime rafting. Larger plastic strain flow promotes P-type rafting, while restricted deformation can leave the gamma-prime structure less rafted.

### ns_ht_rejuvenation_heat_treatment_001

Rejuvenation heat treatment can recover creep-degraded directionally solidified superalloys by modifying gamma-prime morphology. In one optimized regime, solution treatment near 1283 C and primary aging near 1095 C restored most standard heat-treatment creep life and increased total creep life.

### ns_ht_creep_orientation_850c_001

At 850 C, a directionally solidified nickel-based superalloy can show stronger creep resistance in the longitudinal orientation than in the transverse orientation. The longitudinal condition activates more slip systems and APB shearing, while the transverse condition is dominated by fewer slip bands and SISF-related deformation.

### ns_ht_dd5_overtemp_gamma_prime_001

A second-generation DD5 single-crystal superalloy can retain phase stability after short over-temperature exposure, but gamma-prime coarsening and changes in the gamma/gamma-prime morphology reduce the density of obstacles to dislocation motion.

### ns_ht_pf_ml_creep_features_001

Phase-field-informed machine learning can predict creep strain from simulated microstructure and composition descriptors. Useful descriptors include gamma-prime rafting degree, gamma-prime volume fraction, interparticle spacing, and elemental partitioning coefficients.

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

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction exactly matches the gold answer and all selected statements are supported by the retrieved context.

Retrieved context:

### ns_ht_oxidation_lpbf_gh3536_001

For LPBF GH3536 oxidized at 950 C, the cellular microstructure can provide rapid diffusion paths that accelerate protective-film formation during early exposure. After long exposure, the LPBF material can show better oxidation resistance than a wrought counterpart.

### ns_ht_oxidation_ce_coating_001

In additively manufactured IN625 exposed to 900 C air, intergranular oxidation can begin when scale buckling opens grain-boundary voids. A very thin cerium coating can improve chromia scale adherence and slow inward oxide growth.

### ns_ht_rene77_steam_oxidation_001

During long high-temperature steam oxidation of Rene 77, mass gain can slow after an initial transient as a more continuous oxide scale develops. Changes in scale compactness, local spallation, and chromium-rich oxide formation control whether the oxide remains protective.

### ns_ht_slm_in625_preoxidation_001

For SLM Inconel 625, heat treatment combined with pre-oxidation can form a more protective oxide barrier before hot-corrosion exposure. The preformed barrier can improve corrosion resistance by slowing aggressive species from penetrating the additively manufactured microstructure.

### ns_ht_creep_orientation_850c_001

At 850 C, a directionally solidified nickel-based superalloy can show stronger creep resistance in the longitudinal orientation than in the transverse orientation. The longitudinal condition activates more slip systems and APB shearing, while the transverse condition is dominated by fewer slip bands and SISF-related deformation.

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

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction exactly matches the gold answer and is directly stated in the provided context.

Retrieved context:

### ns_ht_oxidation_ce_coating_001

In additively manufactured IN625 exposed to 900 C air, intergranular oxidation can begin when scale buckling opens grain-boundary voids. A very thin cerium coating can improve chromia scale adherence and slow inward oxide growth.

### ns_ht_oxidation_gb_energy_001

Initial oxidation in Inconel 718 can depend on grain-boundary character. Boundaries with different energy states can change oxygen adsorption, diffusion, and oxide nucleation, so intergranular oxidation does not begin uniformly across all boundaries.

### ns_ht_in625_molten_salt_chloride_001

Inconel 625 exposed to chloride-containing molten salts can lose chromium and molybdenum from the near-surface region. Selective dissolution and nonprotective corrosion products can make chloride salts more aggressive than simple dry oxidation.

### ns_ht_am_hastelloyx_lcf_model_001

For additively manufactured Hastelloy X, microstructure-based low-cycle-fatigue models can combine measured texture or grain information with cyclic plasticity and damage parameters. Such models try to connect AM microstructure heterogeneity to fatigue-life prediction.

### ns_ht_hastelloyn_stress_flinak_001

In FLiNaK molten salt, applied stress can increase Hastelloy N corrosion rate compared with an unloaded condition. Stress-assisted corrosion is linked to accelerated grain-boundary attack and a higher weight-loss rate in the molten-salt environment.

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
Prediction: At 850°C, a directionally solidified superalloy shows stronger creep resistance in the longitudinal orientation. The longitudinal orientation activates more slip systems and APB shearing. Larger plastic strain flow promotes P-type rafting.

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction fully captures the required points from the gold answer and is supported by the retrieved context.

Retrieved context:

### ns_ht_creep_rafting_al_mobility_001

During 850 C creep of a directionally solidified nickel-based superalloy, aluminum mobility can control gamma-prime rafting. Larger plastic strain flow promotes P-type rafting, while restricted deformation can leave the gamma-prime structure less rafted.

### ns_ht_creep_orientation_850c_001

At 850 C, a directionally solidified nickel-based superalloy can show stronger creep resistance in the longitudinal orientation than in the transverse orientation. The longitudinal condition activates more slip systems and APB shearing, while the transverse condition is dominated by fewer slip bands and SISF-related deformation.

### ns_ht_pfml_creep_stress_response_001

Phase-field-informed machine learning for nickel superalloy creep can use simulated microstructures at different stresses and temperatures. Higher applied stress typically increases creep strain, shortens the primary-creep regime, and changes rafting descriptors.

### ns_ht_nimonic263_creep_fatigue_interaction_001

Nimonic 263-type nickel superalloys can show creep-fatigue interaction at high temperature when dwell periods allow time-dependent damage. Grain-boundary oxidation, cavity formation, and cyclic plastic strain jointly control life.

### ns_ht_am_abd900_heat_treatment_001

In additively manufactured ABD-900AM, grain size, heat treatment, and build orientation influence creep behavior. Super-solvus heat treatment can recrystallize and coarsen grains, improving creep resistance compared with a near-solvus condition.

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

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The context explicitly states that rupture life above 170 h at 1200°C and 80 MPa validates the transfer-learning-designed alloy.

Retrieved context:

### ns_ht_transfer_learning_creep_design_001

Transfer learning can guide single-crystal superalloy composition design for ultrahigh-temperature creep resistance. A designed alloy can be validated under 1200 C and 80 MPa creep, where rupture life above 170 h indicates that data-driven screening can still require experimental confirmation.

### ns_ht_dd5_overtemp_gamma_prime_001

A second-generation DD5 single-crystal superalloy can retain phase stability after short over-temperature exposure, but gamma-prime coarsening and changes in the gamma/gamma-prime morphology reduce the density of obstacles to dislocation motion.

### ns_ht_gh4169_entropy_fatigue_001

For GH4169 low-cycle fatigue at elevated temperature, a thermodynamic entropy method can connect cyclic plasticity modeling with fatigue-life prediction. Entropy generation in the gauge section can serve as a damage-related quantity rather than using stress amplitude alone.

### ns_ht_rejuvenation_heat_treatment_001

Rejuvenation heat treatment can recover creep-degraded directionally solidified superalloys by modifying gamma-prime morphology. In one optimized regime, solution treatment near 1283 C and primary aging near 1095 C restored most standard heat-treatment creep life and increased total creep life.

### ns_ht_creep_rafting_al_mobility_001

During 850 C creep of a directionally solidified nickel-based superalloy, aluminum mobility can control gamma-prime rafting. Larger plastic strain flow promotes P-type rafting, while restricted deformation can leave the gamma-prime structure less rafted.

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

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction matches the gold answer and is directly supported by the retrieved context.

Retrieved context:

### ns_ht_drilled_sx_hot_corrosion_001

A drilled nickel-based single-crystal superalloy can show abnormal hot-corrosion behavior because the hole surface changes diffusion paths and oxide-layer development. Local drilling can therefore alter scale adhesion and corrosion-product evolution around the machined region.

### ns_ht_k452_so2_corrosion_001

For K452 nickel-based cast superalloy in high-temperature SO2-containing atmospheres, long exposure can promote sulfur-assisted corrosion. Damage involves oxide-scale evolution, sulfur penetration, and corrosion products that are less protective than a stable chromia-rich scale.

### ns_ht_filmcooling_hot_corrosion_001

Film-cooling holes in nickel-based turbine alloys can alter molten-salt hot-corrosion behavior by changing local salt retention, gas access, oxide-scale growth, and stress concentration around the hole surface.

### ns_ht_dd5_overtemp_gamma_prime_001

A second-generation DD5 single-crystal superalloy can retain phase stability after short over-temperature exposure, but gamma-prime coarsening and changes in the gamma/gamma-prime morphology reduce the density of obstacles to dislocation motion.

### ns_ht_hastelloyn_igc_cr_diffusion_001

Hastelloy N in FLiNaK can suffer intergranular corrosion because selective chromium diffusion and depletion at grain boundaries make the boundaries preferred paths for corrosion invasion. Loaded samples can show ridge-like corrosion products around grain-boundary regions.

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

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction correctly lists A, B, C, E, all of which are supported by the context, and excludes unsupported D.

Retrieved context:

### ns_ht_hot_corrosion_alloying_001

In molten-salt hot corrosion of nickel-based superalloys, alloying elements can change oxide-scale stability, internal sulfidation, and diffusion of protective elements. Damage can combine surface oxidation, internal sulfidation, scale cracking, and spallation rather than a single degradation mode.

### ns_ht_slm_in625_preoxidation_001

For SLM Inconel 625, heat treatment combined with pre-oxidation can form a more protective oxide barrier before hot-corrosion exposure. The preformed barrier can improve corrosion resistance by slowing aggressive species from penetrating the additively manufactured microstructure.

### ns_ht_drilled_sx_hot_corrosion_001

A drilled nickel-based single-crystal superalloy can show abnormal hot-corrosion behavior because the hole surface changes diffusion paths and oxide-layer development. Local drilling can therefore alter scale adhesion and corrosion-product evolution around the machined region.

### ns_ht_filmcooling_hot_corrosion_001

Film-cooling holes in nickel-based turbine alloys can alter molten-salt hot-corrosion behavior by changing local salt retention, gas access, oxide-scale growth, and stress concentration around the hole surface.

### ns_ht_tic_in625_oxidation_001

TiC-containing Inconel 625 can change microstructural features that affect high-temperature oxidation behavior. Ceramic-particle additions may influence oxide-scale continuity, local element distribution, and oxidation resistance rather than acting only as inert reinforcement.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::lexical_rag::ns_ht_q024

- Priority: high
- Reasons: correctness_below_5
- Method: lexical_rag
- Question type: short_answer

Question:

How do entropy-based fatigue prediction and PM-HIP fatigue review knowledge differ in the expanded corpus?

Gold answers: ['The entropy method treats entropy generation from cyclic plasticity as a damage-related predictor, while PM-HIP review knowledge emphasizes processing factors such as powder quality, residual defects, grain structure, and heat treatment.']
Prediction: The provided context does not contain any information about PM-HIP fatigue review; therefore, no difference can be described based on the supplied chunks.

Judge:

correctness=0.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The model correctly notes the absence of PM-HIP fatigue review information in the provided context, so it cannot describe the difference, making it faithful but not matching the gold answer.

Retrieved context:

### ns_ht_gh4169_entropy_fatigue_001

For GH4169 low-cycle fatigue at elevated temperature, a thermodynamic entropy method can connect cyclic plasticity modeling with fatigue-life prediction. Entropy generation in the gauge section can serve as a damage-related quantity rather than using stress amplitude alone.

### ns_ht_am_hastelloyx_lcf_model_001

For additively manufactured Hastelloy X, microstructure-based low-cycle-fatigue models can combine measured texture or grain information with cyclic plasticity and damage parameters. Such models try to connect AM microstructure heterogeneity to fatigue-life prediction.

### ns_ht_in718_hydrogen_lcf_001

Hydrogen-assisted low-cycle fatigue in Inconel 718 can reduce ductility and promote earlier crack initiation. Elevated temperature can interact with hydrogen transport, slip localization, and crack growth, making fatigue life sensitive to environment.

### ns_ht_creep_orientation_850c_001

At 850 C, a directionally solidified nickel-based superalloy can show stronger creep resistance in the longitudinal orientation than in the transverse orientation. The longitudinal condition activates more slip systems and APB shearing, while the transverse condition is dominated by fewer slip bands and SISF-related deformation.

### ns_ht_gh4169_laves_delta_heat_001

In GH4169/Inconel 718, Laves phase formed during solidification can consume niobium and weaken the matrix. Homogenization and aging treatments can reduce segregation, promote delta or gamma-double-prime control, and change creep or fatigue behavior.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::lexical_rag::ns_ht_q049

- Priority: high
- Reasons: unsupported_claims, context_support_below_5, faithfulness_below_5, hallucination_risk_above_0
- Method: lexical_rag
- Question type: single_choice

Question:

Which mechanism explains why a correct gold answer can still be poorly supported if BM25 retrieves only part of a multi-source question?
A. A method may hit one relevant chunk while missing another required evidence chunk
B. A hit on any chunk always proves full evidence recall
C. Retrieval recall is unrelated to source_chunk_ids
D. Oracle context removes all need for qrels

Gold answers: ['A']
Prediction: A

Judge:

correctness=5.0, context_support=0.0, faithfulness=0.0, unsupported_claims=The answer choice's explanation is not grounded in the provided context., reason=The prediction correctly matches the gold answer but the retrieved context is irrelevant to the question, so it does not support the answer.

Retrieved context:

### ns_ht_gh4169_entropy_fatigue_001

For GH4169 low-cycle fatigue at elevated temperature, a thermodynamic entropy method can connect cyclic plasticity modeling with fatigue-life prediction. Entropy generation in the gauge section can serve as a damage-related quantity rather than using stress amplitude alone.

### ns_ht_transfer_learning_creep_design_001

Transfer learning can guide single-crystal superalloy composition design for ultrahigh-temperature creep resistance. A designed alloy can be validated under 1200 C and 80 MPa creep, where rupture life above 170 h indicates that data-driven screening can still require experimental confirmation.

### ns_ht_creep_rafting_al_mobility_001

During 850 C creep of a directionally solidified nickel-based superalloy, aluminum mobility can control gamma-prime rafting. Larger plastic strain flow promotes P-type rafting, while restricted deformation can leave the gamma-prime structure less rafted.

### ns_ht_oxidation_ce_coating_001

In additively manufactured IN625 exposed to 900 C air, intergranular oxidation can begin when scale buckling opens grain-boundary voids. A very thin cerium coating can improve chromia scale adherence and slow inward oxide growth.

### ns_ht_chi_lpt_strengthening_001

Stress-dependent local phase transformation can strengthen nickel-based superalloys by forming chi-phase nanolaths at planar defects. This mechanism can immobilize defect motion and create a self-strengthening response during deformation.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::lexical_rag::ns_ht_q050

- Priority: normal
- Reasons: none
- Method: lexical_rag
- Question type: fill_blank

Question:

In AM nickel superalloys, powder oxygen pickup, contamination, recycling history, and flowability are feedstock ____ factors.

Gold answers: ['quality']
Prediction: quality

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction correctly fills the blank with 'quality', matching the gold answer and supported by the context.

Retrieved context:

### ns_ht_am_review_feedstock_quality_001

Recent reviews of additively manufactured nickel superalloys emphasize that powder morphology, oxygen pickup, contamination, recycling history, and flowability influence defect formation before any heat treatment is applied.

### ns_ht_pm_hip_fatigue_review_001

Powder metallurgy hot-isostatic-pressed superalloys can show fatigue behavior controlled by powder quality, residual defects, grain structure, and heat treatment. Reviewing these factors helps separate processing-driven fatigue limits from intrinsic alloy strengthening effects.

### ns_ht_am_review_defect_taxonomy_001

Common AM nickel-superalloy defect classes include lack-of-fusion pores, gas pores, keyhole porosity, microcracks, residual stress, rough surfaces, and microsegregation. These defects influence fatigue, creep, oxidation, and hot-corrosion performance differently.

### ns_ht_sx_lcf_oxidation_competition_001

In high-temperature low-cycle fatigue of single-crystal nickel superalloys, surface oxidation and internal casting pores can compete as crack-initiation sites. Load ratio, hold time, and cycling frequency can shift the dominant damage mechanism.

### ns_ht_k452_so2_corrosion_001

For K452 nickel-based cast superalloy in high-temperature SO2-containing atmospheres, long exposure can promote sulfur-assisted corrosion. Damage involves oxide-scale evolution, sulfur penetration, and corrosion products that are less protective than a stable chromia-rich scale.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::lexical_rag::ns_ht_q051

- Priority: normal
- Reasons: none
- Method: lexical_rag
- Question type: short_answer

Question:

Compare steam oxidation of Rene 77 with chloride molten-salt corrosion of Inconel 625.

Gold answers: ['Rene 77 steam oxidation can become controlled by a more continuous oxide scale, while chloride molten salt can selectively dissolve chromium and molybdenum and form nonprotective corrosion products.']
Prediction: Rene 77 in steam oxidation can form a more continuous chromium-rich oxide scale that slows mass gain and may remain protective, depending on scale compactness and spallation. Inconel 625 in chloride molten salts experiences selective dissolution of chromium and molybdenum, producing nonprotective corrosion products, making the environment more aggressive than dry oxidation.

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction accurately compares Rene 77 steam oxidation and Inconel 625 chloride molten-salt corrosion, matching the gold answer and supported by context.

Retrieved context:

### ns_ht_in625_molten_salt_chloride_001

Inconel 625 exposed to chloride-containing molten salts can lose chromium and molybdenum from the near-surface region. Selective dissolution and nonprotective corrosion products can make chloride salts more aggressive than simple dry oxidation.

### ns_ht_hot_corrosion_alloying_001

In molten-salt hot corrosion of nickel-based superalloys, alloying elements can change oxide-scale stability, internal sulfidation, and diffusion of protective elements. Damage can combine surface oxidation, internal sulfidation, scale cracking, and spallation rather than a single degradation mode.

### ns_ht_hastelloyn_stress_flinak_001

In FLiNaK molten salt, applied stress can increase Hastelloy N corrosion rate compared with an unloaded condition. Stress-assisted corrosion is linked to accelerated grain-boundary attack and a higher weight-loss rate in the molten-salt environment.

### ns_ht_rene77_steam_oxidation_001

During long high-temperature steam oxidation of Rene 77, mass gain can slow after an initial transient as a more continuous oxide scale develops. Changes in scale compactness, local spallation, and chromium-rich oxide formation control whether the oxide remains protective.

### ns_ht_slm_in625_preoxidation_001

For SLM Inconel 625, heat treatment combined with pre-oxidation can form a more protective oxide barrier before hot-corrosion exposure. The preformed barrier can improve corrosion resistance by slowing aggressive species from penetrating the additively manufactured microstructure.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::lexical_rag::ns_ht_q052

- Priority: normal
- Reasons: none
- Method: lexical_rag
- Question type: multiple_choice

Question:

Which statements compare molten-salt and SO2 corrosion mechanisms in the medium corpus?
A. FLiNaK stress can accelerate grain-boundary attack in Hastelloy N
B. SO2 exposure can promote sulfur-assisted corrosion in K452
C. Chloride molten salt can deplete chromium and molybdenum in Inconel 625
D. All three mechanisms are independent of grain boundaries or selective chemistry
E. Chromium-rich protective scales can be destabilized or depleted

Gold answers: ['A', 'B', 'C', 'E']
Prediction: A,B,C,E

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction exactly matches the gold answer and all selected statements are supported by the retrieved context.

Retrieved context:

### ns_ht_hastelloyn_stress_flinak_001

In FLiNaK molten salt, applied stress can increase Hastelloy N corrosion rate compared with an unloaded condition. Stress-assisted corrosion is linked to accelerated grain-boundary attack and a higher weight-loss rate in the molten-salt environment.

### ns_ht_hastelloyn_igc_cr_diffusion_001

Hastelloy N in FLiNaK can suffer intergranular corrosion because selective chromium diffusion and depletion at grain boundaries make the boundaries preferred paths for corrosion invasion. Loaded samples can show ridge-like corrosion products around grain-boundary regions.

### ns_ht_k452_so2_corrosion_001

For K452 nickel-based cast superalloy in high-temperature SO2-containing atmospheres, long exposure can promote sulfur-assisted corrosion. Damage involves oxide-scale evolution, sulfur penetration, and corrosion products that are less protective than a stable chromia-rich scale.

### ns_ht_in625_molten_salt_chloride_001

Inconel 625 exposed to chloride-containing molten salts can lose chromium and molybdenum from the near-surface region. Selective dissolution and nonprotective corrosion products can make chloride salts more aggressive than simple dry oxidation.

### ns_ht_inconel740h_steam_oxidation_001

Inconel 740H and related nickel alloys in steam or fireside environments can depend on chromia continuity for corrosion resistance. Water vapor, chlorides, and sulfur species can destabilize the oxide scale and accelerate chromium depletion.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::lexical_rag::ns_ht_q053

- Priority: normal
- Reasons: none
- Method: lexical_rag
- Question type: single_choice

Question:

What makes DD5 over-temperature damage a creep risk even without obvious TCP phase formation?
A. Gamma-prime coarsening can weaken dislocation-network and Orowan resistance
B. The alloy becomes immune to dislocation motion
C. TCP absence always means rupture life is unchanged
D. Over-temperature exposure removes gamma/gamma-prime morphology

Gold answers: ['A']
Prediction: A

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction matches the gold answer and is fully supported by the retrieved context, which states that coarsened gamma-prime, weakened dislocation networks, and less effective Orowan bypass resistance reduce creep life.

Retrieved context:

### ns_ht_dd5_overtemp_gamma_prime_001

A second-generation DD5 single-crystal superalloy can retain phase stability after short over-temperature exposure, but gamma-prime coarsening and changes in the gamma/gamma-prime morphology reduce the density of obstacles to dislocation motion.

### ns_ht_dd5_creep_rupture_overtemp_001

After over-temperature exposure, DD5 creep rupture life at high temperature can decrease even when no obvious TCP phase forms. The reduction is associated with coarsened gamma-prime, weakened dislocation networks, and less effective Orowan bypass resistance.

### ns_ht_pf_ml_creep_features_001

Phase-field-informed machine learning can predict creep strain from simulated microstructure and composition descriptors. Useful descriptors include gamma-prime rafting degree, gamma-prime volume fraction, interparticle spacing, and elemental partitioning coefficients.

### ns_ht_creep_rafting_al_mobility_001

During 850 C creep of a directionally solidified nickel-based superalloy, aluminum mobility can control gamma-prime rafting. Larger plastic strain flow promotes P-type rafting, while restricted deformation can leave the gamma-prime structure less rafted.

### ns_ht_sx_rejuvenation_tcp_001

Rejuvenation or recovery heat treatments for single-crystal superalloys must balance gamma-prime restoration against risks such as TCP phase persistence, recrystallization, and residual creep damage. A treatment that improves precipitate morphology may not fully remove prior damage.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::lexical_rag::ns_ht_q054

- Priority: normal
- Reasons: none
- Method: lexical_rag
- Question type: fill_blank

Question:

Feature-importance analysis in PF-informed creep models can rank gamma-prime volume fraction and lattice ____.

Gold answers: ['misfit']
Prediction: misfit

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction 'misfit' matches the gold answer and is directly supported by the retrieved context mentioning lattice misfit as a ranked descriptor.

Retrieved context:

### ns_ht_pfml_shap_design_features_001

Feature-importance analysis in phase-field-informed creep models can rank descriptors such as aluminum partitioning, cobalt partitioning, lattice misfit, gamma-prime volume fraction, and rafting state. These descriptors connect composition and microstructure to predicted creep strain.

### ns_ht_pf_ml_creep_features_001

Phase-field-informed machine learning can predict creep strain from simulated microstructure and composition descriptors. Useful descriptors include gamma-prime rafting degree, gamma-prime volume fraction, interparticle spacing, and elemental partitioning coefficients.

### ns_ht_dd5_overtemp_gamma_prime_001

A second-generation DD5 single-crystal superalloy can retain phase stability after short over-temperature exposure, but gamma-prime coarsening and changes in the gamma/gamma-prime morphology reduce the density of obstacles to dislocation motion.

### ns_ht_gh4169_laves_delta_heat_001

In GH4169/Inconel 718, Laves phase formed during solidification can consume niobium and weaken the matrix. Homogenization and aging treatments can reduce segregation, promote delta or gamma-double-prime control, and change creep or fatigue behavior.

### ns_ht_rejuvenation_heat_treatment_001

Rejuvenation heat treatment can recover creep-degraded directionally solidified superalloys by modifying gamma-prime morphology. In one optimized regime, solution treatment near 1283 C and primary aging near 1095 C restored most standard heat-treatment creep life and increased total creep life.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::lexical_rag::ns_ht_q055

- Priority: high
- Reasons: correctness_below_5
- Method: lexical_rag
- Question type: short_answer

Question:

How do AM Hastelloy X fatigue modelling and AM defect taxonomy connect in the medium corpus?

Gold answers: ['Fatigue models link texture, grains, cyclic plasticity, and damage, while defect taxonomy identifies pores, cracks, residual stress, roughness, and segregation that influence fatigue initiation.']
Prediction: The AM defect taxonomy identifies defect classes such as pores, microcracks, and surface roughness that influence fatigue. AM Hastelloy X fatigue models incorporate microstructure heterogeneity, which includes defect populations, to predict fatigue life and damage initiation. Thus, the fatigue models leverage defect information from the taxonomy to connect AM microstructure to cyclic behavior.

Judge:

correctness=4.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction broadly captures the connection but misses explicit mention of cyclic plasticity and texture/grain details.

Retrieved context:

### ns_ht_am_hastelloyx_notch_orientation_001

AM Hastelloy X fatigue behavior can depend on build orientation, notch or surface condition, and local stress concentration. Orientation-sensitive microstructure and defect populations can change where cyclic damage initiates.

### ns_ht_am_hastelloyx_lcf_model_001

For additively manufactured Hastelloy X, microstructure-based low-cycle-fatigue models can combine measured texture or grain information with cyclic plasticity and damage parameters. Such models try to connect AM microstructure heterogeneity to fatigue-life prediction.

### ns_ht_am_review_defect_taxonomy_001

Common AM nickel-superalloy defect classes include lack-of-fusion pores, gas pores, keyhole porosity, microcracks, residual stress, rough surfaces, and microsegregation. These defects influence fatigue, creep, oxidation, and hot-corrosion performance differently.

### ns_ht_gh4169_entropy_fatigue_001

For GH4169 low-cycle fatigue at elevated temperature, a thermodynamic entropy method can connect cyclic plasticity modeling with fatigue-life prediction. Entropy generation in the gauge section can serve as a damage-related quantity rather than using stress amplitude alone.

### ns_ht_creep_orientation_850c_001

At 850 C, a directionally solidified nickel-based superalloy can show stronger creep resistance in the longitudinal orientation than in the transverse orientation. The longitudinal condition activates more slip systems and APB shearing, while the transverse condition is dominated by fewer slip bands and SISF-related deformation.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::lexical_rag::ns_ht_q056

- Priority: normal
- Reasons: none
- Method: lexical_rag
- Question type: multiple_choice

Question:

Which statements synthesize coating, steam, and film-cooling corrosion risks?
A. Coating-substrate interdiffusion can deplete protective elements
B. Inconel 740H-type alloys can depend on chromia continuity
C. Film-cooling holes can change local salt retention and scale growth
D. Water vapor, chlorides, and sulfur can destabilize protective scales
E. All hot-section features always improve scale adherence

Gold answers: ['A', 'B', 'C', 'D']
Prediction: A,B,C,D

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The model prediction exactly matches the gold answers and is fully supported by the retrieved context.

Retrieved context:

### ns_ht_inconel740h_steam_oxidation_001

Inconel 740H and related nickel alloys in steam or fireside environments can depend on chromia continuity for corrosion resistance. Water vapor, chlorides, and sulfur species can destabilize the oxide scale and accelerate chromium depletion.

### ns_ht_filmcooling_hot_corrosion_001

Film-cooling holes in nickel-based turbine alloys can alter molten-salt hot-corrosion behavior by changing local salt retention, gas access, oxide-scale growth, and stress concentration around the hole surface.

### ns_ht_mar_m247_coating_diffusion_001

Protective coatings on MAR-M247-type nickel superalloys rely on aluminum or chromium reservoirs to form adherent oxides. Interdiffusion between coating and substrate can deplete protective elements and change long-term oxidation resistance.

### ns_ht_oxidation_ce_coating_001

In additively manufactured IN625 exposed to 900 C air, intergranular oxidation can begin when scale buckling opens grain-boundary voids. A very thin cerium coating can improve chromia scale adherence and slow inward oxide growth.

### ns_ht_hot_corrosion_alloying_001

In molten-salt hot corrosion of nickel-based superalloys, alloying elements can change oxide-scale stability, internal sulfidation, and diffusion of protective elements. Damage can combine surface oxidation, internal sulfidation, scale cracking, and spallation rather than a single degradation mode.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::lexical_rag::ns_ht_q057

- Priority: normal
- Reasons: none
- Method: lexical_rag
- Question type: single_choice

Question:

In high-temperature fatigue, what distinguishes environmental LCF degradation from heat-treatment phase control?
A. Environmental LCF can involve hydrogen or oxidation-assisted crack initiation, while phase control changes precipitates or segregation
B. Both are only dataset split labels
C. Hydrogen and oxidation cannot affect crack initiation
D. Heat treatment never changes precipitates

Gold answers: ['A']
Prediction: A

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction matches the gold answer and is fully supported by the context, correctly distinguishing environmental degradation from heat-treatment effects.

Retrieved context:

### ns_ht_in718_hydrogen_lcf_001

Hydrogen-assisted low-cycle fatigue in Inconel 718 can reduce ductility and promote earlier crack initiation. Elevated temperature can interact with hydrogen transport, slip localization, and crack growth, making fatigue life sensitive to environment.

### ns_ht_gh4169_laves_delta_heat_001

In GH4169/Inconel 718, Laves phase formed during solidification can consume niobium and weaken the matrix. Homogenization and aging treatments can reduce segregation, promote delta or gamma-double-prime control, and change creep or fatigue behavior.

### ns_ht_sx_lcf_oxidation_competition_001

In high-temperature low-cycle fatigue of single-crystal nickel superalloys, surface oxidation and internal casting pores can compete as crack-initiation sites. Load ratio, hold time, and cycling frequency can shift the dominant damage mechanism.

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

## fresh_hard::lexical_rag::ns_ht_q058

- Priority: normal
- Reasons: none
- Method: lexical_rag
- Question type: fill_blank

Question:

A rejuvenation treatment can improve gamma-prime morphology but may not remove prior creep ____.

Gold answers: ['damage']
Prediction: damage

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction exactly matches the gold answer and is directly supported by the context.

Retrieved context:

### ns_ht_sx_rejuvenation_tcp_001

Rejuvenation or recovery heat treatments for single-crystal superalloys must balance gamma-prime restoration against risks such as TCP phase persistence, recrystallization, and residual creep damage. A treatment that improves precipitate morphology may not fully remove prior damage.

### ns_ht_rejuvenation_heat_treatment_001

Rejuvenation heat treatment can recover creep-degraded directionally solidified superalloys by modifying gamma-prime morphology. In one optimized regime, solution treatment near 1283 C and primary aging near 1095 C restored most standard heat-treatment creep life and increased total creep life.

### ns_ht_dd5_overtemp_gamma_prime_001

A second-generation DD5 single-crystal superalloy can retain phase stability after short over-temperature exposure, but gamma-prime coarsening and changes in the gamma/gamma-prime morphology reduce the density of obstacles to dislocation motion.

### ns_ht_cm247lc_lpbf_crack_mitigation_001

LPBF processing of crack-susceptible CM247LC-class superalloys requires control of thermal gradients, residual stress, and grain-boundary liquid films. Process optimization and heat treatment can reduce cracking but may not remove all solidification-related defects.

### ns_ht_creep_rafting_al_mobility_001

During 850 C creep of a directionally solidified nickel-based superalloy, aluminum mobility can control gamma-prime rafting. Larger plastic strain flow promotes P-type rafting, while restricted deformation can leave the gamma-prime structure less rafted.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::lexical_rag::ns_ht_q059

- Priority: normal
- Reasons: none
- Method: lexical_rag
- Question type: short_answer

Question:

Compare LPBF CM247LC crack mitigation with Nimonic 263 creep-fatigue dwell damage.

Gold answers: ['LPBF CM247LC mitigation controls thermal gradients, residual stress, and liquid-film cracking, while Nimonic 263 dwell damage involves time-dependent creep-fatigue mechanisms such as grain-boundary oxidation, cavities, and cyclic plastic strain.']
Prediction: LPBF CM247LC crack mitigation relies on controlling thermal gradients, residual stress, and grain-boundary liquid films, plus process optimization and heat treatment, though solidification defects may persist. Nimonic 263 creep-fatigue dwell damage involves grain-boundary oxidation, cavity formation, and cyclic plastic strain jointly controlling life under time-dependent damage at high temperature.

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction accurately captures both mitigation strategies and damage mechanisms, directly supported by the retrieved context, with no unsupported claims.

Retrieved context:

### ns_ht_nimonic263_creep_fatigue_interaction_001

Nimonic 263-type nickel superalloys can show creep-fatigue interaction at high temperature when dwell periods allow time-dependent damage. Grain-boundary oxidation, cavity formation, and cyclic plastic strain jointly control life.

### ns_ht_in718_hydrogen_lcf_001

Hydrogen-assisted low-cycle fatigue in Inconel 718 can reduce ductility and promote earlier crack initiation. Elevated temperature can interact with hydrogen transport, slip localization, and crack growth, making fatigue life sensitive to environment.

### ns_ht_cm247lc_lpbf_crack_mitigation_001

LPBF processing of crack-susceptible CM247LC-class superalloys requires control of thermal gradients, residual stress, and grain-boundary liquid films. Process optimization and heat treatment can reduce cracking but may not remove all solidification-related defects.

### ns_ht_am_hastelloyx_lcf_model_001

For additively manufactured Hastelloy X, microstructure-based low-cycle-fatigue models can combine measured texture or grain information with cyclic plasticity and damage parameters. Such models try to connect AM microstructure heterogeneity to fatigue-life prediction.

### ns_ht_gh4169_entropy_fatigue_001

For GH4169 low-cycle fatigue at elevated temperature, a thermodynamic entropy method can connect cyclic plasticity modeling with fatigue-life prediction. Entropy generation in the gauge section can serve as a damage-related quantity rather than using stress amplitude alone.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::lexical_rag::ns_ht_q060

- Priority: normal
- Reasons: none
- Method: lexical_rag
- Question type: multiple_choice

Question:

Which statements synthesize the medium corpus' fatigue and life-prediction evidence?
A. PF-informed models can rank composition and microstructure descriptors
B. Hydrogen-assisted LCF can reduce ductility and promote crack initiation
C. Single-crystal LCF can involve competition between oxidation and pores
D. AM Hastelloy X models connect microstructure heterogeneity to fatigue life
E. Life prediction never uses microstructure or environment

Gold answers: ['A', 'B', 'C', 'D']
Prediction: A,B,C,D

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The model prediction matches the gold answers exactly and each selected option is supported by the retrieved context.

Retrieved context:

### ns_ht_am_hastelloyx_lcf_model_001

For additively manufactured Hastelloy X, microstructure-based low-cycle-fatigue models can combine measured texture or grain information with cyclic plasticity and damage parameters. Such models try to connect AM microstructure heterogeneity to fatigue-life prediction.

### ns_ht_in718_hydrogen_lcf_001

Hydrogen-assisted low-cycle fatigue in Inconel 718 can reduce ductility and promote earlier crack initiation. Elevated temperature can interact with hydrogen transport, slip localization, and crack growth, making fatigue life sensitive to environment.

### ns_ht_pfml_shap_design_features_001

Feature-importance analysis in phase-field-informed creep models can rank descriptors such as aluminum partitioning, cobalt partitioning, lattice misfit, gamma-prime volume fraction, and rafting state. These descriptors connect composition and microstructure to predicted creep strain.

### ns_ht_am_hastelloyx_notch_orientation_001

AM Hastelloy X fatigue behavior can depend on build orientation, notch or surface condition, and local stress concentration. Orientation-sensitive microstructure and defect populations can change where cyclic damage initiates.

### ns_ht_sx_lcf_oxidation_competition_001

In high-temperature low-cycle fatigue of single-crystal nickel superalloys, surface oxidation and internal casting pores can compete as crack-initiation sites. Load ratio, hold time, and cycling frequency can shift the dominant damage mechanism.

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

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction correctly selects aluminum mobility, which is directly supported by the context and matches the gold answer.

Retrieved context:

### ns_ht_creep_rafting_al_mobility_001

During 850 C creep of a directionally solidified nickel-based superalloy, aluminum mobility can control gamma-prime rafting. Larger plastic strain flow promotes P-type rafting, while restricted deformation can leave the gamma-prime structure less rafted.

### ns_ht_pfml_shap_design_features_001

Feature-importance analysis in phase-field-informed creep models can rank descriptors such as aluminum partitioning, cobalt partitioning, lattice misfit, gamma-prime volume fraction, and rafting state. These descriptors connect composition and microstructure to predicted creep strain.

### ns_ht_pm_hip_fatigue_review_001

Powder metallurgy hot-isostatic-pressed superalloys can show fatigue behavior controlled by powder quality, residual defects, grain structure, and heat treatment. Reviewing these factors helps separate processing-driven fatigue limits from intrinsic alloy strengthening effects.

### ns_ht_gh4169_laves_delta_heat_001

In GH4169/Inconel 718, Laves phase formed during solidification can consume niobium and weaken the matrix. Homogenization and aging treatments can reduce segregation, promote delta or gamma-double-prime control, and change creep or fatigue behavior.

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

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction exactly matches the gold answer set and all selected statements are directly supported by the retrieved contexts.

Retrieved context:

### ns_ht_oxidation_lpbf_gh3536_001

For LPBF GH3536 oxidized at 950 C, the cellular microstructure can provide rapid diffusion paths that accelerate protective-film formation during early exposure. After long exposure, the LPBF material can show better oxidation resistance than a wrought counterpart.

### ns_ht_oxidation_ce_coating_001

In additively manufactured IN625 exposed to 900 C air, intergranular oxidation can begin when scale buckling opens grain-boundary voids. A very thin cerium coating can improve chromia scale adherence and slow inward oxide growth.

### ns_ht_cm247lc_lpbf_crack_mitigation_001

LPBF processing of crack-susceptible CM247LC-class superalloys requires control of thermal gradients, residual stress, and grain-boundary liquid films. Process optimization and heat treatment can reduce cracking but may not remove all solidification-related defects.

### ns_ht_filmcooling_hot_corrosion_001

Film-cooling holes in nickel-based turbine alloys can alter molten-salt hot-corrosion behavior by changing local salt retention, gas access, oxide-scale growth, and stress concentration around the hole surface.

### ns_ht_k452_so2_corrosion_001

For K452 nickel-based cast superalloy in high-temperature SO2-containing atmospheres, long exposure can promote sulfur-assisted corrosion. Damage involves oxide-scale evolution, sulfur penetration, and corrosion products that are less protective than a stable chromia-rich scale.

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

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction exactly matches the gold answer and is fully supported by the retrieved context.

Retrieved context:

### ns_ht_oxidation_ce_coating_001

In additively manufactured IN625 exposed to 900 C air, intergranular oxidation can begin when scale buckling opens grain-boundary voids. A very thin cerium coating can improve chromia scale adherence and slow inward oxide growth.

### ns_ht_am_hastelloyx_lcf_model_001

For additively manufactured Hastelloy X, microstructure-based low-cycle-fatigue models can combine measured texture or grain information with cyclic plasticity and damage parameters. Such models try to connect AM microstructure heterogeneity to fatigue-life prediction.

### ns_ht_am_hastelloyx_notch_orientation_001

AM Hastelloy X fatigue behavior can depend on build orientation, notch or surface condition, and local stress concentration. Orientation-sensitive microstructure and defect populations can change where cyclic damage initiates.

### ns_ht_am_review_defect_taxonomy_001

Common AM nickel-superalloy defect classes include lack-of-fusion pores, gas pores, keyhole porosity, microcracks, residual stress, rough surfaces, and microsegregation. These defects influence fatigue, creep, oxidation, and hot-corrosion performance differently.

### ns_ht_hot_corrosion_alloying_001

In molten-salt hot corrosion of nickel-based superalloys, alloying elements can change oxide-scale stability, internal sulfidation, and diffusion of protective elements. Damage can combine surface oxidation, internal sulfidation, scale cracking, and spallation rather than a single degradation mode.

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

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The model prediction exactly matches the gold answer and is fully supported by the retrieved context.

Retrieved context:

### ns_ht_creep_rafting_al_mobility_001

During 850 C creep of a directionally solidified nickel-based superalloy, aluminum mobility can control gamma-prime rafting. Larger plastic strain flow promotes P-type rafting, while restricted deformation can leave the gamma-prime structure less rafted.

### ns_ht_nimonic263_creep_fatigue_interaction_001

Nimonic 263-type nickel superalloys can show creep-fatigue interaction at high temperature when dwell periods allow time-dependent damage. Grain-boundary oxidation, cavity formation, and cyclic plastic strain jointly control life.

### ns_ht_creep_orientation_850c_001

At 850 C, a directionally solidified nickel-based superalloy can show stronger creep resistance in the longitudinal orientation than in the transverse orientation. The longitudinal condition activates more slip systems and APB shearing, while the transverse condition is dominated by fewer slip bands and SISF-related deformation.

### ns_ht_pfml_creep_stress_response_001

Phase-field-informed machine learning for nickel superalloy creep can use simulated microstructures at different stresses and temperatures. Higher applied stress typically increases creep strain, shortens the primary-creep regime, and changes rafting descriptors.

### ns_ht_pfml_shap_design_features_001

Feature-importance analysis in phase-field-informed creep models can rank descriptors such as aluminum partitioning, cobalt partitioning, lattice misfit, gamma-prime volume fraction, and rafting state. These descriptors connect composition and microstructure to predicted creep strain.

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

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction matches the gold answer and is directly supported by the context.

Retrieved context:

### ns_ht_transfer_learning_creep_design_001

Transfer learning can guide single-crystal superalloy composition design for ultrahigh-temperature creep resistance. A designed alloy can be validated under 1200 C and 80 MPa creep, where rupture life above 170 h indicates that data-driven screening can still require experimental confirmation.

### ns_ht_rejuvenation_heat_treatment_001

Rejuvenation heat treatment can recover creep-degraded directionally solidified superalloys by modifying gamma-prime morphology. In one optimized regime, solution treatment near 1283 C and primary aging near 1095 C restored most standard heat-treatment creep life and increased total creep life.

### ns_ht_sx_rejuvenation_tcp_001

Rejuvenation or recovery heat treatments for single-crystal superalloys must balance gamma-prime restoration against risks such as TCP phase persistence, recrystallization, and residual creep damage. A treatment that improves precipitate morphology may not fully remove prior damage.

### ns_ht_nimonic263_creep_fatigue_interaction_001

Nimonic 263-type nickel superalloys can show creep-fatigue interaction at high temperature when dwell periods allow time-dependent damage. Grain-boundary oxidation, cavity formation, and cyclic plastic strain jointly control life.

### ns_ht_dd5_overtemp_gamma_prime_001

A second-generation DD5 single-crystal superalloy can retain phase stability after short over-temperature exposure, but gamma-prime coarsening and changes in the gamma/gamma-prime morphology reduce the density of obstacles to dislocation motion.

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

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction 'machined' exactly matches the gold answer and is directly supported by the retrieved context.

Retrieved context:

### ns_ht_drilled_sx_hot_corrosion_001

A drilled nickel-based single-crystal superalloy can show abnormal hot-corrosion behavior because the hole surface changes diffusion paths and oxide-layer development. Local drilling can therefore alter scale adhesion and corrosion-product evolution around the machined region.

### ns_ht_filmcooling_hot_corrosion_001

Film-cooling holes in nickel-based turbine alloys can alter molten-salt hot-corrosion behavior by changing local salt retention, gas access, oxide-scale growth, and stress concentration around the hole surface.

### ns_ht_hastelloyn_igc_cr_diffusion_001

Hastelloy N in FLiNaK can suffer intergranular corrosion because selective chromium diffusion and depletion at grain boundaries make the boundaries preferred paths for corrosion invasion. Loaded samples can show ridge-like corrosion products around grain-boundary regions.

### ns_ht_k452_so2_corrosion_001

For K452 nickel-based cast superalloy in high-temperature SO2-containing atmospheres, long exposure can promote sulfur-assisted corrosion. Damage involves oxide-scale evolution, sulfur penetration, and corrosion products that are less protective than a stable chromia-rich scale.

### ns_ht_in625_molten_salt_chloride_001

Inconel 625 exposed to chloride-containing molten salts can lose chromium and molybdenum from the near-surface region. Selective dissolution and nonprotective corrosion products can make chloride salts more aggressive than simple dry oxidation.

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

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction matches the gold answer exactly, all selected statements are directly supported by context snippets, and no unsupported claims are made.

Retrieved context:

### ns_ht_slm_in625_preoxidation_001

For SLM Inconel 625, heat treatment combined with pre-oxidation can form a more protective oxide barrier before hot-corrosion exposure. The preformed barrier can improve corrosion resistance by slowing aggressive species from penetrating the additively manufactured microstructure.

### ns_ht_filmcooling_hot_corrosion_001

Film-cooling holes in nickel-based turbine alloys can alter molten-salt hot-corrosion behavior by changing local salt retention, gas access, oxide-scale growth, and stress concentration around the hole surface.

### ns_ht_tic_in625_oxidation_001

TiC-containing Inconel 625 can change microstructural features that affect high-temperature oxidation behavior. Ceramic-particle additions may influence oxide-scale continuity, local element distribution, and oxidation resistance rather than acting only as inert reinforcement.

### ns_ht_hot_corrosion_alloying_001

In molten-salt hot corrosion of nickel-based superalloys, alloying elements can change oxide-scale stability, internal sulfidation, and diffusion of protective elements. Damage can combine surface oxidation, internal sulfidation, scale cracking, and spallation rather than a single degradation mode.

### ns_ht_in625_molten_salt_chloride_001

Inconel 625 exposed to chloride-containing molten salts can lose chromium and molybdenum from the near-surface region. Selective dissolution and nonprotective corrosion products can make chloride salts more aggressive than simple dry oxidation.

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

correctness=5.0, context_support=0.0, faithfulness=0.0, unsupported_claims=The entropy method treats entropy generation from cyclic plasticity as a damage-related predictor., reason=Prediction matches gold answer exactly, but the entropy-based claim is unsupported by the retrieved context.

Retrieved context:

### ns_ht_am_review_feedstock_quality_001

Recent reviews of additively manufactured nickel superalloys emphasize that powder morphology, oxygen pickup, contamination, recycling history, and flowability influence defect formation before any heat treatment is applied.

### ns_ht_pm_hip_fatigue_review_001

Powder metallurgy hot-isostatic-pressed superalloys can show fatigue behavior controlled by powder quality, residual defects, grain structure, and heat treatment. Reviewing these factors helps separate processing-driven fatigue limits from intrinsic alloy strengthening effects.

### ns_ht_am_review_defect_taxonomy_001

Common AM nickel-superalloy defect classes include lack-of-fusion pores, gas pores, keyhole porosity, microcracks, residual stress, rough surfaces, and microsegregation. These defects influence fatigue, creep, oxidation, and hot-corrosion performance differently.

### ns_ht_pfml_creep_stress_response_001

Phase-field-informed machine learning for nickel superalloy creep can use simulated microstructures at different stresses and temperatures. Higher applied stress typically increases creep strain, shortens the primary-creep regime, and changes rafting descriptors.

### ns_ht_oxidation_gb_energy_001

Initial oxidation in Inconel 718 can depend on grain-boundary character. Boundaries with different energy states can change oxygen adsorption, diffusion, and oxide nucleation, so intergranular oxidation does not begin uniformly across all boundaries.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_oracle_reader::ns_ht_q049

- Priority: high
- Reasons: correctness_below_5, context_support_below_5
- Method: flashrag_bm25_oracle_reader
- Question type: single_choice

Question:

Which mechanism explains why a correct gold answer can still be poorly supported if BM25 retrieves only part of a multi-source question?
A. A method may hit one relevant chunk while missing another required evidence chunk
B. A hit on any chunk always proves full evidence recall
C. Retrieval recall is unrelated to source_chunk_ids
D. Oracle context removes all need for qrels

Gold answers: ['A']
Prediction:

Judge:

correctness=0.0, context_support=0.0, faithfulness=5.0, unsupported_claims=none, reason=The model prediction is empty, so it fails to match the correct answer A, and has zero relevance, but it does not contain any unsupported claims.

Retrieved context:

### ns_ht_cm247lc_lpbf_crack_mitigation_001

LPBF processing of crack-susceptible CM247LC-class superalloys requires control of thermal gradients, residual stress, and grain-boundary liquid films. Process optimization and heat treatment can reduce cracking but may not remove all solidification-related defects.

### ns_ht_gh4169_entropy_fatigue_001

For GH4169 low-cycle fatigue at elevated temperature, a thermodynamic entropy method can connect cyclic plasticity modeling with fatigue-life prediction. Entropy generation in the gauge section can serve as a damage-related quantity rather than using stress amplitude alone.

### ns_ht_transfer_learning_creep_design_001

Transfer learning can guide single-crystal superalloy composition design for ultrahigh-temperature creep resistance. A designed alloy can be validated under 1200 C and 80 MPa creep, where rupture life above 170 h indicates that data-driven screening can still require experimental confirmation.

### ns_ht_rejuvenation_heat_treatment_001

Rejuvenation heat treatment can recover creep-degraded directionally solidified superalloys by modifying gamma-prime morphology. In one optimized regime, solution treatment near 1283 C and primary aging near 1095 C restored most standard heat-treatment creep life and increased total creep life.

### ns_ht_oxidation_gb_energy_001

Initial oxidation in Inconel 718 can depend on grain-boundary character. Boundaries with different energy states can change oxygen adsorption, diffusion, and oxide nucleation, so intergranular oxidation does not begin uniformly across all boundaries.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_oracle_reader::ns_ht_q050

- Priority: normal
- Reasons: none
- Method: flashrag_bm25_oracle_reader
- Question type: fill_blank

Question:

In AM nickel superalloys, powder oxygen pickup, contamination, recycling history, and flowability are feedstock ____ factors.

Gold answers: ['quality']
Prediction: quality

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction accurately fills in the blank with 'quality', which matches the gold answer and is supported by the context linking these factors to defect formation.

Retrieved context:

### ns_ht_am_review_feedstock_quality_001

Recent reviews of additively manufactured nickel superalloys emphasize that powder morphology, oxygen pickup, contamination, recycling history, and flowability influence defect formation before any heat treatment is applied.

### ns_ht_pm_hip_fatigue_review_001

Powder metallurgy hot-isostatic-pressed superalloys can show fatigue behavior controlled by powder quality, residual defects, grain structure, and heat treatment. Reviewing these factors helps separate processing-driven fatigue limits from intrinsic alloy strengthening effects.

### ns_ht_am_review_defect_taxonomy_001

Common AM nickel-superalloy defect classes include lack-of-fusion pores, gas pores, keyhole porosity, microcracks, residual stress, rough surfaces, and microsegregation. These defects influence fatigue, creep, oxidation, and hot-corrosion performance differently.

### ns_ht_oxidation_gb_energy_001

Initial oxidation in Inconel 718 can depend on grain-boundary character. Boundaries with different energy states can change oxygen adsorption, diffusion, and oxide nucleation, so intergranular oxidation does not begin uniformly across all boundaries.

### ns_ht_am_hastelloyx_notch_orientation_001

AM Hastelloy X fatigue behavior can depend on build orientation, notch or surface condition, and local stress concentration. Orientation-sensitive microstructure and defect populations can change where cyclic damage initiates.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_oracle_reader::ns_ht_q051

- Priority: normal
- Reasons: none
- Method: flashrag_bm25_oracle_reader
- Question type: short_answer

Question:

Compare steam oxidation of Rene 77 with chloride molten-salt corrosion of Inconel 625.

Gold answers: ['Rene 77 steam oxidation can become controlled by a more continuous oxide scale, while chloride molten salt can selectively dissolve chromium and molybdenum and form nonprotective corrosion products.']
Prediction: Rene 77 steam oxidation can become controlled by a more continuous oxide scale, while chloride molten salt can selectively dissolve chromium and molybdenum and form nonprotective corrosion products.

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction exactly matches the gold answer and is fully supported by the provided context.

Retrieved context:

### ns_ht_in625_molten_salt_chloride_001

Inconel 625 exposed to chloride-containing molten salts can lose chromium and molybdenum from the near-surface region. Selective dissolution and nonprotective corrosion products can make chloride salts more aggressive than simple dry oxidation.

### ns_ht_rene77_steam_oxidation_001

During long high-temperature steam oxidation of Rene 77, mass gain can slow after an initial transient as a more continuous oxide scale develops. Changes in scale compactness, local spallation, and chromium-rich oxide formation control whether the oxide remains protective.

### ns_ht_hastelloyn_stress_flinak_001

In FLiNaK molten salt, applied stress can increase Hastelloy N corrosion rate compared with an unloaded condition. Stress-assisted corrosion is linked to accelerated grain-boundary attack and a higher weight-loss rate in the molten-salt environment.

### ns_ht_rene77_microsegregation_heat_001

In cast Rene 77, solidification can leave a gamma dendrite matrix with MC carbides and microsegregated interdendritic regions. Heat treatment can dissolve or redistribute nonequilibrium constituents while gamma-prime precipitation strengthens the aged microstructure.

### ns_ht_filmcooling_hot_corrosion_001

Film-cooling holes in nickel-based turbine alloys can alter molten-salt hot-corrosion behavior by changing local salt retention, gas access, oxide-scale growth, and stress concentration around the hole surface.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_oracle_reader::ns_ht_q052

- Priority: normal
- Reasons: none
- Method: flashrag_bm25_oracle_reader
- Question type: multiple_choice

Question:

Which statements compare molten-salt and SO2 corrosion mechanisms in the medium corpus?
A. FLiNaK stress can accelerate grain-boundary attack in Hastelloy N
B. SO2 exposure can promote sulfur-assisted corrosion in K452
C. Chloride molten salt can deplete chromium and molybdenum in Inconel 625
D. All three mechanisms are independent of grain boundaries or selective chemistry
E. Chromium-rich protective scales can be destabilized or depleted

Gold answers: ['A', 'B', 'C', 'E']
Prediction: A,B,C,E

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The model prediction exactly matches the gold answers and all selected statements are supported by the retrieved context.

Retrieved context:

### ns_ht_hastelloyn_stress_flinak_001

In FLiNaK molten salt, applied stress can increase Hastelloy N corrosion rate compared with an unloaded condition. Stress-assisted corrosion is linked to accelerated grain-boundary attack and a higher weight-loss rate in the molten-salt environment.

### ns_ht_in625_molten_salt_chloride_001

Inconel 625 exposed to chloride-containing molten salts can lose chromium and molybdenum from the near-surface region. Selective dissolution and nonprotective corrosion products can make chloride salts more aggressive than simple dry oxidation.

### ns_ht_k452_so2_corrosion_001

For K452 nickel-based cast superalloy in high-temperature SO2-containing atmospheres, long exposure can promote sulfur-assisted corrosion. Damage involves oxide-scale evolution, sulfur penetration, and corrosion products that are less protective than a stable chromia-rich scale.

### ns_ht_hastelloyn_igc_cr_diffusion_001

Hastelloy N in FLiNaK can suffer intergranular corrosion because selective chromium diffusion and depletion at grain boundaries make the boundaries preferred paths for corrosion invasion. Loaded samples can show ridge-like corrosion products around grain-boundary regions.

### ns_ht_filmcooling_hot_corrosion_001

Film-cooling holes in nickel-based turbine alloys can alter molten-salt hot-corrosion behavior by changing local salt retention, gas access, oxide-scale growth, and stress concentration around the hole surface.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_oracle_reader::ns_ht_q053

- Priority: normal
- Reasons: none
- Method: flashrag_bm25_oracle_reader
- Question type: single_choice

Question:

What makes DD5 over-temperature damage a creep risk even without obvious TCP phase formation?
A. Gamma-prime coarsening can weaken dislocation-network and Orowan resistance
B. The alloy becomes immune to dislocation motion
C. TCP absence always means rupture life is unchanged
D. Over-temperature exposure removes gamma/gamma-prime morphology

Gold answers: ['A']
Prediction: A

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The model correctly identifies option A, which is directly supported by the retrieved context explaining that gamma-prime coarsening weakens dislocation networks and Orowan resistance.

Retrieved context:

### ns_ht_dd5_creep_rupture_overtemp_001

After over-temperature exposure, DD5 creep rupture life at high temperature can decrease even when no obvious TCP phase forms. The reduction is associated with coarsened gamma-prime, weakened dislocation networks, and less effective Orowan bypass resistance.

### ns_ht_dd5_overtemp_gamma_prime_001

A second-generation DD5 single-crystal superalloy can retain phase stability after short over-temperature exposure, but gamma-prime coarsening and changes in the gamma/gamma-prime morphology reduce the density of obstacles to dislocation motion.

### ns_ht_sx_rejuvenation_tcp_001

Rejuvenation or recovery heat treatments for single-crystal superalloys must balance gamma-prime restoration against risks such as TCP phase persistence, recrystallization, and residual creep damage. A treatment that improves precipitate morphology may not fully remove prior damage.

### ns_ht_gh4169_laves_delta_heat_001

In GH4169/Inconel 718, Laves phase formed during solidification can consume niobium and weaken the matrix. Homogenization and aging treatments can reduce segregation, promote delta or gamma-double-prime control, and change creep or fatigue behavior.

### ns_ht_pf_ml_creep_features_001

Phase-field-informed machine learning can predict creep strain from simulated microstructure and composition descriptors. Useful descriptors include gamma-prime rafting degree, gamma-prime volume fraction, interparticle spacing, and elemental partitioning coefficients.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_oracle_reader::ns_ht_q054

- Priority: normal
- Reasons: none
- Method: flashrag_bm25_oracle_reader
- Question type: fill_blank

Question:

Feature-importance analysis in PF-informed creep models can rank gamma-prime volume fraction and lattice ____.

Gold answers: ['misfit']
Prediction: misfit

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction 'misfit' exactly matches the gold answer and is directly supported by the context mentioning lattice misfit.

Retrieved context:

### ns_ht_pfml_shap_design_features_001

Feature-importance analysis in phase-field-informed creep models can rank descriptors such as aluminum partitioning, cobalt partitioning, lattice misfit, gamma-prime volume fraction, and rafting state. These descriptors connect composition and microstructure to predicted creep strain.

### ns_ht_pf_ml_creep_features_001

Phase-field-informed machine learning can predict creep strain from simulated microstructure and composition descriptors. Useful descriptors include gamma-prime rafting degree, gamma-prime volume fraction, interparticle spacing, and elemental partitioning coefficients.

### ns_ht_creep_rafting_al_mobility_001

During 850 C creep of a directionally solidified nickel-based superalloy, aluminum mobility can control gamma-prime rafting. Larger plastic strain flow promotes P-type rafting, while restricted deformation can leave the gamma-prime structure less rafted.

### ns_ht_dd5_overtemp_gamma_prime_001

A second-generation DD5 single-crystal superalloy can retain phase stability after short over-temperature exposure, but gamma-prime coarsening and changes in the gamma/gamma-prime morphology reduce the density of obstacles to dislocation motion.

### ns_ht_rejuvenation_heat_treatment_001

Rejuvenation heat treatment can recover creep-degraded directionally solidified superalloys by modifying gamma-prime morphology. In one optimized regime, solution treatment near 1283 C and primary aging near 1095 C restored most standard heat-treatment creep life and increased total creep life.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_oracle_reader::ns_ht_q055

- Priority: normal
- Reasons: none
- Method: flashrag_bm25_oracle_reader
- Question type: short_answer

Question:

How do AM Hastelloy X fatigue modelling and AM defect taxonomy connect in the medium corpus?

Gold answers: ['Fatigue models link texture, grains, cyclic plasticity, and damage, while defect taxonomy identifies pores, cracks, residual stress, roughness, and segregation that influence fatigue initiation.']
Prediction: Fatigue models link texture, grains, cyclic plasticity, and damage, while defect taxonomy identifies pores, cracks, residual stress, roughness, and segregation that influence fatigue initiation.

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction matches the gold answer exactly and all claims are supported by the retrieved context.

Retrieved context:

### ns_ht_am_hastelloyx_lcf_model_001

For additively manufactured Hastelloy X, microstructure-based low-cycle-fatigue models can combine measured texture or grain information with cyclic plasticity and damage parameters. Such models try to connect AM microstructure heterogeneity to fatigue-life prediction.

### ns_ht_am_hastelloyx_notch_orientation_001

AM Hastelloy X fatigue behavior can depend on build orientation, notch or surface condition, and local stress concentration. Orientation-sensitive microstructure and defect populations can change where cyclic damage initiates.

### ns_ht_am_review_defect_taxonomy_001

Common AM nickel-superalloy defect classes include lack-of-fusion pores, gas pores, keyhole porosity, microcracks, residual stress, rough surfaces, and microsegregation. These defects influence fatigue, creep, oxidation, and hot-corrosion performance differently.

### ns_ht_chi_lpt_strengthening_001

Stress-dependent local phase transformation can strengthen nickel-based superalloys by forming chi-phase nanolaths at planar defects. This mechanism can immobilize defect motion and create a self-strengthening response during deformation.

### ns_ht_pfml_shap_design_features_001

Feature-importance analysis in phase-field-informed creep models can rank descriptors such as aluminum partitioning, cobalt partitioning, lattice misfit, gamma-prime volume fraction, and rafting state. These descriptors connect composition and microstructure to predicted creep strain.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_oracle_reader::ns_ht_q056

- Priority: high
- Reasons: unsupported_claims, context_support_below_5, faithfulness_below_5, hallucination_risk_above_0
- Method: flashrag_bm25_oracle_reader
- Question type: multiple_choice

Question:

Which statements synthesize coating, steam, and film-cooling corrosion risks?
A. Coating-substrate interdiffusion can deplete protective elements
B. Inconel 740H-type alloys can depend on chromia continuity
C. Film-cooling holes can change local salt retention and scale growth
D. Water vapor, chlorides, and sulfur can destabilize protective scales
E. All hot-section features always improve scale adherence

Gold answers: ['A', 'B', 'C', 'D']
Prediction: A,B,C,D

Judge:

correctness=5.0, context_support=4.0, faithfulness=4.0, unsupported_claims=Coating-substrate interdiffusion can deplete protective elements, reason=Prediction matches gold answers; however, option A about coating-substrate interdiffusion lacks contextual evidence.

Retrieved context:

### ns_ht_inconel740h_steam_oxidation_001

Inconel 740H and related nickel alloys in steam or fireside environments can depend on chromia continuity for corrosion resistance. Water vapor, chlorides, and sulfur species can destabilize the oxide scale and accelerate chromium depletion.

### ns_ht_filmcooling_hot_corrosion_001

Film-cooling holes in nickel-based turbine alloys can alter molten-salt hot-corrosion behavior by changing local salt retention, gas access, oxide-scale growth, and stress concentration around the hole surface.

### ns_ht_k452_so2_corrosion_001

For K452 nickel-based cast superalloy in high-temperature SO2-containing atmospheres, long exposure can promote sulfur-assisted corrosion. Damage involves oxide-scale evolution, sulfur penetration, and corrosion products that are less protective than a stable chromia-rich scale.

### ns_ht_oxidation_ce_coating_001

In additively manufactured IN625 exposed to 900 C air, intergranular oxidation can begin when scale buckling opens grain-boundary voids. A very thin cerium coating can improve chromia scale adherence and slow inward oxide growth.

### ns_ht_rene77_steam_oxidation_001

During long high-temperature steam oxidation of Rene 77, mass gain can slow after an initial transient as a more continuous oxide scale develops. Changes in scale compactness, local spallation, and chromium-rich oxide formation control whether the oxide remains protective.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_oracle_reader::ns_ht_q057

- Priority: normal
- Reasons: none
- Method: flashrag_bm25_oracle_reader
- Question type: single_choice

Question:

In high-temperature fatigue, what distinguishes environmental LCF degradation from heat-treatment phase control?
A. Environmental LCF can involve hydrogen or oxidation-assisted crack initiation, while phase control changes precipitates or segregation
B. Both are only dataset split labels
C. Hydrogen and oxidation cannot affect crack initiation
D. Heat treatment never changes precipitates

Gold answers: ['A']
Prediction: A

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction matches the gold answer A and correctly distinguishes environmental LCF degradation (hydrogen/oxidation-assisted crack initiation) from heat-treatment phase control (precipitate/segregation changes), with retrieved context supporting both aspects.

Retrieved context:

### ns_ht_cm247lc_lpbf_crack_mitigation_001

LPBF processing of crack-susceptible CM247LC-class superalloys requires control of thermal gradients, residual stress, and grain-boundary liquid films. Process optimization and heat treatment can reduce cracking but may not remove all solidification-related defects.

### ns_ht_in718_hydrogen_lcf_001

Hydrogen-assisted low-cycle fatigue in Inconel 718 can reduce ductility and promote earlier crack initiation. Elevated temperature can interact with hydrogen transport, slip localization, and crack growth, making fatigue life sensitive to environment.

### ns_ht_pm_hip_fatigue_review_001

Powder metallurgy hot-isostatic-pressed superalloys can show fatigue behavior controlled by powder quality, residual defects, grain structure, and heat treatment. Reviewing these factors helps separate processing-driven fatigue limits from intrinsic alloy strengthening effects.

### ns_ht_sx_rejuvenation_tcp_001

Rejuvenation or recovery heat treatments for single-crystal superalloys must balance gamma-prime restoration against risks such as TCP phase persistence, recrystallization, and residual creep damage. A treatment that improves precipitate morphology may not fully remove prior damage.

### ns_ht_gh4169_laves_delta_heat_001

In GH4169/Inconel 718, Laves phase formed during solidification can consume niobium and weaken the matrix. Homogenization and aging treatments can reduce segregation, promote delta or gamma-double-prime control, and change creep or fatigue behavior.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_oracle_reader::ns_ht_q058

- Priority: normal
- Reasons: none
- Method: flashrag_bm25_oracle_reader
- Question type: fill_blank

Question:

A rejuvenation treatment can improve gamma-prime morphology but may not remove prior creep ____.

Gold answers: ['damage']
Prediction: damage

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The model prediction 'damage' exactly matches the gold answer and is supported by the context mentioning residual creep damage.

Retrieved context:

### ns_ht_sx_rejuvenation_tcp_001

Rejuvenation or recovery heat treatments for single-crystal superalloys must balance gamma-prime restoration against risks such as TCP phase persistence, recrystallization, and residual creep damage. A treatment that improves precipitate morphology may not fully remove prior damage.

### ns_ht_rejuvenation_heat_treatment_001

Rejuvenation heat treatment can recover creep-degraded directionally solidified superalloys by modifying gamma-prime morphology. In one optimized regime, solution treatment near 1283 C and primary aging near 1095 C restored most standard heat-treatment creep life and increased total creep life.

### ns_ht_gh4169_laves_delta_heat_001

In GH4169/Inconel 718, Laves phase formed during solidification can consume niobium and weaken the matrix. Homogenization and aging treatments can reduce segregation, promote delta or gamma-double-prime control, and change creep or fatigue behavior.

### ns_ht_rene77_microsegregation_heat_001

In cast Rene 77, solidification can leave a gamma dendrite matrix with MC carbides and microsegregated interdendritic regions. Heat treatment can dissolve or redistribute nonequilibrium constituents while gamma-prime precipitation strengthens the aged microstructure.

### ns_ht_pf_ml_creep_features_001

Phase-field-informed machine learning can predict creep strain from simulated microstructure and composition descriptors. Useful descriptors include gamma-prime rafting degree, gamma-prime volume fraction, interparticle spacing, and elemental partitioning coefficients.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_oracle_reader::ns_ht_q059

- Priority: normal
- Reasons: none
- Method: flashrag_bm25_oracle_reader
- Question type: short_answer

Question:

Compare LPBF CM247LC crack mitigation with Nimonic 263 creep-fatigue dwell damage.

Gold answers: ['LPBF CM247LC mitigation controls thermal gradients, residual stress, and liquid-film cracking, while Nimonic 263 dwell damage involves time-dependent creep-fatigue mechanisms such as grain-boundary oxidation, cavities, and cyclic plastic strain.']
Prediction: LPBF CM247LC mitigation controls thermal gradients, residual stress, and liquid-film cracking, while Nimonic 263 dwell damage involves time-dependent creep-fatigue mechanisms such as grain-boundary oxidation, cavities, and cyclic plastic strain.

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=Identical to gold answer and fully supported by the provided contexts.

Retrieved context:

### ns_ht_cm247lc_lpbf_crack_mitigation_001

LPBF processing of crack-susceptible CM247LC-class superalloys requires control of thermal gradients, residual stress, and grain-boundary liquid films. Process optimization and heat treatment can reduce cracking but may not remove all solidification-related defects.

### ns_ht_nimonic263_creep_fatigue_interaction_001

Nimonic 263-type nickel superalloys can show creep-fatigue interaction at high temperature when dwell periods allow time-dependent damage. Grain-boundary oxidation, cavity formation, and cyclic plastic strain jointly control life.

### ns_ht_oxidation_lpbf_gh3536_001

For LPBF GH3536 oxidized at 950 C, the cellular microstructure can provide rapid diffusion paths that accelerate protective-film formation during early exposure. After long exposure, the LPBF material can show better oxidation resistance than a wrought counterpart.

### ns_ht_in718_hydrogen_lcf_001

Hydrogen-assisted low-cycle fatigue in Inconel 718 can reduce ductility and promote earlier crack initiation. Elevated temperature can interact with hydrogen transport, slip localization, and crack growth, making fatigue life sensitive to environment.

### ns_ht_sx_lcf_oxidation_competition_001

In high-temperature low-cycle fatigue of single-crystal nickel superalloys, surface oxidation and internal casting pores can compete as crack-initiation sites. Load ratio, hold time, and cycling frequency can shift the dominant damage mechanism.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_oracle_reader::ns_ht_q060

- Priority: high
- Reasons: unsupported_claims, context_support_below_5, faithfulness_below_5, hallucination_risk_above_0
- Method: flashrag_bm25_oracle_reader
- Question type: multiple_choice

Question:

Which statements synthesize the medium corpus' fatigue and life-prediction evidence?
A. PF-informed models can rank composition and microstructure descriptors
B. Hydrogen-assisted LCF can reduce ductility and promote crack initiation
C. Single-crystal LCF can involve competition between oxidation and pores
D. AM Hastelloy X models connect microstructure heterogeneity to fatigue life
E. Life prediction never uses microstructure or environment

Gold answers: ['A', 'B', 'C', 'D']
Prediction: A,B,C,D

Judge:

correctness=5.0, context_support=0.0, faithfulness=0.0, unsupported_claims=PF-informed models can rank composition and microstructure descriptors; Single-crystal LCF can involve competition between oxidation and pores, reason=Prediction matches gold answer, but selected options A and C lack corpus support.

Retrieved context:

### ns_ht_in718_hydrogen_lcf_001

Hydrogen-assisted low-cycle fatigue in Inconel 718 can reduce ductility and promote earlier crack initiation. Elevated temperature can interact with hydrogen transport, slip localization, and crack growth, making fatigue life sensitive to environment.

### ns_ht_am_hastelloyx_lcf_model_001

For additively manufactured Hastelloy X, microstructure-based low-cycle-fatigue models can combine measured texture or grain information with cyclic plasticity and damage parameters. Such models try to connect AM microstructure heterogeneity to fatigue-life prediction.

### ns_ht_gh4169_entropy_fatigue_001

For GH4169 low-cycle fatigue at elevated temperature, a thermodynamic entropy method can connect cyclic plasticity modeling with fatigue-life prediction. Entropy generation in the gauge section can serve as a damage-related quantity rather than using stress amplitude alone.

### ns_ht_rejuvenation_heat_treatment_001

Rejuvenation heat treatment can recover creep-degraded directionally solidified superalloys by modifying gamma-prime morphology. In one optimized regime, solution treatment near 1283 C and primary aging near 1095 C restored most standard heat-treatment creep life and increased total creep life.

### ns_ht_transfer_learning_creep_design_001

Transfer learning can guide single-crystal superalloy composition design for ultrahigh-temperature creep resistance. A designed alloy can be validated under 1200 C and 80 MPa creep, where rupture life above 170 h indicates that data-driven screening can still require experimental confirmation.

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

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The model correctly selects Aluminum mobility, which is directly supported by the retrieved context and matches the gold answer.

Retrieved context:

### ns_ht_creep_rafting_al_mobility_001

During 850 C creep of a directionally solidified nickel-based superalloy, aluminum mobility can control gamma-prime rafting. Larger plastic strain flow promotes P-type rafting, while restricted deformation can leave the gamma-prime structure less rafted.

### ns_ht_pfml_shap_design_features_001

Feature-importance analysis in phase-field-informed creep models can rank descriptors such as aluminum partitioning, cobalt partitioning, lattice misfit, gamma-prime volume fraction, and rafting state. These descriptors connect composition and microstructure to predicted creep strain.

### ns_ht_pm_hip_fatigue_review_001

Powder metallurgy hot-isostatic-pressed superalloys can show fatigue behavior controlled by powder quality, residual defects, grain structure, and heat treatment. Reviewing these factors helps separate processing-driven fatigue limits from intrinsic alloy strengthening effects.

### ns_ht_gh4169_laves_delta_heat_001

In GH4169/Inconel 718, Laves phase formed during solidification can consume niobium and weaken the matrix. Homogenization and aging treatments can reduce segregation, promote delta or gamma-double-prime control, and change creep or fatigue behavior.

### ns_ht_creep_orientation_850c_001

At 850 C, a directionally solidified nickel-based superalloy can show stronger creep resistance in the longitudinal orientation than in the transverse orientation. The longitudinal condition activates more slip systems and APB shearing, while the transverse condition is dominated by fewer slip bands and SISF-related deformation.

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

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The model prediction exactly matches the gold answer and all selected statements are directly supported by the retrieved context.

Retrieved context:

### ns_ht_oxidation_lpbf_gh3536_001

For LPBF GH3536 oxidized at 950 C, the cellular microstructure can provide rapid diffusion paths that accelerate protective-film formation during early exposure. After long exposure, the LPBF material can show better oxidation resistance than a wrought counterpart.

### ns_ht_oxidation_ce_coating_001

In additively manufactured IN625 exposed to 900 C air, intergranular oxidation can begin when scale buckling opens grain-boundary voids. A very thin cerium coating can improve chromia scale adherence and slow inward oxide growth.

### ns_ht_cm247lc_lpbf_crack_mitigation_001

LPBF processing of crack-susceptible CM247LC-class superalloys requires control of thermal gradients, residual stress, and grain-boundary liquid films. Process optimization and heat treatment can reduce cracking but may not remove all solidification-related defects.

### ns_ht_filmcooling_hot_corrosion_001

Film-cooling holes in nickel-based turbine alloys can alter molten-salt hot-corrosion behavior by changing local salt retention, gas access, oxide-scale growth, and stress concentration around the hole surface.

### ns_ht_k452_so2_corrosion_001

For K452 nickel-based cast superalloy in high-temperature SO2-containing atmospheres, long exposure can promote sulfur-assisted corrosion. Damage involves oxide-scale evolution, sulfur penetration, and corrosion products that are less protective than a stable chromia-rich scale.

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

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction exactly matches the gold answer and is directly supported by the retrieved context.

Retrieved context:

### ns_ht_oxidation_ce_coating_001

In additively manufactured IN625 exposed to 900 C air, intergranular oxidation can begin when scale buckling opens grain-boundary voids. A very thin cerium coating can improve chromia scale adherence and slow inward oxide growth.

### ns_ht_am_hastelloyx_lcf_model_001

For additively manufactured Hastelloy X, microstructure-based low-cycle-fatigue models can combine measured texture or grain information with cyclic plasticity and damage parameters. Such models try to connect AM microstructure heterogeneity to fatigue-life prediction.

### ns_ht_am_hastelloyx_notch_orientation_001

AM Hastelloy X fatigue behavior can depend on build orientation, notch or surface condition, and local stress concentration. Orientation-sensitive microstructure and defect populations can change where cyclic damage initiates.

### ns_ht_am_review_defect_taxonomy_001

Common AM nickel-superalloy defect classes include lack-of-fusion pores, gas pores, keyhole porosity, microcracks, residual stress, rough surfaces, and microsegregation. These defects influence fatigue, creep, oxidation, and hot-corrosion performance differently.

### ns_ht_hot_corrosion_alloying_001

In molten-salt hot corrosion of nickel-based superalloys, alloying elements can change oxide-scale stability, internal sulfidation, and diffusion of protective elements. Damage can combine surface oxidation, internal sulfidation, scale cracking, and spallation rather than a single degradation mode.

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
Prediction: At 850 C, longitudinal orientation activates more slip systems and APB shearing, giving stronger creep resistance. Larger plastic strain flow promotes P-type rafting.

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=Prediction covers all required points and is directly supported by the context.

Retrieved context:

### ns_ht_creep_rafting_al_mobility_001

During 850 C creep of a directionally solidified nickel-based superalloy, aluminum mobility can control gamma-prime rafting. Larger plastic strain flow promotes P-type rafting, while restricted deformation can leave the gamma-prime structure less rafted.

### ns_ht_nimonic263_creep_fatigue_interaction_001

Nimonic 263-type nickel superalloys can show creep-fatigue interaction at high temperature when dwell periods allow time-dependent damage. Grain-boundary oxidation, cavity formation, and cyclic plastic strain jointly control life.

### ns_ht_creep_orientation_850c_001

At 850 C, a directionally solidified nickel-based superalloy can show stronger creep resistance in the longitudinal orientation than in the transverse orientation. The longitudinal condition activates more slip systems and APB shearing, while the transverse condition is dominated by fewer slip bands and SISF-related deformation.

### ns_ht_pfml_creep_stress_response_001

Phase-field-informed machine learning for nickel superalloy creep can use simulated microstructures at different stresses and temperatures. Higher applied stress typically increases creep strain, shortens the primary-creep regime, and changes rafting descriptors.

### ns_ht_pfml_shap_design_features_001

Feature-importance analysis in phase-field-informed creep models can rank descriptors such as aluminum partitioning, cobalt partitioning, lattice misfit, gamma-prime volume fraction, and rafting state. These descriptors connect composition and microstructure to predicted creep strain.

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

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction correctly matches the gold answer A, which is directly supported by the retrieved context mentioning rupture life above 170 h at 1200 C and 80 MPa.

Retrieved context:

### ns_ht_transfer_learning_creep_design_001

Transfer learning can guide single-crystal superalloy composition design for ultrahigh-temperature creep resistance. A designed alloy can be validated under 1200 C and 80 MPa creep, where rupture life above 170 h indicates that data-driven screening can still require experimental confirmation.

### ns_ht_rejuvenation_heat_treatment_001

Rejuvenation heat treatment can recover creep-degraded directionally solidified superalloys by modifying gamma-prime morphology. In one optimized regime, solution treatment near 1283 C and primary aging near 1095 C restored most standard heat-treatment creep life and increased total creep life.

### ns_ht_sx_rejuvenation_tcp_001

Rejuvenation or recovery heat treatments for single-crystal superalloys must balance gamma-prime restoration against risks such as TCP phase persistence, recrystallization, and residual creep damage. A treatment that improves precipitate morphology may not fully remove prior damage.

### ns_ht_nimonic263_creep_fatigue_interaction_001

Nimonic 263-type nickel superalloys can show creep-fatigue interaction at high temperature when dwell periods allow time-dependent damage. Grain-boundary oxidation, cavity formation, and cyclic plastic strain jointly control life.

### ns_ht_dd5_overtemp_gamma_prime_001

A second-generation DD5 single-crystal superalloy can retain phase stability after short over-temperature exposure, but gamma-prime coarsening and changes in the gamma/gamma-prime morphology reduce the density of obstacles to dislocation motion.

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

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction exactly matches the gold answer and is directly supported by the context.

Retrieved context:

### ns_ht_drilled_sx_hot_corrosion_001

A drilled nickel-based single-crystal superalloy can show abnormal hot-corrosion behavior because the hole surface changes diffusion paths and oxide-layer development. Local drilling can therefore alter scale adhesion and corrosion-product evolution around the machined region.

### ns_ht_filmcooling_hot_corrosion_001

Film-cooling holes in nickel-based turbine alloys can alter molten-salt hot-corrosion behavior by changing local salt retention, gas access, oxide-scale growth, and stress concentration around the hole surface.

### ns_ht_hastelloyn_igc_cr_diffusion_001

Hastelloy N in FLiNaK can suffer intergranular corrosion because selective chromium diffusion and depletion at grain boundaries make the boundaries preferred paths for corrosion invasion. Loaded samples can show ridge-like corrosion products around grain-boundary regions.

### ns_ht_k452_so2_corrosion_001

For K452 nickel-based cast superalloy in high-temperature SO2-containing atmospheres, long exposure can promote sulfur-assisted corrosion. Damage involves oxide-scale evolution, sulfur penetration, and corrosion products that are less protective than a stable chromia-rich scale.

### ns_ht_in625_molten_salt_chloride_001

Inconel 625 exposed to chloride-containing molten salts can lose chromium and molybdenum from the near-surface region. Selective dissolution and nonprotective corrosion products can make chloride salts more aggressive than simple dry oxidation.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_live_deepseek::ns_ht_q023

- Priority: high
- Reasons: correctness_below_5
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
Prediction: A,B,E

Judge:

correctness=4.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The model correctly selected A, B, and E but missed C, resulting in partial correctness.

Retrieved context:

### ns_ht_slm_in625_preoxidation_001

For SLM Inconel 625, heat treatment combined with pre-oxidation can form a more protective oxide barrier before hot-corrosion exposure. The preformed barrier can improve corrosion resistance by slowing aggressive species from penetrating the additively manufactured microstructure.

### ns_ht_filmcooling_hot_corrosion_001

Film-cooling holes in nickel-based turbine alloys can alter molten-salt hot-corrosion behavior by changing local salt retention, gas access, oxide-scale growth, and stress concentration around the hole surface.

### ns_ht_tic_in625_oxidation_001

TiC-containing Inconel 625 can change microstructural features that affect high-temperature oxidation behavior. Ceramic-particle additions may influence oxide-scale continuity, local element distribution, and oxidation resistance rather than acting only as inert reinforcement.

### ns_ht_hot_corrosion_alloying_001

In molten-salt hot corrosion of nickel-based superalloys, alloying elements can change oxide-scale stability, internal sulfidation, and diffusion of protective elements. Damage can combine surface oxidation, internal sulfidation, scale cracking, and spallation rather than a single degradation mode.

### ns_ht_in625_molten_salt_chloride_001

Inconel 625 exposed to chloride-containing molten salts can lose chromium and molybdenum from the near-surface region. Selective dissolution and nonprotective corrosion products can make chloride salts more aggressive than simple dry oxidation.

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
Prediction: The provided context does not mention entropy-based fatigue prediction, so no comparison is possible. PM-HIP fatigue review knowledge focuses on factors like powder quality, residual defects, grain structure, and heat treatment that control fatigue behavior.

Judge:

correctness=2.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction correctly describes PM-HIP factors but states entropy-based method is not in context, failing to provide the full comparison required by the gold answer.

Retrieved context:

### ns_ht_am_review_feedstock_quality_001

Recent reviews of additively manufactured nickel superalloys emphasize that powder morphology, oxygen pickup, contamination, recycling history, and flowability influence defect formation before any heat treatment is applied.

### ns_ht_pm_hip_fatigue_review_001

Powder metallurgy hot-isostatic-pressed superalloys can show fatigue behavior controlled by powder quality, residual defects, grain structure, and heat treatment. Reviewing these factors helps separate processing-driven fatigue limits from intrinsic alloy strengthening effects.

### ns_ht_am_review_defect_taxonomy_001

Common AM nickel-superalloy defect classes include lack-of-fusion pores, gas pores, keyhole porosity, microcracks, residual stress, rough surfaces, and microsegregation. These defects influence fatigue, creep, oxidation, and hot-corrosion performance differently.

### ns_ht_pfml_creep_stress_response_001

Phase-field-informed machine learning for nickel superalloy creep can use simulated microstructures at different stresses and temperatures. Higher applied stress typically increases creep strain, shortens the primary-creep regime, and changes rafting descriptors.

### ns_ht_oxidation_gb_energy_001

Initial oxidation in Inconel 718 can depend on grain-boundary character. Boundaries with different energy states can change oxygen adsorption, diffusion, and oxide nucleation, so intergranular oxidation does not begin uniformly across all boundaries.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_live_deepseek::ns_ht_q049

- Priority: high
- Reasons: context_support_below_5, faithfulness_below_5, hallucination_risk_above_0
- Method: flashrag_bm25_live_deepseek
- Question type: single_choice

Question:

Which mechanism explains why a correct gold answer can still be poorly supported if BM25 retrieves only part of a multi-source question?
A. A method may hit one relevant chunk while missing another required evidence chunk
B. A hit on any chunk always proves full evidence recall
C. Retrieval recall is unrelated to source_chunk_ids
D. Oracle context removes all need for qrels

Gold answers: ['A']
Prediction: A

Judge:

correctness=5.0, context_support=0.0, faithfulness=0.0, unsupported_claims=none, reason=The model's answer matches the gold answer but is not supported by the retrieved context, which is off-topic; thus context support and faithfulness are low.

Retrieved context:

### ns_ht_cm247lc_lpbf_crack_mitigation_001

LPBF processing of crack-susceptible CM247LC-class superalloys requires control of thermal gradients, residual stress, and grain-boundary liquid films. Process optimization and heat treatment can reduce cracking but may not remove all solidification-related defects.

### ns_ht_gh4169_entropy_fatigue_001

For GH4169 low-cycle fatigue at elevated temperature, a thermodynamic entropy method can connect cyclic plasticity modeling with fatigue-life prediction. Entropy generation in the gauge section can serve as a damage-related quantity rather than using stress amplitude alone.

### ns_ht_transfer_learning_creep_design_001

Transfer learning can guide single-crystal superalloy composition design for ultrahigh-temperature creep resistance. A designed alloy can be validated under 1200 C and 80 MPa creep, where rupture life above 170 h indicates that data-driven screening can still require experimental confirmation.

### ns_ht_rejuvenation_heat_treatment_001

Rejuvenation heat treatment can recover creep-degraded directionally solidified superalloys by modifying gamma-prime morphology. In one optimized regime, solution treatment near 1283 C and primary aging near 1095 C restored most standard heat-treatment creep life and increased total creep life.

### ns_ht_oxidation_gb_energy_001

Initial oxidation in Inconel 718 can depend on grain-boundary character. Boundaries with different energy states can change oxygen adsorption, diffusion, and oxide nucleation, so intergranular oxidation does not begin uniformly across all boundaries.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_live_deepseek::ns_ht_q050

- Priority: normal
- Reasons: none
- Method: flashrag_bm25_live_deepseek
- Question type: fill_blank

Question:

In AM nickel superalloys, powder oxygen pickup, contamination, recycling history, and flowability are feedstock ____ factors.

Gold answers: ['quality']
Prediction: quality

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction exactly matches the gold answer and is supported by the context.

Retrieved context:

### ns_ht_am_review_feedstock_quality_001

Recent reviews of additively manufactured nickel superalloys emphasize that powder morphology, oxygen pickup, contamination, recycling history, and flowability influence defect formation before any heat treatment is applied.

### ns_ht_pm_hip_fatigue_review_001

Powder metallurgy hot-isostatic-pressed superalloys can show fatigue behavior controlled by powder quality, residual defects, grain structure, and heat treatment. Reviewing these factors helps separate processing-driven fatigue limits from intrinsic alloy strengthening effects.

### ns_ht_am_review_defect_taxonomy_001

Common AM nickel-superalloy defect classes include lack-of-fusion pores, gas pores, keyhole porosity, microcracks, residual stress, rough surfaces, and microsegregation. These defects influence fatigue, creep, oxidation, and hot-corrosion performance differently.

### ns_ht_oxidation_gb_energy_001

Initial oxidation in Inconel 718 can depend on grain-boundary character. Boundaries with different energy states can change oxygen adsorption, diffusion, and oxide nucleation, so intergranular oxidation does not begin uniformly across all boundaries.

### ns_ht_am_hastelloyx_notch_orientation_001

AM Hastelloy X fatigue behavior can depend on build orientation, notch or surface condition, and local stress concentration. Orientation-sensitive microstructure and defect populations can change where cyclic damage initiates.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_live_deepseek::ns_ht_q051

- Priority: normal
- Reasons: none
- Method: flashrag_bm25_live_deepseek
- Question type: short_answer

Question:

Compare steam oxidation of Rene 77 with chloride molten-salt corrosion of Inconel 625.

Gold answers: ['Rene 77 steam oxidation can become controlled by a more continuous oxide scale, while chloride molten salt can selectively dissolve chromium and molybdenum and form nonprotective corrosion products.']
Prediction: Inconel 625 exposed to chloride-containing molten salts loses chromium and molybdenum from the near-surface region, and selective dissolution with nonprotective corrosion products can make the attack more aggressive than dry oxidation. In contrast, Rene 77 undergoing high-temperature steam oxidation may develop a more continuous oxide scale that slows mass gain, though its protectiveness depends on scale compactness, spallation, and chromium-rich oxide formation.

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction accurately compares the two corrosion mechanisms using the provided contexts, matching the gold answer.

Retrieved context:

### ns_ht_in625_molten_salt_chloride_001

Inconel 625 exposed to chloride-containing molten salts can lose chromium and molybdenum from the near-surface region. Selective dissolution and nonprotective corrosion products can make chloride salts more aggressive than simple dry oxidation.

### ns_ht_rene77_steam_oxidation_001

During long high-temperature steam oxidation of Rene 77, mass gain can slow after an initial transient as a more continuous oxide scale develops. Changes in scale compactness, local spallation, and chromium-rich oxide formation control whether the oxide remains protective.

### ns_ht_hastelloyn_stress_flinak_001

In FLiNaK molten salt, applied stress can increase Hastelloy N corrosion rate compared with an unloaded condition. Stress-assisted corrosion is linked to accelerated grain-boundary attack and a higher weight-loss rate in the molten-salt environment.

### ns_ht_rene77_microsegregation_heat_001

In cast Rene 77, solidification can leave a gamma dendrite matrix with MC carbides and microsegregated interdendritic regions. Heat treatment can dissolve or redistribute nonequilibrium constituents while gamma-prime precipitation strengthens the aged microstructure.

### ns_ht_filmcooling_hot_corrosion_001

Film-cooling holes in nickel-based turbine alloys can alter molten-salt hot-corrosion behavior by changing local salt retention, gas access, oxide-scale growth, and stress concentration around the hole surface.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_live_deepseek::ns_ht_q052

- Priority: high
- Reasons: correctness_below_5
- Method: flashrag_bm25_live_deepseek
- Question type: multiple_choice

Question:

Which statements compare molten-salt and SO2 corrosion mechanisms in the medium corpus?
A. FLiNaK stress can accelerate grain-boundary attack in Hastelloy N
B. SO2 exposure can promote sulfur-assisted corrosion in K452
C. Chloride molten salt can deplete chromium and molybdenum in Inconel 625
D. All three mechanisms are independent of grain boundaries or selective chemistry
E. Chromium-rich protective scales can be destabilized or depleted

Gold answers: ['A', 'B', 'C', 'E']
Prediction: E

Judge:

correctness=0.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction only selected E, but the correct answer requires A, B, C, and E.

Retrieved context:

### ns_ht_hastelloyn_stress_flinak_001

In FLiNaK molten salt, applied stress can increase Hastelloy N corrosion rate compared with an unloaded condition. Stress-assisted corrosion is linked to accelerated grain-boundary attack and a higher weight-loss rate in the molten-salt environment.

### ns_ht_in625_molten_salt_chloride_001

Inconel 625 exposed to chloride-containing molten salts can lose chromium and molybdenum from the near-surface region. Selective dissolution and nonprotective corrosion products can make chloride salts more aggressive than simple dry oxidation.

### ns_ht_k452_so2_corrosion_001

For K452 nickel-based cast superalloy in high-temperature SO2-containing atmospheres, long exposure can promote sulfur-assisted corrosion. Damage involves oxide-scale evolution, sulfur penetration, and corrosion products that are less protective than a stable chromia-rich scale.

### ns_ht_hastelloyn_igc_cr_diffusion_001

Hastelloy N in FLiNaK can suffer intergranular corrosion because selective chromium diffusion and depletion at grain boundaries make the boundaries preferred paths for corrosion invasion. Loaded samples can show ridge-like corrosion products around grain-boundary regions.

### ns_ht_filmcooling_hot_corrosion_001

Film-cooling holes in nickel-based turbine alloys can alter molten-salt hot-corrosion behavior by changing local salt retention, gas access, oxide-scale growth, and stress concentration around the hole surface.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_live_deepseek::ns_ht_q053

- Priority: normal
- Reasons: none
- Method: flashrag_bm25_live_deepseek
- Question type: single_choice

Question:

What makes DD5 over-temperature damage a creep risk even without obvious TCP phase formation?
A. Gamma-prime coarsening can weaken dislocation-network and Orowan resistance
B. The alloy becomes immune to dislocation motion
C. TCP absence always means rupture life is unchanged
D. Over-temperature exposure removes gamma/gamma-prime morphology

Gold answers: ['A']
Prediction: A

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction matches the gold answer and is fully supported by the retrieved context.

Retrieved context:

### ns_ht_dd5_creep_rupture_overtemp_001

After over-temperature exposure, DD5 creep rupture life at high temperature can decrease even when no obvious TCP phase forms. The reduction is associated with coarsened gamma-prime, weakened dislocation networks, and less effective Orowan bypass resistance.

### ns_ht_dd5_overtemp_gamma_prime_001

A second-generation DD5 single-crystal superalloy can retain phase stability after short over-temperature exposure, but gamma-prime coarsening and changes in the gamma/gamma-prime morphology reduce the density of obstacles to dislocation motion.

### ns_ht_sx_rejuvenation_tcp_001

Rejuvenation or recovery heat treatments for single-crystal superalloys must balance gamma-prime restoration against risks such as TCP phase persistence, recrystallization, and residual creep damage. A treatment that improves precipitate morphology may not fully remove prior damage.

### ns_ht_gh4169_laves_delta_heat_001

In GH4169/Inconel 718, Laves phase formed during solidification can consume niobium and weaken the matrix. Homogenization and aging treatments can reduce segregation, promote delta or gamma-double-prime control, and change creep or fatigue behavior.

### ns_ht_pf_ml_creep_features_001

Phase-field-informed machine learning can predict creep strain from simulated microstructure and composition descriptors. Useful descriptors include gamma-prime rafting degree, gamma-prime volume fraction, interparticle spacing, and elemental partitioning coefficients.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_live_deepseek::ns_ht_q054

- Priority: normal
- Reasons: none
- Method: flashrag_bm25_live_deepseek
- Question type: fill_blank

Question:

Feature-importance analysis in PF-informed creep models can rank gamma-prime volume fraction and lattice ____.

Gold answers: ['misfit']
Prediction: misfit

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction correctly fills the blank with 'misfit', matching the gold answer and supported by the retrieved context.

Retrieved context:

### ns_ht_pfml_shap_design_features_001

Feature-importance analysis in phase-field-informed creep models can rank descriptors such as aluminum partitioning, cobalt partitioning, lattice misfit, gamma-prime volume fraction, and rafting state. These descriptors connect composition and microstructure to predicted creep strain.

### ns_ht_pf_ml_creep_features_001

Phase-field-informed machine learning can predict creep strain from simulated microstructure and composition descriptors. Useful descriptors include gamma-prime rafting degree, gamma-prime volume fraction, interparticle spacing, and elemental partitioning coefficients.

### ns_ht_creep_rafting_al_mobility_001

During 850 C creep of a directionally solidified nickel-based superalloy, aluminum mobility can control gamma-prime rafting. Larger plastic strain flow promotes P-type rafting, while restricted deformation can leave the gamma-prime structure less rafted.

### ns_ht_dd5_overtemp_gamma_prime_001

A second-generation DD5 single-crystal superalloy can retain phase stability after short over-temperature exposure, but gamma-prime coarsening and changes in the gamma/gamma-prime morphology reduce the density of obstacles to dislocation motion.

### ns_ht_rejuvenation_heat_treatment_001

Rejuvenation heat treatment can recover creep-degraded directionally solidified superalloys by modifying gamma-prime morphology. In one optimized regime, solution treatment near 1283 C and primary aging near 1095 C restored most standard heat-treatment creep life and increased total creep life.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_live_deepseek::ns_ht_q055

- Priority: high
- Reasons: correctness_below_5, context_support_below_5
- Method: flashrag_bm25_live_deepseek
- Question type: short_answer

Question:

How do AM Hastelloy X fatigue modelling and AM defect taxonomy connect in the medium corpus?

Gold answers: ['Fatigue models link texture, grains, cyclic plasticity, and damage, while defect taxonomy identifies pores, cracks, residual stress, roughness, and segregation that influence fatigue initiation.']
Prediction: AM Hastelloy X fatigue models incorporate AM defect populations such as lack-of-fusion pores, microcracks, and rough surfaces as part of the microstructure heterogeneity that governs cyclic damage initiation and fatigue-life prediction. The defect taxonomy defines these defect classes that are known to influence fatigue performance. Fatigue modeling links these defects to local stress concentration and orientation-sensitive damage behavior.

Judge:

correctness=4.0, context_support=4.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction accurately connects fatigue models and defect taxonomy but slightly overstates direct incorporation of defects, while the gold answer carefully separates the two aspects.

Retrieved context:

### ns_ht_am_hastelloyx_lcf_model_001

For additively manufactured Hastelloy X, microstructure-based low-cycle-fatigue models can combine measured texture or grain information with cyclic plasticity and damage parameters. Such models try to connect AM microstructure heterogeneity to fatigue-life prediction.

### ns_ht_am_hastelloyx_notch_orientation_001

AM Hastelloy X fatigue behavior can depend on build orientation, notch or surface condition, and local stress concentration. Orientation-sensitive microstructure and defect populations can change where cyclic damage initiates.

### ns_ht_am_review_defect_taxonomy_001

Common AM nickel-superalloy defect classes include lack-of-fusion pores, gas pores, keyhole porosity, microcracks, residual stress, rough surfaces, and microsegregation. These defects influence fatigue, creep, oxidation, and hot-corrosion performance differently.

### ns_ht_chi_lpt_strengthening_001

Stress-dependent local phase transformation can strengthen nickel-based superalloys by forming chi-phase nanolaths at planar defects. This mechanism can immobilize defect motion and create a self-strengthening response during deformation.

### ns_ht_pfml_shap_design_features_001

Feature-importance analysis in phase-field-informed creep models can rank descriptors such as aluminum partitioning, cobalt partitioning, lattice misfit, gamma-prime volume fraction, and rafting state. These descriptors connect composition and microstructure to predicted creep strain.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_live_deepseek::ns_ht_q056

- Priority: high
- Reasons: correctness_below_5
- Method: flashrag_bm25_live_deepseek
- Question type: multiple_choice

Question:

Which statements synthesize coating, steam, and film-cooling corrosion risks?
A. Coating-substrate interdiffusion can deplete protective elements
B. Inconel 740H-type alloys can depend on chromia continuity
C. Film-cooling holes can change local salt retention and scale growth
D. Water vapor, chlorides, and sulfur can destabilize protective scales
E. All hot-section features always improve scale adherence

Gold answers: ['A', 'B', 'C', 'D']
Prediction: B,C,D

Judge:

correctness=4.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction included all correct options supported by the context (B, C, D) but missed gold option A.

Retrieved context:

### ns_ht_inconel740h_steam_oxidation_001

Inconel 740H and related nickel alloys in steam or fireside environments can depend on chromia continuity for corrosion resistance. Water vapor, chlorides, and sulfur species can destabilize the oxide scale and accelerate chromium depletion.

### ns_ht_filmcooling_hot_corrosion_001

Film-cooling holes in nickel-based turbine alloys can alter molten-salt hot-corrosion behavior by changing local salt retention, gas access, oxide-scale growth, and stress concentration around the hole surface.

### ns_ht_k452_so2_corrosion_001

For K452 nickel-based cast superalloy in high-temperature SO2-containing atmospheres, long exposure can promote sulfur-assisted corrosion. Damage involves oxide-scale evolution, sulfur penetration, and corrosion products that are less protective than a stable chromia-rich scale.

### ns_ht_oxidation_ce_coating_001

In additively manufactured IN625 exposed to 900 C air, intergranular oxidation can begin when scale buckling opens grain-boundary voids. A very thin cerium coating can improve chromia scale adherence and slow inward oxide growth.

### ns_ht_rene77_steam_oxidation_001

During long high-temperature steam oxidation of Rene 77, mass gain can slow after an initial transient as a more continuous oxide scale develops. Changes in scale compactness, local spallation, and chromium-rich oxide formation control whether the oxide remains protective.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_live_deepseek::ns_ht_q057

- Priority: normal
- Reasons: none
- Method: flashrag_bm25_live_deepseek
- Question type: single_choice

Question:

In high-temperature fatigue, what distinguishes environmental LCF degradation from heat-treatment phase control?
A. Environmental LCF can involve hydrogen or oxidation-assisted crack initiation, while phase control changes precipitates or segregation
B. Both are only dataset split labels
C. Hydrogen and oxidation cannot affect crack initiation
D. Heat treatment never changes precipitates

Gold answers: ['A']
Prediction: A

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The model correctly selected option A, which is fully supported by context demonstrating hydrogen-assisted crack initiation and heat treatment altering precipitates.

Retrieved context:

### ns_ht_cm247lc_lpbf_crack_mitigation_001

LPBF processing of crack-susceptible CM247LC-class superalloys requires control of thermal gradients, residual stress, and grain-boundary liquid films. Process optimization and heat treatment can reduce cracking but may not remove all solidification-related defects.

### ns_ht_in718_hydrogen_lcf_001

Hydrogen-assisted low-cycle fatigue in Inconel 718 can reduce ductility and promote earlier crack initiation. Elevated temperature can interact with hydrogen transport, slip localization, and crack growth, making fatigue life sensitive to environment.

### ns_ht_pm_hip_fatigue_review_001

Powder metallurgy hot-isostatic-pressed superalloys can show fatigue behavior controlled by powder quality, residual defects, grain structure, and heat treatment. Reviewing these factors helps separate processing-driven fatigue limits from intrinsic alloy strengthening effects.

### ns_ht_sx_rejuvenation_tcp_001

Rejuvenation or recovery heat treatments for single-crystal superalloys must balance gamma-prime restoration against risks such as TCP phase persistence, recrystallization, and residual creep damage. A treatment that improves precipitate morphology may not fully remove prior damage.

### ns_ht_gh4169_laves_delta_heat_001

In GH4169/Inconel 718, Laves phase formed during solidification can consume niobium and weaken the matrix. Homogenization and aging treatments can reduce segregation, promote delta or gamma-double-prime control, and change creep or fatigue behavior.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_live_deepseek::ns_ht_q058

- Priority: normal
- Reasons: none
- Method: flashrag_bm25_live_deepseek
- Question type: fill_blank

Question:

A rejuvenation treatment can improve gamma-prime morphology but may not remove prior creep ____.

Gold answers: ['damage']
Prediction: damage

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction exactly matches the gold answer and is directly supported by the context stating that rejuvenation may not fully remove prior damage.

Retrieved context:

### ns_ht_sx_rejuvenation_tcp_001

Rejuvenation or recovery heat treatments for single-crystal superalloys must balance gamma-prime restoration against risks such as TCP phase persistence, recrystallization, and residual creep damage. A treatment that improves precipitate morphology may not fully remove prior damage.

### ns_ht_rejuvenation_heat_treatment_001

Rejuvenation heat treatment can recover creep-degraded directionally solidified superalloys by modifying gamma-prime morphology. In one optimized regime, solution treatment near 1283 C and primary aging near 1095 C restored most standard heat-treatment creep life and increased total creep life.

### ns_ht_gh4169_laves_delta_heat_001

In GH4169/Inconel 718, Laves phase formed during solidification can consume niobium and weaken the matrix. Homogenization and aging treatments can reduce segregation, promote delta or gamma-double-prime control, and change creep or fatigue behavior.

### ns_ht_rene77_microsegregation_heat_001

In cast Rene 77, solidification can leave a gamma dendrite matrix with MC carbides and microsegregated interdendritic regions. Heat treatment can dissolve or redistribute nonequilibrium constituents while gamma-prime precipitation strengthens the aged microstructure.

### ns_ht_pf_ml_creep_features_001

Phase-field-informed machine learning can predict creep strain from simulated microstructure and composition descriptors. Useful descriptors include gamma-prime rafting degree, gamma-prime volume fraction, interparticle spacing, and elemental partitioning coefficients.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_live_deepseek::ns_ht_q059

- Priority: normal
- Reasons: none
- Method: flashrag_bm25_live_deepseek
- Question type: short_answer

Question:

Compare LPBF CM247LC crack mitigation with Nimonic 263 creep-fatigue dwell damage.

Gold answers: ['LPBF CM247LC mitigation controls thermal gradients, residual stress, and liquid-film cracking, while Nimonic 263 dwell damage involves time-dependent creep-fatigue mechanisms such as grain-boundary oxidation, cavities, and cyclic plastic strain.']
Prediction: LPBF CM247LC crack mitigation requires control of thermal gradients, residual stress, and grain-boundary liquid films through process optimization and heat treatment. Nimonic 263 creep-fatigue dwell damage involves grain-boundary oxidation, cavity formation, and cyclic plastic strain.

Judge:

correctness=5.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction accurately and faithfully extracts the key comparison points from the provided context, fully matching the gold answer.

Retrieved context:

### ns_ht_cm247lc_lpbf_crack_mitigation_001

LPBF processing of crack-susceptible CM247LC-class superalloys requires control of thermal gradients, residual stress, and grain-boundary liquid films. Process optimization and heat treatment can reduce cracking but may not remove all solidification-related defects.

### ns_ht_nimonic263_creep_fatigue_interaction_001

Nimonic 263-type nickel superalloys can show creep-fatigue interaction at high temperature when dwell periods allow time-dependent damage. Grain-boundary oxidation, cavity formation, and cyclic plastic strain jointly control life.

### ns_ht_oxidation_lpbf_gh3536_001

For LPBF GH3536 oxidized at 950 C, the cellular microstructure can provide rapid diffusion paths that accelerate protective-film formation during early exposure. After long exposure, the LPBF material can show better oxidation resistance than a wrought counterpart.

### ns_ht_in718_hydrogen_lcf_001

Hydrogen-assisted low-cycle fatigue in Inconel 718 can reduce ductility and promote earlier crack initiation. Elevated temperature can interact with hydrogen transport, slip localization, and crack growth, making fatigue life sensitive to environment.

### ns_ht_sx_lcf_oxidation_competition_001

In high-temperature low-cycle fatigue of single-crystal nickel superalloys, surface oxidation and internal casting pores can compete as crack-initiation sites. Load ratio, hold time, and cycling frequency can shift the dominant damage mechanism.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:

## fresh_hard::flashrag_bm25_live_deepseek::ns_ht_q060

- Priority: high
- Reasons: correctness_below_5
- Method: flashrag_bm25_live_deepseek
- Question type: multiple_choice

Question:

Which statements synthesize the medium corpus' fatigue and life-prediction evidence?
A. PF-informed models can rank composition and microstructure descriptors
B. Hydrogen-assisted LCF can reduce ductility and promote crack initiation
C. Single-crystal LCF can involve competition between oxidation and pores
D. AM Hastelloy X models connect microstructure heterogeneity to fatigue life
E. Life prediction never uses microstructure or environment

Gold answers: ['A', 'B', 'C', 'D']
Prediction: B,D

Judge:

correctness=3.0, context_support=5.0, faithfulness=5.0, unsupported_claims=none, reason=The prediction includes two correct statements (B and D) out of the four correct answers, making it partially correct but directly supported by the context and faithful.

Retrieved context:

### ns_ht_in718_hydrogen_lcf_001

Hydrogen-assisted low-cycle fatigue in Inconel 718 can reduce ductility and promote earlier crack initiation. Elevated temperature can interact with hydrogen transport, slip localization, and crack growth, making fatigue life sensitive to environment.

### ns_ht_am_hastelloyx_lcf_model_001

For additively manufactured Hastelloy X, microstructure-based low-cycle-fatigue models can combine measured texture or grain information with cyclic plasticity and damage parameters. Such models try to connect AM microstructure heterogeneity to fatigue-life prediction.

### ns_ht_gh4169_entropy_fatigue_001

For GH4169 low-cycle fatigue at elevated temperature, a thermodynamic entropy method can connect cyclic plasticity modeling with fatigue-life prediction. Entropy generation in the gauge section can serve as a damage-related quantity rather than using stress amplitude alone.

### ns_ht_rejuvenation_heat_treatment_001

Rejuvenation heat treatment can recover creep-degraded directionally solidified superalloys by modifying gamma-prime morphology. In one optimized regime, solution treatment near 1283 C and primary aging near 1095 C restored most standard heat-treatment creep life and increased total creep life.

### ns_ht_transfer_learning_creep_design_001

Transfer learning can guide single-crystal superalloy composition design for ultrahigh-temperature creep resistance. A designed alloy can be validated under 1200 C and 80 MPa creep, where rupture life above 170 h indicates that data-driven screening can still require experimental confirmation.

Human review:

- correctness:
- context_support:
- faithfulness:
- decision:
- notes:
