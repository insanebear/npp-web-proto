import pymc as pm

from .bbn_parameter import *
from .data import generic_data

def create_generic_model():
    # generic data for fault size distritbution (FSD)
    genericData = generic_data()
    generic_function_point = genericData.function_point
    generic_complexity = genericData.complexity
    generic_attr_states = genericData.attr_states

    model = pm.Model()
    with model:
        # Generic Dev Attribute model - Requirement phase
        # prior probability of Dev quality in SR phase
        SR_DevH_prior = pm.Beta("SR_DevH_prior", alpha=4.42, beta=22.04)
        SR_DevM_prior = pm.Beta("SR_DevM_prior", alpha=4.47, beta=2.73)
        SR_DevL_prior = pm.Beta("SR_DevL_prior", alpha=1.25, beta=4.49)
        # Attribute Software Development Planning
        generic_SR_SDP_DevH_like = pm.TruncatedNormal("generic_SR_SDP_DevH_like",
                                            mu=SR_SDP_DevH_npt[generic_attr_states["SR_SDP_state"]][0], sigma=SR_SDP_DevH_npt[generic_attr_states["SR_SDP_state"]][1],
                                            lower=0, upper=1)
        generic_SR_SDP_DevM_like = pm.TruncatedNormal("generic_SR_SDP_DevM_like",
                                            mu=SR_SDP_DevM_npt[generic_attr_states["SR_SDP_state"]][0], sigma=SR_SDP_DevM_npt[generic_attr_states["SR_SDP_state"]][1],
                                            lower=0, upper=1)
        generic_SR_SDP_DevL_like = pm.TruncatedNormal("generic_SR_SDP_DevL_like",
                                            mu=SR_SDP_DevL_npt[generic_attr_states["SR_SDP_state"]][0], sigma=SR_SDP_DevL_npt[generic_attr_states["SR_SDP_state"]][1],
                                            lower=0, upper=1)
        # Attribute Document of a Concept Documentation
        generic_SR_CD_DevH_like = pm.TruncatedNormal("generic_SR_CD_DevH_like",
                                            mu=SR_CD_DevH_npt[generic_attr_states["SR_CD_state"]][0], sigma=SR_CD_DevH_npt[generic_attr_states["SR_CD_state"]][1],
                                            lower=0, upper=1)
        generic_SR_CD_DevM_like = pm.TruncatedNormal("generic_SR_CD_DevM_like",
                                            mu=SR_CD_DevM_npt[generic_attr_states["SR_CD_state"]][0], sigma=SR_CD_DevM_npt[generic_attr_states["SR_CD_state"]][1],
                                            lower=0, upper=1)
        generic_SR_CD_DevL_like = pm.TruncatedNormal("generic_SR_CD_DevL_like",
                                            mu=SR_CD_DevL_npt[generic_attr_states["SR_CD_state"]][0], sigma=SR_CD_DevL_npt[generic_attr_states["SR_CD_state"]][1],
                                            lower=0, upper=1)
        # Attribute Document of Software Requirements Specifications
        generic_SR_SRS_DevH_like = pm.TruncatedNormal("generic_SR_SRS_DevH_like",
                                            mu=SR_SRS_DevH_npt[generic_attr_states["SR_SRS_state"]][0], sigma=SR_SRS_DevH_npt[generic_attr_states["SR_SRS_state"]][1],
                                            lower=0, upper=1)
        generic_SR_SRS_DevM_like = pm.TruncatedNormal("generic_SR_SRS_DevM_like",
                                            mu=SR_SRS_DevM_npt[generic_attr_states["SR_SRS_state"]][0], sigma=SR_SRS_DevM_npt[generic_attr_states["SR_SRS_state"]][1],
                                            lower=0, upper=1)
        generic_SR_SRS_DevL_like = pm.TruncatedNormal("generic_SR_SRS_DevL_like",
                                            mu=SR_SRS_DevL_npt[generic_attr_states["SR_SRS_state"]][0], sigma=SR_SRS_DevL_npt[generic_attr_states["SR_SRS_state"]][1],
                                            lower=0, upper=1)
        # Attribute Traceability Analysis
        generic_SR_TA_DevH_like = pm.TruncatedNormal("generic_SR_TA_DevH_like",
                                            mu=SR_TA_DevH_npt[generic_attr_states["SR_TA_state"]][0], sigma=SR_TA_DevH_npt[generic_attr_states["SR_TA_state"]][1],
                                            lower=0, upper=1)
        generic_SR_TA_DevM_like = pm.TruncatedNormal("generic_SR_TA_DevM_like",
                                            mu=SR_TA_DevM_npt[generic_attr_states["SR_TA_state"]][0], sigma=SR_TA_DevM_npt[generic_attr_states["SR_TA_state"]][1],
                                            lower=0, upper=1)
        generic_SR_TA_DevL_like = pm.TruncatedNormal("generic_SR_TA_DevL_like",
                                            mu=SR_TA_DevL_npt[generic_attr_states["SR_TA_state"]][0], sigma=SR_TA_DevL_npt[generic_attr_states["SR_TA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Criticality Analysis
        generic_SR_CA_DevH_like = pm.TruncatedNormal("generic_SR_CA_DevH_like",
                                            mu=SR_CA_DevH_npt[generic_attr_states["SR_CA_state"]][0], sigma=SR_CA_DevH_npt[generic_attr_states["SR_CA_state"]][1],
                                            lower=0, upper=1)
        generic_SR_CA_DevM_like = pm.TruncatedNormal("generic_SR_CA_DevM_like",
                                            mu=SR_CA_DevM_npt[generic_attr_states["SR_CA_state"]][0], sigma=SR_CA_DevM_npt[generic_attr_states["SR_CA_state"]][1],
                                            lower=0, upper=1)
        generic_SR_CA_DevL_like = pm.TruncatedNormal("generic_SR_CA_DevL_like",
                                            mu=SR_CA_DevL_npt[generic_attr_states["SR_CA_state"]][0], sigma=SR_CA_DevL_npt[generic_attr_states["SR_CA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Hazard Analysis
        generic_SR_HA_DevH_like = pm.TruncatedNormal("generic_SR_HA_DevH_like",
                                            mu=SR_HA_DevH_npt[generic_attr_states["SR_HA_state"]][0], sigma=SR_HA_DevH_npt[generic_attr_states["SR_HA_state"]][1],
                                            lower=0, upper=1)
        generic_SR_HA_DevM_like = pm.TruncatedNormal("generic_SR_HA_DevM_like",
                                            mu=SR_HA_DevM_npt[generic_attr_states["SR_HA_state"]][0], sigma=SR_HA_DevM_npt[generic_attr_states["SR_HA_state"]][1],
                                            lower=0, upper=1)
        generic_SR_HA_DevL_like = pm.TruncatedNormal("generic_SR_HA_DevL_like",
                                            mu=SR_HA_DevL_npt[generic_attr_states["SR_HA_state"]][0], sigma=SR_HA_DevL_npt[generic_attr_states["SR_HA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Security Analysis
        generic_SR_SA_DevH_like = pm.TruncatedNormal("generic_SR_SA_DevH_like",
                                            mu=SR_SA_DevH_npt[generic_attr_states["SR_SA_state"]][0], sigma=SR_SA_DevH_npt[generic_attr_states["SR_SA_state"]][1],
                                            lower=0, upper=1)
        generic_SR_SA_DevM_like = pm.TruncatedNormal("generic_SR_SA_DevM_like",
                                            mu=SR_SA_DevM_npt[generic_attr_states["SR_SA_state"]][0], sigma=SR_SA_DevM_npt[generic_attr_states["SR_SA_state"]][1],
                                            lower=0, upper=1)
        generic_SR_SA_DevL_like = pm.TruncatedNormal("generic_SR_SA_DevL_like",
                                            mu=SR_SA_DevL_npt[generic_attr_states["SR_SA_state"]][0], sigma=SR_SA_DevL_npt[generic_attr_states["SR_SA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Risk Analysis
        generic_SR_RA_DevH_like = pm.TruncatedNormal("generic_SR_RA_DevH_like",
                                            mu=SR_RA_DevH_npt[generic_attr_states["SR_RA_state"]][0], sigma=SR_RA_DevH_npt[generic_attr_states["SR_RA_state"]][1],
                                            lower=0, upper=1)
        generic_SR_RA_DevM_like = pm.TruncatedNormal("generic_SR_RA_DevM_like",
                                            mu=SR_RA_DevM_npt[generic_attr_states["SR_RA_state"]][0], sigma=SR_RA_DevM_npt[generic_attr_states["SR_RA_state"]][1],
                                            lower=0, upper=1)
        generic_SR_RA_DevL_like = pm.TruncatedNormal("generic_SR_RA_DevL_like",
                                            mu=SR_RA_DevL_npt[generic_attr_states["SR_RA_state"]][0], sigma=SR_RA_DevL_npt[generic_attr_states["SR_RA_state"]][1],
                                            lower=0, upper=1)
        # Attribute System/Software Qualification Test Plan Generation
        generic_SR_SQTPG_DevH_like = pm.TruncatedNormal("generic_SR_SQTPG_DevH_like",
                                                mu=SR_SQTPG_DevH_npt[generic_attr_states["SR_SQTPG_state"]][0], sigma=SR_SQTPG_DevH_npt[generic_attr_states["SR_SQTPG_state"]][1],
                                                lower=0, upper=1)
        generic_SR_SQTPG_DevM_like = pm.TruncatedNormal("generic_SR_SQTPG_DevM_like",
                                                mu=SR_SQTPG_DevM_npt[generic_attr_states["SR_SQTPG_state"]][0], sigma=SR_SQTPG_DevM_npt[generic_attr_states["SR_SQTPG_state"]][1],
                                                lower=0, upper=1)
        generic_SR_SQTPG_DevL_like = pm.TruncatedNormal("generic_SR_SQTPG_DevL_like",
                                                mu=SR_SQTPG_DevL_npt[generic_attr_states["SR_SQTPG_state"]][0], sigma=SR_SQTPG_DevL_npt[generic_attr_states["SR_SQTPG_state"]][1],
                                                lower=0, upper=1)
        # Attribute System/Software Acceptance Test Plan Generation
        generic_SR_SATPG_DevH_like = pm.TruncatedNormal("generic_SR_SATPG_DevH_like",
                                                mu=SR_SATPG_DevH_npt[generic_attr_states["SR_SATPG_state"]][0], sigma=SR_SATPG_DevH_npt[generic_attr_states["SR_SATPG_state"]][1],
                                                lower=0, upper=1)
        generic_SR_SATPG_DevM_like = pm.TruncatedNormal("generic_SR_SATPG_DevM_like",
                                                mu=SR_SATPG_DevM_npt[generic_attr_states["SR_SATPG_state"]][0], sigma=SR_SATPG_DevM_npt[generic_attr_states["SR_SATPG_state"]][1],
                                                lower=0, upper=1)
        generic_SR_SATPG_DevL_like = pm.TruncatedNormal("generic_SR_SATPG_DevL_like",
                                                mu=SR_SATPG_DevL_npt[generic_attr_states["SR_SATPG_state"]][0], sigma=SR_SATPG_DevL_npt[generic_attr_states["SR_SATPG_state"]][1],
                                                lower=0, upper=1)
        # Attribute Configuration Management
        generic_SR_CM_DevH_like = pm.TruncatedNormal("generic_SR_CM_DevH_like",
                                            mu=SR_CM_DevH_npt[generic_attr_states["SR_CM_state"]][0], sigma=SR_CM_DevH_npt[generic_attr_states["SR_CM_state"]][1],
                                            lower=0, upper=1)
        generic_SR_CM_DevM_like = pm.TruncatedNormal("generic_SR_CM_DevM_like",
                                            mu=SR_CM_DevM_npt[generic_attr_states["SR_CM_state"]][0], sigma=SR_CM_DevM_npt[generic_attr_states["SR_CM_state"]][1],
                                            lower=0, upper=1)
        generic_SR_CM_DevL_like = pm.TruncatedNormal("generic_SR_CM_DevL_like",
                                            mu=SR_CM_DevL_npt[generic_attr_states["SR_CM_state"]][0], sigma=SR_CM_DevL_npt[generic_attr_states["SR_CM_state"]][1],
                                            lower=0, upper=1)
        # Attribute Review and Audit
        generic_SR_RaA_DevH_like = pm.TruncatedNormal("generic_SR_RaA_DevH_like",
                                            mu=SR_RaA_DevH_npt[generic_attr_states["SR_RaA_state"]][0], sigma=SR_RaA_DevH_npt[generic_attr_states["SR_RaA_state"]][1],
                                            lower=0, upper=1)
        generic_SR_RaA_DevM_like = pm.TruncatedNormal("generic_SR_RaA_DevM_like",
                                            mu=SR_RaA_DevM_npt[generic_attr_states["SR_RaA_state"]][0], sigma=SR_RaA_DevM_npt[generic_attr_states["SR_RaA_state"]][1],
                                            lower=0, upper=1)
        generic_SR_RaA_DevL_like = pm.TruncatedNormal("generic_SR_RaA_DevL_like",
                                            mu=SR_RaA_DevL_npt[generic_attr_states["SR_RaA_state"]][0], sigma=SR_RaA_DevL_npt[generic_attr_states["SR_RaA_state"]][1],
                                            lower=0, upper=1)
        # m1-m3: a part of marginal probability
        # m1 = P(Dev=H)P(attribute states|Dev=H)
        # m2 = P(Dev=M)P(attribute states|Dev=M)
        # m3 = P(Dev=L)P(attribute states|Dev=L)
        generic_SR_Dev_m1 = SR_DevH_prior * generic_SR_SDP_DevH_like * generic_SR_CD_DevH_like * generic_SR_SRS_DevH_like * generic_SR_TA_DevH_like * generic_SR_CA_DevH_like * generic_SR_HA_DevH_like * generic_SR_SA_DevH_like * generic_SR_RA_DevH_like * generic_SR_SQTPG_DevH_like * generic_SR_SATPG_DevH_like * generic_SR_CM_DevH_like * generic_SR_RaA_DevH_like
        generic_SR_Dev_m2 = SR_DevM_prior * generic_SR_SDP_DevM_like * generic_SR_CD_DevM_like * generic_SR_SRS_DevM_like * generic_SR_TA_DevM_like * generic_SR_CA_DevM_like * generic_SR_HA_DevM_like * generic_SR_SA_DevM_like * generic_SR_RA_DevM_like * generic_SR_SQTPG_DevM_like * generic_SR_SATPG_DevM_like * generic_SR_CM_DevM_like * generic_SR_RaA_DevM_like
        generic_SR_Dev_m3 = SR_DevL_prior * generic_SR_SDP_DevL_like * generic_SR_CD_DevL_like * generic_SR_SRS_DevL_like * generic_SR_TA_DevL_like * generic_SR_CA_DevL_like * generic_SR_HA_DevL_like * generic_SR_SA_DevL_like * generic_SR_RA_DevL_like * generic_SR_SQTPG_DevL_like * generic_SR_SATPG_DevL_like * generic_SR_CM_DevL_like * generic_SR_RaA_DevL_like

        # k = 1 / marginal probability
        generic_SR_Dev_k = 1 / (generic_SR_Dev_m1 + generic_SR_Dev_m2 + generic_SR_Dev_m3)

        # posterior probability of Dev quality in SR phase
        generic_SR_DevH_post = generic_SR_Dev_k * generic_SR_Dev_m1
        generic_SR_DevM_post = generic_SR_Dev_k * generic_SR_Dev_m2
        generic_SR_DevL_post = generic_SR_Dev_k * generic_SR_Dev_m3

        # Generic V&V Attribute model - Requirement phase
        # prior probability of V&V quality in SR phase
        SR_VVH_prior = pm.Beta("SR_VVH_prior", alpha=0.67, beta=3.23)
        SR_VVM_prior = pm.Beta("SR_VVM_prior", alpha=3.21, beta=2.21)
        SR_VVL_prior = pm.Beta("SR_VVL_prior", alpha=2.10, beta=7.19)
        # Attribute Software V&V Planning
        generic_SR_SVVP_VVH_like = pm.TruncatedNormal("generic_SR_SVVP_VVH_like",
                                            mu=SR_SVVP_VVH_npt[generic_attr_states["SR_SVVP_state"]][0], sigma=SR_SVVP_VVH_npt[generic_attr_states["SR_SVVP_state"]][1],
                                            lower=0, upper=1)
        generic_SR_SVVP_VVM_like = pm.TruncatedNormal("generic_SR_SVVP_VVM_like",
                                            mu=SR_SVVP_VVM_npt[generic_attr_states["SR_SVVP_state"]][0], sigma=SR_SVVP_VVM_npt[generic_attr_states["SR_SVVP_state"]][1],
                                            lower=0, upper=1)
        generic_SR_SVVP_VVL_like = pm.TruncatedNormal("generic_SR_SVVP_VVL_like",
                                            mu=SR_SVVP_VVL_npt[generic_attr_states["SR_SVVP_state"]][0], sigma=SR_SVVP_VVL_npt[generic_attr_states["SR_SVVP_state"]][1],
                                            lower=0, upper=1)
        # Attribute Concept Documentation Evaluation
        generic_SR_CDE_VVH_like = pm.TruncatedNormal("generic_SR_CDE_VVH_like",
                                            mu=SR_CDE_VVH_npt[generic_attr_states["SR_CDE_state"]][0], sigma=SR_CDE_VVH_npt[generic_attr_states["SR_CDE_state"]][1],
                                            lower=0, upper=1)
        generic_SR_CDE_VVM_like = pm.TruncatedNormal("generic_SR_CDE_VVM_like",
                                            mu=SR_CDE_VVM_npt[generic_attr_states["SR_CDE_state"]][0], sigma=SR_CDE_VVM_npt[generic_attr_states["SR_CDE_state"]][1],
                                            lower=0, upper=1)
        generic_SR_CDE_VVL_like = pm.TruncatedNormal("generic_SR_CDE_VVL_like",
                                            mu=SR_CDE_VVL_npt[generic_attr_states["SR_CDE_state"]][0], sigma=SR_CDE_VVL_npt[generic_attr_states["SR_CDE_state"]][1],
                                            lower=0, upper=1)
        # Attribute Hardware/Software/User Requirements Allocation Analysis
        generic_SR_HRAA_VVH_like = pm.TruncatedNormal("generic_SR_HRAA_VVH_like",
                                            mu=SR_HRAA_VVH_npt[generic_attr_states["SR_HRAA_state"]][0], sigma=SR_HRAA_VVH_npt[generic_attr_states["SR_HRAA_state"]][1],
                                            lower=0, upper=1)
        generic_SR_HRAA_VVM_like = pm.TruncatedNormal("generic_SR_HRAA_VVM_like",
                                            mu=SR_HRAA_VVM_npt[generic_attr_states["SR_HRAA_state"]][0], sigma=SR_HRAA_VVM_npt[generic_attr_states["SR_HRAA_state"]][1],
                                            lower=0, upper=1)
        generic_SR_HRAA_VVL_like = pm.TruncatedNormal("generic_SR_HRAA_VVL_like",
                                            mu=SR_HRAA_VVL_npt[generic_attr_states["SR_HRAA_state"]][0], sigma=SR_HRAA_VVL_npt[generic_attr_states["SR_HRAA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Document of Software Requirements Evaluation
        generic_SR_SRE_VVH_like = pm.TruncatedNormal("generic_SR_SRE_VVH_like",
                                            mu=SR_SRE_VVH_npt[generic_attr_states["SR_SRE_state"]][0], sigma=SR_SRE_VVH_npt[generic_attr_states["SR_SRE_state"]][1],
                                            lower=0, upper=1)
        generic_SR_SRE_VVM_like = pm.TruncatedNormal("generic_SR_SRE_VVM_like",
                                            mu=SR_SRE_VVM_npt[generic_attr_states["SR_SRE_state"]][0], sigma=SR_SRE_VVM_npt[generic_attr_states["SR_SRE_state"]][1],
                                            lower=0, upper=1)
        generic_SR_SRE_VVL_like = pm.TruncatedNormal("generic_SR_SRE_VVL_like",
                                            mu=SR_SRE_VVL_npt[generic_attr_states["SR_SRE_state"]][0], sigma=SR_SRE_VVL_npt[generic_attr_states["SR_SRE_state"]][1],
                                            lower=0, upper=1)
        # Attribute Interface Analysis V&V
        generic_SR_IAVV_VVH_like = pm.TruncatedNormal("generic_SR_IAVV_VVH_like",
                                            mu=SR_IAVV_VVH_npt[generic_attr_states["SR_IAVV_state"]][0], sigma=SR_IAVV_VVH_npt[generic_attr_states["SR_IAVV_state"]][1],
                                            lower=0, upper=1)
        generic_SR_IAVV_VVM_like = pm.TruncatedNormal("generic_SR_IAVV_VVM_like",
                                            mu=SR_IAVV_VVM_npt[generic_attr_states["SR_IAVV_state"]][0], sigma=SR_IAVV_VVM_npt[generic_attr_states["SR_IAVV_state"]][1],
                                            lower=0, upper=1)
        generic_SR_IAVV_VVL_like = pm.TruncatedNormal("generic_SR_IAVV_VVL_like",
                                            mu=SR_IAVV_VVL_npt[generic_attr_states["SR_IAVV_state"]][0], sigma=SR_IAVV_VVL_npt[generic_attr_states["SR_IAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Traceability Analysis V&V
        generic_SR_TAVV_VVH_like = pm.TruncatedNormal("generic_SR_TAVV_VVH_like",
                                            mu=SR_TAVV_VVH_npt[generic_attr_states["SR_TAVV_state"]][0], sigma=SR_TAVV_VVH_npt[generic_attr_states["SR_TAVV_state"]][1],
                                            lower=0, upper=1)
        generic_SR_TAVV_VVM_like = pm.TruncatedNormal("generic_SR_TAVV_VVM_like",
                                            mu=SR_TAVV_VVM_npt[generic_attr_states["SR_TAVV_state"]][0], sigma=SR_TAVV_VVM_npt[generic_attr_states["SR_TAVV_state"]][1],
                                            lower=0, upper=1)
        generic_SR_TAVV_VVL_like = pm.TruncatedNormal("generic_SR_TAVV_VVL_like",
                                            mu=SR_TAVV_VVL_npt[generic_attr_states["SR_TAVV_state"]][0], sigma=SR_TAVV_VVL_npt[generic_attr_states["SR_TAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Criticality Analysis V&V
        generic_SR_CAVV_VVH_like = pm.TruncatedNormal("generic_SR_CAVV_VVH_like",
                                            mu=SR_CAVV_VVH_npt[generic_attr_states["SR_CAVV_state"]][0], sigma=SR_CAVV_VVH_npt[generic_attr_states["SR_CAVV_state"]][1],
                                            lower=0, upper=1)
        generic_SR_CAVV_VVM_like = pm.TruncatedNormal("generic_SR_CAVV_VVM_like",
                                            mu=SR_CAVV_VVM_npt[generic_attr_states["SR_CAVV_state"]][0], sigma=SR_CAVV_VVM_npt[generic_attr_states["SR_CAVV_state"]][1],
                                            lower=0, upper=1)
        generic_SR_CAVV_VVL_like = pm.TruncatedNormal("generic_SR_CAVV_VVL_like",
                                            mu=SR_CAVV_VVL_npt[generic_attr_states["SR_CAVV_state"]][0], sigma=SR_CAVV_VVL_npt[generic_attr_states["SR_CAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Hazard Analysis V&V
        generic_SR_HAVV_VVH_like = pm.TruncatedNormal("generic_SR_HAVV_VVH_like",
                                            mu=SR_HAVV_VVH_npt[generic_attr_states["SR_HAVV_state"]][0], sigma=SR_HAVV_VVH_npt[generic_attr_states["SR_HAVV_state"]][1],
                                            lower=0, upper=1)
        generic_SR_HAVV_VVM_like = pm.TruncatedNormal("generic_SR_HAVV_VVM_like",
                                            mu=SR_HAVV_VVM_npt[generic_attr_states["SR_HAVV_state"]][0], sigma=SR_HAVV_VVM_npt[generic_attr_states["SR_HAVV_state"]][1],
                                            lower=0, upper=1)
        generic_SR_HAVV_VVL_like = pm.TruncatedNormal("generic_SR_HAVV_VVL_like",
                                            mu=SR_HAVV_VVL_npt[generic_attr_states["SR_HAVV_state"]][0], sigma=SR_HAVV_VVL_npt[generic_attr_states["SR_HAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Security Analysis V&V
        generic_SR_SAVV_VVH_like = pm.TruncatedNormal("generic_SR_SAVV_VVH_like",
                                            mu=SR_SAVV_VVH_npt[generic_attr_states["SR_SAVV_state"]][0], sigma=SR_SAVV_VVH_npt[generic_attr_states["SR_SAVV_state"]][1],
                                            lower=0, upper=1)
        generic_SR_SAVV_VVM_like = pm.TruncatedNormal("generic_SR_SAVV_VVM_like",
                                            mu=SR_SAVV_VVM_npt[generic_attr_states["SR_SAVV_state"]][0], sigma=SR_SAVV_VVM_npt[generic_attr_states["SR_SAVV_state"]][1],
                                            lower=0, upper=1)
        generic_SR_SAVV_VVL_like = pm.TruncatedNormal("generic_SR_SAVV_VVL_like",
                                            mu=SR_SAVV_VVL_npt[generic_attr_states["SR_SAVV_state"]][0], sigma=SR_SAVV_VVL_npt[generic_attr_states["SR_SAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Risk Analysis V&V
        generic_SR_RAVV_VVH_like = pm.TruncatedNormal("generic_SR_RAVV_VVH_like",
                                            mu=SR_RAVV_VVH_npt[generic_attr_states["SR_RAVV_state"]][0], sigma=SR_RAVV_VVH_npt[generic_attr_states["SR_RAVV_state"]][1],
                                            lower=0, upper=1)
        generic_SR_RAVV_VVM_like = pm.TruncatedNormal("generic_SR_RAVV_VVM_like",
                                            mu=SR_RAVV_VVM_npt[generic_attr_states["SR_RAVV_state"]][0], sigma=SR_RAVV_VVM_npt[generic_attr_states["SR_RAVV_state"]][1],
                                            lower=0, upper=1)
        generic_SR_RAVV_VVL_like = pm.TruncatedNormal("generic_SR_RAVV_VVL_like",
                                            mu=SR_RAVV_VVL_npt[generic_attr_states["SR_RAVV_state"]][0], sigma=SR_RAVV_VVL_npt[generic_attr_states["SR_RAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute V&V System/Software Quantification Test Plan Generation
        generic_SR_VVSQTPG_VVH_like = pm.TruncatedNormal("generic_SR_VVSQTPG_VVH_like",
                                                mu=SR_VVSQTPG_VVH_npt[generic_attr_states["SR_VVSQTPG_state"]][0], sigma=SR_VVSQTPG_VVH_npt[generic_attr_states["SR_VVSQTPG_state"]][1],
                                                lower=0, upper=1)
        generic_SR_VVSQTPG_VVM_like = pm.TruncatedNormal("generic_SR_VVSQTPG_VVM_like",
                                                mu=SR_VVSQTPG_VVM_npt[generic_attr_states["SR_VVSQTPG_state"]][0], sigma=SR_VVSQTPG_VVM_npt[generic_attr_states["SR_VVSQTPG_state"]][1],
                                                lower=0, upper=1)
        generic_SR_VVSQTPG_VVL_like = pm.TruncatedNormal("generic_SR_VVSQTPG_VVL_like",
                                                mu=SR_VVSQTPG_VVL_npt[generic_attr_states["SR_VVSQTPG_state"]][0], sigma=SR_VVSQTPG_VVL_npt[generic_attr_states["SR_VVSQTPG_state"]][1],
                                                lower=0, upper=1)
        # Attribute V&V Software Acceptance Test Plan Generation
        generic_SR_VVSATPG_VVH_like = pm.TruncatedNormal("generic_SR_VVSATPG_VVH_like",
                                                mu=SR_VVSATPG_VVH_npt[generic_attr_states["SR_VVSATPG_state"]][0], sigma=SR_VVSATPG_VVH_npt[generic_attr_states["SR_VVSATPG_state"]][1],
                                                lower=0, upper=1)
        generic_SR_VVSATPG_VVM_like = pm.TruncatedNormal("generic_SR_VVSATPG_VVM_like",
                                                mu=SR_VVSATPG_VVM_npt[generic_attr_states["SR_VVSATPG_state"]][0], sigma=SR_VVSATPG_VVM_npt[generic_attr_states["SR_VVSATPG_state"]][1],
                                                lower=0, upper=1)
        generic_SR_VVSATPG_VVL_like = pm.TruncatedNormal("generic_SR_VVSATPG_VVL_like",
                                                mu=SR_VVSATPG_VVL_npt[generic_attr_states["SR_VVSATPG_state"]][0], sigma=SR_VVSATPG_VVL_npt[generic_attr_states["SR_VVSATPG_state"]][1],
                                                lower=0, upper=1)
        # Attribute Configuration Management Assessment
        generic_SR_CMA_VVH_like = pm.TruncatedNormal("generic_SR_CMA_VVH_like",
                                            mu=SR_CMA_VVH_npt[generic_attr_states["SR_CMA_state"]][0], sigma=SR_CMA_VVH_npt[generic_attr_states["SR_CMA_state"]][1],
                                            lower=0, upper=1)
        generic_SR_CMA_VVM_like = pm.TruncatedNormal("generic_SR_CMA_VVM_like",
                                            mu=SR_CMA_VVM_npt[generic_attr_states["SR_CMA_state"]][0], sigma=SR_CMA_VVM_npt[generic_attr_states["SR_CMA_state"]][1],
                                            lower=0, upper=1)
        generic_SR_CMA_VVL_like = pm.TruncatedNormal("generic_SR_CMA_VVL_like",
                                            mu=SR_CMA_VVL_npt[generic_attr_states["SR_CMA_state"]][0], sigma=SR_CMA_VVL_npt[generic_attr_states["SR_CMA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Reviews and Audit V&V
        generic_SR_RaAVV_VVH_like = pm.TruncatedNormal("generic_SR_RaAVV_VVH_like",
                                            mu=SR_RaAVV_VVH_npt[generic_attr_states["SR_RaAVV_state"]][0], sigma=SR_RaAVV_VVH_npt[generic_attr_states["SR_RaAVV_state"]][1],
                                            lower=0, upper=1)
        generic_SR_RaAVV_VVM_like = pm.TruncatedNormal("generic_SR_RaAVV_VVM_like",
                                            mu=SR_RaAVV_VVM_npt[generic_attr_states["SR_RaAVV_state"]][0], sigma=SR_RaAVV_VVM_npt[generic_attr_states["SR_RaAVV_state"]][1],
                                            lower=0, upper=1)
        generic_SR_RaAVV_VVL_like = pm.TruncatedNormal("generic_SR_RaAVV_VVL_like",
                                            mu=SR_RaAVV_VVL_npt[generic_attr_states["SR_RaAVV_state"]][0], sigma=SR_RaAVV_VVL_npt[generic_attr_states["SR_RaAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute V&V Requirements Specifications Phase Activity Summary Report Generation
        generic_SR_VVASRG_VVH_like = pm.TruncatedNormal("generic_SR_VVASRG_VVH_like",
                                                mu=SR_VVASRG_VVH_npt[generic_attr_states["SR_VVASRG_state"]][0], sigma=SR_VVASRG_VVH_npt[generic_attr_states["SR_VVASRG_state"]][1],
                                                lower=0, upper=1)
        generic_SR_VVASRG_VVM_like = pm.TruncatedNormal("generic_SR_VVASRG_VVM_like",
                                                mu=SR_VVASRG_VVM_npt[generic_attr_states["SR_VVASRG_state"]][0], sigma=SR_VVASRG_VVM_npt[generic_attr_states["SR_VVASRG_state"]][1],
                                                lower=0, upper=1)
        generic_SR_VVASRG_VVL_like = pm.TruncatedNormal("generic_SR_VVASRG_VVL_like",
                                                mu=SR_VVASRG_VVL_npt[generic_attr_states["SR_VVASRG_state"]][0], sigma=SR_VVASRG_VVL_npt[generic_attr_states["SR_VVASRG_state"]][1],
                                                lower=0, upper=1)
        # m1-m3: a part of marginal probability
        # m1 = P(VV=H)P(attribute states|VV=H)
        # m2 = P(VV=M)P(attribute states|VV=M)
        # m3 = P(VV=L)P(attribute states|VV=L)
        generic_SR_VV_m1 = SR_VVH_prior * generic_SR_SVVP_VVH_like * generic_SR_CDE_VVH_like * generic_SR_HRAA_VVH_like * generic_SR_SRE_VVH_like * generic_SR_IAVV_VVH_like * generic_SR_TAVV_VVH_like * generic_SR_CAVV_VVH_like * generic_SR_HAVV_VVH_like * generic_SR_SAVV_VVH_like * generic_SR_RAVV_VVH_like * generic_SR_VVSQTPG_VVH_like * generic_SR_VVSATPG_VVH_like * generic_SR_CMA_VVH_like * generic_SR_RaAVV_VVH_like * generic_SR_VVASRG_VVH_like
        generic_SR_VV_m2 = SR_VVM_prior * generic_SR_SVVP_VVM_like * generic_SR_CDE_VVM_like * generic_SR_HRAA_VVM_like * generic_SR_SRE_VVM_like * generic_SR_IAVV_VVM_like * generic_SR_TAVV_VVM_like * generic_SR_CAVV_VVM_like * generic_SR_HAVV_VVM_like * generic_SR_SAVV_VVM_like * generic_SR_RAVV_VVM_like * generic_SR_VVSQTPG_VVM_like * generic_SR_VVSATPG_VVM_like * generic_SR_CMA_VVM_like * generic_SR_RaAVV_VVM_like * generic_SR_VVASRG_VVM_like
        generic_SR_VV_m3 = SR_VVL_prior * generic_SR_SVVP_VVL_like * generic_SR_CDE_VVL_like * generic_SR_HRAA_VVL_like * generic_SR_SRE_VVL_like * generic_SR_IAVV_VVL_like * generic_SR_TAVV_VVL_like * generic_SR_CAVV_VVL_like * generic_SR_HAVV_VVL_like * generic_SR_SAVV_VVL_like * generic_SR_RAVV_VVL_like * generic_SR_VVSQTPG_VVL_like * generic_SR_VVSATPG_VVL_like * generic_SR_CMA_VVL_like * generic_SR_RaAVV_VVL_like * generic_SR_VVASRG_VVL_like

        # k = 1 / marginal probability
        generic_SR_VV_k = 1 / (generic_SR_VV_m1 + generic_SR_VV_m2 + generic_SR_VV_m3)

        # posterior probability of V&V quality in SR phase
        generic_SR_VVH_post = generic_SR_VV_k * generic_SR_VV_m1
        generic_SR_VVM_post = generic_SR_VV_k * generic_SR_VV_m2
        generic_SR_VVL_post = generic_SR_VV_k * generic_SR_VV_m3

        # Generic Submodel - Requirement phase
        # Defect Density likelihood: P(Defect Density|state of Dev quality)
        SR_DevH_DD_like = pm.Gamma("SR_DevH_DD_like", alpha=1.1043, beta=3.5507)
        SR_DevM_DD_like = pm.Gamma("SR_DevM_DD_like", alpha=1.3130, beta=3.3811)
        SR_DevL_DD_like = pm.Gamma("SR_DevL_DD_like", alpha=1.3596, beta=3.1705)

        # Defect density: the integral of P(Dev)*P(Defect Density|Dev) dDev
        generic_SR_Defect_Density = (generic_SR_DevH_post * SR_DevH_DD_like + generic_SR_DevM_post * SR_DevM_DD_like + generic_SR_DevL_post * SR_DevL_DD_like)

        generic_SR_Defect_introduced_in_current = generic_function_point * generic_SR_Defect_Density

        # Defect Detection Probability (current) likelihood: P(DDP_current|state of VV quality)
        generic_SR_VVH_DDP_current_like = pm.Beta("generic_SR_VVH_DDP_current_like", alpha=SR_VVH_DDP_current_npt[generic_complexity][0], beta=SR_VVH_DDP_current_npt[generic_complexity][1])
        generic_SR_VVM_DDP_current_like = pm.Beta("generic_SR_VVM_DDP_current_like", alpha=SR_VVM_DDP_current_npt[generic_complexity][0], beta=SR_VVM_DDP_current_npt[generic_complexity][1])
        generic_SR_VVL_DDP_current_like = pm.Beta("generic_SR_VVL_DDP_current_like", alpha=SR_VVL_DDP_current_npt[generic_complexity][0], beta=SR_VVL_DDP_current_npt[generic_complexity][1])

        # Defect Detection Probability (current): the integral of P(DDP_current|VV) dVV
        generic_SR_Defect_Detection_Probability_current = (generic_SR_VVH_post * generic_SR_VVH_DDP_current_like + generic_SR_VVM_post * generic_SR_VVM_DDP_current_like + generic_SR_VVL_post * generic_SR_VVL_DDP_current_like)

        generic_SR_Detected_Defect_current = generic_SR_Defect_introduced_in_current * generic_SR_Defect_Detection_Probability_current

        generic_SR_Remaining_Defect_current = generic_SR_Defect_introduced_in_current - generic_SR_Detected_Defect_current

        # since there's no phase before the SR phase
        generic_SR_Total_Remained_Defect = generic_SR_Remaining_Defect_current

        # Generic Dev Attribute model - Design phase
        # prior probability of Dev quality in SD phase
        SD_DevH_prior = pm.Beta("SD_DevH_prior", alpha=0.56, beta=1.74)
        SD_DevM_prior = pm.Beta("SD_DevM_prior", alpha=2.40, beta=1.81)
        SD_DevL_prior = pm.Beta("SD_DevL_prior", alpha=4.12, beta=22.06)
        # Attribute Development of Software Architecture Description
        generic_SD_SAD_DevH_like = pm.TruncatedNormal("generic_SD_SAD_DevH_like",
                                            mu=SD_SAD_DevH_npt[generic_attr_states["SD_SAD_state"]][0], sigma=SD_SAD_DevH_npt[generic_attr_states["SD_SAD_state"]][1],
                                            lower=0, upper=1)
        generic_SD_SAD_DevM_like = pm.TruncatedNormal("generic_SD_SAD_DevM_like",
                                            mu=SD_SAD_DevM_npt[generic_attr_states["SD_SAD_state"]][0], sigma=SD_SAD_DevM_npt[generic_attr_states["SD_SAD_state"]][1],
                                            lower=0, upper=1)
        generic_SD_SAD_DevL_like = pm.TruncatedNormal("generic_SD_SAD_DevL_like",
                                            mu=SD_SAD_DevL_npt[generic_attr_states["SD_SAD_state"]][0], sigma=SD_SAD_DevL_npt[generic_attr_states["SD_SAD_state"]][1],
                                            lower=0, upper=1)
        # Attribute Development of Software Design Description
        generic_SD_SDD_DevH_like = pm.TruncatedNormal("generic_SD_SDD_DevH_like",
                                            mu=SD_SDD_DevH_npt[generic_attr_states["SD_SDD_state"]][0], sigma=SD_SDD_DevH_npt[generic_attr_states["SD_SDD_state"]][1],
                                            lower=0, upper=1)
        generic_SD_SDD_DevM_like = pm.TruncatedNormal("generic_SD_SDD_DevM_like",
                                            mu=SD_SDD_DevM_npt[generic_attr_states["SD_SDD_state"]][0], sigma=SD_SDD_DevM_npt[generic_attr_states["SD_SDD_state"]][1],
                                            lower=0, upper=1)
        generic_SD_SDD_DevL_like = pm.TruncatedNormal("generic_SD_SDD_DevL_like",
                                            mu=SD_SDD_DevL_npt[generic_attr_states["SD_SDD_state"]][0], sigma=SD_SDD_DevL_npt[generic_attr_states["SD_SDD_state"]][1],
                                            lower=0, upper=1)
        # Attribute Traceability Analysis - Design Phase
        generic_SD_TA_DevH_like = pm.TruncatedNormal("generic_SD_TA_DevH_like",
                                            mu=SD_TA_DevH_npt[generic_attr_states["SD_TA_state"]][0], sigma=SD_TA_DevH_npt[generic_attr_states["SD_TA_state"]][1],
                                            lower=0, upper=1)
        generic_SD_TA_DevM_like = pm.TruncatedNormal("generic_SD_TA_DevM_like",
                                            mu=SD_TA_DevM_npt[generic_attr_states["SD_TA_state"]][0], sigma=SD_TA_DevM_npt[generic_attr_states["SD_TA_state"]][1],
                                            lower=0, upper=1)
        generic_SD_TA_DevL_like = pm.TruncatedNormal("generic_SD_TA_DevL_like",
                                            mu=SD_TA_DevL_npt[generic_attr_states["SD_TA_state"]][0], sigma=SD_TA_DevL_npt[generic_attr_states["SD_TA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Criticality Analysis - Design Phase
        generic_SD_CA_DevH_like = pm.TruncatedNormal("generic_SD_CA_DevH_like",
                                            mu=SD_CA_DevH_npt[generic_attr_states["SD_CA_state"]][0], sigma=SD_CA_DevH_npt[generic_attr_states["SD_CA_state"]][1],
                                            lower=0, upper=1)
        generic_SD_CA_DevM_like = pm.TruncatedNormal("generic_SD_CA_DevM_like",
                                            mu=SD_CA_DevM_npt[generic_attr_states["SD_CA_state"]][0], sigma=SD_CA_DevM_npt[generic_attr_states["SD_CA_state"]][1],
                                            lower=0, upper=1)
        generic_SD_CA_DevL_like = pm.TruncatedNormal("generic_SD_CA_DevL_like",
                                            mu=SD_CA_DevL_npt[generic_attr_states["SD_CA_state"]][0], sigma=SD_CA_DevL_npt[generic_attr_states["SD_CA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Hazard Analysis - Design Phase
        generic_SD_HA_DevH_like = pm.TruncatedNormal("generic_SD_HA_DevH_like",
                                            mu=SD_HA_DevH_npt[generic_attr_states["SD_HA_state"]][0], sigma=SD_HA_DevH_npt[generic_attr_states["SD_HA_state"]][1],
                                            lower=0, upper=1)
        generic_SD_HA_DevM_like = pm.TruncatedNormal("generic_SD_HA_DevM_like",
                                            mu=SD_HA_DevM_npt[generic_attr_states["SD_HA_state"]][0], sigma=SD_HA_DevM_npt[generic_attr_states["SD_HA_state"]][1],
                                            lower=0, upper=1)
        generic_SD_HA_DevL_like = pm.TruncatedNormal("generic_SD_HA_DevL_like",
                                            mu=SD_HA_DevL_npt[generic_attr_states["SD_HA_state"]][0], sigma=SD_HA_DevL_npt[generic_attr_states["SD_HA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Security Analysis - Design Phase
        generic_SD_SA_DevH_like = pm.TruncatedNormal("generic_SD_SA_DevH_like",
                                            mu=SD_SA_DevH_npt[generic_attr_states["SD_SA_state"]][0], sigma=SD_SA_DevH_npt[generic_attr_states["SD_SA_state"]][1],
                                            lower=0, upper=1)
        generic_SD_SA_DevM_like = pm.TruncatedNormal("generic_SD_SA_DevM_like",
                                            mu=SD_SA_DevM_npt[generic_attr_states["SD_SA_state"]][0], sigma=SD_SA_DevM_npt[generic_attr_states["SD_SA_state"]][1],
                                            lower=0, upper=1)
        generic_SD_SA_DevL_like = pm.TruncatedNormal("generic_SD_SA_DevL_like",
                                            mu=SD_SA_DevL_npt[generic_attr_states["SD_SA_state"]][0], sigma=SD_SA_DevL_npt[generic_attr_states["SD_SA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Risk Analysis - Design Phase
        generic_SD_RA_DevH_like = pm.TruncatedNormal("generic_SD_RA_DevH_like",
                                            mu=SD_RA_DevH_npt[generic_attr_states["SD_RA_state"]][0], sigma=SD_RA_DevH_npt[generic_attr_states["SD_RA_state"]][1],
                                            lower=0, upper=1)
        generic_SD_RA_DevM_like = pm.TruncatedNormal("generic_SD_RA_DevM_like",
                                            mu=SD_RA_DevM_npt[generic_attr_states["SD_RA_state"]][0], sigma=SD_RA_DevM_npt[generic_attr_states["SD_RA_state"]][1],
                                            lower=0, upper=1)
        generic_SD_RA_DevL_like = pm.TruncatedNormal("generic_SD_RA_DevL_like",
                                            mu=SD_RA_DevL_npt[generic_attr_states["SD_RA_state"]][0], sigma=SD_RA_DevL_npt[generic_attr_states["SD_RA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Software Component Test Plan Generation
        generic_SD_SCTPG_DevH_like = pm.TruncatedNormal("generic_SD_SCTPG_DevH_like",
                                                mu=SD_SCTPG_DevH_npt[generic_attr_states["SD_SCTPG_state"]][0], sigma=SD_SCTPG_DevH_npt[generic_attr_states["SD_SCTPG_state"]][1],
                                                lower=0, upper=1)
        generic_SD_SCTPG_DevM_like = pm.TruncatedNormal("generic_SD_SCTPG_DevM_like",
                                                mu=SD_SCTPG_DevM_npt[generic_attr_states["SD_SCTPG_state"]][0], sigma=SD_SCTPG_DevM_npt[generic_attr_states["SD_SCTPG_state"]][1],
                                                lower=0, upper=1)
        generic_SD_SCTPG_DevL_like = pm.TruncatedNormal("generic_SD_SCTPG_DevL_like",
                                                mu=SD_SCTPG_DevL_npt[generic_attr_states["SD_SCTPG_state"]][0], sigma=SD_SCTPG_DevL_npt[generic_attr_states["SD_SCTPG_state"]][1],
                                                lower=0, upper=1)
        # Attribute Software Integration Test Plan Generation
        generic_SD_SITPG_DevH_like = pm.TruncatedNormal("generic_SD_SITPG_DevH_like",
                                                mu=SD_SITPG_DevH_npt[generic_attr_states["SD_SITPG_state"]][0], sigma=SD_SITPG_DevH_npt[generic_attr_states["SD_SITPG_state"]][1],
                                                lower=0, upper=1)
        generic_SD_SITPG_DevM_like = pm.TruncatedNormal("generic_SD_SITPG_DevM_like",
                                                mu=SD_SITPG_DevM_npt[generic_attr_states["SD_SITPG_state"]][0], sigma=SD_SITPG_DevM_npt[generic_attr_states["SD_SITPG_state"]][1],
                                                lower=0, upper=1)
        generic_SD_SITPG_DevL_like = pm.TruncatedNormal("generic_SD_SITPG_DevL_like",
                                                mu=SD_SITPG_DevL_npt[generic_attr_states["SD_SITPG_state"]][0], sigma=SD_SITPG_DevL_npt[generic_attr_states["SD_SITPG_state"]][1],
                                                lower=0, upper=1)
        # Attribute Software Component Test Design Generation
        generic_SD_SCTDG_DevH_like = pm.TruncatedNormal("generic_SD_SCTDG_DevH_like",
                                                mu=SD_SCTDG_DevH_npt[generic_attr_states["SD_SCTDG_state"]][0], sigma=SD_SCTDG_DevH_npt[generic_attr_states["SD_SCTDG_state"]][1],
                                                lower=0, upper=1)
        generic_SD_SCTDG_DevM_like = pm.TruncatedNormal("generic_SD_SCTDG_DevM_like",
                                                mu=SD_SCTDG_DevM_npt[generic_attr_states["SD_SCTDG_state"]][0], sigma=SD_SCTDG_DevM_npt[generic_attr_states["SD_SCTDG_state"]][1],
                                                lower=0, upper=1)
        generic_SD_SCTDG_DevL_like = pm.TruncatedNormal("generic_SD_SCTDG_DevL_like",
                                                mu=SD_SCTDG_DevL_npt[generic_attr_states["SD_SCTDG_state"]][0], sigma=SD_SCTDG_DevL_npt[generic_attr_states["SD_SCTDG_state"]][1],
                                                lower=0, upper=1)
        # Attribute Software Integration Test Design Generation
        generic_SD_SITDG_DevH_like = pm.TruncatedNormal("generic_SD_SITDG_DevH_like",
                                                mu=SD_SITDG_DevH_npt[generic_attr_states["SD_SITDG_state"]][0], sigma=SD_SITDG_DevH_npt[generic_attr_states["SD_SITDG_state"]][1],
                                                lower=0, upper=1)
        generic_SD_SITDG_DevM_like = pm.TruncatedNormal("generic_SD_SITDG_DevM_like",
                                                mu=SD_SITDG_DevM_npt[generic_attr_states["SD_SITDG_state"]][0], sigma=SD_SITDG_DevM_npt[generic_attr_states["SD_SITDG_state"]][1],
                                                lower=0, upper=1)
        generic_SD_SITDG_DevL_like = pm.TruncatedNormal("generic_SD_SITDG_DevL_like",
                                                mu=SD_SITDG_DevL_npt[generic_attr_states["SD_SITDG_state"]][0], sigma=SD_SITDG_DevL_npt[generic_attr_states["SD_SITDG_state"]][1],
                                                lower=0, upper=1)
        # Attribute Software Qualification Test Design Generation
        generic_SD_SQTDG_DevH_like = pm.TruncatedNormal("generic_SD_SQTDG_DevH_like",
                                                mu=SD_SQTDG_DevH_npt[generic_attr_states["SD_SQTDG_state"]][0], sigma=SD_SQTDG_DevH_npt[generic_attr_states["SD_SQTDG_state"]][1],
                                                lower=0, upper=1)
        generic_SD_SQTDG_DevM_like = pm.TruncatedNormal("generic_SD_SQTDG_DevM_like",
                                                mu=SD_SQTDG_DevM_npt[generic_attr_states["SD_SQTDG_state"]][0], sigma=SD_SQTDG_DevM_npt[generic_attr_states["SD_SQTDG_state"]][1],
                                                lower=0, upper=1)
        generic_SD_SQTDG_DevL_like = pm.TruncatedNormal("generic_SD_SQTDG_DevL_like",
                                                mu=SD_SQTDG_DevL_npt[generic_attr_states["SD_SQTDG_state"]][0], sigma=SD_SQTDG_DevL_npt[generic_attr_states["SD_SQTDG_state"]][1],
                                                lower=0, upper=1)
        # Attribute Software Acceptance Test Design Generation
        generic_SD_SATDG_DevH_like = pm.TruncatedNormal("generic_SD_SATDG_DevH_like",
                                                mu=SD_SATDG_DevH_npt[generic_attr_states["SD_SATDG_state"]][0], sigma=SD_SATDG_DevH_npt[generic_attr_states["SD_SATDG_state"]][1],
                                                lower=0, upper=1)
        generic_SD_SATDG_DevM_like = pm.TruncatedNormal("generic_SD_SATDG_DevM_like",
                                                mu=SD_SATDG_DevM_npt[generic_attr_states["SD_SATDG_state"]][0], sigma=SD_SATDG_DevM_npt[generic_attr_states["SD_SATDG_state"]][1],
                                                lower=0, upper=1)
        generic_SD_SATDG_DevL_like = pm.TruncatedNormal("generic_SD_SATDG_DevL_like",
                                                mu=SD_SATDG_DevL_npt[generic_attr_states["SD_SATDG_state"]][0], sigma=SD_SATDG_DevL_npt[generic_attr_states["SD_SATDG_state"]][1],
                                                lower=0, upper=1)
        # Attribute Configuration Management - Design Phase
        generic_SD_CM_DevH_like = pm.TruncatedNormal("generic_SD_CM_DevH_like",
                                            mu=SD_CM_DevH_npt[generic_attr_states["SD_CM_state"]][0], sigma=SD_CM_DevH_npt[generic_attr_states["SD_CM_state"]][1],
                                            lower=0, upper=1)
        generic_SD_CM_DevM_like = pm.TruncatedNormal("generic_SD_CM_DevM_like",
                                            mu=SD_CM_DevM_npt[generic_attr_states["SD_CM_state"]][0], sigma=SD_CM_DevM_npt[generic_attr_states["SD_CM_state"]][1],
                                            lower=0, upper=1)
        generic_SD_CM_DevL_like = pm.TruncatedNormal("generic_SD_CM_DevL_like",
                                            mu=SD_CM_DevL_npt[generic_attr_states["SD_CM_state"]][0], sigma=SD_CM_DevL_npt[generic_attr_states["SD_CM_state"]][1],
                                            lower=0, upper=1)
        # Attribute Reviews and Audit - Design Phase
        generic_SD_RaA_DevH_like = pm.TruncatedNormal("generic_SD_RaA_DevH_like",
                                            mu=SD_RaA_DevH_npt[generic_attr_states["SD_RaA_state"]][0], sigma=SD_RaA_DevH_npt[generic_attr_states["SD_RaA_state"]][1],
                                            lower=0, upper=1)
        generic_SD_RaA_DevM_like = pm.TruncatedNormal("generic_SD_RaA_DevM_like",
                                            mu=SD_RaA_DevM_npt[generic_attr_states["SD_RaA_state"]][0], sigma=SD_RaA_DevM_npt[generic_attr_states["SD_RaA_state"]][1],
                                            lower=0, upper=1)
        generic_SD_RaA_DevL_like = pm.TruncatedNormal("generic_SD_RaA_DevL_like",
                                            mu=SD_RaA_DevL_npt[generic_attr_states["SD_RaA_state"]][0], sigma=SD_RaA_DevL_npt[generic_attr_states["SD_RaA_state"]][1],
                                            lower=0, upper=1)
        # m1-m3: a part of marginal probability
        # m1 = P(Dev=H)P(attribute states|Dev=H)
        # m2 = P(Dev=M)P(attribute states|Dev=M)
        # m3 = P(Dev=L)P(attribute states|Dev=L)
        generic_SD_Dev_m1 = SD_DevH_prior * generic_SD_SAD_DevH_like * generic_SD_SDD_DevH_like * generic_SD_TA_DevH_like * generic_SD_CA_DevH_like * generic_SD_HA_DevH_like * generic_SD_SA_DevH_like * generic_SD_RA_DevH_like * generic_SD_SCTPG_DevH_like * generic_SD_SITPG_DevH_like * generic_SD_SCTDG_DevH_like * generic_SD_SITDG_DevH_like * generic_SD_SQTDG_DevH_like * generic_SD_SATDG_DevH_like * generic_SD_CM_DevH_like * generic_SD_RaA_DevH_like
        generic_SD_Dev_m2 = SD_DevM_prior * generic_SD_SAD_DevM_like * generic_SD_SDD_DevM_like * generic_SD_TA_DevM_like * generic_SD_CA_DevM_like * generic_SD_HA_DevM_like * generic_SD_SA_DevM_like * generic_SD_RA_DevM_like * generic_SD_SCTPG_DevM_like * generic_SD_SITPG_DevM_like * generic_SD_SCTDG_DevM_like * generic_SD_SITDG_DevM_like * generic_SD_SQTDG_DevM_like * generic_SD_SATDG_DevM_like * generic_SD_CM_DevM_like * generic_SD_RaA_DevM_like
        generic_SD_Dev_m3 = SD_DevL_prior * generic_SD_SAD_DevL_like * generic_SD_SDD_DevL_like * generic_SD_TA_DevL_like * generic_SD_CA_DevL_like * generic_SD_HA_DevL_like * generic_SD_SA_DevL_like * generic_SD_RA_DevL_like * generic_SD_SCTPG_DevL_like * generic_SD_SITPG_DevL_like * generic_SD_SCTDG_DevL_like * generic_SD_SITDG_DevL_like * generic_SD_SQTDG_DevL_like * generic_SD_SATDG_DevL_like * generic_SD_CM_DevL_like * generic_SD_RaA_DevL_like

        # k = 1 / marginal probability
        generic_SD_Dev_k = 1 / (generic_SD_Dev_m1 + generic_SD_Dev_m2 + generic_SD_Dev_m3)

        # posterior probability of Dev quality in SD phase
        generic_SD_DevH_post = generic_SD_Dev_k * generic_SD_Dev_m1
        generic_SD_DevM_post = generic_SD_Dev_k * generic_SD_Dev_m2
        generic_SD_DevL_post = generic_SD_Dev_k * generic_SD_Dev_m3

        # Generic V&V Attribute model - Design phase
        # prior probability of V&V quality in SD phase
        SD_VVH_prior = pm.Beta("SD_VVH_prior", alpha=0.56, beta=1.74)
        SD_VVM_prior = pm.Beta("SD_VVM_prior", alpha=2.40, beta=1.81)
        SD_VVL_prior = pm.Beta("SD_VVL_prior", alpha=4.12, beta=22.06)
        # Attribute Design Evaluation
        generic_SD_DE_VVH_like = pm.TruncatedNormal("generic_SD_DE_VVH_like",
                                            mu=SD_DE_VVH_npt[generic_attr_states["SD_DE_state"]][0], sigma=SD_DE_VVH_npt[generic_attr_states["SD_DE_state"]][1],
                                            lower=0, upper=1)
        generic_SD_DE_VVM_like = pm.TruncatedNormal("generic_SD_DE_VVM_like",
                                            mu=SD_DE_VVM_npt[generic_attr_states["SD_DE_state"]][0], sigma=SD_DE_VVM_npt[generic_attr_states["SD_DE_state"]][1],
                                            lower=0, upper=1)
        generic_SD_DE_VVL_like = pm.TruncatedNormal("generic_SD_DE_VVL_like",
                                            mu=SD_DE_VVL_npt[generic_attr_states["SD_DE_state"]][0], sigma=SD_DE_VVL_npt[generic_attr_states["SD_DE_state"]][1],
                                            lower=0, upper=1)
        # Attribute Interface Analysis V&V
        generic_SD_IAVV_VVH_like = pm.TruncatedNormal("generic_SD_IAVV_VVH_like",
                                            mu=SD_IAVV_VVH_npt[generic_attr_states["SD_IAVV_state"]][0], sigma=SD_IAVV_VVH_npt[generic_attr_states["SD_IAVV_state"]][1],
                                            lower=0, upper=1)
        generic_SD_IAVV_VVM_like = pm.TruncatedNormal("generic_SD_IAVV_VVM_like",
                                            mu=SD_IAVV_VVM_npt[generic_attr_states["SD_IAVV_state"]][0], sigma=SD_IAVV_VVM_npt[generic_attr_states["SD_IAVV_state"]][1],
                                            lower=0, upper=1)
        generic_SD_IAVV_VVL_like = pm.TruncatedNormal("generic_SD_IAVV_VVL_like",
                                            mu=SD_IAVV_VVL_npt[generic_attr_states["SD_IAVV_state"]][0], sigma=SD_IAVV_VVL_npt[generic_attr_states["SD_IAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Traceability Analysis V&V - Design Phase
        generic_SD_TAVV_VVH_like = pm.TruncatedNormal("generic_SD_TAVV_VVH_like",
                                            mu=SD_TAVV_VVH_npt[generic_attr_states["SD_TAVV_state"]][0], sigma=SD_TAVV_VVH_npt[generic_attr_states["SD_TAVV_state"]][1],
                                            lower=0, upper=1)
        generic_SD_TAVV_VVM_like = pm.TruncatedNormal("generic_SD_TAVV_VVM_like",
                                            mu=SD_TAVV_VVM_npt[generic_attr_states["SD_TAVV_state"]][0], sigma=SD_TAVV_VVM_npt[generic_attr_states["SD_TAVV_state"]][1],
                                            lower=0, upper=1)
        generic_SD_TAVV_VVL_like = pm.TruncatedNormal("generic_SD_TAVV_VVL_like",
                                            mu=SD_TAVV_VVL_npt[generic_attr_states["SD_TAVV_state"]][0], sigma=SD_TAVV_VVL_npt[generic_attr_states["SD_TAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Criticality Analysis V&V - Design Phase
        generic_SD_CAVV_VVH_like = pm.TruncatedNormal("generic_SD_CAVV_VVH_like",
                                            mu=SD_CAVV_VVH_npt[generic_attr_states["SD_CAVV_state"]][0], sigma=SD_CAVV_VVH_npt[generic_attr_states["SD_CAVV_state"]][1],
                                            lower=0, upper=1)
        generic_SD_CAVV_VVM_like = pm.TruncatedNormal("generic_SD_CAVV_VVM_like",
                                            mu=SD_CAVV_VVM_npt[generic_attr_states["SD_CAVV_state"]][0], sigma=SD_CAVV_VVM_npt[generic_attr_states["SD_CAVV_state"]][1],
                                            lower=0, upper=1)
        generic_SD_CAVV_VVL_like = pm.TruncatedNormal("generic_SD_CAVV_VVL_like",
                                            mu=SD_CAVV_VVL_npt[generic_attr_states["SD_CAVV_state"]][0], sigma=SD_CAVV_VVL_npt[generic_attr_states["SD_CAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Hazard Analysis V&V - Design Phase
        generic_SD_HAVV_VVH_like = pm.TruncatedNormal("generic_SD_HAVV_VVH_like",
                                            mu=SD_HAVV_VVH_npt[generic_attr_states["SD_HAVV_state"]][0], sigma=SD_HAVV_VVH_npt[generic_attr_states["SD_HAVV_state"]][1],
                                            lower=0, upper=1)
        generic_SD_HAVV_VVM_like = pm.TruncatedNormal("generic_SD_HAVV_VVM_like",
                                            mu=SD_HAVV_VVM_npt[generic_attr_states["SD_HAVV_state"]][0], sigma=SD_HAVV_VVM_npt[generic_attr_states["SD_HAVV_state"]][1],
                                            lower=0, upper=1)
        generic_SD_HAVV_VVL_like = pm.TruncatedNormal("generic_SD_HAVV_VVL_like",
                                            mu=SD_HAVV_VVL_npt[generic_attr_states["SD_HAVV_state"]][0], sigma=SD_HAVV_VVL_npt[generic_attr_states["SD_HAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Security Analysis V&V - Design Phase
        generic_SD_SAVV_VVH_like = pm.TruncatedNormal("generic_SD_SAVV_VVH_like",
                                            mu=SD_SAVV_VVH_npt[generic_attr_states["SD_SAVV_state"]][0], sigma=SD_SAVV_VVH_npt[generic_attr_states["SD_SAVV_state"]][1],
                                            lower=0, upper=1)
        generic_SD_SAVV_VVM_like = pm.TruncatedNormal("generic_SD_SAVV_VVM_like",
                                            mu=SD_SAVV_VVM_npt[generic_attr_states["SD_SAVV_state"]][0], sigma=SD_SAVV_VVM_npt[generic_attr_states["SD_SAVV_state"]][1],
                                            lower=0, upper=1)
        generic_SD_SAVV_VVL_like = pm.TruncatedNormal("generic_SD_SAVV_VVL_like",
                                            mu=SD_SAVV_VVL_npt[generic_attr_states["SD_SAVV_state"]][0], sigma=SD_SAVV_VVL_npt[generic_attr_states["SD_SAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Risk Analysis V&V - Design Phase
        generic_SD_RAVV_VVH_like = pm.TruncatedNormal("generic_SD_RAVV_VVH_like",
                                            mu=SD_RAVV_VVH_npt[generic_attr_states["SD_RAVV_state"]][0], sigma=SD_RAVV_VVH_npt[generic_attr_states["SD_RAVV_state"]][1],
                                            lower=0, upper=1)
        generic_SD_RAVV_VVM_like = pm.TruncatedNormal("generic_SD_RAVV_VVM_like",
                                            mu=SD_RAVV_VVM_npt[generic_attr_states["SD_RAVV_state"]][0], sigma=SD_RAVV_VVM_npt[generic_attr_states["SD_RAVV_state"]][1],
                                            lower=0, upper=1)
        generic_SD_RAVV_VVL_like = pm.TruncatedNormal("generic_SD_RAVV_VVL_like",
                                            mu=SD_RAVV_VVL_npt[generic_attr_states["SD_RAVV_state"]][0], sigma=SD_RAVV_VVL_npt[generic_attr_states["SD_RAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute V&V Software Component Test Plan Generation
        generic_SD_VVSCTPG_VVH_like = pm.TruncatedNormal("generic_SD_VVSCTPG_VVH_like",
                                                mu=SD_VVSCTPG_VVH_npt[generic_attr_states["SD_VVSCTPG_state"]][0], sigma=SD_VVSCTPG_VVH_npt[generic_attr_states["SD_VVSCTPG_state"]][1],
                                                lower=0, upper=1)
        generic_SD_VVSCTPG_VVM_like = pm.TruncatedNormal("generic_SD_VVSCTPG_VVM_like",
                                                mu=SD_VVSCTPG_VVM_npt[generic_attr_states["SD_VVSCTPG_state"]][0], sigma=SD_VVSCTPG_VVM_npt[generic_attr_states["SD_VVSCTPG_state"]][1],
                                                lower=0, upper=1)
        generic_SD_VVSCTPG_VVL_like = pm.TruncatedNormal("generic_SD_VVSCTPG_VVL_like",
                                                mu=SD_VVSCTPG_VVL_npt[generic_attr_states["SD_VVSCTPG_state"]][0], sigma=SD_VVSCTPG_VVL_npt[generic_attr_states["SD_VVSCTPG_state"]][1],
                                                lower=0, upper=1)
        # Attribute V&V Software Integration Test Plan Generation
        generic_SD_VVSITPG_VVH_like = pm.TruncatedNormal("generic_SD_VVSITPG_VVH_like",
                                                mu=SD_VVSITPG_VVH_npt[generic_attr_states["SD_VVSITPG_state"]][0], sigma=SD_VVSITPG_VVH_npt[generic_attr_states["SD_VVSITPG_state"]][1],
                                                lower=0, upper=1)
        generic_SD_VVSITPG_VVM_like = pm.TruncatedNormal("generic_SD_VVSITPG_VVM_like",
                                                mu=SD_VVSITPG_VVM_npt[generic_attr_states["SD_VVSITPG_state"]][0], sigma=SD_VVSITPG_VVM_npt[generic_attr_states["SD_VVSITPG_state"]][1],
                                                lower=0, upper=1)
        generic_SD_VVSITPG_VVL_like = pm.TruncatedNormal("generic_SD_VVSITPG_VVL_like",
                                                mu=SD_VVSITPG_VVL_npt[generic_attr_states["SD_VVSITPG_state"]][0], sigma=SD_VVSITPG_VVL_npt[generic_attr_states["SD_VVSITPG_state"]][1],
                                                lower=0, upper=1)
        # Attribute V&V Software Component Test Design Generation
        generic_SD_VVSCTDG_VVH_like = pm.TruncatedNormal("generic_SD_VVSCTDG_VVH_like",
                                                mu=SD_VVSCTDG_VVH_npt[generic_attr_states["SD_VVSCTDG_state"]][0], sigma=SD_VVSCTDG_VVH_npt[generic_attr_states["SD_VVSCTDG_state"]][1],
                                                lower=0, upper=1)
        generic_SD_VVSCTDG_VVM_like = pm.TruncatedNormal("generic_SD_VVSCTDG_VVM_like",
                                                mu=SD_VVSCTDG_VVM_npt[generic_attr_states["SD_VVSCTDG_state"]][0], sigma=SD_VVSCTDG_VVM_npt[generic_attr_states["SD_VVSCTDG_state"]][1],
                                                lower=0, upper=1)
        generic_SD_VVSCTDG_VVL_like = pm.TruncatedNormal("generic_SD_VVSCTDG_VVL_like",
                                                mu=SD_VVSCTDG_VVL_npt[generic_attr_states["SD_VVSCTDG_state"]][0], sigma=SD_VVSCTDG_VVL_npt[generic_attr_states["SD_VVSCTDG_state"]][1],
                                                lower=0, upper=1)
        # Attribute V&V Software Integration Test Design Generation
        generic_SD_VVSITDG_VVH_like = pm.TruncatedNormal("generic_SD_VVSITDG_VVH_like",
                                                mu=SD_VVSITDG_VVH_npt[generic_attr_states["SD_VVSITDG_state"]][0], sigma=SD_VVSITDG_VVH_npt[generic_attr_states["SD_VVSITDG_state"]][1],
                                                lower=0, upper=1)
        generic_SD_VVSITDG_VVM_like = pm.TruncatedNormal("generic_SD_VVSITDG_VVM_like",
                                                mu=SD_VVSITDG_VVM_npt[generic_attr_states["SD_VVSITDG_state"]][0], sigma=SD_VVSITDG_VVM_npt[generic_attr_states["SD_VVSITDG_state"]][1],
                                                lower=0, upper=1)
        generic_SD_VVSITDG_VVL_like = pm.TruncatedNormal("generic_SD_VVSITDG_VVL_like",
                                                mu=SD_VVSITDG_VVL_npt[generic_attr_states["SD_VVSITDG_state"]][0], sigma=SD_VVSITDG_VVL_npt[generic_attr_states["SD_VVSITDG_state"]][1],
                                                lower=0, upper=1)
        # Attribute V&V Software Qualification Test Design Generation
        generic_SD_VVSQTDG_VVH_like = pm.TruncatedNormal("generic_SD_VVSQTDG_VVH_like",
                                                mu=SD_VVSQTDG_VVH_npt[generic_attr_states["SD_VVSQTDG_state"]][0], sigma=SD_VVSQTDG_VVH_npt[generic_attr_states["SD_VVSQTDG_state"]][1],
                                                lower=0, upper=1)
        generic_SD_VVSQTDG_VVM_like = pm.TruncatedNormal("generic_SD_VVSQTDG_VVM_like",
                                                mu=SD_VVSQTDG_VVM_npt[generic_attr_states["SD_VVSQTDG_state"]][0], sigma=SD_VVSQTDG_VVM_npt[generic_attr_states["SD_VVSQTDG_state"]][1],
                                                lower=0, upper=1)
        generic_SD_VVSQTDG_VVL_like = pm.TruncatedNormal("generic_SD_VVSQTDG_VVL_like",
                                                mu=SD_VVSQTDG_VVL_npt[generic_attr_states["SD_VVSQTDG_state"]][0], sigma=SD_VVSQTDG_VVL_npt[generic_attr_states["SD_VVSQTDG_state"]][1],
                                                lower=0, upper=1)
        # Attribute V&V Software Acceptance Test Design Generation
        generic_SD_VVSATDG_VVH_like = pm.TruncatedNormal("generic_SD_VVSATDG_VVH_like",
                                                mu=SD_VVSATDG_VVH_npt[generic_attr_states["SD_VVSATDG_state"]][0], sigma=SD_VVSATDG_VVH_npt[generic_attr_states["SD_VVSATDG_state"]][1],
                                                lower=0, upper=1)
        generic_SD_VVSATDG_VVM_like = pm.TruncatedNormal("generic_SD_VVSATDG_VVM_like",
                                                mu=SD_VVSATDG_VVM_npt[generic_attr_states["SD_VVSATDG_state"]][0], sigma=SD_VVSATDG_VVM_npt[generic_attr_states["SD_VVSATDG_state"]][1],
                                                lower=0, upper=1)
        generic_SD_VVSATDG_VVL_like = pm.TruncatedNormal("generic_SD_VVSATDG_VVL_like",
                                                mu=SD_VVSATDG_VVL_npt[generic_attr_states["SD_VVSATDG_state"]][0], sigma=SD_VVSATDG_VVL_npt[generic_attr_states["SD_VVSATDG_state"]][1],
                                                lower=0, upper=1)
        # Attribute Configuration Management V&V - Design Phase
        generic_SD_CMVV_VVH_like = pm.TruncatedNormal("generic_SD_CMVV_VVH_like",
                                            mu=SD_CMVV_VVH_npt[generic_attr_states["SD_CMVV_state"]][0], sigma=SD_CMVV_VVH_npt[generic_attr_states["SD_CMVV_state"]][1],
                                            lower=0, upper=1)
        generic_SD_CMVV_VVM_like = pm.TruncatedNormal("generic_SD_CMVV_VVM_like",
                                            mu=SD_CMVV_VVM_npt[generic_attr_states["SD_CMVV_state"]][0], sigma=SD_CMVV_VVM_npt[generic_attr_states["SD_CMVV_state"]][1],
                                            lower=0, upper=1)
        generic_SD_CMVV_VVL_like = pm.TruncatedNormal("generic_SD_CMVV_VVL_like",
                                            mu=SD_CMVV_VVL_npt[generic_attr_states["SD_CMVV_state"]][0], sigma=SD_CMVV_VVL_npt[generic_attr_states["SD_CMVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Review and Audit V&V - Design Phase
        generic_SD_RaAVV_VVH_like = pm.TruncatedNormal("generic_SD_RaAVV_VVH_like",
                                            mu=SD_RaAVV_VVH_npt[generic_attr_states["SD_RaAVV_state"]][0], sigma=SD_RaAVV_VVH_npt[generic_attr_states["SD_RaAVV_state"]][1],
                                            lower=0, upper=1)
        generic_SD_RaAVV_VVM_like = pm.TruncatedNormal("generic_SD_RaAVV_VVM_like",
                                            mu=SD_RaAVV_VVM_npt[generic_attr_states["SD_RaAVV_state"]][0], sigma=SD_RaAVV_VVM_npt[generic_attr_states["SD_RaAVV_state"]][1],
                                            lower=0, upper=1)
        generic_SD_RaAVV_VVL_like = pm.TruncatedNormal("generic_SD_RaAVV_VVL_like",
                                            mu=SD_RaAVV_VVL_npt[generic_attr_states["SD_RaAVV_state"]][0], sigma=SD_RaAVV_VVL_npt[generic_attr_states["SD_RaAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute V&V Design Phase Activity Summary Report Generation
        generic_SD_VVASRG_VVH_like = pm.TruncatedNormal("generic_SD_VVASRG_VVH_like",
                                            mu=SD_VVASRG_VVH_npt[generic_attr_states["SD_VVASRG_state"]][0], sigma=SD_VVASRG_VVH_npt[generic_attr_states["SD_VVASRG_state"]][1],
                                            lower=0, upper=1)
        generic_SD_VVASRG_VVM_like = pm.TruncatedNormal("generic_SD_VVASRG_VVM_like",
                                            mu=SD_VVASRG_VVM_npt[generic_attr_states["SD_VVASRG_state"]][0], sigma=SD_VVASRG_VVM_npt[generic_attr_states["SD_VVASRG_state"]][1],
                                            lower=0, upper=1)
        generic_SD_VVASRG_VVL_like = pm.TruncatedNormal("generic_SD_VVASRG_VVL_like",
                                            mu=SD_VVASRG_VVL_npt[generic_attr_states["SD_VVASRG_state"]][0], sigma=SD_VVASRG_VVL_npt[generic_attr_states["SD_VVASRG_state"]][1],
                                            lower=0, upper=1)
        # m1-m3: a part of marginal probability
        # m1 = P(VV=H)P(attribute states|VV=H)
        # m2 = P(VV=M)P(attribute states|VV=M)
        # m3 = P(VV=L)P(attribute states|VV=L)
        generic_SD_VV_m1 = SD_VVH_prior * generic_SD_DE_VVH_like * generic_SD_IAVV_VVH_like * generic_SD_TAVV_VVH_like * generic_SD_CAVV_VVH_like * generic_SD_HAVV_VVH_like * generic_SD_SAVV_VVH_like * generic_SD_RAVV_VVH_like * generic_SD_VVSCTPG_VVH_like * generic_SD_VVSITPG_VVH_like * generic_SD_VVSCTDG_VVH_like * generic_SD_VVSITDG_VVH_like * generic_SD_VVSQTDG_VVH_like * generic_SD_VVSATDG_VVH_like * generic_SD_CMVV_VVH_like * generic_SD_RaAVV_VVH_like * generic_SD_VVASRG_VVH_like
        generic_SD_VV_m2 = SD_VVM_prior * generic_SD_DE_VVM_like * generic_SD_IAVV_VVM_like * generic_SD_TAVV_VVM_like * generic_SD_CAVV_VVM_like * generic_SD_HAVV_VVM_like * generic_SD_SAVV_VVM_like * generic_SD_RAVV_VVM_like * generic_SD_VVSCTPG_VVM_like * generic_SD_VVSITPG_VVM_like * generic_SD_VVSCTDG_VVM_like * generic_SD_VVSITDG_VVM_like * generic_SD_VVSQTDG_VVM_like * generic_SD_VVSATDG_VVM_like * generic_SD_CMVV_VVM_like * generic_SD_RaAVV_VVM_like * generic_SD_VVASRG_VVM_like
        generic_SD_VV_m3 = SD_VVL_prior * generic_SD_DE_VVL_like * generic_SD_IAVV_VVL_like * generic_SD_TAVV_VVL_like * generic_SD_CAVV_VVL_like * generic_SD_HAVV_VVL_like * generic_SD_SAVV_VVL_like * generic_SD_RAVV_VVL_like * generic_SD_VVSCTPG_VVL_like * generic_SD_VVSITPG_VVL_like * generic_SD_VVSCTDG_VVL_like * generic_SD_VVSITDG_VVL_like * generic_SD_VVSQTDG_VVL_like * generic_SD_VVSATDG_VVL_like * generic_SD_CMVV_VVL_like * generic_SD_RaAVV_VVL_like * generic_SD_VVASRG_VVL_like

        # k = 1 / marginal probability
        generic_SD_VV_k = 1 / (generic_SD_VV_m1 + generic_SD_VV_m2 + generic_SD_VV_m3)

        # posterior probability of V&V quality in SD phase
        generic_SD_VVH_post = generic_SD_VV_k * generic_SD_VV_m1
        generic_SD_VVM_post = generic_SD_VV_k * generic_SD_VV_m2
        generic_SD_VVL_post = generic_SD_VV_k * generic_SD_VV_m3

        # Generic Submodel - Design phase

        # Defect Density likelihood: P(Defect Density|state of Dev quality)
        SD_DevH_DD_like = pm.Gamma("SD_DevH_DD_like", alpha=2.2558, beta=3.3680)
        SD_DevM_DD_like = pm.Gamma("SD_DevM_DD_like", alpha=2.7565, beta=3.2526)
        SD_DevL_DD_like = pm.Gamma("SD_DevL_DD_like", alpha=3.0353, beta=3.1522)

        # Defect density: the integral of P(Dev)*P(Defect Density|Dev) dDev
        generic_SD_Defect_Density = (generic_SD_DevH_post * SD_DevH_DD_like + generic_SD_DevM_post * SD_DevM_DD_like + generic_SD_DevL_post * SD_DevL_DD_like)

        generic_SD_Defect_introduced_in_current = generic_function_point * generic_SD_Defect_Density

        # Defect Detection Probability (current) likelihood: P(DDP_current|state of VV quality)
        generic_SD_VVH_DDP_current_like = pm.Beta("generic_SD_VVH_DDP_current_like", alpha=SD_VVH_DDP_current_npt[generic_complexity][0], beta=SD_VVH_DDP_current_npt[generic_complexity][1])
        generic_SD_VVM_DDP_current_like = pm.Beta("generic_SD_VVM_DDP_current_like", alpha=SD_VVM_DDP_current_npt[generic_complexity][0], beta=SD_VVM_DDP_current_npt[generic_complexity][1])
        generic_SD_VVL_DDP_current_like = pm.Beta("generic_SD_VVL_DDP_current_like", alpha=SD_VVL_DDP_current_npt[generic_complexity][0], beta=SD_VVL_DDP_current_npt[generic_complexity][1])

        # Defect Detection Probability (current): the integral of P(DDP_current|VV) dVV
        generic_SD_Defect_Detection_Probability_current = generic_SD_VVH_post * generic_SD_VVH_DDP_current_like + generic_SD_VVM_post * generic_SD_VVM_DDP_current_like + generic_SD_VVL_post * generic_SD_VVL_DDP_current_like

        generic_SD_Detected_Defect_current = generic_SD_Defect_introduced_in_current * generic_SD_Defect_Detection_Probability_current

        generic_SD_Remaining_Defect_current = generic_SD_Defect_introduced_in_current - generic_SD_Detected_Defect_current

        # Defect Detection Probability (previous) likelihood: P(DDP_previous|state of VV quality)
        generic_SD_VVH_DDP_previous_like = pm.Beta("generic_SD_VVH_DDP_previous_like", alpha=SD_VVH_DDP_previous_npt[generic_complexity][0], beta=SD_VVH_DDP_previous_npt[generic_complexity][1])
        generic_SD_VVM_DDP_previous_like = pm.Beta("generic_SD_VVM_DDP_previous_like", alpha=SD_VVM_DDP_previous_npt[generic_complexity][0], beta=SD_VVM_DDP_previous_npt[generic_complexity][1])
        generic_SD_VVL_DDP_previous_like = pm.Beta("generic_SD_VVL_DDP_previous_like", alpha=SD_VVL_DDP_previous_npt[generic_complexity][0], beta=SD_VVL_DDP_previous_npt[generic_complexity][1])

        # Defect Detection Probability (previous): the integral of P(DDP_previous|VV) dVV
        generic_SD_Defect_Detection_Probability_previous = generic_SD_VVH_post * generic_SD_VVH_DDP_previous_like + generic_SD_VVM_post * generic_SD_VVM_DDP_previous_like + generic_SD_VVL_post * generic_SD_VVL_DDP_previous_like

        generic_SD_Detected_Defect_previous = generic_SR_Total_Remained_Defect * generic_SD_Defect_Detection_Probability_previous

        generic_SD_Remaining_Defect_previous = generic_SR_Total_Remained_Defect - generic_SD_Detected_Defect_previous

        generic_SD_Total_Remained_Defect = generic_SD_Remaining_Defect_current + generic_SD_Remaining_Defect_previous

        # Generic Dev Attribute model - Implementation phase
        # prior probability of Dev quality in IM phase
        IM_DevH_prior = pm.Beta("IM_DevH_prior", alpha=0.47, beta=1.14)
        IM_DevM_prior = pm.Beta("IM_DevM_prior", alpha=1.70, beta=1.56)
        IM_DevL_prior = pm.Beta("IM_DevL_prior", alpha=2.82, beta=15.00)
        # Attribute Source Code and Source Code Documentation Generation
        generic_IM_SCaSCDG_DevH_like = pm.TruncatedNormal("generic_IM_SCaSCDG_DevH_like",
                                                mu=IM_SCaSCDG_DevH_npt[generic_attr_states["IM_SCaSCDG_state"]][0], sigma=IM_SCaSCDG_DevH_npt[generic_attr_states["IM_SCaSCDG_state"]][1],
                                                lower=0, upper=1)
        generic_IM_SCaSCDG_DevM_like = pm.TruncatedNormal("generic_IM_SCaSCDG_DevM_like",
                                                mu=IM_SCaSCDG_DevM_npt[generic_attr_states["IM_SCaSCDG_state"]][0], sigma=IM_SCaSCDG_DevM_npt[generic_attr_states["IM_SCaSCDG_state"]][1],
                                                lower=0, upper=1)
        generic_IM_SCaSCDG_DevL_like = pm.TruncatedNormal("generic_IM_SCaSCDG_DevL_like",
                                                mu=IM_SCaSCDG_DevL_npt[generic_attr_states["IM_SCaSCDG_state"]][0], sigma=IM_SCaSCDG_DevL_npt[generic_attr_states["IM_SCaSCDG_state"]][1],
                                                lower=0, upper=1)
        # Attribute Traceability Analysis
        generic_IM_TA_DevH_like = pm.TruncatedNormal("generic_IM_TA_DevH_like",
                                            mu=IM_TA_DevH_npt[generic_attr_states["IM_TA_state"]][0], sigma=IM_TA_DevH_npt[generic_attr_states["IM_TA_state"]][1],
                                            lower=0, upper=1)
        generic_IM_TA_DevM_like = pm.TruncatedNormal("generic_IM_TA_DevM_like",
                                            mu=IM_TA_DevM_npt[generic_attr_states["IM_TA_state"]][0], sigma=IM_TA_DevM_npt[generic_attr_states["IM_TA_state"]][1],
                                            lower=0, upper=1)
        generic_IM_TA_DevL_like = pm.TruncatedNormal("generic_IM_TA_DevL_like",
                                            mu=IM_TA_DevL_npt[generic_attr_states["IM_TA_state"]][0], sigma=IM_TA_DevL_npt[generic_attr_states["IM_TA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Criticality Analysis
        generic_IM_CA_DevH_like = pm.TruncatedNormal("generic_IM_CA_DevH_like",
                                            mu=IM_CA_DevH_npt[generic_attr_states["IM_CA_state"]][0], sigma=IM_CA_DevH_npt[generic_attr_states["IM_CA_state"]][1],
                                            lower=0, upper=1)
        generic_IM_CA_DevM_like = pm.TruncatedNormal("generic_IM_CA_DevM_like",
                                            mu=IM_CA_DevM_npt[generic_attr_states["IM_CA_state"]][0], sigma=IM_CA_DevM_npt[generic_attr_states["IM_CA_state"]][1],
                                            lower=0, upper=1)
        generic_IM_CA_DevL_like = pm.TruncatedNormal("generic_IM_CA_DevL_like",
                                            mu=IM_CA_DevL_npt[generic_attr_states["IM_CA_state"]][0], sigma=IM_CA_DevL_npt[generic_attr_states["IM_CA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Hazard Analysis
        generic_IM_HA_DevH_like = pm.TruncatedNormal("generic_IM_HA_DevH_like",
                                            mu=IM_HA_DevH_npt[generic_attr_states["IM_HA_state"]][0], sigma=IM_HA_DevH_npt[generic_attr_states["IM_HA_state"]][1],
                                            lower=0, upper=1)
        generic_IM_HA_DevM_like = pm.TruncatedNormal("generic_IM_HA_DevM_like",
                                            mu=IM_HA_DevM_npt[generic_attr_states["IM_HA_state"]][0], sigma=IM_HA_DevM_npt[generic_attr_states["IM_HA_state"]][1],
                                            lower=0, upper=1)
        generic_IM_HA_DevL_like = pm.TruncatedNormal("generic_IM_HA_DevL_like",
                                            mu=IM_HA_DevL_npt[generic_attr_states["IM_HA_state"]][0], sigma=IM_HA_DevL_npt[generic_attr_states["IM_HA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Security Analysis
        generic_IM_SA_DevH_like = pm.TruncatedNormal("generic_IM_SA_DevH_like",
                                            mu=IM_SA_DevH_npt[generic_attr_states["IM_SA_state"]][0], sigma=IM_SA_DevH_npt[generic_attr_states["IM_SA_state"]][1],
                                            lower=0, upper=1)
        generic_IM_SA_DevM_like = pm.TruncatedNormal("generic_IM_SA_DevM_like",
                                            mu=IM_SA_DevM_npt[generic_attr_states["IM_SA_state"]][0], sigma=IM_SA_DevM_npt[generic_attr_states["IM_SA_state"]][1],
                                            lower=0, upper=1)
        generic_IM_SA_DevL_like = pm.TruncatedNormal("generic_IM_SA_DevL_like",
                                            mu=IM_SA_DevL_npt[generic_attr_states["IM_SA_state"]][0], sigma=IM_SA_DevL_npt[generic_attr_states["IM_SA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Risk Analysis
        generic_IM_RA_DevH_like = pm.TruncatedNormal("generic_IM_RA_DevH_like",
                                            mu=IM_RA_DevH_npt[generic_attr_states["IM_RA_state"]][0], sigma=IM_RA_DevH_npt[generic_attr_states["IM_RA_state"]][1],
                                            lower=0, upper=1)
        generic_IM_RA_DevM_like = pm.TruncatedNormal("generic_IM_RA_DevM_like",
                                            mu=IM_RA_DevM_npt[generic_attr_states["IM_RA_state"]][0], sigma=IM_RA_DevM_npt[generic_attr_states["IM_RA_state"]][1],
                                            lower=0, upper=1)
        generic_IM_RA_DevL_like = pm.TruncatedNormal("generic_IM_RA_DevL_like",
                                            mu=IM_RA_DevL_npt[generic_attr_states["IM_RA_state"]][0], sigma=IM_RA_DevL_npt[generic_attr_states["IM_RA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Component Test Case Generation
        generic_IM_CTCG_DevH_like = pm.TruncatedNormal("generic_IM_CTCG_DevH_like",
                                            mu=IM_CTCG_DevH_npt[generic_attr_states["IM_CTCG_state"]][0], sigma=IM_CTCG_DevH_npt[generic_attr_states["IM_CTCG_state"]][1],
                                            lower=0, upper=1)
        generic_IM_CTCG_DevM_like = pm.TruncatedNormal("generic_IM_CTCG_DevM_like",
                                            mu=IM_CTCG_DevM_npt[generic_attr_states["IM_CTCG_state"]][0], sigma=IM_CTCG_DevM_npt[generic_attr_states["IM_CTCG_state"]][1],
                                            lower=0, upper=1)
        generic_IM_CTCG_DevL_like = pm.TruncatedNormal("generic_IM_CTCG_DevL_like",
                                            mu=IM_CTCG_DevL_npt[generic_attr_states["IM_CTCG_state"]][0], sigma=IM_CTCG_DevL_npt[generic_attr_states["IM_CTCG_state"]][1],
                                            lower=0, upper=1)
        # Attribute Software Integration Test Case Generation
        generic_IM_SITCG_DevH_like = pm.TruncatedNormal("generic_IM_SITCG_DevH_like",
                                                mu=IM_SITCG_DevH_npt[generic_attr_states["IM_SITCG_state"]][0], sigma=IM_SITCG_DevH_npt[generic_attr_states["IM_SITCG_state"]][1],
                                                lower=0, upper=1)
        generic_IM_SITCG_DevM_like = pm.TruncatedNormal("generic_IM_SITCG_DevM_like",
                                                mu=IM_SITCG_DevM_npt[generic_attr_states["IM_SITCG_state"]][0], sigma=IM_SITCG_DevM_npt[generic_attr_states["IM_SITCG_state"]][1],
                                                lower=0, upper=1)
        generic_IM_SITCG_DevL_like = pm.TruncatedNormal("generic_IM_SITCG_DevL_like",
                                                mu=IM_SITCG_DevL_npt[generic_attr_states["IM_SITCG_state"]][0], sigma=IM_SITCG_DevL_npt[generic_attr_states["IM_SITCG_state"]][1],
                                                lower=0, upper=1)
        # Attribute Software Quantification Test Case Generation
        generic_IM_SQTCG_DevH_like = pm.TruncatedNormal("generic_IM_SQTCG_DevH_like",
                                                mu=IM_SQTCG_DevH_npt[generic_attr_states["IM_SQTCG_state"]][0], sigma=IM_SQTCG_DevH_npt[generic_attr_states["IM_SQTCG_state"]][1],
                                                lower=0, upper=1)
        generic_IM_SQTCG_DevM_like = pm.TruncatedNormal("generic_IM_SQTCG_DevM_like",
                                                mu=IM_SQTCG_DevM_npt[generic_attr_states["IM_SQTCG_state"]][0], sigma=IM_SQTCG_DevM_npt[generic_attr_states["IM_SQTCG_state"]][1],
                                                lower=0, upper=1)
        generic_IM_SQTCG_DevL_like = pm.TruncatedNormal("generic_IM_SQTCG_DevL_like",
                                                mu=IM_SQTCG_DevL_npt[generic_attr_states["IM_SQTCG_state"]][0], sigma=IM_SQTCG_DevL_npt[generic_attr_states["IM_SQTCG_state"]][1],
                                                lower=0, upper=1)
        # Attribute Software Acceptance Test Case Generation
        generic_IM_SATCG_DevH_like = pm.TruncatedNormal("generic_IM_SATCG_DevH_like",
                                                mu=IM_SATCG_DevH_npt[generic_attr_states["IM_SATCG_state"]][0], sigma=IM_SATCG_DevH_npt[generic_attr_states["IM_SATCG_state"]][1],
                                                lower=0, upper=1)
        generic_IM_SATCG_DevM_like = pm.TruncatedNormal("generic_IM_SATCG_DevM_like",
                                                mu=IM_SATCG_DevM_npt[generic_attr_states["IM_SATCG_state"]][0], sigma=IM_SATCG_DevM_npt[generic_attr_states["IM_SATCG_state"]][1],
                                                lower=0, upper=1)
        generic_IM_SATCG_DevL_like = pm.TruncatedNormal("generic_IM_SATCG_DevL_like",
                                                mu=IM_SATCG_DevL_npt[generic_attr_states["IM_SATCG_state"]][0], sigma=IM_SATCG_DevL_npt[generic_attr_states["IM_SATCG_state"]][1],
                                                lower=0, upper=1)
        # Attribute Software Component Test Procedure Generation
        generic_IM_SCTPG_DevH_like = pm.TruncatedNormal("generic_IM_SCTPG_DevH_like",
                                                mu=IM_SCTPG_DevH_npt[generic_attr_states["IM_SCTPG_state"]][0], sigma=IM_SCTPG_DevH_npt[generic_attr_states["IM_SCTPG_state"]][1],
                                                lower=0, upper=1)
        generic_IM_SCTPG_DevM_like = pm.TruncatedNormal("generic_IM_SCTPG_DevM_like",
                                                mu=IM_SCTPG_DevM_npt[generic_attr_states["IM_SCTPG_state"]][0], sigma=IM_SCTPG_DevM_npt[generic_attr_states["IM_SCTPG_state"]][1],
                                                lower=0, upper=1)
        generic_IM_SCTPG_DevL_like = pm.TruncatedNormal("generic_IM_SCTPG_DevL_like",
                                                mu=IM_SCTPG_DevL_npt[generic_attr_states["IM_SCTPG_state"]][0], sigma=IM_SCTPG_DevL_npt[generic_attr_states["IM_SCTPG_state"]][1],
                                                lower=0, upper=1)
        # Attribute Software Integration Test Procedure Generation
        generic_IM_SITPG_DevH_like = pm.TruncatedNormal("generic_IM_SITPG_DevH_like",
                                                mu=IM_SITPG_DevH_npt[generic_attr_states["IM_SITPG_state"]][0], sigma=IM_SITPG_DevH_npt[generic_attr_states["IM_SITPG_state"]][1],
                                                lower=0, upper=1)
        generic_IM_SITPG_DevM_like = pm.TruncatedNormal("generic_IM_SITPG_DevM_like",
                                                mu=IM_SITPG_DevM_npt[generic_attr_states["IM_SITPG_state"]][0], sigma=IM_SITPG_DevM_npt[generic_attr_states["IM_SITPG_state"]][1],
                                                lower=0, upper=1)
        generic_IM_SITPG_DevL_like = pm.TruncatedNormal("generic_IM_SITPG_DevL_like",
                                                mu=IM_SITPG_DevL_npt[generic_attr_states["IM_SITPG_state"]][0], sigma=IM_SITPG_DevL_npt[generic_attr_states["IM_SITPG_state"]][1],
                                                lower=0, upper=1)
        # Attribute Software Quantification Test Procedure Generation
        generic_IM_SQTPG_DevH_like = pm.TruncatedNormal("generic_IM_SQTPG_DevH_like",
                                                mu=IM_SQTPG_DevH_npt[generic_attr_states["IM_SQTPG_state"]][0], sigma=IM_SQTPG_DevH_npt[generic_attr_states["IM_SQTPG_state"]][1],
                                                lower=0, upper=1)
        generic_IM_SQTPG_DevM_like = pm.TruncatedNormal("generic_IM_SQTPG_DevM_like",
                                                mu=IM_SQTPG_DevM_npt[generic_attr_states["IM_SQTPG_state"]][0], sigma=IM_SQTPG_DevM_npt[generic_attr_states["IM_SQTPG_state"]][1],
                                                lower=0, upper=1)
        generic_IM_SQTPG_DevL_like = pm.TruncatedNormal("generic_IM_SQTPG_DevL_like",
                                                mu=IM_SQTPG_DevL_npt[generic_attr_states["IM_SQTPG_state"]][0], sigma=IM_SQTPG_DevL_npt[generic_attr_states["IM_SQTPG_state"]][1],
                                                lower=0, upper=1)
        # Attribute Configuration Management
        generic_IM_CM_DevH_like = pm.TruncatedNormal("generic_IM_CM_DevH_like",
                                            mu=IM_CM_DevH_npt[generic_attr_states["IM_CM_state"]][0], sigma=IM_CM_DevH_npt[generic_attr_states["IM_CM_state"]][1],
                                            lower=0, upper=1)
        generic_IM_CM_DevM_like = pm.TruncatedNormal("generic_IM_CM_DevM_like",
                                            mu=IM_CM_DevM_npt[generic_attr_states["IM_CM_state"]][0], sigma=IM_CM_DevM_npt[generic_attr_states["IM_CM_state"]][1],
                                            lower=0, upper=1)
        generic_IM_CM_DevL_like = pm.TruncatedNormal("generic_IM_CM_DevL_like",
                                            mu=IM_CM_DevL_npt[generic_attr_states["IM_CM_state"]][0], sigma=IM_CM_DevL_npt[generic_attr_states["IM_CM_state"]][1],
                                            lower=0, upper=1)
        # Attribute Reviews and Audits
        generic_IM_RaA_DevH_like = pm.TruncatedNormal("generic_IM_RaA_DevH_like",
                                                mu=IM_RaA_DevH_npt[generic_attr_states["IM_RaA_state"]][0], sigma=IM_RaA_DevH_npt[generic_attr_states["IM_RaA_state"]][1],
                                                lower=0, upper=1)
        generic_IM_RaA_DevM_like = pm.TruncatedNormal("generic_IM_RaA_DevM_like",
                                                mu=IM_RaA_DevM_npt[generic_attr_states["IM_RaA_state"]][0], sigma=IM_RaA_DevM_npt[generic_attr_states["IM_RaA_state"]][1],
                                                lower=0, upper=1)
        generic_IM_RaA_DevL_like = pm.TruncatedNormal("generic_IM_RaA_DevL_like",
                                                mu=IM_RaA_DevL_npt[generic_attr_states["IM_RaA_state"]][0], sigma=IM_RaA_DevL_npt[generic_attr_states["IM_RaA_state"]][1],
                                                lower=0, upper=1)
        # Attribute Software Component Test Execution
        generic_IM_SCTE_DevH_like = pm.TruncatedNormal("generic_IM_SCTE_DevH_like",
                                                mu=IM_SCTE_DevH_npt[generic_attr_states["IM_SCTE_state"]][0], sigma=IM_SCTE_DevH_npt[generic_attr_states["IM_SCTE_state"]][1],
                                                lower=0, upper=1)
        generic_IM_SCTE_DevM_like = pm.TruncatedNormal("generic_IM_SCTE_DevM_like",
                                                mu=IM_SCTE_DevM_npt[generic_attr_states["IM_SCTE_state"]][0], sigma=IM_SCTE_DevM_npt[generic_attr_states["IM_SCTE_state"]][1],
                                                lower=0, upper=1)
        generic_IM_SCTE_DevL_like = pm.TruncatedNormal("generic_IM_SCTE_DevL_like",
                                                mu=IM_SCTE_DevL_npt[generic_attr_states["IM_SCTE_state"]][0], sigma=IM_SCTE_DevL_npt[generic_attr_states["IM_SCTE_state"]][1],
                                                lower=0, upper=1)
        # m1-m3: a part of marginal probability
        # m1 = P(Dev=H)P(attribute states|Dev=H)
        # m2 = P(Dev=M)P(attribute states|Dev=M)
        # m3 = P(Dev=L)P(attribute states|Dev=L)
        generic_IM_Dev_m1 = IM_DevH_prior * generic_IM_SCaSCDG_DevH_like * generic_IM_TA_DevH_like * generic_IM_CA_DevH_like * generic_IM_HA_DevH_like * generic_IM_SA_DevH_like * generic_IM_RA_DevH_like * generic_IM_CTCG_DevH_like * generic_IM_SITCG_DevH_like * generic_IM_SQTCG_DevH_like * generic_IM_SATCG_DevH_like * generic_IM_SCTPG_DevH_like * generic_IM_SITPG_DevH_like * generic_IM_SQTPG_DevH_like * generic_IM_CM_DevH_like * generic_IM_RaA_DevH_like * generic_IM_SCTE_DevH_like
        generic_IM_Dev_m2 = IM_DevM_prior * generic_IM_SCaSCDG_DevM_like * generic_IM_TA_DevM_like * generic_IM_CA_DevM_like * generic_IM_HA_DevM_like * generic_IM_SA_DevM_like * generic_IM_RA_DevM_like * generic_IM_CTCG_DevM_like * generic_IM_SITCG_DevM_like * generic_IM_SQTCG_DevM_like * generic_IM_SATCG_DevM_like * generic_IM_SCTPG_DevM_like * generic_IM_SITPG_DevM_like * generic_IM_SQTPG_DevM_like * generic_IM_CM_DevM_like * generic_IM_RaA_DevM_like * generic_IM_SCTE_DevM_like
        generic_IM_Dev_m3 = IM_DevL_prior * generic_IM_SCaSCDG_DevL_like * generic_IM_TA_DevL_like * generic_IM_CA_DevL_like * generic_IM_HA_DevL_like * generic_IM_SA_DevL_like * generic_IM_RA_DevL_like * generic_IM_CTCG_DevL_like * generic_IM_SITCG_DevL_like * generic_IM_SQTCG_DevL_like * generic_IM_SATCG_DevL_like * generic_IM_SCTPG_DevL_like * generic_IM_SITPG_DevL_like * generic_IM_SQTPG_DevL_like * generic_IM_CM_DevL_like * generic_IM_RaA_DevL_like * generic_IM_SCTE_DevL_like

        # k = 1 / marginal probability
        generic_IM_Dev_k = 1 / (generic_IM_Dev_m1 + generic_IM_Dev_m2 + generic_IM_Dev_m3)
        # posterior probability of Dev quality in IM phase
        generic_IM_DevH_post = generic_IM_Dev_k * generic_IM_Dev_m1
        generic_IM_DevM_post = generic_IM_Dev_k * generic_IM_Dev_m2
        generic_IM_DevL_post = generic_IM_Dev_k * generic_IM_Dev_m3

        # Generic V&V Attribute model - Implementation phase
        # prior probability of V&V quality in IM phase
        IM_VVH_prior = pm.Beta("IM_VVH_prior", alpha=0.49, beta=1.27)
        IM_VVM_prior = pm.Beta("IM_VVM_prior", alpha=2.12, beta=1.82)
        IM_VVL_prior = pm.Beta("IM_VVL_prior", alpha=1.90, beta=9.90)
        # Attribute Source Code and Source Code Documentation Evaluation
        generic_IM_SCaSCDE_VVH_like = pm.TruncatedNormal("generic_IM_SCaSCDE_VVH_like",
                                                mu=IM_SCaSCDE_VVH_npt[generic_attr_states["IM_SCaSCDE_state"]][0], sigma=IM_SCaSCDE_VVH_npt[generic_attr_states["IM_SCaSCDE_state"]][1],
                                                lower=0, upper=1)
        generic_IM_SCaSCDE_VVM_like = pm.TruncatedNormal("generic_IM_SCaSCDE_VVM_like",
                                                mu=IM_SCaSCDE_VVM_npt[generic_attr_states["IM_SCaSCDE_state"]][0], sigma=IM_SCaSCDE_VVM_npt[generic_attr_states["IM_SCaSCDE_state"]][1],
                                                lower=0, upper=1)
        generic_IM_SCaSCDE_VVL_like = pm.TruncatedNormal("generic_IM_SCaSCDE_VVL_like",
                                                mu=IM_SCaSCDE_VVL_npt[generic_attr_states["IM_SCaSCDE_state"]][0], sigma=IM_SCaSCDE_VVL_npt[generic_attr_states["IM_SCaSCDE_state"]][1],
                                                lower=0, upper=1)
        # Attribute Interface Analysis V&V
        generic_IM_IAVV_VVH_like = pm.TruncatedNormal("generic_IM_IAVV_VVH_like",
                                            mu=IM_IAVV_VVH_npt[generic_attr_states["IM_IAVV_state"]][0], sigma=IM_IAVV_VVH_npt[generic_attr_states["IM_IAVV_state"]][1],
                                            lower=0, upper=1)
        generic_IM_IAVV_VVM_like = pm.TruncatedNormal("generic_IM_IAVV_VVM_like",
                                            mu=IM_IAVV_VVM_npt[generic_attr_states["IM_IAVV_state"]][0], sigma=IM_IAVV_VVM_npt[generic_attr_states["IM_IAVV_state"]][1],
                                            lower=0, upper=1)
        generic_IM_IAVV_VVL_like = pm.TruncatedNormal("generic_IM_IAVV_VVL_like",
                                            mu=IM_IAVV_VVL_npt[generic_attr_states["IM_IAVV_state"]][0], sigma=IM_IAVV_VVL_npt[generic_attr_states["IM_IAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Traceability Analysis V&V
        generic_IM_TAVV_VVH_like = pm.TruncatedNormal("generic_IM_TAVV_VVH_like",
                                            mu=IM_TAVV_VVH_npt[generic_attr_states["IM_TAVV_state"]][0], sigma=IM_TAVV_VVH_npt[generic_attr_states["IM_TAVV_state"]][1],
                                            lower=0, upper=1)
        generic_IM_TAVV_VVM_like = pm.TruncatedNormal("generic_IM_TAVV_VVM_like",
                                            mu=IM_TAVV_VVM_npt[generic_attr_states["IM_TAVV_state"]][0], sigma=IM_TAVV_VVM_npt[generic_attr_states["IM_TAVV_state"]][1],
                                            lower=0, upper=1)
        generic_IM_TAVV_VVL_like = pm.TruncatedNormal("generic_IM_TAVV_VVL_like",
                                            mu=IM_TAVV_VVL_npt[generic_attr_states["IM_TAVV_state"]][0], sigma=IM_TAVV_VVL_npt[generic_attr_states["IM_TAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Criticality Analysis V&V
        generic_IM_CAVV_VVH_like = pm.TruncatedNormal("generic_IM_CAVV_VVH_like",
                                            mu=IM_CAVV_VVH_npt[generic_attr_states["IM_CAVV_state"]][0], sigma=IM_CAVV_VVH_npt[generic_attr_states["IM_CAVV_state"]][1],
                                            lower=0, upper=1)
        generic_IM_CAVV_VVM_like = pm.TruncatedNormal("generic_IM_CAVV_VVM_like",
                                            mu=IM_CAVV_VVM_npt[generic_attr_states["IM_CAVV_state"]][0], sigma=IM_CAVV_VVM_npt[generic_attr_states["IM_CAVV_state"]][1],
                                            lower=0, upper=1)
        generic_IM_CAVV_VVL_like = pm.TruncatedNormal("generic_IM_CAVV_VVL_like",
                                            mu=IM_CAVV_VVL_npt[generic_attr_states["IM_CAVV_state"]][0], sigma=IM_CAVV_VVL_npt[generic_attr_states["IM_CAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Hazard Analysis V&V
        generic_IM_HAVV_VVH_like = pm.TruncatedNormal("generic_IM_HAVV_VVH_like",
                                            mu=IM_HAVV_VVH_npt[generic_attr_states["IM_HAVV_state"]][0], sigma=IM_HAVV_VVH_npt[generic_attr_states["IM_HAVV_state"]][1],
                                            lower=0, upper=1)
        generic_IM_HAVV_VVM_like = pm.TruncatedNormal("generic_IM_HAVV_VVM_like",
                                            mu=IM_HAVV_VVM_npt[generic_attr_states["IM_HAVV_state"]][0], sigma=IM_HAVV_VVM_npt[generic_attr_states["IM_HAVV_state"]][1],
                                            lower=0, upper=1)
        generic_IM_HAVV_VVL_like = pm.TruncatedNormal("generic_IM_HAVV_VVL_like",
                                            mu=IM_HAVV_VVL_npt[generic_attr_states["IM_HAVV_state"]][0], sigma=IM_HAVV_VVL_npt[generic_attr_states["IM_HAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Security Analysis V&V
        generic_IM_SAVV_VVH_like = pm.TruncatedNormal("generic_IM_SAVV_VVH_like",
                                            mu=IM_SAVV_VVH_npt[generic_attr_states["IM_SAVV_state"]][0], sigma=IM_SAVV_VVH_npt[generic_attr_states["IM_SAVV_state"]][1],
                                            lower=0, upper=1)
        generic_IM_SAVV_VVM_like = pm.TruncatedNormal("generic_IM_SAVV_VVM_like",
                                            mu=IM_SAVV_VVM_npt[generic_attr_states["IM_SAVV_state"]][0], sigma=IM_SAVV_VVM_npt[generic_attr_states["IM_SAVV_state"]][1],
                                            lower=0, upper=1)
        generic_IM_SAVV_VVL_like = pm.TruncatedNormal("generic_IM_SAVV_VVL_like",
                                            mu=IM_SAVV_VVL_npt[generic_attr_states["IM_SAVV_state"]][0], sigma=IM_SAVV_VVL_npt[generic_attr_states["IM_SAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Risk Analysis V&V
        generic_IM_RAVV_VVH_like = pm.TruncatedNormal("generic_IM_RAVV_VVH_like",
                                            mu=IM_RAVV_VVH_npt[generic_attr_states["IM_RAVV_state"]][0], sigma=IM_RAVV_VVH_npt[generic_attr_states["IM_RAVV_state"]][1],
                                            lower=0, upper=1)
        generic_IM_RAVV_VVM_like = pm.TruncatedNormal("generic_IM_RAVV_VVM_like",
                                            mu=IM_RAVV_VVM_npt[generic_attr_states["IM_RAVV_state"]][0], sigma=IM_RAVV_VVM_npt[generic_attr_states["IM_RAVV_state"]][1],
                                            lower=0, upper=1)
        generic_IM_RAVV_VVL_like = pm.TruncatedNormal("generic_IM_RAVV_VVL_like",
                                            mu=IM_RAVV_VVL_npt[generic_attr_states["IM_RAVV_state"]][0], sigma=IM_RAVV_VVL_npt[generic_attr_states["IM_RAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute V&V Software Component Test Case Generation
        generic_IM_VVSCTCG_VVH_like = pm.TruncatedNormal("generic_IM_VVSCTCG_VVH_like",
                                                mu=IM_VVSCTCG_VVH_npt[generic_attr_states["IM_VVSCTCG_state"]][0], sigma=IM_VVSCTCG_VVH_npt[generic_attr_states["IM_VVSCTCG_state"]][1],
                                                lower=0, upper=1)
        generic_IM_VVSCTCG_VVM_like = pm.TruncatedNormal("generic_IM_VVSCTCG_VVM_like",
                                                mu=IM_VVSCTCG_VVM_npt[generic_attr_states["IM_VVSCTCG_state"]][0], sigma=IM_VVSCTCG_VVM_npt[generic_attr_states["IM_VVSCTCG_state"]][1],
                                                lower=0, upper=1)
        generic_IM_VVSCTCG_VVL_like = pm.TruncatedNormal("generic_IM_VVSCTCG_VVL_like",
                                                mu=IM_VVSCTCG_VVL_npt[generic_attr_states["IM_VVSCTCG_state"]][0], sigma=IM_VVSCTCG_VVL_npt[generic_attr_states["IM_VVSCTCG_state"]][1],
                                                lower=0, upper=1)
        # Attribute V&V Software Integration Test Case Generation
        generic_IM_VVSITCG_VVH_like = pm.TruncatedNormal("generic_IM_VVSITCG_VVH_like",
                                                mu=IM_VVSITCG_VVH_npt[generic_attr_states["IM_VVSITCG_state"]][0], sigma=IM_VVSITCG_VVH_npt[generic_attr_states["IM_VVSITCG_state"]][1],
                                                lower=0, upper=1)
        generic_IM_VVSITCG_VVM_like = pm.TruncatedNormal("generic_IM_VVSITCG_VVM_like",
                                                mu=IM_VVSITCG_VVM_npt[generic_attr_states["IM_VVSITCG_state"]][0], sigma=IM_VVSITCG_VVM_npt[generic_attr_states["IM_VVSITCG_state"]][1],
                                                lower=0, upper=1)
        generic_IM_VVSITCG_VVL_like = pm.TruncatedNormal("generic_IM_VVSITCG_VVL_like",
                                                mu=IM_VVSITCG_VVL_npt[generic_attr_states["IM_VVSITCG_state"]][0], sigma=IM_VVSITCG_VVL_npt[generic_attr_states["IM_VVSITCG_state"]][1],
                                                lower=0, upper=1)
        # Attribute V&V Software Quantification Test Case Generation
        generic_IM_VVSQTCG_VVH_like = pm.TruncatedNormal("generic_IM_VVSQTCG_VVH_like",
                                                mu=IM_VVSQTCG_VVH_npt[generic_attr_states["IM_VVSQTCG_state"]][0], sigma=IM_VVSQTCG_VVH_npt[generic_attr_states["IM_VVSQTCG_state"]][1],
                                                lower=0, upper=1)
        generic_IM_VVSQTCG_VVM_like = pm.TruncatedNormal("generic_IM_VVSQTCG_VVM_like",
                                                mu=IM_VVSQTCG_VVM_npt[generic_attr_states["IM_VVSQTCG_state"]][0], sigma=IM_VVSQTCG_VVM_npt[generic_attr_states["IM_VVSQTCG_state"]][1],
                                                lower=0, upper=1)
        generic_IM_VVSQTCG_VVL_like = pm.TruncatedNormal("generic_IM_VVSQTCG_VVL_like",
                                                mu=IM_VVSQTCG_VVL_npt[generic_attr_states["IM_VVSQTCG_state"]][0], sigma=IM_VVSQTCG_VVL_npt[generic_attr_states["IM_VVSQTCG_state"]][1],
                                                lower=0, upper=1)
        # Attribute V&V Software Acceptance Test Case Generation
        generic_IM_VVSATCG_VVH_like = pm.TruncatedNormal("generic_IM_VVSATCG_VVH_like",
                                                mu=IM_VVSATCG_VVH_npt[generic_attr_states["IM_VVSATCG_state"]][0], sigma=IM_VVSATCG_VVH_npt[generic_attr_states["IM_VVSATCG_state"]][1],
                                                lower=0, upper=1)
        generic_IM_VVSATCG_VVM_like = pm.TruncatedNormal("generic_IM_VVSATCG_VVM_like",
                                                mu=IM_VVSATCG_VVM_npt[generic_attr_states["IM_VVSATCG_state"]][0], sigma=IM_VVSATCG_VVM_npt[generic_attr_states["IM_VVSATCG_state"]][1],
                                                lower=0, upper=1)
        generic_IM_VVSATCG_VVL_like = pm.TruncatedNormal("generic_IM_VVSATCG_VVL_like",
                                                mu=IM_VVSATCG_VVL_npt[generic_attr_states["IM_VVSATCG_state"]][0], sigma=IM_VVSATCG_VVL_npt[generic_attr_states["IM_VVSATCG_state"]][1],
                                                lower=0, upper=1)
        # Attribute V&V Software Component Test Procedure Generation
        generic_IM_VVSCTPG_VVH_like = pm.TruncatedNormal("generic_IM_VVSCTPG_VVH_like",
                                                mu=IM_VVSCTPG_VVH_npt[generic_attr_states["IM_VVSCTPG_state"]][0], sigma=IM_VVSCTPG_VVH_npt[generic_attr_states["IM_VVSCTPG_state"]][1],
                                                lower=0, upper=1)
        generic_IM_VVSCTPG_VVM_like = pm.TruncatedNormal("generic_IM_VVSCTPG_VVM_like",
                                                mu=IM_VVSCTPG_VVM_npt[generic_attr_states["IM_VVSCTPG_state"]][0], sigma=IM_VVSCTPG_VVM_npt[generic_attr_states["IM_VVSCTPG_state"]][1],
                                                lower=0, upper=1)
        generic_IM_VVSCTPG_VVL_like = pm.TruncatedNormal("generic_IM_VVSCTPG_VVL_like",
                                                mu=IM_VVSCTPG_VVL_npt[generic_attr_states["IM_VVSCTPG_state"]][0], sigma=IM_VVSCTPG_VVL_npt[generic_attr_states["IM_VVSCTPG_state"]][1],
                                                lower=0, upper=1)
        # Attribute V&V Software Integration Test Procedure Generation
        generic_IM_VVSITPG_VVH_like = pm.TruncatedNormal("generic_IM_VVSITPG_VVH_like",
                                                mu=IM_VVSITPG_VVH_npt[generic_attr_states["IM_VVSITPG_state"]][0], sigma=IM_VVSITPG_VVH_npt[generic_attr_states["IM_VVSITPG_state"]][1],
                                                lower=0, upper=1)
        generic_IM_VVSITPG_VVM_like = pm.TruncatedNormal("generic_IM_VVSITPG_VVM_like",
                                                mu=IM_VVSITPG_VVM_npt[generic_attr_states["IM_VVSITPG_state"]][0], sigma=IM_VVSITPG_VVM_npt[generic_attr_states["IM_VVSITPG_state"]][1],
                                                lower=0, upper=1)
        generic_IM_VVSITPG_VVL_like = pm.TruncatedNormal("generic_IM_VVSITPG_VVL_like",
                                                mu=IM_VVSITPG_VVL_npt[generic_attr_states["IM_VVSITPG_state"]][0], sigma=IM_VVSITPG_VVL_npt[generic_attr_states["IM_VVSITPG_state"]][1],
                                                lower=0, upper=1)
        # Attribute V&V Software Quantification Test Procedure Generation
        generic_IM_VVSQTPG_VVH_like = pm.TruncatedNormal("generic_IM_VVSQTPG_VVH_like",
                                                mu=IM_VVSQTPG_VVH_npt[generic_attr_states["IM_VVSQTPG_state"]][0], sigma=IM_VVSQTPG_VVH_npt[generic_attr_states["IM_VVSQTPG_state"]][1],
                                                lower=0, upper=1)
        generic_IM_VVSQTPG_VVM_like = pm.TruncatedNormal("generic_IM_VVSQTPG_VVM_like",
                                                mu=IM_VVSQTPG_VVM_npt[generic_attr_states["IM_VVSQTPG_state"]][0], sigma=IM_VVSQTPG_VVM_npt[generic_attr_states["IM_VVSQTPG_state"]][1],
                                                lower=0, upper=1)
        generic_IM_VVSQTPG_VVL_like = pm.TruncatedNormal("generic_IM_VVSQTPG_VVL_like",
                                                mu=IM_VVSQTPG_VVL_npt[generic_attr_states["IM_VVSQTPG_state"]][0], sigma=IM_VVSQTPG_VVL_npt[generic_attr_states["IM_VVSQTPG_state"]][1],
                                                lower=0, upper=1)
        # Attribute V&V Software Component Test Execution
        generic_IM_VVSCTE_VVH_like = pm.TruncatedNormal("generic_IM_VVSCTE_VVH_like",
                                                mu=IM_VVSCTE_VVH_npt[generic_attr_states["IM_VVSCTE_state"]][0], sigma=IM_VVSCTE_VVH_npt[generic_attr_states["IM_VVSCTE_state"]][1],
                                                lower=0, upper=1)
        generic_IM_VVSCTE_VVM_like = pm.TruncatedNormal("generic_IM_VVSCTE_VVM_like",
                                                mu=IM_VVSCTE_VVM_npt[generic_attr_states["IM_VVSCTE_state"]][0], sigma=IM_VVSCTE_VVM_npt[generic_attr_states["IM_VVSCTE_state"]][1],
                                                lower=0, upper=1)
        generic_IM_VVSCTE_VVL_like = pm.TruncatedNormal("generic_IM_VVSCTE_VVL_like",
                                                mu=IM_VVSCTE_VVL_npt[generic_attr_states["IM_VVSCTE_state"]][0], sigma=IM_VVSCTE_VVL_npt[generic_attr_states["IM_VVSCTE_state"]][1],
                                                lower=0, upper=1)
        # Attribute Configuration Management V&V
        generic_IM_CMVV_VVH_like = pm.TruncatedNormal("generic_IM_CMVV_VVH_like",
                                            mu=IM_CMVV_VVH_npt[generic_attr_states["IM_CMVV_state"]][0], sigma=IM_CMVV_VVH_npt[generic_attr_states["IM_CMVV_state"]][1],
                                            lower=0, upper=1)
        generic_IM_CMVV_VVM_like = pm.TruncatedNormal("generic_IM_CMVV_VVM_like",
                                            mu=IM_CMVV_VVM_npt[generic_attr_states["IM_CMVV_state"]][0], sigma=IM_CMVV_VVM_npt[generic_attr_states["IM_CMVV_state"]][1],
                                            lower=0, upper=1)
        generic_IM_CMVV_VVL_like = pm.TruncatedNormal("generic_IM_CMVV_VVL_like",
                                            mu=IM_CMVV_VVL_npt[generic_attr_states["IM_CMVV_state"]][0], sigma=IM_CMVV_VVL_npt[generic_attr_states["IM_CMVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Reviews and Audits V&V
        generic_IM_RaAVV_VVH_like = pm.TruncatedNormal("generic_IM_RaAVV_VVH_like",
                                            mu=IM_RaAVV_VVH_npt[generic_attr_states["IM_RaAVV_state"]][0], sigma=IM_RaAVV_VVH_npt[generic_attr_states["IM_RaAVV_state"]][1],
                                            lower=0, upper=1)
        generic_IM_RaAVV_VVM_like = pm.TruncatedNormal("generic_IM_RaAVV_VVM_like",
                                            mu=IM_RaAVV_VVM_npt[generic_attr_states["IM_RaAVV_state"]][0], sigma=IM_RaAVV_VVM_npt[generic_attr_states["IM_RaAVV_state"]][1],
                                            lower=0, upper=1)
        generic_IM_RaAVV_VVL_like = pm.TruncatedNormal("generic_IM_RaAVV_VVL_like",
                                            mu=IM_RaAVV_VVL_npt[generic_attr_states["IM_RaAVV_state"]][0], sigma=IM_RaAVV_VVL_npt[generic_attr_states["IM_RaAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute V&V Implementation Phase Activity Summary Report Generation
        generic_IM_VVASRG_VVH_like = pm.TruncatedNormal("generic_IM_VVASRG_VVH_like",
                                                mu=IM_VVASRG_VVH_npt[generic_attr_states["IM_VVASRG_state"]][0], sigma=IM_VVASRG_VVH_npt[generic_attr_states["IM_VVASRG_state"]][1],
                                                lower=0, upper=1)
        generic_IM_VVASRG_VVM_like = pm.TruncatedNormal("generic_IM_VVASRG_VVM_like",
                                                mu=IM_VVASRG_VVM_npt[generic_attr_states["IM_VVASRG_state"]][0], sigma=IM_VVASRG_VVM_npt[generic_attr_states["IM_VVASRG_state"]][1],
                                                lower=0, upper=1)
        generic_IM_VVASRG_VVL_like = pm.TruncatedNormal("generic_IM_VVASRG_VVL_like",
                                                mu=IM_VVASRG_VVL_npt[generic_attr_states["IM_VVASRG_state"]][0], sigma=IM_VVASRG_VVL_npt[generic_attr_states["IM_VVASRG_state"]][1],
                                                lower=0, upper=1)
        # m1-m3: a part of marginal probability
        # m1 = P(VV=H)P(attribute states|VV=H)
        # m2 = P(VV=M)P(attribute states|VV=M)
        # m3 = P(VV=L)P(attribute states|VV=L)
        generic_IM_VV_m1 = IM_VVH_prior * generic_IM_SCaSCDE_VVH_like * generic_IM_IAVV_VVH_like * generic_IM_TAVV_VVH_like * generic_IM_CAVV_VVH_like * generic_IM_HAVV_VVH_like * generic_IM_SAVV_VVH_like * generic_IM_RAVV_VVH_like * generic_IM_VVSCTCG_VVH_like * generic_IM_VVSITCG_VVH_like * generic_IM_VVSQTCG_VVH_like * generic_IM_VVSATCG_VVH_like * generic_IM_VVSCTPG_VVH_like * generic_IM_VVSITPG_VVH_like * generic_IM_VVSQTPG_VVH_like * generic_IM_VVSCTE_VVH_like * generic_IM_CMVV_VVH_like * generic_IM_RaAVV_VVH_like * generic_IM_VVASRG_VVH_like
        generic_IM_VV_m2 = IM_VVM_prior * generic_IM_SCaSCDE_VVM_like * generic_IM_IAVV_VVM_like * generic_IM_TAVV_VVM_like * generic_IM_CAVV_VVM_like * generic_IM_HAVV_VVM_like * generic_IM_SAVV_VVM_like * generic_IM_RAVV_VVM_like * generic_IM_VVSCTCG_VVM_like * generic_IM_VVSITCG_VVM_like * generic_IM_VVSQTCG_VVM_like * generic_IM_VVSATCG_VVM_like * generic_IM_VVSCTPG_VVM_like * generic_IM_VVSITPG_VVM_like * generic_IM_VVSQTPG_VVM_like * generic_IM_VVSCTE_VVM_like * generic_IM_CMVV_VVM_like * generic_IM_RaAVV_VVM_like * generic_IM_VVASRG_VVM_like
        generic_IM_VV_m3 = IM_VVL_prior * generic_IM_SCaSCDE_VVL_like * generic_IM_IAVV_VVL_like * generic_IM_TAVV_VVL_like * generic_IM_CAVV_VVL_like * generic_IM_HAVV_VVL_like * generic_IM_SAVV_VVL_like * generic_IM_RAVV_VVL_like * generic_IM_VVSCTCG_VVL_like * generic_IM_VVSITCG_VVL_like * generic_IM_VVSQTCG_VVL_like * generic_IM_VVSATCG_VVL_like * generic_IM_VVSCTPG_VVL_like * generic_IM_VVSITPG_VVL_like * generic_IM_VVSQTPG_VVL_like * generic_IM_VVSCTE_VVL_like * generic_IM_CMVV_VVL_like * generic_IM_RaAVV_VVL_like * generic_IM_VVASRG_VVL_like

        # k = 1 / marginal probability
        generic_IM_VV_k = 1 / (generic_IM_VV_m1 + generic_IM_VV_m2 + generic_IM_VV_m3)

        # posterior probability of Dev quality in IM phase
        generic_IM_VVH_post = generic_IM_VV_k * generic_IM_VV_m1
        generic_IM_VVM_post = generic_IM_VV_k * generic_IM_VV_m2
        generic_IM_VVL_post = generic_IM_VV_k * generic_IM_VV_m3

        # Generic Submodel - Implementation phase

        # Defect Density likelihood: P(Defect Density|state of Dev quality)
        IM_DevH_DD_like = pm.Gamma("IM_DevH_DD_like", alpha=2.5989, beta=3.3317)
        IM_DevM_DD_like = pm.Gamma("IM_DevM_DD_like", alpha=3.1588, beta=3.1963)
        IM_DevL_DD_like = pm.Gamma("IM_DevL_DD_like", alpha=3.3807, beta=3.1969)

        # Defect density: the integral of P(Dev)*P(Defect Density|Dev) dDev
        generic_IM_Defect_Density = (generic_IM_DevH_post * IM_DevH_DD_like + generic_IM_DevM_post * IM_DevM_DD_like + generic_IM_DevL_post * IM_DevL_DD_like)

        generic_IM_Defect_introduced_in_current = generic_function_point * generic_IM_Defect_Density

        # Defect Detection Probability (current) likelihood: P(DDP_current|state of VV quality)
        generic_IM_VVH_DDP_current_like = pm.Beta("generic_IM_VVH_DDP_current_like", alpha=IM_VVH_DDP_current_npt[generic_complexity][0], beta=IM_VVH_DDP_current_npt[generic_complexity][1])
        generic_IM_VVM_DDP_current_like = pm.Beta("generic_IM_VVM_DDP_current_like", alpha=IM_VVM_DDP_current_npt[generic_complexity][0], beta=IM_VVM_DDP_current_npt[generic_complexity][1])
        generic_IM_VVL_DDP_current_like = pm.Beta("generic_IM_VVL_DDP_current_like", alpha=IM_VVL_DDP_current_npt[generic_complexity][0], beta=IM_VVL_DDP_current_npt[generic_complexity][1])

        # Defect Detection Probability (current): the integral of P(DDP_current|VV) dVV
        generic_IM_Defect_Detection_Probability_current = generic_IM_VVH_post * generic_IM_VVH_DDP_current_like + generic_IM_VVM_post * generic_IM_VVM_DDP_current_like + generic_IM_VVL_post * generic_IM_VVL_DDP_current_like

        generic_IM_Detected_Defect_current = generic_IM_Defect_introduced_in_current * generic_IM_Defect_Detection_Probability_current

        generic_IM_Remaining_Defect_current = generic_IM_Defect_introduced_in_current - generic_IM_Detected_Defect_current

        # Defect Detection Probability (previous) likelihood: P(DDP_previous|state of VV quality)
        generic_IM_VVH_DDP_previous_like = pm.Beta("generic_IM_VVH_DDP_previous_like", alpha=IM_VVH_DDP_previous_npt[generic_complexity][0], beta=IM_VVH_DDP_previous_npt[generic_complexity][1])
        generic_IM_VVM_DDP_previous_like = pm.Beta("generic_IM_VVM_DDP_previous_like", alpha=IM_VVM_DDP_previous_npt[generic_complexity][0], beta=IM_VVM_DDP_previous_npt[generic_complexity][1])
        generic_IM_VVL_DDP_previous_like = pm.Beta("generic_IM_VVL_DDP_previous_like", alpha=IM_VVL_DDP_previous_npt[generic_complexity][0], beta=IM_VVL_DDP_previous_npt[generic_complexity][1])

        # Defect Detection Probability (previous): the integral of P(DDP_previous|VV) dVV
        generic_IM_Defect_Detection_Probability_previous = generic_IM_VVH_post * generic_IM_VVH_DDP_previous_like + generic_IM_VVM_post * generic_IM_VVM_DDP_previous_like + generic_IM_VVL_post * generic_IM_VVL_DDP_previous_like

        generic_IM_Detected_Defect_previous = generic_SD_Total_Remained_Defect * generic_IM_Defect_Detection_Probability_previous

        generic_IM_Remaining_Defect_previous = generic_SD_Total_Remained_Defect - generic_IM_Detected_Defect_previous

        generic_IM_Total_Remained_Defect = generic_IM_Remaining_Defect_current + generic_IM_Remaining_Defect_previous

        # Generic Dev Attribute model - Test phase
        # prior probability of Dev quality in ST phase
        ST_DevH_prior = pm.Beta("ST_DevH_prior", alpha=0.45, beta=1.29)
        ST_DevM_prior = pm.Beta("ST_DevM_prior", alpha=1.75, beta=1.19)
        ST_DevL_prior = pm.Beta("ST_DevL_prior", alpha=0.83, beta=5.42)
        # Attribute Software Integration Test Execution
        generic_ST_SITE_DevH_like = pm.TruncatedNormal("generic_ST_SITE_DevH_like",
                                            mu=ST_SITE_DevH_npt[generic_attr_states["ST_SITE_state"]][0], sigma=ST_SITE_DevH_npt[generic_attr_states["ST_SITE_state"]][1],
                                            lower=0, upper=1)
        generic_ST_SITE_DevM_like = pm.TruncatedNormal("generic_ST_SITE_DevM_like",
                                            mu=ST_SITE_DevM_npt[generic_attr_states["ST_SITE_state"]][0], sigma=ST_SITE_DevM_npt[generic_attr_states["ST_SITE_state"]][1],
                                            lower=0, upper=1)
        generic_ST_SITE_DevL_like = pm.TruncatedNormal("generic_ST_SITE_DevL_like",
                                            mu=ST_SITE_DevL_npt[generic_attr_states["ST_SITE_state"]][0], sigma=ST_SITE_DevL_npt[generic_attr_states["ST_SITE_state"]][1],
                                            lower=0, upper=1)
        # Attribute Software Qualification Test Execution
        generic_ST_SQTE_DevH_like = pm.TruncatedNormal("generic_ST_SQTE_DevH_like",
                                            mu=ST_SQTE_DevH_npt[generic_attr_states["ST_SQTE_state"]][0], sigma=ST_SQTE_DevH_npt[generic_attr_states["ST_SQTE_state"]][1],
                                            lower=0, upper=1)
        generic_ST_SQTE_DevM_like = pm.TruncatedNormal("generic_ST_SQTE_DevM_like",
                                            mu=ST_SQTE_DevM_npt[generic_attr_states["ST_SQTE_state"]][0], sigma=ST_SQTE_DevM_npt[generic_attr_states["ST_SQTE_state"]][1],
                                            lower=0, upper=1)
        generic_ST_SQTE_DevL_like = pm.TruncatedNormal("generic_ST_SQTE_DevL_like",
                                            mu=ST_SQTE_DevL_npt[generic_attr_states["ST_SQTE_state"]][0], sigma=ST_SQTE_DevL_npt[generic_attr_states["ST_SQTE_state"]][1],
                                            lower=0, upper=1)
        # Attribute Software Acceptance Procedure Generation
        generic_ST_SAPG_DevH_like = pm.TruncatedNormal("generic_ST_SAPG_DevH_like",
                                            mu=ST_SAPG_DevH_npt[generic_attr_states["ST_SAPG_state"]][0], sigma=ST_SAPG_DevH_npt[generic_attr_states["ST_SAPG_state"]][1],
                                            lower=0, upper=1)
        generic_ST_SAPG_DevM_like = pm.TruncatedNormal("generic_ST_SAPG_DevM_like",
                                            mu=ST_SAPG_DevM_npt[generic_attr_states["ST_SAPG_state"]][0], sigma=ST_SAPG_DevM_npt[generic_attr_states["ST_SAPG_state"]][1],
                                            lower=0, upper=1)
        generic_ST_SAPG_DevL_like = pm.TruncatedNormal("generic_ST_SAPG_DevL_like",
                                            mu=ST_SAPG_DevL_npt[generic_attr_states["ST_SAPG_state"]][0], sigma=ST_SAPG_DevL_npt[generic_attr_states["ST_SAPG_state"]][1],
                                            lower=0, upper=1)
        # Attribute Software Acceptance Test Execution
        generic_ST_SATE_DevH_like = pm.TruncatedNormal("generic_ST_SATE_DevH_like",
                                            mu=ST_SATE_DevH_npt[generic_attr_states["ST_SATE_state"]][0], sigma=ST_SATE_DevH_npt[generic_attr_states["ST_SATE_state"]][1],
                                            lower=0, upper=1)
        generic_ST_SATE_DevM_like = pm.TruncatedNormal("generic_ST_SATE_DevM_like",
                                            mu=ST_SATE_DevM_npt[generic_attr_states["ST_SATE_state"]][0], sigma=ST_SATE_DevM_npt[generic_attr_states["ST_SATE_state"]][1],
                                            lower=0, upper=1)
        generic_ST_SATE_DevL_like = pm.TruncatedNormal("generic_ST_SATE_DevL_like",
                                            mu=ST_SATE_DevL_npt[generic_attr_states["ST_SATE_state"]][0], sigma=ST_SATE_DevL_npt[generic_attr_states["ST_SATE_state"]][1],
                                            lower=0, upper=1)
        # Attribute Traceability Analysis - Test Phase
        generic_ST_TA_DevH_like = pm.TruncatedNormal("generic_ST_TA_DevH_like",
                                            mu=ST_TA_DevH_npt[generic_attr_states["ST_TA_state"]][0], sigma=ST_TA_DevH_npt[generic_attr_states["ST_TA_state"]][1],
                                            lower=0, upper=1)
        generic_ST_TA_DevM_like = pm.TruncatedNormal("generic_ST_TA_DevM_like",
                                            mu=ST_TA_DevM_npt[generic_attr_states["ST_TA_state"]][0], sigma=ST_TA_DevM_npt[generic_attr_states["ST_TA_state"]][1],
                                            lower=0, upper=1)
        generic_ST_TA_DevL_like = pm.TruncatedNormal("generic_ST_TA_DevL_like",
                                            mu=ST_TA_DevL_npt[generic_attr_states["ST_TA_state"]][0], sigma=ST_TA_DevL_npt[generic_attr_states["ST_TA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Hazard Analysis - Test Phase
        generic_ST_HA_DevH_like = pm.TruncatedNormal("generic_ST_HA_DevH_like",
                                            mu=ST_HA_DevH_npt[generic_attr_states["ST_HA_state"]][0], sigma=ST_HA_DevH_npt[generic_attr_states["ST_HA_state"]][1],
                                            lower=0, upper=1)
        generic_ST_HA_DevM_like = pm.TruncatedNormal("generic_ST_HA_DevM_like",
                                            mu=ST_HA_DevM_npt[generic_attr_states["ST_HA_state"]][0], sigma=ST_HA_DevM_npt[generic_attr_states["ST_HA_state"]][1],
                                            lower=0, upper=1)
        generic_ST_HA_DevL_like = pm.TruncatedNormal("generic_ST_HA_DevL_like",
                                            mu=ST_HA_DevL_npt[generic_attr_states["ST_HA_state"]][0], sigma=ST_HA_DevL_npt[generic_attr_states["ST_HA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Security Analysis - Test Phase
        generic_ST_SA_DevH_like = pm.TruncatedNormal("generic_ST_SA_DevH_like",
                                            mu=ST_SA_DevH_npt[generic_attr_states["ST_SA_state"]][0], sigma=ST_SA_DevH_npt[generic_attr_states["ST_SA_state"]][1],
                                            lower=0, upper=1)
        generic_ST_SA_DevM_like = pm.TruncatedNormal("generic_ST_SA_DevM_like",
                                            mu=ST_SA_DevM_npt[generic_attr_states["ST_SA_state"]][0], sigma=ST_SA_DevM_npt[generic_attr_states["ST_SA_state"]][1],
                                            lower=0, upper=1)
        generic_ST_SA_DevL_like = pm.TruncatedNormal("generic_ST_SA_DevL_like",
                                            mu=ST_SA_DevL_npt[generic_attr_states["ST_SA_state"]][0], sigma=ST_SA_DevL_npt[generic_attr_states["ST_SA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Risk Analysis - Test Phase
        generic_ST_RA_DevH_like = pm.TruncatedNormal("generic_ST_RA_DevH_like",
                                            mu=ST_RA_DevH_npt[generic_attr_states["ST_RA_state"]][0], sigma=ST_RA_DevH_npt[generic_attr_states["ST_RA_state"]][1],
                                            lower=0, upper=1)
        generic_ST_RA_DevM_like = pm.TruncatedNormal("generic_ST_RA_DevM_like",
                                            mu=ST_RA_DevM_npt[generic_attr_states["ST_RA_state"]][0], sigma=ST_RA_DevM_npt[generic_attr_states["ST_RA_state"]][1],
                                            lower=0, upper=1)
        generic_ST_RA_DevL_like = pm.TruncatedNormal("generic_ST_RA_DevL_like",
                                            mu=ST_RA_DevL_npt[generic_attr_states["ST_RA_state"]][0], sigma=ST_RA_DevL_npt[generic_attr_states["ST_RA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Configuration Management
        generic_ST_CM_DevH_like = pm.TruncatedNormal("generic_ST_CM_DevH_like",
                                            mu=ST_CM_DevH_npt[generic_attr_states["ST_CM_state"]][0], sigma=ST_CM_DevH_npt[generic_attr_states["ST_CM_state"]][1],
                                            lower=0, upper=1)
        generic_ST_CM_DevM_like = pm.TruncatedNormal("generic_ST_CM_DevM_like",
                                            mu=ST_CM_DevM_npt[generic_attr_states["ST_CM_state"]][0], sigma=ST_CM_DevM_npt[generic_attr_states["ST_CM_state"]][1],
                                            lower=0, upper=1)
        generic_ST_CM_DevL_like = pm.TruncatedNormal("generic_ST_CM_DevL_like",
                                            mu=ST_CM_DevL_npt[generic_attr_states["ST_CM_state"]][0], sigma=ST_CM_DevL_npt[generic_attr_states["ST_CM_state"]][1],
                                            lower=0, upper=1)
        # Attribute Review and Audits
        generic_ST_RaA_DevH_like = pm.TruncatedNormal("generic_ST_RaA_DevH_like",
                                            mu=ST_RaA_DevH_npt[generic_attr_states["ST_RaA_state"]][0], sigma=ST_RaA_DevH_npt[generic_attr_states["ST_RaA_state"]][1],
                                            lower=0, upper=1)
        generic_ST_RaA_DevM_like = pm.TruncatedNormal("generic_ST_RaA_DevM_like",
                                            mu=ST_RaA_DevM_npt[generic_attr_states["ST_RaA_state"]][0], sigma=ST_RaA_DevM_npt[generic_attr_states["ST_RaA_state"]][1],
                                            lower=0, upper=1)
        generic_ST_RaA_DevL_like = pm.TruncatedNormal("generic_ST_RaA_DevL_like",
                                            mu=ST_RaA_DevL_npt[generic_attr_states["ST_RaA_state"]][0], sigma=ST_RaA_DevL_npt[generic_attr_states["ST_RaA_state"]][1],
                                            lower=0, upper=1)
        # m1-m3: a part of marginal probability
        # m1 = P(Dev=H)P(attribute states|Dev=H)
        # m2 = P(Dev=M)P(attribute states|Dev=M)
        # m3 = P(Dev=L)P(attribute states|Dev=L)
        generic_ST_Dev_m1 = ST_DevH_prior * generic_ST_SITE_DevH_like * generic_ST_SQTE_DevH_like * generic_ST_SAPG_DevH_like * generic_ST_SATE_DevH_like * generic_ST_TA_DevH_like * generic_ST_HA_DevH_like * generic_ST_SA_DevH_like * generic_ST_RA_DevH_like * generic_ST_CM_DevH_like * generic_ST_RaA_DevH_like
        generic_ST_Dev_m2 = ST_DevM_prior * generic_ST_SITE_DevM_like * generic_ST_SQTE_DevM_like * generic_ST_SAPG_DevM_like * generic_ST_SATE_DevM_like * generic_ST_TA_DevM_like * generic_ST_HA_DevM_like * generic_ST_SA_DevM_like * generic_ST_RA_DevM_like * generic_ST_CM_DevM_like * generic_ST_RaA_DevM_like
        generic_ST_Dev_m3 = ST_DevL_prior * generic_ST_SITE_DevL_like * generic_ST_SQTE_DevL_like * generic_ST_SAPG_DevL_like * generic_ST_SATE_DevL_like * generic_ST_TA_DevL_like * generic_ST_HA_DevL_like * generic_ST_SA_DevL_like * generic_ST_RA_DevL_like * generic_ST_CM_DevL_like * generic_ST_RaA_DevL_like

        # k = 1 / marginal probability
        generic_ST_Dev_k = 1 / (generic_ST_Dev_m1 + generic_ST_Dev_m2 + generic_ST_Dev_m3)
        # posterior probability of Dev quality in ST phase
        generic_ST_DevH_post = generic_ST_Dev_k * generic_ST_Dev_m1
        generic_ST_DevM_post = generic_ST_Dev_k * generic_ST_Dev_m2
        generic_ST_DevL_post = generic_ST_Dev_k * generic_ST_Dev_m3

        # Generic V&V Attribute model - Test phase
        # prior probability of V&V quality in ST phase
        ST_VVH_prior = pm.Beta("ST_VVH_prior", alpha=0.45, beta=1.29)
        ST_VVM_prior = pm.Beta("ST_VVM_prior", alpha=1.75, beta=1.19)
        ST_VVL_prior = pm.Beta("ST_VVL_prior", alpha=0.83, beta=5.42)
        # Attribute V&V Software Integration Test Execution
        generic_ST_VVSITE_VVH_like = pm.TruncatedNormal("generic_ST_VVSITE_VVH_like",
                                                mu=ST_VVSITE_VVH_npt[generic_attr_states["ST_VVSITE_state"]][0], sigma=ST_VVSITE_VVH_npt[generic_attr_states["ST_VVSITE_state"]][1],
                                                lower=0, upper=1)
        generic_ST_VVSITE_VVM_like = pm.TruncatedNormal("generic_ST_VVSITE_VVM_like",
                                                mu=ST_VVSITE_VVM_npt[generic_attr_states["ST_VVSITE_state"]][0], sigma=ST_VVSITE_VVM_npt[generic_attr_states["ST_VVSITE_state"]][1],
                                                lower=0, upper=1)
        generic_ST_VVSITE_VVL_like = pm.TruncatedNormal("generic_ST_VVSITE_VVL_like",
                                                mu=ST_VVSITE_VVL_npt[generic_attr_states["ST_VVSITE_state"]][0], sigma=ST_VVSITE_VVL_npt[generic_attr_states["ST_VVSITE_state"]][1],
                                                lower=0, upper=1)
        # Attribute V&V Software Qualification Test Execution
        generic_ST_VVSQTE_VVH_like = pm.TruncatedNormal("generic_ST_VVSQTE_VVH_like",
                                                mu=ST_VVSQTE_VVH_npt[generic_attr_states["ST_VVSQTE_state"]][0], sigma=ST_VVSQTE_VVH_npt[generic_attr_states["ST_VVSQTE_state"]][1],
                                                lower=0, upper=1)
        generic_ST_VVSQTE_VVM_like = pm.TruncatedNormal("generic_ST_VVSQTE_VVM_like",
                                                mu=ST_VVSQTE_VVM_npt[generic_attr_states["ST_VVSQTE_state"]][0], sigma=ST_VVSQTE_VVM_npt[generic_attr_states["ST_VVSQTE_state"]][1],
                                                lower=0, upper=1)
        generic_ST_VVSQTE_VVL_like = pm.TruncatedNormal("generic_ST_VVSQTE_VVL_like",
                                                mu=ST_VVSQTE_VVL_npt[generic_attr_states["ST_VVSQTE_state"]][0], sigma=ST_VVSQTE_VVL_npt[generic_attr_states["ST_VVSQTE_state"]][1],
                                                lower=0, upper=1)
        # Attribute V&V Software Acceptance Procedure Generation
        generic_ST_VVSAPG_VVH_like = pm.TruncatedNormal("generic_ST_VVSAPG_VVH_like",
                                                mu=ST_VVSAPG_VVH_npt[generic_attr_states["ST_VVSAPG_state"]][0], sigma=ST_VVSAPG_VVH_npt[generic_attr_states["ST_VVSAPG_state"]][1],
                                                lower=0, upper=1)
        generic_ST_VVSAPG_VVM_like = pm.TruncatedNormal("generic_ST_VVSAPG_VVM_like",
                                                mu=ST_VVSAPG_VVM_npt[generic_attr_states["ST_VVSAPG_state"]][0], sigma=ST_VVSAPG_VVM_npt[generic_attr_states["ST_VVSAPG_state"]][1],
                                                lower=0, upper=1)
        generic_ST_VVSAPG_VVL_like = pm.TruncatedNormal("generic_ST_VVSAPG_VVL_like",
                                                mu=ST_VVSAPG_VVL_npt[generic_attr_states["ST_VVSAPG_state"]][0], sigma=ST_VVSAPG_VVL_npt[generic_attr_states["ST_VVSAPG_state"]][1],
                                                lower=0, upper=1)
        # Attribute V&V Software Acceptance Test Execution
        generic_ST_VVSATE_VVH_like = pm.TruncatedNormal("generic_ST_VVSATE_VVH_like",
                                                mu=ST_VVSATE_VVH_npt[generic_attr_states["ST_VVSATE_state"]][0], sigma=ST_VVSATE_VVH_npt[generic_attr_states["ST_VVSATE_state"]][1],
                                                lower=0, upper=1)
        generic_ST_VVSATE_VVM_like = pm.TruncatedNormal("generic_ST_VVSATE_VVM_like",
                                                mu=ST_VVSATE_VVM_npt[generic_attr_states["ST_VVSATE_state"]][0], sigma=ST_VVSATE_VVM_npt[generic_attr_states["ST_VVSATE_state"]][1],
                                                lower=0, upper=1)
        generic_ST_VVSATE_VVL_like = pm.TruncatedNormal("generic_ST_VVSATE_VVL_like",
                                                mu=ST_VVSATE_VVL_npt[generic_attr_states["ST_VVSATE_state"]][0], sigma=ST_VVSATE_VVL_npt[generic_attr_states["ST_VVSATE_state"]][1],
                                                lower=0, upper=1)
        # Attribute Traceability Analysis V&V - Test phase
        generic_ST_TAVV_VVH_like = pm.TruncatedNormal("generic_ST_TAVV_VVH_like",
                                            mu=ST_TAVV_VVH_npt[generic_attr_states["ST_TAVV_state"]][0], sigma=ST_TAVV_VVH_npt[generic_attr_states["ST_TAVV_state"]][1],
                                            lower=0, upper=1)
        generic_ST_TAVV_VVM_like = pm.TruncatedNormal("generic_ST_TAVV_VVM_like",
                                            mu=ST_TAVV_VVM_npt[generic_attr_states["ST_TAVV_state"]][0], sigma=ST_TAVV_VVM_npt[generic_attr_states["ST_TAVV_state"]][1],
                                            lower=0, upper=1)
        generic_ST_TAVV_VVL_like = pm.TruncatedNormal("generic_ST_TAVV_VVL_like",
                                            mu=ST_TAVV_VVL_npt[generic_attr_states["ST_TAVV_state"]][0], sigma=ST_TAVV_VVL_npt[generic_attr_states["ST_TAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Hazard Analysis V&V - Test phase
        generic_ST_HAVV_VVH_like = pm.TruncatedNormal("generic_ST_HAVV_VVH_like",
                                            mu=ST_HAVV_VVH_npt[generic_attr_states["ST_HAVV_state"]][0], sigma=ST_HAVV_VVH_npt[generic_attr_states["ST_HAVV_state"]][1],
                                            lower=0, upper=1)
        generic_ST_HAVV_VVM_like = pm.TruncatedNormal("generic_ST_HAVV_VVM_like",
                                            mu=ST_HAVV_VVM_npt[generic_attr_states["ST_HAVV_state"]][0], sigma=ST_HAVV_VVM_npt[generic_attr_states["ST_HAVV_state"]][1],
                                            lower=0, upper=1)
        generic_ST_HAVV_VVL_like = pm.TruncatedNormal("generic_ST_HAVV_VVL_like",
                                            mu=ST_HAVV_VVL_npt[generic_attr_states["ST_HAVV_state"]][0], sigma=ST_HAVV_VVL_npt[generic_attr_states["ST_HAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Security Analysis V&V - Test phase
        generic_ST_SAVV_VVH_like = pm.TruncatedNormal("generic_ST_SAVV_VVH_like",
                                            mu=ST_SAVV_VVH_npt[generic_attr_states["ST_SAVV_state"]][0], sigma=ST_SAVV_VVH_npt[generic_attr_states["ST_SAVV_state"]][1],
                                            lower=0, upper=1)
        generic_ST_SAVV_VVM_like = pm.TruncatedNormal("generic_ST_SAVV_VVM_like",
                                            mu=ST_SAVV_VVM_npt[generic_attr_states["ST_SAVV_state"]][0], sigma=ST_SAVV_VVM_npt[generic_attr_states["ST_SAVV_state"]][1],
                                            lower=0, upper=1)
        generic_ST_SAVV_VVL_like = pm.TruncatedNormal("generic_ST_SAVV_VVL_like",
                                            mu=ST_SAVV_VVL_npt[generic_attr_states["ST_SAVV_state"]][0], sigma=ST_SAVV_VVL_npt[generic_attr_states["ST_SAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Risk Analysis V&V - Test phase
        generic_ST_RAVV_VVH_like = pm.TruncatedNormal("generic_ST_RAVV_VVH_like",
                                            mu=ST_RAVV_VVH_npt[generic_attr_states["ST_RAVV_state"]][0], sigma=ST_RAVV_VVH_npt[generic_attr_states["ST_RAVV_state"]][1],
                                            lower=0, upper=1)
        generic_ST_RAVV_VVM_like = pm.TruncatedNormal("generic_ST_RAVV_VVM_like",
                                            mu=ST_RAVV_VVM_npt[generic_attr_states["ST_RAVV_state"]][0], sigma=ST_RAVV_VVM_npt[generic_attr_states["ST_RAVV_state"]][1],
                                            lower=0, upper=1)
        generic_ST_RAVV_VVL_like = pm.TruncatedNormal("generic_ST_RAVV_VVL_like",
                                            mu=ST_RAVV_VVL_npt[generic_attr_states["ST_RAVV_state"]][0], sigma=ST_RAVV_VVL_npt[generic_attr_states["ST_RAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Configuration Management V&V - Test phase
        generic_ST_CMVV_VVH_like = pm.TruncatedNormal("generic_ST_CMVV_VVH_like",
                                            mu=ST_CMVV_VVH_npt[generic_attr_states["ST_CMVV_state"]][0], sigma=ST_CMVV_VVH_npt[generic_attr_states["ST_CMVV_state"]][1],
                                            lower=0, upper=1)
        generic_ST_CMVV_VVM_like = pm.TruncatedNormal("generic_ST_CMVV_VVM_like",
                                            mu=ST_CMVV_VVM_npt[generic_attr_states["ST_CMVV_state"]][0], sigma=ST_CMVV_VVM_npt[generic_attr_states["ST_CMVV_state"]][1],
                                            lower=0, upper=1)
        generic_ST_CMVV_VVL_like = pm.TruncatedNormal("generic_ST_CMVV_VVL_like",
                                            mu=ST_CMVV_VVL_npt[generic_attr_states["ST_CMVV_state"]][0], sigma=ST_CMVV_VVL_npt[generic_attr_states["ST_CMVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Review and Audit V&V - Test phase
        generic_ST_RaAVV_VVH_like = pm.TruncatedNormal("generic_ST_RaAVV_VVH_like",
                                            mu=ST_RaAVV_VVH_npt[generic_attr_states["ST_RaAVV_state"]][0], sigma=ST_RaAVV_VVH_npt[generic_attr_states["ST_RaAVV_state"]][1],
                                            lower=0, upper=1)
        generic_ST_RaAVV_VVM_like = pm.TruncatedNormal("generic_ST_RaAVV_VVM_like",
                                            mu=ST_RaAVV_VVM_npt[generic_attr_states["ST_RaAVV_state"]][0], sigma=ST_RaAVV_VVM_npt[generic_attr_states["ST_RaAVV_state"]][1],
                                            lower=0, upper=1)
        generic_ST_RaAVV_VVL_like = pm.TruncatedNormal("generic_ST_RaAVV_VVL_like",
                                            mu=ST_RaAVV_VVL_npt[generic_attr_states["ST_RaAVV_state"]][0], sigma=ST_RaAVV_VVL_npt[generic_attr_states["ST_RaAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute V&V Test phase Activity Summary Report Generation
        generic_ST_VVASRG_VVH_like = pm.TruncatedNormal("generic_ST_VVASRG_VVH_like",
                                                mu=ST_VVASRG_VVH_npt[generic_attr_states["ST_VVASRG_state"]][0], sigma=ST_VVASRG_VVH_npt[generic_attr_states["ST_VVASRG_state"]][1],
                                                lower=0, upper=1)
        generic_ST_VVASRG_VVM_like = pm.TruncatedNormal("generic_ST_VVASRG_VVM_like",
                                                mu=ST_VVASRG_VVM_npt[generic_attr_states["ST_VVASRG_state"]][0], sigma=ST_VVASRG_VVM_npt[generic_attr_states["ST_VVASRG_state"]][1],
                                                lower=0, upper=1)
        generic_ST_VVASRG_VVL_like = pm.TruncatedNormal("generic_ST_VVASRG_VVL_like",
                                                mu=ST_VVASRG_VVL_npt[generic_attr_states["ST_VVASRG_state"]][0], sigma=ST_VVASRG_VVL_npt[generic_attr_states["ST_VVASRG_state"]][1],
                                                lower=0, upper=1)
        # m1-m3: a part of marginal probability
        # m1 = P(VV=H)P(attribute states|VV=H)
        # m2 = P(VV=M)P(attribute states|VV=M)
        # m3 = P(VV=L)P(attribute states|VV=L)
        generic_ST_VV_m1 = ST_VVH_prior * generic_ST_VVSITE_VVH_like * generic_ST_VVSQTE_VVH_like * generic_ST_VVSAPG_VVH_like * generic_ST_VVSATE_VVH_like * generic_ST_TAVV_VVH_like * generic_ST_HAVV_VVH_like * generic_ST_SAVV_VVH_like * generic_ST_RAVV_VVH_like * generic_ST_CMVV_VVH_like * generic_ST_RaAVV_VVH_like * generic_ST_VVASRG_VVH_like
        generic_ST_VV_m2 = ST_VVM_prior * generic_ST_VVSITE_VVM_like * generic_ST_VVSQTE_VVM_like * generic_ST_VVSAPG_VVM_like * generic_ST_VVSATE_VVM_like * generic_ST_TAVV_VVM_like * generic_ST_HAVV_VVM_like * generic_ST_SAVV_VVM_like * generic_ST_RAVV_VVM_like * generic_ST_CMVV_VVM_like * generic_ST_RaAVV_VVM_like * generic_ST_VVASRG_VVM_like
        generic_ST_VV_m3 = ST_VVL_prior * generic_ST_VVSITE_VVL_like * generic_ST_VVSQTE_VVL_like * generic_ST_VVSAPG_VVL_like * generic_ST_VVSATE_VVL_like * generic_ST_TAVV_VVL_like * generic_ST_HAVV_VVL_like * generic_ST_SAVV_VVL_like * generic_ST_RAVV_VVL_like * generic_ST_CMVV_VVL_like * generic_ST_RaAVV_VVL_like * generic_ST_VVASRG_VVL_like

        # k = 1 / marginal probability
        generic_ST_VV_k = 1 / (generic_ST_VV_m1 + generic_ST_VV_m2 + generic_ST_VV_m3)

        # posterior probability of V&V quality in ST phase
        generic_ST_VVH_post = generic_ST_VV_k * generic_ST_VV_m1
        generic_ST_VVM_post = generic_ST_VV_k * generic_ST_VV_m2
        generic_ST_VVL_post = generic_ST_VV_k * generic_ST_VV_m3

        # Generic Submodel - Test phase

        # Defect Density likelihood: P(Defect Density|state of Dev quality)
        ST_DevH_DD_like = pm.Gamma("ST_DevH_DD_like", alpha=1.2439, beta=4.3055)
        ST_DevM_DD_like = pm.Gamma("ST_DevM_DD_like", alpha=1.5775, beta=3.9236)
        ST_DevL_DD_like = pm.Gamma("ST_DevL_DD_like", alpha=1.5630, beta=3.1705)

        # Defect density: the integral of P(Dev)*P(Defect Density|Dev) dDev
        generic_ST_Defect_Density = (generic_ST_DevH_post * ST_DevH_DD_like + generic_ST_DevM_post * ST_DevM_DD_like + generic_ST_DevL_post * ST_DevL_DD_like)

        generic_ST_Defect_introduced_in_current = generic_function_point * generic_ST_Defect_Density

        # Defect Detection Probability (current) likelihood: P(DDP_current|state of Dev quality, state of VV quality)
        generic_ST_DevH_VVH_DDP_current_like = pm.Beta("generic_ST_DevH_VVH_DDP_current_like", alpha=ST_DevH_VVH_DDP_current_npt[generic_complexity][0], beta=ST_DevH_VVH_DDP_current_npt[generic_complexity][1])
        generic_ST_DevH_VVM_DDP_current_like = pm.Beta("generic_ST_DevH_VVM_DDP_current_like", alpha=ST_DevH_VVM_DDP_current_npt[generic_complexity][0], beta=ST_DevH_VVM_DDP_current_npt[generic_complexity][1])
        generic_ST_DevH_VVL_DDP_current_like = pm.Beta("generic_ST_DevH_VVL_DDP_current_like", alpha=ST_DevH_VVL_DDP_current_npt[generic_complexity][0], beta=ST_DevH_VVL_DDP_current_npt[generic_complexity][1])
        generic_ST_DevM_VVH_DDP_current_like = pm.Beta("generic_ST_DevM_VVH_DDP_current_like", alpha=ST_DevM_VVH_DDP_current_npt[generic_complexity][0], beta=ST_DevM_VVH_DDP_current_npt[generic_complexity][1])
        generic_ST_DevM_VVM_DDP_current_like = pm.Beta("generic_ST_DevM_VVM_DDP_current_like", alpha=ST_DevM_VVM_DDP_current_npt[generic_complexity][0], beta=ST_DevM_VVM_DDP_current_npt[generic_complexity][1])
        generic_ST_DevM_VVL_DDP_current_like = pm.Beta("generic_ST_DevM_VVL_DDP_current_like", alpha=ST_DevM_VVL_DDP_current_npt[generic_complexity][0], beta=ST_DevM_VVL_DDP_current_npt[generic_complexity][1])
        generic_ST_DevL_VVH_DDP_current_like = pm.Beta("generic_ST_DevL_VVH_DDP_current_like", alpha=ST_DevL_VVH_DDP_current_npt[generic_complexity][0], beta=ST_DevL_VVH_DDP_current_npt[generic_complexity][1])
        generic_ST_DevL_VVM_DDP_current_like = pm.Beta("generic_ST_DevL_VVM_DDP_current_like", alpha=ST_DevL_VVM_DDP_current_npt[generic_complexity][0], beta=ST_DevL_VVM_DDP_current_npt[generic_complexity][1])
        generic_ST_DevL_VVL_DDP_current_like = pm.Beta("generic_ST_DevL_VVL_DDP_current_like", alpha=ST_DevL_VVL_DDP_current_npt[generic_complexity][0], beta=ST_DevL_VVL_DDP_current_npt[generic_complexity][1])

        # Defect Detection Probability (current): the integral of P(DDP_current|Dev, VV) dDev,VV
        generic_ST_Defect_Detection_Probability_current = generic_ST_DevH_post * generic_ST_VVH_post * generic_ST_DevH_VVH_DDP_current_like + generic_ST_DevH_post * generic_ST_VVM_post * generic_ST_DevH_VVM_DDP_current_like + generic_ST_DevH_post * generic_ST_VVL_post * generic_ST_DevH_VVL_DDP_current_like + generic_ST_DevM_post * generic_ST_VVH_post * generic_ST_DevM_VVH_DDP_current_like + generic_ST_DevM_post * generic_ST_VVM_post * generic_ST_DevM_VVM_DDP_current_like + generic_ST_DevM_post * generic_ST_VVL_post * generic_ST_DevM_VVL_DDP_current_like + generic_ST_DevL_post * generic_ST_VVH_post * generic_ST_DevL_VVH_DDP_current_like + generic_ST_DevL_post * generic_ST_VVM_post * generic_ST_DevL_VVM_DDP_current_like + generic_ST_DevL_post * generic_ST_VVL_post * generic_ST_DevL_VVL_DDP_current_like

        generic_ST_Detected_Defect_current = generic_ST_Defect_introduced_in_current * generic_ST_Defect_Detection_Probability_current

        generic_ST_Remaining_Defect_current = generic_ST_Defect_introduced_in_current - generic_ST_Detected_Defect_current

        # Defect Detection Probability (previous) likelihood: P(DDP_previous|state of Dev quality, state of VV quality)
        generic_ST_DevH_VVH_DDP_previous_like = pm.Beta("generic_ST_DevH_VVH_DDP_previous_like", alpha=ST_DevH_VVH_DDP_previous_npt[generic_complexity][0], beta=ST_DevH_VVH_DDP_previous_npt[generic_complexity][1])
        generic_ST_DevH_VVM_DDP_previous_like = pm.Beta("generic_ST_DevH_VVM_DDP_previous_like", alpha=ST_DevH_VVM_DDP_previous_npt[generic_complexity][0], beta=ST_DevH_VVM_DDP_previous_npt[generic_complexity][1])
        generic_ST_DevH_VVL_DDP_previous_like = pm.Beta("generic_ST_DevH_VVL_DDP_previous_like", alpha=ST_DevH_VVL_DDP_previous_npt[generic_complexity][0], beta=ST_DevH_VVL_DDP_previous_npt[generic_complexity][1])
        generic_ST_DevM_VVH_DDP_previous_like = pm.Beta("generic_ST_DevM_VVH_DDP_previous_like", alpha=ST_DevM_VVH_DDP_previous_npt[generic_complexity][0], beta=ST_DevM_VVH_DDP_previous_npt[generic_complexity][1])
        generic_ST_DevM_VVM_DDP_previous_like = pm.Beta("generic_ST_DevM_VVM_DDP_previous_like", alpha=ST_DevM_VVM_DDP_previous_npt[generic_complexity][0], beta=ST_DevM_VVM_DDP_previous_npt[generic_complexity][1])
        generic_ST_DevM_VVL_DDP_previous_like = pm.Beta("generic_ST_DevM_VVL_DDP_previous_like", alpha=ST_DevM_VVL_DDP_previous_npt[generic_complexity][0], beta=ST_DevM_VVL_DDP_previous_npt[generic_complexity][1])
        generic_ST_DevL_VVH_DDP_previous_like = pm.Beta("generic_ST_DevL_VVH_DDP_previous_like", alpha=ST_DevL_VVH_DDP_previous_npt[generic_complexity][0], beta=ST_DevL_VVH_DDP_previous_npt[generic_complexity][1])
        generic_ST_DevL_VVM_DDP_previous_like = pm.Beta("generic_ST_DevL_VVM_DDP_previous_like", alpha=ST_DevL_VVM_DDP_previous_npt[generic_complexity][0], beta=ST_DevL_VVM_DDP_previous_npt[generic_complexity][1])
        generic_ST_DevL_VVL_DDP_previous_like = pm.Beta("generic_ST_DevL_VVL_DDP_previous_like", alpha=ST_DevL_VVL_DDP_previous_npt[generic_complexity][0], beta=ST_DevL_VVL_DDP_previous_npt[generic_complexity][1])

        # Defect Detection Probability (previous): the integral of P(DDP_previous|Dev, VV) dDev,VV
        generic_ST_Defect_Detection_Probability_previous = generic_ST_DevH_post * generic_ST_VVH_post * generic_ST_DevH_VVH_DDP_previous_like + generic_ST_DevH_post * generic_ST_VVM_post * generic_ST_DevH_VVM_DDP_previous_like + generic_ST_DevH_post * generic_ST_VVL_post * generic_ST_DevH_VVL_DDP_previous_like + generic_ST_DevM_post * generic_ST_VVH_post * generic_ST_DevM_VVH_DDP_previous_like + generic_ST_DevM_post * generic_ST_VVM_post * generic_ST_DevM_VVM_DDP_previous_like + generic_ST_DevM_post * generic_ST_VVL_post * generic_ST_DevM_VVL_DDP_previous_like + generic_ST_DevL_post * generic_ST_VVH_post * generic_ST_DevL_VVH_DDP_previous_like + generic_ST_DevL_post * generic_ST_VVM_post * generic_ST_DevL_VVM_DDP_previous_like + generic_ST_DevL_post * generic_ST_VVL_post * generic_ST_DevL_VVL_DDP_previous_like

        generic_ST_Detected_Defect_previous = generic_IM_Total_Remained_Defect * generic_ST_Defect_Detection_Probability_previous

        generic_ST_Remaining_Defect_previous = generic_IM_Total_Remained_Defect - generic_ST_Detected_Defect_previous

        generic_ST_Total_Remained_Defect = generic_ST_Remaining_Defect_current + generic_ST_Remaining_Defect_previous

        # Generic Dev Attribute model - Installation & Checkout phase
        # prior probability of Dev quality in IC phase
        IC_DevH_prior = pm.Beta("IC_DevH_prior", alpha=0.99, beta=1.66)
        IC_DevM_prior = pm.Beta("IC_DevM_prior", alpha=1.28, beta=1.05)
        IC_DevL_prior = pm.Beta("IC_DevL_prior", alpha=2.83, beta=32.73)
        # Attribute Installation Procedure Generation
        generic_IC_IPG_DevH_like = pm.TruncatedNormal("generic_IC_IPG_DevH_like",
                                            mu=IC_IPG_DevH_npt[generic_attr_states["IC_IPG_state"]][0], sigma=IC_IPG_DevH_npt[generic_attr_states["IC_IPG_state"]][1],
                                            lower=0, upper=1)
        generic_IC_IPG_DevM_like = pm.TruncatedNormal("generic_IC_IPG_DevM_like",
                                            mu=IC_IPG_DevM_npt[generic_attr_states["IC_IPG_state"]][0], sigma=IC_IPG_DevM_npt[generic_attr_states["IC_IPG_state"]][1],
                                            lower=0, upper=1)
        generic_IC_IPG_DevL_like = pm.TruncatedNormal("generic_IC_IPG_DevL_like",
                                            mu=IC_IPG_DevL_npt[generic_attr_states["IC_IPG_state"]][0], sigma=IC_IPG_DevL_npt[generic_attr_states["IC_IPG_state"]][1],
                                            lower=0, upper=1)
        # Attribute Installation and Checkout
        generic_IC_IaC_DevH_like = pm.TruncatedNormal("generic_IC_IaC_DevH_like",
                                            mu=IC_IaC_DevH_npt[generic_attr_states["IC_IaC_state"]][0], sigma=IC_IaC_DevH_npt[generic_attr_states["IC_IaC_state"]][1],
                                            lower=0, upper=1)
        generic_IC_IaC_DevM_like = pm.TruncatedNormal("generic_IC_IaC_DevM_like",
                                            mu=IC_IaC_DevM_npt[generic_attr_states["IC_IaC_state"]][0], sigma=IC_IaC_DevM_npt[generic_attr_states["IC_IaC_state"]][1],
                                            lower=0, upper=1)
        generic_IC_IaC_DevL_like = pm.TruncatedNormal("generic_IC_IaC_DevL_like",
                                            mu=IC_IaC_DevL_npt[generic_attr_states["IC_IaC_state"]][0], sigma=IC_IaC_DevL_npt[generic_attr_states["IC_IaC_state"]][1],
                                            lower=0, upper=1)
        # Attribute Hazard Analysis - IC phase
        generic_IC_HA_DevH_like = pm.TruncatedNormal("generic_IC_HA_DevH_like",
                                            mu=IC_HA_DevH_npt[generic_attr_states["IC_HA_state"]][0], sigma=IC_HA_DevH_npt[generic_attr_states["IC_HA_state"]][1],
                                            lower=0, upper=1)
        generic_IC_HA_DevM_like = pm.TruncatedNormal("generic_IC_HA_DevM_like",
                                            mu=IC_HA_DevM_npt[generic_attr_states["IC_HA_state"]][0], sigma=IC_HA_DevM_npt[generic_attr_states["IC_HA_state"]][1],
                                            lower=0, upper=1)
        generic_IC_HA_DevL_like = pm.TruncatedNormal("generic_IC_HA_DevL_like",
                                            mu=IC_HA_DevL_npt[generic_attr_states["IC_HA_state"]][0], sigma=IC_HA_DevL_npt[generic_attr_states["IC_HA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Security Analysis - IC phase
        generic_IC_SA_DevH_like = pm.TruncatedNormal("generic_IC_SA_DevH_like",
                                            mu=IC_SA_DevH_npt[generic_attr_states["IC_SA_state"]][0], sigma=IC_SA_DevH_npt[generic_attr_states["IC_SA_state"]][1],
                                            lower=0, upper=1)
        generic_IC_SA_DevM_like = pm.TruncatedNormal("generic_IC_SA_DevM_like",
                                            mu=IC_SA_DevM_npt[generic_attr_states["IC_SA_state"]][0], sigma=IC_SA_DevM_npt[generic_attr_states["IC_SA_state"]][1],
                                            lower=0, upper=1)
        generic_IC_SA_DevL_like = pm.TruncatedNormal("generic_IC_SA_DevL_like",
                                            mu=IC_SA_DevL_npt[generic_attr_states["IC_SA_state"]][0], sigma=IC_SA_DevL_npt[generic_attr_states["IC_SA_state"]][1],
                                            lower=0, upper=1)
        # Attribute Security Analysis - IC phase
        generic_IC_RA_DevH_like = pm.TruncatedNormal("generic_IC_RA_DevH_like",
                                            mu=IC_RA_DevH_npt[generic_attr_states["IC_RA_state"]][0], sigma=IC_RA_DevH_npt[generic_attr_states["IC_RA_state"]][1],
                                            lower=0, upper=1)
        generic_IC_RA_DevM_like = pm.TruncatedNormal("generic_IC_RA_DevM_like",
                                            mu=IC_RA_DevM_npt[generic_attr_states["IC_RA_state"]][0], sigma=IC_RA_DevM_npt[generic_attr_states["IC_RA_state"]][1],
                                            lower=0, upper=1)
        generic_IC_RA_DevL_like = pm.TruncatedNormal("generic_IC_RA_DevL_like",
                                            mu=IC_RA_DevL_npt[generic_attr_states["IC_RA_state"]][0], sigma=IC_RA_DevL_npt[generic_attr_states["IC_RA_state"]][1],
                                            lower=0, upper=1)
        # m1-m3: a part of marginal probability
        # m1 = P(Dev=H)P(attribute states|Dev=H)
        # m2 = P(Dev=M)P(attribute states|Dev=M)
        # m3 = P(Dev=L)P(attribute states|Dev=L)
        generic_IC_Dev_m1 = IC_DevH_prior * generic_IC_IPG_DevH_like * generic_IC_IaC_DevH_like * generic_IC_HA_DevH_like * generic_IC_SA_DevH_like * generic_IC_RA_DevH_like
        generic_IC_Dev_m2 = IC_DevM_prior * generic_IC_IPG_DevM_like * generic_IC_IaC_DevM_like * generic_IC_HA_DevM_like * generic_IC_SA_DevM_like * generic_IC_RA_DevM_like
        generic_IC_Dev_m3 = IC_DevL_prior * generic_IC_IPG_DevL_like * generic_IC_IaC_DevL_like * generic_IC_HA_DevL_like * generic_IC_SA_DevL_like * generic_IC_RA_DevL_like

        # k = 1 / marginal probability
        generic_IC_Dev_k = 1 / (generic_IC_Dev_m1 + generic_IC_Dev_m2 + generic_IC_Dev_m3)

        # posterior probability of Dev quality in IC phase
        generic_IC_DevH_post = generic_IC_Dev_k * generic_IC_Dev_m1
        generic_IC_DevM_post = generic_IC_Dev_k * generic_IC_Dev_m2
        generic_IC_DevL_post = generic_IC_Dev_k * generic_IC_Dev_m3

        # Generic V&V Attribute model - Installation & Checkout phase
        # prior probability of V&V quality in IC phase
        IC_VVH_prior = pm.Beta("IC_VVH_prior", alpha=1.05, beta=2.26)
        IC_VVM_prior = pm.Beta("IC_VVM_prior", alpha=1.45, beta=1.10)
        IC_VVL_prior = pm.Beta("IC_VVL_prior", alpha=1.28, beta=8.56)
        # Attribute Installation Configuration Audit V&V
        generic_IC_ICAVV_VVH_like = pm.TruncatedNormal("generic_IC_ICAVV_VVH_like",
                                            mu=IC_ICAVV_VVH_npt[generic_attr_states["IC_ICAVV_state"]][0], sigma=IC_ICAVV_VVH_npt[generic_attr_states["IC_ICAVV_state"]][1],
                                            lower=0, upper=1)
        generic_IC_ICAVV_VVM_like = pm.TruncatedNormal("generic_IC_ICAVV_VVM_like",
                                            mu=IC_ICAVV_VVM_npt[generic_attr_states["IC_ICAVV_state"]][0], sigma=IC_ICAVV_VVM_npt[generic_attr_states["IC_ICAVV_state"]][1],
                                            lower=0, upper=1)
        generic_IC_ICAVV_VVL_like = pm.TruncatedNormal("generic_IC_ICAVV_VVL_like",
                                            mu=IC_ICAVV_VVL_npt[generic_attr_states["IC_ICAVV_state"]][0], sigma=IC_ICAVV_VVL_npt[generic_attr_states["IC_ICAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Installation Checkout V&V
        generic_IC_ICVV_VVH_like = pm.TruncatedNormal("generic_IC_ICVV_VVH_like",
                                            mu=IC_ICVV_VVH_npt[generic_attr_states["IC_ICVV_state"]][0], sigma=IC_ICVV_VVH_npt[generic_attr_states["IC_ICVV_state"]][1],
                                            lower=0, upper=1)
        generic_IC_ICVV_VVM_like = pm.TruncatedNormal("generic_IC_ICVV_VVM_like",
                                            mu=IC_ICVV_VVM_npt[generic_attr_states["IC_ICVV_state"]][0], sigma=IC_ICVV_VVM_npt[generic_attr_states["IC_ICVV_state"]][1],
                                            lower=0, upper=1)
        generic_IC_ICVV_VVL_like = pm.TruncatedNormal("generic_IC_ICVV_VVL_like",
                                            mu=IC_ICVV_VVL_npt[generic_attr_states["IC_ICVV_state"]][0], sigma=IC_ICVV_VVL_npt[generic_attr_states["IC_ICVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Hazard Analysis V&V
        generic_IC_HAVV_VVH_like = pm.TruncatedNormal("generic_IC_HAVV_VVH_like",
                                            mu=IC_HAVV_VVH_npt[generic_attr_states["IC_HAVV_state"]][0], sigma=IC_HAVV_VVH_npt[generic_attr_states["IC_HAVV_state"]][1],
                                            lower=0, upper=1)
        generic_IC_HAVV_VVM_like = pm.TruncatedNormal("generic_IC_HAVV_VVM_like",
                                            mu=IC_HAVV_VVM_npt[generic_attr_states["IC_HAVV_state"]][0], sigma=IC_HAVV_VVM_npt[generic_attr_states["IC_HAVV_state"]][1],
                                            lower=0, upper=1)
        generic_IC_HAVV_VVL_like = pm.TruncatedNormal("generic_IC_HAVV_VVL_like",
                                            mu=IC_HAVV_VVL_npt[generic_attr_states["IC_HAVV_state"]][0], sigma=IC_HAVV_VVL_npt[generic_attr_states["IC_HAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Security Analysis V&V
        generic_IC_SAVV_VVH_like = pm.TruncatedNormal("generic_IC_SAVV_VVH_like",
                                            mu=IC_SAVV_VVH_npt[generic_attr_states["IC_SAVV_state"]][0], sigma=IC_SAVV_VVH_npt[generic_attr_states["IC_SAVV_state"]][1],
                                            lower=0, upper=1)
        generic_IC_SAVV_VVM_like = pm.TruncatedNormal("generic_IC_SAVV_VVM_like",
                                            mu=IC_SAVV_VVM_npt[generic_attr_states["IC_SAVV_state"]][0], sigma=IC_SAVV_VVM_npt[generic_attr_states["IC_SAVV_state"]][1],
                                            lower=0, upper=1)
        generic_IC_SAVV_VVL_like = pm.TruncatedNormal("generic_IC_SAVV_VVL_like",
                                            mu=IC_SAVV_VVL_npt[generic_attr_states["IC_SAVV_state"]][0], sigma=IC_SAVV_VVL_npt[generic_attr_states["IC_SAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute Risk Analysis V&V
        generic_IC_RAVV_VVH_like = pm.TruncatedNormal("generic_IC_RAVV_VVH_like",
                                            mu=IC_RAVV_VVH_npt[generic_attr_states["IC_RAVV_state"]][0], sigma=IC_RAVV_VVH_npt[generic_attr_states["IC_RAVV_state"]][1],
                                            lower=0, upper=1)
        generic_IC_RAVV_VVM_like = pm.TruncatedNormal("generic_IC_RAVV_VVM_like",
                                            mu=IC_RAVV_VVM_npt[generic_attr_states["IC_RAVV_state"]][0], sigma=IC_RAVV_VVM_npt[generic_attr_states["IC_RAVV_state"]][1],
                                            lower=0, upper=1)
        generic_IC_RAVV_VVL_like = pm.TruncatedNormal("generic_IC_RAVV_VVL_like",
                                            mu=IC_RAVV_VVL_npt[generic_attr_states["IC_RAVV_state"]][0], sigma=IC_RAVV_VVL_npt[generic_attr_states["IC_RAVV_state"]][1],
                                            lower=0, upper=1)
        # Attribute V&V Installation and Checkout Phase Activity Summary Report Generation
        generic_IC_VVASRG_VVH_like = pm.TruncatedNormal("generic_IC_VVASRG_VVH_like",
                                                mu=IC_VVASRG_VVH_npt[generic_attr_states["IC_VVASRG_state"]][0], sigma=IC_VVASRG_VVH_npt[generic_attr_states["IC_VVASRG_state"]][1],
                                                lower=0, upper=1)
        generic_IC_VVASRG_VVM_like = pm.TruncatedNormal("generic_IC_VVASRG_VVM_like",
                                                mu=IC_VVASRG_VVM_npt[generic_attr_states["IC_VVASRG_state"]][0], sigma=IC_VVASRG_VVM_npt[generic_attr_states["IC_VVASRG_state"]][1],
                                                lower=0, upper=1)
        generic_IC_VVASRG_VVL_like = pm.TruncatedNormal("generic_IC_VVASRG_VVL_like",
                                                mu=IC_VVASRG_VVL_npt[generic_attr_states["IC_VVASRG_state"]][0], sigma=IC_VVASRG_VVL_npt[generic_attr_states["IC_VVASRG_state"]][1],
                                                lower=0, upper=1)
        # Attribute V&V Final Report Generation
        generic_IC_VVFRG_VVH_like = pm.TruncatedNormal("generic_IC_VVFRG_VVH_like",
                                            mu=IC_VVFRG_VVH_npt[generic_attr_states["IC_VVFRG_state"]][0], sigma=IC_VVFRG_VVH_npt[generic_attr_states["IC_VVFRG_state"]][1],
                                            lower=0, upper=1)
        generic_IC_VVFRG_VVM_like = pm.TruncatedNormal("generic_IC_VVFRG_VVM_like",
                                            mu=IC_VVFRG_VVM_npt[generic_attr_states["IC_VVFRG_state"]][0], sigma=IC_VVFRG_VVM_npt[generic_attr_states["IC_VVFRG_state"]][1],
                                            lower=0, upper=1)
        generic_IC_VVFRG_VVL_like = pm.TruncatedNormal("generic_IC_VVFRG_VVL_like",
                                            mu=IC_VVFRG_VVL_npt[generic_attr_states["IC_VVFRG_state"]][0], sigma=IC_VVFRG_VVL_npt[generic_attr_states["IC_VVFRG_state"]][1],
                                            lower=0, upper=1)
        # m1-m3: a part of marginal probability
        # m1 = P(VV=H)P(attribute states|VV=H)
        # m2 = P(VV=M)P(attribute states|VV=M)
        # m3 = P(VV=L)P(attribute states|VV=L)
        generic_IC_VV_m1 = IC_VVH_prior * generic_IC_ICAVV_VVH_like * generic_IC_ICVV_VVH_like * generic_IC_HAVV_VVH_like * generic_IC_SAVV_VVH_like * generic_IC_RAVV_VVH_like * generic_IC_VVASRG_VVH_like * generic_IC_VVFRG_VVH_like
        generic_IC_VV_m2 = IC_VVM_prior * generic_IC_ICAVV_VVM_like * generic_IC_ICVV_VVM_like * generic_IC_HAVV_VVM_like * generic_IC_SAVV_VVM_like * generic_IC_RAVV_VVM_like * generic_IC_VVASRG_VVM_like * generic_IC_VVFRG_VVM_like
        generic_IC_VV_m3 = IC_VVL_prior * generic_IC_ICAVV_VVL_like * generic_IC_ICVV_VVL_like * generic_IC_HAVV_VVL_like * generic_IC_SAVV_VVL_like * generic_IC_RAVV_VVL_like * generic_IC_VVASRG_VVL_like * generic_IC_VVFRG_VVL_like

        # k = 1 / marginal probability
        generic_IC_VV_k = 1 / (generic_IC_VV_m1 + generic_IC_VV_m2 + generic_IC_VV_m3)

        # posterior probability of V&V quality in IC phase
        generic_IC_VVH_post = generic_IC_VV_k * generic_IC_VV_m1
        generic_IC_VVM_post = generic_IC_VV_k * generic_IC_VV_m2
        generic_IC_VVL_post = generic_IC_VV_k * generic_IC_VV_m3

        # Generic Submodel - Installation & Checkout phase

        # Defect Density likelihood: P(Defect Density|state of Dev quality)
        IC_DevH_DD_like = pm.Gamma("IC_DevH_DD_like", alpha=0.6106, beta=3.4640)
        IC_DevM_DD_like = pm.Gamma("IC_DevM_DD_like", alpha=0.6838, beta=2.6797)
        IC_DevL_DD_like = pm.Gamma("IC_DevL_DD_like", alpha=0.6514, beta=2.3803)

        # Defect density: the integral of P(Dev)*P(Defect Density|Dev) dDev
        generic_IC_Defect_Density = (generic_IC_DevH_post * IC_DevH_DD_like + generic_IC_DevM_post * IC_DevM_DD_like + generic_IC_DevL_post * IC_DevL_DD_like)

        generic_IC_Defect_introduced_in_current = generic_function_point * generic_IC_Defect_Density

        # Defect Detection Probability (current) likelihood: P(DDP_current|state of VV quality)
        generic_IC_VVH_DDP_current_like = pm.Beta("generic_IC_VVH_DDP_current_like", alpha=IC_VVH_DDP_current_npt[generic_complexity][0], beta=IC_VVH_DDP_current_npt[generic_complexity][1])
        generic_IC_VVM_DDP_current_like = pm.Beta("generic_IC_VVM_DDP_current_like", alpha=IC_VVM_DDP_current_npt[generic_complexity][0], beta=IC_VVM_DDP_current_npt[generic_complexity][1])
        generic_IC_VVL_DDP_current_like = pm.Beta("generic_IC_VVL_DDP_current_like", alpha=IC_VVL_DDP_current_npt[generic_complexity][0], beta=IC_VVL_DDP_current_npt[generic_complexity][1])

        # Defect Detection Probability (current): the integral of P(DDP_current|VV) dVV
        generic_IC_Defect_Detection_Probability_current = generic_IC_VVH_post * generic_IC_VVH_DDP_current_like + generic_IC_VVM_post * generic_IC_VVM_DDP_current_like + generic_IC_VVL_post * generic_IC_VVL_DDP_current_like

        generic_IC_Detected_Defect_current = generic_IC_Defect_introduced_in_current * generic_IC_Defect_Detection_Probability_current

        generic_IC_Remaining_Defect_current = generic_IC_Defect_introduced_in_current - generic_IC_Detected_Defect_current

        # Defect Detection Probability (previous) likelihood: P(DDP_previous|state of VV quality)
        generic_IC_VVH_DDP_previous_like = pm.Beta("generic_IC_VVH_DDP_previous_like", alpha=IC_VVH_DDP_previous_npt[generic_complexity][0], beta=IC_VVH_DDP_previous_npt[generic_complexity][1])
        generic_IC_VVM_DDP_previous_like = pm.Beta("generic_IC_VVM_DDP_previous_like", alpha=IC_VVM_DDP_previous_npt[generic_complexity][0], beta=IC_VVM_DDP_previous_npt[generic_complexity][1])
        generic_IC_VVL_DDP_previous_like = pm.Beta("generic_IC_VVL_DDP_previous_like", alpha=IC_VVL_DDP_previous_npt[generic_complexity][0], beta=IC_VVL_DDP_previous_npt[generic_complexity][1])

        # Defect Detection Probability (previous): the integral of P(DDP_previous|VV) dVV
        generic_IC_Defect_Detection_Probability_previous = generic_IC_VVH_post * generic_IC_VVH_DDP_previous_like + generic_IC_VVM_post * generic_IC_VVM_DDP_previous_like + generic_IC_VVL_post * generic_IC_VVL_DDP_previous_like

        generic_IC_Detected_Defect_previous = generic_ST_Total_Remained_Defect * generic_IC_Defect_Detection_Probability_previous

        generic_IC_Remaining_Defect_previous = generic_ST_Total_Remained_Defect - generic_IC_Detected_Defect_previous

        generic_IC_Total_Remained_Defect = pm.Deterministic("generic_IC_Total_Remained_Defect", generic_IC_Remaining_Defect_current + generic_IC_Remaining_Defect_previous)

        generic_SFP = pm.LogNormal("generic_SFP", mu=(-10.45), sigma=2.217)

        generic_FSD = pm.Deterministic("generic_FSD", generic_SFP / generic_IC_Total_Remained_Defect)
    return model
