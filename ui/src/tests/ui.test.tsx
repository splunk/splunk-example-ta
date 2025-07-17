import { screen, waitForElementToBeRemoved } from "@testing-library/react";
import { it, expect, vi } from "vitest";
import { http, HttpResponse } from "msw";

import { renderConfigurationPage } from "@splunk/add-on-ucc-framework";
import { getGlobalConfig } from "./utils";
import { server } from "../../tests/mocks/server";
import { mockServerResponseWithContent } from "../../tests/mocks/serverData";
import AdvancedInputsTabClass from "../ucc-ui-extensions/AdvancedInputsTab";
import DateInputClass from "../ucc-ui-extensions/DateInput";

function mockResponse() {
  server.use(
    http.get(`/servicesNS/nobody/-/:endpointUrl/:serviceName`, () =>
      HttpResponse.json(mockServerResponseWithContent)
    ),
    http.get(`/servicesNS/nobody/-/:endpointUrl`, () =>
      HttpResponse.json(mockServerResponseWithContent)
    )
  );
}

it("should show UCC label 2", async () => {
  vi.spyOn(console, "error").mockImplementation(console.log);
  mockResponse();
  const container = renderConfigurationPage(getGlobalConfig(), {
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
  const data = await screen.findByText(
    "Mocked Input name",
    {},
    { timeout: 5000 }
  );
  expect(data).toBeInTheDocument();
}, 6000);
