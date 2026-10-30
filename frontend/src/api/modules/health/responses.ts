import { z } from "zod";
import { HealthStatusSchema } from "./domain";

export const HealthResponseSchema = z.object({
  status: HealthStatusSchema.or(z.string()),
  app: z.string().optional(),
  round: z.number().int().optional(),
  database: z.string().optional(),
});
