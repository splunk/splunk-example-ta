import { screen, render } from "@testing-library/react";
import React from "react";
import { AdvancedInputsTab } from "./AdvancedInputsTab.tsx";
import { server } from "../../../tests/mocks/server.ts";
import { http, HttpResponse } from "msw";

jest.mock("@splunk/splunk-utils/config", () => ({
  ...jest.requireActual("@splunk/splunk-utils/config"),
  app: "test_app",
}));

function setup() {
  return render(<AdvancedInputsTab />);
}

function mockResponse(errorResponse: Response) {
  server.use(
    http.get(`/servicesNS/-/test_app/test_app_example`, () => {
      return errorResponse;
    }),
  );
}

describe("AdvancedInputsTab", () => {
  it("should render table", async () => {
    const response = HttpResponse.json({
      entry: [
        {
          name: "test_name",
          content: {
            account: "test",
            disabled: false,
            fetch_from: "test",
            index: "test",
            interval: 123,
          },
        },
      ],
    });

    mockResponse(response);
    const { findByRole } = setup();

    expect(await findByRole("table")).toBeInTheDocument();
    expect(await findByRole("cell", { name: "test_name" })).toBeInTheDocument();
  });

  it("should render error message", async () => {
    const serverErrorMessage = "Internal error";
    const errorResponse = HttpResponse.json(
      { message: serverErrorMessage },
      { status: 500 },
    );
    mockResponse(errorResponse);
    setup();

    expect(await screen.findByText("Something went wrong")).toBeInTheDocument();
    expect(screen.queryByText(serverErrorMessage)).not.toBeInTheDocument();
  });
});
