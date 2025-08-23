export const MOCKED_TA_NAME = "Splunk_TA_Example";
export const MOCKED_TA_INPUT = "account";

export const mockServerResponseWithContent = {
  links: {
    create: `/servicesNS/nobody/Splunk_TA_Example/account/_new`,
  },
  updated: "2023-08-21T11:54:12+00:00",
  entry: [
    {
      id: 1,
      name: "Mocked Input name",
      content: {
        disabled: true,
        fields1: "value1",
        fields2: "value2",
      },
    },
  ],
  messages: [],
};
