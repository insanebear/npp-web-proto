export interface SimulationMetric {
    mean?: number;
    sd?: number;
    median?: number;
    q5?: number;
    q95?: number;
    // TODO: remove legacy keys once all stored results are migrated to q5/q95
    q2_5?: number;
    q97_5?: number;
    [key: string]: number | undefined;
}

export interface SimulationInput {
    [tabName: string]: Record<string, string | number | boolean> | undefined;
    settings?: {
        nChains?: number;
        nIter?: number;
        nBurnin?: number;
        nThin?: number;
        workingDir?: string;
        includeTraceData?: boolean;
    };
}

export interface SimulationOutput {
    PFD?: SimulationMetric;
    SR_Total_Remained_Defect?: SimulationMetric;
    SD_Total_Remained_Defect?: SimulationMetric;
    IM_Total_Remained_Defect?: SimulationMetric;
    ST_Total_Remained_Defect?: SimulationMetric;
    IC_Total_Remained_Defect?: SimulationMetric;
    traces?: number[];
    __rawText?: string;
    [key: string]: SimulationMetric | unknown;
}

export interface SimulationResults {
    input: SimulationInput;
    output: SimulationOutput;
    __rawText?: string;
}

export interface PfdUpdateResult {
    input?: {
      bbn_input?: {
        source: string;
        bucket?: string;
        key?: string;
        description?: string;
        size?: number;
        path?: string;
      };
      [key: string]: unknown;
    };
    output?: unknown;
    [key: string]: unknown;
}