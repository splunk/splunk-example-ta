import { getDefaultFetchInit } from "@splunk/splunk-utils/fetch";
import { createRESTURL } from "@splunk/splunk-utils/url";
import { ResponseError } from "./ResponseError";

type ParamsRecord = Record<string, string | number | undefined>;

export interface RequestParams {
  endpointUrl: string;
  params?: ParamsRecord;
  signal?: AbortSignal;
  body?: BodyInit;
}

const DEFAULT_PARAMS = { output_mode: "json" };

function createUrl(endpointUrl: string, params: ParamsRecord): URL {
  const url = new URL(createRESTURL(endpointUrl), window.location.origin);
  Object.entries({ ...DEFAULT_PARAMS, ...params })
    .filter(([, value]) => value !== undefined && value !== null)
    .forEach(([key, value]) => url.searchParams.append(key, value.toString()));
  return url;
}

function handleErrorResponse(response: Response) {
  if (!response.ok) {
    throw new ResponseError({ response, message: "Something went wrong" });
  }
}

async function fetchWithErrorHandling<TData>(
  url: URL,
  options: RequestInit,
): Promise<TData> {
  const defaultInit = getDefaultFetchInit();

  const response = await fetch(url.toString(), {
    ...defaultInit,
    ...options,
  });

  handleErrorResponse(response);

  return await response.json();
}

export async function getRequest<TData>({
  endpointUrl,
  params = {},
  signal,
}: RequestParams) {
  const url = createUrl(endpointUrl, params);
  const options = {
    method: "GET",
    signal,
  } satisfies RequestInit;

  return fetchWithErrorHandling<TData>(url, options);
}

export async function postRequest<TData>({
  endpointUrl,
  params = {},
  body,
  signal,
}: RequestParams) {
  const url = createUrl(endpointUrl, params);
  const defaultInit = getDefaultFetchInit();
  const headers = {
    ...defaultInit.headers,
    "Content-Type": "application/x-www-form-urlencoded",
  } satisfies HeadersInit;

  const options = {
    method: "POST",
    headers,
    signal,
    body,
  } satisfies RequestInit;

  return fetchWithErrorHandling<TData>(url, options);
}

export async function deleteRequest<TData>({
  endpointUrl,
  params = {},
  signal,
}: RequestParams) {
  const url = createUrl(endpointUrl, params);

  const options = {
    method: "DELETE",
    signal,
  } satisfies RequestInit;

  return fetchWithErrorHandling<TData>(url, options);
}
