import { setupServer } from "msw/node";

export const server = setupServer();

server.listen({
  onUnhandledRequest: "warn",
});
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

process.once("SIGINT", () => server.close());
process.once("SIGTERM", () => server.close());
