# input data of model
data <- list(
    # Dev Attribute model - Requirement phase

    # node probability tables of attribute: P(attribute state|Dev=H/M/L)
    # Dimension: row, col
    # row represents attribute states (H/M/L), column represents mu and sigma
    # (1,1) (2,1) (1,2) (2,2) (1,3) (2,3)
    SR_SDP_DevH_npt=structure(.Data=c(0.625, 0.117, 0.325, 0.147, 0.050, 0.032), .Dim=c(2,3)),
    SR_SDP_DevM_npt=structure(.Data=c(0.193, 0.073, 0.643, 0.113, 0.164, 0.103), .Dim=c(2,3)),
    SR_SDP_DevL_npt=structure(.Data=c(0.063, 0.068, 0.303, 0.190, 0.633, 0.178), .Dim=c(2,3)),

    SR_CD_DevH_npt=structure(.Data=c(0.675, 0.129, 0.267, 0.082, 0.058, 0.074), .Dim=c(2,3)),
    SR_CD_DevM_npt=structure(.Data=c(0.221, 0.091, 0.643, 0.113, 0.136, 0.063), .Dim=c(2,3)),
    SR_CD_DevL_npt=structure(.Data=c(0.050, 0.032, 0.292, 0.146, 0.658, 0.153), .Dim=c(2,3)),

    SR_SRS_DevH_npt=structure(.Data=c(0.717, 0.098, 0.242, 0.092, 0.042, 0.038), .Dim=c(2,3)),
    SR_SRS_DevM_npt=structure(.Data=c(0.186, 0.090, 0.657, 0.098, 0.157, 0.079), .Dim=c(2,3)),
    SR_SRS_DevL_npt=structure(.Data=c(0.042, 0.038, 0.275, 0.141, 0.683, 0.133), .Dim=c(2,3)),

    SR_TA_DevH_npt=structure(.Data=c(0.567, 0.175, 0.295, 0.105, 0.138, 0.108), .Dim=c(2,3)),
    SR_TA_DevM_npt=structure(.Data=c(0.143, 0.113, 0.657, 0.098, 0.200, 0.100), .Dim=c(2,3)),
    SR_TA_DevL_npt=structure(.Data=c(0.068, 0.089, 0.223, 0.116, 0.708, 0.150), .Dim=c(2,3)),

    SR_CA_DevH_npt=structure(.Data=c(0.642, 0.215, 0.270, 0.143, 0.088, 0.101), .Dim=c(2,3)),
    SR_CA_DevM_npt=structure(.Data=c(0.179, 0.141, 0.636, 0.138, 0.186, 0.111), .Dim=c(2,3)),
    SR_CA_DevL_npt=structure(.Data=c(0.088, 0.101, 0.295, 0.105, 0.617, 0.169), .Dim=c(2,3)),

    SR_HA_DevH_npt=structure(.Data=c(0.606, 0.188, 0.297, 0.113, 0.097, 0.120), .Dim=c(2,3)),
    SR_HA_DevM_npt=structure(.Data=c(0.176, 0.118, 0.619, 0.157, 0.205, 0.089), .Dim=c(2,3)),
    SR_HA_DevL_npt=structure(.Data=c(0.081, 0.126, 0.289, 0.100, 0.631, 0.181), .Dim=c(2,3)),

    SR_SA_DevH_npt=structure(.Data=c(0.642, 0.146, 0.292, 0.111, 0.067, 0.068), .Dim=c(2,3)),
    SR_SA_DevM_npt=structure(.Data=c(0.186, 0.135, 0.636, 0.125, 0.179, 0.070), .Dim=c(2,3)),
    SR_SA_DevL_npt=structure(.Data=c(0.063, 0.085, 0.312, 0.130, 0.625, 0.170), .Dim=c(2,3)),

    SR_RA_DevH_npt=structure(.Data=c(0.536, 0.215, 0.303, 0.114, 0.161, 0.149), .Dim=c(2,3)),
    SR_RA_DevM_npt=structure(.Data=c(0.190, 0.151, 0.612, 0.193, 0.198, 0.108), .Dim=c(2,3)),
    SR_RA_DevL_npt=structure(.Data=c(0.119, 0.135, 0.276, 0.122, 0.606, 0.213), .Dim=c(2,3)),

    SR_SQTPG_DevH_npt=structure(.Data=c(0.717, 0.157, 0.258, 0.136, 0.025, 0.027), .Dim=c(2,3)),
    SR_SQTPG_DevM_npt=structure(.Data=c(0.183, 0.107, 0.648, 0.180, 0.169, 0.125), .Dim=c(2,3)),
    SR_SQTPG_DevL_npt=structure(.Data=c(0.058, 0.074, 0.233, 0.103, 0.708, 0.159), .Dim=c(2,3)),

    SR_SATPG_DevH_npt=structure(.Data=c(0.667, 0.129, 0.300, 0.114, 0.033, 0.026), .Dim=c(2,3)),
    SR_SATPG_DevM_npt=structure(.Data=c(0.207, 0.084, 0.657, 0.113, 0.136, 0.085), .Dim=c(2,3)),
    SR_SATPG_DevL_npt=structure(.Data=c(0.063, 0.085, 0.287, 0.096, 0.650, 0.158), .Dim=c(2,3)),

    SR_CM_DevH_npt=structure(.Data=c(0.589, 0.149, 0.297, 0.027, 0.114, 0.127), .Dim=c(2,3)),
    SR_CM_DevM_npt=structure(.Data=c(0.212, 0.086, 0.583, 0.159, 0.205, 0.117), .Dim=c(2,3)),
    SR_CM_DevL_npt=structure(.Data=c(0.139, 0.127, 0.306, 0.014, 0.556, 0.137), .Dim=c(2,3)),

    SR_RaA_DevH_npt=structure(.Data=c(0.589, 0.193, 0.272, 0.085, 0.139, 0.127), .Dim=c(2,3)),
    SR_RaA_DevM_npt=structure(.Data=c(0.226, 0.139, 0.605, 0.198, 0.169, 0.099), .Dim=c(2,3)),
    SR_RaA_DevL_npt=structure(.Data=c(0.132, 0.137, 0.296, 0.122, 0.572, 0.201), .Dim=c(2,3)),

    # state of attribute: 1 -> High, 2 -> Medium, 3 -> Low
    SR_SDP_state=2, SR_CD_state=2, SR_SRS_state=2, SR_TA_state=2, SR_CA_state=3,
    SR_HA_state=2, SR_SA_state=3, SR_RA_state=3, SR_SQTPG_state=2, SR_SATPG_state=2,
    SR_CM_state=2, SR_RaA_state=2,
    generic_SR_SDP_state=2, generic_SR_CD_state=2, generic_SR_SRS_state=2, generic_SR_TA_state=2, generic_SR_CA_state=2, generic_SR_HA_state=2, generic_SR_SA_state=2, generic_SR_RA_state=2, generic_SR_SQTPG_state=2, generic_SR_SATPG_state=2, generic_SR_CM_state=2, generic_SR_RaA_state=2,


    # V&V Attribute model - Requirement phase

    # node probability tables of attribute: P(attribute state|VV=H/M/L)
    # Dimension: row, col
    # row represents attribute states (H/M/L), column represents mu and sigma
    # (1,1) (2,1) (1,2) (2,2) (1,3) (2,3)
    SR_SVVP_VVH_npt=structure(.Data=c(0.750, 0.122, 0.208, 0.102, 0.042, 0.038), .Dim=c(2,3)),
    SR_SVVP_VVM_npt=structure(.Data=c(0.179, 0.057, 0.643, 0.113, 0.179, 0.099), .Dim=c(2,3)),
    SR_SVVP_VVL_npt=structure(.Data=c(0.075, 0.069, 0.242, 0.092, 0.683, 0.133), .Dim=c(2,3)),

    SR_CDE_VVH_npt=structure(.Data=c(0.692, 0.102, 0.267, 0.082, 0.042, 0.020), .Dim=c(2,3)),
    SR_CDE_VVM_npt=structure(.Data=c(0.171, 0.095, 0.671, 0.125, 0.157, 0.053), .Dim=c(2,3)),
    SR_CDE_VVL_npt=structure(.Data=c(0.067, 0.075, 0.208, 0.102, 0.725, 0.157), .Dim=c(2,3)),

    SR_HRAA_VVH_npt=structure(.Data=c(0.733, 0.129, 0.233, 0.103, 0.033, 0.026), .Dim=c(2,3)),
    SR_HRAA_VVM_npt=structure(.Data=c(0.164, 0.085, 0.657, 0.140, 0.179, 0.057), .Dim=c(2,3)),
    SR_HRAA_VVL_npt=structure(.Data=c(0.058, 0.074, 0.233, 0.103, 0.708, 0.159), .Dim=c(2,3)),

    SR_SRE_VVH_npt=structure(.Data=c(0.733, 0.129, 0.233, 0.103, 0.033, 0.026), .Dim=c(2,3)),
    SR_SRE_VVM_npt=structure(.Data=c(0.171, 0.095, 0.671, 0.125, 0.157, 0.053), .Dim=c(2,3)),
    SR_SRE_VVL_npt=structure(.Data=c(0.042, 0.038, 0.208, 0.102, 0.750, 0.122), .Dim=c(2,3)),

    SR_IAVV_VVH_npt=structure(.Data=c(0.692, 0.102, 0.267, 0.082, 0.042, 0.020), .Dim=c(2,3)),
    SR_IAVV_VVM_npt=structure(.Data=c(0.150, 0.087, 0.686, 0.146, 0.164, 0.063), .Dim=c(2,3)),
    SR_IAVV_VVL_npt=structure(.Data=c(0.058, 0.074, 0.233, 0.103, 0.708, 0.159), .Dim=c(2,3)),

    SR_TAVV_VVH_npt=structure(.Data=c(0.692, 0.188, 0.245, 0.116, 0.063, 0.085), .Dim=c(2,3)),
    SR_TAVV_VVM_npt=structure(.Data=c(0.143, 0.098, 0.671, 0.125, 0.186, 0.090), .Dim=c(2,3)),
    SR_TAVV_VVL_npt=structure(.Data=c(0.050, 0.077, 0.200, 0.110, 0.750, 0.173), .Dim=c(2,3)),

    SR_CAVV_VVH_npt=structure(.Data=c(0.642, 0.146, 0.292, 0.111, 0.067, 0.068), .Dim=c(2,3)),
    SR_CAVV_VVM_npt=structure(.Data=c(0.164, 0.099, 0.629, 0.160, 0.207, 0.079), .Dim=c(2,3)),
    SR_CAVV_VVL_npt=structure(.Data=c(0.108, 0.102, 0.233, 0.103, 0.658, 0.196), .Dim=c(2,3)),

    SR_HAVV_VVH_npt=structure(.Data=c(0.667, 0.129, 0.292, 0.111, 0.042, 0.020), .Dim=c(2,3)),
    SR_HAVV_VVM_npt=structure(.Data=c(0.157, 0.093, 0.643, 0.151, 0.200, 0.076), .Dim=c(2,3)),
    SR_HAVV_VVL_npt=structure(.Data=c(0.088, 0.101, 0.245, 0.116, 0.667, 0.204), .Dim=c(2,3)),

    SR_SAVV_VVH_npt=structure(.Data=c(0.642, 0.146, 0.292, 0.111, 0.067, 0.068), .Dim=c(2,3)),
    SR_SAVV_VVM_npt=structure(.Data=c(0.157, 0.093, 0.643, 0.151, 0.200, 0.076), .Dim=c(2,3)),
    SR_SAVV_VVL_npt=structure(.Data=c(0.088, 0.101, 0.245, 0.116, 0.667, 0.204), .Dim=c(2,3)),

    SR_RAVV_VVH_npt=structure(.Data=c(0.589, 0.193, 0.297, 0.113, 0.114, 0.127), .Dim=c(2,3)),
    SR_RAVV_VVM_npt=structure(.Data=c(0.198, 0.142, 0.598, 0.197, 0.205, 0.094), .Dim=c(2,3)),
    SR_RAVV_VVL_npt=structure(.Data=c(0.136, 0.139, 0.251, 0.119, 0.614, 0.246), .Dim=c(2,3)),

    SR_VVSQTPG_VVH_npt=structure(.Data=c(0.792, 0.174, 0.192, 0.150, 0.017, 0.026), .Dim=c(2,3)),
    SR_VVSQTPG_VVM_npt=structure(.Data=c(0.207, 0.102, 0.636, 0.138, 0.157, 0.061), .Dim=c(2,3)),
    SR_VVSQTPG_VVL_npt=structure(.Data=c(0.080, 0.107, 0.212, 0.125, 0.708, 0.225), .Dim=c(2,3)),

    SR_VVSATPG_VVH_npt=structure(.Data=c(0.642, 0.146, 0.292, 0.111, 0.067, 0.068), .Dim=c(2,3)),
    SR_VVSATPG_VVM_npt=structure(.Data=c(0.214, 0.069, 0.643, 0.079, 0.143, 0.053), .Dim=c(2,3)),
    SR_VVSATPG_VVL_npt=structure(.Data=c(0.102, 0.101, 0.290, 0.099, 0.608, 0.188), .Dim=c(2,3)),

    SR_CMA_VVH_npt=structure(.Data=c(0.547, 0.128, 0.306, 0.014, 0.147, 0.117), .Dim=c(2,3)),
    SR_CMA_VVM_npt=structure(.Data=c(0.219, 0.092, 0.562, 0.142, 0.219, 0.092), .Dim=c(2,3)),
    SR_CMA_VVL_npt=structure(.Data=c(0.169, 0.123, 0.284, 0.094, 0.547, 0.203), .Dim=c(2,3)),

    SR_RaAVV_VVH_npt=structure(.Data=c(0.589, 0.193, 0.272, 0.085, 0.139, 0.127), .Dim=c(2,3)),
    SR_RaAVV_VVM_npt=structure(.Data=c(0.205, 0.121, 0.633, 0.180, 0.162, 0.089), .Dim=c(2,3)),
    SR_RaAVV_VVL_npt=structure(.Data=c(0.136, 0.139, 0.251, 0.119, 0.614, 0.246), .Dim=c(2,3)),

    SR_VVASRG_VVH_npt=structure(.Data=c(0.667, 0.129, 0.267, 0.082, 0.067, 0.068), .Dim=c(2,3)),
    SR_VVASRG_VVM_npt=structure(.Data=c(0.186, 0.107, 0.671, 0.125, 0.143, 0.053), .Dim=c(2,3)),
    SR_VVASRG_VVL_npt=structure(.Data=c(0.093, 0.108, 0.257, 0.125, 0.650, 0.224), .Dim=c(2,3)),

    # state of attribute: 1 -> High, 2 -> Medium, 3 -> Low
    SR_SVVP_state=2, SR_CDE_state=2, SR_HRAA_state=3, SR_SRE_state=2, SR_IAVV_state=2,
    SR_TAVV_state=2, SR_CAVV_state=3, SR_HAVV_state=3, SR_SAVV_state=3, SR_RAVV_state=3,
    SR_VVSQTPG_state=3, SR_VVSATPG_state=3, SR_CMA_state=2, SR_RaAVV_state=3, SR_VVASRG_state=2,
    generic_SR_SVVP_state=2, generic_SR_CDE_state=2, generic_SR_HRAA_state=2, generic_SR_SRE_state=2, generic_SR_IAVV_state=2, generic_SR_TAVV_state=2, generic_SR_CAVV_state=2, generic_SR_HAVV_state=2, generic_SR_SAVV_state=2, generic_SR_RAVV_state=2, generic_SR_VVSQTPG_state=2, generic_SR_VVSATPG_state=2, generic_SR_CMA_state=2, generic_SR_RaAVV_state=2, generic_SR_VVASRG_state=2,


    # Submodel - Requirement phase

    # node probability tables of DDP_current: P(DDP_current|VV=H/M/L)
    # Dimension: row, col
    # row represents Complexity (H/M/L), column represents alpha and beta
    # (1,1) (2,1) (1,2) (2,2) (1,3) (2,3)
    SR_VVH_DDP_current_npt=structure(.Data=c(3.012, 1.68, 6.446, 1.427, 3.739, 0.588), .Dim=c(2,3)),
    SR_VVM_DDP_current_npt=structure(.Data=c(2.299, 1.728, 3.911, 1.498, 4.087, 1.056), .Dim=c(2,3)),
    SR_VVL_DDP_current_npt=structure(.Data=c(1.272, 1.78, 1.637, 1.51, 1.81, 1.403), .Dim=c(2,3)),

    # posterior probability of Dev/V&V qualities in SR phase
    # SR_DevH=0, SR_DevM=0.99, SR_DevL=0.01,
    # SR_VVH=0, SR_VVM=0.17, SR_VVL = 0.83,

    # number of function points (same in all phases)
    SR_FP=56,
    generic_SR_FP=50,


    # Dev Attribute model - Design phase

    # node probability tables of attribute: P(attribute state|Dev=H/M/L)
    # Dimension: row, col
    # row represents attribute states (H/M/L), column represents mu and sigma
    # (1,1) (2,1) (1,2) (2,2) (1,3) (2,3)
    SD_SAD_DevH_npt=structure(.Data=c(0.725, 0.157, 0.208, 0.102, 0.067, 0.075), .Dim=c(2,3)),
    SD_SAD_DevM_npt=structure(.Data=c(0.221, 0.064, 0.586, 0.107, 0.193, 0.067), .Dim=c(2,3)),
    SD_SAD_DevL_npt=structure(.Data=c(0.072, 0.094, 0.228, 0.108, 0.700, 0.164), .Dim=c(2,3)),

    SD_SDD_DevH_npt=structure(.Data=c(0.792, 0.124, 0.192, 0.102, 0.017, 0.026), .Dim=c(2,3)),
    SD_SDD_DevM_npt=structure(.Data=c(0.200, 0.076, 0.629, 0.095, 0.171, 0.091), .Dim=c(2,3)),
    SD_SDD_DevL_npt=structure(.Data=c(0.072, 0.111, 0.203, 0.119, 0.725, 0.223), .Dim=c(2,3)),

    SD_TA_DevH_npt=structure(.Data=c(0.617, 0.186, 0.295, 0.118, 0.088, 0.101), .Dim=c(2,3)),
    SD_TA_DevM_npt=structure(.Data=c(0.200, 0.153, 0.629, 0.147, 0.171, 0.070), .Dim=c(2,3)),
    SD_TA_DevL_npt=structure(.Data=c(0.080, 0.107, 0.212, 0.125, 0.708, 0.225), .Dim=c(2,3)),

    SD_CA_DevH_npt=structure(.Data=c(0.658, 0.196, 0.258, 0.136, 0.083, 0.093), .Dim=c(2,3)),
    SD_CA_DevM_npt=structure(.Data=c(0.164, 0.131, 0.643, 0.143, 0.193, 0.098), .Dim=c(2,3)),
    SD_CA_DevL_npt=structure(.Data=c(0.080, 0.107, 0.237, 0.113, 0.683, 0.207), .Dim=c(2,3)),

    SD_HA_DevH_npt=structure(.Data=c(0.650, 0.148, 0.317, 0.129, 0.033, 0.026), .Dim=c(2,3)),
    SD_HA_DevM_npt=structure(.Data=c(0.150, 0.104, 0.643, 0.113, 0.207, 0.084), .Dim=c(2,3)),
    SD_HA_DevL_npt=structure(.Data=c(0.055, 0.089, 0.237, 0.113, 0.708, 0.188), .Dim=c(2,3)),

    SD_SA_DevH_npt=structure(.Data=c(0.625, 0.170, 0.303, 0.116, 0.072, 0.080), .Dim=c(2,3)),
    SD_SA_DevM_npt=structure(.Data=c(0.143, 0.127, 0.650, 0.126, 0.207, 0.073), .Dim=c(2,3)),
    SD_SA_DevL_npt=structure(.Data=c(0.055, 0.089, 0.295, 0.187, 0.650, 0.224), .Dim=c(2,3)),

    SD_RA_DevH_npt=structure(.Data=c(0.617, 0.186, 0.295, 0.118, 0.088, 0.101), .Dim=c(2,3)),
    SD_RA_DevM_npt=structure(.Data=c(0.179, 0.163, 0.614, 0.195, 0.207, 0.084), .Dim=c(2,3)),
    SD_RA_DevL_npt=structure(.Data=c(0.130, 0.202, 0.262, 0.131, 0.608, 0.276), .Dim=c(2,3)),

    SD_SCTPG_DevH_npt=structure(.Data=c(0.708, 0.159, 0.258, 0.136, 0.033, 0.026), .Dim=c(2,3)),
    SD_SCTPG_DevM_npt=structure(.Data=c(0.176, 0.115, 0.612, 0.179, 0.212, 0.086), .Dim=c(2,3)),
    SD_SCTPG_DevL_npt=structure(.Data=c(0.083, 0.093, 0.267, 0.082, 0.650, 0.148), .Dim=c(2,3)),

    SD_SITPG_DevH_npt=structure(.Data=c(0.708, 0.159, 0.258, 0.136, 0.033, 0.026), .Dim=c(2,3)),
    SD_SITPG_DevM_npt=structure(.Data=c(0.164, 0.099, 0.629, 0.138, 0.207, 0.079), .Dim=c(2,3)),
    SD_SITPG_DevL_npt=structure(.Data=c(0.058, 0.074, 0.258, 0.080, 0.683, 0.133), .Dim=c(2,3)),

    SD_SCTDG_DevH_npt=structure(.Data=c(0.750, 0.173, 0.225, 0.147, 0.025, 0.027), .Dim=c(2,3)),
    SD_SCTDG_DevM_npt=structure(.Data=c(0.136, 0.085, 0.700, 0.141, 0.164, 0.085), .Dim=c(2,3)),
    SD_SCTDG_DevL_npt=structure(.Data=c(0.050, 0.077, 0.200, 0.110, 0.750, 0.173), .Dim=c(2,3)),

    SD_SITDG_DevH_npt=structure(.Data=c(0.750, 0.173, 0.225, 0.147, 0.025, 0.027), .Dim=c(2,3)),
    SD_SITDG_DevM_npt=structure(.Data=c(0.136, 0.085, 0.686, 0.146, 0.179, 0.081), .Dim=c(2,3)),
    SD_SITDG_DevL_npt=structure(.Data=c(0.050, 0.077, 0.225, 0.099, 0.725, 0.157), .Dim=c(2,3)),

    SD_SQTDG_DevH_npt=structure(.Data=c(0.708, 0.159, 0.258, 0.136, 0.033, 0.026), .Dim=c(2,3)),
    SD_SQTDG_DevM_npt=structure(.Data=c(0.200, 0.126, 0.621, 0.168, 0.179, 0.064), .Dim=c(2,3)),
    SD_SQTDG_DevL_npt=structure(.Data=c(0.083, 0.093, 0.233, 0.103, 0.683, 0.181), .Dim=c(2,3)),

    SD_SATDG_DevH_npt=structure(.Data=c(0.683, 0.133, 0.283, 0.113, 0.033, 0.026), .Dim=c(2,3)),
    SD_SATDG_DevM_npt=structure(.Data=c(0.193, 0.124, 0.650, 0.161, 0.157, 0.061), .Dim=c(2,3)),
    SD_SATDG_DevL_npt=structure(.Data=c(0.083, 0.093, 0.258, 0.080, 0.658, 0.153), .Dim=c(2,3)),

    SD_CM_DevH_npt=structure(.Data=c(0.614, 0.143, 0.297, 0.027, 0.089, 0.121), .Dim=c(2,3)),
    SD_CM_DevM_npt=structure(.Data=c(0.183, 0.090, 0.605, 0.164, 0.212, 0.091), .Dim=c(2,3)),
    SD_CM_DevL_npt=structure(.Data=c(0.139, 0.127, 0.272, 0.085, 0.589, 0.193), .Dim=c(2,3)),

    SD_RaA_DevH_npt=structure(.Data=c(0.631, 0.232, 0.247, 0.116, 0.122, 0.142), .Dim=c(2,3)),
    SD_RaA_DevM_npt=structure(.Data=c(0.226, 0.139, 0.598, 0.197, 0.176, 0.090), .Dim=c(2,3)),
    SD_RaA_DevL_npt=structure(.Data=c(0.124, 0.144, 0.229, 0.114, 0.647, 0.245), .Dim=c(2,3)),

    # state of attribute: 1 -> High, 2 -> Medium, 3 -> Low
    SD_SAD_state=2, SD_SDD_state=2, SD_TA_state=2, SD_CA_state=3, SD_HA_state=2,
    SD_SA_state=3, SD_RA_state=3, SD_SCTPG_state=2, SD_SITPG_state=2, SD_SCTDG_state=2,
    SD_SITDG_state=2, SD_SQTDG_state=2, SD_SATDG_state=2, SD_CM_state=2, SD_RaA_state=2,
    generic_SD_SAD_state=2, generic_SD_SDD_state=2, generic_SD_TA_state=2, generic_SD_CA_state=2, generic_SD_HA_state=2, generic_SD_SA_state=2, generic_SD_RA_state=2, generic_SD_SCTPG_state=2, generic_SD_SITPG_state=2, generic_SD_SCTDG_state=2, generic_SD_SITDG_state=2, generic_SD_SQTDG_state=2, generic_SD_SATDG_state=2, generic_SD_CM_state=2, generic_SD_RaA_state=2,


    # V&V Attribute model - Design phase

    # node probability tables of attribute: P(attribute state|VV=H/M/L)
    # Dimension: row, col
    # row represents attribute states (H/M/L), column represents mu and sigma
    # (1,1) (2,1) (1,2) (2,2) (1,3) (2,3)
    SD_DE_VVH_npt=structure(.Data=c(0.817, 0.129, 0.167, 0.103, 0.017, 0.026), .Dim=c(2,3)),
    SD_DE_VVM_npt=structure(.Data=c(0.171, 0.095, 0.657, 0.098, 0.171, 0.049), .Dim=c(2,3)),
    SD_DE_VVL_npt=structure(.Data=c(0.055, 0.089, 0.212, 0.125, 0.733, 0.204), .Dim=c(2,3)),

    SD_IAVV_VVH_npt=structure(.Data=c(0.692, 0.102, 0.267, 0.082, 0.042, 0.020), .Dim=c(2,3)),
    SD_IAVV_VVM_npt=structure(.Data=c(0.157, 0.098, 0.686, 0.107, 0.157, 0.053), .Dim=c(2,3)),
    SD_IAVV_VVL_npt=structure(.Data=c(0.088, 0.101, 0.245, 0.116, 0.667, 0.204), .Dim=c(2,3)),

    SD_TAVV_VVH_npt=structure(.Data=c(0.733, 0.204, 0.212, 0.125, 0.055, 0.089), .Dim=c(2,3)),
    SD_TAVV_VVM_npt=structure(.Data=c(0.200, 0.153, 0.629, 0.147, 0.171, 0.070), .Dim=c(2,3)),
    SD_TAVV_VVL_npt=structure(.Data=c(0.050, 0.077, 0.200, 0.110, 0.750, 0.173), .Dim=c(2,3)),

    SD_CAVV_VVH_npt=structure(.Data=c(0.617, 0.157, 0.292, 0.111, 0.092, 0.086), .Dim=c(2,3)),
    SD_CAVV_VVM_npt=structure(.Data=c(0.164, 0.099, 0.614, 0.135, 0.221, 0.064), .Dim=c(2,3)),
    SD_CAVV_VVL_npt=structure(.Data=c(0.113, 0.108, 0.245, 0.116, 0.642, 0.215), .Dim=c(2,3)),

    SD_HAVV_VVH_npt=structure(.Data=c(0.617, 0.157, 0.292, 0.111, 0.092, 0.086), .Dim=c(2,3)),
    SD_HAVV_VVM_npt=structure(.Data=c(0.157, 0.093, 0.629, 0.125, 0.214, 0.063), .Dim=c(2,3)),
    SD_HAVV_VVL_npt=structure(.Data=c(0.088, 0.101, 0.245, 0.116, 0.667, 0.204), .Dim=c(2,3)),

    SD_SAVV_VVH_npt=structure(.Data=c(0.617, 0.157, 0.292, 0.111, 0.092, 0.086), .Dim=c(2,3)),
    SD_SAVV_VVM_npt=structure(.Data=c(0.164, 0.103, 0.643, 0.113, 0.193, 0.073), .Dim=c(2,3)),
    SD_SAVV_VVL_npt=structure(.Data=c(0.083, 0.093, 0.233, 0.103, 0.683, 0.181), .Dim=c(2,3)),

    SD_RAVV_VVH_npt=structure(.Data=c(0.592, 0.163, 0.292, 0.111, 0.117, 0.093), .Dim=c(2,3)),
    SD_RAVV_VVM_npt=structure(.Data=c(0.193, 0.162, 0.607, 0.224, 0.200, 0.112), .Dim=c(2,3)),
    SD_RAVV_VVL_npt=structure(.Data=c(0.163, 0.193, 0.245, 0.116, 0.592, 0.280), .Dim=c(2,3)),

    SD_VVSCTPG_VVH_npt=structure(.Data=c(0.683, 0.181, 0.258, 0.136, 0.058, 0.074), .Dim=c(2,3)),
    SD_VVSCTPG_VVM_npt=structure(.Data=c(0.193, 0.073, 0.643, 0.113, 0.164, 0.063), .Dim=c(2,3)),
    SD_VVSCTPG_VVL_npt=structure(.Data=c(0.092, 0.086, 0.267, 0.082, 0.642, 0.146), .Dim=c(2,3)),

    SD_VVSITPG_VVH_npt=structure(.Data=c(0.683, 0.181, 0.258, 0.136, 0.058, 0.074), .Dim=c(2,3)),
    SD_VVSITPG_VVM_npt=structure(.Data=c(0.186, 0.069, 0.657, 0.098, 0.157, 0.053), .Dim=c(2,3)),
    SD_VVSITPG_VVL_npt=structure(.Data=c(0.092, 0.086, 0.267, 0.082, 0.642, 0.146), .Dim=c(2,3)),

    SD_VVSCTDG_VVH_npt=structure(.Data=c(0.725, 0.199, 0.225, 0.147, 0.050, 0.077), .Dim=c(2,3)),
    SD_VVSCTDG_VVM_npt=structure(.Data=c(0.171, 0.111, 0.686, 0.107, 0.129, 0.049), .Dim=c(2,3)),
    SD_VVSCTDG_VVL_npt=structure(.Data=c(0.088, 0.101, 0.245, 0.116, 0.667, 0.204), .Dim=c(2,3)),

    SD_VVSITDG_VVH_npt=structure(.Data=c(0.767, 0.207, 0.192, 0.150, 0.042, 0.080), .Dim=c(2,3)),
    SD_VVSITDG_VVM_npt=structure(.Data=c(0.186, 0.135, 0.664, 0.138, 0.150, 0.050), .Dim=c(2,3)),
    SD_VVSITDG_VVL_npt=structure(.Data=c(0.080, 0.107, 0.212, 0.125, 0.708, 0.225), .Dim=c(2,3)),

    SD_VVSQTDG_VVH_npt=structure(.Data=c(0.725, 0.199, 0.225, 0.147, 0.050, 0.077), .Dim=c(2,3)),
    SD_VVSQTDG_VVM_npt=structure(.Data=c(0.214, 0.146, 0.614, 0.144, 0.171, 0.039), .Dim=c(2,3)),
    SD_VVSQTDG_VVL_npt=structure(.Data=c(0.088, 0.101, 0.245, 0.116, 0.667, 0.204), .Dim=c(2,3)),

    SD_VVSATDG_VVH_npt=structure(.Data=c(0.708, 0.159, 0.233, 0.103, 0.058, 0.074), .Dim=c(2,3)),
    SD_VVSATDG_VVM_npt=structure(.Data=c(0.200, 0.129, 0.636, 0.125, 0.164, 0.048), .Dim=c(2,3)),
    SD_VVSATDG_VVL_npt=structure(.Data=c(0.088, 0.101, 0.245, 0.116, 0.667, 0.204), .Dim=c(2,3)),

    SD_CMVV_VVH_npt=structure(.Data=c(0.547, 0.128, 0.306, 0.014, 0.147, 0.117), .Dim=c(2,3)),
    SD_CMVV_VVM_npt=structure(.Data=c(0.212, 0.122, 0.590, 0.169, 0.198, 0.100), .Dim=c(2,3)),
    SD_CMVV_VVL_npt=structure(.Data=c(0.169, 0.123, 0.284, 0.094, 0.547, 0.203), .Dim=c(2,3)),

    SD_RaAVV_VVH_npt=structure(.Data=c(0.656, 0.223, 0.239, 0.108, 0.106, 0.134), .Dim=c(2,3)),
    SD_RaAVV_VVM_npt=structure(.Data=c(0.219, 0.139, 0.612, 0.193, 0.169, 0.085), .Dim=c(2,3)),
    SD_RaAVV_VVL_npt=structure(.Data=c(0.136, 0.139, 0.251, 0.119, 0.614, 0.246), .Dim=c(2,3)),

    SD_VVASRG_VVH_npt=structure(.Data=c(0.642, 0.146, 0.267, 0.082, 0.092, 0.086), .Dim=c(2,3)),
    SD_VVASRG_VVM_npt=structure(.Data=c(0.193, 0.110, 0.657, 0.140, 0.150, 0.065), .Dim=c(2,3)),
    SD_VVASRG_VVL_npt=structure(.Data=c(0.080, 0.088, 0.220, 0.098, 0.700, 0.164), .Dim=c(2,3)),

    # state of attribute: 1 -> High, 2 -> Medium, 3 -> Low
    SD_DE_state=2, SD_IAVV_state=2, SD_TAVV_state=2, SD_CAVV_state=3, SD_HAVV_state=3,
    SD_SAVV_state=3, SD_RAVV_state=3, SD_VVSCTPG_state=3, SD_VVSITPG_state=3, SD_VVSCTDG_state=3,
    SD_VVSITDG_state=3, SD_VVSQTDG_state=3, SD_VVSATDG_state=3, SD_CMVV_state=2, SD_RaAVV_state=2,
    SD_VVASRG_state=2,
    generic_SD_DE_state=2, generic_SD_IAVV_state=2, generic_SD_TAVV_state=2, generic_SD_CAVV_state=2, generic_SD_HAVV_state=2, generic_SD_SAVV_state=2, generic_SD_RAVV_state=2, generic_SD_VVSCTPG_state=2, generic_SD_VVSITPG_state=2, generic_SD_VVSCTDG_state=2, generic_SD_VVSITDG_state=2, generic_SD_VVSQTDG_state=2, generic_SD_VVSATDG_state=2, generic_SD_CMVV_state=2, generic_SD_RaAVV_state=2, generic_SD_VVASRG_state=2,


    # Submodel - Design phase

    # node probability tables of DDP_current: P(DDP_current|VV=H/M/L)
    # Dimension: row, col
    # row represents Complexity (H/M/L), column represents alpha and beta
    # (1,1) (2,1) (1,2) (2,2) (1,3) (2,3)
    SD_VVH_DDP_current_npt=structure(.Data=c(3.621, 1.789, 5.446, 1.341, 3.336, 0.524), .Dim=c(2,3)),
    SD_VVM_DDP_current_npt=structure(.Data=c(2.671, 2.264, 4.244, 1.817, 3.930, 1.024), .Dim=c(2,3)),
    SD_VVL_DDP_current_npt=structure(.Data=c(1.382, 2.044, 1.755, 1.712, 2.269, 1.748), .Dim=c(2,3)),

    SD_VVH_DDP_previous_npt=structure(.Data=c(1.3095, 1.7345, 1.2688, 1.0514, 1.0873, 0.8117), .Dim=c(2,3)),
    SD_VVM_DDP_previous_npt=structure(.Data=c(1.0128, 2.1429, 1.1353, 1.7571, 1.2079, 1.4215), .Dim=c(2,3)),
    SD_VVL_DDP_previous_npt=structure(.Data=c(1.1601, 6.0078, 1.5224, 6.3937, 1.9101, 6.7609), .Dim=c(2,3)),

    # posterior probability of Dev/V&V qualities in SR phase
    # SD_DevH=0, SD_DevM=1, SD_DevL=0,
    # SD_VVH=0, SD_VVM=0, SD_VVL = 1,

    # number of function points (same in all phases)
    SD_FP=56,
    generic_SD_FP=50,


    # Dev Attribute model - Implementation phase

    # node probability tables of attribute: P(attribute state|Dev=H/M/L)
    # Dimension: row, col
    # row represents attribute states (H/M/L), column represents mu and sigma
    # (1,1) (2,1) (1,2) (2,2) (1,3) (2,3)
    IM_SCaSCDG_DevH_npt=structure(.Data=c(0.667, 0.160, 0.275, 0.117, 0.058, 0.074), .Dim=c(2,3)),
    IM_SCaSCDG_DevM_npt=structure(.Data=c(0.150, 0.087, 0.650, 0.104, 0.200, 0.096), .Dim=c(2,3)),
    IM_SCaSCDG_DevL_npt=structure(.Data=c(0.055, 0.089, 0.237, 0.113, 0.708, 0.188), .Dim=c(2,3)),

    IM_TA_DevH_npt=structure(.Data=c(0.600, 0.176, 0.303, 0.116, 0.097, 0.094), .Dim=c(2,3)),
    IM_TA_DevM_npt=structure(.Data=c(0.200, 0.153, 0.600, 0.126, 0.200, 0.076), .Dim=c(2,3)),
    IM_TA_DevL_npt=structure(.Data=c(0.080, 0.107, 0.237, 0.113, 0.683, 0.207), .Dim=c(2,3)),

    IM_CA_DevH_npt=structure(.Data=c(0.658, 0.196, 0.258, 0.136, 0.083, 0.093), .Dim=c(2,3)),
    IM_CA_DevM_npt=structure(.Data=c(0.164, 0.131, 0.621, 0.135, 0.214, 0.075), .Dim=c(2,3)),
    IM_CA_DevL_npt=structure(.Data=c(0.088, 0.101, 0.245, 0.116, 0.667, 0.204), .Dim=c(2,3)),

    IM_HA_DevH_npt=structure(.Data=c(0.658, 0.153, 0.283, 0.113, 0.058, 0.074), .Dim=c(2,3)),
    IM_HA_DevM_npt=structure(.Data=c(0.157, 0.127, 0.636, 0.125, 0.207, 0.073), .Dim=c(2,3)),
    IM_HA_DevL_npt=structure(.Data=c(0.055, 0.089, 0.228, 0.113, 0.717, 0.191), .Dim=c(2,3)),

    IM_SA_DevH_npt=structure(.Data=c(0.642, 0.146, 0.300, 0.114, 0.058, 0.074), .Dim=c(2,3)),
    IM_SA_DevM_npt=structure(.Data=c(0.143, 0.098, 0.657, 0.098, 0.200, 0.082), .Dim=c(2,3)),
    IM_SA_DevL_npt=structure(.Data=c(0.055, 0.089, 0.212, 0.125, 0.733, 0.204), .Dim=c(2,3)),

    IM_RA_DevH_npt=structure(.Data=c(0.617, 0.160, 0.292, 0.111, 0.092, 0.092), .Dim=c(2,3)),
    IM_RA_DevM_npt=structure(.Data=c(0.221, 0.208, 0.586, 0.210, 0.193, 0.117), .Dim=c(2,3)),
    IM_RA_DevL_npt=structure(.Data=c(0.147, 0.239, 0.245, 0.116, 0.608, 0.311), .Dim=c(2,3)),

    IM_CTCG_DevH_npt=structure(.Data=c(0.750, 0.173, 0.225, 0.147, 0.025, 0.027), .Dim=c(2,3)),
    IM_CTCG_DevM_npt=structure(.Data=c(0.164, 0.085, 0.643, 0.113, 0.193, 0.045), .Dim=c(2,3)),
    IM_CTCG_DevL_npt=structure(.Data=c(0.083, 0.093, 0.233, 0.103, 0.683, 0.181), .Dim=c(2,3)),

    IM_SITCG_DevH_npt=structure(.Data=c(0.750, 0.173, 0.225, 0.147, 0.025, 0.027), .Dim=c(2,3)),
    IM_SITCG_DevM_npt=structure(.Data=c(0.164, 0.085, 0.643, 0.113, 0.193, 0.045), .Dim=c(2,3)),
    IM_SITCG_DevL_npt=structure(.Data=c(0.058, 0.074, 0.233, 0.103, 0.708, 0.159), .Dim=c(2,3)),

    IM_SQTCG_DevH_npt=structure(.Data=c(0.750, 0.173, 0.225, 0.147, 0.025, 0.027), .Dim=c(2,3)),
    IM_SQTCG_DevM_npt=structure(.Data=c(0.171, 0.091, 0.629, 0.125, 0.200, 0.050), .Dim=c(2,3)),
    IM_SQTCG_DevL_npt=structure(.Data=c(0.058, 0.074, 0.233, 0.103, 0.708, 0.159), .Dim=c(2,3)),

    IM_SATCG_DevH_npt=structure(.Data=c(0.692, 0.180, 0.258, 0.136, 0.050, 0.077), .Dim=c(2,3)),
    IM_SATCG_DevM_npt=structure(.Data=c(0.207, 0.127, 0.593, 0.148, 0.200, 0.058), .Dim=c(2,3)),
    IM_SATCG_DevL_npt=structure(.Data=c(0.097, 0.139, 0.231, 0.105, 0.672, 0.226), .Dim=c(2,3)),

    IM_SCTPG_DevH_npt=structure(.Data=c(0.708, 0.159, 0.258, 0.136, 0.033, 0.026), .Dim=c(2,3)),
    IM_SCTPG_DevM_npt=structure(.Data=c(0.171, 0.076, 0.657, 0.098, 0.171, 0.076), .Dim=c(2,3)),
    IM_SCTPG_DevL_npt=structure(.Data=c(0.083, 0.093, 0.233, 0.103, 0.683, 0.181), .Dim=c(2,3)),

    IM_SITPG_DevH_npt=structure(.Data=c(0.750, 0.173, 0.225, 0.147, 0.025, 0.027), .Dim=c(2,3)),
    IM_SITPG_DevM_npt=structure(.Data=c(0.186, 0.069, 0.657, 0.098, 0.157, 0.053), .Dim=c(2,3)),
    IM_SITPG_DevL_npt=structure(.Data=c(0.092, 0.086, 0.267, 0.082, 0.642, 0.146), .Dim=c(2,3)),

    IM_SQTPG_DevH_npt=structure(.Data=c(0.708, 0.159, 0.258, 0.136, 0.033, 0.026), .Dim=c(2,3)),
    IM_SQTPG_DevM_npt=structure(.Data=c(0.200, 0.076, 0.629, 0.125, 0.171, 0.070), .Dim=c(2,3)),
    IM_SQTPG_DevL_npt=structure(.Data=c(0.108, 0.102, 0.233, 0.103, 0.658, 0.196), .Dim=c(2,3)),

    IM_CM_DevH_npt=structure(.Data=c(0.564, 0.149, 0.297, 0.027, 0.139, 0.127), .Dim=c(2,3)),
    IM_CM_DevM_npt=structure(.Data=c(0.212, 0.086, 0.548, 0.143, 0.240, 0.075), .Dim=c(2,3)),
    IM_CM_DevL_npt=structure(.Data=c(0.164, 0.120, 0.272, 0.085, 0.564, 0.193), .Dim=c(2,3)),

    IM_RaA_DevH_npt=structure(.Data=c(0.589, 0.193, 0.272, 0.085, 0.139, 0.127), .Dim=c(2,3)),
    IM_RaA_DevM_npt=structure(.Data=c(0.183, 0.121, 0.619, 0.186, 0.198, 0.100), .Dim=c(2,3)),
    IM_RaA_DevL_npt=structure(.Data=c(0.141, 0.129, 0.271, 0.097, 0.589, 0.203), .Dim=c(2,3)),

    IM_SCTE_DevH_npt=structure(.Data=c(0.817, 0.129, 0.167, 0.103, 0.017, 0.026), .Dim=c(2,3)),
    IM_SCTE_DevM_npt=structure(.Data=c(0.171, 0.076, 0.700, 0.100, 0.129, 0.049), .Dim=c(2,3)),
    IM_SCTE_DevL_npt=structure(.Data=c(0.072, 0.111, 0.203, 0.119, 0.725, 0.223), .Dim=c(2,3)),

    # state of attribute: 1 -> High, 2 -> Medium, 3 -> Low
    IM_SCaSCDG_state=3, IM_TA_state=2, IM_CA_state=3, IM_HA_state=3, IM_SA_state=3,
    IM_RA_state=3, IM_CTCG_state=2, IM_SITCG_state=2, IM_SQTCG_state=2, IM_SATCG_state=2,
    IM_SCTPG_state=2, IM_SITPG_state=2, IM_SQTPG_state=2, IM_CM_state=2, IM_RaA_state=2,
    IM_SCTE_state=2,
    generic_IM_SCaSCDG_state=2, generic_IM_TA_state=2, generic_IM_CA_state=2, generic_IM_HA_state=2, generic_IM_SA_state=2, generic_IM_RA_state=2, generic_IM_CTCG_state=2, generic_IM_SITCG_state=2, generic_IM_SQTCG_state=2, generic_IM_SATCG_state=2, generic_IM_SCTPG_state=2, generic_IM_SITPG_state=2, generic_IM_SQTPG_state=2, generic_IM_CM_state=2, generic_IM_RaA_state=2, generic_IM_SCTE_state=2,


    # V&V Attribute model - Implementation phase

    # node probability tables of attribute: P(attribute state|VV=H/M/L)
    # Dimension: row, col
    # row represents attribute states (H/M/L), column represents mu and sigma
    # (1,1) (2,1) (1,2) (2,2) (1,3) (2,3)
    IM_SCaSCDE_VVH_npt=structure(.Data=c(0.708, 0.159, 0.258, 0.136, 0.033, 0.026), .Dim=c(2,3)),
    IM_SCaSCDE_VVM_npt=structure(.Data=c(0.193, 0.124, 0.607, 0.117, 0.200, 0.065), .Dim=c(2,3)),
    IM_SCaSCDE_VVL_npt=structure(.Data=c(0.058, 0.074, 0.233, 0.103, 0.708, 0.159), .Dim=c(2,3)),

    IM_IAVV_VVH_npt=structure(.Data=c(0.617, 0.157, 0.292, 0.111, 0.092, 0.086), .Dim=c(2,3)),
    IM_IAVV_VVM_npt=structure(.Data=c(0.207, 0.127, 0.593, 0.148, 0.200, 0.058), .Dim=c(2,3)),
    IM_IAVV_VVL_npt=structure(.Data=c(0.097, 0.094, 0.278, 0.092, 0.625, 0.170), .Dim=c(2,3)),

    IM_TAVV_VVH_npt=structure(.Data=c(0.692, 0.188, 0.245, 0.116, 0.063, 0.085), .Dim=c(2,3)),
    IM_TAVV_VVM_npt=structure(.Data=c(0.171, 0.107, 0.629, 0.125, 0.200, 0.076), .Dim=c(2,3)),
    IM_TAVV_VVL_npt=structure(.Data=c(0.075, 0.099, 0.200, 0.110, 0.725, 0.199), .Dim=c(2,3)),

    IM_CAVV_VVH_npt=structure(.Data=c(0.617, 0.157, 0.292, 0.111, 0.092, 0.086), .Dim=c(2,3)),
    IM_CAVV_VVM_npt=structure(.Data=c(0.171, 0.107, 0.629, 0.125, 0.200, 0.076), .Dim=c(2,3)),
    IM_CAVV_VVL_npt=structure(.Data=c(0.122, 0.099, 0.278, 0.092, 0.600, 0.176), .Dim=c(2,3)),

    IM_HAVV_VVH_npt=structure(.Data=c(0.642, 0.146, 0.292, 0.111, 0.067, 0.068), .Dim=c(2,3)),
    IM_HAVV_VVM_npt=structure(.Data=c(0.164, 0.103, 0.643, 0.113, 0.193, 0.073), .Dim=c(2,3)),
    IM_HAVV_VVL_npt=structure(.Data=c(0.088, 0.101, 0.245, 0.116, 0.667, 0.204), .Dim=c(2,3)),

    IM_SAVV_VVH_npt=structure(.Data=c(0.642, 0.146, 0.292, 0.111, 0.067, 0.068), .Dim=c(2,3)),
    IM_SAVV_VVM_npt=structure(.Data=c(0.164, 0.103, 0.643, 0.113, 0.193, 0.073), .Dim=c(2,3)),
    IM_SAVV_VVL_npt=structure(.Data=c(0.097, 0.094, 0.278, 0.092, 0.625, 0.170), .Dim=c(2,3)),

    IM_RAVV_VVH_npt=structure(.Data=c(0.633, 0.147, 0.292, 0.111, 0.075, 0.069), .Dim=c(2,3)),
    IM_RAVV_VVM_npt=structure(.Data=c(0.236, 0.206, 0.593, 0.205, 0.171, 0.081), .Dim=c(2,3)),
    IM_RAVV_VVL_npt=structure(.Data=c(0.188, 0.221, 0.278, 0.092, 0.533, 0.271), .Dim=c(2,3)),

    IM_VVSCTCG_VVH_npt=structure(.Data=c(0.750, 0.173, 0.225, 0.147, 0.025, 0.027), .Dim=c(2,3)),
    IM_VVSCTCG_VVM_npt=structure(.Data=c(0.193, 0.073, 0.643, 0.113, 0.164, 0.063), .Dim=c(2,3)),
    IM_VVSCTCG_VVL_npt=structure(.Data=c(0.088, 0.101, 0.245, 0.116, 0.667, 0.204), .Dim=c(2,3)),

    IM_VVSITCG_VVH_npt=structure(.Data=c(0.750, 0.173, 0.225, 0.147, 0.025, 0.027), .Dim=c(2,3)),
    IM_VVSITCG_VVM_npt=structure(.Data=c(0.193, 0.073, 0.643, 0.113, 0.164, 0.063), .Dim=c(2,3)),
    IM_VVSITCG_VVL_npt=structure(.Data=c(0.088, 0.101, 0.245, 0.116, 0.667, 0.204), .Dim=c(2,3)),

    IM_VVSQTCG_VVH_npt=structure(.Data=c(0.708, 0.159, 0.258, 0.136, 0.033, 0.026), .Dim=c(2,3)),
    IM_VVSQTCG_VVM_npt=structure(.Data=c(0.193, 0.073, 0.643, 0.113, 0.164, 0.063), .Dim=c(2,3)),
    IM_VVSQTCG_VVL_npt=structure(.Data=c(0.102, 0.101, 0.290, 0.099, 0.608, 0.188), .Dim=c(2,3)),

    IM_VVSATCG_VVH_npt=structure(.Data=c(0.642, 0.146, 0.292, 0.111, 0.067, 0.068), .Dim=c(2,3)),
    IM_VVSATCG_VVM_npt=structure(.Data=c(0.207, 0.130, 0.636, 0.160, 0.157, 0.061), .Dim=c(2,3)),
    IM_VVSATCG_VVL_npt=structure(.Data=c(0.149, 0.133, 0.296, 0.101, 0.556, 0.216), .Dim=c(2,3)),

    IM_VVSCTPG_VVH_npt=structure(.Data=c(0.708, 0.159, 0.258, 0.136, 0.033, 0.026), .Dim=c(2,3)),
    IM_VVSCTPG_VVM_npt=structure(.Data=c(0.207, 0.130, 0.636, 0.160, 0.157, 0.061), .Dim=c(2,3)),
    IM_VVSCTPG_VVL_npt=structure(.Data=c(0.117, 0.093, 0.267, 0.082, 0.617, 0.157), .Dim=c(2,3)),

    IM_VVSITPG_VVH_npt=structure(.Data=c(0.708, 0.159, 0.258, 0.136, 0.033, 0.026), .Dim=c(2,3)),
    IM_VVSITPG_VVM_npt=structure(.Data=c(0.207, 0.130, 0.636, 0.160, 0.157, 0.061), .Dim=c(2,3)),
    IM_VVSITPG_VVL_npt=structure(.Data=c(0.117, 0.093, 0.267, 0.082, 0.617, 0.157), .Dim=c(2,3)),

    IM_VVSQTPG_VVH_npt=structure(.Data=c(0.708, 0.159, 0.258, 0.136, 0.033, 0.026), .Dim=c(2,3)),
    IM_VVSQTPG_VVM_npt=structure(.Data=c(0.207, 0.130, 0.636, 0.160, 0.157, 0.061), .Dim=c(2,3)),
    IM_VVSQTPG_VVL_npt=structure(.Data=c(0.117, 0.093, 0.267, 0.082, 0.617, 0.157), .Dim=c(2,3)),

    IM_VVSCTE_VVH_npt=structure(.Data=c(0.817, 0.129, 0.167, 0.103, 0.017, 0.026), .Dim=c(2,3)),
    IM_VVSCTE_VVM_npt=structure(.Data=c(0.164, 0.103, 0.700, 0.173, 0.136, 0.085), .Dim=c(2,3)),
    IM_VVSCTE_VVL_npt=structure(.Data=c(0.080, 0.107, 0.212, 0.125, 0.708, 0.225), .Dim=c(2,3)),

    IM_CMVV_VVH_npt=structure(.Data=c(0.547, 0.128, 0.306, 0.014, 0.147, 0.117), .Dim=c(2,3)),
    IM_CMVV_VVM_npt=structure(.Data=c(0.190, 0.117, 0.569, 0.176, 0.240, 0.115), .Dim=c(2,3)),
    IM_CMVV_VVL_npt=structure(.Data=c(0.169, 0.123, 0.284, 0.094, 0.547, 0.203), .Dim=c(2,3)),

    IM_RaAVV_VVH_npt=structure(.Data=c(0.656, 0.223, 0.239, 0.108, 0.106, 0.134), .Dim=c(2,3)),
    IM_RaAVV_VVM_npt=structure(.Data=c(0.219, 0.139, 0.612, 0.193, 0.169, 0.085), .Dim=c(2,3)),
    IM_RaAVV_VVL_npt=structure(.Data=c(0.136, 0.139, 0.251, 0.119, 0.614, 0.246), .Dim=c(2,3)),

    IM_VVASRG_VVH_npt=structure(.Data=c(0.667, 0.129, 0.267, 0.082, 0.067, 0.068), .Dim=c(2,3)),
    IM_VVASRG_VVM_npt=structure(.Data=c(0.214, 0.146, 0.629, 0.168, 0.157, 0.045), .Dim=c(2,3)),
    IM_VVASRG_VVL_npt=structure(.Data=c(0.102, 0.101, 0.290, 0.099, 0.608, 0.188), .Dim=c(2,3)),

    # state of attribute: 1 -> High, 2 -> Medium, 3 -> Low
    IM_SCaSCDE_state=3, IM_IAVV_state=2, IM_TAVV_state=2, IM_CAVV_state=3, IM_HAVV_state=3,
    IM_SAVV_state=3, IM_RAVV_state=3, IM_VVSCTCG_state=3, IM_VVSITCG_state=3, IM_VVSQTCG_state=3,
    IM_VVSATCG_state=3, IM_VVSCTPG_state=3, IM_VVSITPG_state=3, IM_VVSQTPG_state=3, IM_VVSCTE_state=3,
    IM_CMVV_state=2, IM_RaAVV_state=2, IM_VVASRG_state=3,
    generic_IM_SCaSCDE_state=2, generic_IM_IAVV_state=2, generic_IM_TAVV_state=2, generic_IM_CAVV_state=2, generic_IM_HAVV_state=2, generic_IM_SAVV_state=2, generic_IM_RAVV_state=2, generic_IM_VVSCTCG_state=2, generic_IM_VVSITCG_state=2, generic_IM_VVSQTCG_state=2, generic_IM_VVSATCG_state=2, generic_IM_VVSCTPG_state=2, generic_IM_VVSITPG_state=2, generic_IM_VVSQTPG_state=2, generic_IM_VVSCTE_state=2, generic_IM_CMVV_state=2, generic_IM_RaAVV_state=2, generic_IM_VVASRG_state=2,


    # Submodel - Implementation phase

    # node probability tables of DDP_current: P(DDP_current|VV=H/M/L)
    # Dimension: row, col
    # row represents Complexity (H/M/L), column represents alpha and beta
    # (1,1) (2,1) (1,2) (2,2) (1,3) (2,3)
    IM_VVH_DDP_current_npt=structure(.Data=c(2.255, 1.225, 4.730, 1.051, 3.836, 0.410), .Dim=c(2,3)),
    IM_VVM_DDP_current_npt=structure(.Data=c(1.637, 1.272, 2.564, 1.073, 4.352, 0.832), .Dim=c(2,3)),
    IM_VVL_DDP_current_npt=structure(.Data=c(0.957, 1.176, 1.306, 1.050, 1.793, 1.181), .Dim=c(2,3)),

    # node probability tables of DDP_previous: P(DDP_previous|VV=H/M/L)
    # Dimension: row, col
    # row represents Complexity (H/M/L), column represents alpha and beta
    # (1,1) (2,1) (1,2) (2,2) (1,3) (2,3)
    IM_VVH_DDP_previous_npt=structure(.Data=c(1.7034, 2.0265, 1.9422, 1.4440, 1.6298, 0.9597), .Dim=c(2,3)),
    IM_VVM_DDP_previous_npt=structure(.Data=c(1.0646, 2.2064, 1.2764, 1.9959, 1.4098, 1.5461), .Dim=c(2,3)),
    IM_VVL_DDP_previous_npt=structure(.Data=c(1.1049, 4.0713, 1.4181, 4.2264, 2.1135, 5.1104), .Dim=c(2,3)),

    # posterior probability of Dev/V&V qualities in IM phase
    # IM_DevH=0, IM_DevM=1, IM_DevL=0,
    # IM_VVH=0, IM_VVM=0, IM_VVL=1,

    # number of function points (same in all phases)
    IM_FP=56,
    generic_IM_FP=50,


    # Dev Attribute model - Test phase

    # node probability tables of attribute: P(attribute state|Dev=H/M/L)
    # Dimension: row, col
    # row represents attribute states (H/M/L), column represents mu and sigma
    # (1,1) (2,1) (1,2) (2,2) (1,3) (2,3)
    ST_SITE_DevH_npt=structure(.Data=c(0.792, 0.174, 0.167, 0.103, 0.042, 0.080), .Dim=c(2,3)),
    ST_SITE_DevM_npt=structure(.Data=c(0.193, 0.110, 0.650, 0.150, 0.157, 0.061), .Dim=c(2,3)),
    ST_SITE_DevL_npt=structure(.Data=c(0.080, 0.107, 0.212, 0.125, 0.708, 0.225), .Dim=c(2,3)),

    ST_SQTE_DevH_npt=structure(.Data=c(0.750, 0.173, 0.200, 0.110, 0.050, 0.077), .Dim=c(2,3)),
    ST_SQTE_DevM_npt=structure(.Data=c(0.186, 0.063, 0.643, 0.127, 0.171, 0.070), .Dim=c(2,3)),
    ST_SQTE_DevL_npt=structure(.Data=c(0.075, 0.099, 0.200, 0.110, 0.725, 0.199), .Dim=c(2,3)),

    ST_SAPG_DevH_npt=structure(.Data=c(0.667, 0.129, 0.267, 0.082, 0.067, 0.068), .Dim=c(2,3)),
    ST_SAPG_DevM_npt=structure(.Data=c(0.171, 0.091, 0.643, 0.151, 0.186, 0.063), .Dim=c(2,3)),
    ST_SAPG_DevL_npt=structure(.Data=c(0.068, 0.074, 0.233, 0.103, 0.708, 0.159), .Dim=c(2,3)),

    ST_SATE_DevH_npt=structure(.Data=c(0.708, 0.159, 0.233, 0.103, 0.058, 0.074), .Dim=c(2,3)),
    ST_SATE_DevM_npt=structure(.Data=c(0.157, 0.093, 0.686, 0.157, 0.157, 0.073), .Dim=c(2,3)),
    ST_SATE_DevL_npt=structure(.Data=c(0.075, 0.099, 0.200, 0.110, 0.725, 0.199), .Dim=c(2,3)),

    ST_TA_DevH_npt=structure(.Data=c(0.625, 0.170, 0.278, 0.092, 0.097, 0.094), .Dim=c(2,3)),
    ST_TA_DevM_npt=structure(.Data=c(0.157, 0.127, 0.650, 0.150, 0.193, 0.084), .Dim=c(2,3)),
    ST_TA_DevL_npt=structure(.Data=c(0.055, 0.089, 0.212, 0.125, 0.733, 0.204), .Dim=c(2,3)),

    ST_HA_DevH_npt=structure(.Data=c(0.642, 0.146, 0.292, 0.111, 0.067, 0.068), .Dim=c(2,3)),
    ST_HA_DevM_npt=structure(.Data=c(0.157, 0.127, 0.636, 0.125, 0.207, 0.073), .Dim=c(2,3)),
    ST_HA_DevL_npt=structure(.Data=c(0.063, 0.085, 0.245, 0.116, 0.692, 0.188), .Dim=c(2,3)),

    ST_SA_DevH_npt=structure(.Data=c(0.617, 0.157, 0.292, 0.111, 0.092, 0.086), .Dim=c(2,3)),
    ST_SA_DevM_npt=structure(.Data=c(0.164, 0.131, 0.621, 0.135, 0.214, 0.075), .Dim=c(2,3)),
    ST_SA_DevL_npt=structure(.Data=c(0.055, 0.089, 0.253, 0.122, 0.692, 0.188), .Dim=c(2,3)),

    ST_RA_DevH_npt=structure(.Data=c(0.667, 0.160, 0.275, 0.117, 0.058, 0.074), .Dim=c(2,3)),
    ST_RA_DevM_npt=structure(.Data=c(0.243, 0.276, 0.593, 0.228, 0.164, 0.111), .Dim=c(2,3)),
    ST_RA_DevL_npt=structure(.Data=c(0.180, 0.317, 0.220, 0.109, 0.600, 0.348), .Dim=c(2,3)),

    ST_CM_DevH_npt=structure(.Data=c(0.522, 0.118, 0.306, 0.014, 0.172, 0.108), .Dim=c(2,3)),
    ST_CM_DevM_npt=structure(.Data=c(0.212, 0.086, 0.548, 0.143, 0.240, 0.075), .Dim=c(2,3)),
    ST_CM_DevL_npt=structure(.Data=c(0.164, 0.120, 0.272, 0.085, 0.564, 0.193), .Dim=c(2,3)),

    ST_RaA_DevH_npt=structure(.Data=c(0.539, 0.189, 0.272, 0.085, 0.189, 0.107), .Dim=c(2,3)),
    ST_RaA_DevM_npt=structure(.Data=c(0.190, 0.124, 0.605, 0.192, 0.205, 0.102), .Dim=c(2,3)),
    ST_RaA_DevL_npt=structure(.Data=c(0.124, 0.144, 0.229, 0.114, 0.647, 0.245), .Dim=c(2,3)),

    # state of attribute: 1 -> High, 2 -> Medium, 3 -> Low
    ST_SITE_state=2, ST_SQTE_state=2, ST_SAPG_state=2, ST_SATE_state=2, ST_TA_state=2,
    ST_HA_state=3, ST_SA_state=3, ST_RA_state=3, ST_CM_state=2, ST_RaA_state=2,
    generic_ST_SITE_state=2, generic_ST_SQTE_state=2, generic_ST_SAPG_state=2, generic_ST_SATE_state=2, generic_ST_TA_state=2, generic_ST_HA_state=2, generic_ST_SA_state=2, generic_ST_RA_state=2, generic_ST_CM_state=2, generic_ST_RaA_state=2,


    # V&V Attribute model - Test phase

    # node probability tables of attribute: P(attribute state|VV=H/M/L)
    # Dimension: row, col
    # row represents attribute states (H/M/L), column represents mu and sigma
    # (1,1) (2,1) (1,2) (2,2) (1,3) (2,3)
    ST_VVSITE_VVH_npt=structure(.Data=c(0.808, 0.143, 0.153, 0.086, 0.038, 0.072), .Dim=c(2,3)),
    ST_VVSITE_VVM_npt=structure(.Data=c(0.179, 0.129, 0.679, 0.195, 0.143, 0.084), .Dim=c(2,3)),
    ST_VVSITE_VVL_npt=structure(.Data=c(0.080, 0.107, 0.212, 0.125, 0.708, 0.225), .Dim=c(2,3)),

    ST_VVSQTE_VVH_npt=structure(.Data=c(0.767, 0.147, 0.187, 0.099, 0.047, 0.070), .Dim=c(2,3)),
    ST_VVSQTE_VVM_npt=structure(.Data=c(0.179, 0.129, 0.679, 0.195, 0.143, 0.084), .Dim=c(2,3)),
    ST_VVSQTE_VVL_npt=structure(.Data=c(0.088, 0.101, 0.245, 0.116, 0.667, 0.204), .Dim=c(2,3)),

    ST_VVSAPG_VVH_npt=structure(.Data=c(0.683, 0.108, 0.253, 0.082, 0.063, 0.061), .Dim=c(2,3)),
    ST_VVSAPG_VVM_npt=structure(.Data=c(0.193, 0.124, 0.636, 0.160, 0.171, 0.057), .Dim=c(2,3)),
    ST_VVSAPG_VVL_npt=structure(.Data=c(0.097, 0.094, 0.278, 0.092, 0.625, 0.170), .Dim=c(2,3)),

    ST_VVSATE_VVH_npt=structure(.Data=c(0.808, 0.143, 0.153, 0.086, 0.038, 0.072), .Dim=c(2,3)),
    ST_VVSATE_VVM_npt=structure(.Data=c(0.179, 0.129, 0.679, 0.195, 0.143, 0.084), .Dim=c(2,3)),
    ST_VVSATE_VVL_npt=structure(.Data=c(0.080, 0.107, 0.212, 0.125, 0.708, 0.225), .Dim=c(2,3)),

    ST_TAVV_VVH_npt=structure(.Data=c(0.650, 0.158, 0.278, 0.092, 0.072, 0.080), .Dim=c(2,3)),
    ST_TAVV_VVM_npt=structure(.Data=c(0.157, 0.098, 0.671, 0.125, 0.171, 0.076), .Dim=c(2,3)),
    ST_TAVV_VVL_npt=structure(.Data=c(0.083, 0.093, 0.233, 0.103, 0.683, 0.181), .Dim=c(2,3)),

    ST_HAVV_VVH_npt=structure(.Data=c(0.642, 0.146, 0.292, 0.111, 0.067, 0.068), .Dim=c(2,3)),
    ST_HAVV_VVM_npt=structure(.Data=c(0.157, 0.093, 0.629, 0.125, 0.214, 0.063), .Dim=c(2,3)),
    ST_HAVV_VVL_npt=structure(.Data=c(0.088, 0.101, 0.245, 0.116, 0.667, 0.204), .Dim=c(2,3)),

    ST_SAVV_VVH_npt=structure(.Data=c(0.642, 0.146, 0.292, 0.111, 0.067, 0.068), .Dim=c(2,3)),
    ST_SAVV_VVM_npt=structure(.Data=c(0.179, 0.129, 0.621, 0.135, 0.200, 0.065), .Dim=c(2,3)),
    ST_SAVV_VVL_npt=structure(.Data=c(0.088, 0.101, 0.245, 0.116, 0.667, 0.204), .Dim=c(2,3)),

    ST_RAVV_VVH_npt=structure(.Data=c(0.667, 0.160, 0.275, 0.117, 0.058, 0.074), .Dim=c(2,3)),
    ST_RAVV_VVM_npt=structure(.Data=c(0.264, 0.269, 0.579, 0.231, 0.157, 0.102), .Dim=c(2,3)),
    ST_RAVV_VVL_npt=structure(.Data=c(0.213, 0.304, 0.228, 0.113, 0.558, 0.341), .Dim=c(2,3)),

    ST_CMVV_VVH_npt=structure(.Data=c(0.614, 0.188, 0.272, 0.085, 0.114, 0.127), .Dim=c(2,3)),
    ST_CMVV_VVM_npt=structure(.Data=c(0.205, 0.117, 0.576, 0.172, 0.219, 0.092), .Dim=c(2,3)),
    ST_CMVV_VVL_npt=structure(.Data=c(0.194, 0.108, 0.284, 0.094, 0.522, 0.197), .Dim=c(2,3)),

    ST_RaAVV_VVH_npt=structure(.Data=c(0.631, 0.232, 0.239, 0.108, 0.131, 0.135), .Dim=c(2,3)),
    ST_RaAVV_VVM_npt=structure(.Data=c(0.226, 0.139, 0.598, 0.197, 0.176, 0.090), .Dim=c(2,3)),
    ST_RaAVV_VVL_npt=structure(.Data=c(0.144, 0.134, 0.251, 0.119, 0.606, 0.245), .Dim=c(2,3)),

    ST_VVASRG_VVH_npt=structure(.Data=c(0.667, 0.129, 0.267, 0.082, 0.067, 0.068), .Dim=c(2,3)),
    ST_VVASRG_VVM_npt=structure(.Data=c(0.221, 0.147, 0.614, 0.175, 0.164, 0.056), .Dim=c(2,3)),
    ST_VVASRG_VVL_npt=structure(.Data=c(0.127, 0.104, 0.290, 0.099, 0.583, 0.191), .Dim=c(2,3)),

    # state of attribute: 1 -> High, 2 -> Medium, 3 -> Low
    ST_VVSITE_state=3, ST_VVSQTE_state=3, ST_VVSAPG_state=3, ST_VVSATE_state=3, ST_TAVV_state=3,
    ST_HAVV_state=3, ST_SAVV_state=3, ST_RAVV_state=3, ST_CMVV_state=3, ST_RaAVV_state=3,
    ST_VVASRG_state=3,
    generic_ST_VVSITE_state=2, generic_ST_VVSQTE_state=2, generic_ST_VVSAPG_state=2, generic_ST_VVSATE_state=2, generic_ST_TAVV_state=2, generic_ST_HAVV_state=2, generic_ST_SAVV_state=2, generic_ST_RAVV_state=2, generic_ST_CMVV_state=2, generic_ST_RaAVV_state=2, generic_ST_VVASRG_state=2,


    # Submodel - Test phase

    # node probability tables of DDP_current: P(DDP_current|Dev=H/M/L, VV=H/M/L)
    # Dimension: row, col
    # row represents Complexity (H/M/L), column represents alpha and beta
    # (1,1) (2,1) (1,2) (2,2) (1,3) (2,3)
    ST_DevH_VVH_DDP_current_npt=structure(.Data=c(48.615, 11.761, 36.812, 11.989, 20.044, 9.475), .Dim=c(2,3)),
    ST_DevH_VVM_DDP_current_npt=structure(.Data=c(19.336, 7.330, 10.749, 6.233, 10.726, 7.557), .Dim=c(2,3)),
    ST_DevH_VVL_DDP_current_npt=structure(.Data=c(11.156, 6.261, 7.508, 6.189, 7.131, 7.104), .Dim=c(2,3)),

    ST_DevM_VVH_DDP_current_npt=structure(.Data=c(10.558, 1.279, 26.193, 5.173, 14.519, 4.744), .Dim=c(2,3)),
    ST_DevM_VVM_DDP_current_npt=structure(.Data=c(44.689, 11.028, 8.001, 3.376, 8.403, 4.477), .Dim=c(2,3)),
    ST_DevM_VVL_DDP_current_npt=structure(.Data=c(15.643, 6.342, 5.951, 3.796, 5.967, 4.726), .Dim=c(2,3)),

    ST_DevL_VVH_DDP_current_npt=structure(.Data=c(24.051, 2.022, 21.058, 3.308, 11.276, 3.138), .Dim=c(2,3)),
    ST_DevL_VVM_DDP_current_npt=structure(.Data=c(12.033, 2.493, 6.565, 2.431, 7.795, 3.703), .Dim=c(2,3)),
    ST_DevL_VVL_DDP_current_npt=structure(.Data=c(7.018, 2.497, 4.976, 2.840, 5.091, 3.647), .Dim=c(2,3)),

    # node probability tables of DDP_previous: P(DDP_previous|Dev=H/M/L, VV=H/M/L)
    # Dimension: row, col
    # row represents Complexity (H/M/L), column represents alpha and beta
    # (1,1) (2,1) (1,2) (2,2) (1,3) (2,3)
    ST_DevH_VVH_DDP_previous_npt=structure(.Data=c(64.1113, 15.6275, 37.8885, 12.2042, 15.0247, 6.7230), .Dim=c(2,3)),
    ST_DevH_VVM_DDP_previous_npt=structure(.Data=c(15.5834, 6.7702, 7.6550, 4.7268, 7.7542, 5.7831), .Dim=c(2,3)),
    ST_DevH_VVL_DDP_previous_npt=structure(.Data=c(8.3954, 4.8811, 5.7545, 4.8246, 5.5333, 5.5696), .Dim=c(2,3)),

    ST_DevM_VVH_DDP_previous_npt=structure(.Data=c(37.1415, 4.5249, 26.3886, 5.1372, 11.2259, 3.4673), .Dim=c(2,3)),
    ST_DevM_VVM_DDP_previous_npt=structure(.Data=c(7.3323, 2.5763, 5.8803, 2.7207, 5.9910, 3.4135), .Dim=c(2,3)),
    ST_DevM_VVL_DDP_previous_npt=structure(.Data=c(6.4427, 2.7710, 4.5403, 2.9566, 4.5498, 3.6371), .Dim=c(2,3)),

    ST_DevL_VVH_DDP_previous_npt=structure(.Data=c(29.0140, 2.4546, 21.5491, 3.3479, 9.4293, 2.5205), .Dim=c(2,3)),
    ST_DevL_VVM_DDP_previous_npt=structure(.Data=c(10.3286, 2.6785, 50.2210, 2.1903, 5.1108, 2.6217), .Dim=c(2,3)),
    ST_DevL_VVL_DDP_previous_npt=structure(.Data=c(5.8949, 2.2929, 3.9427, 2.3282, 3.9133, 2.8338), .Dim=c(2,3)),

    # posterior probability of Dev/V&V qualities in ST phase
    # ST_DevH=0, ST_DevM=0.99, ST_DevL=0.01,
    # ST_VVH=0, ST_VVM=0, ST_VVL = 1,

    # number of function points (same in all phases)
    ST_FP=56,
    generic_ST_FP=50,


    # Dev Attribute model - Installation & Checkout phase

    # node probability tables of attribute: P(attribute state|Dev=H/M/L)
    # Dimension: row, col
    # row represents attribute states (H/M/L), column represents mu and sigma
    # (1,1) (2,1) (1,2) (2,2) (1,3) (2,3)
    IC_IPG_DevH_npt=structure(.Data=c(0.850, 0.112, 0.140, 0.089, 0.010, 0.022), .Dim=c(2,3)),
    IC_IPG_DevM_npt=structure(.Data=c(0.210, 0.124, 0.630, 0.164, 0.160, 0.065), .Dim=c(2,3)),
    IC_IPG_DevL_npt=structure(.Data=c(0.056, 0.100, 0.194, 0.131, 0.750, 0.224), .Dim=c(2,3)),

    IC_IaC_DevH_npt=structure(.Data=c(0.800, 0.137, 0.180, 0.110, 0.020, 0.027), .Dim=c(2,3)),
    IC_IaC_DevM_npt=structure(.Data=c(0.200, 0.122, 0.650, 0.150, 0.150, 0.050), .Dim=c(2,3)),
    IC_IaC_DevL_npt=structure(.Data=c(0.046, 0.103, 0.184, 0.123, 0.770, 0.217), .Dim=c(2,3)),

    IC_HA_DevH_npt=structure(.Data=c(0.670, 0.144, 0.290, 0.124, 0.040, 0.022), .Dim=c(2,3)),
    IC_HA_DevM_npt=structure(.Data=c(0.140, 0.055, 0.640, 0.089, 0.220, 0.084), .Dim=c(2,3)),
    IC_HA_DevL_npt=structure(.Data=c(0.020, 0.027, 0.210, 0.102, 0.770, 0.125), .Dim=c(2,3)),

    IC_SA_DevH_npt=structure(.Data=c(0.670, 0.144, 0.290, 0.124, 0.040, 0.022), .Dim=c(2,3)),
    IC_SA_DevM_npt=structure(.Data=c(0.150, 0.071, 0.620, 0.110, 0.230, 0.084), .Dim=c(2,3)),
    IC_SA_DevL_npt=structure(.Data=c(0.030, 0.027, 0.220, 0.110, 0.750, 0.137), .Dim=c(2,3)),

    IC_RA_DevH_npt=structure(.Data=c(0.690, 0.201, 0.250, 0.150, 0.060, 0.082), .Dim=c(2,3)),
    IC_RA_DevM_npt=structure(.Data=c(0.280, 0.349, 0.540, 0.261, 0.180, 0.130), .Dim=c(2,3)),
    IC_RA_DevL_npt=structure(.Data=c(0.200, 0.392, 0.180, 0.110, 0.620, 0.368), .Dim=c(2,3)),

    # state of attribute: 1 -> High, 2 -> Medium, 3 -> Low
    IC_IPG_state=2, IC_IaC_state=2, IC_HA_state=2, IC_SA_state=2, IC_RA_state=2,
    generic_IC_IPG_state=2, generic_IC_IaC_state=2, generic_IC_HA_state=2, generic_IC_SA_state=2, generic_IC_RA_state=2,


    # V&V Attribute model - Installation & Checkout phase

    # node probability tables of attribute: P(attribute state|VV=H/M/L)
    # Dimension: row, col
    # row represents attribute states (H/M/L), column represents mu and sigma
    # (1,1) (2,1) (1,2) (2,2) (1,3) (2,3)
    IC_ICAVV_VVH_npt=structure(.Data=c(0.700, 0.112, 0.260, 0.089, 0.040, 0.022), .Dim=c(2,3)),
    IC_ICAVV_VVM_npt=structure(.Data=c(0.200, 0.122, 0.610, 0.124, 0.190, 0.074), .Dim=c(2,3)),
    IC_ICAVV_VVL_npt=structure(.Data=c(0.066, 0.095, 0.234, 0.126, 0.700, 0.209), .Dim=c(2,3)),

    IC_ICVV_VVH_npt=structure(.Data=c(0.800, 0.137, 0.180, 0.110, 0.020, 0.027), .Dim=c(2,3)),
    IC_ICVV_VVM_npt=structure(.Data=c(0.200, 0.122, 0.650, 0.150, 0.150, 0.050), .Dim=c(2,3)),
    IC_ICVV_VVL_npt=structure(.Data=c(0.056, 0.100, 0.194, 0.131, 0.750, 0.224), .Dim=c(2,3)),

    IC_HAVV_VVH_npt=structure(.Data=c(0.670, 0.144, 0.290, 0.124, 0.040, 0.022), .Dim=c(2,3)),
    IC_HAVV_VVM_npt=structure(.Data=c(0.170, 0.067, 0.620, 0.110, 0.210, 0.074), .Dim=c(2,3)),
    IC_HAVV_VVL_npt=structure(.Data=c(0.060, 0.082, 0.220, 0.110, 0.720, 0.175), .Dim=c(2,3)),

    IC_SAVV_VVH_npt=structure(.Data=c(0.670, 0.144, 0.290, 0.124, 0.040, 0.022), .Dim=c(2,3)),
    IC_SAVV_VVM_npt=structure(.Data=c(0.170, 0.067, 0.620, 0.110, 0.210, 0.074), .Dim=c(2,3)),
    IC_SAVV_VVL_npt=structure(.Data=c(0.060, 0.082, 0.220, 0.110, 0.720, 0.175), .Dim=c(2,3)),

    IC_RAVV_VVH_npt=structure(.Data=c(0.720, 0.175, 0.250, 0.150, 0.030, 0.027), .Dim=c(2,3)),
    IC_RAVV_VVM_npt=structure(.Data=c(0.310, 0.336, 0.520, 0.259, 0.170, 0.120), .Dim=c(2,3)),
    IC_RAVV_VVL_npt=structure(.Data=c(0.230, 0.383, 0.180, 0.110, 0.590, 0.371), .Dim=c(2,3)),

    IC_VVASRG_VVH_npt=structure(.Data=c(0.700, 0.112, 0.260, 0.089, 0.040, 0.022), .Dim=c(2,3)),
    IC_VVASRG_VVM_npt=structure(.Data=c(0.220, 0.110, 0.610, 0.124, 0.170, 0.045), .Dim=c(2,3)),
    IC_VVASRG_VVL_npt=structure(.Data=c(0.076, 0.089, 0.274, 0.102, 0.650, 0.177), .Dim=c(2,3)),

    IC_VVFRG_VVH_npt=structure(.Data=c(0.700, 0.112, 0.260, 0.089, 0.040, 0.022), .Dim=c(2,3)),
    IC_VVFRG_VVM_npt=structure(.Data=c(0.220, 0.110, 0.610, 0.124, 0.170, 0.045), .Dim=c(2,3)),
    IC_VVFRG_VVL_npt=structure(.Data=c(0.076, 0.089, 0.274, 0.102, 0.650, 0.177), .Dim=c(2,3)),

    # state of attribute: 1 -> High, 2 -> Medium, 3 -> Low
    IC_ICAVV_state=2, IC_ICVV_state=2, IC_HAVV_state=2, IC_SAVV_state=2, IC_RAVV_state=2, IC_VVASRG_state=2, IC_VVFRG_state=2,
    generic_IC_ICAVV_state=2, generic_IC_ICVV_state=2, generic_IC_HAVV_state=2, generic_IC_SAVV_state=2, generic_IC_RAVV_state=2, generic_IC_VVASRG_state=2, generic_IC_VVFRG_state=2,


    # Submodel - Installation & Checkout phase

    # node probability tables of DDP_current: P(DDP_current|VV=H/M/L)
    # Dimension: row, col
    # row represents Complexity (H/M/L), column represents alpha and beta
    # (1,1) (2,1) (1,2) (2,2) (1,3) (2,3)
    IC_VVH_DDP_current_npt=structure(.Data=c(5.384, 2.365, 12.448, 1.775, 12.356, 1.037), .Dim=c(2,3)),
    IC_VVM_DDP_current_npt=structure(.Data=c(2.740, 1.900, 4.483, 1.730, 6.000, 1.458), .Dim=c(2,3)),
    IC_VVL_DDP_current_npt=structure(.Data=c(2.205, 3.069, 2.934, 3.080, 4.015, 3.324), .Dim=c(2,3)),

    # node probability tables of DDP_previous: P(DDP_previous|VV=H/M/L)
    # Dimension: row, col
    # row represents Complexity (H/M/L), column represents alpha and beta
    # (1,1) (2,1) (1,2) (2,2) (1,3) (2,3)
    IC_VVH_DDP_previous_npt=structure(.Data=c(3.2360, 1.7659, 6.2600, 1.5622, 13.8766, 1.4457), .Dim=c(2,3)),
    IC_VVM_DDP_previous_npt=structure(.Data=c(1.6810, 1.5003, 2.2365, 1.3126, 3.1949, 1.3703), .Dim=c(2,3)),
    IC_VVL_DDP_previous_npt=structure(.Data=c(0.8258, 1.3336, 0.8505, 1.0864, 0.9799, 1.0904), .Dim=c(2,3)),

    # posterior probability of Dev/V&V qualities in IC phase
    # IC_DevH=0.01, IC_DevM=0.99, IC_DevL=0,
    # IC_VVH=0, IC_VVM=1, IC_VVL=0,

    # number of function points (same in all phases)
    IC_FP=56,
    generic_IC_FP=50
)
