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

type ValueSetter = (newValue: AcceptableFormValueOrNullish) => void;

export abstract class CustomControlBase {
  public globalConfig: object;
  public el: HTMLElement;
  public data: ControlData;
  public setValue: ValueSetter;
  public util: UtilBaseForm;

  protected constructor(
    globalConfig: object,
    el: HTMLElement,
    data: ControlData,
    setValue: ValueSetter,
    util: UtilBaseForm,
  ) {
    this.globalConfig = globalConfig;
    this.el = el;
    this.data = data;
    this.setValue = setValue;
    this.util = util;
  }

  render?(): void;

  validation?(field: string, value: ControlData["value"]): string | undefined;
}
