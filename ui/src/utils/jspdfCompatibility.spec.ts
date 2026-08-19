import { exportDataUrisToPdfDataUri } from "@splunk/dashboard-utils";

const PNG_DATA_URI =
  "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=";

describe("jsPDF compatibility", () => {
  it("supports the PDF export operations used by dashboard-utils", () => {
    const result = exportDataUrisToPdfDataUri({
      pages: [
        {
          clientWidth: 1,
          clientHeight: 1,
          dataUri: PNG_DATA_URI,
        },
      ],
    });

    expect(result).toMatch(
      /^data:application\/pdf;filename=generated\.pdf;base64,/,
    );
  });
});
