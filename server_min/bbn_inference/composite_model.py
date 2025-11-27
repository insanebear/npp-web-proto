import pymc as pm

from .bbn_parameter import *
from .bbn_utils import from_posterior

def create_SR_Dev_model(attr_states):
    model = pm.Model()

    with model:
        # Dev Attribute model - Requirement phase
        # prior probability of Dev quality in SR phase
        SR_DevH_prior = pm.Beta("SR_DevH_prior", alpha=4.42, beta=22.04)
        SR_DevM_prior = pm.Beta("SR_DevM_prior", alpha=4.47, beta=2.73)
        SR_DevL_prior = pm.Beta("SR_DevL_prior", alpha=1.25, beta=4.49)
        # Attribute Software Development Planning
        SR_SDP_DevH_like = pm.TruncatedNormal("SR_SDP_DevH_like",
                                            mu=SR_SDP_DevH_npt[attr_states["SR_SDP_state"]][0], sigma=SR_SDP_DevH_npt[attr_states["SR_SDP_state"]][1],
                                            lower=0, upper=1)
        SR_SDP_DevM_like = pm.TruncatedNormal("SR_SDP_DevM_like",
                                            mu=SR_SDP_DevM_npt[attr_states["SR_SDP_state"]][0], sigma=SR_SDP_DevM_npt[attr_states["SR_SDP_state"]][1],
                                            lower=0, upper=1)
        SR_SDP_DevL_like = pm.TruncatedNormal("SR_SDP_DevL_like",
                                            mu=SR_SDP_DevL_npt[attr_states["SR_SDP_state"]][0], sigma=SR_SDP_DevL_npt[attr_states["SR_SDP_state"]][1],
                                            lower=0, upper=1)
        # Attribute Document of a Concept Documentation
        SR_CD_DevH_like = pm.TruncatedNormal("SR_CD_DevH_like",
                                            mu=SR_CD_DevH_npt[attr_states["SR_CD_state"]][0], sigma=SR_CD_DevH_npt[attr_states["SR_CD_state"]][1],
                                            lower=0, upper=1)
        SR_CD_DevM_like = pm.TruncatedNormal("SR_CD_DevM_like",
                                            mu=SR_CD_DevM_npt[attr_states["SR_CD_state"]][0], sigma=SR_CD_DevM_npt[attr_states["SR_CD_state"]][1],
                                            lower=0, upper=1)
        SR_CD_DevL_like = pm.TruncatedNormal("SR_CD_DevL_like",
                                            mu=SR_CD_DevL_npt[attr_states["SR_CD_state"]][0], sigma=SR_CD_DevL_npt[attr_states["SR_CD_state"]][1],
                                            lower=0, upper=1)
        # Attribute Document of Software Requirements Specifications
        SR_SRS_DevH_like = pm.TruncatedNormal("SR_SRS_DevH_like",
                                            mu=SR_SRS_DevH_npt[attr_states["SR_SRS_state"]][0], sigma=SR_SRS_DevH_npt[attr_states["SR_SRS_state"]][1],
                                            lower=0, upper=1)
        SR_SRS_DevM_like = pm.TruncatedNormal("SR_SRS_DevM_like",
                                            mu=SR_SRS_DevM_npt[attr_states["SR_SRS_state"]][0], sigma=SR_SRS_DevM_npt[attr_states["SR_SRS_state"]][1],
                                            lower=0, upper=1)
        SR_SRS_DevL_like = pm.TruncatedNormal("SR_SRS_DevL_like",
                                            mu=SR_SRS_DevL_npt[attr_states["SR_SRS_state"]][0], sigma=SR_SRS_DevL_npt[attr_states["SR_SRS_state"]][1],
                                            lower=0, upper=1)
        # Attribute Traceability Analysis
        SR_TA_DevH_like = pm.TruncatedNormal("SR_TA_DevH_like",
                                            mu=SR_TA_DevH_npt[attr_states["SR_TA_state"]][0], sigma=SR_TA_DevH_npt[attr_states["SR_TA_state"]][1],
                                            lower=0, upper=1)
        SR_TA_DevM_like = pm.TruncatedNormal("SR_TA_DevM_like",
                                            mu=SR_TA_DevM_npt[attr_states["SR_TA_state"]][0], sigma=SR_TA_DevM_npt[attr_states["SR_TA_state"]][1],
                                            lower=0, upper=1)
        SR_TA_DevL_like = pm.TruncatedNormal("SR_TA_DevL_like",
                                            mu=SR_TA_DevL_npt[attr_states["SR_TA_state"]][0], sigma=SR_TA_DevL_npt[attr_states["SR_TA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Criticality Analysis
        SR_CA_DevH_like = pm.TruncatedNormal("SR_CA_DevH_like",
                                            mu=SR_CA_DevH_npt[attr_states["SR_CA_state"]][0], sigma=SR_CA_DevH_npt[attr_states["SR_CA_state"]][1],
                                            lower=0, upper=1)
        SR_CA_DevM_like = pm.TruncatedNormal("SR_CA_DevM_like",
                                            mu=SR_CA_DevM_npt[attr_states["SR_CA_state"]][0], sigma=SR_CA_DevM_npt[attr_states["SR_CA_state"]][1],
                                            lower=0, upper=1)
        SR_CA_DevL_like = pm.TruncatedNormal("SR_CA_DevL_like",
                                            mu=SR_CA_DevL_npt[attr_states["SR_CA_state"]][0], sigma=SR_CA_DevL_npt[attr_states["SR_CA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Hazard Analysis
        SR_HA_DevH_like = pm.TruncatedNormal("SR_HA_DevH_like",
                                            mu=SR_HA_DevH_npt[attr_states["SR_HA_state"]][0], sigma=SR_HA_DevH_npt[attr_states["SR_HA_state"]][1],
                                            lower=0, upper=1)
        SR_HA_DevM_like = pm.TruncatedNormal("SR_HA_DevM_like",
                                            mu=SR_HA_DevM_npt[attr_states["SR_HA_state"]][0], sigma=SR_HA_DevM_npt[attr_states["SR_HA_state"]][1],
                                            lower=0, upper=1)
        SR_HA_DevL_like = pm.TruncatedNormal("SR_HA_DevL_like",
                                            mu=SR_HA_DevL_npt[attr_states["SR_HA_state"]][0], sigma=SR_HA_DevL_npt[attr_states["SR_HA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Security Analysis
        SR_SA_DevH_like = pm.TruncatedNormal("SR_SA_DevH_like",
                                            mu=SR_SA_DevH_npt[attr_states["SR_SA_state"]][0], sigma=SR_SA_DevH_npt[attr_states["SR_SA_state"]][1],
                                            lower=0, upper=1)
        SR_SA_DevM_like = pm.TruncatedNormal("SR_SA_DevM_like",
                                            mu=SR_SA_DevM_npt[attr_states["SR_SA_state"]][0], sigma=SR_SA_DevM_npt[attr_states["SR_SA_state"]][1],
                                            lower=0, upper=1)
        SR_SA_DevL_like = pm.TruncatedNormal("SR_SA_DevL_like",
                                            mu=SR_SA_DevL_npt[attr_states["SR_SA_state"]][0], sigma=SR_SA_DevL_npt[attr_states["SR_SA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Risk Analysis
        SR_RA_DevH_like = pm.TruncatedNormal("SR_RA_DevH_like",
                                            mu=SR_RA_DevH_npt[attr_states["SR_RA_state"]][0], sigma=SR_RA_DevH_npt[attr_states["SR_RA_state"]][1],
                                            lower=0, upper=1)
        SR_RA_DevM_like = pm.TruncatedNormal("SR_RA_DevM_like",
                                            mu=SR_RA_DevM_npt[attr_states["SR_RA_state"]][0], sigma=SR_RA_DevM_npt[attr_states["SR_RA_state"]][1],
                                            lower=0, upper=1)
        SR_RA_DevL_like = pm.TruncatedNormal("SR_RA_DevL_like",
                                            mu=SR_RA_DevL_npt[attr_states["SR_RA_state"]][0], sigma=SR_RA_DevL_npt[attr_states["SR_RA_state"]][1],
                                            lower=0, upper=1)
        # Attribute System/Software Qualification Test Plan Generation
        SR_SQTPG_DevH_like = pm.TruncatedNormal("SR_SQTPG_DevH_like",
                                                mu=SR_SQTPG_DevH_npt[attr_states["SR_SQTPG_state"]][0], sigma=SR_SQTPG_DevH_npt[attr_states["SR_SQTPG_state"]][1],
                                                lower=0, upper=1)
        SR_SQTPG_DevM_like = pm.TruncatedNormal("SR_SQTPG_DevM_like",
                                                mu=SR_SQTPG_DevM_npt[attr_states["SR_SQTPG_state"]][0], sigma=SR_SQTPG_DevM_npt[attr_states["SR_SQTPG_state"]][1],
                                                lower=0, upper=1)
        SR_SQTPG_DevL_like = pm.TruncatedNormal("SR_SQTPG_DevL_like",
                                                mu=SR_SQTPG_DevL_npt[attr_states["SR_SQTPG_state"]][0], sigma=SR_SQTPG_DevL_npt[attr_states["SR_SQTPG_state"]][1],
                                                lower=0, upper=1)
        # Attribute System/Software Acceptance Test Plan Generation
        SR_SATPG_DevH_like = pm.TruncatedNormal("SR_SATPG_DevH_like",
                                                mu=SR_SATPG_DevH_npt[attr_states["SR_SATPG_state"]][0], sigma=SR_SATPG_DevH_npt[attr_states["SR_SATPG_state"]][1],
                                                lower=0, upper=1)
        SR_SATPG_DevM_like = pm.TruncatedNormal("SR_SATPG_DevM_like",
                                                mu=SR_SATPG_DevM_npt[attr_states["SR_SATPG_state"]][0], sigma=SR_SATPG_DevM_npt[attr_states["SR_SATPG_state"]][1],
                                                lower=0, upper=1)
        SR_SATPG_DevL_like = pm.TruncatedNormal("SR_SATPG_DevL_like",
                                                mu=SR_SATPG_DevL_npt[attr_states["SR_SATPG_state"]][0], sigma=SR_SATPG_DevL_npt[attr_states["SR_SATPG_state"]][1],
                                                lower=0, upper=1)
        # Attribute Configuration Management
        SR_CM_DevH_like = pm.TruncatedNormal("SR_CM_DevH_like",
                                            mu=SR_CM_DevH_npt[attr_states["SR_CM_state"]][0], sigma=SR_CM_DevH_npt[attr_states["SR_CM_state"]][1],
                                            lower=0, upper=1)
        SR_CM_DevM_like = pm.TruncatedNormal("SR_CM_DevM_like",
                                            mu=SR_CM_DevM_npt[attr_states["SR_CM_state"]][0], sigma=SR_CM_DevM_npt[attr_states["SR_CM_state"]][1],
                                            lower=0, upper=1)
        SR_CM_DevL_like = pm.TruncatedNormal("SR_CM_DevL_like",
                                            mu=SR_CM_DevL_npt[attr_states["SR_CM_state"]][0], sigma=SR_CM_DevL_npt[attr_states["SR_CM_state"]][1],
                                            lower=0, upper=1)
        # Attribute Review and Audit
        SR_RaA_DevH_like = pm.TruncatedNormal("SR_RaA_DevH_like",
                                            mu=SR_RaA_DevH_npt[attr_states["SR_RaA_state"]][0], sigma=SR_RaA_DevH_npt[attr_states["SR_RaA_state"]][1],
                                            lower=0, upper=1)
        SR_RaA_DevM_like = pm.TruncatedNormal("SR_RaA_DevM_like",
                                            mu=SR_RaA_DevM_npt[attr_states["SR_RaA_state"]][0], sigma=SR_RaA_DevM_npt[attr_states["SR_RaA_state"]][1],
                                            lower=0, upper=1)
        SR_RaA_DevL_like = pm.TruncatedNormal("SR_RaA_DevL_like",
                                            mu=SR_RaA_DevL_npt[attr_states["SR_RaA_state"]][0], sigma=SR_RaA_DevL_npt[attr_states["SR_RaA_state"]][1],
                                            lower=0, upper=1)
        # m1-m3: a part of marginal probability
        # m1 = P(Dev=H)P(attribute states|Dev=H)
        # m2 = P(Dev=M)P(attribute states|Dev=M)
        # m3 = P(Dev=L)P(attribute states|Dev=L)
        SR_Dev_m1 = SR_DevH_prior * SR_SDP_DevH_like * SR_CD_DevH_like * SR_SRS_DevH_like * SR_TA_DevH_like * SR_CA_DevH_like * SR_HA_DevH_like * SR_SA_DevH_like * SR_RA_DevH_like * SR_SQTPG_DevH_like * SR_SATPG_DevH_like * SR_CM_DevH_like * SR_RaA_DevH_like
        SR_Dev_m2 = SR_DevM_prior * SR_SDP_DevM_like * SR_CD_DevM_like * SR_SRS_DevM_like * SR_TA_DevM_like * SR_CA_DevM_like * SR_HA_DevM_like * SR_SA_DevM_like * SR_RA_DevM_like * SR_SQTPG_DevM_like * SR_SATPG_DevM_like * SR_CM_DevM_like * SR_RaA_DevM_like
        SR_Dev_m3 = SR_DevL_prior * SR_SDP_DevL_like * SR_CD_DevL_like * SR_SRS_DevL_like * SR_TA_DevL_like * SR_CA_DevL_like * SR_HA_DevL_like * SR_SA_DevL_like * SR_RA_DevL_like * SR_SQTPG_DevL_like * SR_SATPG_DevL_like * SR_CM_DevL_like * SR_RaA_DevL_like

        # k = 1 / marginal probability
        SR_Dev_k = 1 / (SR_Dev_m1 + SR_Dev_m2 + SR_Dev_m3)

        # posterior probability of Dev quality in SR phase
        SR_DevH_post = pm.Deterministic("SR_DevH_post", SR_Dev_k * SR_Dev_m1)
        SR_DevM_post = pm.Deterministic("SR_DevM_post", SR_Dev_k * SR_Dev_m2)
        SR_DevL_post = pm.Deterministic("SR_DevL_post", SR_Dev_k * SR_Dev_m3)
    return model

def create_SR_VV_model(attr_states):
    model = pm.Model()

    with model:
        # V&V Attribute model - Requirement phase
        # prior probability of V&V quality in SR phase
        SR_VVH_prior = pm.Beta("SR_VVH_prior", alpha=0.67, beta=3.23)
        SR_VVM_prior = pm.Beta("SR_VVM_prior", alpha=3.21, beta=2.21)
        SR_VVL_prior = pm.Beta("SR_VVL_prior", alpha=2.10, beta=7.19)
        # Attribute Software V&V Planning
        SR_SVVP_VVH_like = pm.TruncatedNormal("SR_SVVP_VVH_like",
                                            mu=SR_SVVP_VVH_npt[attr_states["SR_SVVP_state"]][0], sigma=SR_SVVP_VVH_npt[attr_states["SR_SVVP_state"]][1],
                                            lower=0, upper=1)
        SR_SVVP_VVM_like = pm.TruncatedNormal("SR_SVVP_VVM_like",
                                            mu=SR_SVVP_VVM_npt[attr_states["SR_SVVP_state"]][0], sigma=SR_SVVP_VVM_npt[attr_states["SR_SVVP_state"]][1],
                                            lower=0, upper=1)
        SR_SVVP_VVL_like = pm.TruncatedNormal("SR_SVVP_VVL_like",
                                            mu=SR_SVVP_VVL_npt[attr_states["SR_SVVP_state"]][0], sigma=SR_SVVP_VVL_npt[attr_states["SR_SVVP_state"]][1],
                                            lower=0, upper=1)
        # Attribute Concept Documentation Evaluation
        SR_CDE_VVH_like = pm.TruncatedNormal("SR_CDE_VVH_like",
                                            mu=SR_CDE_VVH_npt[attr_states["SR_CDE_state"]][0], sigma=SR_CDE_VVH_npt[attr_states["SR_CDE_state"]][1],
                                            lower=0, upper=1)
        SR_CDE_VVM_like = pm.TruncatedNormal("SR_CDE_VVM_like",
                                            mu=SR_CDE_VVM_npt[attr_states["SR_CDE_state"]][0], sigma=SR_CDE_VVM_npt[attr_states["SR_CDE_state"]][1],
                                            lower=0, upper=1)
        SR_CDE_VVL_like = pm.TruncatedNormal("SR_CDE_VVL_like",
                                            mu=SR_CDE_VVL_npt[attr_states["SR_CDE_state"]][0], sigma=SR_CDE_VVL_npt[attr_states["SR_CDE_state"]][1],
                                            lower=0, upper=1)
        # Attribute Hardware/Software/User Requirements Allocation Analysis
        SR_HRAA_VVH_like = pm.TruncatedNormal("SR_HRAA_VVH_like",
                                            mu=SR_HRAA_VVH_npt[attr_states["SR_HRAA_state"]][0], sigma=SR_HRAA_VVH_npt[attr_states["SR_HRAA_state"]][1],
                                            lower=0, upper=1)
        SR_HRAA_VVM_like = pm.TruncatedNormal("SR_HRAA_VVM_like",
                                            mu=SR_HRAA_VVM_npt[attr_states["SR_HRAA_state"]][0], sigma=SR_HRAA_VVM_npt[attr_states["SR_HRAA_state"]][1],
                                            lower=0, upper=1)
        SR_HRAA_VVL_like = pm.TruncatedNormal("SR_HRAA_VVL_like",
                                            mu=SR_HRAA_VVL_npt[attr_states["SR_HRAA_state"]][0], sigma=SR_HRAA_VVL_npt[attr_states["SR_HRAA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Document of Software Requirements Evaluation
        SR_SRE_VVH_like = pm.TruncatedNormal("SR_SRE_VVH_like",
                                            mu=SR_SRE_VVH_npt[attr_states["SR_SRE_state"]][0], sigma=SR_SRE_VVH_npt[attr_states["SR_SRE_state"]][1],
                                            lower=0, upper=1)
        SR_SRE_VVM_like = pm.TruncatedNormal("SR_SRE_VVM_like",
                                            mu=SR_SRE_VVM_npt[attr_states["SR_SRE_state"]][0], sigma=SR_SRE_VVM_npt[attr_states["SR_SRE_state"]][1],
                                            lower=0, upper=1)
        SR_SRE_VVL_like = pm.TruncatedNormal("SR_SRE_VVL_like",
                                            mu=SR_SRE_VVL_npt[attr_states["SR_SRE_state"]][0], sigma=SR_SRE_VVL_npt[attr_states["SR_SRE_state"]][1],
                                            lower=0, upper=1)
        # Attribute Interface Analysis V&V
        SR_IAVV_VVH_like = pm.TruncatedNormal("SR_IAVV_VVH_like",
                                            mu=SR_IAVV_VVH_npt[attr_states["SR_IAVV_state"]][0], sigma=SR_IAVV_VVH_npt[attr_states["SR_IAVV_state"]][1],
                                            lower=0, upper=1)
        SR_IAVV_VVM_like = pm.TruncatedNormal("SR_IAVV_VVM_like",
                                            mu=SR_IAVV_VVM_npt[attr_states["SR_IAVV_state"]][0], sigma=SR_IAVV_VVM_npt[attr_states["SR_IAVV_state"]][1],
                                            lower=0, upper=1)
        SR_IAVV_VVL_like = pm.TruncatedNormal("SR_IAVV_VVL_like",
                                            mu=SR_IAVV_VVL_npt[attr_states["SR_IAVV_state"]][0], sigma=SR_IAVV_VVL_npt[attr_states["SR_IAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Traceability Analysis V&V
        SR_TAVV_VVH_like = pm.TruncatedNormal("SR_TAVV_VVH_like",
                                            mu=SR_TAVV_VVH_npt[attr_states["SR_TAVV_state"]][0], sigma=SR_TAVV_VVH_npt[attr_states["SR_TAVV_state"]][1],
                                            lower=0, upper=1)
        SR_TAVV_VVM_like = pm.TruncatedNormal("SR_TAVV_VVM_like",
                                            mu=SR_TAVV_VVM_npt[attr_states["SR_TAVV_state"]][0], sigma=SR_TAVV_VVM_npt[attr_states["SR_TAVV_state"]][1],
                                            lower=0, upper=1)
        SR_TAVV_VVL_like = pm.TruncatedNormal("SR_TAVV_VVL_like",
                                            mu=SR_TAVV_VVL_npt[attr_states["SR_TAVV_state"]][0], sigma=SR_TAVV_VVL_npt[attr_states["SR_TAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Criticality Analysis V&V
        SR_CAVV_VVH_like = pm.TruncatedNormal("SR_CAVV_VVH_like",
                                            mu=SR_CAVV_VVH_npt[attr_states["SR_CAVV_state"]][0], sigma=SR_CAVV_VVH_npt[attr_states["SR_CAVV_state"]][1],
                                            lower=0, upper=1)
        SR_CAVV_VVM_like = pm.TruncatedNormal("SR_CAVV_VVM_like",
                                            mu=SR_CAVV_VVM_npt[attr_states["SR_CAVV_state"]][0], sigma=SR_CAVV_VVM_npt[attr_states["SR_CAVV_state"]][1],
                                            lower=0, upper=1)
        SR_CAVV_VVL_like = pm.TruncatedNormal("SR_CAVV_VVL_like",
                                            mu=SR_CAVV_VVL_npt[attr_states["SR_CAVV_state"]][0], sigma=SR_CAVV_VVL_npt[attr_states["SR_CAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Hazard Analysis V&V
        SR_HAVV_VVH_like = pm.TruncatedNormal("SR_HAVV_VVH_like",
                                            mu=SR_HAVV_VVH_npt[attr_states["SR_HAVV_state"]][0], sigma=SR_HAVV_VVH_npt[attr_states["SR_HAVV_state"]][1],
                                            lower=0, upper=1)
        SR_HAVV_VVM_like = pm.TruncatedNormal("SR_HAVV_VVM_like",
                                            mu=SR_HAVV_VVM_npt[attr_states["SR_HAVV_state"]][0], sigma=SR_HAVV_VVM_npt[attr_states["SR_HAVV_state"]][1],
                                            lower=0, upper=1)
        SR_HAVV_VVL_like = pm.TruncatedNormal("SR_HAVV_VVL_like",
                                            mu=SR_HAVV_VVL_npt[attr_states["SR_HAVV_state"]][0], sigma=SR_HAVV_VVL_npt[attr_states["SR_HAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Security Analysis V&V
        SR_SAVV_VVH_like = pm.TruncatedNormal("SR_SAVV_VVH_like",
                                            mu=SR_SAVV_VVH_npt[attr_states["SR_SAVV_state"]][0], sigma=SR_SAVV_VVH_npt[attr_states["SR_SAVV_state"]][1],
                                            lower=0, upper=1)
        SR_SAVV_VVM_like = pm.TruncatedNormal("SR_SAVV_VVM_like",
                                            mu=SR_SAVV_VVM_npt[attr_states["SR_SAVV_state"]][0], sigma=SR_SAVV_VVM_npt[attr_states["SR_SAVV_state"]][1],
                                            lower=0, upper=1)
        SR_SAVV_VVL_like = pm.TruncatedNormal("SR_SAVV_VVL_like",
                                            mu=SR_SAVV_VVL_npt[attr_states["SR_SAVV_state"]][0], sigma=SR_SAVV_VVL_npt[attr_states["SR_SAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Risk Analysis V&V
        SR_RAVV_VVH_like = pm.TruncatedNormal("SR_RAVV_VVH_like",
                                            mu=SR_RAVV_VVH_npt[attr_states["SR_RAVV_state"]][0], sigma=SR_RAVV_VVH_npt[attr_states["SR_RAVV_state"]][1],
                                            lower=0, upper=1)
        SR_RAVV_VVM_like = pm.TruncatedNormal("SR_RAVV_VVM_like",
                                            mu=SR_RAVV_VVM_npt[attr_states["SR_RAVV_state"]][0], sigma=SR_RAVV_VVM_npt[attr_states["SR_RAVV_state"]][1],
                                            lower=0, upper=1)
        SR_RAVV_VVL_like = pm.TruncatedNormal("SR_RAVV_VVL_like",
                                            mu=SR_RAVV_VVL_npt[attr_states["SR_RAVV_state"]][0], sigma=SR_RAVV_VVL_npt[attr_states["SR_RAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute V&V System/Software Quantification Test Plan Generation
        SR_VVSQTPG_VVH_like = pm.TruncatedNormal("SR_VVSQTPG_VVH_like",
                                                mu=SR_VVSQTPG_VVH_npt[attr_states["SR_VVSQTPG_state"]][0], sigma=SR_VVSQTPG_VVH_npt[attr_states["SR_VVSQTPG_state"]][1],
                                                lower=0, upper=1)
        SR_VVSQTPG_VVM_like = pm.TruncatedNormal("SR_VVSQTPG_VVM_like",
                                                mu=SR_VVSQTPG_VVM_npt[attr_states["SR_VVSQTPG_state"]][0], sigma=SR_VVSQTPG_VVM_npt[attr_states["SR_VVSQTPG_state"]][1],
                                                lower=0, upper=1)
        SR_VVSQTPG_VVL_like = pm.TruncatedNormal("SR_VVSQTPG_VVL_like",
                                                mu=SR_VVSQTPG_VVL_npt[attr_states["SR_VVSQTPG_state"]][0], sigma=SR_VVSQTPG_VVL_npt[attr_states["SR_VVSQTPG_state"]][1],
                                                lower=0, upper=1)
        # Attribute V&V Software Acceptance Test Plan Generation
        SR_VVSATPG_VVH_like = pm.TruncatedNormal("SR_VVSATPG_VVH_like",
                                                mu=SR_VVSATPG_VVH_npt[attr_states["SR_VVSATPG_state"]][0], sigma=SR_VVSATPG_VVH_npt[attr_states["SR_VVSATPG_state"]][1],
                                                lower=0, upper=1)
        SR_VVSATPG_VVM_like = pm.TruncatedNormal("SR_VVSATPG_VVM_like",
                                                mu=SR_VVSATPG_VVM_npt[attr_states["SR_VVSATPG_state"]][0], sigma=SR_VVSATPG_VVM_npt[attr_states["SR_VVSATPG_state"]][1],
                                                lower=0, upper=1)
        SR_VVSATPG_VVL_like = pm.TruncatedNormal("SR_VVSATPG_VVL_like",
                                                mu=SR_VVSATPG_VVL_npt[attr_states["SR_VVSATPG_state"]][0], sigma=SR_VVSATPG_VVL_npt[attr_states["SR_VVSATPG_state"]][1],
                                                lower=0, upper=1)
        # Attribute Configuration Management Assessment
        SR_CMA_VVH_like = pm.TruncatedNormal("SR_CMA_VVH_like",
                                            mu=SR_CMA_VVH_npt[attr_states["SR_CMA_state"]][0], sigma=SR_CMA_VVH_npt[attr_states["SR_CMA_state"]][1],
                                            lower=0, upper=1)
        SR_CMA_VVM_like = pm.TruncatedNormal("SR_CMA_VVM_like",
                                            mu=SR_CMA_VVM_npt[attr_states["SR_CMA_state"]][0], sigma=SR_CMA_VVM_npt[attr_states["SR_CMA_state"]][1],
                                            lower=0, upper=1)
        SR_CMA_VVL_like = pm.TruncatedNormal("SR_CMA_VVL_like",
                                            mu=SR_CMA_VVL_npt[attr_states["SR_CMA_state"]][0], sigma=SR_CMA_VVL_npt[attr_states["SR_CMA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Reviews and Audit V&V
        SR_RaAVV_VVH_like = pm.TruncatedNormal("SR_RaAVV_VVH_like",
                                            mu=SR_RaAVV_VVH_npt[attr_states["SR_RaAVV_state"]][0], sigma=SR_RaAVV_VVH_npt[attr_states["SR_RaAVV_state"]][1],
                                            lower=0, upper=1)
        SR_RaAVV_VVM_like = pm.TruncatedNormal("SR_RaAVV_VVM_like",
                                            mu=SR_RaAVV_VVM_npt[attr_states["SR_RaAVV_state"]][0], sigma=SR_RaAVV_VVM_npt[attr_states["SR_RaAVV_state"]][1],
                                            lower=0, upper=1)
        SR_RaAVV_VVL_like = pm.TruncatedNormal("SR_RaAVV_VVL_like",
                                            mu=SR_RaAVV_VVL_npt[attr_states["SR_RaAVV_state"]][0], sigma=SR_RaAVV_VVL_npt[attr_states["SR_RaAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute V&V Requirements Specifications Phase Activity Summary Report Generation
        SR_VVASRG_VVH_like = pm.TruncatedNormal("SR_VVASRG_VVH_like",
                                                mu=SR_VVASRG_VVH_npt[attr_states["SR_VVASRG_state"]][0], sigma=SR_VVASRG_VVH_npt[attr_states["SR_VVASRG_state"]][1],
                                                lower=0, upper=1)
        SR_VVASRG_VVM_like = pm.TruncatedNormal("SR_VVASRG_VVM_like",
                                                mu=SR_VVASRG_VVM_npt[attr_states["SR_VVASRG_state"]][0], sigma=SR_VVASRG_VVM_npt[attr_states["SR_VVASRG_state"]][1],
                                                lower=0, upper=1)
        SR_VVASRG_VVL_like = pm.TruncatedNormal("SR_VVASRG_VVL_like",
                                                mu=SR_VVASRG_VVL_npt[attr_states["SR_VVASRG_state"]][0], sigma=SR_VVASRG_VVL_npt[attr_states["SR_VVASRG_state"]][1],
                                                lower=0, upper=1)
        # m1-m3: a part of marginal probability
        # m1 = P(VV=H)P(attribute states|VV=H)
        # m2 = P(VV=M)P(attribute states|VV=M)
        # m3 = P(VV=L)P(attribute states|VV=L)
        SR_VV_m1 = SR_VVH_prior * SR_SVVP_VVH_like * SR_CDE_VVH_like * SR_HRAA_VVH_like * SR_SRE_VVH_like * SR_IAVV_VVH_like * SR_TAVV_VVH_like * SR_CAVV_VVH_like * SR_HAVV_VVH_like * SR_SAVV_VVH_like * SR_RAVV_VVH_like * SR_VVSQTPG_VVH_like * SR_VVSATPG_VVH_like * SR_CMA_VVH_like * SR_RaAVV_VVH_like * SR_VVASRG_VVH_like
        SR_VV_m2 = SR_VVM_prior * SR_SVVP_VVM_like * SR_CDE_VVM_like * SR_HRAA_VVM_like * SR_SRE_VVM_like * SR_IAVV_VVM_like * SR_TAVV_VVM_like * SR_CAVV_VVM_like * SR_HAVV_VVM_like * SR_SAVV_VVM_like * SR_RAVV_VVM_like * SR_VVSQTPG_VVM_like * SR_VVSATPG_VVM_like * SR_CMA_VVM_like * SR_RaAVV_VVM_like * SR_VVASRG_VVM_like
        SR_VV_m3 = SR_VVL_prior * SR_SVVP_VVL_like * SR_CDE_VVL_like * SR_HRAA_VVL_like * SR_SRE_VVL_like * SR_IAVV_VVL_like * SR_TAVV_VVL_like * SR_CAVV_VVL_like * SR_HAVV_VVL_like * SR_SAVV_VVL_like * SR_RAVV_VVL_like * SR_VVSQTPG_VVL_like * SR_VVSATPG_VVL_like * SR_CMA_VVL_like * SR_RaAVV_VVL_like * SR_VVASRG_VVL_like

        # k = 1 / marginal probability
        SR_VV_k = 1 / (SR_VV_m1 + SR_VV_m2 + SR_VV_m3)

        # posterior probability of V&V quality in SR phase
        SR_VVH_post = pm.Deterministic("SR_VVH_post", SR_VV_k * SR_VV_m1)
        SR_VVM_post = pm.Deterministic("SR_VVM_post", SR_VV_k * SR_VV_m2)
        SR_VVL_post = pm.Deterministic("SR_VVL_post", SR_VV_k * SR_VV_m3)
    return model

def create_SD_Dev_model(attr_states):
    model = pm.Model()

    with model:
        # Dev Attribute model - Design phase
        # prior probability of Dev quality in SD phase
        SD_DevH_prior = pm.Beta("SD_DevH_prior", alpha=0.56, beta=1.74)
        SD_DevM_prior = pm.Beta("SD_DevM_prior", alpha=2.40, beta=1.81)
        SD_DevL_prior = pm.Beta("SD_DevL_prior", alpha=4.12, beta=22.06)
        # Attribute Development of Software Architecture Description
        SD_SAD_DevH_like = pm.TruncatedNormal("SD_SAD_DevH_like",
                                            mu=SD_SAD_DevH_npt[attr_states["SD_SAD_state"]][0], sigma=SD_SAD_DevH_npt[attr_states["SD_SAD_state"]][1],
                                            lower=0, upper=1)
        SD_SAD_DevM_like = pm.TruncatedNormal("SD_SAD_DevM_like",
                                            mu=SD_SAD_DevM_npt[attr_states["SD_SAD_state"]][0], sigma=SD_SAD_DevM_npt[attr_states["SD_SAD_state"]][1],
                                            lower=0, upper=1)
        SD_SAD_DevL_like = pm.TruncatedNormal("SD_SAD_DevL_like",
                                            mu=SD_SAD_DevL_npt[attr_states["SD_SAD_state"]][0], sigma=SD_SAD_DevL_npt[attr_states["SD_SAD_state"]][1],
                                            lower=0, upper=1)
        # Attribute Development of Software Design Description
        SD_SDD_DevH_like = pm.TruncatedNormal("SD_SDD_DevH_like",
                                            mu=SD_SDD_DevH_npt[attr_states["SD_SDD_state"]][0], sigma=SD_SDD_DevH_npt[attr_states["SD_SDD_state"]][1],
                                            lower=0, upper=1)
        SD_SDD_DevM_like = pm.TruncatedNormal("SD_SDD_DevM_like",
                                            mu=SD_SDD_DevM_npt[attr_states["SD_SDD_state"]][0], sigma=SD_SDD_DevM_npt[attr_states["SD_SDD_state"]][1],
                                            lower=0, upper=1)
        SD_SDD_DevL_like = pm.TruncatedNormal("SD_SDD_DevL_like",
                                            mu=SD_SDD_DevL_npt[attr_states["SD_SDD_state"]][0], sigma=SD_SDD_DevL_npt[attr_states["SD_SDD_state"]][1],
                                            lower=0, upper=1)
        # Attribute Traceability Analysis - Design Phase
        SD_TA_DevH_like = pm.TruncatedNormal("SD_TA_DevH_like",
                                            mu=SD_TA_DevH_npt[attr_states["SD_TA_state"]][0], sigma=SD_TA_DevH_npt[attr_states["SD_TA_state"]][1],
                                            lower=0, upper=1)
        SD_TA_DevM_like = pm.TruncatedNormal("SD_TA_DevM_like",
                                            mu=SD_TA_DevM_npt[attr_states["SD_TA_state"]][0], sigma=SD_TA_DevM_npt[attr_states["SD_TA_state"]][1],
                                            lower=0, upper=1)
        SD_TA_DevL_like = pm.TruncatedNormal("SD_TA_DevL_like",
                                            mu=SD_TA_DevL_npt[attr_states["SD_TA_state"]][0], sigma=SD_TA_DevL_npt[attr_states["SD_TA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Criticality Analysis - Design Phase
        SD_CA_DevH_like = pm.TruncatedNormal("SD_CA_DevH_like",
                                            mu=SD_CA_DevH_npt[attr_states["SD_CA_state"]][0], sigma=SD_CA_DevH_npt[attr_states["SD_CA_state"]][1],
                                            lower=0, upper=1)
        SD_CA_DevM_like = pm.TruncatedNormal("SD_CA_DevM_like",
                                            mu=SD_CA_DevM_npt[attr_states["SD_CA_state"]][0], sigma=SD_CA_DevM_npt[attr_states["SD_CA_state"]][1],
                                            lower=0, upper=1)
        SD_CA_DevL_like = pm.TruncatedNormal("SD_CA_DevL_like",
                                            mu=SD_CA_DevL_npt[attr_states["SD_CA_state"]][0], sigma=SD_CA_DevL_npt[attr_states["SD_CA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Hazard Analysis - Design Phase
        SD_HA_DevH_like = pm.TruncatedNormal("SD_HA_DevH_like",
                                            mu=SD_HA_DevH_npt[attr_states["SD_HA_state"]][0], sigma=SD_HA_DevH_npt[attr_states["SD_HA_state"]][1],
                                            lower=0, upper=1)
        SD_HA_DevM_like = pm.TruncatedNormal("SD_HA_DevM_like",
                                            mu=SD_HA_DevM_npt[attr_states["SD_HA_state"]][0], sigma=SD_HA_DevM_npt[attr_states["SD_HA_state"]][1],
                                            lower=0, upper=1)
        SD_HA_DevL_like = pm.TruncatedNormal("SD_HA_DevL_like",
                                            mu=SD_HA_DevL_npt[attr_states["SD_HA_state"]][0], sigma=SD_HA_DevL_npt[attr_states["SD_HA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Security Analysis - Design Phase
        SD_SA_DevH_like = pm.TruncatedNormal("SD_SA_DevH_like",
                                            mu=SD_SA_DevH_npt[attr_states["SD_SA_state"]][0], sigma=SD_SA_DevH_npt[attr_states["SD_SA_state"]][1],
                                            lower=0, upper=1)
        SD_SA_DevM_like = pm.TruncatedNormal("SD_SA_DevM_like",
                                            mu=SD_SA_DevM_npt[attr_states["SD_SA_state"]][0], sigma=SD_SA_DevM_npt[attr_states["SD_SA_state"]][1],
                                            lower=0, upper=1)
        SD_SA_DevL_like = pm.TruncatedNormal("SD_SA_DevL_like",
                                            mu=SD_SA_DevL_npt[attr_states["SD_SA_state"]][0], sigma=SD_SA_DevL_npt[attr_states["SD_SA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Risk Analysis - Design Phase
        SD_RA_DevH_like = pm.TruncatedNormal("SD_RA_DevH_like",
                                            mu=SD_RA_DevH_npt[attr_states["SD_RA_state"]][0], sigma=SD_RA_DevH_npt[attr_states["SD_RA_state"]][1],
                                            lower=0, upper=1)
        SD_RA_DevM_like = pm.TruncatedNormal("SD_RA_DevM_like",
                                            mu=SD_RA_DevM_npt[attr_states["SD_RA_state"]][0], sigma=SD_RA_DevM_npt[attr_states["SD_RA_state"]][1],
                                            lower=0, upper=1)
        SD_RA_DevL_like = pm.TruncatedNormal("SD_RA_DevL_like",
                                            mu=SD_RA_DevL_npt[attr_states["SD_RA_state"]][0], sigma=SD_RA_DevL_npt[attr_states["SD_RA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Software Component Test Plan Generation
        SD_SCTPG_DevH_like = pm.TruncatedNormal("SD_SCTPG_DevH_like",
                                                mu=SD_SCTPG_DevH_npt[attr_states["SD_SCTPG_state"]][0], sigma=SD_SCTPG_DevH_npt[attr_states["SD_SCTPG_state"]][1],
                                                lower=0, upper=1)
        SD_SCTPG_DevM_like = pm.TruncatedNormal("SD_SCTPG_DevM_like",
                                                mu=SD_SCTPG_DevM_npt[attr_states["SD_SCTPG_state"]][0], sigma=SD_SCTPG_DevM_npt[attr_states["SD_SCTPG_state"]][1],
                                                lower=0, upper=1)
        SD_SCTPG_DevL_like = pm.TruncatedNormal("SD_SCTPG_DevL_like",
                                                mu=SD_SCTPG_DevL_npt[attr_states["SD_SCTPG_state"]][0], sigma=SD_SCTPG_DevL_npt[attr_states["SD_SCTPG_state"]][1],
                                                lower=0, upper=1)
        # Attribute Software Integration Test Plan Generation
        SD_SITPG_DevH_like = pm.TruncatedNormal("SD_SITPG_DevH_like",
                                                mu=SD_SITPG_DevH_npt[attr_states["SD_SITPG_state"]][0], sigma=SD_SITPG_DevH_npt[attr_states["SD_SITPG_state"]][1],
                                                lower=0, upper=1)
        SD_SITPG_DevM_like = pm.TruncatedNormal("SD_SITPG_DevM_like",
                                                mu=SD_SITPG_DevM_npt[attr_states["SD_SITPG_state"]][0], sigma=SD_SITPG_DevM_npt[attr_states["SD_SITPG_state"]][1],
                                                lower=0, upper=1)
        SD_SITPG_DevL_like = pm.TruncatedNormal("SD_SITPG_DevL_like",
                                                mu=SD_SITPG_DevL_npt[attr_states["SD_SITPG_state"]][0], sigma=SD_SITPG_DevL_npt[attr_states["SD_SITPG_state"]][1],
                                                lower=0, upper=1)
        # Attribute Software Component Test Design Generation
        SD_SCTDG_DevH_like = pm.TruncatedNormal("SD_SCTDG_DevH_like",
                                                mu=SD_SCTDG_DevH_npt[attr_states["SD_SCTDG_state"]][0], sigma=SD_SCTDG_DevH_npt[attr_states["SD_SCTDG_state"]][1],
                                                lower=0, upper=1)
        SD_SCTDG_DevM_like = pm.TruncatedNormal("SD_SCTDG_DevM_like",
                                                mu=SD_SCTDG_DevM_npt[attr_states["SD_SCTDG_state"]][0], sigma=SD_SCTDG_DevM_npt[attr_states["SD_SCTDG_state"]][1],
                                                lower=0, upper=1)
        SD_SCTDG_DevL_like = pm.TruncatedNormal("SD_SCTDG_DevL_like",
                                                mu=SD_SCTDG_DevL_npt[attr_states["SD_SCTDG_state"]][0], sigma=SD_SCTDG_DevL_npt[attr_states["SD_SCTDG_state"]][1],
                                                lower=0, upper=1)
        # Attribute Software Integration Test Design Generation
        SD_SITDG_DevH_like = pm.TruncatedNormal("SD_SITDG_DevH_like",
                                                mu=SD_SITDG_DevH_npt[attr_states["SD_SITDG_state"]][0], sigma=SD_SITDG_DevH_npt[attr_states["SD_SITDG_state"]][1],
                                                lower=0, upper=1)
        SD_SITDG_DevM_like = pm.TruncatedNormal("SD_SITDG_DevM_like",
                                                mu=SD_SITDG_DevM_npt[attr_states["SD_SITDG_state"]][0], sigma=SD_SITDG_DevM_npt[attr_states["SD_SITDG_state"]][1],
                                                lower=0, upper=1)
        SD_SITDG_DevL_like = pm.TruncatedNormal("SD_SITDG_DevL_like",
                                                mu=SD_SITDG_DevL_npt[attr_states["SD_SITDG_state"]][0], sigma=SD_SITDG_DevL_npt[attr_states["SD_SITDG_state"]][1],
                                                lower=0, upper=1)
        # Attribute Software Qualification Test Design Generation
        SD_SQTDG_DevH_like = pm.TruncatedNormal("SD_SQTDG_DevH_like",
                                                mu=SD_SQTDG_DevH_npt[attr_states["SD_SQTDG_state"]][0], sigma=SD_SQTDG_DevH_npt[attr_states["SD_SQTDG_state"]][1],
                                                lower=0, upper=1)
        SD_SQTDG_DevM_like = pm.TruncatedNormal("SD_SQTDG_DevM_like",
                                                mu=SD_SQTDG_DevM_npt[attr_states["SD_SQTDG_state"]][0], sigma=SD_SQTDG_DevM_npt[attr_states["SD_SQTDG_state"]][1],
                                                lower=0, upper=1)
        SD_SQTDG_DevL_like = pm.TruncatedNormal("SD_SQTDG_DevL_like",
                                                mu=SD_SQTDG_DevL_npt[attr_states["SD_SQTDG_state"]][0], sigma=SD_SQTDG_DevL_npt[attr_states["SD_SQTDG_state"]][1],
                                                lower=0, upper=1)
        # Attribute Software Acceptance Test Design Generation
        SD_SATDG_DevH_like = pm.TruncatedNormal("SD_SATDG_DevH_like",
                                                mu=SD_SATDG_DevH_npt[attr_states["SD_SATDG_state"]][0], sigma=SD_SATDG_DevH_npt[attr_states["SD_SATDG_state"]][1],
                                                lower=0, upper=1)
        SD_SATDG_DevM_like = pm.TruncatedNormal("SD_SATDG_DevM_like",
                                                mu=SD_SATDG_DevM_npt[attr_states["SD_SATDG_state"]][0], sigma=SD_SATDG_DevM_npt[attr_states["SD_SATDG_state"]][1],
                                                lower=0, upper=1)
        SD_SATDG_DevL_like = pm.TruncatedNormal("SD_SATDG_DevL_like",
                                                mu=SD_SATDG_DevL_npt[attr_states["SD_SATDG_state"]][0], sigma=SD_SATDG_DevL_npt[attr_states["SD_SATDG_state"]][1],
                                                lower=0, upper=1)
        # Attribute Configuration Management - Design Phase
        SD_CM_DevH_like = pm.TruncatedNormal("SD_CM_DevH_like",
                                            mu=SD_CM_DevH_npt[attr_states["SD_CM_state"]][0], sigma=SD_CM_DevH_npt[attr_states["SD_CM_state"]][1],
                                            lower=0, upper=1)
        SD_CM_DevM_like = pm.TruncatedNormal("SD_CM_DevM_like",
                                            mu=SD_CM_DevM_npt[attr_states["SD_CM_state"]][0], sigma=SD_CM_DevM_npt[attr_states["SD_CM_state"]][1],
                                            lower=0, upper=1)
        SD_CM_DevL_like = pm.TruncatedNormal("SD_CM_DevL_like",
                                            mu=SD_CM_DevL_npt[attr_states["SD_CM_state"]][0], sigma=SD_CM_DevL_npt[attr_states["SD_CM_state"]][1],
                                            lower=0, upper=1)
        # Attribute Reviews and Audit - Design Phase
        SD_RaA_DevH_like = pm.TruncatedNormal("SD_RaA_DevH_like",
                                            mu=SD_RaA_DevH_npt[attr_states["SD_RaA_state"]][0], sigma=SD_RaA_DevH_npt[attr_states["SD_RaA_state"]][1],
                                            lower=0, upper=1)
        SD_RaA_DevM_like = pm.TruncatedNormal("SD_RaA_DevM_like",
                                            mu=SD_RaA_DevM_npt[attr_states["SD_RaA_state"]][0], sigma=SD_RaA_DevM_npt[attr_states["SD_RaA_state"]][1],
                                            lower=0, upper=1)
        SD_RaA_DevL_like = pm.TruncatedNormal("SD_RaA_DevL_like",
                                            mu=SD_RaA_DevL_npt[attr_states["SD_RaA_state"]][0], sigma=SD_RaA_DevL_npt[attr_states["SD_RaA_state"]][1],
                                            lower=0, upper=1)
        # m1-m3: a part of marginal probability
        # m1 = P(Dev=H)P(attribute states|Dev=H)
        # m2 = P(Dev=M)P(attribute states|Dev=M)
        # m3 = P(Dev=L)P(attribute states|Dev=L)
        SD_Dev_m1 = SD_DevH_prior * SD_SAD_DevH_like * SD_SDD_DevH_like * SD_TA_DevH_like * SD_CA_DevH_like * SD_HA_DevH_like * SD_SA_DevH_like * SD_RA_DevH_like * SD_SCTPG_DevH_like * SD_SITPG_DevH_like * SD_SCTDG_DevH_like * SD_SITDG_DevH_like * SD_SQTDG_DevH_like * SD_SATDG_DevH_like * SD_CM_DevH_like * SD_RaA_DevH_like
        SD_Dev_m2 = SD_DevM_prior * SD_SAD_DevM_like * SD_SDD_DevM_like * SD_TA_DevM_like * SD_CA_DevM_like * SD_HA_DevM_like * SD_SA_DevM_like * SD_RA_DevM_like * SD_SCTPG_DevM_like * SD_SITPG_DevM_like * SD_SCTDG_DevM_like * SD_SITDG_DevM_like * SD_SQTDG_DevM_like * SD_SATDG_DevM_like * SD_CM_DevM_like * SD_RaA_DevM_like
        SD_Dev_m3 = SD_DevL_prior * SD_SAD_DevL_like * SD_SDD_DevL_like * SD_TA_DevL_like * SD_CA_DevL_like * SD_HA_DevL_like * SD_SA_DevL_like * SD_RA_DevL_like * SD_SCTPG_DevL_like * SD_SITPG_DevL_like * SD_SCTDG_DevL_like * SD_SITDG_DevL_like * SD_SQTDG_DevL_like * SD_SATDG_DevL_like * SD_CM_DevL_like * SD_RaA_DevL_like

        # k = 1 / marginal probability
        SD_Dev_k = 1 / (SD_Dev_m1 + SD_Dev_m2 + SD_Dev_m3)

        # posterior probability of Dev quality in SD phase
        SD_DevH_post = pm.Deterministic("SD_DevH_post", SD_Dev_k * SD_Dev_m1)
        SD_DevM_post = pm.Deterministic("SD_DevM_post", SD_Dev_k * SD_Dev_m2)
        SD_DevL_post = pm.Deterministic("SD_DevL_post", SD_Dev_k * SD_Dev_m3)
    return model

def create_SD_VV_model(attr_states):
    model = pm.Model()

    with model:
        # V&V Attribute model - Design phase
        # prior probability of V&V quality in SD phase
        SD_VVH_prior = pm.Beta("SD_VVH_prior", alpha=0.56, beta=1.74)
        SD_VVM_prior = pm.Beta("SD_VVM_prior", alpha=2.40, beta=1.81)
        SD_VVL_prior = pm.Beta("SD_VVL_prior", alpha=4.12, beta=22.06)
        # Attribute Design Evaluation
        SD_DE_VVH_like = pm.TruncatedNormal("SD_DE_VVH_like",
                                            mu=SD_DE_VVH_npt[attr_states["SD_DE_state"]][0], sigma=SD_DE_VVH_npt[attr_states["SD_DE_state"]][1],
                                            lower=0, upper=1)
        SD_DE_VVM_like = pm.TruncatedNormal("SD_DE_VVM_like",
                                            mu=SD_DE_VVM_npt[attr_states["SD_DE_state"]][0], sigma=SD_DE_VVM_npt[attr_states["SD_DE_state"]][1],
                                            lower=0, upper=1)
        SD_DE_VVL_like = pm.TruncatedNormal("SD_DE_VVL_like",
                                            mu=SD_DE_VVL_npt[attr_states["SD_DE_state"]][0], sigma=SD_DE_VVL_npt[attr_states["SD_DE_state"]][1],
                                            lower=0, upper=1)
        # Attribute Interface Analysis V&V
        SD_IAVV_VVH_like = pm.TruncatedNormal("SD_IAVV_VVH_like",
                                            mu=SD_IAVV_VVH_npt[attr_states["SD_IAVV_state"]][0], sigma=SD_IAVV_VVH_npt[attr_states["SD_IAVV_state"]][1],
                                            lower=0, upper=1)
        SD_IAVV_VVM_like = pm.TruncatedNormal("SD_IAVV_VVM_like",
                                            mu=SD_IAVV_VVM_npt[attr_states["SD_IAVV_state"]][0], sigma=SD_IAVV_VVM_npt[attr_states["SD_IAVV_state"]][1],
                                            lower=0, upper=1)
        SD_IAVV_VVL_like = pm.TruncatedNormal("SD_IAVV_VVL_like",
                                            mu=SD_IAVV_VVL_npt[attr_states["SD_IAVV_state"]][0], sigma=SD_IAVV_VVL_npt[attr_states["SD_IAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Traceability Analysis V&V - Design Phase
        SD_TAVV_VVH_like = pm.TruncatedNormal("SD_TAVV_VVH_like",
                                            mu=SD_TAVV_VVH_npt[attr_states["SD_TAVV_state"]][0], sigma=SD_TAVV_VVH_npt[attr_states["SD_TAVV_state"]][1],
                                            lower=0, upper=1)
        SD_TAVV_VVM_like = pm.TruncatedNormal("SD_TAVV_VVM_like",
                                            mu=SD_TAVV_VVM_npt[attr_states["SD_TAVV_state"]][0], sigma=SD_TAVV_VVM_npt[attr_states["SD_TAVV_state"]][1],
                                            lower=0, upper=1)
        SD_TAVV_VVL_like = pm.TruncatedNormal("SD_TAVV_VVL_like",
                                            mu=SD_TAVV_VVL_npt[attr_states["SD_TAVV_state"]][0], sigma=SD_TAVV_VVL_npt[attr_states["SD_TAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Criticality Analysis V&V - Design Phase
        SD_CAVV_VVH_like = pm.TruncatedNormal("SD_CAVV_VVH_like",
                                            mu=SD_CAVV_VVH_npt[attr_states["SD_CAVV_state"]][0], sigma=SD_CAVV_VVH_npt[attr_states["SD_CAVV_state"]][1],
                                            lower=0, upper=1)
        SD_CAVV_VVM_like = pm.TruncatedNormal("SD_CAVV_VVM_like",
                                            mu=SD_CAVV_VVM_npt[attr_states["SD_CAVV_state"]][0], sigma=SD_CAVV_VVM_npt[attr_states["SD_CAVV_state"]][1],
                                            lower=0, upper=1)
        SD_CAVV_VVL_like = pm.TruncatedNormal("SD_CAVV_VVL_like",
                                            mu=SD_CAVV_VVL_npt[attr_states["SD_CAVV_state"]][0], sigma=SD_CAVV_VVL_npt[attr_states["SD_CAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Hazard Analysis V&V - Design Phase
        SD_HAVV_VVH_like = pm.TruncatedNormal("SD_HAVV_VVH_like",
                                            mu=SD_HAVV_VVH_npt[attr_states["SD_HAVV_state"]][0], sigma=SD_HAVV_VVH_npt[attr_states["SD_HAVV_state"]][1],
                                            lower=0, upper=1)
        SD_HAVV_VVM_like = pm.TruncatedNormal("SD_HAVV_VVM_like",
                                            mu=SD_HAVV_VVM_npt[attr_states["SD_HAVV_state"]][0], sigma=SD_HAVV_VVM_npt[attr_states["SD_HAVV_state"]][1],
                                            lower=0, upper=1)
        SD_HAVV_VVL_like = pm.TruncatedNormal("SD_HAVV_VVL_like",
                                            mu=SD_HAVV_VVL_npt[attr_states["SD_HAVV_state"]][0], sigma=SD_HAVV_VVL_npt[attr_states["SD_HAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Security Analysis V&V - Design Phase
        SD_SAVV_VVH_like = pm.TruncatedNormal("SD_SAVV_VVH_like",
                                            mu=SD_SAVV_VVH_npt[attr_states["SD_SAVV_state"]][0], sigma=SD_SAVV_VVH_npt[attr_states["SD_SAVV_state"]][1],
                                            lower=0, upper=1)
        SD_SAVV_VVM_like = pm.TruncatedNormal("SD_SAVV_VVM_like",
                                            mu=SD_SAVV_VVM_npt[attr_states["SD_SAVV_state"]][0], sigma=SD_SAVV_VVM_npt[attr_states["SD_SAVV_state"]][1],
                                            lower=0, upper=1)
        SD_SAVV_VVL_like = pm.TruncatedNormal("SD_SAVV_VVL_like",
                                            mu=SD_SAVV_VVL_npt[attr_states["SD_SAVV_state"]][0], sigma=SD_SAVV_VVL_npt[attr_states["SD_SAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Risk Analysis V&V - Design Phase
        SD_RAVV_VVH_like = pm.TruncatedNormal("SD_RAVV_VVH_like",
                                            mu=SD_RAVV_VVH_npt[attr_states["SD_RAVV_state"]][0], sigma=SD_RAVV_VVH_npt[attr_states["SD_RAVV_state"]][1],
                                            lower=0, upper=1)
        SD_RAVV_VVM_like = pm.TruncatedNormal("SD_RAVV_VVM_like",
                                            mu=SD_RAVV_VVM_npt[attr_states["SD_RAVV_state"]][0], sigma=SD_RAVV_VVM_npt[attr_states["SD_RAVV_state"]][1],
                                            lower=0, upper=1)
        SD_RAVV_VVL_like = pm.TruncatedNormal("SD_RAVV_VVL_like",
                                            mu=SD_RAVV_VVL_npt[attr_states["SD_RAVV_state"]][0], sigma=SD_RAVV_VVL_npt[attr_states["SD_RAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute V&V Software Component Test Plan Generation
        SD_VVSCTPG_VVH_like = pm.TruncatedNormal("SD_VVSCTPG_VVH_like",
                                                mu=SD_VVSCTPG_VVH_npt[attr_states["SD_VVSCTPG_state"]][0], sigma=SD_VVSCTPG_VVH_npt[attr_states["SD_VVSCTPG_state"]][1],
                                                lower=0, upper=1)
        SD_VVSCTPG_VVM_like = pm.TruncatedNormal("SD_VVSCTPG_VVM_like",
                                                mu=SD_VVSCTPG_VVM_npt[attr_states["SD_VVSCTPG_state"]][0], sigma=SD_VVSCTPG_VVM_npt[attr_states["SD_VVSCTPG_state"]][1],
                                                lower=0, upper=1)
        SD_VVSCTPG_VVL_like = pm.TruncatedNormal("SD_VVSCTPG_VVL_like",
                                                mu=SD_VVSCTPG_VVL_npt[attr_states["SD_VVSCTPG_state"]][0], sigma=SD_VVSCTPG_VVL_npt[attr_states["SD_VVSCTPG_state"]][1],
                                                lower=0, upper=1)
        # Attribute V&V Software Integration Test Plan Generation
        SD_VVSITPG_VVH_like = pm.TruncatedNormal("SD_VVSITPG_VVH_like",
                                                mu=SD_VVSITPG_VVH_npt[attr_states["SD_VVSITPG_state"]][0], sigma=SD_VVSITPG_VVH_npt[attr_states["SD_VVSITPG_state"]][1],
                                                lower=0, upper=1)
        SD_VVSITPG_VVM_like = pm.TruncatedNormal("SD_VVSITPG_VVM_like",
                                                mu=SD_VVSITPG_VVM_npt[attr_states["SD_VVSITPG_state"]][0], sigma=SD_VVSITPG_VVM_npt[attr_states["SD_VVSITPG_state"]][1],
                                                lower=0, upper=1)
        SD_VVSITPG_VVL_like = pm.TruncatedNormal("SD_VVSITPG_VVL_like",
                                                mu=SD_VVSITPG_VVL_npt[attr_states["SD_VVSITPG_state"]][0], sigma=SD_VVSITPG_VVL_npt[attr_states["SD_VVSITPG_state"]][1],
                                                lower=0, upper=1)
        # Attribute V&V Software Component Test Design Generation
        SD_VVSCTDG_VVH_like = pm.TruncatedNormal("SD_VVSCTDG_VVH_like",
                                                mu=SD_VVSCTDG_VVH_npt[attr_states["SD_VVSCTDG_state"]][0], sigma=SD_VVSCTDG_VVH_npt[attr_states["SD_VVSCTDG_state"]][1],
                                                lower=0, upper=1)
        SD_VVSCTDG_VVM_like = pm.TruncatedNormal("SD_VVSCTDG_VVM_like",
                                                mu=SD_VVSCTDG_VVM_npt[attr_states["SD_VVSCTDG_state"]][0], sigma=SD_VVSCTDG_VVM_npt[attr_states["SD_VVSCTDG_state"]][1],
                                                lower=0, upper=1)
        SD_VVSCTDG_VVL_like = pm.TruncatedNormal("SD_VVSCTDG_VVL_like",
                                                mu=SD_VVSCTDG_VVL_npt[attr_states["SD_VVSCTDG_state"]][0], sigma=SD_VVSCTDG_VVL_npt[attr_states["SD_VVSCTDG_state"]][1],
                                                lower=0, upper=1)
        # Attribute V&V Software Integration Test Design Generation
        SD_VVSITDG_VVH_like = pm.TruncatedNormal("SD_VVSITDG_VVH_like",
                                                mu=SD_VVSITDG_VVH_npt[attr_states["SD_VVSITDG_state"]][0], sigma=SD_VVSITDG_VVH_npt[attr_states["SD_VVSITDG_state"]][1],
                                                lower=0, upper=1)
        SD_VVSITDG_VVM_like = pm.TruncatedNormal("SD_VVSITDG_VVM_like",
                                                mu=SD_VVSITDG_VVM_npt[attr_states["SD_VVSITDG_state"]][0], sigma=SD_VVSITDG_VVM_npt[attr_states["SD_VVSITDG_state"]][1],
                                                lower=0, upper=1)
        SD_VVSITDG_VVL_like = pm.TruncatedNormal("SD_VVSITDG_VVL_like",
                                                mu=SD_VVSITDG_VVL_npt[attr_states["SD_VVSITDG_state"]][0], sigma=SD_VVSITDG_VVL_npt[attr_states["SD_VVSITDG_state"]][1],
                                                lower=0, upper=1)
        # Attribute V&V Software Qualification Test Design Generation
        SD_VVSQTDG_VVH_like = pm.TruncatedNormal("SD_VVSQTDG_VVH_like",
                                                mu=SD_VVSQTDG_VVH_npt[attr_states["SD_VVSQTDG_state"]][0], sigma=SD_VVSQTDG_VVH_npt[attr_states["SD_VVSQTDG_state"]][1],
                                                lower=0, upper=1)
        SD_VVSQTDG_VVM_like = pm.TruncatedNormal("SD_VVSQTDG_VVM_like",
                                                mu=SD_VVSQTDG_VVM_npt[attr_states["SD_VVSQTDG_state"]][0], sigma=SD_VVSQTDG_VVM_npt[attr_states["SD_VVSQTDG_state"]][1],
                                                lower=0, upper=1)
        SD_VVSQTDG_VVL_like = pm.TruncatedNormal("SD_VVSQTDG_VVL_like",
                                                mu=SD_VVSQTDG_VVL_npt[attr_states["SD_VVSQTDG_state"]][0], sigma=SD_VVSQTDG_VVL_npt[attr_states["SD_VVSQTDG_state"]][1],
                                                lower=0, upper=1)
        # Attribute V&V Software Acceptance Test Design Generation
        SD_VVSATDG_VVH_like = pm.TruncatedNormal("SD_VVSATDG_VVH_like",
                                                mu=SD_VVSATDG_VVH_npt[attr_states["SD_VVSATDG_state"]][0], sigma=SD_VVSATDG_VVH_npt[attr_states["SD_VVSATDG_state"]][1],
                                                lower=0, upper=1)
        SD_VVSATDG_VVM_like = pm.TruncatedNormal("SD_VVSATDG_VVM_like",
                                                mu=SD_VVSATDG_VVM_npt[attr_states["SD_VVSATDG_state"]][0], sigma=SD_VVSATDG_VVM_npt[attr_states["SD_VVSATDG_state"]][1],
                                                lower=0, upper=1)
        SD_VVSATDG_VVL_like = pm.TruncatedNormal("SD_VVSATDG_VVL_like",
                                                mu=SD_VVSATDG_VVL_npt[attr_states["SD_VVSATDG_state"]][0], sigma=SD_VVSATDG_VVL_npt[attr_states["SD_VVSATDG_state"]][1],
                                                lower=0, upper=1)
        # Attribute Configuration Management V&V - Design Phase
        SD_CMVV_VVH_like = pm.TruncatedNormal("SD_CMVV_VVH_like",
                                            mu=SD_CMVV_VVH_npt[attr_states["SD_CMVV_state"]][0], sigma=SD_CMVV_VVH_npt[attr_states["SD_CMVV_state"]][1],
                                            lower=0, upper=1)
        SD_CMVV_VVM_like = pm.TruncatedNormal("SD_CMVV_VVM_like",
                                            mu=SD_CMVV_VVM_npt[attr_states["SD_CMVV_state"]][0], sigma=SD_CMVV_VVM_npt[attr_states["SD_CMVV_state"]][1],
                                            lower=0, upper=1)
        SD_CMVV_VVL_like = pm.TruncatedNormal("SD_CMVV_VVL_like",
                                            mu=SD_CMVV_VVL_npt[attr_states["SD_CMVV_state"]][0], sigma=SD_CMVV_VVL_npt[attr_states["SD_CMVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Review and Audit V&V - Design Phase
        SD_RaAVV_VVH_like = pm.TruncatedNormal("SD_RaAVV_VVH_like",
                                            mu=SD_RaAVV_VVH_npt[attr_states["SD_RaAVV_state"]][0], sigma=SD_RaAVV_VVH_npt[attr_states["SD_RaAVV_state"]][1],
                                            lower=0, upper=1)
        SD_RaAVV_VVM_like = pm.TruncatedNormal("SD_RaAVV_VVM_like",
                                            mu=SD_RaAVV_VVM_npt[attr_states["SD_RaAVV_state"]][0], sigma=SD_RaAVV_VVM_npt[attr_states["SD_RaAVV_state"]][1],
                                            lower=0, upper=1)
        SD_RaAVV_VVL_like = pm.TruncatedNormal("SD_RaAVV_VVL_like",
                                            mu=SD_RaAVV_VVL_npt[attr_states["SD_RaAVV_state"]][0], sigma=SD_RaAVV_VVL_npt[attr_states["SD_RaAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute V&V Design Phase Activity Summary Report Generation
        SD_VVASRG_VVH_like = pm.TruncatedNormal("SD_VVASRG_VVH_like",
                                            mu=SD_VVASRG_VVH_npt[attr_states["SD_VVASRG_state"]][0], sigma=SD_VVASRG_VVH_npt[attr_states["SD_VVASRG_state"]][1],
                                            lower=0, upper=1)
        SD_VVASRG_VVM_like = pm.TruncatedNormal("SD_VVASRG_VVM_like",
                                            mu=SD_VVASRG_VVM_npt[attr_states["SD_VVASRG_state"]][0], sigma=SD_VVASRG_VVM_npt[attr_states["SD_VVASRG_state"]][1],
                                            lower=0, upper=1)
        SD_VVASRG_VVL_like = pm.TruncatedNormal("SD_VVASRG_VVL_like",
                                            mu=SD_VVASRG_VVL_npt[attr_states["SD_VVASRG_state"]][0], sigma=SD_VVASRG_VVL_npt[attr_states["SD_VVASRG_state"]][1],
                                            lower=0, upper=1)
        # m1-m3: a part of marginal probability
        # m1 = P(VV=H)P(attribute states|VV=H)
        # m2 = P(VV=M)P(attribute states|VV=M)
        # m3 = P(VV=L)P(attribute states|VV=L)
        SD_VV_m1 = SD_VVH_prior * SD_DE_VVH_like * SD_IAVV_VVH_like * SD_TAVV_VVH_like * SD_CAVV_VVH_like * SD_HAVV_VVH_like * SD_SAVV_VVH_like * SD_RAVV_VVH_like * SD_VVSCTPG_VVH_like * SD_VVSITPG_VVH_like * SD_VVSCTDG_VVH_like * SD_VVSITDG_VVH_like * SD_VVSQTDG_VVH_like * SD_VVSATDG_VVH_like * SD_CMVV_VVH_like * SD_RaAVV_VVH_like * SD_VVASRG_VVH_like
        SD_VV_m2 = SD_VVM_prior * SD_DE_VVM_like * SD_IAVV_VVM_like * SD_TAVV_VVM_like * SD_CAVV_VVM_like * SD_HAVV_VVM_like * SD_SAVV_VVM_like * SD_RAVV_VVM_like * SD_VVSCTPG_VVM_like * SD_VVSITPG_VVM_like * SD_VVSCTDG_VVM_like * SD_VVSITDG_VVM_like * SD_VVSQTDG_VVM_like * SD_VVSATDG_VVM_like * SD_CMVV_VVM_like * SD_RaAVV_VVM_like * SD_VVASRG_VVM_like
        SD_VV_m3 = SD_VVL_prior * SD_DE_VVL_like * SD_IAVV_VVL_like * SD_TAVV_VVL_like * SD_CAVV_VVL_like * SD_HAVV_VVL_like * SD_SAVV_VVL_like * SD_RAVV_VVL_like * SD_VVSCTPG_VVL_like * SD_VVSITPG_VVL_like * SD_VVSCTDG_VVL_like * SD_VVSITDG_VVL_like * SD_VVSQTDG_VVL_like * SD_VVSATDG_VVL_like * SD_CMVV_VVL_like * SD_RaAVV_VVL_like * SD_VVASRG_VVL_like

        # k = 1 / marginal probability
        SD_VV_k = 1 / (SD_VV_m1 + SD_VV_m2 + SD_VV_m3)

        # posterior probability of V&V quality in SD phase
        SD_VVH_post = pm.Deterministic("SD_VVH_post", SD_VV_k * SD_VV_m1)
        SD_VVM_post = pm.Deterministic("SD_VVM_post", SD_VV_k * SD_VV_m2)
        SD_VVL_post = pm.Deterministic("SD_VVL_post", SD_VV_k * SD_VV_m3)
    return model

def create_IM_Dev_model(attr_states):
    model = pm.Model()

    with model:
        # Dev Attribute model - Implementation phase
        # prior probability of Dev quality in IM phase
        IM_DevH_prior = pm.Beta("IM_DevH_prior", alpha=0.47, beta=1.14)
        IM_DevM_prior = pm.Beta("IM_DevM_prior", alpha=1.70, beta=1.56)
        IM_DevL_prior = pm.Beta("IM_DevL_prior", alpha=2.82, beta=15.00)
        # Attribute Source Code and Source Code Documentation Generation
        IM_SCaSCDG_DevH_like = pm.TruncatedNormal("IM_SCaSCDG_DevH_like",
                                                mu=IM_SCaSCDG_DevH_npt[attr_states["IM_SCaSCDG_state"]][0], sigma=IM_SCaSCDG_DevH_npt[attr_states["IM_SCaSCDG_state"]][1],
                                                lower=0, upper=1)
        IM_SCaSCDG_DevM_like = pm.TruncatedNormal("IM_SCaSCDG_DevM_like",
                                                mu=IM_SCaSCDG_DevM_npt[attr_states["IM_SCaSCDG_state"]][0], sigma=IM_SCaSCDG_DevM_npt[attr_states["IM_SCaSCDG_state"]][1],
                                                lower=0, upper=1)
        IM_SCaSCDG_DevL_like = pm.TruncatedNormal("IM_SCaSCDG_DevL_like",
                                                mu=IM_SCaSCDG_DevL_npt[attr_states["IM_SCaSCDG_state"]][0], sigma=IM_SCaSCDG_DevL_npt[attr_states["IM_SCaSCDG_state"]][1],
                                                lower=0, upper=1)
        # Attribute Traceability Analysis
        IM_TA_DevH_like = pm.TruncatedNormal("IM_TA_DevH_like",
                                            mu=IM_TA_DevH_npt[attr_states["IM_TA_state"]][0], sigma=IM_TA_DevH_npt[attr_states["IM_TA_state"]][1],
                                            lower=0, upper=1)
        IM_TA_DevM_like = pm.TruncatedNormal("IM_TA_DevM_like",
                                            mu=IM_TA_DevM_npt[attr_states["IM_TA_state"]][0], sigma=IM_TA_DevM_npt[attr_states["IM_TA_state"]][1],
                                            lower=0, upper=1)
        IM_TA_DevL_like = pm.TruncatedNormal("IM_TA_DevL_like",
                                            mu=IM_TA_DevL_npt[attr_states["IM_TA_state"]][0], sigma=IM_TA_DevL_npt[attr_states["IM_TA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Criticality Analysis
        IM_CA_DevH_like = pm.TruncatedNormal("IM_CA_DevH_like",
                                            mu=IM_CA_DevH_npt[attr_states["IM_CA_state"]][0], sigma=IM_CA_DevH_npt[attr_states["IM_CA_state"]][1],
                                            lower=0, upper=1)
        IM_CA_DevM_like = pm.TruncatedNormal("IM_CA_DevM_like",
                                            mu=IM_CA_DevM_npt[attr_states["IM_CA_state"]][0], sigma=IM_CA_DevM_npt[attr_states["IM_CA_state"]][1],
                                            lower=0, upper=1)
        IM_CA_DevL_like = pm.TruncatedNormal("IM_CA_DevL_like",
                                            mu=IM_CA_DevL_npt[attr_states["IM_CA_state"]][0], sigma=IM_CA_DevL_npt[attr_states["IM_CA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Hazard Analysis
        IM_HA_DevH_like = pm.TruncatedNormal("IM_HA_DevH_like",
                                            mu=IM_HA_DevH_npt[attr_states["IM_HA_state"]][0], sigma=IM_HA_DevH_npt[attr_states["IM_HA_state"]][1],
                                            lower=0, upper=1)
        IM_HA_DevM_like = pm.TruncatedNormal("IM_HA_DevM_like",
                                            mu=IM_HA_DevM_npt[attr_states["IM_HA_state"]][0], sigma=IM_HA_DevM_npt[attr_states["IM_HA_state"]][1],
                                            lower=0, upper=1)
        IM_HA_DevL_like = pm.TruncatedNormal("IM_HA_DevL_like",
                                            mu=IM_HA_DevL_npt[attr_states["IM_HA_state"]][0], sigma=IM_HA_DevL_npt[attr_states["IM_HA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Security Analysis
        IM_SA_DevH_like = pm.TruncatedNormal("IM_SA_DevH_like",
                                            mu=IM_SA_DevH_npt[attr_states["IM_SA_state"]][0], sigma=IM_SA_DevH_npt[attr_states["IM_SA_state"]][1],
                                            lower=0, upper=1)
        IM_SA_DevM_like = pm.TruncatedNormal("IM_SA_DevM_like",
                                            mu=IM_SA_DevM_npt[attr_states["IM_SA_state"]][0], sigma=IM_SA_DevM_npt[attr_states["IM_SA_state"]][1],
                                            lower=0, upper=1)
        IM_SA_DevL_like = pm.TruncatedNormal("IM_SA_DevL_like",
                                            mu=IM_SA_DevL_npt[attr_states["IM_SA_state"]][0], sigma=IM_SA_DevL_npt[attr_states["IM_SA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Risk Analysis
        IM_RA_DevH_like = pm.TruncatedNormal("IM_RA_DevH_like",
                                            mu=IM_RA_DevH_npt[attr_states["IM_RA_state"]][0], sigma=IM_RA_DevH_npt[attr_states["IM_RA_state"]][1],
                                            lower=0, upper=1)
        IM_RA_DevM_like = pm.TruncatedNormal("IM_RA_DevM_like",
                                            mu=IM_RA_DevM_npt[attr_states["IM_RA_state"]][0], sigma=IM_RA_DevM_npt[attr_states["IM_RA_state"]][1],
                                            lower=0, upper=1)
        IM_RA_DevL_like = pm.TruncatedNormal("IM_RA_DevL_like",
                                            mu=IM_RA_DevL_npt[attr_states["IM_RA_state"]][0], sigma=IM_RA_DevL_npt[attr_states["IM_RA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Component Test Case Generation
        IM_CTCG_DevH_like = pm.TruncatedNormal("IM_CTCG_DevH_like",
                                            mu=IM_CTCG_DevH_npt[attr_states["IM_CTCG_state"]][0], sigma=IM_CTCG_DevH_npt[attr_states["IM_CTCG_state"]][1],
                                            lower=0, upper=1)
        IM_CTCG_DevM_like = pm.TruncatedNormal("IM_CTCG_DevM_like",
                                            mu=IM_CTCG_DevM_npt[attr_states["IM_CTCG_state"]][0], sigma=IM_CTCG_DevM_npt[attr_states["IM_CTCG_state"]][1],
                                            lower=0, upper=1)
        IM_CTCG_DevL_like = pm.TruncatedNormal("IM_CTCG_DevL_like",
                                            mu=IM_CTCG_DevL_npt[attr_states["IM_CTCG_state"]][0], sigma=IM_CTCG_DevL_npt[attr_states["IM_CTCG_state"]][1],
                                            lower=0, upper=1)
        # Attribute Software Integration Test Case Generation
        IM_SITCG_DevH_like = pm.TruncatedNormal("IM_SITCG_DevH_like",
                                                mu=IM_SITCG_DevH_npt[attr_states["IM_SITCG_state"]][0], sigma=IM_SITCG_DevH_npt[attr_states["IM_SITCG_state"]][1],
                                                lower=0, upper=1)
        IM_SITCG_DevM_like = pm.TruncatedNormal("IM_SITCG_DevM_like",
                                                mu=IM_SITCG_DevM_npt[attr_states["IM_SITCG_state"]][0], sigma=IM_SITCG_DevM_npt[attr_states["IM_SITCG_state"]][1],
                                                lower=0, upper=1)
        IM_SITCG_DevL_like = pm.TruncatedNormal("IM_SITCG_DevL_like",
                                                mu=IM_SITCG_DevL_npt[attr_states["IM_SITCG_state"]][0], sigma=IM_SITCG_DevL_npt[attr_states["IM_SITCG_state"]][1],
                                                lower=0, upper=1)
        # Attribute Software Quantification Test Case Generation
        IM_SQTCG_DevH_like = pm.TruncatedNormal("IM_SQTCG_DevH_like",
                                                mu=IM_SQTCG_DevH_npt[attr_states["IM_SQTCG_state"]][0], sigma=IM_SQTCG_DevH_npt[attr_states["IM_SQTCG_state"]][1],
                                                lower=0, upper=1)
        IM_SQTCG_DevM_like = pm.TruncatedNormal("IM_SQTCG_DevM_like",
                                                mu=IM_SQTCG_DevM_npt[attr_states["IM_SQTCG_state"]][0], sigma=IM_SQTCG_DevM_npt[attr_states["IM_SQTCG_state"]][1],
                                                lower=0, upper=1)
        IM_SQTCG_DevL_like = pm.TruncatedNormal("IM_SQTCG_DevL_like",
                                                mu=IM_SQTCG_DevL_npt[attr_states["IM_SQTCG_state"]][0], sigma=IM_SQTCG_DevL_npt[attr_states["IM_SQTCG_state"]][1],
                                                lower=0, upper=1)
        # Attribute Software Acceptance Test Case Generation
        IM_SATCG_DevH_like = pm.TruncatedNormal("IM_SATCG_DevH_like",
                                                mu=IM_SATCG_DevH_npt[attr_states["IM_SATCG_state"]][0], sigma=IM_SATCG_DevH_npt[attr_states["IM_SATCG_state"]][1],
                                                lower=0, upper=1)
        IM_SATCG_DevM_like = pm.TruncatedNormal("IM_SATCG_DevM_like",
                                                mu=IM_SATCG_DevM_npt[attr_states["IM_SATCG_state"]][0], sigma=IM_SATCG_DevM_npt[attr_states["IM_SATCG_state"]][1],
                                                lower=0, upper=1)
        IM_SATCG_DevL_like = pm.TruncatedNormal("IM_SATCG_DevL_like",
                                                mu=IM_SATCG_DevL_npt[attr_states["IM_SATCG_state"]][0], sigma=IM_SATCG_DevL_npt[attr_states["IM_SATCG_state"]][1],
                                                lower=0, upper=1)
        # Attribute Software Component Test Procedure Generation
        IM_SCTPG_DevH_like = pm.TruncatedNormal("IM_SCTPG_DevH_like",
                                                mu=IM_SCTPG_DevH_npt[attr_states["IM_SCTPG_state"]][0], sigma=IM_SCTPG_DevH_npt[attr_states["IM_SCTPG_state"]][1],
                                                lower=0, upper=1)
        IM_SCTPG_DevM_like = pm.TruncatedNormal("IM_SCTPG_DevM_like",
                                                mu=IM_SCTPG_DevM_npt[attr_states["IM_SCTPG_state"]][0], sigma=IM_SCTPG_DevM_npt[attr_states["IM_SCTPG_state"]][1],
                                                lower=0, upper=1)
        IM_SCTPG_DevL_like = pm.TruncatedNormal("IM_SCTPG_DevL_like",
                                                mu=IM_SCTPG_DevL_npt[attr_states["IM_SCTPG_state"]][0], sigma=IM_SCTPG_DevL_npt[attr_states["IM_SCTPG_state"]][1],
                                                lower=0, upper=1)
        # Attribute Software Integration Test Procedure Generation
        IM_SITPG_DevH_like = pm.TruncatedNormal("IM_SITPG_DevH_like",
                                                mu=IM_SITPG_DevH_npt[attr_states["IM_SITPG_state"]][0], sigma=IM_SITPG_DevH_npt[attr_states["IM_SITPG_state"]][1],
                                                lower=0, upper=1)
        IM_SITPG_DevM_like = pm.TruncatedNormal("IM_SITPG_DevM_like",
                                                mu=IM_SITPG_DevM_npt[attr_states["IM_SITPG_state"]][0], sigma=IM_SITPG_DevM_npt[attr_states["IM_SITPG_state"]][1],
                                                lower=0, upper=1)
        IM_SITPG_DevL_like = pm.TruncatedNormal("IM_SITPG_DevL_like",
                                                mu=IM_SITPG_DevL_npt[attr_states["IM_SITPG_state"]][0], sigma=IM_SITPG_DevL_npt[attr_states["IM_SITPG_state"]][1],
                                                lower=0, upper=1)
        # Attribute Software Quantification Test Procedure Generation
        IM_SQTPG_DevH_like = pm.TruncatedNormal("IM_SQTPG_DevH_like",
                                                mu=IM_SQTPG_DevH_npt[attr_states["IM_SQTPG_state"]][0], sigma=IM_SQTPG_DevH_npt[attr_states["IM_SQTPG_state"]][1],
                                                lower=0, upper=1)
        IM_SQTPG_DevM_like = pm.TruncatedNormal("IM_SQTPG_DevM_like",
                                                mu=IM_SQTPG_DevM_npt[attr_states["IM_SQTPG_state"]][0], sigma=IM_SQTPG_DevM_npt[attr_states["IM_SQTPG_state"]][1],
                                                lower=0, upper=1)
        IM_SQTPG_DevL_like = pm.TruncatedNormal("IM_SQTPG_DevL_like",
                                                mu=IM_SQTPG_DevL_npt[attr_states["IM_SQTPG_state"]][0], sigma=IM_SQTPG_DevL_npt[attr_states["IM_SQTPG_state"]][1],
                                                lower=0, upper=1)
        # Attribute Configuration Management
        IM_CM_DevH_like = pm.TruncatedNormal("IM_CM_DevH_like",
                                            mu=IM_CM_DevH_npt[attr_states["IM_CM_state"]][0], sigma=IM_CM_DevH_npt[attr_states["IM_CM_state"]][1],
                                            lower=0, upper=1)
        IM_CM_DevM_like = pm.TruncatedNormal("IM_CM_DevM_like",
                                            mu=IM_CM_DevM_npt[attr_states["IM_CM_state"]][0], sigma=IM_CM_DevM_npt[attr_states["IM_CM_state"]][1],
                                            lower=0, upper=1)
        IM_CM_DevL_like = pm.TruncatedNormal("IM_CM_DevL_like",
                                            mu=IM_CM_DevL_npt[attr_states["IM_CM_state"]][0], sigma=IM_CM_DevL_npt[attr_states["IM_CM_state"]][1],
                                            lower=0, upper=1)
        # Attribute Reviews and Audits
        IM_RaA_DevH_like = pm.TruncatedNormal("IM_RaA_DevH_like",
                                                mu=IM_RaA_DevH_npt[attr_states["IM_RaA_state"]][0], sigma=IM_RaA_DevH_npt[attr_states["IM_RaA_state"]][1],
                                                lower=0, upper=1)
        IM_RaA_DevM_like = pm.TruncatedNormal("IM_RaA_DevM_like",
                                                mu=IM_RaA_DevM_npt[attr_states["IM_RaA_state"]][0], sigma=IM_RaA_DevM_npt[attr_states["IM_RaA_state"]][1],
                                                lower=0, upper=1)
        IM_RaA_DevL_like = pm.TruncatedNormal("IM_RaA_DevL_like",
                                                mu=IM_RaA_DevL_npt[attr_states["IM_RaA_state"]][0], sigma=IM_RaA_DevL_npt[attr_states["IM_RaA_state"]][1],
                                                lower=0, upper=1)
        # Attribute Software Component Test Execution
        IM_SCTE_DevH_like = pm.TruncatedNormal("IM_SCTE_DevH_like",
                                                mu=IM_SCTE_DevH_npt[attr_states["IM_SCTE_state"]][0], sigma=IM_SCTE_DevH_npt[attr_states["IM_SCTE_state"]][1],
                                                lower=0, upper=1)
        IM_SCTE_DevM_like = pm.TruncatedNormal("IM_SCTE_DevM_like",
                                                mu=IM_SCTE_DevM_npt[attr_states["IM_SCTE_state"]][0], sigma=IM_SCTE_DevM_npt[attr_states["IM_SCTE_state"]][1],
                                                lower=0, upper=1)
        IM_SCTE_DevL_like = pm.TruncatedNormal("IM_SCTE_DevL_like",
                                                mu=IM_SCTE_DevL_npt[attr_states["IM_SCTE_state"]][0], sigma=IM_SCTE_DevL_npt[attr_states["IM_SCTE_state"]][1],
                                                lower=0, upper=1)
        # m1-m3: a part of marginal probability
        # m1 = P(Dev=H)P(attribute states|Dev=H)
        # m2 = P(Dev=M)P(attribute states|Dev=M)
        # m3 = P(Dev=L)P(attribute states|Dev=L)
        IM_Dev_m1 = IM_DevH_prior * IM_SCaSCDG_DevH_like * IM_TA_DevH_like * IM_CA_DevH_like * IM_HA_DevH_like * IM_SA_DevH_like * IM_RA_DevH_like * IM_CTCG_DevH_like * IM_SITCG_DevH_like * IM_SQTCG_DevH_like * IM_SATCG_DevH_like * IM_SCTPG_DevH_like * IM_SITPG_DevH_like * IM_SQTPG_DevH_like * IM_CM_DevH_like * IM_RaA_DevH_like * IM_SCTE_DevH_like
        IM_Dev_m2 = IM_DevM_prior * IM_SCaSCDG_DevM_like * IM_TA_DevM_like * IM_CA_DevM_like * IM_HA_DevM_like * IM_SA_DevM_like * IM_RA_DevM_like * IM_CTCG_DevM_like * IM_SITCG_DevM_like * IM_SQTCG_DevM_like * IM_SATCG_DevM_like * IM_SCTPG_DevM_like * IM_SITPG_DevM_like * IM_SQTPG_DevM_like * IM_CM_DevM_like * IM_RaA_DevM_like * IM_SCTE_DevM_like
        IM_Dev_m3 = IM_DevL_prior * IM_SCaSCDG_DevL_like * IM_TA_DevL_like * IM_CA_DevL_like * IM_HA_DevL_like * IM_SA_DevL_like * IM_RA_DevL_like * IM_CTCG_DevL_like * IM_SITCG_DevL_like * IM_SQTCG_DevL_like * IM_SATCG_DevL_like * IM_SCTPG_DevL_like * IM_SITPG_DevL_like * IM_SQTPG_DevL_like * IM_CM_DevL_like * IM_RaA_DevL_like * IM_SCTE_DevL_like

        # k = 1 / marginal probability
        IM_Dev_k = 1 / (IM_Dev_m1 + IM_Dev_m2 + IM_Dev_m3)
        # posterior probability of Dev quality in IM phase
        IM_DevH_post = pm.Deterministic("IM_DevH_post", IM_Dev_k * IM_Dev_m1)
        IM_DevM_post = pm.Deterministic("IM_DevM_post", IM_Dev_k * IM_Dev_m2)
        IM_DevL_post = pm.Deterministic("IM_DevL_post", IM_Dev_k * IM_Dev_m3)
    return model

def create_IM_VV_model(attr_states):
    model = pm.Model()

    with model:
        # V&V Attribute model - Implementation phase
        # prior probability of V&V quality in IM phase
        IM_VVH_prior = pm.Beta("IM_VVH_prior", alpha=0.49, beta=1.27)
        IM_VVM_prior = pm.Beta("IM_VVM_prior", alpha=2.12, beta=1.82)
        IM_VVL_prior = pm.Beta("IM_VVL_prior", alpha=1.90, beta=9.90)
        # Attribute Source Code and Source Code Documentation Evaluation
        IM_SCaSCDE_VVH_like = pm.TruncatedNormal("IM_SCaSCDE_VVH_like",
                                                mu=IM_SCaSCDE_VVH_npt[attr_states["IM_SCaSCDE_state"]][0], sigma=IM_SCaSCDE_VVH_npt[attr_states["IM_SCaSCDE_state"]][1],
                                                lower=0, upper=1)
        IM_SCaSCDE_VVM_like = pm.TruncatedNormal("IM_SCaSCDE_VVM_like",
                                                mu=IM_SCaSCDE_VVM_npt[attr_states["IM_SCaSCDE_state"]][0], sigma=IM_SCaSCDE_VVM_npt[attr_states["IM_SCaSCDE_state"]][1],
                                                lower=0, upper=1)
        IM_SCaSCDE_VVL_like = pm.TruncatedNormal("IM_SCaSCDE_VVL_like",
                                                mu=IM_SCaSCDE_VVL_npt[attr_states["IM_SCaSCDE_state"]][0], sigma=IM_SCaSCDE_VVL_npt[attr_states["IM_SCaSCDE_state"]][1],
                                                lower=0, upper=1)
        # Attribute Interface Analysis V&V
        IM_IAVV_VVH_like = pm.TruncatedNormal("IM_IAVV_VVH_like",
                                            mu=IM_IAVV_VVH_npt[attr_states["IM_IAVV_state"]][0], sigma=IM_IAVV_VVH_npt[attr_states["IM_IAVV_state"]][1],
                                            lower=0, upper=1)
        IM_IAVV_VVM_like = pm.TruncatedNormal("IM_IAVV_VVM_like",
                                            mu=IM_IAVV_VVM_npt[attr_states["IM_IAVV_state"]][0], sigma=IM_IAVV_VVM_npt[attr_states["IM_IAVV_state"]][1],
                                            lower=0, upper=1)
        IM_IAVV_VVL_like = pm.TruncatedNormal("IM_IAVV_VVL_like",
                                            mu=IM_IAVV_VVL_npt[attr_states["IM_IAVV_state"]][0], sigma=IM_IAVV_VVL_npt[attr_states["IM_IAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Traceability Analysis V&V
        IM_TAVV_VVH_like = pm.TruncatedNormal("IM_TAVV_VVH_like",
                                            mu=IM_TAVV_VVH_npt[attr_states["IM_TAVV_state"]][0], sigma=IM_TAVV_VVH_npt[attr_states["IM_TAVV_state"]][1],
                                            lower=0, upper=1)
        IM_TAVV_VVM_like = pm.TruncatedNormal("IM_TAVV_VVM_like",
                                            mu=IM_TAVV_VVM_npt[attr_states["IM_TAVV_state"]][0], sigma=IM_TAVV_VVM_npt[attr_states["IM_TAVV_state"]][1],
                                            lower=0, upper=1)
        IM_TAVV_VVL_like = pm.TruncatedNormal("IM_TAVV_VVL_like",
                                            mu=IM_TAVV_VVL_npt[attr_states["IM_TAVV_state"]][0], sigma=IM_TAVV_VVL_npt[attr_states["IM_TAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Criticality Analysis V&V
        IM_CAVV_VVH_like = pm.TruncatedNormal("IM_CAVV_VVH_like",
                                            mu=IM_CAVV_VVH_npt[attr_states["IM_CAVV_state"]][0], sigma=IM_CAVV_VVH_npt[attr_states["IM_CAVV_state"]][1],
                                            lower=0, upper=1)
        IM_CAVV_VVM_like = pm.TruncatedNormal("IM_CAVV_VVM_like",
                                            mu=IM_CAVV_VVM_npt[attr_states["IM_CAVV_state"]][0], sigma=IM_CAVV_VVM_npt[attr_states["IM_CAVV_state"]][1],
                                            lower=0, upper=1)
        IM_CAVV_VVL_like = pm.TruncatedNormal("IM_CAVV_VVL_like",
                                            mu=IM_CAVV_VVL_npt[attr_states["IM_CAVV_state"]][0], sigma=IM_CAVV_VVL_npt[attr_states["IM_CAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Hazard Analysis V&V
        IM_HAVV_VVH_like = pm.TruncatedNormal("IM_HAVV_VVH_like",
                                            mu=IM_HAVV_VVH_npt[attr_states["IM_HAVV_state"]][0], sigma=IM_HAVV_VVH_npt[attr_states["IM_HAVV_state"]][1],
                                            lower=0, upper=1)
        IM_HAVV_VVM_like = pm.TruncatedNormal("IM_HAVV_VVM_like",
                                            mu=IM_HAVV_VVM_npt[attr_states["IM_HAVV_state"]][0], sigma=IM_HAVV_VVM_npt[attr_states["IM_HAVV_state"]][1],
                                            lower=0, upper=1)
        IM_HAVV_VVL_like = pm.TruncatedNormal("IM_HAVV_VVL_like",
                                            mu=IM_HAVV_VVL_npt[attr_states["IM_HAVV_state"]][0], sigma=IM_HAVV_VVL_npt[attr_states["IM_HAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Security Analysis V&V
        IM_SAVV_VVH_like = pm.TruncatedNormal("IM_SAVV_VVH_like",
                                            mu=IM_SAVV_VVH_npt[attr_states["IM_SAVV_state"]][0], sigma=IM_SAVV_VVH_npt[attr_states["IM_SAVV_state"]][1],
                                            lower=0, upper=1)
        IM_SAVV_VVM_like = pm.TruncatedNormal("IM_SAVV_VVM_like",
                                            mu=IM_SAVV_VVM_npt[attr_states["IM_SAVV_state"]][0], sigma=IM_SAVV_VVM_npt[attr_states["IM_SAVV_state"]][1],
                                            lower=0, upper=1)
        IM_SAVV_VVL_like = pm.TruncatedNormal("IM_SAVV_VVL_like",
                                            mu=IM_SAVV_VVL_npt[attr_states["IM_SAVV_state"]][0], sigma=IM_SAVV_VVL_npt[attr_states["IM_SAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Risk Analysis V&V
        IM_RAVV_VVH_like = pm.TruncatedNormal("IM_RAVV_VVH_like",
                                            mu=IM_RAVV_VVH_npt[attr_states["IM_RAVV_state"]][0], sigma=IM_RAVV_VVH_npt[attr_states["IM_RAVV_state"]][1],
                                            lower=0, upper=1)
        IM_RAVV_VVM_like = pm.TruncatedNormal("IM_RAVV_VVM_like",
                                            mu=IM_RAVV_VVM_npt[attr_states["IM_RAVV_state"]][0], sigma=IM_RAVV_VVM_npt[attr_states["IM_RAVV_state"]][1],
                                            lower=0, upper=1)
        IM_RAVV_VVL_like = pm.TruncatedNormal("IM_RAVV_VVL_like",
                                            mu=IM_RAVV_VVL_npt[attr_states["IM_RAVV_state"]][0], sigma=IM_RAVV_VVL_npt[attr_states["IM_RAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute V&V Software Component Test Case Generation
        IM_VVSCTCG_VVH_like = pm.TruncatedNormal("IM_VVSCTCG_VVH_like",
                                                mu=IM_VVSCTCG_VVH_npt[attr_states["IM_VVSCTCG_state"]][0], sigma=IM_VVSCTCG_VVH_npt[attr_states["IM_VVSCTCG_state"]][1],
                                                lower=0, upper=1)
        IM_VVSCTCG_VVM_like = pm.TruncatedNormal("IM_VVSCTCG_VVM_like",
                                                mu=IM_VVSCTCG_VVM_npt[attr_states["IM_VVSCTCG_state"]][0], sigma=IM_VVSCTCG_VVM_npt[attr_states["IM_VVSCTCG_state"]][1],
                                                lower=0, upper=1)
        IM_VVSCTCG_VVL_like = pm.TruncatedNormal("IM_VVSCTCG_VVL_like",
                                                mu=IM_VVSCTCG_VVL_npt[attr_states["IM_VVSCTCG_state"]][0], sigma=IM_VVSCTCG_VVL_npt[attr_states["IM_VVSCTCG_state"]][1],
                                                lower=0, upper=1)
        # Attribute V&V Software Integration Test Case Generation
        IM_VVSITCG_VVH_like = pm.TruncatedNormal("IM_VVSITCG_VVH_like",
                                                mu=IM_VVSITCG_VVH_npt[attr_states["IM_VVSITCG_state"]][0], sigma=IM_VVSITCG_VVH_npt[attr_states["IM_VVSITCG_state"]][1],
                                                lower=0, upper=1)
        IM_VVSITCG_VVM_like = pm.TruncatedNormal("IM_VVSITCG_VVM_like",
                                                mu=IM_VVSITCG_VVM_npt[attr_states["IM_VVSITCG_state"]][0], sigma=IM_VVSITCG_VVM_npt[attr_states["IM_VVSITCG_state"]][1],
                                                lower=0, upper=1)
        IM_VVSITCG_VVL_like = pm.TruncatedNormal("IM_VVSITCG_VVL_like",
                                                mu=IM_VVSITCG_VVL_npt[attr_states["IM_VVSITCG_state"]][0], sigma=IM_VVSITCG_VVL_npt[attr_states["IM_VVSITCG_state"]][1],
                                                lower=0, upper=1)
        # Attribute V&V Software Quantification Test Case Generation
        IM_VVSQTCG_VVH_like = pm.TruncatedNormal("IM_VVSQTCG_VVH_like",
                                                mu=IM_VVSQTCG_VVH_npt[attr_states["IM_VVSQTCG_state"]][0], sigma=IM_VVSQTCG_VVH_npt[attr_states["IM_VVSQTCG_state"]][1],
                                                lower=0, upper=1)
        IM_VVSQTCG_VVM_like = pm.TruncatedNormal("IM_VVSQTCG_VVM_like",
                                                mu=IM_VVSQTCG_VVM_npt[attr_states["IM_VVSQTCG_state"]][0], sigma=IM_VVSQTCG_VVM_npt[attr_states["IM_VVSQTCG_state"]][1],
                                                lower=0, upper=1)
        IM_VVSQTCG_VVL_like = pm.TruncatedNormal("IM_VVSQTCG_VVL_like",
                                                mu=IM_VVSQTCG_VVL_npt[attr_states["IM_VVSQTCG_state"]][0], sigma=IM_VVSQTCG_VVL_npt[attr_states["IM_VVSQTCG_state"]][1],
                                                lower=0, upper=1)
        # Attribute V&V Software Acceptance Test Case Generation
        IM_VVSATCG_VVH_like = pm.TruncatedNormal("IM_VVSATCG_VVH_like",
                                                mu=IM_VVSATCG_VVH_npt[attr_states["IM_VVSATCG_state"]][0], sigma=IM_VVSATCG_VVH_npt[attr_states["IM_VVSATCG_state"]][1],
                                                lower=0, upper=1)
        IM_VVSATCG_VVM_like = pm.TruncatedNormal("IM_VVSATCG_VVM_like",
                                                mu=IM_VVSATCG_VVM_npt[attr_states["IM_VVSATCG_state"]][0], sigma=IM_VVSATCG_VVM_npt[attr_states["IM_VVSATCG_state"]][1],
                                                lower=0, upper=1)
        IM_VVSATCG_VVL_like = pm.TruncatedNormal("IM_VVSATCG_VVL_like",
                                                mu=IM_VVSATCG_VVL_npt[attr_states["IM_VVSATCG_state"]][0], sigma=IM_VVSATCG_VVL_npt[attr_states["IM_VVSATCG_state"]][1],
                                                lower=0, upper=1)
        # Attribute V&V Software Component Test Procedure Generation
        IM_VVSCTPG_VVH_like = pm.TruncatedNormal("IM_VVSCTPG_VVH_like",
                                                mu=IM_VVSCTPG_VVH_npt[attr_states["IM_VVSCTPG_state"]][0], sigma=IM_VVSCTPG_VVH_npt[attr_states["IM_VVSCTPG_state"]][1],
                                                lower=0, upper=1)
        IM_VVSCTPG_VVM_like = pm.TruncatedNormal("IM_VVSCTPG_VVM_like",
                                                mu=IM_VVSCTPG_VVM_npt[attr_states["IM_VVSCTPG_state"]][0], sigma=IM_VVSCTPG_VVM_npt[attr_states["IM_VVSCTPG_state"]][1],
                                                lower=0, upper=1)
        IM_VVSCTPG_VVL_like = pm.TruncatedNormal("IM_VVSCTPG_VVL_like",
                                                mu=IM_VVSCTPG_VVL_npt[attr_states["IM_VVSCTPG_state"]][0], sigma=IM_VVSCTPG_VVL_npt[attr_states["IM_VVSCTPG_state"]][1],
                                                lower=0, upper=1)
        # Attribute V&V Software Integration Test Procedure Generation
        IM_VVSITPG_VVH_like = pm.TruncatedNormal("IM_VVSITPG_VVH_like",
                                                mu=IM_VVSITPG_VVH_npt[attr_states["IM_VVSITPG_state"]][0], sigma=IM_VVSITPG_VVH_npt[attr_states["IM_VVSITPG_state"]][1],
                                                lower=0, upper=1)
        IM_VVSITPG_VVM_like = pm.TruncatedNormal("IM_VVSITPG_VVM_like",
                                                mu=IM_VVSITPG_VVM_npt[attr_states["IM_VVSITPG_state"]][0], sigma=IM_VVSITPG_VVM_npt[attr_states["IM_VVSITPG_state"]][1],
                                                lower=0, upper=1)
        IM_VVSITPG_VVL_like = pm.TruncatedNormal("IM_VVSITPG_VVL_like",
                                                mu=IM_VVSITPG_VVL_npt[attr_states["IM_VVSITPG_state"]][0], sigma=IM_VVSITPG_VVL_npt[attr_states["IM_VVSITPG_state"]][1],
                                                lower=0, upper=1)
        # Attribute V&V Software Quantification Test Procedure Generation
        IM_VVSQTPG_VVH_like = pm.TruncatedNormal("IM_VVSQTPG_VVH_like",
                                                mu=IM_VVSQTPG_VVH_npt[attr_states["IM_VVSQTPG_state"]][0], sigma=IM_VVSQTPG_VVH_npt[attr_states["IM_VVSQTPG_state"]][1],
                                                lower=0, upper=1)
        IM_VVSQTPG_VVM_like = pm.TruncatedNormal("IM_VVSQTPG_VVM_like",
                                                mu=IM_VVSQTPG_VVM_npt[attr_states["IM_VVSQTPG_state"]][0], sigma=IM_VVSQTPG_VVM_npt[attr_states["IM_VVSQTPG_state"]][1],
                                                lower=0, upper=1)
        IM_VVSQTPG_VVL_like = pm.TruncatedNormal("IM_VVSQTPG_VVL_like",
                                                mu=IM_VVSQTPG_VVL_npt[attr_states["IM_VVSQTPG_state"]][0], sigma=IM_VVSQTPG_VVL_npt[attr_states["IM_VVSQTPG_state"]][1],
                                                lower=0, upper=1)
        # Attribute V&V Software Component Test Execution
        IM_VVSCTE_VVH_like = pm.TruncatedNormal("IM_VVSCTE_VVH_like",
                                                mu=IM_VVSCTE_VVH_npt[attr_states["IM_VVSCTE_state"]][0], sigma=IM_VVSCTE_VVH_npt[attr_states["IM_VVSCTE_state"]][1],
                                                lower=0, upper=1)
        IM_VVSCTE_VVM_like = pm.TruncatedNormal("IM_VVSCTE_VVM_like",
                                                mu=IM_VVSCTE_VVM_npt[attr_states["IM_VVSCTE_state"]][0], sigma=IM_VVSCTE_VVM_npt[attr_states["IM_VVSCTE_state"]][1],
                                                lower=0, upper=1)
        IM_VVSCTE_VVL_like = pm.TruncatedNormal("IM_VVSCTE_VVL_like",
                                                mu=IM_VVSCTE_VVL_npt[attr_states["IM_VVSCTE_state"]][0], sigma=IM_VVSCTE_VVL_npt[attr_states["IM_VVSCTE_state"]][1],
                                                lower=0, upper=1)
        # Attribute Configuration Management V&V
        IM_CMVV_VVH_like = pm.TruncatedNormal("IM_CMVV_VVH_like",
                                            mu=IM_CMVV_VVH_npt[attr_states["IM_CMVV_state"]][0], sigma=IM_CMVV_VVH_npt[attr_states["IM_CMVV_state"]][1],
                                            lower=0, upper=1)
        IM_CMVV_VVM_like = pm.TruncatedNormal("IM_CMVV_VVM_like",
                                            mu=IM_CMVV_VVM_npt[attr_states["IM_CMVV_state"]][0], sigma=IM_CMVV_VVM_npt[attr_states["IM_CMVV_state"]][1],
                                            lower=0, upper=1)
        IM_CMVV_VVL_like = pm.TruncatedNormal("IM_CMVV_VVL_like",
                                            mu=IM_CMVV_VVL_npt[attr_states["IM_CMVV_state"]][0], sigma=IM_CMVV_VVL_npt[attr_states["IM_CMVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Reviews and Audits V&V
        IM_RaAVV_VVH_like = pm.TruncatedNormal("IM_RaAVV_VVH_like",
                                            mu=IM_RaAVV_VVH_npt[attr_states["IM_RaAVV_state"]][0], sigma=IM_RaAVV_VVH_npt[attr_states["IM_RaAVV_state"]][1],
                                            lower=0, upper=1)
        IM_RaAVV_VVM_like = pm.TruncatedNormal("IM_RaAVV_VVM_like",
                                            mu=IM_RaAVV_VVM_npt[attr_states["IM_RaAVV_state"]][0], sigma=IM_RaAVV_VVM_npt[attr_states["IM_RaAVV_state"]][1],
                                            lower=0, upper=1)
        IM_RaAVV_VVL_like = pm.TruncatedNormal("IM_RaAVV_VVL_like",
                                            mu=IM_RaAVV_VVL_npt[attr_states["IM_RaAVV_state"]][0], sigma=IM_RaAVV_VVL_npt[attr_states["IM_RaAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute V&V Implementation Phase Activity Summary Report Generation
        IM_VVASRG_VVH_like = pm.TruncatedNormal("IM_VVASRG_VVH_like",
                                                mu=IM_VVASRG_VVH_npt[attr_states["IM_VVASRG_state"]][0], sigma=IM_VVASRG_VVH_npt[attr_states["IM_VVASRG_state"]][1],
                                                lower=0, upper=1)
        IM_VVASRG_VVM_like = pm.TruncatedNormal("IM_VVASRG_VVM_like",
                                                mu=IM_VVASRG_VVM_npt[attr_states["IM_VVASRG_state"]][0], sigma=IM_VVASRG_VVM_npt[attr_states["IM_VVASRG_state"]][1],
                                                lower=0, upper=1)
        IM_VVASRG_VVL_like = pm.TruncatedNormal("IM_VVASRG_VVL_like",
                                                mu=IM_VVASRG_VVL_npt[attr_states["IM_VVASRG_state"]][0], sigma=IM_VVASRG_VVL_npt[attr_states["IM_VVASRG_state"]][1],
                                                lower=0, upper=1)
        # m1-m3: a part of marginal probability
        # m1 = P(VV=H)P(attribute states|VV=H)
        # m2 = P(VV=M)P(attribute states|VV=M)
        # m3 = P(VV=L)P(attribute states|VV=L)
        IM_VV_m1 = IM_VVH_prior * IM_SCaSCDE_VVH_like * IM_IAVV_VVH_like * IM_TAVV_VVH_like * IM_CAVV_VVH_like * IM_HAVV_VVH_like * IM_SAVV_VVH_like * IM_RAVV_VVH_like * IM_VVSCTCG_VVH_like * IM_VVSITCG_VVH_like * IM_VVSQTCG_VVH_like * IM_VVSATCG_VVH_like * IM_VVSCTPG_VVH_like * IM_VVSITPG_VVH_like * IM_VVSQTPG_VVH_like * IM_VVSCTE_VVH_like * IM_CMVV_VVH_like * IM_RaAVV_VVH_like * IM_VVASRG_VVH_like
        IM_VV_m2 = IM_VVM_prior * IM_SCaSCDE_VVM_like * IM_IAVV_VVM_like * IM_TAVV_VVM_like * IM_CAVV_VVM_like * IM_HAVV_VVM_like * IM_SAVV_VVM_like * IM_RAVV_VVM_like * IM_VVSCTCG_VVM_like * IM_VVSITCG_VVM_like * IM_VVSQTCG_VVM_like * IM_VVSATCG_VVM_like * IM_VVSCTPG_VVM_like * IM_VVSITPG_VVM_like * IM_VVSQTPG_VVM_like * IM_VVSCTE_VVM_like * IM_CMVV_VVM_like * IM_RaAVV_VVM_like * IM_VVASRG_VVM_like
        IM_VV_m3 = IM_VVL_prior * IM_SCaSCDE_VVL_like * IM_IAVV_VVL_like * IM_TAVV_VVL_like * IM_CAVV_VVL_like * IM_HAVV_VVL_like * IM_SAVV_VVL_like * IM_RAVV_VVL_like * IM_VVSCTCG_VVL_like * IM_VVSITCG_VVL_like * IM_VVSQTCG_VVL_like * IM_VVSATCG_VVL_like * IM_VVSCTPG_VVL_like * IM_VVSITPG_VVL_like * IM_VVSQTPG_VVL_like * IM_VVSCTE_VVL_like * IM_CMVV_VVL_like * IM_RaAVV_VVL_like * IM_VVASRG_VVL_like

        # k = 1 / marginal probability
        IM_VV_k = 1 / (IM_VV_m1 + IM_VV_m2 + IM_VV_m3)

        # posterior probability of Dev quality in IM phase
        IM_VVH_post = pm.Deterministic("IM_VVH_post", IM_VV_k * IM_VV_m1)
        IM_VVM_post = pm.Deterministic("IM_VVM_post", IM_VV_k * IM_VV_m2)
        IM_VVL_post = pm.Deterministic("IM_VVL_post", IM_VV_k * IM_VV_m3)
    return model

def create_ST_Dev_model(attr_states):
    model = pm.Model()
    with model:
        # Dev Attribute model - Test phase
        # prior probability of Dev quality in ST phase
        ST_DevH_prior = pm.Beta("ST_DevH_prior", alpha=0.45, beta=1.29)
        ST_DevM_prior = pm.Beta("ST_DevM_prior", alpha=1.75, beta=1.19)
        ST_DevL_prior = pm.Beta("ST_DevL_prior", alpha=0.83, beta=5.42)
        # Attribute Software Integration Test Execution
        ST_SITE_DevH_like = pm.TruncatedNormal("ST_SITE_DevH_like",
                                            mu=ST_SITE_DevH_npt[attr_states["ST_SITE_state"]][0], sigma=ST_SITE_DevH_npt[attr_states["ST_SITE_state"]][1],
                                            lower=0, upper=1)
        ST_SITE_DevM_like = pm.TruncatedNormal("ST_SITE_DevM_like",
                                            mu=ST_SITE_DevM_npt[attr_states["ST_SITE_state"]][0], sigma=ST_SITE_DevM_npt[attr_states["ST_SITE_state"]][1],
                                            lower=0, upper=1)
        ST_SITE_DevL_like = pm.TruncatedNormal("ST_SITE_DevL_like",
                                            mu=ST_SITE_DevL_npt[attr_states["ST_SITE_state"]][0], sigma=ST_SITE_DevL_npt[attr_states["ST_SITE_state"]][1],
                                            lower=0, upper=1)
        # Attribute Software Qualification Test Execution
        ST_SQTE_DevH_like = pm.TruncatedNormal("ST_SQTE_DevH_like",
                                            mu=ST_SQTE_DevH_npt[attr_states["ST_SQTE_state"]][0], sigma=ST_SQTE_DevH_npt[attr_states["ST_SQTE_state"]][1],
                                            lower=0, upper=1)
        ST_SQTE_DevM_like = pm.TruncatedNormal("ST_SQTE_DevM_like",
                                            mu=ST_SQTE_DevM_npt[attr_states["ST_SQTE_state"]][0], sigma=ST_SQTE_DevM_npt[attr_states["ST_SQTE_state"]][1],
                                            lower=0, upper=1)
        ST_SQTE_DevL_like = pm.TruncatedNormal("ST_SQTE_DevL_like",
                                            mu=ST_SQTE_DevL_npt[attr_states["ST_SQTE_state"]][0], sigma=ST_SQTE_DevL_npt[attr_states["ST_SQTE_state"]][1],
                                            lower=0, upper=1)
        # Attribute Software Acceptance Procedure Generation
        ST_SAPG_DevH_like = pm.TruncatedNormal("ST_SAPG_DevH_like",
                                            mu=ST_SAPG_DevH_npt[attr_states["ST_SAPG_state"]][0], sigma=ST_SAPG_DevH_npt[attr_states["ST_SAPG_state"]][1],
                                            lower=0, upper=1)
        ST_SAPG_DevM_like = pm.TruncatedNormal("ST_SAPG_DevM_like",
                                            mu=ST_SAPG_DevM_npt[attr_states["ST_SAPG_state"]][0], sigma=ST_SAPG_DevM_npt[attr_states["ST_SAPG_state"]][1],
                                            lower=0, upper=1)
        ST_SAPG_DevL_like = pm.TruncatedNormal("ST_SAPG_DevL_like",
                                            mu=ST_SAPG_DevL_npt[attr_states["ST_SAPG_state"]][0], sigma=ST_SAPG_DevL_npt[attr_states["ST_SAPG_state"]][1],
                                            lower=0, upper=1)
        # Attribute Software Acceptance Test Execution
        ST_SATE_DevH_like = pm.TruncatedNormal("ST_SATE_DevH_like",
                                            mu=ST_SATE_DevH_npt[attr_states["ST_SATE_state"]][0], sigma=ST_SATE_DevH_npt[attr_states["ST_SATE_state"]][1],
                                            lower=0, upper=1)
        ST_SATE_DevM_like = pm.TruncatedNormal("ST_SATE_DevM_like",
                                            mu=ST_SATE_DevM_npt[attr_states["ST_SATE_state"]][0], sigma=ST_SATE_DevM_npt[attr_states["ST_SATE_state"]][1],
                                            lower=0, upper=1)
        ST_SATE_DevL_like = pm.TruncatedNormal("ST_SATE_DevL_like",
                                            mu=ST_SATE_DevL_npt[attr_states["ST_SATE_state"]][0], sigma=ST_SATE_DevL_npt[attr_states["ST_SATE_state"]][1],
                                            lower=0, upper=1)
        # Attribute Traceability Analysis - Test Phase
        ST_TA_DevH_like = pm.TruncatedNormal("ST_TA_DevH_like",
                                            mu=ST_TA_DevH_npt[attr_states["ST_TA_state"]][0], sigma=ST_TA_DevH_npt[attr_states["ST_TA_state"]][1],
                                            lower=0, upper=1)
        ST_TA_DevM_like = pm.TruncatedNormal("ST_TA_DevM_like",
                                            mu=ST_TA_DevM_npt[attr_states["ST_TA_state"]][0], sigma=ST_TA_DevM_npt[attr_states["ST_TA_state"]][1],
                                            lower=0, upper=1)
        ST_TA_DevL_like = pm.TruncatedNormal("ST_TA_DevL_like",
                                            mu=ST_TA_DevL_npt[attr_states["ST_TA_state"]][0], sigma=ST_TA_DevL_npt[attr_states["ST_TA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Hazard Analysis - Test Phase
        ST_HA_DevH_like = pm.TruncatedNormal("ST_HA_DevH_like",
                                            mu=ST_HA_DevH_npt[attr_states["ST_HA_state"]][0], sigma=ST_HA_DevH_npt[attr_states["ST_HA_state"]][1],
                                            lower=0, upper=1)
        ST_HA_DevM_like = pm.TruncatedNormal("ST_HA_DevM_like",
                                            mu=ST_HA_DevM_npt[attr_states["ST_HA_state"]][0], sigma=ST_HA_DevM_npt[attr_states["ST_HA_state"]][1],
                                            lower=0, upper=1)
        ST_HA_DevL_like = pm.TruncatedNormal("ST_HA_DevL_like",
                                            mu=ST_HA_DevL_npt[attr_states["ST_HA_state"]][0], sigma=ST_HA_DevL_npt[attr_states["ST_HA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Security Analysis - Test Phase
        ST_SA_DevH_like = pm.TruncatedNormal("ST_SA_DevH_like",
                                            mu=ST_SA_DevH_npt[attr_states["ST_SA_state"]][0], sigma=ST_SA_DevH_npt[attr_states["ST_SA_state"]][1],
                                            lower=0, upper=1)
        ST_SA_DevM_like = pm.TruncatedNormal("ST_SA_DevM_like",
                                            mu=ST_SA_DevM_npt[attr_states["ST_SA_state"]][0], sigma=ST_SA_DevM_npt[attr_states["ST_SA_state"]][1],
                                            lower=0, upper=1)
        ST_SA_DevL_like = pm.TruncatedNormal("ST_SA_DevL_like",
                                            mu=ST_SA_DevL_npt[attr_states["ST_SA_state"]][0], sigma=ST_SA_DevL_npt[attr_states["ST_SA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Risk Analysis - Test Phase
        ST_RA_DevH_like = pm.TruncatedNormal("ST_RA_DevH_like",
                                            mu=ST_RA_DevH_npt[attr_states["ST_RA_state"]][0], sigma=ST_RA_DevH_npt[attr_states["ST_RA_state"]][1],
                                            lower=0, upper=1)
        ST_RA_DevM_like = pm.TruncatedNormal("ST_RA_DevM_like",
                                            mu=ST_RA_DevM_npt[attr_states["ST_RA_state"]][0], sigma=ST_RA_DevM_npt[attr_states["ST_RA_state"]][1],
                                            lower=0, upper=1)
        ST_RA_DevL_like = pm.TruncatedNormal("ST_RA_DevL_like",
                                            mu=ST_RA_DevL_npt[attr_states["ST_RA_state"]][0], sigma=ST_RA_DevL_npt[attr_states["ST_RA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Configuration Management
        ST_CM_DevH_like = pm.TruncatedNormal("ST_CM_DevH_like",
                                            mu=ST_CM_DevH_npt[attr_states["ST_CM_state"]][0], sigma=ST_CM_DevH_npt[attr_states["ST_CM_state"]][1],
                                            lower=0, upper=1)
        ST_CM_DevM_like = pm.TruncatedNormal("ST_CM_DevM_like",
                                            mu=ST_CM_DevM_npt[attr_states["ST_CM_state"]][0], sigma=ST_CM_DevM_npt[attr_states["ST_CM_state"]][1],
                                            lower=0, upper=1)
        ST_CM_DevL_like = pm.TruncatedNormal("ST_CM_DevL_like",
                                            mu=ST_CM_DevL_npt[attr_states["ST_CM_state"]][0], sigma=ST_CM_DevL_npt[attr_states["ST_CM_state"]][1],
                                            lower=0, upper=1)
        # Attribute Review and Audits
        ST_RaA_DevH_like = pm.TruncatedNormal("ST_RaA_DevH_like",
                                            mu=ST_RaA_DevH_npt[attr_states["ST_RaA_state"]][0], sigma=ST_RaA_DevH_npt[attr_states["ST_RaA_state"]][1],
                                            lower=0, upper=1)
        ST_RaA_DevM_like = pm.TruncatedNormal("ST_RaA_DevM_like",
                                            mu=ST_RaA_DevM_npt[attr_states["ST_RaA_state"]][0], sigma=ST_RaA_DevM_npt[attr_states["ST_RaA_state"]][1],
                                            lower=0, upper=1)
        ST_RaA_DevL_like = pm.TruncatedNormal("ST_RaA_DevL_like",
                                            mu=ST_RaA_DevL_npt[attr_states["ST_RaA_state"]][0], sigma=ST_RaA_DevL_npt[attr_states["ST_RaA_state"]][1],
                                            lower=0, upper=1)
        # m1-m3: a part of marginal probability
        # m1 = P(Dev=H)P(attribute states|Dev=H)
        # m2 = P(Dev=M)P(attribute states|Dev=M)
        # m3 = P(Dev=L)P(attribute states|Dev=L)
        ST_Dev_m1 = ST_DevH_prior * ST_SITE_DevH_like * ST_SQTE_DevH_like * ST_SAPG_DevH_like * ST_SATE_DevH_like * ST_TA_DevH_like * ST_HA_DevH_like * ST_SA_DevH_like * ST_RA_DevH_like * ST_CM_DevH_like * ST_RaA_DevH_like
        ST_Dev_m2 = ST_DevM_prior * ST_SITE_DevM_like * ST_SQTE_DevM_like * ST_SAPG_DevM_like * ST_SATE_DevM_like * ST_TA_DevM_like * ST_HA_DevM_like * ST_SA_DevM_like * ST_RA_DevM_like * ST_CM_DevM_like * ST_RaA_DevM_like
        ST_Dev_m3 = ST_DevL_prior * ST_SITE_DevL_like * ST_SQTE_DevL_like * ST_SAPG_DevL_like * ST_SATE_DevL_like * ST_TA_DevL_like * ST_HA_DevL_like * ST_SA_DevL_like * ST_RA_DevL_like * ST_CM_DevL_like * ST_RaA_DevL_like

        # k = 1 / marginal probability
        ST_Dev_k = 1 / (ST_Dev_m1 + ST_Dev_m2 + ST_Dev_m3)
        # posterior probability of Dev quality in ST phase
        ST_DevH_post = pm.Deterministic("ST_DevH_post", ST_Dev_k * ST_Dev_m1)
        ST_DevM_post = pm.Deterministic("ST_DevM_post", ST_Dev_k * ST_Dev_m2)
        ST_DevL_post = pm.Deterministic("ST_DevL_post", ST_Dev_k * ST_Dev_m3)
    return model

def create_ST_VV_model(attr_states):
    model = pm.Model()
    with model:
        # V&V Attribute model - Test phase
        # prior probability of V&V quality in ST phase
        ST_VVH_prior = pm.Beta("ST_VVH_prior", alpha=0.45, beta=1.29)
        ST_VVM_prior = pm.Beta("ST_VVM_prior", alpha=1.75, beta=1.19)
        ST_VVL_prior = pm.Beta("ST_VVL_prior", alpha=0.83, beta=5.42)
        # Attribute V&V Software Integration Test Execution
        ST_VVSITE_VVH_like = pm.TruncatedNormal("ST_VVSITE_VVH_like",
                                                mu=ST_VVSITE_VVH_npt[attr_states["ST_VVSITE_state"]][0], sigma=ST_VVSITE_VVH_npt[attr_states["ST_VVSITE_state"]][1],
                                                lower=0, upper=1)
        ST_VVSITE_VVM_like = pm.TruncatedNormal("ST_VVSITE_VVM_like",
                                                mu=ST_VVSITE_VVM_npt[attr_states["ST_VVSITE_state"]][0], sigma=ST_VVSITE_VVM_npt[attr_states["ST_VVSITE_state"]][1],
                                                lower=0, upper=1)
        ST_VVSITE_VVL_like = pm.TruncatedNormal("ST_VVSITE_VVL_like",
                                                mu=ST_VVSITE_VVL_npt[attr_states["ST_VVSITE_state"]][0], sigma=ST_VVSITE_VVL_npt[attr_states["ST_VVSITE_state"]][1],
                                                lower=0, upper=1)
        # Attribute V&V Software Qualification Test Execution
        ST_VVSQTE_VVH_like = pm.TruncatedNormal("ST_VVSQTE_VVH_like",
                                                mu=ST_VVSQTE_VVH_npt[attr_states["ST_VVSQTE_state"]][0], sigma=ST_VVSQTE_VVH_npt[attr_states["ST_VVSQTE_state"]][1],
                                                lower=0, upper=1)
        ST_VVSQTE_VVM_like = pm.TruncatedNormal("ST_VVSQTE_VVM_like",
                                                mu=ST_VVSQTE_VVM_npt[attr_states["ST_VVSQTE_state"]][0], sigma=ST_VVSQTE_VVM_npt[attr_states["ST_VVSQTE_state"]][1],
                                                lower=0, upper=1)
        ST_VVSQTE_VVL_like = pm.TruncatedNormal("ST_VVSQTE_VVL_like",
                                                mu=ST_VVSQTE_VVL_npt[attr_states["ST_VVSQTE_state"]][0], sigma=ST_VVSQTE_VVL_npt[attr_states["ST_VVSQTE_state"]][1],
                                                lower=0, upper=1)
        # Attribute V&V Software Acceptance Procedure Generation
        ST_VVSAPG_VVH_like = pm.TruncatedNormal("ST_VVSAPG_VVH_like",
                                                mu=ST_VVSAPG_VVH_npt[attr_states["ST_VVSAPG_state"]][0], sigma=ST_VVSAPG_VVH_npt[attr_states["ST_VVSAPG_state"]][1],
                                                lower=0, upper=1)
        ST_VVSAPG_VVM_like = pm.TruncatedNormal("ST_VVSAPG_VVM_like",
                                                mu=ST_VVSAPG_VVM_npt[attr_states["ST_VVSAPG_state"]][0], sigma=ST_VVSAPG_VVM_npt[attr_states["ST_VVSAPG_state"]][1],
                                                lower=0, upper=1)
        ST_VVSAPG_VVL_like = pm.TruncatedNormal("ST_VVSAPG_VVL_like",
                                                mu=ST_VVSAPG_VVL_npt[attr_states["ST_VVSAPG_state"]][0], sigma=ST_VVSAPG_VVL_npt[attr_states["ST_VVSAPG_state"]][1],
                                                lower=0, upper=1)
        # Attribute V&V Software Acceptance Test Execution
        ST_VVSATE_VVH_like = pm.TruncatedNormal("ST_VVSATE_VVH_like",
                                                mu=ST_VVSATE_VVH_npt[attr_states["ST_VVSATE_state"]][0], sigma=ST_VVSATE_VVH_npt[attr_states["ST_VVSATE_state"]][1],
                                                lower=0, upper=1)
        ST_VVSATE_VVM_like = pm.TruncatedNormal("ST_VVSATE_VVM_like",
                                                mu=ST_VVSATE_VVM_npt[attr_states["ST_VVSATE_state"]][0], sigma=ST_VVSATE_VVM_npt[attr_states["ST_VVSATE_state"]][1],
                                                lower=0, upper=1)
        ST_VVSATE_VVL_like = pm.TruncatedNormal("ST_VVSATE_VVL_like",
                                                mu=ST_VVSATE_VVL_npt[attr_states["ST_VVSATE_state"]][0], sigma=ST_VVSATE_VVL_npt[attr_states["ST_VVSATE_state"]][1],
                                                lower=0, upper=1)
        # Attribute Traceability Analysis V&V - Test phase
        ST_TAVV_VVH_like = pm.TruncatedNormal("ST_TAVV_VVH_like",
                                            mu=ST_TAVV_VVH_npt[attr_states["ST_TAVV_state"]][0], sigma=ST_TAVV_VVH_npt[attr_states["ST_TAVV_state"]][1],
                                            lower=0, upper=1)
        ST_TAVV_VVM_like = pm.TruncatedNormal("ST_TAVV_VVM_like",
                                            mu=ST_TAVV_VVM_npt[attr_states["ST_TAVV_state"]][0], sigma=ST_TAVV_VVM_npt[attr_states["ST_TAVV_state"]][1],
                                            lower=0, upper=1)
        ST_TAVV_VVL_like = pm.TruncatedNormal("ST_TAVV_VVL_like",
                                            mu=ST_TAVV_VVL_npt[attr_states["ST_TAVV_state"]][0], sigma=ST_TAVV_VVL_npt[attr_states["ST_TAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Hazard Analysis V&V - Test phase
        ST_HAVV_VVH_like = pm.TruncatedNormal("ST_HAVV_VVH_like",
                                            mu=ST_HAVV_VVH_npt[attr_states["ST_HAVV_state"]][0], sigma=ST_HAVV_VVH_npt[attr_states["ST_HAVV_state"]][1],
                                            lower=0, upper=1)
        ST_HAVV_VVM_like = pm.TruncatedNormal("ST_HAVV_VVM_like",
                                            mu=ST_HAVV_VVM_npt[attr_states["ST_HAVV_state"]][0], sigma=ST_HAVV_VVM_npt[attr_states["ST_HAVV_state"]][1],
                                            lower=0, upper=1)
        ST_HAVV_VVL_like = pm.TruncatedNormal("ST_HAVV_VVL_like",
                                            mu=ST_HAVV_VVL_npt[attr_states["ST_HAVV_state"]][0], sigma=ST_HAVV_VVL_npt[attr_states["ST_HAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Security Analysis V&V - Test phase
        ST_SAVV_VVH_like = pm.TruncatedNormal("ST_SAVV_VVH_like",
                                            mu=ST_SAVV_VVH_npt[attr_states["ST_SAVV_state"]][0], sigma=ST_SAVV_VVH_npt[attr_states["ST_SAVV_state"]][1],
                                            lower=0, upper=1)
        ST_SAVV_VVM_like = pm.TruncatedNormal("ST_SAVV_VVM_like",
                                            mu=ST_SAVV_VVM_npt[attr_states["ST_SAVV_state"]][0], sigma=ST_SAVV_VVM_npt[attr_states["ST_SAVV_state"]][1],
                                            lower=0, upper=1)
        ST_SAVV_VVL_like = pm.TruncatedNormal("ST_SAVV_VVL_like",
                                            mu=ST_SAVV_VVL_npt[attr_states["ST_SAVV_state"]][0], sigma=ST_SAVV_VVL_npt[attr_states["ST_SAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Risk Analysis V&V - Test phase
        ST_RAVV_VVH_like = pm.TruncatedNormal("ST_RAVV_VVH_like",
                                            mu=ST_RAVV_VVH_npt[attr_states["ST_RAVV_state"]][0], sigma=ST_RAVV_VVH_npt[attr_states["ST_RAVV_state"]][1],
                                            lower=0, upper=1)
        ST_RAVV_VVM_like = pm.TruncatedNormal("ST_RAVV_VVM_like",
                                            mu=ST_RAVV_VVM_npt[attr_states["ST_RAVV_state"]][0], sigma=ST_RAVV_VVM_npt[attr_states["ST_RAVV_state"]][1],
                                            lower=0, upper=1)
        ST_RAVV_VVL_like = pm.TruncatedNormal("ST_RAVV_VVL_like",
                                            mu=ST_RAVV_VVL_npt[attr_states["ST_RAVV_state"]][0], sigma=ST_RAVV_VVL_npt[attr_states["ST_RAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Configuration Management V&V - Test phase
        ST_CMVV_VVH_like = pm.TruncatedNormal("ST_CMVV_VVH_like",
                                            mu=ST_CMVV_VVH_npt[attr_states["ST_CMVV_state"]][0], sigma=ST_CMVV_VVH_npt[attr_states["ST_CMVV_state"]][1],
                                            lower=0, upper=1)
        ST_CMVV_VVM_like = pm.TruncatedNormal("ST_CMVV_VVM_like",
                                            mu=ST_CMVV_VVM_npt[attr_states["ST_CMVV_state"]][0], sigma=ST_CMVV_VVM_npt[attr_states["ST_CMVV_state"]][1],
                                            lower=0, upper=1)
        ST_CMVV_VVL_like = pm.TruncatedNormal("ST_CMVV_VVL_like",
                                            mu=ST_CMVV_VVL_npt[attr_states["ST_CMVV_state"]][0], sigma=ST_CMVV_VVL_npt[attr_states["ST_CMVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Review and Audit V&V - Test phase
        ST_RaAVV_VVH_like = pm.TruncatedNormal("ST_RaAVV_VVH_like",
                                            mu=ST_RaAVV_VVH_npt[attr_states["ST_RaAVV_state"]][0], sigma=ST_RaAVV_VVH_npt[attr_states["ST_RaAVV_state"]][1],
                                            lower=0, upper=1)
        ST_RaAVV_VVM_like = pm.TruncatedNormal("ST_RaAVV_VVM_like",
                                            mu=ST_RaAVV_VVM_npt[attr_states["ST_RaAVV_state"]][0], sigma=ST_RaAVV_VVM_npt[attr_states["ST_RaAVV_state"]][1],
                                            lower=0, upper=1)
        ST_RaAVV_VVL_like = pm.TruncatedNormal("ST_RaAVV_VVL_like",
                                            mu=ST_RaAVV_VVL_npt[attr_states["ST_RaAVV_state"]][0], sigma=ST_RaAVV_VVL_npt[attr_states["ST_RaAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute V&V Test phase Activity Summary Report Generation
        ST_VVASRG_VVH_like = pm.TruncatedNormal("ST_VVASRG_VVH_like",
                                                mu=ST_VVASRG_VVH_npt[attr_states["ST_VVASRG_state"]][0], sigma=ST_VVASRG_VVH_npt[attr_states["ST_VVASRG_state"]][1],
                                                lower=0, upper=1)
        ST_VVASRG_VVM_like = pm.TruncatedNormal("ST_VVASRG_VVM_like",
                                                mu=ST_VVASRG_VVM_npt[attr_states["ST_VVASRG_state"]][0], sigma=ST_VVASRG_VVM_npt[attr_states["ST_VVASRG_state"]][1],
                                                lower=0, upper=1)
        ST_VVASRG_VVL_like = pm.TruncatedNormal("ST_VVASRG_VVL_like",
                                                mu=ST_VVASRG_VVL_npt[attr_states["ST_VVASRG_state"]][0], sigma=ST_VVASRG_VVL_npt[attr_states["ST_VVASRG_state"]][1],
                                                lower=0, upper=1)
        # m1-m3: a part of marginal probability
        # m1 = P(VV=H)P(attribute states|VV=H)
        # m2 = P(VV=M)P(attribute states|VV=M)
        # m3 = P(VV=L)P(attribute states|VV=L)
        ST_VV_m1 = ST_VVH_prior * ST_VVSITE_VVH_like * ST_VVSQTE_VVH_like * ST_VVSAPG_VVH_like * ST_VVSATE_VVH_like * ST_TAVV_VVH_like * ST_HAVV_VVH_like * ST_SAVV_VVH_like * ST_RAVV_VVH_like * ST_CMVV_VVH_like * ST_RaAVV_VVH_like * ST_VVASRG_VVH_like
        ST_VV_m2 = ST_VVM_prior * ST_VVSITE_VVM_like * ST_VVSQTE_VVM_like * ST_VVSAPG_VVM_like * ST_VVSATE_VVM_like * ST_TAVV_VVM_like * ST_HAVV_VVM_like * ST_SAVV_VVM_like * ST_RAVV_VVM_like * ST_CMVV_VVM_like * ST_RaAVV_VVM_like * ST_VVASRG_VVM_like
        ST_VV_m3 = ST_VVL_prior * ST_VVSITE_VVL_like * ST_VVSQTE_VVL_like * ST_VVSAPG_VVL_like * ST_VVSATE_VVL_like * ST_TAVV_VVL_like * ST_HAVV_VVL_like * ST_SAVV_VVL_like * ST_RAVV_VVL_like * ST_CMVV_VVL_like * ST_RaAVV_VVL_like * ST_VVASRG_VVL_like

        # k = 1 / marginal probability
        ST_VV_k = 1 / (ST_VV_m1 + ST_VV_m2 + ST_VV_m3)

        # posterior probability of V&V quality in ST phase
        ST_VVH_post = pm.Deterministic("ST_VVH_post", ST_VV_k * ST_VV_m1)
        ST_VVM_post = pm.Deterministic("ST_VVM_post", ST_VV_k * ST_VV_m2)
        ST_VVL_post = pm.Deterministic("ST_VVL_post", ST_VV_k * ST_VV_m3)
    return model

def create_IC_Dev_model(attr_states):
    model = pm.Model()

    with model:
        # Dev Attribute model - Installation & Checkout phase
        # prior probability of Dev quality in IC phase
        IC_DevH_prior = pm.Beta("IC_DevH_prior", alpha=0.99, beta=1.66)
        IC_DevM_prior = pm.Beta("IC_DevM_prior", alpha=1.28, beta=1.05)
        IC_DevL_prior = pm.Beta("IC_DevL_prior", alpha=2.83, beta=32.73)
        # Attribute Installation Procedure Generation
        IC_IPG_DevH_like = pm.TruncatedNormal("IC_IPG_DevH_like",
                                            mu=IC_IPG_DevH_npt[attr_states["IC_IPG_state"]][0], sigma=IC_IPG_DevH_npt[attr_states["IC_IPG_state"]][1],
                                            lower=0, upper=1)
        IC_IPG_DevM_like = pm.TruncatedNormal("IC_IPG_DevM_like",
                                            mu=IC_IPG_DevM_npt[attr_states["IC_IPG_state"]][0], sigma=IC_IPG_DevM_npt[attr_states["IC_IPG_state"]][1],
                                            lower=0, upper=1)
        IC_IPG_DevL_like = pm.TruncatedNormal("IC_IPG_DevL_like",
                                            mu=IC_IPG_DevL_npt[attr_states["IC_IPG_state"]][0], sigma=IC_IPG_DevL_npt[attr_states["IC_IPG_state"]][1],
                                            lower=0, upper=1)
        # Attribute Installation and Checkout
        IC_IaC_DevH_like = pm.TruncatedNormal("IC_IaC_DevH_like",
                                            mu=IC_IaC_DevH_npt[attr_states["IC_IaC_state"]][0], sigma=IC_IaC_DevH_npt[attr_states["IC_IaC_state"]][1],
                                            lower=0, upper=1)
        IC_IaC_DevM_like = pm.TruncatedNormal("IC_IaC_DevM_like",
                                            mu=IC_IaC_DevM_npt[attr_states["IC_IaC_state"]][0], sigma=IC_IaC_DevM_npt[attr_states["IC_IaC_state"]][1],
                                            lower=0, upper=1)
        IC_IaC_DevL_like = pm.TruncatedNormal("IC_IaC_DevL_like",
                                            mu=IC_IaC_DevL_npt[attr_states["IC_IaC_state"]][0], sigma=IC_IaC_DevL_npt[attr_states["IC_IaC_state"]][1],
                                            lower=0, upper=1)
        # Attribute Hazard Analysis - IC phase
        IC_HA_DevH_like = pm.TruncatedNormal("IC_HA_DevH_like",
                                            mu=IC_HA_DevH_npt[attr_states["IC_HA_state"]][0], sigma=IC_HA_DevH_npt[attr_states["IC_HA_state"]][1],
                                            lower=0, upper=1)
        IC_HA_DevM_like = pm.TruncatedNormal("IC_HA_DevM_like",
                                            mu=IC_HA_DevM_npt[attr_states["IC_HA_state"]][0], sigma=IC_HA_DevM_npt[attr_states["IC_HA_state"]][1],
                                            lower=0, upper=1)
        IC_HA_DevL_like = pm.TruncatedNormal("IC_HA_DevL_like",
                                            mu=IC_HA_DevL_npt[attr_states["IC_HA_state"]][0], sigma=IC_HA_DevL_npt[attr_states["IC_HA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Security Analysis - IC phase
        IC_SA_DevH_like = pm.TruncatedNormal("IC_SA_DevH_like",
                                            mu=IC_SA_DevH_npt[attr_states["IC_SA_state"]][0], sigma=IC_SA_DevH_npt[attr_states["IC_SA_state"]][1],
                                            lower=0, upper=1)
        IC_SA_DevM_like = pm.TruncatedNormal("IC_SA_DevM_like",
                                            mu=IC_SA_DevM_npt[attr_states["IC_SA_state"]][0], sigma=IC_SA_DevM_npt[attr_states["IC_SA_state"]][1],
                                            lower=0, upper=1)
        IC_SA_DevL_like = pm.TruncatedNormal("IC_SA_DevL_like",
                                            mu=IC_SA_DevL_npt[attr_states["IC_SA_state"]][0], sigma=IC_SA_DevL_npt[attr_states["IC_SA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Security Analysis - IC phase
        IC_RA_DevH_like = pm.TruncatedNormal("IC_RA_DevH_like",
                                            mu=IC_RA_DevH_npt[attr_states["IC_RA_state"]][0], sigma=IC_RA_DevH_npt[attr_states["IC_RA_state"]][1],
                                            lower=0, upper=1)
        IC_RA_DevM_like = pm.TruncatedNormal("IC_RA_DevM_like",
                                            mu=IC_RA_DevM_npt[attr_states["IC_RA_state"]][0], sigma=IC_RA_DevM_npt[attr_states["IC_RA_state"]][1],
                                            lower=0, upper=1)
        IC_RA_DevL_like = pm.TruncatedNormal("IC_RA_DevL_like",
                                            mu=IC_RA_DevL_npt[attr_states["IC_RA_state"]][0], sigma=IC_RA_DevL_npt[attr_states["IC_RA_state"]][1],
                                            lower=0, upper=1)
        # m1-m3: a part of marginal probability
        # m1 = P(Dev=H)P(attribute states|Dev=H)
        # m2 = P(Dev=M)P(attribute states|Dev=M)
        # m3 = P(Dev=L)P(attribute states|Dev=L)
        IC_Dev_m1 = IC_DevH_prior * IC_IPG_DevH_like * IC_IaC_DevH_like * IC_HA_DevH_like * IC_SA_DevH_like * IC_RA_DevH_like
        IC_Dev_m2 = IC_DevM_prior * IC_IPG_DevM_like * IC_IaC_DevM_like * IC_HA_DevM_like * IC_SA_DevM_like * IC_RA_DevM_like
        IC_Dev_m3 = IC_DevL_prior * IC_IPG_DevL_like * IC_IaC_DevL_like * IC_HA_DevL_like * IC_SA_DevL_like * IC_RA_DevL_like

        # k = 1 / marginal probability
        IC_Dev_k = 1 / (IC_Dev_m1 + IC_Dev_m2 + IC_Dev_m3)

        # posterior probability of Dev quality in IC phase
        IC_DevH_post = pm.Deterministic("IC_DevH_post", IC_Dev_k * IC_Dev_m1)
        IC_DevM_post = pm.Deterministic("IC_DevM_post", IC_Dev_k * IC_Dev_m2)
        IC_DevL_post = pm.Deterministic("IC_DevL_post", IC_Dev_k * IC_Dev_m3)
    return model

def create_IC_VV_model(attr_states):
    model = pm.Model()

    with model:
        # V&V Attribute model - Installation & Checkout phase
        # prior probability of V&V quality in IC phase
        IC_VVH_prior = pm.Beta("IC_VVH_prior", alpha=1.05, beta=2.26)
        IC_VVM_prior = pm.Beta("IC_VVM_prior", alpha=1.45, beta=1.10)
        IC_VVL_prior = pm.Beta("IC_VVL_prior", alpha=1.28, beta=8.56)
        # Attribute Installation Configuration Audit V&V
        IC_ICAVV_VVH_like = pm.TruncatedNormal("IC_ICAVV_VVH_like",
                                            mu=IC_ICAVV_VVH_npt[attr_states["IC_ICAVV_state"]][0], sigma=IC_ICAVV_VVH_npt[attr_states["IC_ICAVV_state"]][1],
                                            lower=0, upper=1)
        IC_ICAVV_VVM_like = pm.TruncatedNormal("IC_ICAVV_VVM_like",
                                            mu=IC_ICAVV_VVM_npt[attr_states["IC_ICAVV_state"]][0], sigma=IC_ICAVV_VVM_npt[attr_states["IC_ICAVV_state"]][1],
                                            lower=0, upper=1)
        IC_ICAVV_VVL_like = pm.TruncatedNormal("IC_ICAVV_VVL_like",
                                            mu=IC_ICAVV_VVL_npt[attr_states["IC_ICAVV_state"]][0], sigma=IC_ICAVV_VVL_npt[attr_states["IC_ICAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Installation Checkout V&V
        IC_ICVV_VVH_like = pm.TruncatedNormal("IC_ICVV_VVH_like",
                                            mu=IC_ICVV_VVH_npt[attr_states["IC_ICVV_state"]][0], sigma=IC_ICVV_VVH_npt[attr_states["IC_ICVV_state"]][1],
                                            lower=0, upper=1)
        IC_ICVV_VVM_like = pm.TruncatedNormal("IC_ICVV_VVM_like",
                                            mu=IC_ICVV_VVM_npt[attr_states["IC_ICVV_state"]][0], sigma=IC_ICVV_VVM_npt[attr_states["IC_ICVV_state"]][1],
                                            lower=0, upper=1)
        IC_ICVV_VVL_like = pm.TruncatedNormal("IC_ICVV_VVL_like",
                                            mu=IC_ICVV_VVL_npt[attr_states["IC_ICVV_state"]][0], sigma=IC_ICVV_VVL_npt[attr_states["IC_ICVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Hazard Analysis V&V
        IC_HAVV_VVH_like = pm.TruncatedNormal("IC_HAVV_VVH_like",
                                            mu=IC_HAVV_VVH_npt[attr_states["IC_HAVV_state"]][0], sigma=IC_HAVV_VVH_npt[attr_states["IC_HAVV_state"]][1],
                                            lower=0, upper=1)
        IC_HAVV_VVM_like = pm.TruncatedNormal("IC_HAVV_VVM_like",
                                            mu=IC_HAVV_VVM_npt[attr_states["IC_HAVV_state"]][0], sigma=IC_HAVV_VVM_npt[attr_states["IC_HAVV_state"]][1],
                                            lower=0, upper=1)
        IC_HAVV_VVL_like = pm.TruncatedNormal("IC_HAVV_VVL_like",
                                            mu=IC_HAVV_VVL_npt[attr_states["IC_HAVV_state"]][0], sigma=IC_HAVV_VVL_npt[attr_states["IC_HAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Security Analysis V&V
        IC_SAVV_VVH_like = pm.TruncatedNormal("IC_SAVV_VVH_like",
                                            mu=IC_SAVV_VVH_npt[attr_states["IC_SAVV_state"]][0], sigma=IC_SAVV_VVH_npt[attr_states["IC_SAVV_state"]][1],
                                            lower=0, upper=1)
        IC_SAVV_VVM_like = pm.TruncatedNormal("IC_SAVV_VVM_like",
                                            mu=IC_SAVV_VVM_npt[attr_states["IC_SAVV_state"]][0], sigma=IC_SAVV_VVM_npt[attr_states["IC_SAVV_state"]][1],
                                            lower=0, upper=1)
        IC_SAVV_VVL_like = pm.TruncatedNormal("IC_SAVV_VVL_like",
                                            mu=IC_SAVV_VVL_npt[attr_states["IC_SAVV_state"]][0], sigma=IC_SAVV_VVL_npt[attr_states["IC_SAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Risk Analysis V&V
        IC_RAVV_VVH_like = pm.TruncatedNormal("IC_RAVV_VVH_like",
                                            mu=IC_RAVV_VVH_npt[attr_states["IC_RAVV_state"]][0], sigma=IC_RAVV_VVH_npt[attr_states["IC_RAVV_state"]][1],
                                            lower=0, upper=1)
        IC_RAVV_VVM_like = pm.TruncatedNormal("IC_RAVV_VVM_like",
                                            mu=IC_RAVV_VVM_npt[attr_states["IC_RAVV_state"]][0], sigma=IC_RAVV_VVM_npt[attr_states["IC_RAVV_state"]][1],
                                            lower=0, upper=1)
        IC_RAVV_VVL_like = pm.TruncatedNormal("IC_RAVV_VVL_like",
                                            mu=IC_RAVV_VVL_npt[attr_states["IC_RAVV_state"]][0], sigma=IC_RAVV_VVL_npt[attr_states["IC_RAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute V&V Installation and Checkout Phase Activity Summary Report Generation
        IC_VVASRG_VVH_like = pm.TruncatedNormal("IC_VVASRG_VVH_like",
                                                mu=IC_VVASRG_VVH_npt[attr_states["IC_VVASRG_state"]][0], sigma=IC_VVASRG_VVH_npt[attr_states["IC_VVASRG_state"]][1],
                                                lower=0, upper=1)
        IC_VVASRG_VVM_like = pm.TruncatedNormal("IC_VVASRG_VVM_like",
                                                mu=IC_VVASRG_VVM_npt[attr_states["IC_VVASRG_state"]][0], sigma=IC_VVASRG_VVM_npt[attr_states["IC_VVASRG_state"]][1],
                                                lower=0, upper=1)
        IC_VVASRG_VVL_like = pm.TruncatedNormal("IC_VVASRG_VVL_like",
                                                mu=IC_VVASRG_VVL_npt[attr_states["IC_VVASRG_state"]][0], sigma=IC_VVASRG_VVL_npt[attr_states["IC_VVASRG_state"]][1],
                                                lower=0, upper=1)
        # Attribute V&V Final Report Generation
        IC_VVFRG_VVH_like = pm.TruncatedNormal("IC_VVFRG_VVH_like",
                                            mu=IC_VVFRG_VVH_npt[attr_states["IC_VVFRG_state"]][0], sigma=IC_VVFRG_VVH_npt[attr_states["IC_VVFRG_state"]][1],
                                            lower=0, upper=1)
        IC_VVFRG_VVM_like = pm.TruncatedNormal("IC_VVFRG_VVM_like",
                                            mu=IC_VVFRG_VVM_npt[attr_states["IC_VVFRG_state"]][0], sigma=IC_VVFRG_VVM_npt[attr_states["IC_VVFRG_state"]][1],
                                            lower=0, upper=1)
        IC_VVFRG_VVL_like = pm.TruncatedNormal("IC_VVFRG_VVL_like",
                                            mu=IC_VVFRG_VVL_npt[attr_states["IC_VVFRG_state"]][0], sigma=IC_VVFRG_VVL_npt[attr_states["IC_VVFRG_state"]][1],
                                            lower=0, upper=1)
        # m1-m3: a part of marginal probability
        # m1 = P(VV=H)P(attribute states|VV=H)
        # m2 = P(VV=M)P(attribute states|VV=M)
        # m3 = P(VV=L)P(attribute states|VV=L)
        IC_VV_m1 = IC_VVH_prior * IC_ICAVV_VVH_like * IC_ICVV_VVH_like * IC_HAVV_VVH_like * IC_SAVV_VVH_like * IC_RAVV_VVH_like * IC_VVASRG_VVH_like * IC_VVFRG_VVH_like
        IC_VV_m2 = IC_VVM_prior * IC_ICAVV_VVM_like * IC_ICVV_VVM_like * IC_HAVV_VVM_like * IC_SAVV_VVM_like * IC_RAVV_VVM_like * IC_VVASRG_VVM_like * IC_VVFRG_VVM_like
        IC_VV_m3 = IC_VVL_prior * IC_ICAVV_VVL_like * IC_ICVV_VVL_like * IC_HAVV_VVL_like * IC_SAVV_VVL_like * IC_RAVV_VVL_like * IC_VVASRG_VVL_like * IC_VVFRG_VVL_like

        # k = 1 / marginal probability
        IC_VV_k = 1 / (IC_VV_m1 + IC_VV_m2 + IC_VV_m3)

        # posterior probability of V&V quality in IC phase
        IC_VVH_post = pm.Deterministic("IC_VVH_post", IC_VV_k * IC_VV_m1)
        IC_VVM_post = pm.Deterministic("IC_VVM_post", IC_VV_k * IC_VV_m2)
        IC_VVL_post = pm.Deterministic("IC_VVL_post", IC_VV_k * IC_VV_m3)
    return model

def create_composite_model(SR_Dev_trace, SR_VV_trace, SD_Dev_trace, SD_VV_trace,
                           IM_Dev_trace, IM_VV_trace, ST_Dev_trace, ST_VV_trace,
                           IC_Dev_trace, IC_VV_trace,
                           generic_trace, function_point, complexity, interpolation_bins):
    model = pm.Model()
    with model:
        # Submodel - Requirement phase
        temp_h = SR_Dev_trace.posterior["SR_DevH_post"].mean().item()
        temp_m = SR_Dev_trace.posterior["SR_DevM_post"].mean().item()
        temp_l = SR_Dev_trace.posterior["SR_DevL_post"].mean().item()
        SR_DevH_post = temp_h / (temp_h + temp_m + temp_l)
        SR_DevM_post = temp_m / (temp_h + temp_m + temp_l)
        SR_DevL_post = temp_l / (temp_h + temp_m + temp_l)

        temp_h = SR_VV_trace.posterior["SR_VVH_post"].mean().item()
        temp_m = SR_VV_trace.posterior["SR_VVM_post"].mean().item()
        temp_l = SR_VV_trace.posterior["SR_VVL_post"].mean().item()
        SR_VVH_post = temp_h / (temp_h + temp_m + temp_l)
        SR_VVM_post = temp_m / (temp_h + temp_m + temp_l)
        SR_VVL_post = temp_l / (temp_h + temp_m + temp_l)

        # Defect Density likelihood: P(Defect Density|state of Dev quality)
        SR_DevH_DD_like = pm.Gamma("SR_DevH_DD_like", alpha=1.1043, beta=3.5507)
        SR_DevM_DD_like = pm.Gamma("SR_DevM_DD_like", alpha=1.3130, beta=3.3811)
        SR_DevL_DD_like = pm.Gamma("SR_DevL_DD_like", alpha=1.3596, beta=3.1705)

        # Defect density: the integral of P(Dev)*P(Defect Density|Dev) dDev
        SR_Defect_Density = (SR_DevH_post * SR_DevH_DD_like + SR_DevM_post * SR_DevM_DD_like + SR_DevL_post * SR_DevL_DD_like)

        SR_Defect_introduced_in_current = pm.Deterministic("SR_Defect_introduced_in_current", function_point * SR_Defect_Density)

        # Defect Detection Probability (current) likelihood: P(DDP_current|state of VV quality)
        SR_VVH_DDP_current_like = pm.Beta("SR_VVH_DDP_current_like", alpha=SR_VVH_DDP_current_npt[complexity][0], beta=SR_VVH_DDP_current_npt[complexity][1])
        SR_VVM_DDP_current_like = pm.Beta("SR_VVM_DDP_current_like", alpha=SR_VVM_DDP_current_npt[complexity][0], beta=SR_VVM_DDP_current_npt[complexity][1])
        SR_VVL_DDP_current_like = pm.Beta("SR_VVL_DDP_current_like", alpha=SR_VVL_DDP_current_npt[complexity][0], beta=SR_VVL_DDP_current_npt[complexity][1])

        # Defect Detection Probability (current): the integral of P(DDP_current|VV) dVV
        SR_Defect_Detection_Probability_current = (SR_VVH_post * SR_VVH_DDP_current_like + SR_VVM_post * SR_VVM_DDP_current_like + SR_VVL_post * SR_VVL_DDP_current_like)

        SR_Detected_Defect_current = SR_Defect_introduced_in_current * SR_Defect_Detection_Probability_current

        SR_Remaining_Defect_current = SR_Defect_introduced_in_current - SR_Detected_Defect_current

        # since there's no phase before the SR phase
        SR_Total_Remained_Defect = pm.Deterministic("SR_Total_Remained_Defect", SR_Remaining_Defect_current)

        # Submodel - Design phase
        temp_h = SD_Dev_trace.posterior["SD_DevH_post"].mean().item()
        temp_m = SD_Dev_trace.posterior["SD_DevM_post"].mean().item()
        temp_l = SD_Dev_trace.posterior["SD_DevL_post"].mean().item()
        SD_DevH_post = temp_h / (temp_h + temp_m + temp_l)
        SD_DevM_post = temp_m / (temp_h + temp_m + temp_l)
        SD_DevL_post = temp_l / (temp_h + temp_m + temp_l)

        temp_h = SD_VV_trace.posterior["SD_VVH_post"].mean().item()
        temp_m = SD_VV_trace.posterior["SD_VVM_post"].mean().item()
        temp_l = SD_VV_trace.posterior["SD_VVL_post"].mean().item()
        SD_VVH_post = temp_h / (temp_h + temp_m + temp_l)
        SD_VVM_post = temp_m / (temp_h + temp_m + temp_l)
        SD_VVL_post = temp_l / (temp_h + temp_m + temp_l)

        # Defect Density likelihood: P(Defect Density|state of Dev quality)
        SD_DevH_DD_like = pm.Gamma("SD_DevH_DD_like", alpha=2.2558, beta=3.3680)
        SD_DevM_DD_like = pm.Gamma("SD_DevM_DD_like", alpha=2.7565, beta=3.2526)
        SD_DevL_DD_like = pm.Gamma("SD_DevL_DD_like", alpha=3.0353, beta=3.1522)

        # Defect density: the integral of P(Dev)*P(Defect Density|Dev) dDev
        SD_Defect_Density = (SD_DevH_post * SD_DevH_DD_like + SD_DevM_post * SD_DevM_DD_like + SD_DevL_post * SD_DevL_DD_like)

        SD_Defect_introduced_in_current = pm.Deterministic("SD_Defect_introduced_in_current", function_point * SD_Defect_Density)

        # Defect Detection Probability (current) likelihood: P(DDP_current|state of VV quality)
        SD_VVH_DDP_current_like = pm.Beta("SD_VVH_DDP_current_like", alpha=SD_VVH_DDP_current_npt[complexity][0], beta=SD_VVH_DDP_current_npt[complexity][1])
        SD_VVM_DDP_current_like = pm.Beta("SD_VVM_DDP_current_like", alpha=SD_VVM_DDP_current_npt[complexity][0], beta=SD_VVM_DDP_current_npt[complexity][1])
        SD_VVL_DDP_current_like = pm.Beta("SD_VVL_DDP_current_like", alpha=SD_VVL_DDP_current_npt[complexity][0], beta=SD_VVL_DDP_current_npt[complexity][1])

        # Defect Detection Probability (current): the integral of P(DDP_current|VV) dVV
        SD_Defect_Detection_Probability_current = SD_VVH_post * SD_VVH_DDP_current_like + SD_VVM_post * SD_VVM_DDP_current_like + SD_VVL_post * SD_VVL_DDP_current_like

        SD_Detected_Defect_current = SD_Defect_introduced_in_current * SD_Defect_Detection_Probability_current

        SD_Remaining_Defect_current = SD_Defect_introduced_in_current - SD_Detected_Defect_current

        # Defect Detection Probability (previous) likelihood: P(DDP_previous|state of VV quality)
        SD_VVH_DDP_previous_like = pm.Beta("SD_VVH_DDP_previous_like", alpha=SD_VVH_DDP_previous_npt[complexity][0], beta=SD_VVH_DDP_previous_npt[complexity][1])
        SD_VVM_DDP_previous_like = pm.Beta("SD_VVM_DDP_previous_like", alpha=SD_VVM_DDP_previous_npt[complexity][0], beta=SD_VVM_DDP_previous_npt[complexity][1])
        SD_VVL_DDP_previous_like = pm.Beta("SD_VVL_DDP_previous_like", alpha=SD_VVL_DDP_previous_npt[complexity][0], beta=SD_VVL_DDP_previous_npt[complexity][1])

        # Defect Detection Probability (previous): the integral of P(DDP_previous|VV) dVV
        SD_Defect_Detection_Probability_previous = SD_VVH_post * SD_VVH_DDP_previous_like + SD_VVM_post * SD_VVM_DDP_previous_like + SD_VVL_post * SD_VVL_DDP_previous_like

        SD_Detected_Defect_previous = SR_Total_Remained_Defect * SD_Defect_Detection_Probability_previous

        SD_Remaining_Defect_previous = SR_Total_Remained_Defect - SD_Detected_Defect_previous

        SD_Total_Remained_Defect = pm.Deterministic("SD_Total_Remained_Defect", SD_Remaining_Defect_current + SD_Remaining_Defect_previous)

        # Submodel - Implementation phase
        temp_h = IM_Dev_trace.posterior["IM_DevH_post"].mean().item()
        temp_m = IM_Dev_trace.posterior["IM_DevM_post"].mean().item()
        temp_l = IM_Dev_trace.posterior["IM_DevL_post"].mean().item()
        IM_DevH_post = temp_h / (temp_h + temp_m + temp_l)
        IM_DevM_post = temp_m / (temp_h + temp_m + temp_l)
        IM_DevL_post = temp_l / (temp_h + temp_m + temp_l)

        temp_h = IM_VV_trace.posterior["IM_VVH_post"].mean().item()
        temp_m = IM_VV_trace.posterior["IM_VVM_post"].mean().item()
        temp_l = IM_VV_trace.posterior["IM_VVL_post"].mean().item()
        IM_VVH_post = temp_h / (temp_h + temp_m + temp_l)
        IM_VVM_post = temp_m / (temp_h + temp_m + temp_l)
        IM_VVL_post = temp_l / (temp_h + temp_m + temp_l)

        # Defect Density likelihood: P(Defect Density|state of Dev quality)
        IM_DevH_DD_like = pm.Gamma("IM_DevH_DD_like", alpha=2.5989, beta=3.3317)
        IM_DevM_DD_like = pm.Gamma("IM_DevM_DD_like", alpha=3.1588, beta=3.1963)
        IM_DevL_DD_like = pm.Gamma("IM_DevL_DD_like", alpha=3.3807, beta=3.1969)

        # Defect density: the integral of P(Dev)*P(Defect Density|Dev) dDev
        IM_Defect_Density = (IM_DevH_post * IM_DevH_DD_like + IM_DevM_post * IM_DevM_DD_like + IM_DevL_post * IM_DevL_DD_like)

        IM_Defect_introduced_in_current = pm.Deterministic("IM_Defect_introduced_in_current", function_point * IM_Defect_Density)

        # Defect Detection Probability (current) likelihood: P(DDP_current|state of VV quality)
        IM_VVH_DDP_current_like = pm.Beta("IM_VVH_DDP_current_like", alpha=IM_VVH_DDP_current_npt[complexity][0], beta=IM_VVH_DDP_current_npt[complexity][1])
        IM_VVM_DDP_current_like = pm.Beta("IM_VVM_DDP_current_like", alpha=IM_VVM_DDP_current_npt[complexity][0], beta=IM_VVM_DDP_current_npt[complexity][1])
        IM_VVL_DDP_current_like = pm.Beta("IM_VVL_DDP_current_like", alpha=IM_VVL_DDP_current_npt[complexity][0], beta=IM_VVL_DDP_current_npt[complexity][1])

        # Defect Detection Probability (current): the integral of P(DDP_current|VV) dVV
        IM_Defect_Detection_Probability_current = IM_VVH_post * IM_VVH_DDP_current_like + IM_VVM_post * IM_VVM_DDP_current_like + IM_VVL_post * IM_VVL_DDP_current_like

        IM_Detected_Defect_current = IM_Defect_introduced_in_current * IM_Defect_Detection_Probability_current

        IM_Remaining_Defect_current = IM_Defect_introduced_in_current - IM_Detected_Defect_current

        # Defect Detection Probability (previous) likelihood: P(DDP_previous|state of VV quality)
        IM_VVH_DDP_previous_like = pm.Beta("IM_VVH_DDP_previous_like", alpha=IM_VVH_DDP_previous_npt[complexity][0], beta=IM_VVH_DDP_previous_npt[complexity][1])
        IM_VVM_DDP_previous_like = pm.Beta("IM_VVM_DDP_previous_like", alpha=IM_VVM_DDP_previous_npt[complexity][0], beta=IM_VVM_DDP_previous_npt[complexity][1])
        IM_VVL_DDP_previous_like = pm.Beta("IM_VVL_DDP_previous_like", alpha=IM_VVL_DDP_previous_npt[complexity][0], beta=IM_VVL_DDP_previous_npt[complexity][1])

        # Defect Detection Probability (previous): the integral of P(DDP_previous|VV) dVV
        IM_Defect_Detection_Probability_previous = IM_VVH_post * IM_VVH_DDP_previous_like + IM_VVM_post * IM_VVM_DDP_previous_like + IM_VVL_post * IM_VVL_DDP_previous_like

        IM_Detected_Defect_previous = SD_Total_Remained_Defect * IM_Defect_Detection_Probability_previous

        IM_Remaining_Defect_previous = SD_Total_Remained_Defect - IM_Detected_Defect_previous

        IM_Total_Remained_Defect = pm.Deterministic("IM_Total_Remained_Defect", IM_Remaining_Defect_current + IM_Remaining_Defect_previous)

        # Submodel - Test phase
        temp_h = ST_Dev_trace.posterior["ST_DevH_post"].mean().item()
        temp_m = ST_Dev_trace.posterior["ST_DevM_post"].mean().item()
        temp_l = ST_Dev_trace.posterior["ST_DevL_post"].mean().item()
        ST_DevH_post = temp_h / (temp_h + temp_m + temp_l)
        ST_DevM_post = temp_m / (temp_h + temp_m + temp_l)
        ST_DevL_post = temp_l / (temp_h + temp_m + temp_l)

        temp_h = ST_VV_trace.posterior["ST_VVH_post"].mean().item()
        temp_m = ST_VV_trace.posterior["ST_VVM_post"].mean().item()
        temp_l = ST_VV_trace.posterior["ST_VVL_post"].mean().item()
        ST_VVH_post = temp_h / (temp_h + temp_m + temp_l)
        ST_VVM_post = temp_m / (temp_h + temp_m + temp_l)
        ST_VVL_post = temp_l / (temp_h + temp_m + temp_l)

        # Defect Density likelihood: P(Defect Density|state of Dev quality)
        ST_DevH_DD_like = pm.Gamma("ST_DevH_DD_like", alpha=1.2439, beta=4.3055)
        ST_DevM_DD_like = pm.Gamma("ST_DevM_DD_like", alpha=1.5775, beta=3.9236)
        ST_DevL_DD_like = pm.Gamma("ST_DevL_DD_like", alpha=1.5630, beta=3.1705)

        # Defect density: the integral of P(Dev)*P(Defect Density|Dev) dDev
        ST_Defect_Density = (ST_DevH_post * ST_DevH_DD_like + ST_DevM_post * ST_DevM_DD_like + ST_DevL_post * ST_DevL_DD_like)

        ST_Defect_introduced_in_current = pm.Deterministic("ST_Defect_introduced_in_current", function_point * ST_Defect_Density)

        # Defect Detection Probability (current) likelihood: P(DDP_current|state of Dev quality, state of VV quality)
        ST_DevH_VVH_DDP_current_like = pm.Beta("ST_DevH_VVH_DDP_current_like", alpha=ST_DevH_VVH_DDP_current_npt[complexity][0], beta=ST_DevH_VVH_DDP_current_npt[complexity][1])
        ST_DevH_VVM_DDP_current_like = pm.Beta("ST_DevH_VVM_DDP_current_like", alpha=ST_DevH_VVM_DDP_current_npt[complexity][0], beta=ST_DevH_VVM_DDP_current_npt[complexity][1])
        ST_DevH_VVL_DDP_current_like = pm.Beta("ST_DevH_VVL_DDP_current_like", alpha=ST_DevH_VVL_DDP_current_npt[complexity][0], beta=ST_DevH_VVL_DDP_current_npt[complexity][1])
        ST_DevM_VVH_DDP_current_like = pm.Beta("ST_DevM_VVH_DDP_current_like", alpha=ST_DevM_VVH_DDP_current_npt[complexity][0], beta=ST_DevM_VVH_DDP_current_npt[complexity][1])
        ST_DevM_VVM_DDP_current_like = pm.Beta("ST_DevM_VVM_DDP_current_like", alpha=ST_DevM_VVM_DDP_current_npt[complexity][0], beta=ST_DevM_VVM_DDP_current_npt[complexity][1])
        ST_DevM_VVL_DDP_current_like = pm.Beta("ST_DevM_VVL_DDP_current_like", alpha=ST_DevM_VVL_DDP_current_npt[complexity][0], beta=ST_DevM_VVL_DDP_current_npt[complexity][1])
        ST_DevL_VVH_DDP_current_like = pm.Beta("ST_DevL_VVH_DDP_current_like", alpha=ST_DevL_VVH_DDP_current_npt[complexity][0], beta=ST_DevL_VVH_DDP_current_npt[complexity][1])
        ST_DevL_VVM_DDP_current_like = pm.Beta("ST_DevL_VVM_DDP_current_like", alpha=ST_DevL_VVM_DDP_current_npt[complexity][0], beta=ST_DevL_VVM_DDP_current_npt[complexity][1])
        ST_DevL_VVL_DDP_current_like = pm.Beta("ST_DevL_VVL_DDP_current_like", alpha=ST_DevL_VVL_DDP_current_npt[complexity][0], beta=ST_DevL_VVL_DDP_current_npt[complexity][1])

        # Defect Detection Probability (current): the integral of P(DDP_current|Dev, VV) dDev,VV
        ST_Defect_Detection_Probability_current = ST_DevH_post * ST_VVH_post * ST_DevH_VVH_DDP_current_like + ST_DevH_post * ST_VVM_post * ST_DevH_VVM_DDP_current_like + ST_DevH_post * ST_VVL_post * ST_DevH_VVL_DDP_current_like + ST_DevM_post * ST_VVH_post * ST_DevM_VVH_DDP_current_like + ST_DevM_post * ST_VVM_post * ST_DevM_VVM_DDP_current_like + ST_DevM_post * ST_VVL_post * ST_DevM_VVL_DDP_current_like + ST_DevL_post * ST_VVH_post * ST_DevL_VVH_DDP_current_like + ST_DevL_post * ST_VVM_post * ST_DevL_VVM_DDP_current_like + ST_DevL_post * ST_VVL_post * ST_DevL_VVL_DDP_current_like

        ST_Detected_Defect_current = ST_Defect_introduced_in_current * ST_Defect_Detection_Probability_current

        ST_Remaining_Defect_current = ST_Defect_introduced_in_current - ST_Detected_Defect_current

        # Defect Detection Probability (previous) likelihood: P(DDP_previous|state of Dev quality, state of VV quality)
        ST_DevH_VVH_DDP_previous_like = pm.Beta("ST_DevH_VVH_DDP_previous_like", alpha=ST_DevH_VVH_DDP_previous_npt[complexity][0], beta=ST_DevH_VVH_DDP_previous_npt[complexity][1])
        ST_DevH_VVM_DDP_previous_like = pm.Beta("ST_DevH_VVM_DDP_previous_like", alpha=ST_DevH_VVM_DDP_previous_npt[complexity][0], beta=ST_DevH_VVM_DDP_previous_npt[complexity][1])
        ST_DevH_VVL_DDP_previous_like = pm.Beta("ST_DevH_VVL_DDP_previous_like", alpha=ST_DevH_VVL_DDP_previous_npt[complexity][0], beta=ST_DevH_VVL_DDP_previous_npt[complexity][1])
        ST_DevM_VVH_DDP_previous_like = pm.Beta("ST_DevM_VVH_DDP_previous_like", alpha=ST_DevM_VVH_DDP_previous_npt[complexity][0], beta=ST_DevM_VVH_DDP_previous_npt[complexity][1])
        ST_DevM_VVM_DDP_previous_like = pm.Beta("ST_DevM_VVM_DDP_previous_like", alpha=ST_DevM_VVM_DDP_previous_npt[complexity][0], beta=ST_DevM_VVM_DDP_previous_npt[complexity][1])
        ST_DevM_VVL_DDP_previous_like = pm.Beta("ST_DevM_VVL_DDP_previous_like", alpha=ST_DevM_VVL_DDP_previous_npt[complexity][0], beta=ST_DevM_VVL_DDP_previous_npt[complexity][1])
        ST_DevL_VVH_DDP_previous_like = pm.Beta("ST_DevL_VVH_DDP_previous_like", alpha=ST_DevL_VVH_DDP_previous_npt[complexity][0], beta=ST_DevL_VVH_DDP_previous_npt[complexity][1])
        ST_DevL_VVM_DDP_previous_like = pm.Beta("ST_DevL_VVM_DDP_previous_like", alpha=ST_DevL_VVM_DDP_previous_npt[complexity][0], beta=ST_DevL_VVM_DDP_previous_npt[complexity][1])
        ST_DevL_VVL_DDP_previous_like = pm.Beta("ST_DevL_VVL_DDP_previous_like", alpha=ST_DevL_VVL_DDP_previous_npt[complexity][0], beta=ST_DevL_VVL_DDP_previous_npt[complexity][1])

        # Defect Detection Probability (previous): the integral of P(DDP_previous|Dev, VV) dDev,VV
        ST_Defect_Detection_Probability_previous = ST_DevH_post * ST_VVH_post * ST_DevH_VVH_DDP_previous_like + ST_DevH_post * ST_VVM_post * ST_DevH_VVM_DDP_previous_like + ST_DevH_post * ST_VVL_post * ST_DevH_VVL_DDP_previous_like + ST_DevM_post * ST_VVH_post * ST_DevM_VVH_DDP_previous_like + ST_DevM_post * ST_VVM_post * ST_DevM_VVM_DDP_previous_like + ST_DevM_post * ST_VVL_post * ST_DevM_VVL_DDP_previous_like + ST_DevL_post * ST_VVH_post * ST_DevL_VVH_DDP_previous_like + ST_DevL_post * ST_VVM_post * ST_DevL_VVM_DDP_previous_like + ST_DevL_post * ST_VVL_post * ST_DevL_VVL_DDP_previous_like

        ST_Detected_Defect_previous = IM_Total_Remained_Defect * ST_Defect_Detection_Probability_previous

        ST_Remaining_Defect_previous = IM_Total_Remained_Defect - ST_Detected_Defect_previous

        ST_Total_Remained_Defect = pm.Deterministic("ST_Total_Remained_Defect", ST_Remaining_Defect_current + ST_Remaining_Defect_previous)

        # Submodel - Installation & Checkout phase
        temp_h = IC_Dev_trace.posterior["IC_DevH_post"].mean().item()
        temp_m = IC_Dev_trace.posterior["IC_DevM_post"].mean().item()
        temp_l = IC_Dev_trace.posterior["IC_DevL_post"].mean().item()
        IC_DevH_post = temp_h / (temp_h + temp_m + temp_l)
        IC_DevM_post = temp_m / (temp_h + temp_m + temp_l)
        IC_DevL_post = temp_l / (temp_h + temp_m + temp_l)

        temp_h = IC_VV_trace.posterior["IC_VVH_post"].mean().item()
        temp_m = IC_VV_trace.posterior["IC_VVM_post"].mean().item()
        temp_l = IC_VV_trace.posterior["IC_VVL_post"].mean().item()
        IC_VVH_post = temp_h / (temp_h + temp_m + temp_l)
        IC_VVM_post = temp_m / (temp_h + temp_m + temp_l)
        IC_VVL_post = temp_l / (temp_h + temp_m + temp_l)

        # Defect Density likelihood: P(Defect Density|state of Dev quality)
        IC_DevH_DD_like = pm.Gamma("IC_DevH_DD_like", alpha=0.6106, beta=3.4640)
        IC_DevM_DD_like = pm.Gamma("IC_DevM_DD_like", alpha=0.6838, beta=2.6797)
        IC_DevL_DD_like = pm.Gamma("IC_DevL_DD_like", alpha=0.6514, beta=2.3803)

        # Defect density: the integral of P(Dev)*P(Defect Density|Dev) dDev
        IC_Defect_Density = (IC_DevH_post * IC_DevH_DD_like + IC_DevM_post * IC_DevM_DD_like + IC_DevL_post * IC_DevL_DD_like)

        IC_Defect_introduced_in_current = pm.Deterministic("IC_Defect_introduced_in_current", function_point * IC_Defect_Density)

        # Defect Detection Probability (current) likelihood: P(DDP_current|state of VV quality)
        IC_VVH_DDP_current_like = pm.Beta("IC_VVH_DDP_current_like", alpha=IC_VVH_DDP_current_npt[complexity][0], beta=IC_VVH_DDP_current_npt[complexity][1])
        IC_VVM_DDP_current_like = pm.Beta("IC_VVM_DDP_current_like", alpha=IC_VVM_DDP_current_npt[complexity][0], beta=IC_VVM_DDP_current_npt[complexity][1])
        IC_VVL_DDP_current_like = pm.Beta("IC_VVL_DDP_current_like", alpha=IC_VVL_DDP_current_npt[complexity][0], beta=IC_VVL_DDP_current_npt[complexity][1])

        # Defect Detection Probability (current): the integral of P(DDP_current|VV) dVV
        IC_Defect_Detection_Probability_current = IC_VVH_post * IC_VVH_DDP_current_like + IC_VVM_post * IC_VVM_DDP_current_like + IC_VVL_post * IC_VVL_DDP_current_like

        IC_Detected_Defect_current = IC_Defect_introduced_in_current * IC_Defect_Detection_Probability_current

        IC_Remaining_Defect_current = IC_Defect_introduced_in_current - IC_Detected_Defect_current

        # Defect Detection Probability (previous) likelihood: P(DDP_previous|state of VV quality)
        IC_VVH_DDP_previous_like = pm.Beta("IC_VVH_DDP_previous_like", alpha=IC_VVH_DDP_previous_npt[complexity][0], beta=IC_VVH_DDP_previous_npt[complexity][1])
        IC_VVM_DDP_previous_like = pm.Beta("IC_VVM_DDP_previous_like", alpha=IC_VVM_DDP_previous_npt[complexity][0], beta=IC_VVM_DDP_previous_npt[complexity][1])
        IC_VVL_DDP_previous_like = pm.Beta("IC_VVL_DDP_previous_like", alpha=IC_VVL_DDP_previous_npt[complexity][0], beta=IC_VVL_DDP_previous_npt[complexity][1])

        # Defect Detection Probability (previous): the integral of P(DDP_previous|VV) dVV
        IC_Defect_Detection_Probability_previous = IC_VVH_post * IC_VVH_DDP_previous_like + IC_VVM_post * IC_VVM_DDP_previous_like + IC_VVL_post * IC_VVL_DDP_previous_like

        IC_Detected_Defect_previous = ST_Total_Remained_Defect * IC_Defect_Detection_Probability_previous

        IC_Remaining_Defect_previous = ST_Total_Remained_Defect - IC_Detected_Defect_previous

        IC_Total_Remained_Defect = pm.Deterministic("IC_Total_Remained_Defect", IC_Remaining_Defect_current + IC_Remaining_Defect_previous)

        generic_SFP = pm.LogNormal("generic_SFP", mu=(-10.45), sigma=2.217)
        generic_number_of_defects = from_posterior("generic_number_of_defects", generic_trace.posterior["generic_IC_Total_Remained_Defect"], bins=interpolation_bins)

        generic_FSD = pm.Deterministic("generic_FSD", generic_SFP / generic_number_of_defects)

        PFD = pm.Deterministic("PFD", generic_FSD * IC_Total_Remained_Defect)
    return model
