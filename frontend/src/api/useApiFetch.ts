import { createFetch } from "@vueuse/core";
import { ErrorPayloadSchema } from "./modules/shared/schemas";

const getBaseUrl = (): string => {
  if (typeof import.meta !== "undefined" && import.meta.env?.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL;
  }
  if (typeof globalThis !== "undefined" && "process" in globalThis) {
    const proc = (globalThis as unknown as { process?: { env?: Record<string, string> } }).process;
    if (proc?.env?.VITE_API_BASE_URL) {
      return proc.env.VITE_API_BASE_URL;
    }
  }
  return "http://localhost:8000";
};

const API_BASE_URL = getBaseUrl();

function normalizeHeaders(headersInit: HeadersInit | undefined): Record<string, string> {
  if (!headersInit) return {};
  if (headersInit instanceof Headers) {
    return Object.fromEntries(headersInit.entries());
  }
  if (Array.isArray(headersInit)) {
    return Object.fromEntries(headersInit);
  }
  return { ...headersInit };
}

export const useApiFetch = createFetch({
  baseUrl: API_BASE_URL,
  options: {
    updateDataOnError: true,
    async beforeFetch({ options }) {
      const headers = normalizeHeaders(options.headers);
      if (!headers["Content-Type"]) {
        headers["Content-Type"] = "application/json";
      }
      options.headers = headers;
      return { options };
    },
    async onFetchError(ctx) {
      if (ctx.data) {
        const parsed = ErrorPayloadSchema.safeParse(ctx.data);
        if (parsed.success && parsed.data.message) {
          ctx.error = new Error(parsed.data.message);
        }
      }
      return ctx;
    },
  },
  fetchOptions: {
    mode: "cors",
  },
});
