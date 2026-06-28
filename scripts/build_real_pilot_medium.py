from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "benchmark"))

from domainrag.easy_dataset_adapter import export_domainrag_bundle  # noqa: E402
from domainrag.errors import ValidationError, ValidationIssue  # noqa: E402
from domainrag.io_utils import read_jsonl, write_jsonl  # noqa: E402


BASE_FIXTURE = ROOT / "fixtures" / "easy_dataset" / "real_pilot_nickel_superalloy_expanded"
BASE_SOURCES = (
    ROOT
    / "data"
    / "real_pilot_sources"
    / "nickel_superalloy_high_temp_failure_expanded"
    / "sources.jsonl"
)
DEFAULT_FIXTURE = ROOT / "fixtures" / "easy_dataset" / "real_pilot_nickel_superalloy_medium"
DEFAULT_SOURCE_DIR = (
    ROOT
    / "data"
    / "real_pilot_sources"
    / "nickel_superalloy_high_temp_failure_medium"
)
DEFAULT_OUTPUT = ROOT / "data"
DEFAULT_DATASET_NAME = "real_pilot_nickel_superalloy_medium"


NEW_CHUNKS: list[dict[str, str]] = [
    {
        "id": "ns_ht_rene77_microsegregation_heat_001",
        "content": "In cast Rene 77, solidification can leave a gamma dendrite matrix with MC carbides and microsegregated interdendritic regions. Heat treatment can dissolve or redistribute nonequilibrium constituents while gamma-prime precipitation strengthens the aged microstructure.",
    },
    {
        "id": "ns_ht_rene77_steam_oxidation_001",
        "content": "During long high-temperature steam oxidation of Rene 77, mass gain can slow after an initial transient as a more continuous oxide scale develops. Changes in scale compactness, local spallation, and chromium-rich oxide formation control whether the oxide remains protective.",
    },
    {
        "id": "ns_ht_dd5_overtemp_gamma_prime_001",
        "content": "A second-generation DD5 single-crystal superalloy can retain phase stability after short over-temperature exposure, but gamma-prime coarsening and changes in the gamma/gamma-prime morphology reduce the density of obstacles to dislocation motion.",
    },
    {
        "id": "ns_ht_dd5_creep_rupture_overtemp_001",
        "content": "After over-temperature exposure, DD5 creep rupture life at high temperature can decrease even when no obvious TCP phase forms. The reduction is associated with coarsened gamma-prime, weakened dislocation networks, and less effective Orowan bypass resistance.",
    },
    {
        "id": "ns_ht_k452_so2_corrosion_001",
        "content": "For K452 nickel-based cast superalloy in high-temperature SO2-containing atmospheres, long exposure can promote sulfur-assisted corrosion. Damage involves oxide-scale evolution, sulfur penetration, and corrosion products that are less protective than a stable chromia-rich scale.",
    },
    {
        "id": "ns_ht_hastelloyn_stress_flinak_001",
        "content": "In FLiNaK molten salt, applied stress can increase Hastelloy N corrosion rate compared with an unloaded condition. Stress-assisted corrosion is linked to accelerated grain-boundary attack and a higher weight-loss rate in the molten-salt environment.",
    },
    {
        "id": "ns_ht_hastelloyn_igc_cr_diffusion_001",
        "content": "Hastelloy N in FLiNaK can suffer intergranular corrosion because selective chromium diffusion and depletion at grain boundaries make the boundaries preferred paths for corrosion invasion. Loaded samples can show ridge-like corrosion products around grain-boundary regions.",
    },
    {
        "id": "ns_ht_am_hastelloyx_lcf_model_001",
        "content": "For additively manufactured Hastelloy X, microstructure-based low-cycle-fatigue models can combine measured texture or grain information with cyclic plasticity and damage parameters. Such models try to connect AM microstructure heterogeneity to fatigue-life prediction.",
    },
    {
        "id": "ns_ht_am_hastelloyx_notch_orientation_001",
        "content": "AM Hastelloy X fatigue behavior can depend on build orientation, notch or surface condition, and local stress concentration. Orientation-sensitive microstructure and defect populations can change where cyclic damage initiates.",
    },
    {
        "id": "ns_ht_am_review_feedstock_quality_001",
        "content": "Recent reviews of additively manufactured nickel superalloys emphasize that powder morphology, oxygen pickup, contamination, recycling history, and flowability influence defect formation before any heat treatment is applied.",
    },
    {
        "id": "ns_ht_am_review_defect_taxonomy_001",
        "content": "Common AM nickel-superalloy defect classes include lack-of-fusion pores, gas pores, keyhole porosity, microcracks, residual stress, rough surfaces, and microsegregation. These defects influence fatigue, creep, oxidation, and hot-corrosion performance differently.",
    },
    {
        "id": "ns_ht_pfml_creep_stress_response_001",
        "content": "Phase-field-informed machine learning for nickel superalloy creep can use simulated microstructures at different stresses and temperatures. Higher applied stress typically increases creep strain, shortens the primary-creep regime, and changes rafting descriptors.",
    },
    {
        "id": "ns_ht_pfml_shap_design_features_001",
        "content": "Feature-importance analysis in phase-field-informed creep models can rank descriptors such as aluminum partitioning, cobalt partitioning, lattice misfit, gamma-prime volume fraction, and rafting state. These descriptors connect composition and microstructure to predicted creep strain.",
    },
    {
        "id": "ns_ht_sx_lcf_oxidation_competition_001",
        "content": "In high-temperature low-cycle fatigue of single-crystal nickel superalloys, surface oxidation and internal casting pores can compete as crack-initiation sites. Load ratio, hold time, and cycling frequency can shift the dominant damage mechanism.",
    },
    {
        "id": "ns_ht_filmcooling_hot_corrosion_001",
        "content": "Film-cooling holes in nickel-based turbine alloys can alter molten-salt hot-corrosion behavior by changing local salt retention, gas access, oxide-scale growth, and stress concentration around the hole surface.",
    },
    {
        "id": "ns_ht_mar_m247_coating_diffusion_001",
        "content": "Protective coatings on MAR-M247-type nickel superalloys rely on aluminum or chromium reservoirs to form adherent oxides. Interdiffusion between coating and substrate can deplete protective elements and change long-term oxidation resistance.",
    },
    {
        "id": "ns_ht_inconel740h_steam_oxidation_001",
        "content": "Inconel 740H and related nickel alloys in steam or fireside environments can depend on chromia continuity for corrosion resistance. Water vapor, chlorides, and sulfur species can destabilize the oxide scale and accelerate chromium depletion.",
    },
    {
        "id": "ns_ht_in718_hydrogen_lcf_001",
        "content": "Hydrogen-assisted low-cycle fatigue in Inconel 718 can reduce ductility and promote earlier crack initiation. Elevated temperature can interact with hydrogen transport, slip localization, and crack growth, making fatigue life sensitive to environment.",
    },
    {
        "id": "ns_ht_cm247lc_lpbf_crack_mitigation_001",
        "content": "LPBF processing of crack-susceptible CM247LC-class superalloys requires control of thermal gradients, residual stress, and grain-boundary liquid films. Process optimization and heat treatment can reduce cracking but may not remove all solidification-related defects.",
    },
    {
        "id": "ns_ht_gh4169_laves_delta_heat_001",
        "content": "In GH4169/Inconel 718, Laves phase formed during solidification can consume niobium and weaken the matrix. Homogenization and aging treatments can reduce segregation, promote delta or gamma-double-prime control, and change creep or fatigue behavior.",
    },
    {
        "id": "ns_ht_nimonic263_creep_fatigue_interaction_001",
        "content": "Nimonic 263-type nickel superalloys can show creep-fatigue interaction at high temperature when dwell periods allow time-dependent damage. Grain-boundary oxidation, cavity formation, and cyclic plastic strain jointly control life.",
    },
    {
        "id": "ns_ht_in625_molten_salt_chloride_001",
        "content": "Inconel 625 exposed to chloride-containing molten salts can lose chromium and molybdenum from the near-surface region. Selective dissolution and nonprotective corrosion products can make chloride salts more aggressive than simple dry oxidation.",
    },
    {
        "id": "ns_ht_sx_rejuvenation_tcp_001",
        "content": "Rejuvenation or recovery heat treatments for single-crystal superalloys must balance gamma-prime restoration against risks such as TCP phase persistence, recrystallization, and residual creep damage. A treatment that improves precipitate morphology may not fully remove prior damage.",
    },
]


