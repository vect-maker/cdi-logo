import type { z } from "zod";
import type { HealthStatusSchema } from "./domain";
import type { HealthCheckRequestSchema } from "./requests";
import type { HealthResponseSchema } from "./responses";

export type HealthStatus = z.infer<typeof HealthStatusSchema>;
export type HealthCheckRequest = z.infer<typeof HealthCheckRequestSchema>;
export type HealthResponse = z.infer<typeof HealthResponseSchema>;
