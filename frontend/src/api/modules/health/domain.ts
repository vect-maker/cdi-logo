import { z } from "zod";

export const HealthStatusSchema = z.enum(["ok", "degraded", "down"]);