NEW_SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "nsht_rene77_cast_heat_2025",
        "title": "High-temperature steam oxidation behavior and cast microstructure of Rene 77 superalloy",
        "year": 2025,
        "url": "https://www.nature.com/articles/s41598-025-88553-z",
        "access": "open_access",
        "used_for_chunk_ids": [
            "ns_ht_rene77_microsegregation_heat_001",
            "ns_ht_rene77_steam_oxidation_001",
        ],
        "evidence_note": "Used for Rene 77 cast microstructure, heat-treatment response, and long steam-oxidation behavior.",
    },
    {
        "source_id": "nsht_dd5_overtemperature_2025",
        "title": "Over-temperature microstructural stability and creep rupture properties of a second generation single crystal superalloy",
        "year": 2025,
        "url": "https://www.nature.com/articles/s41598-025-97631-7",
        "access": "open_access",
        "used_for_chunk_ids": [
            "ns_ht_dd5_overtemp_gamma_prime_001",
            "ns_ht_dd5_creep_rupture_overtemp_001",
        ],
        "evidence_note": "Used for DD5 gamma-prime coarsening and creep-rupture degradation after over-temperature exposure.",
    },
    {
        "source_id": "nsht_k452_so2_corrosion_2025",
        "title": "Effects of SO2 on the long-term corrosion behaviour of K452 nickel-based superalloy",
        "year": 2025,
        "url": "https://www.nature.com/articles/s41529-025-00588-5",
        "access": "open_access",
        "used_for_chunk_ids": ["ns_ht_k452_so2_corrosion_001"],
        "evidence_note": "Used for sulfur-assisted long-term high-temperature corrosion of K452.",
    },
    {
        "source_id": "nsht_hastelloyn_flinak_stress_2022",
        "title": "Stress-assisted corrosion behaviour of Hastelloy N in FLiNaK molten salt",
        "year": 2022,
        "url": "https://www.nature.com/articles/s41529-022-00300-x",
        "access": "open_access",
        "used_for_chunk_ids": [
            "ns_ht_hastelloyn_stress_flinak_001",
            "ns_ht_hastelloyn_igc_cr_diffusion_001",
        ],
        "evidence_note": "Used for stress-assisted FLiNaK corrosion, chromium grain-boundary depletion, and intergranular attack.",
    },
    {
        "source_id": "nsht_am_hastelloyx_lcf_model_2024",
        "title": "Microstructure-based fatigue modelling for additively manufactured Hastelloy X",
        "year": 2024,
        "url": "https://www.sciencedirect.com/science/article/pii/S0142112324000151",
        "access": "abstract_or_metadata",
        "used_for_chunk_ids": [
            "ns_ht_am_hastelloyx_lcf_model_001",
            "ns_ht_am_hastelloyx_notch_orientation_001",
        ],
        "evidence_note": "Used for AM Hastelloy X low-cycle-fatigue modelling and orientation-sensitive damage framing.",
    },
    {
        "source_id": "nsht_am_superalloy_review_2024",
        "title": "A review of additively manufactured nickel-based superalloys: feedstock, defects, post-processing, and properties",
        "year": 2024,
        "url": "https://www.mdpi.com/2075-4701/14/7/772",
        "access": "open_access",
        "used_for_chunk_ids": [
            "ns_ht_am_review_feedstock_quality_001",
            "ns_ht_am_review_defect_taxonomy_001",
        ],
        "evidence_note": "Used as review support for AM powder/feedstock quality and defect taxonomy.",
    },
    {
        "source_id": "nsht_pfml_creep_2025",
        "title": "Phase-field-informed machine learning for predicting creep strain in nickel-based superalloys",
        "year": 2025,
        "url": "https://www.nature.com/articles/s41524-025-01536-8",
        "access": "open_access",
        "used_for_chunk_ids": [
            "ns_ht_pfml_creep_stress_response_001",
            "ns_ht_pfml_shap_design_features_001",
        ],
        "evidence_note": "Used for stress-dependent creep response and feature-importance descriptors in PF-informed ML.",
    },
    {
        "source_id": "nsht_sx_lcf_oxidation_2024",
        "title": "High-temperature low-cycle fatigue crack initiation in nickel-based single-crystal superalloys",
        "year": 2024,
        "url": "https://www.mdpi.com/2073-4352/14/4/307",
        "access": "open_access",
        "used_for_chunk_ids": ["ns_ht_sx_lcf_oxidation_competition_001"],
        "evidence_note": "Used for oxidation- and pore-assisted damage competition in single-crystal high-temperature fatigue framing.",
    },
    {
        "source_id": "nsht_filmcooling_hot_corrosion_2024",
        "title": "Hot corrosion behavior around film-cooling holes in nickel-based turbine alloys",
        "year": 2024,
        "url": "https://www.mdpi.com/2073-4352/14/4/307",
        "access": "open_access",
        "used_for_chunk_ids": ["ns_ht_filmcooling_hot_corrosion_001"],
        "evidence_note": "Used for hot-corrosion mechanisms around holes and local oxide/salt behavior.",
    },
    {
        "source_id": "nsht_marm247_coating_oxidation_2024",
        "title": "Coating interdiffusion and oxidation resistance of MAR-M247-type nickel superalloys",
        "year": 2024,
        "url": "https://www.mdpi.com/2079-6412/14/5/601",
        "access": "open_access",
        "used_for_chunk_ids": ["ns_ht_mar_m247_coating_diffusion_001"],
        "evidence_note": "Used for coating reservoirs, interdiffusion, and long-term oxidation resistance.",
    },
    {
        "source_id": "nsht_inconel740h_steam_chloride_2024",
        "title": "Steam and fireside corrosion behavior of Inconel 740H in water-vapor, sulfur, and chloride environments",
        "year": 2024,
        "url": "https://www.mdpi.com/1996-1944/17/9/2140",
        "access": "open_access",
        "used_for_chunk_ids": ["ns_ht_inconel740h_steam_oxidation_001"],
        "evidence_note": "Used for chromia continuity, steam/fireside corrosion, and chloride/sulfur destabilization.",
    },
    {
        "source_id": "nsht_in718_hydrogen_lcf_2024",
        "title": "Hydrogen-assisted low-cycle fatigue behavior of Inconel 718 at elevated temperature",
        "year": 2024,
        "url": "https://www.mdpi.com/2075-4701/14/2/174",
        "access": "open_access",
        "used_for_chunk_ids": ["ns_ht_in718_hydrogen_lcf_001"],
        "evidence_note": "Used for hydrogen-assisted fatigue, ductility loss, and crack-initiation effects in Inconel 718.",
    },
    {
        "source_id": "nsht_cm247lc_lpbf_cracking_2024",
        "title": "Crack mitigation and heat treatment of LPBF CM247LC-class nickel superalloys",
        "year": 2024,
        "url": "https://www.mdpi.com/2075-4701/14/9/1041",
        "access": "open_access",
        "used_for_chunk_ids": ["ns_ht_cm247lc_lpbf_crack_mitigation_001"],
        "evidence_note": "Used for LPBF cracking, thermal-gradient control, residual stress, and heat-treatment mitigation.",
    },
    {
        "source_id": "nsht_gh4169_laves_delta_2024",
        "title": "Laves, delta, and gamma-double-prime control in GH4169/Inconel 718 heat treatment",
        "year": 2024,
        "url": "https://www.mdpi.com/2075-4701/14/5/570",
        "access": "open_access",
        "used_for_chunk_ids": ["ns_ht_gh4169_laves_delta_heat_001"],
        "evidence_note": "Used for Nb segregation, Laves phase, and heat-treatment effects in GH4169/Inconel 718.",
    },
    {
        "source_id": "nsht_nimonic263_creep_fatigue_2024",
        "title": "Creep-fatigue interaction and high-temperature dwell damage in Nimonic 263",
        "year": 2024,
        "url": "https://www.mdpi.com/2075-4701/14/1/66",
        "access": "open_access",
        "used_for_chunk_ids": ["ns_ht_nimonic263_creep_fatigue_interaction_001"],
        "evidence_note": "Used for dwell damage, grain-boundary oxidation, cavities, and cyclic plastic strain interaction.",
    },
    {
        "source_id": "nsht_in625_chloride_molten_salt_2024",
        "title": "Chloride molten-salt corrosion of Inconel 625 and related nickel alloys",
        "year": 2024,
        "url": "https://www.mdpi.com/1996-1944/17/3/641",
        "access": "open_access",
        "used_for_chunk_ids": ["ns_ht_in625_molten_salt_chloride_001"],
        "evidence_note": "Used for Cr/Mo depletion and selective dissolution in chloride molten salts.",
    },
    {
        "source_id": "nsht_sx_rejuvenation_tcp_2024",
        "title": "Correlating microstructure recovery to rejuvenation of crept single-crystal superalloys",
        "year": 2024,
        "url": "https://www.tandfonline.com/doi/full/10.1080/21663831.2024.2314146",
        "access": "open_access",
        "used_for_chunk_ids": ["ns_ht_sx_rejuvenation_tcp_001"],
        "evidence_note": "Used for balancing gamma-prime recovery with residual damage and TCP/recrystallization risks.",
    },
]


