
class State():
    High = 0
    Medium = 1
    Low = 2

attributes = ["SR_SDP_state", "SR_CD_state", "SR_SRS_state", "SR_TA_state", "SR_CA_state", "SR_HA_state", "SR_SA_state", "SR_RA_state", "SR_SQTPG_state", "SR_SATPG_state", "SR_CM_state", "SR_RaA_state",
              "SR_SVVP_state", "SR_CDE_state", "SR_HRAA_state", "SR_SRE_state", "SR_IAVV_state", "SR_TAVV_state", "SR_CAVV_state", "SR_HAVV_state", "SR_SAVV_state", "SR_RAVV_state", "SR_VVSQTPG_state", "SR_VVSATPG_state", "SR_CMA_state", "SR_RaAVV_state", "SR_VVASRG_state",
              "SD_SAD_state", "SD_SDD_state", "SD_TA_state", "SD_CA_state", "SD_HA_state", "SD_SA_state", "SD_RA_state", "SD_SCTPG_state", "SD_SITPG_state", "SD_SCTDG_state", "SD_SITDG_state", "SD_SQTDG_state", "SD_SATDG_state", "SD_CM_state", "SD_RaA_state",
              "SD_DE_state", "SD_IAVV_state", "SD_TAVV_state", "SD_CAVV_state", "SD_HAVV_state", "SD_SAVV_state", "SD_RAVV_state", "SD_VVSCTPG_state", "SD_VVSITPG_state", "SD_VVSCTDG_state", "SD_VVSITDG_state", "SD_VVSQTDG_state", "SD_VVSATDG_state", "SD_CMVV_state", "SD_RaAVV_state", "SD_VVASRG_state",
              "IM_SCaSCDG_state", "IM_TA_state", "IM_CA_state", "IM_HA_state", "IM_SA_state", "IM_RA_state", "IM_CTCG_state", "IM_SITCG_state", "IM_SQTCG_state", "IM_SATCG_state", "IM_SCTPG_state", "IM_SITPG_state", "IM_SQTPG_state", "IM_CM_state", "IM_RaA_state", "IM_SCTE_state",
              "IM_SCaSCDE_state", "IM_IAVV_state", "IM_TAVV_state", "IM_CAVV_state", "IM_HAVV_state", "IM_SAVV_state", "IM_RAVV_state", "IM_VVSCTCG_state", "IM_VVSITCG_state", "IM_VVSQTCG_state", "IM_VVSATCG_state", "IM_VVSCTPG_state", "IM_VVSITPG_state", "IM_VVSQTPG_state", "IM_VVSCTE_state", "IM_CMVV_state", "IM_RaAVV_state", "IM_VVASRG_state",
              "ST_SITE_state", "ST_SQTE_state", "ST_SAPG_state", "ST_SATE_state", "ST_TA_state", "ST_HA_state", "ST_SA_state", "ST_RA_state", "ST_CM_state", "ST_RaA_state",
              "ST_VVSITE_state", "ST_VVSQTE_state", "ST_VVSAPG_state", "ST_VVSATE_state", "ST_TAVV_state", "ST_HAVV_state", "ST_SAVV_state", "ST_RAVV_state", "ST_CMVV_state", "ST_RaAVV_state", "ST_VVASRG_state",
              "IC_IPG_state", "IC_IaC_state", "IC_HA_state", "IC_SA_state", "IC_RA_state",
              "IC_ICAVV_state", "IC_ICVV_state", "IC_HAVV_state", "IC_SAVV_state", "IC_RAVV_state", "IC_VVASRG_state", "IC_VVFRG_state"
             ]

class BayesianData:

    def __init__(self):
        self.function_point = 0
        self.complexity = self.calc_complexity()
        self.attr_states = {attribute: State.Low for attribute in attributes}

    def calc_complexity(self):
        # Complexity: (FP >= 1000)? High: (FP >= 100)? Medium: Low
        if self.function_point >= 1000:
            return State.High
        if self.function_point >= 100:
            return State.Medium
        return State.Low

    def set_function_point(self, fp):
        self.function_point = fp
        self.complexity = self.calc_complexity()
