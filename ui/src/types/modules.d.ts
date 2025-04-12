declare module "@splunk/splunk-utils/config" {
  export const CSRFToken: string | null;
  export function getCSRFToken(): string | null;
  export const isAvailable: boolean;
  export function extractAppName(pathname?: string): string | undefined;
  export const app: string | undefined;
  export const appBuild: string | undefined;
  export const buildNumber: number | undefined;
  export const buildPushNumber: number | undefined;
  export const config: Record<string, unknown> | undefined;
  export const locale: string | undefined;
  export const portNumber: number | undefined;
  export const rootPath: string | undefined;
  export const serverTimezoneInfo: string | undefined;
  export const splunkdPath: string | undefined;
  export const username: string | undefined;
  export const versionLabel: string | undefined;
}