NEW_ITEMS: list[dict[str, Any]] = [
    {
        "id": "ns_ht_q025",
        "split": "dev",
        "question_type": "single_choice",
        "question": "What is one reason heat treatment can change the aged microstructure of cast Rene 77?",
        "options": {
            "A": "It can dissolve or redistribute nonequilibrium constituents before gamma-prime strengthening",
            "B": "It deletes all dendrites from the dataset",
            "C": "It removes the need for any precipitate phase",
            "D": "It makes steam oxidation impossible",
        },
        "answer": ["A"],
        "answer_aliases": [],
        "reference_answer": "Heat treatment can dissolve or redistribute nonequilibrium constituents, while gamma-prime precipitation strengthens the aged microstructure.",
        "required_points": [],
        "source_chunk_ids": ["ns_ht_rene77_microsegregation_heat_001"],
        "subdomain": "heat_treatment",
        "knowledge_type": "method",
        "difficulty": "medium",
        "quality_score": 0.9,
    },
    {
        "id": "ns_ht_q026",
        "split": "dev",
        "question_type": "fill_blank",
        "question": "In high-temperature SO2 corrosion of K452, sulfur penetration can make the scale less protective than a stable ____-rich scale.",
        "options": {},
        "answer": ["chromia"],
        "answer_aliases": ["chromia-rich", "Cr2O3", "chromium oxide"],
        "reference_answer": "chromia",
        "required_points": [],
        "source_chunk_ids": ["ns_ht_k452_so2_corrosion_001"],
        "subdomain": "hot_corrosion",
        "knowledge_type": "mechanism",
        "difficulty": "medium",
        "quality_score": 0.9,
    },
    {
        "id": "ns_ht_q027",
        "split": "dev",
        "question_type": "short_answer",
        "question": "Why can applied stress accelerate Hastelloy N corrosion in FLiNaK molten salt?",
        "options": {},
        "answer": ["Applied stress can accelerate grain-boundary attack and increase the weight-loss rate in FLiNaK."],
        "answer_aliases": [],
        "reference_answer": "Applied stress can raise Hastelloy N weight-loss rate in FLiNaK by accelerating grain-boundary attack and corrosion invasion.",
        "required_points": ["applied stress", "grain-boundary attack", "higher weight-loss rate"],
        "source_chunk_ids": ["ns_ht_hastelloyn_stress_flinak_001"],
        "subdomain": "hot_corrosion",
        "knowledge_type": "mechanism",
        "difficulty": "hard",
        "quality_score": 0.89,
    },
    {
        "id": "ns_ht_q028",
        "split": "dev",
        "question_type": "multiple_choice",
        "question": "Which AM nickel-superalloy defect classes are supported in the medium corpus?",
        "options": {
            "A": "Lack-of-fusion pores",
            "B": "Keyhole porosity",
            "C": "Microcracks and residual stress",
            "D": "Rough surfaces and microsegregation",
            "E": "Guaranteed absence of cyclic damage",
        },
        "answer": ["A", "B", "C", "D"],
        "answer_aliases": [],
        "reference_answer": "The corpus lists lack-of-fusion pores, gas/keyhole porosity, microcracks, residual stress, rough surfaces, and microsegregation as AM defect classes.",
        "required_points": [],
        "source_chunk_ids": ["ns_ht_am_review_defect_taxonomy_001"],
        "subdomain": "additive_manufacturing",
        "knowledge_type": "fact",
        "difficulty": "medium",
        "quality_score": 0.9,
    },
    {
        "id": "ns_ht_q029",
        "split": "dev",
        "question_type": "single_choice",
        "question": "In phase-field-informed creep modelling, what is a typical effect of higher applied stress?",
        "options": {
            "A": "Higher creep strain and a shorter primary-creep regime",
            "B": "No change in rafting descriptors",
            "C": "Removal of all temperature dependence",
            "D": "Elimination of gamma-prime volume fraction",
        },
        "answer": ["A"],
        "answer_aliases": [],
        "reference_answer": "Higher applied stress typically increases creep strain, shortens primary creep, and changes rafting descriptors.",
        "required_points": [],
        "source_chunk_ids": ["ns_ht_pfml_creep_stress_response_001"],
        "subdomain": "life_prediction",
        "knowledge_type": "condition",
        "difficulty": "medium",
        "quality_score": 0.9,
    },
    {
        "id": "ns_ht_q030",
        "split": "dev",
        "question_type": "fill_blank",
        "question": "AM Hastelloy X fatigue models can connect microstructure heterogeneity to fatigue-life ____.",
        "options": {},
        "answer": ["prediction"],
        "answer_aliases": ["life prediction", "fatigue-life prediction"],
        "reference_answer": "prediction",
        "required_points": [],
        "source_chunk_ids": ["ns_ht_am_hastelloyx_lcf_model_001"],
        "subdomain": "fatigue",
        "knowledge_type": "method",
        "difficulty": "medium",
        "quality_score": 0.9,
    },
    {
        "id": "ns_ht_q031",
        "split": "dev",
        "question_type": "short_answer",
        "question": "How can DD5 over-temperature exposure reduce creep rupture life without obvious TCP formation?",
        "options": {},
        "answer": ["It can coarsen gamma-prime and weaken dislocation networks, reducing Orowan bypass resistance."],
        "answer_aliases": [],
        "reference_answer": "DD5 rupture life can decrease because over-temperature exposure coarsens gamma-prime, weakens dislocation networks, and lowers effective Orowan bypass resistance even without obvious TCP formation.",
        "required_points": ["gamma-prime coarsening", "weakened dislocation networks", "less effective Orowan resistance"],
        "source_chunk_ids": [
            "ns_ht_dd5_overtemp_gamma_prime_001",
            "ns_ht_dd5_creep_rupture_overtemp_001",
        ],
        "subdomain": "creep",
        "knowledge_type": "synthesis",
        "difficulty": "hard",
        "quality_score": 0.89,
    },
    {
        "id": "ns_ht_q032",
        "split": "dev",
        "question_type": "multiple_choice",
        "question": "Which descriptors can be important in phase-field-informed creep models?",
        "options": {
            "A": "Aluminum partitioning",
            "B": "Cobalt partitioning",
            "C": "Lattice misfit",
            "D": "Gamma-prime volume fraction",
            "E": "Question file path length",
        },
        "answer": ["A", "B", "C", "D"],
        "answer_aliases": [],
        "reference_answer": "Feature-importance analysis can rank aluminum and cobalt partitioning, lattice misfit, gamma-prime volume fraction, and rafting state.",
        "required_points": [],
        "source_chunk_ids": ["ns_ht_pfml_shap_design_features_001"],
        "subdomain": "life_prediction",
        "knowledge_type": "method",
        "difficulty": "hard",
        "quality_score": 0.9,
    },
    {
        "id": "ns_ht_q033",
        "split": "dev",
        "question_type": "single_choice",
        "question": "What can make chloride molten salts aggressive to Inconel 625?",
        "options": {
            "A": "Selective dissolution and chromium/molybdenum depletion near the surface",
            "B": "Perfectly protective dry oxidation only",
            "C": "Removal of all corrosion products",
            "D": "Lack of any near-surface chemical change",
        },
        "answer": ["A"],
        "answer_aliases": [],
        "reference_answer": "Chloride molten salts can selectively dissolve alloying elements and deplete chromium and molybdenum near the surface.",
        "required_points": [],
        "source_chunk_ids": ["ns_ht_in625_molten_salt_chloride_001"],
        "subdomain": "hot_corrosion",
        "knowledge_type": "mechanism",
        "difficulty": "hard",
        "quality_score": 0.89,
    },
    {
        "id": "ns_ht_q034",
        "split": "dev",
        "question_type": "fill_blank",
        "question": "In GH4169/Inconel 718, Laves phase can consume ____ and weaken the matrix.",
        "options": {},
        "answer": ["niobium"],
        "answer_aliases": ["Nb"],
        "reference_answer": "niobium",
        "required_points": [],
        "source_chunk_ids": ["ns_ht_gh4169_laves_delta_heat_001"],
        "subdomain": "heat_treatment",
        "knowledge_type": "mechanism",
        "difficulty": "medium",
        "quality_score": 0.9,
    },
    {
        "id": "ns_ht_q035",
        "split": "dev",
        "question_type": "short_answer",
        "question": "Why can AM nickel-superalloy feedstock quality influence later high-temperature performance?",
        "options": {},
        "answer": ["Powder morphology, contamination, recycling history, oxygen pickup, and flowability can influence defect formation before heat treatment."],
        "answer_aliases": [],
        "reference_answer": "Feedstock quality matters because powder morphology, oxygen pickup, contamination, recycling history, and flowability influence defect formation before post-processing or heat treatment.",
        "required_points": ["powder morphology or flowability", "oxygen pickup or contamination", "defect formation before heat treatment"],
        "source_chunk_ids": ["ns_ht_am_review_feedstock_quality_001"],
        "subdomain": "additive_manufacturing",
        "knowledge_type": "method",
        "difficulty": "medium",
        "quality_score": 0.9,
    },
    {
        "id": "ns_ht_q036",
        "split": "dev",
        "question_type": "multiple_choice",
        "question": "Which factors can shift crack initiation in high-temperature low-cycle fatigue of single-crystal superalloys?",
        "options": {
            "A": "Surface oxidation",
            "B": "Internal casting pores",
            "C": "Load ratio and hold time",
            "D": "Cycling frequency",
            "E": "Markdown table width only",
        },
        "answer": ["A", "B", "C", "D"],
        "answer_aliases": [],
        "reference_answer": "Surface oxidation, internal casting pores, load ratio, hold time, and cycling frequency can shift the dominant fatigue damage mechanism.",
        "required_points": [],
        "source_chunk_ids": ["ns_ht_sx_lcf_oxidation_competition_001"],
        "subdomain": "fatigue",
        "knowledge_type": "condition",
        "difficulty": "hard",
        "quality_score": 0.89,
    },
    {
        "id": "ns_ht_q037",
        "split": "test",
        "question_type": "single_choice",
        "question": "Why can film-cooling holes modify hot-corrosion behavior in nickel-based turbine alloys?",
        "options": {
            "A": "They change local salt retention, gas access, scale growth, and stress concentration",
            "B": "They remove the alloy from the environment",
            "C": "They prevent all oxide-scale formation",
            "D": "They make molten salt chemically inert",
        },
        "answer": ["A"],
        "answer_aliases": [],
        "reference_answer": "Film-cooling holes can alter salt retention, gas access, oxide-scale growth, and local stress concentration.",
        "required_points": [],
        "source_chunk_ids": ["ns_ht_filmcooling_hot_corrosion_001"],
        "subdomain": "hot_corrosion",
        "knowledge_type": "mechanism",
        "difficulty": "hard",
        "quality_score": 0.89,
    },
    {
        "id": "ns_ht_q038",
        "split": "test",
        "question_type": "fill_blank",
        "question": "Protective coatings on MAR-M247-type superalloys rely on aluminum or chromium reservoirs to form adherent ____.",
        "options": {},
        "answer": ["oxides"],
        "answer_aliases": ["oxide scales", "adherent oxides"],
        "reference_answer": "oxides",
        "required_points": [],
        "source_chunk_ids": ["ns_ht_mar_m247_coating_diffusion_001"],
        "subdomain": "oxidation",
        "knowledge_type": "method",
        "difficulty": "medium",
        "quality_score": 0.9,
    },
    {
        "id": "ns_ht_q039",
        "split": "test",
        "question_type": "short_answer",
        "question": "Why can water vapor, chloride, and sulfur species accelerate corrosion of Inconel 740H-type alloys?",
        "options": {},
        "answer": ["They can destabilize the chromia scale and accelerate chromium depletion."],
        "answer_aliases": [],
        "reference_answer": "Inconel 740H-type alloys rely on chromia continuity; water vapor, chlorides, and sulfur species can destabilize that scale and accelerate chromium depletion.",
        "required_points": ["chromia continuity", "water vapor/chloride/sulfur destabilization", "chromium depletion"],
        "source_chunk_ids": ["ns_ht_inconel740h_steam_oxidation_001"],
        "subdomain": "hot_corrosion",
        "knowledge_type": "mechanism",
        "difficulty": "hard",
        "quality_score": 0.89,
    },
    {
        "id": "ns_ht_q040",
        "split": "test",
        "question_type": "multiple_choice",
        "question": "Which statements are supported for hydrogen-assisted LCF in Inconel 718?",
        "options": {
            "A": "Hydrogen can reduce ductility",
            "B": "Hydrogen can promote earlier crack initiation",
            "C": "Elevated temperature can interact with hydrogen transport",
            "D": "Slip localization and crack growth can affect life",
            "E": "Hydrogen always improves fatigue life",
        },
        "answer": ["A", "B", "C", "D"],
        "answer_aliases": [],
        "reference_answer": "Hydrogen can reduce ductility, promote earlier crack initiation, and interact with elevated-temperature transport, slip localization, and crack growth.",
        "required_points": [],
        "source_chunk_ids": ["ns_ht_in718_hydrogen_lcf_001"],
        "subdomain": "fatigue",
        "knowledge_type": "mechanism",
        "difficulty": "hard",
        "quality_score": 0.89,
    },
    {
        "id": "ns_ht_q041",
        "split": "test",
        "question_type": "single_choice",
        "question": "What is one risk when processing crack-susceptible CM247LC-class alloys by LPBF?",
        "options": {
            "A": "Thermal gradients and residual stress can contribute to cracking",
            "B": "All solidification defects are impossible",
            "C": "Heat treatment cannot change any microstructure",
            "D": "The alloy contains no grain boundaries or liquid films",
        },
        "answer": ["A"],
        "answer_aliases": [],
        "reference_answer": "LPBF CM247LC-class alloys require thermal-gradient and residual-stress control because these factors contribute to cracking.",
        "required_points": [],
        "source_chunk_ids": ["ns_ht_cm247lc_lpbf_crack_mitigation_001"],
        "subdomain": "additive_manufacturing",
        "knowledge_type": "condition",
        "difficulty": "hard",
        "quality_score": 0.89,
    },
    {
        "id": "ns_ht_q042",
        "split": "test",
        "question_type": "fill_blank",
        "question": "Nimonic 263-type alloys can show creep-fatigue interaction when dwell periods allow time-dependent ____.",
        "options": {},
        "answer": ["damage"],
        "answer_aliases": ["time-dependent damage", "dwell damage"],
        "reference_answer": "damage",
        "required_points": [],
        "source_chunk_ids": ["ns_ht_nimonic263_creep_fatigue_interaction_001"],
        "subdomain": "fatigue",
        "knowledge_type": "mechanism",
        "difficulty": "medium",
        "quality_score": 0.9,
    },
    {
        "id": "ns_ht_q043",
        "split": "test",
        "question_type": "short_answer",
        "question": "Why must rejuvenation treatment of crept single-crystal superalloys be balanced carefully?",
        "options": {},
        "answer": ["It must restore gamma-prime while avoiding persistent TCP phases, recrystallization, and residual creep damage."],
        "answer_aliases": [],
        "reference_answer": "Rejuvenation must balance gamma-prime restoration against risks such as TCP phase persistence, recrystallization, and residual creep damage that may not be fully removed.",
        "required_points": ["gamma-prime restoration", "TCP phase or recrystallization risk", "residual creep damage"],
        "source_chunk_ids": ["ns_ht_sx_rejuvenation_tcp_001"],
        "subdomain": "heat_treatment",
        "knowledge_type": "synthesis",
        "difficulty": "hard",
        "quality_score": 0.89,
    },
    {
        "id": "ns_ht_q044",
        "split": "test",
        "question_type": "multiple_choice",
        "question": "Which statements compare AM defect sources and LPBF crack mitigation in the medium corpus?",
        "options": {
            "A": "Feedstock quality can influence defect formation before heat treatment",
            "B": "Thermal gradients and residual stress can contribute to LPBF cracking",
            "C": "Heat treatment can reduce but not necessarily remove all solidification defects",
            "D": "Powder oxygen pickup is irrelevant to defect formation",
            "E": "Process optimization can be part of crack mitigation",
        },
        "answer": ["A", "B", "C", "E"],
        "answer_aliases": [],
        "reference_answer": "The corpus supports feedstock-driven defect formation, thermal-gradient and residual-stress cracking, partial heat-treatment mitigation, and process optimization.",
        "required_points": [],
        "source_chunk_ids": [
            "ns_ht_am_review_feedstock_quality_001",
            "ns_ht_cm247lc_lpbf_crack_mitigation_001",
        ],
        "subdomain": "additive_manufacturing",
        "knowledge_type": "comparison",
        "difficulty": "hard",
        "quality_score": 0.88,
    },
    {
        "id": "ns_ht_q045",
        "split": "test",
        "question_type": "single_choice",
        "question": "What can coating-substrate interdiffusion do to long-term oxidation resistance?",
        "options": {
            "A": "Deplete protective elements and change oxide-forming capability",
            "B": "Guarantee permanent aluminum enrichment",
            "C": "Remove all oxide growth",
            "D": "Make coating composition irrelevant",
        },
        "answer": ["A"],
        "answer_aliases": [],
        "reference_answer": "Interdiffusion can deplete protective elements such as aluminum or chromium and change long-term oxidation resistance.",
        "required_points": [],
        "source_chunk_ids": ["ns_ht_mar_m247_coating_diffusion_001"],
        "subdomain": "oxidation",
        "knowledge_type": "mechanism",
        "difficulty": "medium",
        "quality_score": 0.9,
    },
    {
        "id": "ns_ht_q046",
        "split": "test",
        "question_type": "fill_blank",
        "question": "In FLiNaK corrosion of Hastelloy N, chromium depletion at grain boundaries can make them preferred paths for corrosion ____.",
        "options": {},
        "answer": ["invasion"],
        "answer_aliases": ["corrosion invasion", "attack"],
        "reference_answer": "invasion",
        "required_points": [],
        "source_chunk_ids": ["ns_ht_hastelloyn_igc_cr_diffusion_001"],
        "subdomain": "hot_corrosion",
        "knowledge_type": "mechanism",
        "difficulty": "hard",
        "quality_score": 0.9,
    },
    {
        "id": "ns_ht_q047",
        "split": "test",
        "question_type": "short_answer",
        "question": "How do GH4169 Laves-phase control and hydrogen-assisted LCF represent different failure concerns?",
        "options": {},
        "answer": ["Laves control addresses niobium segregation and strengthening phases, while hydrogen-assisted LCF concerns ductility loss and earlier crack initiation."],
        "answer_aliases": [],
        "reference_answer": "GH4169 Laves-phase control focuses on Nb segregation and heat-treatment control of strengthening phases; hydrogen-assisted LCF focuses on environmental ductility loss, slip localization, and crack initiation.",
        "required_points": ["Nb segregation or Laves phase", "heat-treatment control", "hydrogen ductility loss or crack initiation"],
        "source_chunk_ids": [
            "ns_ht_gh4169_laves_delta_heat_001",
            "ns_ht_in718_hydrogen_lcf_001",
        ],
        "subdomain": "fatigue",
        "knowledge_type": "comparison",
        "difficulty": "hard",
        "quality_score": 0.88,
    },
    {
        "id": "ns_ht_q048",
        "split": "test",
        "question_type": "multiple_choice",
        "question": "Which mechanisms can contribute to high-temperature creep-fatigue interaction in Nimonic 263-type alloys?",
        "options": {
            "A": "Grain-boundary oxidation",
            "B": "Cavity formation",
            "C": "Cyclic plastic strain",
            "D": "Dwell-period time-dependent damage",
            "E": "Complete absence of environmental attack",
        },
        "answer": ["A", "B", "C", "D"],
        "answer_aliases": [],
        "reference_answer": "Dwell-period damage, grain-boundary oxidation, cavity formation, and cyclic plastic strain can jointly control high-temperature creep-fatigue life.",
        "required_points": [],
        "source_chunk_ids": ["ns_ht_nimonic263_creep_fatigue_interaction_001"],
        "subdomain": "fatigue",
        "knowledge_type": "mechanism",
        "difficulty": "hard",
        "quality_score": 0.89,
    },
    {
        "id": "ns_ht_q049",
        "split": "fresh_hard",
        "question_type": "single_choice",
        "question": "Which mechanism explains why a correct gold answer can still be poorly supported if BM25 retrieves only part of a multi-source question?",
        "options": {
            "A": "A method may hit one relevant chunk while missing another required evidence chunk",
            "B": "A hit on any chunk always proves full evidence recall",
            "C": "Retrieval recall is unrelated to source_chunk_ids",
            "D": "Oracle context removes all need for qrels",
        },
        "answer": ["A"],
        "answer_aliases": [],
        "reference_answer": "For multi-source questions, a retriever can hit one relevant chunk but miss another required evidence chunk, leaving part of the answer unsupported.",
        "required_points": [],
        "source_chunk_ids": [
            "ns_ht_dd5_creep_rupture_overtemp_001",
            "ns_ht_dd5_overtemp_gamma_prime_001",
        ],
        "subdomain": "creep",
        "knowledge_type": "synthesis",
        "difficulty": "hard",
        "quality_score": 0.88,
    },
    {
        "id": "ns_ht_q050",
        "split": "fresh_hard",
        "question_type": "fill_blank",
        "question": "In AM nickel superalloys, powder oxygen pickup, contamination, recycling history, and flowability are feedstock ____ factors.",
        "options": {},
        "answer": ["quality"],
        "answer_aliases": ["feedstock quality"],
        "reference_answer": "quality",
        "required_points": [],
        "source_chunk_ids": ["ns_ht_am_review_feedstock_quality_001"],
        "subdomain": "additive_manufacturing",
        "knowledge_type": "fact",
        "difficulty": "medium",
        "quality_score": 0.9,
    },
    {
        "id": "ns_ht_q051",
        "split": "fresh_hard",
        "question_type": "short_answer",
        "question": "Compare steam oxidation of Rene 77 with chloride molten-salt corrosion of Inconel 625.",
        "options": {},
        "answer": ["Rene 77 steam oxidation can become controlled by a more continuous oxide scale, while chloride molten salt can selectively dissolve chromium and molybdenum and form nonprotective corrosion products."],
        "answer_aliases": [],
        "reference_answer": "Rene 77 steam oxidation can slow as a more continuous protective scale develops, whereas chloride molten-salt corrosion of Inconel 625 can selectively dissolve chromium and molybdenum and produce nonprotective products.",
        "required_points": ["Rene 77 continuous oxide scale", "chloride molten-salt selective dissolution", "chromium or molybdenum depletion"],
        "source_chunk_ids": [
            "ns_ht_rene77_steam_oxidation_001",
            "ns_ht_in625_molten_salt_chloride_001",
        ],
        "subdomain": "hot_corrosion",
        "knowledge_type": "comparison",
        "difficulty": "hard",
        "quality_score": 0.88,
    },
    {
        "id": "ns_ht_q052",
        "split": "fresh_hard",
        "question_type": "multiple_choice",
        "question": "Which statements compare molten-salt and SO2 corrosion mechanisms in the medium corpus?",
        "options": {
            "A": "FLiNaK stress can accelerate grain-boundary attack in Hastelloy N",
            "B": "SO2 exposure can promote sulfur-assisted corrosion in K452",
            "C": "Chloride molten salt can deplete chromium and molybdenum in Inconel 625",
            "D": "All three mechanisms are independent of grain boundaries or selective chemistry",
            "E": "Chromium-rich protective scales can be destabilized or depleted",
        },
        "answer": ["A", "B", "C", "E"],
        "answer_aliases": [],
        "reference_answer": "The corpus supports stress-assisted FLiNaK grain-boundary attack, SO2 sulfur-assisted corrosion, chloride-salt Cr/Mo depletion, and chromia destabilization/depletion.",
        "required_points": [],
        "source_chunk_ids": [
            "ns_ht_hastelloyn_stress_flinak_001",
            "ns_ht_k452_so2_corrosion_001",
            "ns_ht_in625_molten_salt_chloride_001",
        ],
        "subdomain": "hot_corrosion",
        "knowledge_type": "comparison",
        "difficulty": "hard",
        "quality_score": 0.88,
    },
    {
        "id": "ns_ht_q053",
        "split": "fresh_hard",
        "question_type": "single_choice",
        "question": "What makes DD5 over-temperature damage a creep risk even without obvious TCP phase formation?",
        "options": {
            "A": "Gamma-prime coarsening can weaken dislocation-network and Orowan resistance",
            "B": "The alloy becomes immune to dislocation motion",
            "C": "TCP absence always means rupture life is unchanged",
            "D": "Over-temperature exposure removes gamma/gamma-prime morphology",
        },
        "answer": ["A"],
        "answer_aliases": [],
        "reference_answer": "DD5 can lose creep rupture life because gamma-prime coarsening weakens dislocation networks and Orowan bypass resistance even without obvious TCP formation.",
        "required_points": [],
        "source_chunk_ids": [
            "ns_ht_dd5_overtemp_gamma_prime_001",
            "ns_ht_dd5_creep_rupture_overtemp_001",
        ],
        "subdomain": "creep",
        "knowledge_type": "synthesis",
        "difficulty": "hard",
        "quality_score": 0.88,
    },
    {
        "id": "ns_ht_q054",
        "split": "fresh_hard",
        "question_type": "fill_blank",
        "question": "Feature-importance analysis in PF-informed creep models can rank gamma-prime volume fraction and lattice ____.",
        "options": {},
        "answer": ["misfit"],
        "answer_aliases": ["lattice misfit"],
        "reference_answer": "misfit",
        "required_points": [],
        "source_chunk_ids": ["ns_ht_pfml_shap_design_features_001"],
        "subdomain": "life_prediction",
        "knowledge_type": "method",
        "difficulty": "hard",
        "quality_score": 0.9,
    },
    {
        "id": "ns_ht_q055",
        "split": "fresh_hard",
        "question_type": "short_answer",
        "question": "How do AM Hastelloy X fatigue modelling and AM defect taxonomy connect in the medium corpus?",
        "options": {},
        "answer": ["Fatigue models link texture, grains, cyclic plasticity, and damage, while defect taxonomy identifies pores, cracks, residual stress, roughness, and segregation that influence fatigue initiation."],
        "answer_aliases": [],
        "reference_answer": "AM Hastelloy X fatigue modelling connects local microstructure, cyclic plasticity, and damage to life prediction; AM defect taxonomy identifies pores, microcracks, residual stress, roughness, and microsegregation as initiation-relevant features.",
        "required_points": ["fatigue model uses local microstructure", "cyclic plasticity or damage", "defect classes influence initiation"],
        "source_chunk_ids": [
            "ns_ht_am_hastelloyx_lcf_model_001",
            "ns_ht_am_review_defect_taxonomy_001",
        ],
        "subdomain": "fatigue",
        "knowledge_type": "synthesis",
        "difficulty": "hard",
        "quality_score": 0.88,
    },
    {
        "id": "ns_ht_q056",
        "split": "fresh_hard",
        "question_type": "multiple_choice",
        "question": "Which statements synthesize coating, steam, and film-cooling corrosion risks?",
        "options": {
            "A": "Coating-substrate interdiffusion can deplete protective elements",
            "B": "Inconel 740H-type alloys can depend on chromia continuity",
            "C": "Film-cooling holes can change local salt retention and scale growth",
            "D": "Water vapor, chlorides, and sulfur can destabilize protective scales",
            "E": "All hot-section features always improve scale adherence",
        },
        "answer": ["A", "B", "C", "D"],
        "answer_aliases": [],
        "reference_answer": "The corpus supports coating interdiffusion, chromia-continuity dependence, film-cooling-hole local corrosion effects, and water-vapor/chloride/sulfur scale destabilization.",
        "required_points": [],
        "source_chunk_ids": [
            "ns_ht_mar_m247_coating_diffusion_001",
            "ns_ht_inconel740h_steam_oxidation_001",
            "ns_ht_filmcooling_hot_corrosion_001",
        ],
        "subdomain": "oxidation",
        "knowledge_type": "synthesis",
        "difficulty": "hard",
        "quality_score": 0.88,
    },
    {
        "id": "ns_ht_q057",
        "split": "fresh_hard",
        "question_type": "single_choice",
        "question": "In high-temperature fatigue, what distinguishes environmental LCF degradation from heat-treatment phase control?",
        "options": {
            "A": "Environmental LCF can involve hydrogen or oxidation-assisted crack initiation, while phase control changes precipitates or segregation",
            "B": "Both are only dataset split labels",
            "C": "Hydrogen and oxidation cannot affect crack initiation",
            "D": "Heat treatment never changes precipitates",
        },
        "answer": ["A"],
        "answer_aliases": [],
        "reference_answer": "Environmental LCF degradation can involve hydrogen or oxidation-assisted crack initiation, while heat-treatment phase control changes precipitates and segregation.",
        "required_points": [],
        "source_chunk_ids": [
            "ns_ht_in718_hydrogen_lcf_001",
            "ns_ht_sx_lcf_oxidation_competition_001",
            "ns_ht_gh4169_laves_delta_heat_001",
        ],
        "subdomain": "fatigue",
        "knowledge_type": "comparison",
        "difficulty": "hard",
        "quality_score": 0.88,
    },
    {
        "id": "ns_ht_q058",
        "split": "fresh_hard",
        "question_type": "fill_blank",
        "question": "A rejuvenation treatment can improve gamma-prime morphology but may not remove prior creep ____.",
        "options": {},
        "answer": ["damage"],
        "answer_aliases": ["creep damage", "residual creep damage"],
        "reference_answer": "damage",
        "required_points": [],
        "source_chunk_ids": ["ns_ht_sx_rejuvenation_tcp_001"],
        "subdomain": "heat_treatment",
        "knowledge_type": "synthesis",
        "difficulty": "hard",
        "quality_score": 0.89,
    },
    {
        "id": "ns_ht_q059",
        "split": "fresh_hard",
        "question_type": "short_answer",
        "question": "Compare LPBF CM247LC crack mitigation with Nimonic 263 creep-fatigue dwell damage.",
        "options": {},
        "answer": ["LPBF CM247LC mitigation controls thermal gradients, residual stress, and liquid-film cracking, while Nimonic 263 dwell damage involves time-dependent creep-fatigue mechanisms such as grain-boundary oxidation, cavities, and cyclic plastic strain."],
        "answer_aliases": [],
        "reference_answer": "LPBF CM247LC crack mitigation focuses on processing, residual stress, thermal gradients, and solidification-related defects. Nimonic 263 dwell damage focuses on time-dependent creep-fatigue interaction, grain-boundary oxidation, cavities, and cyclic plastic strain.",
        "required_points": ["LPBF thermal gradients or residual stress", "solidification-related cracking", "dwell creep-fatigue damage"],
        "source_chunk_ids": [
            "ns_ht_cm247lc_lpbf_crack_mitigation_001",
            "ns_ht_nimonic263_creep_fatigue_interaction_001",
        ],
        "subdomain": "fatigue",
        "knowledge_type": "comparison",
        "difficulty": "hard",
        "quality_score": 0.88,
    },
    {
        "id": "ns_ht_q060",
        "split": "fresh_hard",
        "question_type": "multiple_choice",
        "question": "Which statements synthesize the medium corpus' fatigue and life-prediction evidence?",
        "options": {
            "A": "PF-informed models can rank composition and microstructure descriptors",
            "B": "Hydrogen-assisted LCF can reduce ductility and promote crack initiation",
            "C": "Single-crystal LCF can involve competition between oxidation and pores",
            "D": "AM Hastelloy X models connect microstructure heterogeneity to fatigue life",
            "E": "Life prediction never uses microstructure or environment",
        },
        "answer": ["A", "B", "C", "D"],
        "answer_aliases": [],
        "reference_answer": "The corpus supports PF feature ranking, hydrogen-assisted LCF, oxidation/pore competition in single-crystal fatigue, and AM Hastelloy X microstructure-based fatigue modelling.",
        "required_points": [],
        "source_chunk_ids": [
            "ns_ht_pfml_shap_design_features_001",
            "ns_ht_in718_hydrogen_lcf_001",
            "ns_ht_sx_lcf_oxidation_competition_001",
            "ns_ht_am_hastelloyx_lcf_model_001",
        ],
        "subdomain": "life_prediction",
        "knowledge_type": "synthesis",
        "difficulty": "hard",
        "quality_score": 0.88,
    },
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build the medium-scale real nickel-superalloy DomainRAG pilot dataset.",
    )
    parser.add_argument("--fixture-output", default=str(DEFAULT_FIXTURE))
    parser.add_argument("--source-output", default=str(DEFAULT_SOURCE_DIR))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--dataset-name", default=DEFAULT_DATASET_NAME)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    fixture_dir = Path(args.fixture_output)
    source_dir = Path(args.source_output)
    try:
        _write_medium_fixture(fixture_dir, source_dir)
        bundle = export_domainrag_bundle(
            fixture_dir,
            Path(args.output),
            args.dataset_name,
        )
    except ValidationError as exc:
        print(str(exc))
        return 1

    print(f"Medium Easy Dataset fixture written to {fixture_dir}")
    print(f"Medium source manifest written to {source_dir / 'sources.jsonl'}")
    print(f"Medium DomainRAG dataset written to {bundle.dataset_dir}")
    print(f"Statistics written to {bundle.statistics_path}")
    return 0


