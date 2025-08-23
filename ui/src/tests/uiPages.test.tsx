import { screen, waitForElementToBeRemoved } from "@testing-library/react";
import { it, expect, vi } from "vitest";
import { http, HttpResponse } from "msw";
import { renderConfigurationPage, renderInputsPage } from "@splunk/add-on-ucc-framework";
import userEvent from "@testing-library/user-event";

import { getGlobalConfig } from "./utils";
import { server } from "../../tests/mocks/server";
import AdvancedInputsTabClass from "../ucc-ui-extensions/AdvancedInputsTab";
import DateInputClass from "../ucc-ui-extensions/DateInput";
import { mockServerResponseWithContent } from "../../tests/mocks/serverData";

function mockResponse() {
  server.use(
    http.get(`/servicesNS/nobody/-/:endpointUrl/:serviceName`, () => {
      console.log("Mocking server response for endpoint serviceName");
      return HttpResponse.json(mockServerResponseWithContent);
    }),
    http.get(`/servicesNS/nobody/-/:endpointUrl`, () => {
      console.log("Mocking server response for endpoint endpointUrl");
      return HttpResponse.json(mockServerResponseWithContent);
    })
  );
}

vi.mock("@splunk/splunk-utils/themes", () => ({
  getUserTheme: () => Promise.resolve("light"),
}));

vi.mock("@splunk/search-job", () => {
  console.log("2 Mocking @splunk/search-job", "cloud");

  const create = () => ({
    getResults: () => ({
      subscribe: (
        callbackFunction: (params: {
          results: { instance_type: string }[];
        }) => void
      ) => {
        console.log("2 Search job results:", "cloud");
        callbackFunction({ results: [{ instance_type: "cloud" }] });
        return { unsubscribe: () => {} };
      },
    }),
  });

  // Return both the named export and default export
  return {
    create,
    default: { create }, // Add this default export
  };
});

it("Should open account addition form", async () => {
  vi.spyOn(console, "error").mockImplementation(console.log);
  mockResponse();
  renderConfigurationPage(getGlobalConfig(), {
    DateInput: {
      component: DateInputClass,
      type: "control",
    },
    AdvancedInputsTab: {
      component: AdvancedInputsTabClass,
      type: "tab",
    },
  });

  await waitForElementToBeRemoved(() => screen.getByText("Waiting"));

  expect(screen.getByText("Configuration")).toBeInTheDocument();
  const data = await screen.findByText("Mocked Input name");
  expect(data).toBeInTheDocument();
  const newInput = screen.getByRole("button", {
    name: "Add",
  });
  expect(newInput).toBeInTheDocument();

  await userEvent.click(newInput);
  expect(await screen.findByText("Add Accounts")).toBeInTheDocument();
});

it("Should open inputs addition form", async () => {
  vi.spyOn(console, 'error').mockImplementation(() => {})
  mockResponse();
  renderInputsPage(getGlobalConfig(), {
    DateInput: {
      component: DateInputClass,
      type: "control",
    },
    AdvancedInputsTab: {
      component: AdvancedInputsTabClass,
      type: "tab",
    },
  });

  await waitForElementToBeRemoved(() => screen.getByText("Waiting"));

  expect(screen.getByText("Inputs")).toBeInTheDocument();
  const data = await screen.findByText("Mocked Input name");
  expect(data).toBeInTheDocument();
  const newInput = screen.getByRole("button", {
    name: "Create New Input",
  });
  expect(newInput).toBeInTheDocument();

  await userEvent.click(newInput);
  expect(await screen.findByText("Add example")).toBeInTheDocument();
});
