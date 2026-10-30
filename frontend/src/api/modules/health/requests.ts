import { z } from "zod";

export const HealthCheckRequestSchema = z.object({
  verbose: z.boolean().optional(),
});
