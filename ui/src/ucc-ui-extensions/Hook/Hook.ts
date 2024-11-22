import {
  AcceptableFormValueOrNullish,
  BaseFormState,
  UtilBaseForm,
} from "../../utils/types.ts";
import { Mode } from "../../utils/modes.ts";
import { debounce, invariant } from "es-toolkit";

type DataDict = Record<string, AcceptableFormValueOrNullish>;

class Hook {
  globalConfig: object;
  serviceName: string;
  state: BaseFormState;
  mode: Mode;
  util: UtilBaseForm;
  groupName: string;
  _debouncedNameChange = debounce(this._nameChange.bind(this), 200);

  constructor(
    globalConfig: object,
    serviceName: string,
    state: BaseFormState,
    mode: Mode,
    util: UtilBaseForm,
    groupName: string,
  ) {
    this.globalConfig = globalConfig;
    this.serviceName = serviceName;
    this.state = state;
    this.mode = mode;
    this.util = util;
    this.groupName = groupName;
    console.log("Inside Hook mode: ", mode);
  }

  onCreate() {
    if (this.mode === "create") {
      console.log("in Hook: onCreate");
      this.util.setState((prevState: BaseFormState) => {
        const data = {
          ...prevState.data,
          test_field: { value: this.groupName },
        };
        return { data };
      });
    }
  }

  onChange(
    field: string,
    value: AcceptableFormValueOrNullish,
    newState: BaseFormState,
  ) {
    console.log("in Hook: onChange ", field, " value : ", value);
    console.log("in Hook: onChange state: ", this.state);
    if (field === "name") {
      this._debouncedNameChange(newState);
    }
  }

  onRender() {
    console.log("in Hook: onRender");
  }

  async onSave(dataDict: DataDict) {
    console.log("in Hook: onSave with data: ", dataDict);
    const { name: accountname, auth_type, url: endpoint } = dataDict;

    this.util.setState((prevState: BaseFormState) =>
      this.util.clearAllErrorMsg(prevState),
    );

    try {
      invariant(
        typeof accountname === "string" && accountname.trim(),
        "Field account name is required and must be a string",
      );
      invariant(
        typeof endpoint === "string" && endpoint.trim(),
        "Field URL is required and must be a string",
      );
      invariant(
        endpoint.startsWith("https://"),
        "URL should start with 'https://' as only secure URLs are supported.",
      );

      if (auth_type === "oauth") {
        this.util.setState((prevState: BaseFormState) => {
          const data = {
            ...prevState.data,
            endpoint: { value: endpoint.replace("https://", "") },
          };
          return { data };
        });
      }
      return true;
    } catch (error) {
      if (error instanceof Error) {
        this.util.setErrorMsg(error.message);
      } else {
        this.util.setErrorMsg("An unknown error occurred");
      }
      return false;
    }
  }

  onSaveSuccess() {
    console.log("in Hook: onSaveSuccess");
  }

  onSaveFail() {
    console.log("in Hook: onSaveFail");
  }

  onEditLoad() {
    console.log("in Hook: onEditLoad");
  }

  _nameChange(newState: BaseFormState) {
    console.log("in Hook: _nameChange", newState);
  }
}

export default Hook;