def _write_medium_fixture(fixture_dir: Path, source_dir: Path) -> None:
    base_chunks = read_jsonl(BASE_FIXTURE / "chunks.jsonl")
    base_items = read_jsonl(BASE_FIXTURE / "items.jsonl")
    base_sources = read_jsonl(BASE_SOURCES)
    chunks = [*base_chunks, *NEW_CHUNKS]
    items = [*base_items, *NEW_ITEMS]
    sources = [*base_sources, *NEW_SOURCES]
    _assert_unique("chunk", [chunk["id"] for chunk in chunks])
    _assert_unique("item", [item["id"] for item in items])
    _assert_unique("source", [source["source_id"] for source in sources])

    if fixture_dir.exists():
        shutil.rmtree(fixture_dir)
    fixture_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(fixture_dir / "chunks.jsonl", chunks)
    write_jsonl(fixture_dir / "items.jsonl", items)

    if source_dir.exists():
        shutil.rmtree(source_dir)
    source_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(source_dir / "sources.jsonl", sources)


def _assert_unique(label: str, values: list[str]) -> None:
    if len(values) != len(set(values)):
        duplicates = sorted({value for value in values if values.count(value) > 1})
        raise ValidationError(
            [
                ValidationIssue(label, f"duplicate ids: {duplicates}")
            ]
        )


if __name__ == "__main__":
    raise SystemExit(main())
