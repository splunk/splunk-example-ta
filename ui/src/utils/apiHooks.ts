import { getRequest, RequestParams } from "./api.ts";
import { useEffect, useState } from "react";
import { isPlainObject } from "es-toolkit";

/**
 * Hashes the request parameters to use as a key in the cache.
 * @param params
 */
function hashParams(params: RequestParams): string {
  const url = params.endpointUrl;
  const requestParams = params.params;

  const paramsHash = JSON.stringify(requestParams, (_, val) =>
    isPlainObject(val)
      ? Object.keys(val)
          .sort()
          .reduce(
            (result, key) => {
              result[key] = val[key];
              return result;
            },
            {} as Record<string, unknown>,
          )
      : val,
  );

  return `${url}::${paramsHash ?? ""}`;
}

const cache = new Map<string, RequestParams>();

export function useGetRequest<TData>(params: RequestParams) {
  const [data, setData] = useState<TData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isLoaded, setIsLoaded] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  // params is a new object on every render
  // hashing is used to preserve a reference to the params object
  const hash = hashParams(params);
  if (!cache.has(hash)) {
    cache.set(hash, params);
  }
  const cachedParams = cache.get(hash) ?? params;

  useEffect(() => {
    let isMounted = true;
    const abortController = new AbortController();

    getRequest<TData>({ signal: abortController.signal, ...cachedParams })
      .then((data) => {
        if (isMounted) {
          setData(data);
          setIsLoaded(true);
          setIsLoading(false);
        }
      })
      .catch((error) => {
        if (isMounted) {
          setError(error);
          setIsLoading(false);
        }
      });

    return () => {
      isMounted = false;
      abortController.abort();
    };
  }, [cachedParams]);

  return { data, isLoading, isLoaded, error };
}
