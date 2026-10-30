import { useApiFetch } from "../../useApiFetch";
import { HealthResponseSchema } from "./responses";
import type { HealthResponse } from "./types";

export const useHealthApi = () => {
  /**
   * Check FastAPI backend health and database connectivity.
   */
  async function getHealth(): Promise<HealthResponse> {
    const { data, error } = await useApiFetch("/health").get().json();
    if (error.value || !data.value) {
      throw error.value ?? new Error("Health check failed");
    }
    return HealthResponseSchema.parse(data.value);
  }

  return {
    getHealth,
  };
};
