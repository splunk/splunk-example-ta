import { Mode } from "./modes.ts";

export type AcceptableFormValue =
  | string
  | number
  | boolean
  | { fileContent?: string };
export type AcceptableFormValueOrNull = AcceptableFormValue | null;
export type AcceptableFormValueOrNullish =
  | AcceptableFormValueOrNull
  | undefined;

export type AcceptableFormRecord = Record<string, AcceptableFormValueOrNull>;

export type StandardPages = "configuration" | "inputs";

export interface BaseFormStateData {
  [x: string]: {
    disabled: boolean;
    error: boolean;
    fileNameToDisplay?: string;
    value?: AcceptableFormValueOrNullish;
    display: boolean;
    markdownMessage?: unknown;
    dependencyValues?: string;
    modifiedEntitiesData?: {
      help?: string;
      label?: string;
      required?: boolean;
    };
  };
}

export interface BaseFormState {
  serviceName?: string;
  mode?: Mode;
  page?: StandardPages;
  stanzaName?: string;
  data: BaseFormStateData;
  errorMsg?: string;
  warningMsg?: string;
  stateModified?: boolean;
}

export interface UtilBaseForm {
  setState: (callback: (prevState: BaseFormState) => void) => void;
  setErrorFieldMsg: (field: string, msg: string) => void;
  clearAllErrorMsg: (State: BaseFormState) => unknown;
  setErrorMsg: (msg: string) => void;
}

export interface ControlData {
  value: AcceptableFormValueOrNullish;
  mode: Mode;
  serviceName: string;
}
